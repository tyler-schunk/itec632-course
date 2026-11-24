"""
Find the Larkspur Ridge IT corpus, wherever the notebook is running.

    from itec632.corpus import corpus_dir, load_docs, db_path
    root = corpus_dir()          # Path to .../larkspur-corpus
    docs = load_docs()           # list of dicts: doc_id, title, version, effective_date, ..., text, path
    con = sqlite3.connect(db_path())

Search order: $ITEC632_CORPUS, then a corpus/larkspur-corpus folder in the
current directory or any parent (Docker lab / local fallback), then (Colab)
download the course repository from GitHub once and cache it.
"""
import io
import os
import re
import urllib.request
import zipfile
from pathlib import Path

# Instructor: set to the public repo once it exists (also in compose.yaml).
REPO = os.environ.get("ITEC632_REPO", "tyler-schunk/itec632-course")
BRANCH = os.environ.get("ITEC632_BRANCH", "main")
_CACHE = Path(os.environ.get("ITEC632_CACHE", Path.home() / ".itec632"))


def corpus_dir() -> Path:
    env = os.environ.get("ITEC632_CORPUS")
    if env and Path(env).is_dir():
        return Path(env)
    here = Path.cwd().resolve()
    for p in [here, *here.parents]:
        cand = p / "corpus" / "larkspur-corpus"
        if cand.is_dir():
            return cand
    cached = _CACHE / "larkspur-corpus"
    if cached.is_dir():
        return cached
    url = f"https://github.com/{REPO}/archive/refs/heads/{BRANCH}.zip"
    print(f"Downloading the course corpus from {url} (one time)...")
    data = urllib.request.urlopen(url, timeout=120).read()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        prefix = None
        for name in z.namelist():
            if "/corpus/larkspur-corpus/" in name:
                prefix = name.split("/corpus/larkspur-corpus/")[0] + "/corpus/larkspur-corpus/"
                break
        if prefix is None:
            raise RuntimeError("Corpus not found in the repository download.")
        for name in z.namelist():
            if name.startswith(prefix) and not name.endswith("/"):
                out = cached / name[len(prefix):]
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(z.read(name))
    return cached


def db_path() -> Path:
    return corpus_dir() / "data" / "larkspur.db"


_FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def _front_matter(text: str):
    m = _FM.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.split("#", 1)[0].strip().strip('"').strip("'")
    return meta, text[m.end():]


def load_docs(folders=("client-docs", "runbooks", "internal")):
    """Every Markdown document with its front-matter fields, body text, and path."""
    root = corpus_dir()
    docs = []
    for folder in folders:
        for path in sorted((root / folder).glob("*.md")):
            meta, body = _front_matter(path.read_text(encoding="utf-8"))
            docs.append({**meta, "folder": folder, "path": str(path.relative_to(root)), "text": body})
    return docs
