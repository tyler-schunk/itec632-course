"""
Hybrid retrieval (Ch. 6): BM25 term matching + embedding similarity, fused with
reciprocal rank fusion (RRF).

    from coapp.retrieve import build_index, retrieve
    index = build_index(docs)                  # docs from itec632.corpus.load_docs()
    chunks = retrieve(index, "What does server management cost?", k=5)

Each chunk is a dict: doc_id, version, title, effective_date, text, score.
The embeddings are cached on disk (COAPP_CACHE_DIR) so a restart does not
re-embed the whole corpus.
"""
import hashlib
import json
import re

import numpy as np
from rank_bm25 import BM25Okapi

from . import config

_WORD = re.compile(r"[a-z0-9$%.]+")
_STOP = set("a an the is are was were be to of in on for and or what how do does i we our it this that "
            "with at by from as can my your who when which".split())


def tokenize(text: str) -> list:
    return [t.strip(".") for t in _WORD.findall(text.lower()) if t.strip(".") and t not in _STOP]


def chunk_doc(doc: dict, size: int = config.CHUNK_CHARS, overlap: int = config.CHUNK_OVERLAP) -> list:
    """Split one document on Markdown headings, then into windows of about `size` characters."""
    sections = re.split(r"\n(?=#{1,3} )", doc["text"])
    chunks = []
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        start = 0
        while start < len(sec):
            piece = sec[start:start + size]
            chunks.append({
                "doc_id": doc.get("doc_id", ""), "version": str(doc.get("version", "")),
                "title": doc.get("title", ""), "effective_date": str(doc.get("effective_date", "")),
                "text": piece,
            })
            if start + size >= len(sec):
                break
            start += size - overlap
    return chunks


def _embed(texts: list) -> np.ndarray:
    client = config.get_client()
    out = []
    for i in range(0, len(texts), config.EMBED_BATCH):
        batch = [t[:2000] for t in texts[i:i + config.EMBED_BATCH]]
        resp = client.embeddings.create(model=config.EMBED_MODEL, input=batch)
        out.extend(d.embedding for d in sorted(resp.data, key=lambda d: d.index))
    arr = np.array(out, dtype=np.float32)
    arr /= np.linalg.norm(arr, axis=1, keepdims=True) + 1e-9
    return arr


def _fingerprint(chunks: list) -> str:
    h = hashlib.sha256(config.EMBED_MODEL.encode())
    for c in chunks:
        h.update((c["doc_id"] + c["version"] + c["text"]).encode())
    return h.hexdigest()[:16]


def build_index(docs: list, use_embeddings: bool | None = None) -> dict:
    """Chunk the documents and build BM25 + (optionally) embedding indexes."""
    use_embeddings = config.USE_EMBEDDINGS if use_embeddings is None else use_embeddings
    chunks = [c for d in docs for c in chunk_doc(d)]
    # Prefix the title so short chunks still carry their topic.
    bm25 = BM25Okapi([tokenize(c["title"] + " " + c["text"]) for c in chunks])
    index = {"chunks": chunks, "bm25": bm25, "emb": None, "embed_error": None}
    if use_embeddings:
        fp = _fingerprint(chunks)
        cache = config.CACHE_DIR / f"emb_{fp}.npy"
        try:
            if cache.exists():
                index["emb"] = np.load(cache)
            else:
                index["emb"] = _embed([c["title"] + "\n" + c["text"] for c in chunks])
                try:
                    config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
                    np.save(cache, index["emb"])
                except OSError:
                    pass  # caching is optional (e.g. read-only folder)
        except Exception as e:  # gateway down: keep working with BM25 only
            index["embed_error"] = f"{type(e).__name__}: {e}"
    return index


def retrieve(index: dict, question: str, k: int = config.TOP_K) -> list:
    """Top-k chunks by reciprocal rank fusion of BM25 and embedding rankings."""
    chunks = index["chunks"]
    bm = index["bm25"].get_scores(tokenize(question))
    rankings = [np.argsort(-bm)[:50]]
    if index.get("emb") is not None:
        try:
            q = _embed([question])[0]
            rankings.append(np.argsort(-(index["emb"] @ q))[:50])
        except Exception:
            pass  # embedding call failed for this query: BM25 only
    fused = {}
    for ranking in rankings:
        for rank, i in enumerate(ranking):
            fused[int(i)] = fused.get(int(i), 0.0) + 1.0 / (60 + rank + 1)
    top = sorted(fused, key=fused.get, reverse=True)[:k]
    return [{**chunks[i], "score": round(fused[i], 5)} for i in top]


def save_chunks(index: dict, path) -> None:
    """Write the chunk texts to JSON (handy for debugging)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(index["chunks"], f, indent=1)
