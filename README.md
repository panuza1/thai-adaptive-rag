# Adaptive Retrieval Strategy for Cost-Efficient and Reliable Thai RAG Systems

Research workspace for an undergraduate AUCC 2027 submission. **Frozen 60-query held-out retrieval and ablation study completed; independent reliability annotation remains pending.** See `progress.md` for actual execution evidence and blockers.

## Reproduce

Python 3.10+, Linux. No paid APIs. First run downloads public data/models; allow disk space and network time. Use a fresh output directory for every run; existing results are never overwritten by the retrieval/generation runners.

```bash
python -m venv .venv
.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install -r requirements.txt
mkdir -p data/raw
curl --fail --location --retry 3 https://raw.githubusercontent.com/iapp-technology/iapp-wiki-qa-dataset/644a29c59bac62d5b15b9e9b06c55bba00708eca/squad_format/data/train.jsonl -o data/raw/train.jsonl
.venv/bin/python -m src.prepare --output data/processed_v2
.venv/bin/python -m pytest -q
env -u PYTHONPATH HF_HUB_DISABLE_XET=1 OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 .venv/bin/python -m src.run --config experiments/pilot.json --output results/pilot_new
.venv/bin/python -m src.analyze results/pilot_new
.venv/bin/python -m src.generate results/pilot_new
```

Generator defaults to local Qwen2.5-0.5B-Instruct, a resource-conscious initial candidate whose Thai suitability must be validated. It is not an established optimal Thai generator. All arms share the model/prompt/decoding. Human labels remain null until annotation. Strict exact match penalizes citation/prose additions; interpret it alongside semantic human correctness, not as the sole answer score.

For exact reruns use a completed run's `config.json` (resolved model commit SHAs) and `requirements.lock.txt`. Pass the recorded generator revision with `--revision`. Data manifest records SHA256. `requirements.txt` pins direct dependencies, while the run lock pins transitive dependencies too; each successful run saves its actual environment. Source hashes are saved. The input training file currently has SHA256 `9ecbc1bdd4bdc43a447c62d46c9ab0874b98c72f5ba9941448c1f78264ca8bda`.

## Files

- `literature_review.md`: verified sources, research gap and explicit review limitations.
- `research_design.md`: split protocol, metrics, calibration, ablations and validity gates.
- `src/core.py`, `prepare.py`, `run.py`: retrieval policy, preprocessing and actual B1/B2/B3/P1 execution.
- `src/generate.py`: local RAG generation with input/output token accounting and annotation fields.
- `src/analyze.py`: paired article-cluster bootstrap, CSV summary, grayscale latency-quality plot, routing regret cases.
- `experiments/pilot.json`: provisional development settings; do not use these as validated thresholds.
- `paper/draft.md`: English content draft; results explicitly pending where unavailable.
- `paper/aucc_requirements.md`: official pages/template and conflicting deadlines.

The pilot uses 30 development questions against the complete processed corpus, not a toy corpus. BM25 uses Thai newmm tokens; E5 uses required query/passage prefixes; hybrid uses RRF; cross encoder reranks 20 candidates. The router reuses its initial dense search. CPU timing uses four torch threads and shuffled system order. Index build/download times are separate from warm request latency. Full test evaluation, annotated hallucination evaluation and learned routing are not completed automatically by running the pilot.

Do not distribute source contributor/payment fields: preprocessing retains only task data. Review Wikipedia-derived text licensing/attribution before redistributing the corpus. No web service, UI, database or paid integration is required.

If the machine exports ROS or other global `PYTHONPATH` entries, prefix commands with `env -u PYTHONPATH` for isolation. `HF_HUB_DISABLE_XET=1` selects ordinary HTTP model downloads when the Xet transfer stalls. Interrupted outputs are retained for diagnosis; use a new output directory to retry.

A smaller lexical-only sanity experiment is available without neural model downloads:

```bash
env -u PYTHONPATH .venv/bin/python -m src.lexical_pilot --output results/lexical_repeat
```

It saves real per-query outputs, bootstrap intervals and a plot, but is an additional BM25-only baseline, not a substitute for B1/B2/B3/P1. For a matched three-query generator smoke test use `python -m src.generate results/pilot_new --limit 3`; the default evaluates all four primary systems on the retrieval run's queries. Score adjudicated labels with `python -m src.score_answers path/to/adjudicated.jsonl`; consult `experiments/annotation_protocol.md` first.

Recovery for the current network interruption: `env -u PYTHONPATH HF_HUB_DISABLE_XET=1 .venv/bin/python experiments/resume_pilot.py`. This bounded job resumes the pinned E5 transfer, verifies its published SHA256, caches the weight, and runs/analyzes `results/pilot_04` offline. Do not start a second copy while `results/resume_status.json` reports an active job. Check the log and process if a status appears stale. It does not run generation or human annotation.

## Completed held-out experiment

See `results/heldout_01/findings.md`, `failure_analysis.md`, `summary.csv`, `paired_bootstrap.json`, and `validation_checks.json`. All 1,620 retrieval rows use the frozen 60 test queries, three repetitions and nine configurations. No test tuning was performed. The E5 and generator checksums are archived in `results/model_integrity.json`.

Reproduce into a **new** output directory:

```bash
env -u PYTHONPATH HF_HUB_OFFLINE=1 OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 .venv/bin/python -m src.run --config experiments/heldout.json --output results/heldout_new
.venv/bin/python -m src.analyze results/heldout_new
.venv/bin/python -m src.report_results results/heldout_new
env -u PYTHONPATH HF_HUB_OFFLINE=1 OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 .venv/bin/python -m src.generate results/heldout_new --model Qwen/Qwen2.5-0.5B-Instruct --revision 7ae557604adf67be50417f59c2c2f167def9a775
.venv/bin/python -m src.answer_report results/heldout_new
```

Use offline mode only after model downloads complete. `src.generate --resume` validates the original configuration and saved evidence, preserves completed records and appends missing responses after an interruption. Never rerun the old orchestration scripts against completed output directories. `src.answer_report` requires all matched outputs, creates actual cost/token summaries, paired uncertainty estimates, plots, and an unfilled annotation packet. Give annotators only `annotation_packet.jsonl`; retain `annotation_mapping_private.json` separately. The packet's null judgments are not evaluation results.

## Scientific validation follow-up

Original `results/heldout_01` files are immutable for this phase; SHA256 checks are in `results/validation_02/original_output_hashes.json`.

- `results/e2e_01/status.json`: active direct request benchmark status; do not launch a competing run. The timer encloses the complete warm RAG request, not a sum of separate stages. Protocol: `experiments/e2e_protocol.md`.
- `src.validate_statistics`: all six paired primary-system comparisons and article-cluster intervals for mean/median/p95. Retrieval validation is already in `results/validation_02/retrieval`.
- `results/validation_02/routing_analysis.md`: all six label-defined regret cases, including unjudged answer-bearing evidence and underspecified questions. These are not all proven routing mistakes.
- `results/validation_02/annotation`: blinded packet and unfilled rater files. Independent human raters are unavailable; semantic correctness and faithfulness remain pending.
- `paper/aucc2027_manuscript.docx`: template-based working draft. Build with the Codex bundled Python and `paper/build_manuscript.py`, then render/inspect using `paper/qa/render_with_system_lo.py`. Source: `paper/draft.md`. Affiliation/advisor and human evaluation remain pending.

Analysis command after the direct run completes:

```bash
env -u PYTHONPATH .venv/bin/python -m experiments.finalize_validation
```

It validates all 240 direct requests and original output hashes, writes separate statistics, and updates the manuscript content and progress. Rebuild and visually inspect the document after its content changes. Neither the follow-up runner nor analysis calibrates the policy on test data.
