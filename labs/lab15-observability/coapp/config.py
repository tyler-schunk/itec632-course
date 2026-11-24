"""
Co. app settings (v3: retrieval + tools).

Everything that changes between environments comes from environment variables,
so the same code runs in the course Jupyter container, in your own Docker
service (Lab 14), and in a plain Python venv:

    LITELLM_BASE_URL, LITELLM_API_KEY   gateway URL and your key (from .env)
    ITEC632_CORPUS                      path to corpus/larkspur-corpus (optional)
    COAPP_MODEL                         chat model alias (default: qwen-moe)
    COAPP_CACHE_DIR                     where the retrieval index is cached
    COAPP_TIMEOUT_S                     per-request timeout for model calls
"""
import os
import tempfile
from pathlib import Path

try:  # inside the course image the helper package is installed
    from itec632 import MODELS, NO_THINK
except ImportError:  # inside the Lab 14 service image it is not, so define the same values
    MODELS = {"main": "qwen-moe", "dense": "qwen-dense", "gemma": "gemma-moe",
              "small": "qwen-small", "embed": "embed", "rerank": "rerank"}
    NO_THINK = {"chat_template_kwargs": {"enable_thinking": False}}

MODEL = os.environ.get("COAPP_MODEL", MODELS["main"])
EMBED_MODEL = MODELS["embed"]
TODAY = "2026-11-02"            # "today" in the Larkspur world

# Retrieval
TOP_K = 5
CHUNK_CHARS = 1200              # target chunk size in characters
CHUNK_OVERLAP = 150
EMBED_BATCH = 64
USE_EMBEDDINGS = os.environ.get("COAPP_USE_EMBEDDINGS", "1") != "0"

# Generation
TEMPERATURE = 0.2
MAX_TOKENS = 700
MAX_TOOL_ROUNDS = 3
TIMEOUT_S = float(os.environ.get("COAPP_TIMEOUT_S", "120"))

CACHE_DIR = Path(os.environ.get("COAPP_CACHE_DIR", Path(tempfile.gettempdir()) / "coapp_cache"))


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


def db_path() -> Path:
    return corpus_dir() / "data" / "larkspur.db"


def gateway_settings():
    """(base_url, api_key) from the environment, loading a .env file if one is found."""
    try:
        from dotenv import find_dotenv, load_dotenv
        load_dotenv(find_dotenv(usecwd=True), override=False)
    except ImportError:
        pass
    return (os.environ.get("LITELLM_BASE_URL", "").strip(),
            os.environ.get("LITELLM_API_KEY", "").strip())


_client = None


def get_client():
    """One shared OpenAI-compatible client for the gateway (thread-safe, reused)."""
    global _client
    if _client is None:
        from openai import OpenAI
        base_url, api_key = gateway_settings()
        if not base_url or not api_key:
            raise RuntimeError("LITELLM_BASE_URL / LITELLM_API_KEY are not set (check your .env).")
        _client = OpenAI(base_url=base_url, api_key=api_key, timeout=TIMEOUT_S, max_retries=1)
    return _client
