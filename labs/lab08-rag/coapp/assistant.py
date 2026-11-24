"""
Co. app v2: retrieval-augmented answers (YOUR copy: one TODO in answer()).

    from coapp.assistant import answer
    out = answer("What does server management cost?")
    out["answer"], out["sources"], out["retrieved"]

Returns the course-standard dict plus retrieval details:
    {"answer": str, "sources": [{"doc_id", "version", "title"}], "tool_calls": [], "model": str,
     "latency_s": float, "prompt_version": str,
     "retrieved": [{"doc_id", "version", "effective_date", "score"}], "retrieval": {...}}
"""
import re
import time

from . import config, prompts
from .retrieve import LAST_INFO, build_index, retrieve

_INDEX = None


def load_corpus_docs() -> list:
    try:
        from itec632.corpus import load_docs
    except ImportError:
        from ._docs import load_docs
    return load_docs()


def get_index() -> dict:
    """Build the retrieval index once per process (embeddings come from the .npy cache after the first run)."""
    global _INDEX
    if _INDEX is None:
        _INDEX = build_index(load_corpus_docs())
    return _INDEX


def cited_sources(answer_text: str, chunks: list) -> list:
    """Documents the answer cites as [DOC-ID]; if it cites none, every retrieved document."""
    cited = set(re.findall(r"\[([A-Z][A-Z0-9-]+)\]", answer_text or ""))
    use = [c for c in chunks if c.get("doc_id") in cited] or list(chunks)
    seen, out = set(), []
    for c in use:
        key = (c.get("doc_id"), str(c.get("version")))
        if key not in seen:
            seen.add(key)
            out.append({"doc_id": c.get("doc_id"), "version": str(c.get("version")), "title": c.get("title", "")})
    return out


def answer(question: str, history: list | None = None, k: int | None = None, context_chunks: list | None = None,
           build=None, model: str | None = None, **retrieve_kwargs) -> dict:
    """Retrieve context for the question, then answer from it.

    context_chunks: skip retrieval and use these chunks (handy for testing).
    retrieve_kwargs: passed to retrieve(), e.g. use_rerank=True or prefer_current_version=False.
    """
    t0 = time.perf_counter()
    if context_chunks is None:
        # TODO (B3): retrieve the chunks for this question with retrieve(). It needs the index
        #   (get_index() returns it), the question, k (use config.TOP_K when k is None),
        #   and **retrieve_kwargs passed straight through.
        chunks = []
        info = dict(LAST_INFO)
    else:
        chunks, info = list(context_chunks), {"retrievers": ["given"]}
    messages = (build or prompts.build_messages)(question, chunks, history)
    model = model or config.MODEL
    r = config.get_client().chat.completions.create(
        model=model, messages=messages, temperature=config.TEMPERATURE,
        max_tokens=config.MAX_TOKENS, extra_body=config.NO_THINK)
    text = re.sub(r"<think>.*?</think>", "", r.choices[0].message.content or "", flags=re.S).strip()
    return {
        "answer": text,
        "sources": cited_sources(text, chunks),
        "tool_calls": [],
        "model": model,
        "latency_s": round(time.perf_counter() - t0, 3),
        "prompt_version": getattr(prompts, "PROMPT_VERSION", "?"),
        "retrieved": [{"doc_id": c["doc_id"], "version": c["version"], "effective_date": c["effective_date"],
                       "score": c.get("score")} for c in chunks],
        "retrieval": info,
    }
