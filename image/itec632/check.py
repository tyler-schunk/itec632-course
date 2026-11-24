"""
ITEC 632 setup check. Run it in a notebook cell:

    from itec632.check import run_checks
    run_checks()

or from a terminal:  python -m itec632.check

Each step prints a green check or a red X with what to do next.
"""
import hashlib
import importlib
import platform
import socket
import sys
import time
from urllib.parse import urlparse

from . import MODELS, NO_THINK, settings

OK, BAD, INFO = "✅", "❌", "ℹ️"
PACKAGES = ["openai", "httpx", "pandas", "numpy", "matplotlib", "sklearn",
            "rank_bm25", "pydantic", "jsonschema", "fastapi", "dotenv"]


def _line(ok, msg, fix=""):
    print(f"{OK if ok else BAD}  {msg}")
    if not ok and fix:
        print(f"     -> {fix}")
    return ok


def run_checks():
    print("ITEC 632 setup check\n" + "-" * 40)
    results = []

    # 1. Python
    v = sys.version_info
    results.append(_line(v >= (3, 11), f"Python {v.major}.{v.minor}",
                         "Use the course Docker image (docker compose up)."))

    # 2. Packages
    missing = []
    for p in PACKAGES:
        try:
            importlib.import_module(p)
        except ImportError:
            missing.append(p)
    results.append(_line(not missing, "Course packages installed" + (f" (missing: {missing})" if missing else ""),
                         "Run: docker compose pull, then docker compose up"))

    # 3. Settings
    base_url, key = settings()
    have = bool(base_url) and key.startswith("sk-") and "paste" not in key.lower()
    results.append(_line(have, "Gateway URL and key found in .env",
                         "Copy .env.example to .env and paste in the two values from your key email. "
                         "Then stop (Ctrl+C) and run docker compose up again."))
    if not have:
        return _summary(results)

    # 4. Network: can we reach the gateway at all? (VPN check)
    u = urlparse(base_url)
    host, port = u.hostname, u.port or (443 if u.scheme == "https" else 80)
    try:
        with socket.create_connection((host, port), timeout=5):
            reach = True
    except OSError:
        reach = False
    results.append(_line(reach, f"Can reach the gateway at {host}:{port}",
                         "Connect to the KU VPN and try again. If you're on the VPN already, "
                         "disconnect/reconnect it, then restart Docker Desktop."))
    if not reach:
        return _summary(results)

    # 5. Key accepted + models visible
    from openai import OpenAI, AuthenticationError
    client = OpenAI(base_url=base_url, api_key=key, timeout=120)
    try:
        ids = {m.id for m in client.models.list().data}
        need = set(MODELS.values())
        results.append(_line(need <= ids, f"Key accepted; {len(ids & need)}/{len(need)} course models visible",
                             "Email the instructor a screenshot of this output."))
    except AuthenticationError:
        results.append(_line(False, "Key accepted", "Check for typos or extra spaces in LITELLM_API_KEY in .env."))
        return _summary(results)
    except Exception as e:  # noqa: BLE001
        results.append(_line(False, f"Model list ({type(e).__name__})", "Email the instructor a screenshot."))
        return _summary(results)

    # 6. A real chat request
    try:
        t0 = time.time()
        r = client.chat.completions.create(
            model=MODELS["main"], max_tokens=30, extra_body=NO_THINK,
            messages=[{"role": "user", "content": "Say hello to a new ITEC 632 student in 8 words or fewer."}],
        )
        txt = (r.choices[0].message.content or "").strip()
        results.append(_line(bool(txt), f"Chat works ({time.time()-t0:.1f}s): {txt!r}"))
    except Exception as e:  # noqa: BLE001
        results.append(_line(False, f"Chat request failed: {str(e)[:120]}", "Wait a minute and re-run; if it repeats, email the instructor."))

    # 7. Embeddings
    try:
        e = client.embeddings.create(model=MODELS["embed"], input=["hello"])
        results.append(_line(len(e.data[0].embedding) > 0, f"Embeddings work (dimension {len(e.data[0].embedding)})"))
    except Exception as e:  # noqa: BLE001
        results.append(_line(False, f"Embeddings failed: {str(e)[:120]}", "Email the instructor a screenshot."))

    return _summary(results, key)


def _summary(results, key=""):
    print("-" * 40)
    if all(results):
        # Setup code for the Module 1 submission: proves the check passed with this key.
        code = hashlib.sha256(f"itec632|{key}|{platform.system()}".encode()).hexdigest()[:10].upper()
        print(f"{OK}  ALL CHECKS PASSED.  Setup code: {code}")
    else:
        print(f"{INFO}  Fix the first red item above, then run this check again.")
    return all(results)


if __name__ == "__main__":
    sys.exit(0 if run_checks() else 1)
