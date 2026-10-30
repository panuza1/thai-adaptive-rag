# Evidence inventory

- `lexical_pilot/`: actual 30-query **development** BM25-only sanity run; full 3,221-chunk corpus. Not dense/hybrid/adaptive results. Includes per-query scores/rankings, mean summary, bootstrap intervals and inspected grayscale figure.
- `pilot_01/`, `pilot_01.log`: interrupted Xet model download; no experiment results.
- `pilot_02/`, `pilot_02.log`: interrupted ordinary-HTTP retry with resolved model revisions. Only completed `rows.jsonl` plus `metadata.json` constitute a successful run. `run_executed.py` archives the executed runner before subsequent preparation changes.
- `data_audit.json`: original v1 near-duplicate candidates. v2 preparation repairs same-title duplicate pairs. It does not claim absence of semantic overlap.
- `prepare_v1.py`: archived original preparation; `prepare_v2.log`: corrected split counts. Original processed data retained while the v1 pilot runs; v2 stored separately.
- `tokenizer_audit.json`: corpus-only tokenizer length check at pinned model revisions; no document exceeds 512 tokens. Pairwise reranker query overhead still requires checking.
- `tests.log`: latest actual pytest output. `hardware.txt`: hardware observations. `environment.lock.txt`: isolated installed versions. `install-*.log`, `prefetch-*.log`: transfer/install evidence, not model measurements.

Never fill missing generation/annotation measurements with zero. Development numbers do not establish test-set gains or novelty. Latency observations here are single-machine development measurements, not transferable performance promises.

- `pilot_03.log`: neural run failed during E5 download with SSL unexpected EOF; no completed neural measurements.
- `lexical_v2/`: corrected 3,223-chunk BM25 development pilot, same 30 selected questions.
- `reranker_api_check.json`: cached reranker successfully loaded and returned finite scores on two synthetic pairs; API validation only.
- `resume_status.json`, `resume_pilot.log`: bounded resumed download and automatic offline retrieval/analysis job. `pilot_04` is valid only after successful completion; consult its metadata and row count.

## Completed frozen held-out study

`heldout_01/experiment_report.md` is the consolidated actual-evidence report. Raw data: `rows.jsonl` (1,620) and `generation.jsonl` (240); resolved retrieval/generator configs, environment lock and source hashes are retained. `summary.csv`, `answer_summary.csv`, both paired-bootstrap JSON files, `computational_cost.json`, three PNG plots and `failure_analysis.md` are derived artifacts. `validation_checks.json` verifies matched queries and split/ranking invariants. `completion_metadata.json` records the five-response generation resume. `model_integrity.json` verifies E5/generator weights.

Human annotation is pending: distribute only `heldout_01/annotation_packet.jsonl` to annotators, not `annotation_mapping_private.json`. No null label should be counted as a successful answer or faithful claim. Retrieval metadata's `generation_status` was captured before the later generation phase; consult `heldout_status.json` for current completion.
