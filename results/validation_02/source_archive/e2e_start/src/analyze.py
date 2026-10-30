"""Article-cluster paired bootstrap; descriptive intervals, no significance claims."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def bootstrap(values,groups,seed=2027,n=2000):
    rng=np.random.default_rng(seed); keys=sorted(set(groups))
    arrays=[np.asarray([v for v,g in zip(values,groups) if g==key]) for key in keys]
    means=[np.concatenate([arrays[i] for i in rng.integers(len(keys),size=len(keys))]).mean() for _ in range(n)]
    return np.quantile(means,[.025,.975]).tolist()


def analyze(path):
    out=Path(path); rows=[json.loads(s) for s in (out/'rows.jsonl').read_text().splitlines()]
    systems=sorted(set(r['system'] for r in rows)); summary=[]; paired=[]
    for system in systems:
        rs=[r for r in rows if r['system']==system]
        summary.append({'system':system,'n_queries':len(set(r['query_id'] for r in rs)),
                        **{m:float(np.mean([r[m] for r in rs])) for m in ['recall','mrr','ndcg','retrieval_seconds','router_seconds','reranked_pairs']},
                        'latency_p95':float(np.quantile([r['retrieval_seconds'] for r in rs],.95))})
    for baseline in ['B1','B2','B3']:
        def aggregate(system):
            keys=sorted(set(r['query_id'] for r in rows if r['system']==system))
            return {q:[r for r in rows if r['system']==system and r['query_id']==q] for q in keys}
        a,b=aggregate('P1:none'),aggregate(baseline)
        assert a.keys()==b.keys()
        for metric in ['ndcg','recall','retrieval_seconds']:
            delta=[np.mean([r[metric] for r in a[q]])-np.mean([r[metric] for r in b[q]]) for q in a]
            ci=bootstrap(delta,[a[q][0]['group'] for q in a])
            paired.append({'comparison':'P1:none - '+baseline,'metric':metric,'mean_delta':float(np.mean(delta)),'ci95':ci})
    (out/'paired_bootstrap.json').write_text(json.dumps(paired,indent=2))
    with (out/'summary.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(summary[0])); writer.writeheader(); writer.writerows(summary)
    fig,ax=plt.subplots(figsize=(7,4))
    for s in [s for s in summary if s['system'] in ['B1','B2','B3','P1:none']]:
        ax.scatter(s['retrieval_seconds']*1000,s['ndcg'],color='black',marker='x')
        ax.annotate(s['system'],(s['retrieval_seconds']*1000,s['ndcg']),fontsize=9,xytext=(4,5),textcoords='offset points')
    ax.set(xlabel='Mean retrieval latency (ms)',ylabel='nDCG@5',title=json.loads((out/'config.json').read_text())['split'].capitalize()+' retrieval comparison')
    ax.margins(x=.12,y=.15)
    fig.tight_layout(); fig.savefig(out/'tradeoff.png',dpi=180); plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(10,5),sharey=True)
    labels=[s['system'] for s in summary]
    axes[0].barh(labels,[s['ndcg'] for s in summary],color='gray')
    axes[1].barh(labels,[s['retrieval_seconds']*1000 for s in summary],color='gray')
    axes[0].set_xlabel('nDCG@5');axes[1].set_xlabel('Mean retrieval latency (ms)')
    fig.tight_layout();fig.savefig(out/'ablations.png',dpi=180);plt.close(fig)
    routes=Counter(r['strategy'] for r in rows if r['system']=='P1:none')
    (out/'routing.json').write_text(json.dumps(routes,indent=2))
    failures=[]
    for r in rows:
        if r['system']=='P1:none':
            others=[s for s in rows if s['query_id']==r['query_id'] and s['repeat']==r['repeat'] and s['system'] in ['B1','B2','B3']]
            best=max(s['ndcg'] for s in others)
            failures.append(r | {'retrieval_oracle_ndcg':best,'routing_regret':best-r['ndcg']})
    (out/'routing_cases.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in failures))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('path'); analyze(p.parse_args().path)
