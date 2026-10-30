# Paired statistical validation

Source: `results/e2e_01`. 60 paired questions from 55 article groups. Cluster percentile bootstrap: 2,000 resamples, seed 2027.

| Method | Mean seconds [95% CI] | Median seconds [95% CI] | p95 seconds [95% CI] |
|---|---:|---:|---:|
| B1 | 41.7654 [39.9111, 43.4943] | 41.8385 [39.6533, 43.1878] | 53.5094 [49.4855, 57.5443] |
| B2 | 40.5896 [38.4807, 42.6152] | 42.0511 [39.6727, 43.6601] | 54.0611 [48.1520, 57.2021] |
| B3 | 42.1408 [40.2721, 43.9743] | 43.0269 [40.7263, 45.0438] | 52.8824 [49.6373, 56.6446] |
| P1:none | 42.4885 [40.5450, 44.4500] | 41.6603 [39.2993, 45.0254] | 55.2722 [52.3148, 57.1660] |

## Paired mean differences

| Comparison | Metric | Difference | 95% interval |
|---|---|---:|---|
| B1 - B2 | recall | -0.016667 | [-0.05, 0.0] |
| B1 - B2 | ndcg | -0.003110 | [-0.04015373299031427, 0.03593402761820425] |
| B1 - B2 | end_to_end_seconds | 1.175802 | [-0.1254313281592569, 2.4670348569050544] |
| B1 - B3 | recall | -0.033333 | [-0.08333333333333333, 0.0] |
| B1 - B3 | ndcg | -0.008205 | [-0.04190869401240051, 0.02599512293589235] |
| B1 - B3 | end_to_end_seconds | -0.375410 | [-1.7515122478513332, 0.9101855096093678] |
| B1 - P1:none | recall | -0.033333 | [-0.08333333333333333, 0.0] |
| B1 - P1:none | ndcg | 0.000129 | [-0.03008951043333111, 0.03243518031061509] |
| B1 - P1:none | end_to_end_seconds | -0.723120 | [-1.726897148967311, 0.24748912061051556] |
| B2 - B3 | recall | -0.016667 | [-0.05172413793103448, 0.0] |
| B2 - B3 | ndcg | -0.005095 | [-0.047857189381000045, 0.034095069517198005] |
| B2 - B3 | end_to_end_seconds | -1.551212 | [-3.0049371137335776, -0.11338275150723016] |
| B2 - P1:none | recall | -0.016667 | [-0.05172413793103448, 0.0] |
| B2 - P1:none | ndcg | 0.003239 | [-0.04121217955197717, 0.044289060059101965] |
| B2 - P1:none | end_to_end_seconds | -1.898921 | [-3.460868009734719, -0.24106409690906144] |
| B3 - P1:none | recall | 0.000000 | [0.0, 0.0] |
| B3 - P1:none | ndcg | 0.008333 | [0.0, 0.023433143231290723] |
| B3 - P1:none | end_to_end_seconds | -0.347709 | [-1.897360930494347, 1.207559062512049] |

Exploratory percentile intervals, no multiplicity correction or formal hypothesis tests; no significance/equivalence claims. p95 depends on few observations; single-session variability is not cross-session reproducibility.
