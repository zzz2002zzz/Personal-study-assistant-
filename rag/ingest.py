"""
RAG ingestion: load the PM notes corpus (20 PDF files), extract text,
chunk it, embed with a local sentence-transformers model, and persist to
a Chroma vector store.

Chunking strategy
------------------
Each PDF is generated with an explicit "SECTION: <heading>" marker at the
start of every topic/term inside it (visible as a bold sub-heading in the
PDF, but also present as literal text in the extracted content stream).
We split the extracted text on those markers so a chunk never crosses a
topic boundary halfway - the PDF equivalent of splitting a markdown file
on "## " headers.

Within a section, if it is longer than CHUNK_WORDS words, a sliding
window (CHUNK_WORDS words, OVERLAP_WORDS overlap) further splits it so a
single fact/formula is never cut exactly in half at a chunk boundary.

Every chunk is prefixed with "[filename | section heading]" before being
embedded, so the embedding captures topic + content together, which
measurably improves retrieval precision for short queries.

PDF text extraction: pypdf (pure Python, no external system
dependencies - important for Streamlit Community Cloud's free tier).

Embedding model: sentence-transformers/all-MiniLM-L6-v2 (free, local,
384-dim, fast enough to embed the whole corpus in seconds on CPU).

Vector store: Chroma (persistent, local directory on disk).
"""

import os
import re
import glob
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

CORPUS_DIR = os.path.join(os.path.dirname(__file__), "..", "corpus_pdf")
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
COLLECTION_NAME = "pm_notes"

CHUNK_WORDS = 180
OVERLAP_WORDS = 40

SECTION_MARKER = "SECTION:"


def extract_pdf_text(filepath: str) -> str:
    reader = PdfReader(filepath)
    pages_text = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages_text)


def split_into_sections(text: str):
    """Split extracted PDF text into (heading, body) tuples on 'SECTION:' markers."""
    parts = re.split(rf"\n(?=\s*{SECTION_MARKER} )", text)
    sections = []
    for part in parts:
        part = part.strip()
        if not part.startswith(SECTION_MARKER):
            # This is the document title / preamble before the first
            # SECTION marker - not a chunkable section on its own.
            continue
        first_line, _, rest = part.partition("\n")
        heading = first_line.replace(SECTION_MARKER, "", 1).strip()
        body = rest.strip()
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
    files = sorted(glob.glob(os.path.join(CORPUS_DIR, "*.pdf")))
    for filepath in files:
        filename = os.path.basename(filepath)
        text = extract_pdf_text(filepath)
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