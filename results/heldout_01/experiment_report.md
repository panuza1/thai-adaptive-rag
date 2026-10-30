# Frozen held-out experiment report

All measurements below come from `rows.jsonl` and `generation.jsonl`. The test sample was frozen before outcome inspection: 60 questions, 55 article groups, 3,223 corpus chunks, three retrieval repetitions, and four primary systems plus five retrieval ablations. The generation comparison has 60 matched questions per primary system. No test tuning occurred.

## Which method performs best?

B3 has the highest observed nDCG@5 among primary systems (0.931418); B1 has the lowest mean retrieval latency (17.49 ms). B3 and P1 tie on Recall@5 (0.983333). There is no single winner across all objectives. P1 has lower observed nDCG than each primary baseline.

## Does adaptive routing help?

Against B3, P1 reduces mean warm retrieval latency by 80.85%, including router overhead, and reranked pairs by 83.33%. Mean routing overhead is 0.230 ms. nDCG decreases by 0.008333; its paired article-cluster bootstrap interval is [−0.023433, 0.000000]. Equal observed recall is not proof of population equivalence. Against B1/B2, P1 has higher recall but lower nDCG and substantially greater latency.

## Answer generation and resource measurements

Each system uses the same pinned Qwen2.5-0.5B-Instruct model, Thai prompt, five passages and greedy decoding with 128 new tokens. Strict normalized exact match is format-sensitive: explanatory text and citations can yield zero even when the reference answer is present. It is not semantic accuracy.

| System | Strict EM | Input tokens/query | Output tokens/query | Estimated request seconds | Estimated process CPU seconds/request | Token-cap responses |
|---|---:|---:|---:|---:|---:|---:|
| B1 | 0.0333 | 1924.32 | 59.40 | 42.275 | 158.966 | 12/60 |
| B2 | 0.0333 | 1904.27 | 51.15 | 41.758 | 157.287 | 11/60 |
| B3 | 0.0167 | 1917.45 | 54.58 | 42.841 | 162.460 | 11/60 |
| P1:none | 0.0333 | 1940.22 | 60.82 | 43.495 | 164.289 | 12/60 |

P1 shows **no observed overall cost saving** against B3: estimated request wall time is 1.53% higher, estimated process CPU time is 1.13% higher, and total input-plus-output tokens are 1.47% higher. Generation dominates runtime. The paired estimated request-time difference is +0.6545 seconds, with exploratory 95% interval [−0.5456, 1.8908]; no stable speedup or slowdown is established by this interval.

Estimated request durations sum the saved retrieval repeat-0 duration and a separately measured generation duration. They are not direct full-request timing. Retrieval summaries elsewhere average all three repeats. Generation has one run per query/system; the final five records were resumed after interruption, so session drift is an additional limitation. CPU time sums process time across threads and can exceed wall time.

The complete held-out run consumed 461,175 input tokens and 13,557 output tokens. Measured generation segments total 10,136.49 wall seconds and 38,206.47 process CPU seconds. Retrieval, including all repeats/ablations, totals 347.35 wall seconds and 1,550.36 process CPU seconds; shared setup takes 158.07 wall seconds. These exclude downloads, model loading, analysis and idle intervals. API charges are USD 0 because inference is local. Electricity, amortized hardware cost and total financial cost were not measured.

## Ablations and failure cases

Removing reranking gives the highest observed nDCG across the nine configurations (0.939880) at 19.25 ms/query, but reduces Recall@5 to 0.966667. It therefore exposes a weakness in the full policy; selecting it after viewing this test is exploratory. Length/keyword removals do not change aggregate quality here. Removing confidence reduces recall; removing hybrid retrieval reduces both recall and nDCG. See the complete ablation table and plot.

Six questions have positive routing regret versus the best per-query primary baseline. Four are sent to reranking despite a better alternative, and two remain on dense retrieval despite a better alternative. A short underspecified band-nationality question illustrates source-context dependence in the converted QA task. Generation can contradict retrieved evidence, and long citation IDs can exhaust the token budget. See `failure_analysis.md` for traceable examples.

## Supported research contribution and remaining gates

The defensible contribution is a reproducible, overhead-inclusive Thai study of a transparent retrieval decision policy, including its negative results and ablation evidence. It demonstrates retrieval-stage savings relative to always-reranking on this sample, but does not establish a general cost benefit, new algorithmic novelty, better answers or reduced hallucinations. A learned router is not justified by these results alone.

Independent human semantic correctness, claim faithfulness, unsupported-claim rate and hallucination comparisons remain **pending**, with annotation coverage 0/240. The blinded packet is ready; judgments must not be inferred from retrieval recall, exact match or selected assistant-reviewed cases. Balanced abstention evaluation also requires validated unanswerable questions. Direct request timing, broader untouched evaluation, residual duplicate sensitivity, literature-detail checks and final conference typesetting remain outstanding.
