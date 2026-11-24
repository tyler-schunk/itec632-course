"""
Per-request traces and feedback storage (Ch. 10, "Monitoring and Observability").

Every /ask request produces ONE trace record (a JSON object on one line of
logs/traces.jsonl): what came in (redacted), how it was routed, what was retrieved,
which tools ran, how many tokens it used, how long each step took, what the
guardrails did, and any error. /feedback appends to logs/feedback.jsonl.

JSONL ("JSON Lines") is easy to append to from a service and easy to load later:
    pd.read_json("logs/traces.jsonl", lines=True)

The last 2,000 traces are also kept in memory, so the service can look up a
request_id for feedback and serve GET /traces even if the log folder is not writable.
"""
import datetime as dt
import json
import os
import threading
import time
import uuid
from collections import deque
from contextlib import contextmanager
from pathlib import Path

LOG_DIR = Path(os.environ.get("COAPP_LOG_DIR", "logs"))
TRACE_FILE = LOG_DIR / "traces.jsonl"
FEEDBACK_FILE = LOG_DIR / "feedback.jsonl"

_lock = threading.Lock()
_recent = deque(maxlen=2000)
_by_id = {}
status = {"log_writable": None, "last_write_error": None}


def new_request_id() -> str:
    return uuid.uuid4().hex[:12]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def append_jsonl(path: Path, record: dict) -> bool:
    """Append one JSON line. Returns False (and remembers the error) if the file can't be written."""
    line = json.dumps(record, default=str, ensure_ascii=False)
    with _lock:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            status["log_writable"] = True
            return True
        except OSError as e:
            status["log_writable"] = False
            status["last_write_error"] = f"{type(e).__name__}: {e}"[:200]
            return False


class Trace:
    """Collects one request's trace. Use .step("name") to time a step."""

    def __init__(self, request_id: str):
        self.t0 = time.perf_counter()
        self.record = {"request_id": request_id, "ts": now_iso(), "steps": {}, "error": None}

    @contextmanager
    def step(self, name: str):
        t = time.perf_counter()
        try:
            yield
        finally:
            self.record["steps"][f"{name}_s"] = round(time.perf_counter() - t, 4)

    def set(self, **fields):
        self.record.update(fields)

    def finish(self) -> dict:
        self.record["latency_s"] = round(time.perf_counter() - self.t0, 4)
        with _lock:
            _recent.append(self.record)
            _by_id[self.record["request_id"]] = self.record
            if len(_by_id) > _recent.maxlen:
                live = {r["request_id"] for r in _recent}
                for k in [k for k in _by_id if k not in live]:
                    del _by_id[k]
        append_jsonl(TRACE_FILE, self.record)
        return self.record


def find_trace(request_id: str):
    return _by_id.get(request_id)


def recent_traces(limit: int = 200) -> list:
    with _lock:
        return list(_recent)[-limit:]
