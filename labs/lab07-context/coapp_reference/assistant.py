"""
Co. app v1: answer a question from a fixed, hand-picked set of documents (no retrieval yet).

    from coapp.assistant import answer
    out = answer("What does server management cost?")
    out["answer"], out["sources"]

Returns the course-standard dict:
    {"answer": str, "sources": [{"doc_id", "version", "title"}], "tool_calls": [], "model": str,
     "latency_s": float, "prompt_version": str}
"""
import re
import time

from . import config, prompts

_DEFAULT_CHUNKS = None


def doc_to_chunk(doc: dict, score: float = 1.0) -> dict:
    """Turn a load_docs() document (or a gold_contexts passage) into a course-standard Chunk dict."""
    return {"doc_id": doc.get("doc_id", ""), "version": str(doc.get("version", "")),
            "title": doc.get("title", ""), "effective_date": str(doc.get("effective_date", "")),
            "text": doc.get("text", ""), "score": score}


def default_context() -> list:
    """The hand-picked v1 context: whole current documents listed in config.DEFAULT_CONTEXT_DOC_IDS."""
    global _DEFAULT_CHUNKS
    if _DEFAULT_CHUNKS is None:
        try:
            from itec632.corpus import load_docs
            docs = load_docs()
        except ImportError:
            docs = []
        by_id = {}
        for d in docs:
            if d.get("doc_id") in config.DEFAULT_CONTEXT_DOC_IDS:
                old = by_id.get(d["doc_id"])
                if old is None or str(d.get("effective_date", "")) > str(old.get("effective_date", "")):
                    by_id[d["doc_id"]] = d
        _DEFAULT_CHUNKS = [doc_to_chunk(by_id[i]) for i in config.DEFAULT_CONTEXT_DOC_IDS if i in by_id]
    return _DEFAULT_CHUNKS


def _trim(chunks: list, max_chars: int) -> list:
    out, total = [], 0
    for c in chunks:
        if total + len(c.get("text", "")) > max_chars and out:
            break
        out.append(c)
        total += len(c.get("text", ""))
    return out


def cited_sources(answer_text: str, chunks: list) -> list:
    """Documents the answer cites as [DOC-ID]; if it cites none, every document it was given."""
    cited = set(re.findall(r"\[([A-Z][A-Z0-9-]+)\]", answer_text or ""))
    use = [c for c in chunks if c.get("doc_id") in cited] or list(chunks)
    seen, out = set(), []
    for c in use:
        key = (c.get("doc_id"), str(c.get("version")))
        if key not in seen:
            seen.add(key)
            out.append({"doc_id": c.get("doc_id"), "version": str(c.get("version")), "title": c.get("title", "")})
    return out


def answer(question: str, history: list | None = None, context_chunks: list | None = None,
           build=None, model: str | None = None) -> dict:
    """Answer one question. context_chunks defaults to the hand-picked documents.

    build: optional replacement for prompts.build_messages (used in Lab 7 to compare prompt versions).
    """
    chunks = default_context() if context_chunks is None else list(context_chunks)
    chunks = _trim(chunks, config.MAX_CONTEXT_CHARS)
    build = build or prompts.build_messages
    messages = build(question, chunks, history)
    model = model or config.MODEL
    t0 = time.perf_counter()
    r = config.get_client().chat.completions.create(
        model=model, messages=messages, temperature=config.TEMPERATURE,
        max_tokens=config.MAX_TOKENS, extra_body=config.NO_THINK)
    latency = time.perf_counter() - t0
    text = re.sub(r"<think>.*?</think>", "", r.choices[0].message.content or "", flags=re.S).strip()
    return {
        "answer": text,
        "sources": cited_sources(text, chunks),
        "tool_calls": [],
        "model": model,
        "latency_s": round(latency, 3),
        "prompt_version": getattr(prompts, "PROMPT_VERSION", "?"),
    }
