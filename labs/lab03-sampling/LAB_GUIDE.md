# Lab 03 - Post-Training and Sampling

The second half of Chapter 2 of *AI Engineering* explains two things that shape every answer a model gives. **Post-training** (supervised finetuning and preference finetuning) turns a text-continuation model into an assistant. **Sampling** picks each output token from a probability distribution, which explains why models can be creative, inconsistent, and sometimes confidently wrong. In this lab you turn the sampling knobs (temperature, top-k, top-p) on a small model in Colab, watch what each one does to the next-token probabilities and to real answers, choose the settings you would ship for Larkspur's help-desk assistant and for client announcements, measure how temperature changes diversity and hallucination on Larkspur questions, and compare a base model with its post-trained sibling. Then, on the course cluster, you test whether `qwen-moe`'s "thinking" mode (a way to spend more compute at inference time, related to what Chapter 2 calls test time compute) is worth its cost for SLA due-date questions that Larkspur's technicians ask every day, and whether `temperature=0` really makes answers repeatable.

**Where you'd use this at work:** Every AI product exposes temperature and "reasoning" settings. Knowing what they do lets you choose settings for a help-desk bot (consistent answers) versus a writing assistant, and decide whether a reasoning mode is worth its slower, pricier answers.

## Where you'll work

| Notebook | Where | Time |
|---|---|---|
| 1. `lab03_colab.ipynb` | Google Colab, free T4 GPU | about 1.5 hours |
| 2. `lab03_cluster.ipynb` | Your Docker JupyterLab, on the KU VPN | about 2 hours (including about 15 minutes of waiting for thinking runs) |

Do the Colab notebook first; the cluster notebook builds on it.

## Module objectives

| MO | Objective (Bloom level) | CO |
|---|---|---|
| MO 3.1 | Configure temperature, top-k, and top-p for a given task and explain their effect on the next-token distribution and on generated text (Bloom: Apply) | CO1 |
| MO 3.2 | Measure how sampling settings affect output diversity, answer consistency, and hallucination (Bloom: Analyze) | CO1, CO2 |
| MO 3.3 | Compare a base model with its post-trained version to explain the effects of supervised and preference finetuning (Bloom: Analyze) | CO1 |
| MO 3.4 | Evaluate the accuracy, latency, and token cost of thinking versus non-thinking modes on a multi-step task (Bloom: Evaluate) | CO2, CO4 |

## Steps

**Reading:** Chapter 2, "Post-Training" (including "Supervised Finetuning" and "Preference Finetuning") and "Sampling" (including "Sampling Fundamentals", "Sampling Strategies", "Test Time Compute", "Structured Outputs", and "The Probabilistic Nature of AI"). Optional preview for the thinking experiment: Chapter 5, "Give the Model Time to Think".

**Colab notebook**
1. Open `labs/lab03-sampling/lab03_colab.ipynb` in Google Colab and select **Runtime > Change runtime type > T4 GPU**.
2. Run the setup cells (the model downloads take a few minutes).
3. **Part A:** read the next-token probabilities for a help-desk prompt, predict and then measure what temperature, top-k, and top-p do to them (the helpers are provided; you choose settings and record what you see), write the `generate()` call that samples real answers with your settings, and pick recommended settings for two Larkspur jobs (policy answers and a client announcement).
4. **Part B:** finish `distinct_n` and run the diversity experiment; complete the consistency/hallucination loop; load the base model and complete the entropy and observation TODOs.
5. Answer analysis Q2 and Q3 (Q1 is optional and not graded), run `ck.report()`, and download the .ipynb (File > Download > Download .ipynb).

**Cluster notebook**
6. Connect to the **KU VPN**, run `docker compose up`, and open `labs/lab03-sampling/lab03_cluster.ipynb`.
7. **Part A:** compare one thinking and one non-thinking request, finish `extract_answer`, and test `temperature=0` consistency.
8. **Part B:** read the SLA printout and the worked example, work out one due time (S4) by hand, then run the 8-question SLA benchmark in both modes (16 requests; thinking requests are slow, so let it run), build the summary table, inspect one reasoning trace, and re-test consistency at `temperature=0`.
9. Answer analysis Q4-Q6 and the **AI-use reflection** (it covers both notebooks), run `ck.report()`, and save.

## What to submit

Upload **both** notebooks **with outputs** in one Canvas submission:
- `lab03_colab.ipynb`
- `lab03_cluster.ipynb`

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (both notebooks, scaled from the two `ck.report()` lines) | 50 | Grading script |
| Written analysis (Q2-Q3 in Colab, Q4-Q6 on the cluster; Q1 is optional) | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and trade-offs (10) |
| AI-use reflection (in the cluster notebook) | 10 | Complete and specific (10), generic (5), missing (0) |

## Getting unstuck

- **A.2 or A.3 "read off" checks fail:** copy the numbers from the table exactly as printed (`top1_prob` is a fraction such as 0.42, not 42). If you re-ran the table with different temperatures, re-run your read-off cell and its check too.
- **A.4 errors with "temperature" in the message:** with sampling on, every temperature must be above 0. Temperature 0 means greedy, which is sampling off (A.5 handles that case for you).
- **Colab runs out of memory when loading the base model:** Runtime > Restart session, then Run all (both 1.7B models fit only if nothing else was loaded first).
- **`nan` or `inf` errors:** change `DTYPE` to `torch.float32` in the setup cell (the T4 has no bfloat16 support). float32 uses twice the memory, so restart the session first.
- **Thinking accuracy is 0 or very low:** accuracy itself is not graded (report what you got), but check that answers are being read: look at `bench_df[["qid", "think", "predicted", "reference"]]`. If `predicted` is `None`, the model did not write the `ANSWER:` line or `extract_answer` missed it; print one raw `answer` to see the format.
- **A thinking request seems stuck:** it can take over a minute. If a request times out, the loop records an error and continues; you need at least 14 of 16 to pass the check, so re-run B.1 if many failed.
- Paste the exact error into Copilot Chat. For the SLA questions, try working one out by hand first; it makes the reasoning traces much easier to judge.
