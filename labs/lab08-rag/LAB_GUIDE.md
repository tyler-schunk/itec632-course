# Lab 08 - Retrieval-Augmented Generation (Co. app v2)

Chapter 6 of *AI Engineering* introduces retrieval-augmented generation (RAG): instead of hand-picking context, the application retrieves the most relevant pieces of its knowledge base for each question and gives them to the model. In this lab you set up and compare the parts of a retriever:
- chunking (fixed size versus by heading), which you write;
- term-based retrieval with a BM25 index, which you build;
- embedding retrieval and hybrid retrieval with reciprocal rank fusion, which are provided for you to run and interpret;
- reranking, with a fallback you write for when the reranker is down.

You measure each setup with recall@k and MRR (provided) against the gold evaluation set and choose the configuration your numbers support. Then you plug retrieval into **Co. app v2** and evaluate it end to end: answer accuracy, trap questions where outdated documents lurk, and whether it admits when it doesn't know.

**Where you'd use this at work:** "Chat with our knowledge base" is the most common AI project in IT. The settings you test here (chunking, keyword versus semantic versus hybrid search, reranking) are the same ones you configure in commercial RAG products, and the failure diagnosis is how you troubleshoot them.

## Where you'll work

- **Cluster notebook:** `lab08_cluster.ipynb` in your Docker JupyterLab, on the KU VPN. In Part B you also edit `coapp/retrieve.py` and `coapp/assistant.py` in the JupyterLab editor.
- **Time:** about 4.5-5 hours: about 2-2.5 hours for Part A (including a few minutes of waiting while the corpus is embedded), 1.5 hours for Part B, and 1 hour for the analysis. The notebook names the library calls you need, and the search math (cosine similarity, fusion, metrics) is provided.
- **Cluster use:** about 230 requests:
  - about 45 batched embedding calls for the corpus (one time; cached in `.coapp_cache/`),
  - about 65 rerank calls,
  - about 115 calls for the end-to-end evaluation (cached in `lab08_app_results.jsonl`).

## Module objectives

| MO | Objective | CO |
|---|---|---|
| MO 8.1 | Compare fixed-size and structure-based chunking strategies and their trade-offs (Bloom: Analyze) | CO3 |
| MO 8.2 | Apply term-based (BM25), embedding-based, and hybrid (RRF) retrieval, plus reranking with a graceful fallback (Bloom: Apply) | CO3 |
| MO 8.3 | Evaluate retrievers with recall@k and MRR against gold source documents (Bloom: Evaluate) | CO2, CO3 |
| MO 8.4 | Build a retrieval-augmented assistant that prefers current document versions, and evaluate it end to end (Bloom: Create) | CO3 |
| MO 8.5 | Diagnose RAG failures as retrieval, stale-context, or generation errors (Bloom: Analyze) | CO2, CO3 |

## Steps

1. Read Chapter 6, the "RAG" section: "RAG Architecture", "Retrieval Algorithms" (including the sidebar "Sparse Versus Dense Retrieval", "Term-based retrieval", "Embedding-based retrieval", "Comparing retrieval algorithms", and "Combining retrieval algorithms"), and "Retrieval Optimization" (especially "Chunking strategy" and "Reranking"). Skim "Query rewriting" and "Contextual retrieval".
2. Open `labs/lab08-rag/lab08_cluster.ipynb` and run the setup cell.
3. **Part A** (guided practice):
   - A1: write `chunk_by_heading()` and compare it with fixed-size chunks.
   - A2: build a BM25 index and search it.
   - A3: embed the corpus in batches (cached), then predict and check whether BM25 or the provided embedding search handles a paraphrased question better.
   - A4: predict and check how reciprocal rank fusion (provided) merges two rankings.
   - A5: reranking with a fallback when the reranker fails.
   - A6: compare every setup on recall@k and MRR (provided), then choose the configuration and decide whether reranking is worth its extra request.
4. **Part B** (applied lab), building the Co. app v2:
   - B1-B2: complete the TODOs in `coapp/retrieve.py` (`chunk_doc`, `prefer_current`; `rrf_fuse` is provided). You can paste your Part A code: the Part A helpers (`make_chunk`, `merge_small`, `heading_of`, `split_long`) are already in `retrieve.py` under the same names.
   - B3: complete the TODO in `coapp/assistant.py` (call `retrieve`), then run the smoke test.
   - B4: run the end-to-end evaluation on 30 gold questions.
   - B5: diagnose three wrong answers.
5. Answer the four **written analysis** questions with your own numbers, citing Chapter 6.
6. Complete the **AI-use reflection**.
7. Run the notebook top to bottom, check that `ck.report()` printed, and save.

`coapp_reference/` is a complete v2. Read it if you're stuck. Lab 9 builds on it.

## What to submit

Upload to Canvas:
- `lab08_cluster.ipynb` **with outputs**
- `coapp/retrieve.py`
- `coapp/assistant.py`

Don't upload `.coapp_cache/`.

## Grading

| Component | Points | How graded |
|---|---|---|
| Auto-checks | 50 | The grading script reads the `ck.report()` summary line and scales your check score to 50 |
| Written analysis | 40 | Uses your own results (15), correct concepts with chapter citation (15), clear reasoning and trade-offs (10) |
| AI-use reflection | 10 | Complete and specific (10), generic (5), missing (0) |

## Getting unstuck

- **The embedding cell is slow:** the first pass over about 800 chunks takes a few minutes, because it paces itself to stay under your key's token limit. After that, the vectors load from `.coapp_cache/` in a second. If you change how chunks are made, the texts change and the corpus is embedded again, so settle your chunking first.
- **Rate-limit errors (429):** wait a minute and rerun the cell. Embeddings already saved to the cache aren't redone, and the B4 evaluation picks up where it stopped.
- **The rerank call fails:** that's what the fallback is for. Your table then shows hybrid+rerank equal to hybrid, and `a6_rerank_failed_calls` is above 0. Mention it in Q1. Tell the instructor if it fails every time.
- **You fixed `retrieve.py` or `assistant.py` but the B4 numbers didn't change:** save the file and rerun the reload cell before B4. The B4 cache is keyed by your code, so changed code gets fresh answers. To start B4 over completely, delete `lab08_app_results.jsonl`.
- **`b3_retrieval_used` fails:** the TODO in `coapp/assistant.py` still has `chunks = []`. Save the file after editing, then rerun the reload cell.
- **Anything else:** ask Copilot Chat about the exact error, and paste in the traceback and the cell.
