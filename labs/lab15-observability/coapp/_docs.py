"""
Minimal copy of itec632.corpus.load_docs(), used only where the itec632 helper
package is not installed (the Lab 14/15 service image). Same output format.
"""
import re

from . import config

_FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def _front_matter(text):
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
    root = config.corpus_dir()
    docs = []
    for folder in folders:
        for path in sorted((root / folder).glob("*.md")):
            meta, body = _front_matter(path.read_text(encoding="utf-8"))
            docs.append({**meta, "folder": folder, "path": str(path.relative_to(root)), "text": body})
    return docs
