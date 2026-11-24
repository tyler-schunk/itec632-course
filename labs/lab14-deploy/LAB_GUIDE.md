# Lab 14 - Deploying the Assistant

Until now the Larkspur help-desk assistant (the "Co. app") has run inside notebooks, and nobody on the service desk can use a notebook. In this lab you turn the Co. app v3 (retrieval + tools) into a small **web service**. It runs in its own **Docker container** and answers `POST /ask` over HTTP. You also add the first architecture layers that **Chapter 10** of *AI Engineering* describes. An **input guardrail** redacts PII and secrets and blocks out-of-scope requests. An **output guardrail** requires a citation or "I don't know" and strips key-like strings. A **gateway-style model route** retries on `gemma-moe` when `qwen-moe` fails or times out. Then you test the deployed service the way users reach it, over HTTP, and measure how much latency the service layer adds. Ch. 9 gives the deployment context (latency and throughput).

## Where you'll work

- **Cluster notebook:** `lab14_cluster.ipynb` in your local Docker JupyterLab, with the **KU VPN** on.
- **Plus a terminal on your own computer** (not in Jupyter) to run `docker compose up --build` in this folder. The course lab keeps running at the same time.
- **Time:** about 4-5 hours.
- **Cluster use:** about 200 requests. The notebook paces itself.

How the pieces connect:

```
your browser ──> JupyterLab (course container, port 8888)
                     │  lab14_cluster.ipynb calls http://host.docker.internal:8000
                     ▼
                 Co. app service (YOUR container from this folder, port 8000)
                     │  input guardrail -> qwen-moe (fallback gemma-moe) + retrieval + tools -> output guardrail
                     ▼
                 course LiteLLM gateway (KU VPN)
```

## Module objectives

| MO | Objective | CO |
|---|---|---|
| MO 14.1 | **Package** an LLM application as a container image that uses pinned dependencies, runs as a non-root user, and takes its secrets from the environment at run time (Bloom: Apply) | CO5 |
| MO 14.2 | **Implement** a FastAPI service with health and question endpoints that return a validated response schema (Bloom: Apply) | CO3, CO5 |
| MO 14.3 | **Construct** input and output guardrails and a fallback model route following Ch. 10's architecture steps (Bloom: Create) | CO5 |
| MO 14.4 | **Evaluate** a deployed service with an HTTP test suite and a small load test, comparing latency through the service and direct (Bloom: Evaluate) | CO2, CO4 |
| MO 14.5 | **Analyze** which Ch. 10 architecture components a system implements, and the latency and false-positive trade-offs of guardrails (Bloom: Analyze) | CO5 |

## Steps

1. Read Chapter 10, the first half: "AI Engineering Architecture", that is "Step 1. Enhance Context", "Step 2. Put in Guardrails" (input guardrails, output guardrails, guardrail implementation), "Step 3. Add Model Router and Gateway", "Step 4. Reduce Latency with Caches" and "Step 5. Add Agent Patterns". Skim Ch. 9's "Inference Performance Metrics" again.
2. Open `labs/lab14-deploy/lab14_cluster.ipynb` in JupyterLab. Also open `app/main.py`, `app/guardrails.py` and `app/gateway.py` (double-click them in the file browser). Run **Run > Run All Cells** once to see what's left. Part A runs fully. Part B needs your service running (B1), so until then the notebook reports after about 30 seconds that the service isn't reachable, skips the Part B requests, and leaves their checks red. That's expected.
3. **Part A (guided):** work through A1-A6. Some TODOs are in the notebook and some are in the `app/` files. Each TODO names its step.
   - A1: Docker concepts. Write a secret scanner for Dockerfiles and check that our Dockerfile and `compose.yaml` follow the rules.
   - A2: FastAPI basics. Add an endpoint to a demo app, then fix `/health` in `app/main.py`.
   - A3: PII/secret redaction patterns in `app/guardrails.py`.
   - A4: the out-of-scope check in `app/guardrails.py`.
   - A5: the citation rule of the output guardrail in `app/guardrails.py`.
   - A6: the fallback loop in `app/gateway.py`.
4. **Part B (applied):**
   - B1: in a terminal **on your computer**, in this folder, run `docker compose up --build`. Leave it running. Open http://localhost:8000/docs in your browser to see the API.
   - B2: run the HTTP test suite: health, 10 gold questions, guardrail tests (add your own; if one slips past the keyword rules, that's a finding to extend the patterns or discuss, not a failed check), and the fallback test.
   - B3: run the load test (service vs direct, and a paced burst of 20 overlapping requests), plus the guardrail cost and false-positive measurement.
   - **Whenever you change a file in `app/`, stop the service (Ctrl+C) and run `docker compose up --build` again.**
5. Answer the four written-analysis questions using your own numbers, with chapter citations.
6. Complete the AI-use reflection, run the final cell, save. Stop the service with Ctrl+C or `docker compose down`.

Files in this folder:

| File | What it is |
|---|---|
| `coapp/` | Co. app v3 reference (retrieval with BM25 + embeddings, read-only SQLite tools, `answer()`). You may replace it with your own Lab 9 version (see `coapp/__init__.py`). |
| `app/main.py` | The FastAPI service: `GET /health`, `POST /ask` |
| `app/guardrails.py` | Input guardrail (redaction, scope check) and output guardrail |
| `app/gateway.py` | Model route with fallback, and simulated failures for testing |
| `Dockerfile`, `.dockerignore`, `requirements.txt` | How the image is built |
| `compose.yaml` | How the container runs: your `.env`, the read-only corpus, port 8000 |
| `cache/` | Embedding cache shared by the notebook and the container (created at run time) |
| `data/fallback_qa.jsonl` | A small question set, used only if the course gold set is missing |

## What to submit

- `lab14_cluster.ipynb` **with outputs**, uploaded to Canvas. The last cell must show the self-check summary.
- You don't need to upload the `app/` files: the notebook's checks test them.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (30 check points in the notebook, scaled) | 50 | Grading script reads the `ck.report()` line |
| Written analysis (4 questions) | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and trade-offs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

## Getting unstuck

- **`service_health` fails, but http://localhost:8000/health works in your browser.** Your notebook runs inside the course container, where `localhost` means the container itself, so the notebook uses `http://host.docker.internal:8000`. Docker Desktop on Windows and Mac provides that name automatically.
  - **Linux:** the course `compose.yaml` (the one in the top folder) already maps `host.docker.internal` for you with `extra_hosts: - "host.docker.internal:host-gateway"`. If your copy of it is older and lacks those lines, add them under the `lab:` service and restart the course lab with `docker compose up`. You **do** still need one change in this lab's `compose.yaml`: change the port line from `"127.0.0.1:8000:8000"` to `"8000:8000"`, then run `docker compose up --build` again. On Linux, `host.docker.internal` points at Docker's bridge address, not 127.0.0.1, so a port published only on 127.0.0.1 can't be reached from the course container.
  - Still stuck? Use **Plan B** in the notebook: it runs the service inside the course container with uvicorn. Mention that in your analysis.
- **The build fails at `pip install`.** Check your internet connection. The image downloads packages from PyPI, which doesn't need the VPN, but some campus or VPN setups block it. Try again off the VPN for the build only, then reconnect before `docker compose up`.
- **The service starts but `/ask` returns 502 "all models failed".** The container can't reach the gateway. Check that the VPN is on and that the top-level `.env` has your URL and key (compose reads `../../.env`). The service terminal shows the error for each attempt.
- **Your edits don't seem to change anything over HTTP.** The container runs a copy of your code that was baked in when the image was built. Stop it and run `docker compose up --build`. The in-notebook checks in Part A use the files directly, so they update right away.
- **Port 8000 is already in use.** Another program, or your Lab 15 service, uses it. Stop the other one, or change the first `8000` in `compose.yaml` and set `COAPP_URL` (for example `os.environ["COAPP_URL"] = "http://host.docker.internal:8001"` before the setup cell).
- Anything else: ask Copilot Chat with the exact error text (from the notebook or the service terminal), then email the instructor with a screenshot.
