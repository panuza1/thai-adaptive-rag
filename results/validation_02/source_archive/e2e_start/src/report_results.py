"""Generate a descriptive report solely from a completed retrieval run."""
import argparse
import csv
import json
from pathlib import Path


def report(path):
    out=Path(path)
    cfg=json.loads((out/'config.json').read_text())
    rows=[json.loads(s) for s in (out/'rows.jsonl').read_text().splitlines()]
    systems=['B1','B2','B3','P1:none']+['P1:'+a for a in cfg['ablations'] if a!='none']
    keys={(r['query_id'],r['repeat'],r['system']) for r in rows}
    n=len({r['query_id'] for r in rows})
    assert len(keys)==len(rows)==n*cfg['repeats']*len(systems), 'Incomplete or duplicate experiment rows'
    summaries={s['system']:s for s in csv.DictReader((out/'summary.csv').open())}
    primary=['B1','B2','B3','P1:none']
    lines=['# Observed retrieval findings',f"Split: {cfg['split']}; queries: {n}; repetitions: {cfg['repeats']}. Fixed heuristic, no test tuning.",
           '| System | Recall@5 | MRR@5 | nDCG@5 | Mean seconds | Router seconds |',
           '|---|---:|---:|---:|---:|---:|']
    for name in primary:
        s=summaries[name];lines.append('| '+name+' | '+' | '.join(f'{float(s[k]):.6f}' for k in ['recall','mrr','ndcg','retrieval_seconds','router_seconds'])+' |')
    p=summaries['P1:none']
    for baseline in primary[:3]:
        b=summaries[baseline]
        saving=100*(1-float(p['retrieval_seconds'])/float(b['retrieval_seconds']))
        delta=float(p['ndcg'])-float(b['ndcg'])
        lines.append(f'P1 versus {baseline}: observed mean retrieval-time reduction {saving:.2f}% (negative means slower); nDCG difference {delta:+.6f}.')
    best=max(primary,key=lambda k:float(summaries[k]['ndcg']))
    fastest=min(primary,key=lambda k:float(summaries[k]['retrieval_seconds']))
    lines.append(f'Highest observed retrieval nDCG: {best} (ties possible). Lowest mean retrieval latency: {fastest}. These are separate objectives.')
    cases=[json.loads(s) for s in (out/'routing_cases.jsonl').read_text().splitlines() if json.loads(s)['repeat']==0]
    failures=sorted((r for r in cases if r['routing_regret']>0),key=lambda r:-r['routing_regret'])
    lines.append(f'Routing regret relative to the best per-query static baseline occurs on {len(failures)} of {n} queries. This is a label-informed diagnostic, not a deployable oracle.')
    for r in failures[:10]:lines.append(f"- Query {r['query_id']}: selected {r['strategy']}; nDCG {r['ndcg']:.4f}; oracle {r['retrieval_oracle_ndcg']:.4f}; features {r['features']}.")
    lines+=['## Paired uncertainty', 'Article-cluster bootstrap intervals from the same paired queries; exploratory, not proof of answer non-inferiority.']
    for r in json.loads((out/'paired_bootstrap.json').read_text()):lines.append(f"- {r['comparison']}, {r['metric']}: delta {r['mean_delta']:.6f}, 95% interval {r['ci95']}.")
    lines+=['## Supported scope','The evidence can support a measured retrieval-quality/latency tradeoff for this fixed policy, corpus, sample and CPU configuration. It does not establish algorithmic novelty, answer correctness, reduced hallucinations or general Thai-domain superiority.',
            'Generation correctness, faithfulness, direct request-level end-to-end latency, energy and hardware monetary cost require separate evidence. See generation outputs if present; missing annotations are not successful outcomes.']
    (out/'findings.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path');report(p.parse_args().path)
