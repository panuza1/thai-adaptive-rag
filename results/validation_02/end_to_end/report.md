### Direct end-to-end latency validation

The integrated benchmark completed 240 requests on the same 60 frozen questions, with one request per method/question and balanced within-query execution positions. The reported interval starts before dense query encoding and ends after final answer decoding. No separate stage durations are added to obtain this measurement.

| Method | Mean (s) | Median (s) | p95 (s) | SD (s) |
|---|---:|---:|---:|---:|
| B1 | 41.765 | 41.839 | 53.509 | 7.312 |
| B2 | 40.590 | 42.051 | 54.061 | 8.439 |
| B3 | 42.141 | 43.027 | 52.882 | 7.370 |
| P1 | 42.489 | 41.660 | 55.272 | 7.823 |

Mean latency 95% article-cluster bootstrap intervals are B1 [39.911, 43.494] seconds; B2 [38.481, 42.615] seconds; B3 [40.272, 43.974] seconds; P1 [40.545, 44.450] seconds.

P1 versus B3 has an observed direct mean latency reduction of -0.83% (negative means slower). This comparison measures the complete warm request and should not be confused with the 80.85% retrieval-only reduction.

The P1-minus-B3 mean difference is 0.3477 seconds, with 95% interval [-1.2076, 1.8974]. No formal significance or equivalence test is claimed.

Rankings match the original run on 240/240 requests, and decoded answers match on 240/240 requests. Model revisions, thresholds, CPU thread count, prompt and generation budget remain fixed. The generator's recorded dtype is bfloat16 on CPU. The workstation was not isolated from other activity; the benchmark quantifies this session, not guaranteed production latency.

Median and p95 intervals and all six pairwise comparisons are retained in the supplementary statistical output. The p95 is sensitive to a few observations and only one request was timed per query/method.
