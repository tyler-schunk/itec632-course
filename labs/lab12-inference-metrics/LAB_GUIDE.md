# Lab 12 - Inference Performance Metrics on Real Hardware

Chapter 9 of *AI Engineering* ("Understanding Inference Optimization") explains how to measure an inference service: time to first token (TTFT), time per output token (TPOT), throughput, goodput, and utilization (MFU and MBU), and why prefill is compute-bound while decode is memory-bandwidth-bound. In this lab you measure all of it on the course cluster: three Mac Studio M3 Ultra machines running oMLX behind a LiteLLM gateway. You time streamed responses from `qwen-moe`, `qwen-dense` and `qwen-small`, watch TTFT grow with prompt length, send parallel requests to see the throughput/latency trade-off, and finish with a capacity estimate: how many Larkspur Ridge IT technicians could this cluster serve at a response-time target you define?

**Where you'd use this at work:** Capacity planning for AI works like capacity planning for any service: a response-time target (SLO), p90 latency, and how many users one server can support. You produce the estimate a manager asks for before buying hardware.

## Where you'll work

Cluster notebook `lab12_cluster.ipynb` in your local Docker JupyterLab, on the KU VPN. About **4-5 hours**, including 20-30 minutes of waiting while measurements run. The notebook sends about 120 requests in total (136 if you do the optional 8-way test).

## Module objectives

| MO | Objective | CO |
|---|---|---|
| MO 12.1 | Measure TTFT, TPOT, total latency and output speed from streamed responses, and report them as medians and p90 (Bloom: Apply) | CO4 |
| MO 12.2 | Analyze measured differences between MoE, dense and small models using prefill vs decode, compute-bound vs memory-bandwidth-bound, and MBU (Bloom: Analyze) | CO1, CO4 |
| MO 12.3 | Analyze how prompt length and concurrency change latency, throughput and goodput against a service-level objective (Bloom: Analyze) | CO4 |
| MO 12.4 | Estimate the serving capacity of a deployment for a real user population and defend the assumptions (Bloom: Evaluate) | CO4, CO5 |

## Steps

1. Connect to the KU VPN, run `docker compose up`, open `labs/lab12-inference-metrics/lab12_cluster.ipynb`.
2. Read the first part of Chapter 9, "Understanding Inference Optimization": "Inference Overview" (including "Computational bottlenecks"), "Inference Performance Metrics" and "AI Accelerators". It ends where the section "Inference Optimization" starts. Keep it open for the analysis.
3. **Setup:** run the setup cell. It records the time you started (in UTC). Write down your local time too.
4. **Part A (guided):**
   - A1: finish `compute_metrics()` (TTFT, TPOT, total latency, tokens/second) and check that `total ~= TTFT + TPOT x (n - 1)`.
   - A2: measure all three models 6 times each; read the median and p90 table.
   - A3: read the course cluster table (which model runs at which precision on which Mac), predict which model decodes fastest, then compute the bandwidth "speed limit" and MBU for each model.
   - A4: measure TTFT at about 500, 2K and 8K prompt tokens for `qwen-moe` and `qwen-dense`, and estimate prefill speed.
5. **Part B (applied):**
   - B1: define your SLO; finish `run_burst()` (parallel requests with `asyncio.gather`) and `burst_metrics()` (throughput, goodput, SLO pass rate).
   - B2: run the concurrency sweep (1, 2, 4 parallel) **once**, and read the table, the plots, and the slowest-requests table.
   - B3 (optional): the 8-way test, only if your instructor announces the higher limit.
   - B4: set your capacity assumptions and compute how many technicians the cluster could serve.
6. Answer the five analysis questions and the AI-use reflection in the notebook.
7. Run the final `ck.report()` cell, save, and download the notebook.

## What to submit

- `lab12_cluster.ipynb` **with all outputs** (File > Download). The optional `lab12_measurements.csv` the notebook writes is not required.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (scaled from the `ck.report()` line) | 50 | Grading script |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and trade-offs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

Your numbers will differ from classmates' (different times, different cluster load). That is expected and is not graded; your explanation of them is. Checks that depend only on cluster behavior (for example whether `qwen-dense` decoded more slowly) are recorded but not graded.

## Getting unstuck

- **`RateLimitError` / HTTP 429 in the `error` column:** you sent more than 4 requests at once or more than 60 per minute. Wait a minute and re-run only the cell that failed. Do not raise the concurrency above 4 unless the instructor announced it.
- **Numbers look strange (a 10-second TTFT in the middle of normal ones):** that is probably a classmate's long request or the VPN. Keep it; discuss it in Q4. Re-run a cell only if most requests failed.
- **`SyntaxError: 'await' outside function`:** you are running the code as a script, not in Jupyter. Run cells in the notebook, in order.
- **All metrics are `None`:** `compute_metrics()` is not finished yet. Fix it, re-run its cell, then re-run the cells after it.
- Ask Copilot Chat with the exact error message, and paste the function you are working on.
