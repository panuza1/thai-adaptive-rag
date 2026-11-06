"""Read-only audit of the frozen held-out retrieval results and their qrels."""
import json
import math
from collections import Counter
from pathlib import Path

from src.core import metrics


SYSTEMS = ('B1', 'B2', 'B3', 'P1:none')


def audit(queries, documents, frozen_ids, rows, config):
    query_by_id = {q['id']: q for q in queries}
    doc_ids = {d['id'] for d in documents}
    if len(query_by_id) != len(queries) or len(doc_ids) != len(documents):
        raise ValueError('Duplicate query or document IDs')
    if len(set(frozen_ids)) != len(frozen_ids):
        raise ValueError('Duplicate frozen query IDs')

    for qid in frozen_ids:
        q = query_by_id[qid]
        if q['split'] != 'test' or not q['relevant'] or not set(q['relevant']) <= doc_ids:
            raise ValueError(f'Invalid test query or gold chunks: {qid}')

    repeats = range(config['repeats'])
    expected = {(qid, system, repeat)
                for qid in frozen_ids for system in SYSTEMS for repeat in repeats}
    observed = {}
    for r in rows:
        key = (r['query_id'], r['system'], r['repeat'])
        if r['system'] not in SYSTEMS:
            continue  # Original experiment also includes five P1 ablations.
        if key not in expected or key in observed:
            raise ValueError(f'Unexpected or repeated result: {key}')
        q = query_by_id[r['query_id']]
        if r['group'] != q['group'] or not set(r['ranking']) <= doc_ids:
            raise ValueError(f'Incorrect group or unknown document: {key}')
        computed = metrics(r['ranking'], set(q['relevant']), config['k'])
        if any(not math.isclose(computed[name], r[name], abs_tol=1e-10)
               for name in ('recall', 'mrr', 'ndcg')):
            raise ValueError(f'Stored retrieval score does not match qrels: {key}')
        observed[key] = r
    if observed.keys() != expected:
        raise ValueError(f'Missing {len(expected - observed.keys())} paired results')

    means = {}
    for qid in frozen_ids:
        means[qid] = {}
        for system in SYSTEMS:
            samples = [observed[qid, system, i] for i in repeats]
            if len({tuple(r['ranking']) for r in samples}) != 1:
                raise ValueError(f'Ranking changed across repetitions: {qid}, {system}')
            means[qid][system] = {
                name: sum(r[name] for r in samples) / len(samples)
                for name in ('recall', 'ndcg', 'retrieval_seconds')
            }

    failures = {s: [q for q in frozen_ids if means[q][s]['recall'] < 1] for s in SYSTEMS}
    oracle_ndcg = []
    oracle_recall = []
    cheapest_at_b3_quality = []
    oracle_winners = Counter()
    cases = []
    for qid in frozen_ids:
        scores = means[qid]
        baselines = {s: scores[s] for s in SYSTEMS[:3]}
        best_ndcg = max(v['ndcg'] for v in baselines.values())
        best_recall = max(v['recall'] for v in baselines.values())
        oracle_ndcg.append(best_ndcg)
        oracle_recall.append(best_recall)
        b3 = scores['B3']
        eligible = [s for s, v in baselines.items()
                    if v['ndcg'] >= b3['ndcg'] - 1e-10
                    and v['recall'] >= b3['recall'] - 1e-10]
        cheapest = min(eligible, key=lambda s: (baselines[s]['retrieval_seconds'], s))
        oracle_winners[cheapest] += 1
        cheapest_at_b3_quality.append(baselines[cheapest]['retrieval_seconds'])
        missed = [s for s in SYSTEMS if qid in failures[s]]
        if missed or scores['P1:none']['ndcg'] < best_ndcg - 1e-10:
            cases.append({
                'query_id': qid,
                'gold_chunks': len(query_by_id[qid]['relevant']),
                'missed_by': missed,
                'quality_oracle_ndcg': best_ndcg,
                'quality_oracle_recall': best_recall,
                'cheapest_at_b3_quality': cheapest,
                'scores': scores,
            })

    def mean(values):
        return sum(values) / len(values)

    return {
        'queries': len(frozen_ids),
        'article_groups': len({query_by_id[q]['group'] for q in frozen_ids}),
        'corpus_chunks': len(doc_ids),
        'validated_primary_rows': len(observed),
        'gold_chunks_per_query': dict(sorted(Counter(
            len(query_by_id[q]['relevant']) for q in frozen_ids).items())),
        'recall_at_5_is_binary_on_this_sample': all(
            len(query_by_id[q]['relevant']) == 1 for q in frozen_ids),
        'recall_failures_by_system': {s: len(ids) for s, ids in failures.items()},
        'shared_recall_failures': len(set.intersection(*(set(ids) for ids in failures.values()))),
        'mean_ndcg': {s: mean([means[q][s]['ndcg'] for q in frozen_ids]) for s in SYSTEMS},
        'oracle': {
            'best_static_per_query_ndcg': mean(oracle_ndcg),
            'best_static_per_query_recall': mean(oracle_recall),
            'cheapest_static_at_or_above_b3_quality_ms': mean(cheapest_at_b3_quality) * 1000,
            'b3_retrieval_ms': mean([means[q]['B3']['retrieval_seconds'] for q in frozen_ids]) * 1000,
            'cheapest_static_selection_counts': dict(oracle_winners),
        },
        'diagnostic_cases': cases,
        'limitations': [
            'Gold relevance is derived from answer spans, not exhaustive passage judgments.',
            'All oracle choices use observed test labels and are hindsight diagnostics, not deployable policies.',
            'Observed retrieval timings are one CPU session, not production cost estimates.',
            'These test-set diagnostics must not be used to tune the existing frozen test run.',
        ],
    }


def main():
    data = Path('data/processed_v2')
    queries = [json.loads(s) for s in (data/'queries.jsonl').read_text().splitlines()]
    documents = [json.loads(s) for s in (data/'documents.jsonl').read_text().splitlines()]
    ids = json.loads(Path('experiments/heldout_query_ids.json').read_text())
    rows = [json.loads(s) for s in Path('results/heldout_01/rows.jsonl').read_text().splitlines()]
    config = json.loads(Path('experiments/heldout.json').read_text())
    report = audit(queries, documents, ids, rows, config)
    target = Path('results/validation_03/benchmark_audit.json')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f"Verified {report['validated_primary_rows']} primary rows for {report['queries']} questions; report: {target}")


if __name__ == '__main__':
    main()
