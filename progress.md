# Progress and evidence log

Updated 2026-10-29. This is a real research implementation in progress, not a completed or submission-ready study.

## Phase 0 — environment and conference verification

Completed: inspected empty workspace; preserved user data; CPU i5-12450H, 12 logical CPUs, ~32 GiB RAM, RTX 3050 4 GiB; ~24 GB initially available disk. Isolated Python 3.10 environment. CPU-only torch installed; no paid API used. Official AUCC pages and English DOCX template obtained. Deadline and page-count conflicts recorded in `paper/aucc_requirements.md`.

Evidence: downloaded template and extracted text; installation logs under `results/`. Next: organizer confirmation, author/advisor details and final template layout after results.

## Phase 1 — focused literature review

Completed: verified identities/links for 12 original works covering RAG, BM25, dense retrieval, fusion, reranking, adaptive routing, MIRACL and grounding evaluation. Defined candidate gap, questions and falsifiable hypotheses. Explicitly recognized close prior work on external-feature routing.

Unresolved: full-text dataset/metric details for several papers remain marked pending; exhaustive Thai-specific related-work search and latest 2026 literature screening are incomplete. No novelty claim established. Next: complete nearest-neighbor method comparison before final paper claims.

## Phase 2 — protocol and data

Completed: fixed B1/B2/B3/P1 controls; reproducible custom development/validation/test grouping of upstream training data; raw-span checking; deduplication; corpus without question/answer insertion. Data preparation observed 3,221 chunks, 5,667 retained questions (3,360 / 1,130 / 1,177). 94 exclusions logged. Upstream articles in this input each have a single context; code now asserts this. No test performance evaluated.

Evidence: `data/processed/manifest.json`, source SHA256 in README. Unresolved: near-duplicate and contamination audit, MIRACL secondary evaluation, independently labeled unanswerable examples. Next: development calibration followed by frozen validation and test protocol.

## Phase 3 — implementation

Completed in source: Thai normalization/chunking, BM25, E5 dense embeddings, RRF, cross encoder, rule router, five ablations, local generation, retrieval metrics, paired cluster bootstrap, plotting and routing cases. Six focused tests pass on the initial system Python; isolated environment test log records subsequent execution. Model APIs checked against official documentation/model cards.

Unresolved: neural end-to-end execution status is recorded below as downloads/runs complete. Generator and human-reliability assessment are not yet validated. No learned router: baseline evidence does not yet justify it. Next: run actual development baseline comparisons.

## Phase 4 — experimental evaluation

Running available development pilots. The independent BM25-only run is a sanity baseline, not B1/B2/B3/P1 evidence. Do not infer dense/adaptive or answer-quality results from it. Model download and install logs retained. Held-out retrieval, end-to-end generation, human correctness/faithfulness and abstention results pending.

## Phase 5 — ablations and statistics

Code implements feature removals and no-hybrid/no-reranking paths, cluster bootstrap and oracle-regret diagnostics. Actual neural ablation measurements pending execution; no significance claimed. Next: inspect route frequencies and errors before deciding whether to calibrate or learn a router.

## Phase 6 — paper

Completed: English content draft with required sections and verified linked references; pending findings explicitly labeled. Official template and formatting checklist archived. Unresolved: final experiment tables, human annotation, full reference formatting, typesetting/visual proof, authors, advisor certification and submission-date reconciliation. Next: populate only from verified outputs.

### Execution evidence update

- Independent BM25-only development sanity run completed on 30 questions against 3,221 chunks: Recall@5 0.966667, MRR@5 0.933333, nDCG@5 0.942062, mean warm retrieval 0.004743 seconds. These values are from `results/lexical_pilot/summary.json`; one run is not a stable latency estimate.
- Eight unit/data/metric/bootstrap tests pass in the isolated environment (`results/tests.log`).
- CPU torch and neural dependencies installed. `results/environment.lock.txt` records installed versions; model download/execution is in `results/pilot_01.log`.
- Generator supports `--limit` for a matched-query engineering smoke run. Such outputs must not be represented as held-out evaluation.

### Literature revision and transfer recovery

Expanded review with Thai QA, Thai legal hybrid/reranking, Thai Royal Gazette evidence retrieval (NLLP 2026), TSWAP and AB-RAG. These sources further narrow the contribution; draft now explicitly disclaims first Thai hybrid/query-dependent retrieval. Model download attempt `pilot_01` was manually interrupted after Xet stalled; retry `pilot_02` uses ordinary HTTP and the same resolved model revisions. No model evaluation measurements are attributed to the interrupted attempt.

### Data leakage correction

Corpus-only char-5gram audit (`results/data_audit.json`) found five cross-split candidates; manual title/text inspection identified two duplicate-article pairs and three distinct-entity/template pairs. Preparation v2 now joins identical normalized titles OR contexts into connected components before splitting. Saved separately as `data/processed_v2` to preserve the in-progress v1 run. New counts: development 3,360, validation 1,133, test 1,174. Six assignments changed. All 30 selected development pilot records are identical between versions (including group IDs), so their observed pilot scores are unaffected. Eleven tests pass, including a same-title variant regression. The three distinct-entity/template pairs remain a documented sensitivity-analysis concern.

Tokenizer audit at pinned model revisions: longest E5 document input 270 tokens; longest reranker document input 268 tokens; no standalone document exceeds 512. Reranker pair overhead is additional. Results saved in `results/tokenizer_audit.json`. BM25 plot visually inspected; labels and intervals are readable. Direct package versions are now pinned in `requirements.txt`; isolated `pip check` reports no broken requirements.

The reproducible `src.check_token_budget` audit now checks all corpus/query token lengths. Conservative maximum query-document pair bounds are 353 tokens for E5 and 348 for the reranker, below 512. This is a preprocessing audit, not test performance evaluation. Command: `env -u PYTHONPATH HF_HUB_DISABLE_XET=1 .venv/bin/python -m src.check_token_budget results/pilot_02/config.json`.

A second data-preparation defect was found during inspection: distinct raw whitespace variants could overwrite chunk IDs derived from normalized text. Chunk IDs now use raw-text SHA256 plus raw offset; normalized text/title components still control split grouping. Corrected corpus has 3,223 chunks. `results/lexical_v2` is the corrected 30-query BM25 run; quality metrics are unchanged. Twelve tests pass. The neural run was restarted as `pilot_03` on the corrected corpus; `pilot_02` remains an interrupted download, not experimental evidence. Public-model HTTP transfers restart after interruption in this environment, so no further interruption is planned.

### Continued execution after user approval

Reranker download completed and offline inference passed a two-pair finite-score API check. E5 and generator transfers failed with `SSL: UNEXPECTED_EOF_WHILE_READING`; `pilot_03` contains no completed model experiment. A curl transfer obtained partial E5 bytes successfully. Started `experiments/resume_pilot.py` as a bounded background job: up to 30 resumable attempts, published E5 SHA256 verification, offline B1/B2/B3/P1 plus ablations, then paired analysis. Live state: `results/resume_status.json`; log: `results/resume_pilot.log`. This job does not run generation. No completed neural scores are claimed until its status and output artifacts confirm success.

During runner inspection, corrected an accidental duplicated initialization block that had replaced NumPy seeding with an unused `np.data_dir` assignment. Python, NumPy and Torch seeds are now all set correctly. Existing numerical unit tests and compilation checks were rerun after this correction. Remaining human annotation, test-set calibration/freeze, complete literature audit and final paper formatting are still pending.

### Requested held-out continuation

Inspected progress and live recovery state first; E5 resumed bytes were still downloading and no neural run had completed. Preserved all completed lexical results and existing recovery process. Froze 60 test query IDs, unchanged router thresholds and three retrieval timing repetitions before accessing test outcomes; confirmed test/development/validation group disjointness. Queued `experiments/complete_heldout.py` to use the completed development retrieval run, execute held-out retrieval plus all ablations, verify/download the pinned generator, check four-system development generation, and run held-out generation. State is tracked in `results/heldout_status.json`. This is execution planning, not evidence of completion.

Corrected latency labeling: separately measured retrieval and generation durations are summed as **estimated** end-to-end latency, not represented as a direct full-request wall measurement. Generator process CPU time is also recorded. Total energy/hardware cost is unmeasured. Human semantic correctness and claim support remain pending; automatic exact match cannot replace either.

### Completed development neural pilot (actual evidence)

E5 file SHA256 verified: `1a55775f53449dac10a2bcbc312469fac40b96d53198c407081a831f81c98477`. `results/pilot_04` completed all 270 rows (30 development queries × 9 systems), including raw rankings, frozen configuration, metadata, paired bootstrap, routing cases and comparison plot. nDCG@5: B1 0.897689, B2 0.942062, B3 0.966667, P1 0.966667. Mean retrieval seconds: B1 0.017701, B2 0.027503, B3 1.185838, P1 0.368337. This is development evidence only, not held-out or answer-quality evidence. P1 reranks 5.333 pairs per query on average versus B3's 20; observed routing overhead is included. The independently frozen held-out run has started; no threshold changes were made in response to pilot scores.

### Frozen held-out study completed — continuation findings

- Inspected `progress.md` and `results/resume_status.json` before continuing. No old retrieval run or download was restarted. The stale held-out status said generation was active, but no worker remained; 235/240 complete generation records were present. Added guarded `--resume`, validated unchanged config/evidence, and appended only the five missing records. All original outputs are retained.
- Reverified E5 and generator SHA256 and sizes; evidence: `results/model_integrity.json`. The existing development end-to-end smoke contains four matched outputs with nonzero input/output tokens. This smoke occurred before held-out generation but after held-out retrieval; the entire requested end-to-end smoke did not precede retrieval execution.
- **Phase 4 complete for automatic measurements:** `results/heldout_01` contains 1,620 retrieval rows (60 frozen test queries × 9 systems × 3 repetitions) and 240 generation responses. The sample covers 55 article groups. Frozen IDs, disjoint group splits, unique rankings and repeat consistency pass `validation_checks.json`. Test outcomes did not change thresholds, prompts or generation parameters.
- Primary results (Recall@5 / nDCG@5 / mean warm retrieval ms): B1 0.950000 / 0.923213 / 17.49; B2 0.966667 / 0.926323 / 25.10; B3 0.983333 / 0.931418 / 1051.13; P1 0.983333 / 0.923085 / 201.29. P1 saves 80.85% retrieval time against B3, including 0.230 ms mean router overhead, but is slower than B1/B2 and has lower nDCG than all three. The nDCG P1−B3 interval is [−0.023433, 0.000000]; equal observed recall is not equivalence evidence.
- **Phase 5 completed for retrieval:** all five ablations, paired article-cluster bootstrap, routing cases and plots are saved. P1 without reranking achieves nDCG 0.939880 at 19.25 ms but Recall@5 drops to 0.966667. Length/keyword removal gives no aggregate quality benefit on this sample. Six questions show routing regret, including four reranker selections with a better alternative. See `failure_analysis.md`. These exploratory findings do not authorize retuning on the test sample.
- Generation strict EM: B1/B2/P1 each 2/60; B3 1/60. This format-sensitive metric cannot substitute for semantic correctness. Estimated request latency (separately measured retrieval repeat 0 plus generation): B1 42.275 s, B2 41.758 s, B3 42.841 s, P1 43.495 s. P1 shows **no observed overall latency saving**. P1−B3 estimate is +0.6545 s, 95% cluster interval [−0.5456, 1.8908]. There is no evidence of a stable end-to-end speedup. Five resumed responses and one generation repetition limit timing inference.
- Total generation tokens: 461,175 input and 13,557 output. Generation segments consumed 10,136.49 wall seconds and 38,206.47 process CPU seconds; retrieval segments across all repeats/ablations consumed 347.35 wall seconds and 1,550.36 process CPU seconds. Index setup was 158.07 wall seconds. Download/load/analysis/idle time is excluded. API charges USD 0; electricity, hardware amortization and total financial cost remain unmeasured.
- Answer semantic correctness and claim-level faithfulness remain **pending**, not zero or successful. Exported a blinded 240-response packet, preserving private method mapping. No independent human annotations exist. Selected assistant-reviewed failure examples demonstrate unsupported/contradictory answers despite available evidence but cannot establish a population hallucination rate. Balanced abstention needs a validated unanswerable set.
- **Phase 6 updated:** `paper/draft.md` now reports actual held-out findings, negative results, ablations and limitations. `results/heldout_01/experiment_report.md` answers the method/benefit/cost/tradeoff/failure/contribution questions. All three plots were visually checked. Thirteen tests pass, including resume configuration/evidence safeguards; the full answer report ran successfully with complete-output assertions.
- **Phases 1–2:** prior literature and fixed design are preserved. Full literature detail verification, residual near-duplicate sensitivity and model-pretraining contamination limitations remain. No new novelty claim is supported.

Next action: obtain two independent Thai-proficient annotations using `experiments/annotation_protocol.md` and the blinded packet, adjudicate disagreements, then compute semantic correctness and claim-grounding measures. Direct full-request timing needs an integrated measurement session; current sums are explicitly estimates. Any policy/prompt improvement must use development/validation data and a new untouched test sample. Final AUCC template formatting, authors/advisor material and conference requirement discrepancies remain unresolved. The paper is not yet submission-ready.

### Validation continuation — task 4 complete

Preserved original held-out outputs with a SHA256 manifest in `results/validation_02/original_output_hashes.json`. Investigated all six label-defined regret cases and the ten C-route ablation cases. New evidence changes the interpretation: the park query's top reranked passage explicitly contains the answer despite being unjudged; the band question omits its entity. These are not all proven incorrect routing decisions. The no-reranking gain decomposes into four improved, one worsened and 55 unchanged query nDCGs; recall loses one query. Full trace and future development-only proposals: `results/validation_02/routing_analysis.md`, `routing_evidence.json`, `reranking_effects.json`. No policy, query selection or existing labels/results changed. Next: incorporate this qualification into the paper and obtain pooled independent judgments later.

### Validation continuation — task 2 feasible preparation complete

The author confirmed no independent Thai annotators are currently available. Prepared immutable blinded evidence packet and two separate unfilled label files in `results/validation_02/annotation/`; neither contains method labels. Expanded `experiments/annotation_protocol.md` with semantic-correctness rules, four-way claim support, ambiguity/reference-quality flags, missing-data handling, agreement/adjudication and explicit denominators. Human evaluation remains blocked by unavailable annotators (0/240 labels), not completed. Assistant case reviews and strict EM are not human judgments. Next: recruit two independent raters, use development-only training examples, retain raw disagreements, adjudicate and run paired evaluation. No unsupported hallucination-reduction claim is made.

### Validation continuation — task 3 retrieval analysis complete

Computed all six primary-system paired comparisons across the same 60 test queries, preserving 55 article clusters and averaging the three retrieval repetitions within query. Saved mean/median/p95 estimates and percentile intervals, plus Recall@5/nDCG@5/latency differences, in `results/validation_02/retrieval/`. Bootstrap uses 2,000 cluster resamples, seed 2027. These are exploratory intervals without hypothesis testing or multiplicity adjustment; no significance/equivalence claim. Direct end-to-end paired statistics will use the separate integrated benchmark once its 240 requests complete. Fifteen tests pass, including direct timer boundaries and cluster membership preservation.

### Validation continuation — task 5 working manuscript prepared

Expanded the English manuscript with operational routing/fusion definitions, data provenance and leakage controls, measurement boundaries, cluster-statistical estimands, blinded evaluation rubric, all regret mechanisms, and threats to validity. Added the author's supplied name/email; affiliation and advisor remain pending. Created an AUCC-template-based DOCX and two grayscale data-derived figures; preliminary render is 8 pages. Reference DOCX and unrelated package parts remain unchanged. Final direct-benchmark numbers and final full-page visual inspection remain pending until the live benchmark completes. Official page/portal deadline conflict remains; no similarity report or advisor certification is claimed.

### Stability-first continuation — active direct benchmark preserved

Inspected required progress, resume status, original experiment report and paper draft. Existing CPU benchmark PID 82554 remains active; 35 complete records were present at inspection, with valid JSON and no logged errors. No duplicate benchmark, precision/device/thread/batch change or restart was performed. Original held-out data remains immutable. Prepared complete-run integrity checks and sample standard deviations for post-processing only. Final direct results remain pending until all 240 paired records exist. The former monitoring helper was not running; monitoring may be restarted independently without launching inference. Independent human evaluators are still unavailable.

### Validation continuation — task 1 and direct task 3 complete

The integrated benchmark completed all 240 paired requests. Each elapsed duration is one perf_counter interval from before query encoding through final decoded answer; it includes router, retrieval, reranking, evidence assembly, tokenization and generation. Warmup uses a development query; loading/index setup is separate. Balanced method positions and frozen model/prompt/router settings are saved in `results/e2e_01/config.json`. Mean, median, p95 and article-cluster bootstrap intervals, plus all six pairwise quality/latency comparisons, are in `results/validation_02/end_to_end/`. No significance/equivalence claim. Original held-out artifacts remain byte-identical.

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

Next: independent human annotation remains unavailable. Finish final manuscript render/visual checks and retain missing affiliation/advisor/submission materials as pending.

### Final verification completed — 2026-10-30

Preserved the original running CPU process through completion: 240/240 direct requests, 60 unique frozen queries per method, no duplicates, invalid/nonfinite timings or missing pairs. All original held-out files match their saved SHA256 values. Rankings and decoded answers match the original run on all 240 requests. Model precision, devices, thread counts and generation parameters were not changed.

Direct means/medians/p95/SD seconds: B1 41.765/41.839/53.509/7.312; B2 40.590/42.051/54.061/8.439; B3 42.141/43.027/52.882/7.370; P1 42.489/41.660/55.272/7.823. P1 mean differences versus B1/B2/B3 are +0.723/+1.899/+0.348 seconds. P1−B3 95% article-cluster interval is [−1.2076, 1.8974]. No observed mean end-to-end saving; no formal significance claim. Original generation-stage measurements remain separate; integrated request timing includes all online work and does not separately time generation.

Fifteen existing tests pass in the final run. Recomputed statistics in a temporary directory and obtained byte-identical statistics JSON. Verified all direct table values against actual output, three tables and two embedded grayscale figures. Visually inspected all eight final rendered pages (`paper/qa/manuscript_delivery`); tables, captions and references are readable, with no clipping. The original template and unrelated package parts remain unchanged. Updated existing manuscript Results, abstract and Conclusion with verified direct results without rewriting from scratch.

Consolidated follow-up report: `results/validation_02/experiment_report.md`; original `results/heldout_01/experiment_report.md` remains unchanged. Current editable draft: `paper/aucc2027_manuscript.docx` (8 pages). Independent semantic correctness/faithfulness remains pending because human raters are unavailable. Source-derived qrels, ambiguous questions, 60-query sample, one integrated timing per method/query, CPU bfloat16 and background load limit generalization. Electricity/hardware monetary cost is unmeasured. Affiliation/advisor, certification, similarity report and official deadline reconciliation remain submission gates. No further experiments or test tuning were performed.

### LaTeX migration canceled; original workflow retained — 2026-10-30

The author canceled migration and will transfer content manually. No further LaTeX files are created or edited. Existing partial migration artifacts remain preserved and inactive; no completed work was deleted. Confirmed no migration, export, render or benchmark process remains active. SHA256 comparison confirms `paper/draft.md`, `paper/aucc2027_manuscript.docx` and the official Word template are unchanged from before migration. These original Markdown/Word files remain the maintained workflow.

Rechecked completed benchmark integrity: 240 unique matched records, finite measurements and unchanged configurations/original results. Independent human evaluation remains unavailable with 0/240 labels. Prepared `paper/submission_readiness.md` with verified evidence, permissible claims, a concrete annotation handoff and remaining author/advisor/certification/similarity/deadline gates. Existing tests record 15 passes; no implementation or research-result change warrants rerunning experiments/tests. All feasible preparation in this continuation is complete; the next scientific action requires genuine independent annotations. No submission or external communication was performed.
