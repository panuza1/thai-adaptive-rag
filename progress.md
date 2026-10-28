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
