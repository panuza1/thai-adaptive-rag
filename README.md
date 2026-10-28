# Adaptive Retrieval Strategy for Cost-Efficient and Reliable Thai RAG Systems

Research workspace for an undergraduate AUCC 2027 submission. **Development stage; no completed held-out study or verified reliability claim.** See `progress.md` for actual execution evidence and blockers.

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
env -u PYTHONPATH HF_HUB_DISABLE_XET=1 OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 .venv/bin/python -m src.run --config experiments/pilot.json --output results/pilot_01
.venv/bin/python -m src.analyze results/pilot_01
.venv/bin/python -m src.generate results/pilot_01
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

It saves real per-query outputs, bootstrap intervals and a plot, but is an additional BM25-only baseline, not a substitute for B1/B2/B3/P1. For a matched three-query generator smoke test use `python -m src.generate results/pilot_01 --limit 3`; the default evaluates all four primary systems on the retrieval run's queries. Score adjudicated labels with `python -m src.score_answers path/to/adjudicated.jsonl`; consult `experiments/annotation_protocol.md` first.
