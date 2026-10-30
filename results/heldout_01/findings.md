# Observed retrieval findings
Split: test; queries: 60; repetitions: 3. Fixed heuristic, no test tuning.
| System | Recall@5 | MRR@5 | nDCG@5 | Mean seconds | Router seconds |
|---|---:|---:|---:|---:|---:|
| B1 | 0.950000 | 0.913889 | 0.923213 | 0.017493 | 0.000000 |
| B2 | 0.966667 | 0.913056 | 0.926323 | 0.025103 | 0.000000 |
| B3 | 0.983333 | 0.913889 | 0.931418 | 1.051134 | 0.000000 |
| P1:none | 0.983333 | 0.902778 | 0.923085 | 0.201289 | 0.000230 |
P1 versus B1: observed mean retrieval-time reduction -1050.66% (negative means slower); nDCG difference -0.000129.
P1 versus B2: observed mean retrieval-time reduction -701.85% (negative means slower); nDCG difference -0.003239.
P1 versus B3: observed mean retrieval-time reduction 80.85% (negative means slower); nDCG difference -0.008333.
Highest observed retrieval nDCG: B3 (ties possible). Lowest mean retrieval latency: B1. These are separate objectives.
Routing regret relative to the best per-query static baseline occurs on 6 of 60 queries. This is a label-informed diagnostic, not a deployable oracle.
- Query oUNCj0S0anI3YTYCKL3X_000: selected C; nDCG 0.4307; oracle 1.0000; features {'length': 3, 'exact': False, 'margin': 0.0042760372161865234}.
- Query ICQ054THVjycHK3DNNt0_003: selected C; nDCG 0.6309; oracle 1.0000; features {'length': 12, 'exact': False, 'margin': 0.017958104610443115}.
- Query x4fSbfJrXClYXpMMSwja_002: selected C; nDCG 0.6309; oracle 1.0000; features {'length': 7, 'exact': False, 'margin': 0.0005936622619628906}.
- Query zcQWGlRuU1bLyQEaW2Ea_004: selected A; nDCG 0.6309; oracle 1.0000; features {'length': 13, 'exact': False, 'margin': 0.034128785133361816}.
- Query B4M37Q5xCcVGgB4IF5IV_002: selected A; nDCG 0.5000; oracle 0.6309; features {'length': 13, 'exact': False, 'margin': 0.0560452938079834}.
- Query vrMwo56XajptJAiH2Br0_004: selected C; nDCG 0.5000; oracle 0.6309; features {'length': 8, 'exact': False, 'margin': 0.013211607933044434}.
## Paired uncertainty
Article-cluster bootstrap intervals from the same paired queries; exploratory, not proof of answer non-inferiority.
- P1:none - B1, ndcg: delta -0.000129, 95% interval [-0.03243518031061509, 0.0300895104333311].
- P1:none - B1, recall: delta 0.033333, 95% interval [0.0, 0.08333333333333333].
- P1:none - B1, retrieval_seconds: delta 0.183795, 95% interval [0.0862913214528263, 0.2903058621966693].
- P1:none - B2, ndcg: delta -0.003239, 95% interval [-0.04428906005910197, 0.04121217955197717].
- P1:none - B2, recall: delta 0.016667, 95% interval [0.0, 0.05172413793103448].
- P1:none - B2, retrieval_seconds: delta 0.176186, 95% interval [0.07898794957724703, 0.2823663327640776].
- P1:none - B3, ndcg: delta -0.008333, 95% interval [-0.023433143231290726, 0.0].
- P1:none - B3, recall: delta 0.000000, 95% interval [0.0, 0.0].
- P1:none - B3, retrieval_seconds: delta -0.849845, 95% interval [-0.9470451210926094, -0.7423371452971437].
## Supported scope
The evidence can support a measured retrieval-quality/latency tradeoff for this fixed policy, corpus, sample and CPU configuration. It does not establish algorithmic novelty, answer correctness, reduced hallucinations or general Thai-domain superiority.
Generation correctness, faithfulness, direct request-level end-to-end latency, energy and hardware monetary cost require separate evidence. See generation outputs if present; missing annotations are not successful outcomes.
