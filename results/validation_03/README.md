# Frozen held-out benchmark audit (2026-11-06)

Reproduce without downloading models or rerunning experiments:

```bash
python -m src.audit_retrieval
```

The script checks that each frozen query belongs to the test partition, has existing gold chunk IDs, and has exactly one row per method/repetition. It independently recomputes Recall@5, MRR@5 and nDCG@5 for the 720 primary-system rows (60 queries × 4 methods × 3 repeats). The other 900 retrieval rows are five already-preserved P1 ablations. Raw results and qrels are not modified.

## Findings from `benchmark_audit.json`

- Corpus: **3,223 chunks**. Held-out sample: **60 queries from 55 article groups**.
- All 60 held-out queries have **exactly one annotated relevant chunk**. For this *particular* dataset, mean Recall@5 equals the fraction of queries that retrieved that one labeled chunk: B1 **57/60**, B2 **58/60**, B3 **59/60**, P1 **59/60**. This conversion is not valid for general multi-relevant retrieval tasks.
- **One query is missed by all four methods.** Improving the routing choice between these recorded rankings cannot raise label-defined Recall@5 above **59/60**.
- The best B1/B2/B3 nDCG score chosen *after seeing the labels for each query* averages **0.955391** versus B3's **0.931418** and P1's **0.923085**. This is an oracle ceiling for the recorded static rankings, not an estimated deployable router score.
- If a hindsight oracle chooses the cheapest static method that is **no worse than B3 on both labeled Recall and nDCG for each query**, observed retrieval time averages **50.72 ms** versus B3's **1,051.13 ms**; it picks B1/B2/B3 on 56/2/2 questions. This is *not* a proven 95% real-world speedup: the selector uses test labels, is not implementable, and single-session CPU timings are not production costs.

These findings suggest limited label-defined Recall headroom but some rank-order heterogeneity. They do **not** prove the corpus is easy, that the router is defective, or that answer quality improves. The original qrels are derived from one answer span, so an answer-bearing passage may be penalized when it is not among the annotated chunks. Pooling human passage judgments is still required.

## Next experiment: cheaper reranking baseline

`experiments/rerank_top10_dev.json` sets `rerank_k=10`, retaining `candidate_k=20` for initial Dense/Hybrid retrieval. The existing top-20 behavior is unchanged when `rerank_k` is omitted. Both B3 and the P1 C route use the same capped reranking candidates.

Run the new configuration on **development data only** in a fresh output directory:

```bash
python -m src.run --config experiments/rerank_top10_dev.json --output results/rerank_top10_dev_01
python -m src.analyze results/rerank_top10_dev_01
```

Model weights, dependencies and a suitable controlled CPU measurement environment are required; **this experiment has not been executed here**. It is an exploratory baseline, not a post-hoc change to the held-out test. Do not compare latency across dissimilar machines/sessions as a controlled speedup. If this approach looks worthwhile on development data, evaluate it against top-20 in an interleaved matched session on separate untouched validation data before claiming a benefit.
