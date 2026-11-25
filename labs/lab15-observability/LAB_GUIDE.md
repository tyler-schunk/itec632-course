# Lab 15 - Monitoring, Routing, and User Feedback

A deployed assistant you can't see into is one you can't fix or improve. In this lab you finish the Larkspur Co. app's architecture with the second half of **Chapter 10** of *AI Engineering*:
- a **model router** that sends simple questions to the small, cheap `qwen-small` and harder ones to `qwen-moe`,
- a **trace** for every request (one JSON line with route, model, retrieved documents, tool calls, tokens, latency per step, guardrail actions and errors),
- a **`POST /feedback`** endpoint for thumbs up/down.

Then you simulate 40 user sessions against your service, analyze the traces (latency percentiles per route, router accuracy, failure categories, token cost, feedback rate), and build a small monitoring **dashboard**. You also add two responsible-AI habits: telling users that answers are AI-generated, and logging only redacted text.

**Where you'd use this at work:** Once an AI service is live, IT owns it. Logs, traces, dashboards, alert thresholds, and user feedback tell you when it breaks or drifts. This is the monitoring side of running AI in production.

## Where you'll work

- **Cluster notebook:** `lab15_cluster.ipynb` in your local Docker JupyterLab, with the **KU VPN** on.
- **Plus a terminal on your own computer** to run `docker compose up --build` in this folder. **Stop the Lab 14 service first**, because both use port 8000.
- **Time:** about 4-5 hours. The simulated sessions take 5-15 minutes of waiting.
- **Cluster use:** about 200 requests. The notebook paces itself.

This folder's `app/` already contains a working help-desk service (with guardrails and a fallback route) plus the new Lab 15 files, so you can do this lab even if your Lab 14 service didn't fully work.

## Module objectives

| MO | Objective | CO |
|---|---|---|
| MO 15.1 | **Implement** a query router that chooses between a small and a large model, and compare a heuristic router with a model-based classifier (Bloom: Apply) | CO4, CO5 |
| MO 15.2 | **Construct** per-request traces and a feedback endpoint that link every rating to the exact request it rates (Bloom: Create) | CO5 |
| MO 15.3 | **Analyze** traces for latency percentiles, router accuracy, failure categories, token cost and feedback rate (Bloom: Analyze) | CO2, CO5 |
| MO 15.4 | **Design** a monitoring dashboard and alert thresholds for an AI application, based on Ch. 10's monitoring and observability metrics (Bloom: Create) | CO5 |
| MO 15.5 | **Evaluate** how user feedback should be collected and used, with responsible-AI practices for disclosure and logging (Bloom: Evaluate) | CO5, CO6 |

## Steps

1. Read Chapter 10, the second half: "Step 3. Add Model Router and Gateway" (Router, Gateway) again, "Monitoring and Observability" (Metrics, Logs and traces, Drift detection), "AI Pipeline Orchestration" (skim), and "User Feedback" (Extracting Conversational Feedback, Feedback Design, Feedback Limitations).
2. Stop your Lab 14 service. Open `labs/lab15-observability/lab15_cluster.ipynb`, plus `app/router.py` and `app/main.py`. Run **Run > Run All Cells** once to see what's left. Part A runs fully; Run All then stops on purpose at B2 (after a minute or two) until your Lab 15 service is running, so it doesn't send requests to a service that isn't there.
3. **Part A (guided):**
   - A1: implement `classify_heuristic()` in `app/router.py`, then compare it with the `qwen-small` classifier.
   - A2: read how a trace is built (`app/tracing.py`), predict the percentiles of a small example, and choose the dashboard number that shows the slow tail.
   - A3: implement `POST /feedback` in `app/main.py`, then predict how the simulated user rates three tricky answers and find its blind spot.
   - A4: log only the redacted question in the trace, and see the AI disclosure in each response.
4. **Part B (applied):**
   - B1: in a terminal **on your computer**, in this folder: `docker compose up --build`.
   - B2: simulate 40 user sessions: gold questions, paraphrases, out-of-scope requests and follow-ups, with simulated feedback.
   - B3: load your traces from `logs/traces.jsonl`. Compute latency per route, router accuracy, failure categories (write `failure_category()`), token cost and feedback rate. Optionally check your own key's usage on the gateway.
   - B4: build the dashboard (saved as `dashboard.png`).
   - B5: set alert thresholds and write "What I'd monitor in production".
5. Answer the four written-analysis questions using your own numbers, with chapter citations.
6. Complete the AI-use reflection, run the final cell, save. Stop the service.

New files in this folder (everything else is the working help-desk service: guardrails, fallback route and the Co. app):

| File | What it is |
|---|---|
| `app/router.py` | `choose_route()`: heuristic, classifier, hybrid or large-only (env `ROUTER_MODE` in `compose.yaml`) |
| `app/tracing.py` | `Trace` (times each step), JSONL writing, in-memory lookup by `request_id` |
| `app/main.py` | `/ask` now routes, traces and returns `request_id` + `disclosure`; new `POST /feedback` and `GET /traces` |
| `logs/` | `traces.jsonl` and `feedback.jsonl`, written by the service and read by your notebook |

**About logging on the course cluster:** the instructor's LiteLLM gateway logs every request your service sends (model, tokens, time and prompt text). You can't see those logs, but your own traces should match them: the same number of model calls per request and similar token counts. The notebook shows your own key's usage if the gateway allows it.

## What to submit

- `lab15_cluster.ipynb` **with outputs**, uploaded to Canvas. The last cell must show the self-check summary.
- Optional: `dashboard.png`.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (30 check points in the notebook, scaled) | 50 | Grading script reads the `ck.report()` line |
| Written analysis (4 questions + "What I'd monitor in production") | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and trade-offs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

## Getting unstuck

- **The notebook can't reach the service** (`service_health` fails). This is the same fix as Lab 14. On Linux, the course `compose.yaml` already has the `extra_hosts` line for `host.docker.internal`, but you must change the port line in **this** lab's `compose.yaml` from `"127.0.0.1:8000:8000"` to `"8000:8000"` and rebuild. Or use Plan B in the notebook. Check that `/health` shows `"version": "lab15-1.0"`. If it shows `lab14`, your old service is still running.
- **`traces_complete` fails, or the notebook finds 0 traces.** Open `logs/traces.jsonl` in JupyterLab. If it's missing, the container can't write to `logs/`. On Linux, run `chmod 777 logs` in this folder on your computer and restart the service. The notebook falls back to `GET /traces` automatically, so the analysis still works.
- **`feedback_posted` fails with 501.** The container still runs the old code. Stop it and run `docker compose up --build` after finishing the A3 TODO.
- **You can't get the service running at all.** Run the last cell (`ck.report()`) on its own so your Part A checks are recorded, and explain what happened in your analysis.
- **Router accuracy looks low.** That's a finding, not a bug (the notebook explains why next to the table). The gold set's `difficulty` describes how hard a question is for a *person*, which isn't the same as whether it needs the large model. Look at which questions disagree and discuss it in Q3.
- Anything else: ask Copilot Chat with the exact error text, then email the instructor with a screenshot.
