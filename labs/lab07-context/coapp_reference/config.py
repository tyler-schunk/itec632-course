"""
Co. app settings (v1: prompts + hand-picked context; Lab 7 reference).

Values that change between environments come from environment variables:
    LITELLM_BASE_URL, LITELLM_API_KEY   gateway URL and key (from .env)
    ITEC632_CORPUS                      path to corpus/larkspur-corpus (optional)
    COAPP_MODEL                         chat model alias (default: qwen-moe)
"""
import os
from pathlib import Path

try:  # inside the course image the helper package is installed
    from itec632 import MODELS, NO_THINK
except ImportError:  # e.g. a slim service image: same values
    MODELS = {"main": "qwen-moe", "dense": "qwen-dense", "gemma": "gemma-moe",
              "small": "qwen-small", "embed": "embed", "rerank": "rerank"}
    NO_THINK = {"chat_template_kwargs": {"enable_thinking": False}}

MODEL = os.environ.get("COAPP_MODEL", MODELS["main"])
TODAY = "2026-11-02"            # "today" in the Larkspur world

# Generation
TEMPERATURE = 0.2
MAX_TOKENS = 600
TIMEOUT_S = float(os.environ.get("COAPP_TIMEOUT_S", "120"))

# v1 has no retrieval. If answer() gets no context, it uses these hand-picked CURRENT documents.
DEFAULT_CONTEXT_DOC_IDS = ["SVC-CAT-2026", "PRICE-2026", "SLA-EXH-2026"]
MAX_CONTEXT_CHARS = 40000       # keep requests well under the ~32K-token cluster limit


def corpus_dir() -> Path:
    """Find corpus/larkspur-corpus: $ITEC632_CORPUS, the itec632 helper, or a parent folder."""
    env = os.environ.get("ITEC632_CORPUS")
    if env and Path(env).is_dir():
        return Path(env)
    try:
        from itec632.corpus import corpus_dir as _cd
        return _cd()
    except ImportError:
        pass
    here = Path.cwd().resolve()
    for p in [here, *here.parents]:
        cand = p / "corpus" / "larkspur-corpus"
        if cand.is_dir():
            return cand
    raise RuntimeError("Can't find corpus/larkspur-corpus. Set ITEC632_CORPUS to its path.")


_client = None


def get_client():
    """One shared OpenAI-compatible client for the gateway."""
    global _client
    if _client is None:
        try:
            from itec632 import get_client as _gc
            _client = _gc(timeout=TIMEOUT_S)
        except ImportError:
            from openai import OpenAI
            _client = OpenAI(base_url=os.environ["LITELLM_BASE_URL"], api_key=os.environ["LITELLM_API_KEY"],
                             timeout=TIMEOUT_S)
    return _client
