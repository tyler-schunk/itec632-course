"""
Co. app settings (v2: retrieval-augmented generation; Lab 8 reference).

Values that change between environments come from environment variables:
    LITELLM_BASE_URL, LITELLM_API_KEY   gateway URL and key (from .env)
    ITEC632_CORPUS                      path to corpus/larkspur-corpus (optional)
    COAPP_MODEL                         chat model alias (default: qwen-moe)
    COAPP_CACHE_DIR                     where the embedding cache (.npy) is written (default: ./.coapp_cache)
    COAPP_USE_EMBEDDINGS=0              BM25 only (no embedding calls)
    COAPP_USE_RERANK=1                  rerank candidates with the gateway's rerank model
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
EMBED_MODEL = MODELS["embed"]
RERANK_MODEL = MODELS["rerank"]
TODAY = "2026-11-02"            # "today" in the Larkspur world

# Generation
TEMPERATURE = 0.2
MAX_TOKENS = 600
TIMEOUT_S = float(os.environ.get("COAPP_TIMEOUT_S", "120"))

# Retrieval
TOP_K = 5                       # chunks handed to the model
CHUNK_CHARS = 1500              # max characters per chunk (heading-aware chunking)
MIN_CHUNK_CHARS = 250           # tiny sections are merged with the next one
CANDIDATES = 30                 # per-retriever candidates before fusion
RRF_K = 60                      # reciprocal rank fusion constant
RERANK_CANDIDATES = 20          # how many fused candidates the reranker sees
EMBED_BATCH = 32                # inputs per embeddings request
EMBED_TOKENS_PER_MIN = 150_000  # pacing for the corpus embedding pass (key limit is 300k/min)
USE_EMBEDDINGS = os.environ.get("COAPP_USE_EMBEDDINGS", "1") != "0"
USE_RERANK = os.environ.get("COAPP_USE_RERANK", "0") == "1"
PREFER_CURRENT = True           # drop older versions when several versions of one doc_id are retrieved

CACHE_DIR = Path(os.environ.get("COAPP_CACHE_DIR", Path.cwd() / ".coapp_cache"))
MAX_CONTEXT_CHARS = 40000


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


def gateway_settings():
    """(base_url, api_key) from the environment, loading a .env file if one is found."""
    try:
        from dotenv import find_dotenv, load_dotenv
        load_dotenv(find_dotenv(usecwd=True), override=False)
    except ImportError:
        pass
    return (os.environ.get("LITELLM_BASE_URL", "").strip(), os.environ.get("LITELLM_API_KEY", "").strip())


_client = None


def get_client():
    """One shared OpenAI-compatible client for the gateway."""
    global _client
    if _client is None:
        from openai import OpenAI
        base_url, api_key = gateway_settings()
        if not base_url or not api_key:
            raise RuntimeError("LITELLM_BASE_URL / LITELLM_API_KEY are not set (check your .env).")
        _client = OpenAI(base_url=base_url, api_key=api_key, timeout=TIMEOUT_S)
    return _client
