"""
RAG ingestion: load the PM notes corpus, chunk it, embed with a local
sentence-transformers model, and persist to a Chroma vector store.

Chunking strategy
------------------
Each note file is organised around markdown '## ' section headers (one
per PM sub-topic, e.g. "Risk Response Strategies"). We first split each
file on those headers so a chunk never crosses a topic boundary halfway.
Within a section, if the section is longer than CHUNK_WORDS words, we
apply a sliding window (CHUNK_WORDS words, OVERLAP_WORDS overlap) so a
single fact/formula is never cut in half exactly at a chunk boundary.

Every chunk is prefixed with "[filename | section heading]" before being
embedded. This means the embedding captures topic context *and* content,
which noticeably improves retrieval precision for short queries like
"what is scope creep" versus embedding raw body text alone.

Embedding model: sentence-transformers/all-MiniLM-L6-v2
  - Free, runs locally (no API cost/latency for embeddings).
  - 384-dim, fast enough to embed the whole corpus in seconds on CPU,
    which matters for Streamlit Community Cloud's free-tier compute.

Vector store: Chroma (persistent, local directory on disk)
  - Zero-cost, no external service/account needed, works fine for a
    single-user demo app deployed on Streamlit Cloud.
"""

import os
import re
import glob
import chromadb
from chromadb.utils import embedding_functions

CORPUS_DIR = os.path.join(os.path.dirname(__file__), "..", "corpus")
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
COLLECTION_NAME = "pm_notes"

CHUNK_WORDS = 180
OVERLAP_WORDS = 40


def split_into_sections(text: str):
    """Split a markdown file into (heading, body) tuples on '## ' headers."""
    parts = re.split(r"\n(?=## )", text)
    sections = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        lines = part.split("\n", 1)
        heading = lines[0].lstrip("#").strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        if body:
            sections.append((heading, body))
    return sections


def sliding_window_chunks(words, size=CHUNK_WORDS, overlap=OVERLAP_WORDS):
    if len(words) <= size:
        return [" ".join(words)]
    chunks = []
    step = size - overlap
    for start in range(0, len(words), step):
        window = words[start:start + size]
        if not window:
            break
        chunks.append(" ".join(window))
        if start + size >= len(words):
            break
    return chunks


def build_chunks():
    chunks, metadatas, ids = [], [], []
    files = sorted(glob.glob(os.path.join(CORPUS_DIR, "*.md")))
    for filepath in files:
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        sections = split_into_sections(text)
        for sec_idx, (heading, body) in enumerate(sections):
            words = body.split()
            for chunk_idx, chunk_text in enumerate(sliding_window_chunks(words)):
                chunk_id = f"{filename}::{sec_idx}::{chunk_idx}"
                prefixed = f"[{filename} | {heading}]\n{chunk_text}"
                chunks.append(prefixed)
                metadatas.append({"source": filename, "heading": heading})
                ids.append(chunk_id)
    return chunks, metadatas, ids


def get_embedding_function():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )


def build_or_load_vectorstore(force_rebuild: bool = False):
    client = chromadb.PersistentClient(path=DB_DIR)
    ef = get_embedding_function()

    existing = [c.name for c in client.list_collections()]

    if COLLECTION_NAME in existing and force_rebuild:
        client.delete_collection(COLLECTION_NAME)
        existing.remove(COLLECTION_NAME)

    if COLLECTION_NAME in existing:
        return client.get_collection(COLLECTION_NAME, embedding_function=ef)

    collection = client.create_collection(COLLECTION_NAME, embedding_function=ef)
    chunks, metadatas, ids = build_chunks()
    batch = 100  # Chroma batch-add limit safety margin
    for i in range(0, len(chunks), batch):
        collection.add(
            documents=chunks[i:i + batch],
            metadatas=metadatas[i:i + batch],
            ids=ids[i:i + batch],
        )
    return collection


if __name__ == "__main__":
    col = build_or_load_vectorstore(force_rebuild=True)
    print(f"Ingested {col.count()} chunks into '{COLLECTION_NAME}'.")
