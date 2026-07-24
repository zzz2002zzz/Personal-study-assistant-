"""
Retrieval interface used by Agent 2 (Answerer). Lazily builds/loads the
Chroma collection once per process and exposes a simple retrieve(query, k)
function returning the top-k most similar note chunks.
"""

from rag.ingest import build_or_load_vectorstore

_collection = None


def get_collection():
    global _collection
    if _collection is None:
        _collection = build_or_load_vectorstore()
    return _collection


def retrieve(query: str, k: int = 4):
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=k)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]
    return [
        {"text": d, "source": m["source"], "heading": m["heading"], "distance": dist}
        for d, m, dist in zip(docs, metas, distances)
    ]
