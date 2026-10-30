# Paired statistical validation

Source: `results/heldout_01`. 60 paired questions from 55 article groups. Cluster percentile bootstrap: 2,000 resamples, seed 2027.

| Method | Mean seconds [95% CI] | Median seconds [95% CI] | p95 seconds [95% CI] |
|---|---:|---:|---:|
| B1 | 0.0175 [0.0169, 0.0181] | 0.0178 [0.0166, 0.0182] | 0.0209 [0.0202, 0.0220] |
| B2 | 0.0251 [0.0238, 0.0266] | 0.0244 [0.0239, 0.0252] | 0.0318 [0.0290, 0.0366] |
| B3 | 1.0511 [1.0103, 1.0916] | 1.0381 [0.9994, 1.1066] | 1.2693 [1.2259, 1.4393] |
| P1:none | 0.2013 [0.1039, 0.3081] | 0.0182 [0.0177, 0.0190] | 1.1702 [0.8993, 1.3222] |

## Paired mean differences

| Comparison | Metric | Difference | 95% interval |
|---|---|---:|---|
| B1 - B2 | recall | -0.016667 | [-0.05, 0.0] |
| B1 - B2 | ndcg | -0.003110 | [-0.04015373299031427, 0.03593402761820425] |
| B1 - B2 | retrieval_seconds | -0.007610 | [-0.008713145388152495, -0.0066911808493653226] |
| B1 - B3 | recall | -0.033333 | [-0.08333333333333333, 0.0] |
| B1 - B3 | ndcg | -0.008205 | [-0.04190869401240051, 0.02599512293589235] |
| B1 - B3 | retrieval_seconds | -1.033640 | [-1.0739383550881625, -0.993092542768822] |
| B1 - P1:none | recall | -0.033333 | [-0.08333333333333333, 0.0] |
| B1 - P1:none | ndcg | 0.000129 | [-0.03008951043333111, 0.03243518031061509] |
| B1 - P1:none | retrieval_seconds | -0.183795 | [-0.2903058621966694, -0.08629132145282635] |
| B2 - B3 | recall | -0.016667 | [-0.05172413793103448, 0.0] |
| B2 - B3 | ndcg | -0.005095 | [-0.047857189381000045, 0.034095069517198005] |
| B2 - B3 | retrieval_seconds | -1.026031 | [-1.0661079587515003, -0.9861588643824609] |
| B2 - P1:none | recall | -0.016667 | [-0.05172413793103448, 0.0] |
| B2 - P1:none | ndcg | 0.003239 | [-0.04121217955197717, 0.044289060059101965] |
| B2 - P1:none | retrieval_seconds | -0.176186 | [-0.2823663327640777, -0.07898794957724709] |
| B3 - P1:none | recall | 0.000000 | [0.0, 0.0] |
| B3 - P1:none | ndcg | 0.008333 | [0.0, 0.023433143231290723] |
| B3 - P1:none | retrieval_seconds | 0.849845 | [0.7423371452971438, 0.9470451210926093] |

Exploratory percentile intervals, no multiplicity correction or formal hypothesis tests; no significance/equivalence claims. p95 depends on few observations; single-session variability is not cross-session reproducibility.
