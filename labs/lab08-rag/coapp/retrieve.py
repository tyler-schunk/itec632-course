"""
Retrieval for Co. app v2 (YOUR copy: complete the TODOs in chunk_doc and prefer_current) (Ch. 6, "RAG"): heading-aware chunking, term-based (BM25) and embedding
retrieval fused with reciprocal rank fusion (RRF), optional reranking, and metadata-aware filtering
that prefers the current version when several versions of one document are retrieved.

    from coapp.retrieve import build_index, retrieve
    index = build_index(docs)                      # docs from itec632.corpus.load_docs()
    chunks = retrieve(index, "What does server management cost?", k=5)

Each chunk is a dict: doc_id, version, title, effective_date, text, score (plus section).
Embeddings are computed in batches and cached as a .npy file in config.CACHE_DIR.
After each retrieve() call, LAST_INFO describes what happened (rerank used or failed, stale chunks dropped).
"""
import hashlib
import re
import time

import numpy as np
from rank_bm25 import BM25Okapi

from . import config

LAST_INFO = {}

_WORD = re.compile(r"[a-z0-9]+(?:\.[0-9]+)?")
STOPWORDS = set("a an the is are was were be been to of in on for and or what how do does did i we our it its this "
                "that with at by from as can my your who when which there their should would will if not any".split())


def tokenize(text: str) -> list:
    """Lowercase word/number tokens without stopwords (keeps numbers like 247.50)."""
    return [t for t in _WORD.findall((text or "").lower()) if t not in STOPWORDS]


# ---------------------------------------------------------------- chunking
def _split_long(text: str, max_chars: int) -> list:
    """Split text into pieces of at most max_chars, preferring paragraph boundaries."""
    if len(text) <= max_chars:
        return [text]
    pieces, buf = [], ""
    for para in text.split("\n\n"):
        while len(para) > max_chars:                       # one huge paragraph: hard split
            if buf:
                pieces.append(buf); buf = ""
            pieces.append(para[:max_chars]); para = para[max_chars:]
        if buf and len(buf) + 2 + len(para) > max_chars:
            pieces.append(buf); buf = para
        else:
            buf = f"{buf}\n\n{para}" if buf else para
    if buf:
        pieces.append(buf)
    return pieces


# The Part A helpers, under the same names as in the notebook, so code pasted from Part A runs here unchanged.
split_long = _split_long


def make_chunk(doc: dict, text: str, section: str = "") -> dict:
    """One chunk: a piece of text plus its document's metadata (version and effective_date as strings)."""
    return {"doc_id": doc.get("doc_id", ""), "version": str(doc.get("version", "")), "title": doc.get("title", ""),
            "effective_date": str(doc.get("effective_date", "")), "section": section, "text": text}


def merge_small(sections: list, min_chars: int, max_chars: int) -> list:
    """Glue a tiny section (for example a lone heading) onto the next one."""
    merged, buf = [], ""
    for s in sections:
        if buf and len(buf) < min_chars and len(buf) + len(s) + 2 <= max_chars:
            buf = f"{buf}\n\n{s}"
        else:
            if buf:
                merged.append(buf)
            buf = s
    if buf:
        merged.append(buf)
    return merged


def heading_of(section: str) -> str:
    """The section's heading text without the leading '#' characters ('' if it has no heading)."""
    return section.splitlines()[0].lstrip("# ").strip() if section.startswith("#") else ""


def chunk_doc(doc: dict, max_chars: int = config.CHUNK_CHARS, min_chars: int = config.MIN_CHUNK_CHARS) -> list:
    """Split one document at Markdown headings (#, ##, ###, ####); merge tiny sections; split long ones.

    TODO (B1): replace the placeholder with the body of your chunk_by_heading() from Part A (everything
    below its `def` line). The helpers it uses (make_chunk, merge_small, heading_of, split_long) are defined
    above under the same names, so the pasted code runs as is. Keep this function's own name and arguments:
    max_chars and min_chars come from config, and `doc` is the same kind of dict as in Part A.
    The placeholder below returns the whole document as ONE chunk (it runs, but retrieves poorly).
    """
    return [{"doc_id": doc.get("doc_id", ""), "version": str(doc.get("version", "")), "title": doc.get("title", ""),
             "effective_date": str(doc.get("effective_date", "")), "section": "", "text": doc.get("text", "")}]


# ---------------------------------------------------------------- embeddings
def embed_texts(texts: list, batch_size: int = config.EMBED_BATCH) -> np.ndarray:
    """Embed many texts with a few batched requests, paced to stay under the token-per-minute limit."""
    client = config.get_client()
    out = []
    for i in range(0, len(texts), batch_size):
        batch = [t[:6000] for t in texts[i:i + batch_size]]
        t0 = time.time()
        resp = client.embeddings.create(model=config.EMBED_MODEL, input=batch)
        out.extend(d.embedding for d in sorted(resp.data, key=lambda d: d.index))
        est_tokens = sum(len(t) for t in batch) / 4
        if i + batch_size < len(texts):
            time.sleep(max(0.0, est_tokens / config.EMBED_TOKENS_PER_MIN * 60 - (time.time() - t0)))
    arr = np.array(out, dtype=np.float32)
    return arr / (np.linalg.norm(arr, axis=1, keepdims=True) + 1e-9)


def _fingerprint(texts: list) -> str:
    h = hashlib.sha256(config.EMBED_MODEL.encode())
    for t in texts:
        h.update(t.encode())
    return h.hexdigest()[:16]


def chunk_embed_text(c: dict) -> str:
    """What gets embedded: title and section give each chunk its topic (a light form of contextual retrieval)."""
    return f"{c['title']} - {c.get('section', '')}\n{c['text']}"


# ---------------------------------------------------------------- index
def build_index(docs: list, use_embeddings: bool | None = None) -> dict:
    """Chunk the documents, build a BM25 index and (optionally) an embedding matrix (cached to .npy)."""
    use_embeddings = config.USE_EMBEDDINGS if use_embeddings is None else use_embeddings
    chunks = [c for d in docs for c in chunk_doc(d)]
    bm25 = BM25Okapi([tokenize(c["title"] + " " + c.get("section", "") + " " + c["text"]) for c in chunks])
    latest = {}
    for c in chunks:
        latest[c["doc_id"]] = max(latest.get(c["doc_id"], ""), c["effective_date"])
    index = {"chunks": chunks, "bm25": bm25, "emb": None, "embed_error": None, "latest": latest, "qcache": {}}
    if use_embeddings:
        texts = [chunk_embed_text(c) for c in chunks]
        cache = config.CACHE_DIR / f"emb_{_fingerprint(texts)}.npy"
        try:
            if cache.exists():
                index["emb"] = np.load(cache)
            else:
                index["emb"] = embed_texts(texts)
                try:
                    config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
                    np.save(cache, index["emb"])
                except OSError:
                    pass                                      # caching is optional
        except Exception as e:                                # gateway down: keep working with BM25 only
            index["embed_error"] = f"{type(e).__name__}: {e}"
    return index


# ---------------------------------------------------------------- ranking pieces
def rrf_fuse(rankings: list, k: int = config.RRF_K) -> list:
    """Reciprocal rank fusion: each ranking is a list of chunk ids, best first.
    Returns [(chunk_id, fused_score)] sorted best first. score = sum over rankings of 1 / (k + rank), rank from 1.
    Provided (same math as the notebook's rrf() in A4): a chunk found by both retrievers collects two small
    scores, so it usually beats a chunk that only one retriever ranked first."""
    scores = {}
    for ranking in rankings:
        for rank, cid in enumerate(ranking, start=1):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)


def prefer_current(chunks: list) -> tuple:
    """If several versions of the same doc_id were retrieved, keep only chunks from the newest effective_date.
    Returns (kept_chunks, number_dropped).

    TODO (B2): for each doc_id find the newest effective_date among `chunks` (ISO dates compare as strings),
    keep only chunks with that date (in their original order), and return two things: the kept list and
    how many chunks were dropped.
    The placeholder keeps everything.
    """
    return list(chunks), 0


def rerank_scores(query: str, texts: list, top_n: int | None = None):
    """Call the gateway's Cohere-style rerank endpoint: POST {base without /v1}/rerank.
    Returns [(index_into_texts, relevance_score)] best first. Raises on any failure."""
    import httpx
    base, key = config.gateway_settings()
    root = base.rstrip("/")
    root = root[:-3] if root.endswith("/v1") else root
    r = httpx.post(f"{root}/rerank", headers={"Authorization": f"Bearer {key}"}, timeout=60,
                   json={"model": config.RERANK_MODEL, "query": query, "documents": texts,
                         "top_n": top_n or len(texts)})
    r.raise_for_status()
    return [(int(x["index"]), float(x["relevance_score"])) for x in r.json()["results"]]


def _query_vec(index: dict, question: str):
    if question not in index["qcache"]:
        index["qcache"][question] = embed_texts([question])[0]
    return index["qcache"][question]


def retrieve(index: dict, question: str, k: int = config.TOP_K, use_rerank: bool | None = None,
             prefer_current_version: bool | None = None) -> list:
    """Top-k chunks for a question: BM25 + embeddings fused with RRF, optional rerank, prefer current versions."""
    use_rerank = config.USE_RERANK if use_rerank is None else use_rerank
    prefer = config.PREFER_CURRENT if prefer_current_version is None else prefer_current_version
    info = {"retrievers": ["bm25"], "reranked": False, "rerank_error": None, "stale_dropped": 0}
    chunks = index["chunks"]

    bm = index["bm25"].get_scores(tokenize(question))
    rankings = [list(np.argsort(-bm)[:config.CANDIDATES])]
    if index.get("emb") is not None:
        try:
            sims = index["emb"] @ _query_vec(index, question)
            rankings.append(list(np.argsort(-sims)[:config.CANDIDATES]))
            info["retrievers"].append("embedding")
        except Exception as e:                                # embedding call failed: BM25 only
            info["embed_error"] = f"{type(e).__name__}: {e}"
    fused = rrf_fuse([[int(i) for i in r] for r in rankings])
    cands = [{**chunks[cid], "score": round(s, 5)} for cid, s in fused]

    if prefer:
        cands, info["stale_dropped"] = prefer_current(cands)

    if use_rerank and cands:
        top = cands[:config.RERANK_CANDIDATES]
        try:
            order = rerank_scores(question, [chunk_embed_text(c) for c in top])
            cands = [{**top[i], "score": round(s, 5)} for i, s in order]
            info["reranked"] = True
        except Exception as e:                                # rerank failed: keep the fused order
            info["rerank_error"] = f"{type(e).__name__}: {str(e)[:200]}"
    LAST_INFO.clear()
    LAST_INFO.update(info)
    return cands[:k]


def is_stale(index: dict, chunk: dict) -> bool:
    """True if a newer version of this chunk's doc_id exists in the corpus."""
    return chunk["effective_date"] < index["latest"].get(chunk["doc_id"], "")
