# Lab 04: Evaluation Methodology - perplexity, exact metrics, and AI judges

Chapter 3 of *AI Engineering* argues that evaluation is the hardest part of building with foundation models, and it gives you a toolbox: language-modeling metrics (cross-entropy, perplexity, bits-per-byte), exact evaluation against reference answers (exact match, lexical and semantic similarity), and AI as a judge, with its well-known biases. In this lab you use every tool in that box on Larkspur Ridge IT's help-desk questions. You use perplexity and bits-per-byte to see which texts a model finds predictable and to flag garbled tickets automatically, score real model answers four different ways, and then test whether an LLM judge prefers its own family's answers or whichever answer it reads first. By the end you should know which metric to trust for which job, and why the help-desk assistant's evaluation can't rely on any single number.

**Where you'd use this at work:** Before an organization rolls out or renews an AI tool, someone has to show that it works on the organization's own questions. This lab gives you the methods: reference answers, AI judges and their biases, and spot checks by a person.

## Where you'll work

| Notebook | Environment | Time |
|---|---|---|
| `lab04_colab.ipynb` | Google Colab, free **T4 GPU** (loads small Hugging Face models) | about 45 minutes |
| `lab04_cluster.ipynb` | Your Docker JupyterLab on the **KU VPN** (course cluster) | about 2.5-3 hours |

Total: about 3.5 hours plus the Chapter 3 reading, including the written answers (1 question in the Colab notebook, 3 in the cluster notebook) and one AI-use reflection (in the cluster notebook). The two notebooks are independent; do them in either order.

## Module objectives

| MO | Objective (Bloom level) | CO |
|---|---|---|
| MO 4.1 | **Interpret** perplexity and bits-per-byte across texts, models, and tokenizers, and **use** them to flag abnormal text such as garbled tickets (Bloom: Apply) | CO1, CO2 |
| MO 4.2 | **Apply** exact match, token F1, and embedding similarity to help-desk answers, **identify** answers where each one gives the wrong verdict, and **choose** which to trust for a type of question (Bloom: Analyze) | CO2 |
| MO 4.3 | **Design** a scoring rubric and **use** an LLM as a judge with robust output parsing (Bloom: Create) | CO2 |
| MO 4.4 | **Measure** self-preference and position bias in LLM judges and their agreement with human labels (Bloom: Evaluate) | CO2 |
| MO 4.5 | **Recommend** an evaluation approach for the Larkspur help-desk assistant, justified with your own results and the chapter (Bloom: Evaluate) | CO2 |

## Steps

1. Read Chapter 3: "Challenges of Evaluating Foundation Models", "Understanding Language Modeling Metrics" (entropy through "Perplexity Interpretation and Use Cases"), "Exact Evaluation" (including "Similarity Measurements Against Reference Data" and "Introduction to Embedding"), "AI as a Judge" (including "How to Use AI as a Judge" and "Limitations of AI as a Judge"), and "Ranking Models with Comparative Evaluation". The analysis questions cite these sections.
2. **Colab:** open `lab04_colab.ipynb` in Colab (File > Open notebook > GitHub, or upload it), set the runtime to **T4 GPU**, and work through it top to bottom.
   - Part A: run the given `lm_metrics()` function on a Larkspur runbook and read its three numbers (cross-entropy, perplexity, bits-per-byte).
   - Part B: predict, then measure, how a runbook, the same text shuffled, random characters, a public-domain book, and your own paragraph rank; compare three models (one with a different tokenizer); see how context lowers perplexity; and pick a bits-per-byte threshold that flags a garbled ticket among real Larkspur tickets.
3. **Cluster:** with the VPN on, open `labs/lab04-eval-methods/lab04_cluster.ipynb` in your Docker JupyterLab.
   - Part A: run the given exact-match, token-F1, and embedding-similarity metrics, predict their verdicts before you look, try to fool token F1 with answers of your own, decide which metric you would trust for answers that are prices or times, and write an LLM-judge rubric.
   - Part B: get `qwen-small` answers to 25 gold questions (`corpus/larkspur-corpus/eval/`), score them four ways, run the judge-bias experiment with `qwen-moe` and `gemma-moe` and give your verdict on each bias from the numbers, and **label 10 answers yourself** to see which metric agrees with you.
4. Answer the written analysis questions in **each** notebook (Colab: Q1; cluster: Q1-Q3). The AI-use reflection is only in the cluster notebook and covers the whole lab. Questions marked *Optional* are not graded.
5. Run the final `ck.report()` cell in each notebook and save.

## What to submit

Upload **both** notebooks to Canvas, with all outputs visible:
- `lab04_colab.ipynb` (download it from Colab: File > Download > Download .ipynb)
- `lab04_cluster.ipynb`

Canvas accepts multiple files in one submission.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks (both notebooks, scaled) | 50 | Grading script reads the `ck.report()` line in each notebook |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and tradeoffs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

## Getting unstuck

- **Colab says "CUDA not available" or is very slow:** Runtime > Change runtime type > T4 GPU, then Runtime > Restart and run all. If you hit "CUDA out of memory" in B2, restart the runtime and run all again; the notebook frees each model before loading the next.
- **A Colab check about a prediction fails:** predictions are graded only on being filled in, not on being right. Check the spelling (`"higher"`/`"lower"`, the exact text and ticket names) and that you re-ran the check cell after editing.
- **A cluster verdict check fails (B3):** the check accepts any verdict the numbers support, and leaves borderline numbers to you. Compare your printed index or rate with the size guidance in the notebook and check the spelling of the verdict.
- **Judge scores come back as `None`:** print the raw judge reply. Usually the rubric lost its "Reply with JSON only" line, or a placeholder like `{answer}` was deleted. `parse_score()` already handles most messy outputs.
- **Rate-limit or timeout errors on the cluster:** just re-run the cell. Every reply is cached in `lab04_cache.json`, so finished requests are not sent again. Don't delete that file mid-lab.
- **You changed your rubric (or `build_messages()`):** just re-run the cells after it. The cache recognizes the changed prompt and asks the model again (about 80 requests for a full rubric change).
- Ask Copilot Chat with the exact error message and the cell that produced it; then check its suggestion against the TODO hint before pasting.
