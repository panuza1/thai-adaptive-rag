# Evidence inventory

- `lexical_pilot/`: actual 30-query **development** BM25-only sanity run; full 3,221-chunk corpus. Not dense/hybrid/adaptive results. Includes per-query scores/rankings, mean summary, bootstrap intervals and inspected grayscale figure.
- `pilot_01/`, `pilot_01.log`: interrupted Xet model download; no experiment results.
- `pilot_02/`, `pilot_02.log`: ordinary-HTTP retry with resolved model revisions. Only completed `rows.jsonl` plus `metadata.json` constitute a successful run. `run_executed.py` archives the executed runner before subsequent preparation changes.
- `data_audit.json`: original v1 near-duplicate candidates. v2 preparation repairs same-title duplicate pairs. It does not claim absence of semantic overlap.
- `prepare_v1.py`: archived original preparation; `prepare_v2.log`: corrected split counts. Original processed data retained while the v1 pilot runs; v2 stored separately.
- `tokenizer_audit.json`: corpus-only tokenizer length check at pinned model revisions; no document exceeds 512 tokens. Pairwise reranker query overhead still requires checking.
- `tests.log`: latest actual pytest output. `hardware.txt`: hardware observations. `environment.lock.txt`: isolated installed versions. `install-*.log`, `prefetch-*.log`: transfer/install evidence, not model measurements.

Never fill missing generation/annotation measurements with zero. Development numbers do not establish test-set gains or novelty. Latency observations here are single-machine development measurements, not transferable performance promises.
