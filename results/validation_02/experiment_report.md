# Final validation report

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

Independent semantic correctness and faithfulness: pending (no human raters). Automated strict exact match and qualitative evidence cases remain in the original report and routing analysis. No hallucination-reduction claim.

## P1 comparisons

- P1 minus B1: 0.723120 seconds, 95% cluster interval [-0.24748912061051556, 1.726897148967311].
- P1 minus B2: 1.898921 seconds, 95% cluster interval [0.24106409690906144, 3.460868009734719].
- P1 minus B3: 0.347709 seconds, 95% cluster interval [-1.207559062512049, 1.897360930494347].

Original retrieval report: `../heldout_01/experiment_report.md`. Original raw results remain unchanged. Direct request timing includes all online work; it does not measure electricity or amortized hardware cost. Generation-stage timings in the original report are from the separate original run; the integrated benchmark does not isolate generation alone.
