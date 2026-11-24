# Lab 13 - Inference Service Optimization

The second half of Chapter 9 of *AI Engineering* ("Inference Optimization") covers how to make a model service faster and cheaper: model compression such as quantization, and service-level techniques such as batching and prompt caching. This week you apply them to Larkspur Ridge IT's help-desk assistant on the course cluster. You measure what oMLX's prompt cache does to TTFT (and why the order of the prompt decides whether it works), compare sequential and concurrent processing, control output length, try routing easy questions to a small model, and connect quantization to the speed numbers you measured in Lab 12. The optional stretch builds a response cache (exact and semantic) and measures how often it is wrong.

## Where you'll work

Cluster notebook `lab13_cluster.ipynb` in your local Docker JupyterLab, on the KU VPN. **This is a Part-A-only week** (side project 3 is due): Part A takes about **2.5 hours** and is graded; Part B is an optional stretch worth up to 10 bonus auto-check points. Part A sends about 75 requests, several with about 6,000-token prompts; Part B adds about 30.

## Module objectives

| MO | Objective | CO |
|---|---|---|
| MO 13.1 | Measure the effect of prompt caching on TTFT and explain why prefix order and backend routing decide cache hits (Bloom: Analyze) | CO4 |
| MO 13.2 | Compare batching, output length control and model routing by their measured latency and cost (Bloom: Analyze) | CO4 |
| MO 13.3 | Estimate how quantization changes model memory and decode speed using memory-bandwidth reasoning (Bloom: Apply) | CO1, CO4 |
| MO 13.4 | Recommend and justify which serving optimizations a real application should adopt, with evidence (Bloom: Evaluate) | CO4, CO5 |

## Steps

1. Connect to the KU VPN, run `docker compose up`, open `labs/lab13-serving-optimization/lab13_cluster.ipynb`.
2. Read the second half of Chapter 9, the section "Inference Optimization": "Model Optimization" (especially "Model compression" and "Attention mechanism optimization", where the KV cache is explained) and "Inference Service Optimization" ("Batching", "Decoupling prefill and decode", "Prompt caching", "Parallelism"). For the optional Part B, also skim Chapter 10's "Step 4. Reduce Latency with Caches".
3. **Part A (graded):**
   - A1 Prompt caching: write `prefix_last()`, run the cache experiment once, compute the cold/warm speedup, and look at which Mac served each warm request.
   - A2 Batching: finish the `asyncio.gather` line and compare 8 tickets processed sequentially vs 4 at a time.
   - A3 Output length: write `request_cost()` and a concise-answer instruction; compare it with a hard `max_tokens` cap.
   - A4 Routing: write the `is_hard()` heuristic; compare all-`qwen-moe`, all-`qwen-small` and routed on latency, cost and a keyword quality check.
   - A5 Quantization: write `weight_gb()` and read the memory and speed-limit table (no GPU work).
4. **Part B (optional bonus):** set `RUN_PART_B = True`, finish `ResponseCache.lookup()` (exact match, then cosine similarity with a threshold), replay 50 help-desk questions, and read the threshold sweep.
5. Answer the four analysis questions and the AI-use reflection.
6. Run the final `ck.report()` cell, save, and download the notebook.

## What to submit

- `lab13_cluster.ipynb` **with all outputs**. If you did Part B, its results are in the same notebook.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks, Part A (scaled from the `ck.report()` line) | 50 | Grading script |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and trade-offs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |
| Part B stretch (optional) | up to 10 bonus | Bonus auto-checks, shown as `bonus_score` in the report |

## Getting unstuck

- **Warm requests are not faster than cold ones:** check that warm requests reuse the *same* tag and put the documents *first*. Then look at the `backend` column: `qwen-moe` runs on two Macs, each with its own cache, so the first warm request on the second Mac is cold.
- **`RateLimitError` (429) on long prompts:** your key allows 300,000 tokens per minute and these prompts are about 6,000 tokens each. Wait a minute and re-run only the failed cell.
- **The concise check fails:** make `CONCISE_STYLE` stricter (a sentence limit works better than "be brief").
- **Part B: every question is a miss:** your `lookup()` is still returning `"miss"`; run the unit-test cell after each TODO.
- Ask Copilot Chat with the exact error message, and paste the function you are working on.
