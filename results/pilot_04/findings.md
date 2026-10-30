# Observed retrieval findings

Split: development; queries: 30; repetitions: 1. Fixed heuristic, no test tuning.

| System | Recall@5 | MRR@5 | nDCG@5 | Mean seconds | Router seconds |

|---|---:|---:|---:|---:|---:|

| B1 | 0.933333 | 0.886111 | 0.897689 | 0.017701 | 0.000000 |

| B2 | 0.966667 | 0.933333 | 0.942062 | 0.027503 | 0.000000 |

| B3 | 0.966667 | 0.966667 | 0.966667 | 1.185838 | 0.000000 |

| P1:none | 0.966667 | 0.966667 | 0.966667 | 0.368337 | 0.000260 |

P1 versus B1: observed mean retrieval-time reduction -1980.87% (negative means slower); nDCG difference +0.068977.

P1 versus B2: observed mean retrieval-time reduction -1239.26% (negative means slower); nDCG difference +0.024605.

P1 versus B3: observed mean retrieval-time reduction 68.94% (negative means slower); nDCG difference +0.000000.

Highest observed retrieval nDCG: B3 (ties possible). Lowest mean retrieval latency: B1. These are separate objectives.

Routing regret relative to the best per-query static baseline occurs on 0 of 30 queries. This is a label-informed diagnostic, not a deployable oracle.

## Paired uncertainty

Article-cluster bootstrap intervals from the same paired queries; exploratory, not proof of answer non-inferiority.

- P1:none - B1, ndcg: delta 0.068977, 95% interval [0.0, 0.1615736544215044].

- P1:none - B1, recall: delta 0.033333, 95% interval [0.0, 0.10344827586206896].

- P1:none - B1, retrieval_seconds: delta 0.350636, 95% interval [0.14083603142232617, 0.6003765029922697].

- P1:none - B2, ndcg: delta 0.024605, 95% interval [0.0, 0.06363280110836939].

- P1:none - B2, recall: delta 0.000000, 95% interval [0.0, 0.0].

- P1:none - B2, retrieval_seconds: delta 0.340834, 95% interval [0.13186639099394326, 0.5904952448033293].

- P1:none - B3, ndcg: delta 0.000000, 95% interval [0.0, 0.0].

- P1:none - B3, recall: delta 0.000000, 95% interval [0.0, 0.0].

- P1:none - B3, retrieval_seconds: delta -0.817501, 95% interval [-1.0703391495649293, -0.539124590725916].

## Supported scope

The evidence can support a measured retrieval-quality/latency tradeoff for this fixed policy, corpus, sample and CPU configuration. It does not establish algorithmic novelty, answer correctness, reduced hallucinations or general Thai-domain superiority.

Generation correctness, faithfulness, direct request-level end-to-end latency, energy and hardware monetary cost require separate evidence. See generation outputs if present; missing annotations are not successful outcomes.