"""
Self-check and submission summary for ITEC 632 labs.

In a lab notebook:

    from itec632.grading import LabChecker
    ck = LabChecker("lab06", part="cluster")      # part: "cluster" or "colab"

    ck.check("schema_valid", ok, points=2, hint="Your JSON did not match the schema; see step 3.")
    ck.record("accuracy", acc)                    # numbers the written analysis refers to
    ...
    ck.report()                                   # last cell of the notebook

report() prints a readable table plus one machine-readable line that the
instructor's grading script reads from the submitted .ipynb. The line carries
a short checksum so accidental or casual edits to the output are detectable.
(It is tamper-evident, not tamper-proof; the instructor spot re-runs notebooks.)
"""
import datetime as _dt
import hashlib
import json
import os
import platform

MARKER = "ITEC632-RESULT::"
_SALT = "itec632|larkspur|v1"   # public on purpose: this is a consistency check, not security
_GREEN, _RED = "✅", "❌"


def _sig(payload_json: str) -> str:
    return hashlib.sha256(f"{_SALT}|{payload_json}".encode()).hexdigest()[:12]


def _env() -> str:
    if "COLAB_RELEASE_TAG" in os.environ or "COLAB_GPU" in os.environ:
        return "colab"
    if os.path.exists("/.dockerenv"):
        return "docker"
    return platform.system().lower()


class LabChecker:
    def __init__(self, lab: str, part: str = "cluster"):
        self.lab, self.part = lab, part
        self.checks = {}   # name -> dict(passed, points, hint)
        self.records = {}  # name -> value

    def check(self, name: str, passed, points: float = 1, hint: str = "") -> bool:
        """Record a pass/fail check and print the result right away."""
        passed = bool(passed)
        self.checks[name] = {"passed": passed, "points": points, "hint": hint}
        mark = _GREEN if passed else _RED
        print(f"{mark}  {name}  ({points if passed else 0}/{points})")
        if not passed and hint:
            print(f"     -> {hint}")
        return passed

    def record(self, name: str, value):
        """Save a value (a metric, a count, a short string) for the summary."""
        if isinstance(value, float):
            value = round(value, 4)
        try:
            json.dumps(value)
        except TypeError:
            value = str(value)
        self.records[name] = value
        return value

    def score(self):
        got = sum(c["points"] for c in self.checks.values() if c["passed"])
        total = sum(c["points"] for c in self.checks.values())
        return got, total

    def report(self):
        got, total = self.score()
        print("=" * 60)
        print(f"ITEC 632 {self.lab} ({self.part}) - self-check summary")
        print("-" * 60)
        for n, c in self.checks.items():
            print(f"{_GREEN if c['passed'] else _RED}  {n:40} {c['points'] if c['passed'] else 0:>4}/{c['points']}")
        if self.records:
            print("-" * 60)
            for k, v in self.records.items():
                print(f"   {k:40} {v}")
        print("-" * 60)
        print(f"Auto-checked points: {got}/{total}   (the written analysis is graded separately)")
        payload = {
            "lab": self.lab, "part": self.part, "score": got, "max": total,
            "checks": {k: v["passed"] for k, v in self.checks.items()},
            "records": self.records,
            "env": _env(),
            "utc": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        pj = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        print(f"{MARKER}{pj}::{_sig(pj)}")
        if got < total:
            print("Fix the red items above and re-run, or explain in your analysis what you tried.")
        print("Save the notebook (with outputs) and upload the .ipynb to Canvas.")
        return got, total


def parse_result_line(line: str):
    """Used by the grading script. Returns (payload_dict, signature_ok) or None."""
    if MARKER not in line:
        return None
    body = line.split(MARKER, 1)[1].strip()
    try:
        pj, sig = body.rsplit("::", 1)
        return json.loads(pj), _sig(pj) == sig.strip()
    except ValueError:
        return None
