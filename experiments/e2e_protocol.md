# Direct end-to-end benchmark protocol

This follow-up measures the frozen policy without selecting new parameters. It does not overwrite `results/heldout_01`. The original output SHA256 manifest is stored in `results/validation_02/original_output_hashes.json`.

Run `env -u PYTHONPATH HF_HUB_OFFLINE=1 OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 .venv/bin/python -m src.benchmark_e2e --output results/e2e_new` only for a new run. The active run is `results/e2e_01`; do not start a competing copy. One serial request per system and frozen test query gives 240 observations. Query order is seeded and shuffled; Latin-square rotations in randomized four-query blocks balance system position. All four systems are warmed on the same development question. No answer or retrieval cache is used for a timed request.

The single request timer encloses query encoding, dense search, feature extraction and routing where applicable, BM25/RRF, reranking, evidence lookup and assembly, chat-template processing, tokenization, generation and final decode. Corpus/model loading and index setup are measured separately. Metric calculation, old-output parity comparisons and disk logging occur after the request timer. CPU execution is synchronous. The recorded generator dtype is bfloat16; no precision optimization was made after inspecting test outcomes.

The benchmark shares the exact retrieval function with the original runner after a scope-only extraction. The serialized config records source hashes, model revisions, hardware, thread settings and schedule. Each output records original ranking/answer parity. Comparing parity is a verification step after measurement, not a routing input.

Analysis requires 240 unique matched records. Article-cluster bootstrap preserves 55 source groups and all paired questions; mean, median and p95 intervals and all six pairwise mean differences are computed with 2,000 resamples. A median difference means the difference of system medians, not the median paired difference. No formal significance, multiplicity-adjusted inference or non-inferiority claim is planned.

Limitations: one request per method/query, single CPU workstation/session, no server queue/network measurement, ordinary workstation background activity, and uncertain precision for p95. Paper preparation/short analysis processes may coexist; render commands are assigned low scheduling priority. These conditions are disclosed rather than claiming an isolated hardware benchmark. Energy and hardware monetary cost remain unmeasured.

After successful completion run `env -u PYTHONPATH .venv/bin/python -m experiments.finalize_validation`; it refuses incomplete runs, checks original hashes and writes separate validation results plus paper/progress updates.
