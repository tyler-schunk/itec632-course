"""
ITEC 632 course helpers.

    from itec632 import get_client, MODELS, NO_THINK

    client = get_client()
    reply = client.chat.completions.create(
        model=MODELS["main"],
        messages=[{"role": "user", "content": "Hello!"}],
        extra_body=NO_THINK,          # optional: turn off Qwen's "thinking" mode
    )
    print(reply.choices[0].message.content)
"""
import os

__all__ = ["get_client", "MODELS", "NO_THINK", "settings", "strip_think"]

# Course model names on the gateway. These stay the same all semester even if
# the instructor swaps the underlying model, so your notebooks keep working.
MODELS = {
    "main": "qwen-moe",      # Qwen3.6 MoE (35B total, 3B active) - use this by default
    "dense": "qwen-dense",   # Qwen3.8 27B dense - for dense vs MoE comparisons
    "gemma": "gemma-moe",    # Gemma 4 26B-A4B - a different model family
    "small": "qwen-small",   # Qwen3.5 4B - small and fast
    "embed": "embed",        # Qwen3 embedding model
    "rerank": "rerank",      # Qwen3 reranker
}

# Pass as extra_body=NO_THINK to get a direct answer without a reasoning phase.
NO_THINK = {"chat_template_kwargs": {"enable_thinking": False}}


def settings():
    """Return (base_url, api_key) from the environment or a .env file."""
    try:
        from dotenv import find_dotenv, load_dotenv
        load_dotenv(find_dotenv(usecwd=True), override=False)
    except ImportError:
        pass
    base_url = os.environ.get("LITELLM_BASE_URL", "").strip()
    api_key = os.environ.get("LITELLM_API_KEY", "").strip()
    return base_url, api_key


def get_client(timeout=300):
    """An OpenAI-compatible client pointed at the course cluster."""
    from openai import OpenAI
    base_url, api_key = settings()
    if not base_url or not api_key or "paste" in api_key.lower():
        raise RuntimeError(
            "LITELLM_BASE_URL / LITELLM_API_KEY are not set. Copy .env.example to .env, "
            "paste in the values from your key email, then restart: docker compose up"
        )
    return OpenAI(base_url=base_url, api_key=api_key, timeout=timeout)


def strip_think(text):
    """Remove any <think>...</think> reasoning block a model left in its answer."""
    import re
    return re.sub(r"<think>.*?</think>", "", text or "", flags=re.S).strip()
