"""Paired article-cluster intervals; no significance or equivalence claims."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import numpy as np

SYSTEMS=['B1','B2','B3','P1:none']


def cluster_indices(groups,seed=2027,n=2000):
    rng=np.random.default_rng(seed);keys=sorted(set(groups))
    members=[np.flatnonzero(np.asarray(groups)==g) for g in keys]
    return [np.concatenate([members[i] for i in rng.integers(len(keys),size=len(keys))]) for _ in range(n)]


def summarize(values,indices):
    values=np.asarray(values)
    functions={'mean':np.mean,'median':np.median,'p95':lambda v:np.quantile(v,.95)}
    return {name:{'estimate':float(fn(values)),'ci95':np.quantile([fn(values[ix]) for ix in indices],[.025,.975]).tolist()} for name,fn in functions.items()}


def analyze(source,output,e2e=False):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    rows=[json.loads(s) for s in (Path(source)/'rows.jsonl').read_text().splitlines()]
    frozen=json.loads(Path('experiments/heldout_query_ids.json').read_text());n=1 if e2e else 3
    grouped={(q,s):[r for r in rows if r['query_id']==q and r['system']==s] for q in frozen for s in SYSTEMS}
    assert all(len(rs)==n for rs in grouped.values()),'Incomplete paired experiment'
    assert len({(r['query_id'],r['system'],r['repeat']) for r in rows})==len(rows),'Duplicate rows'
    if e2e:assert len(rows)==240
    groups=[grouped[(q,'B1')][0]['group'] for q in frozen];indices=cluster_indices(groups)
    latency='end_to_end_seconds' if e2e else 'retrieval_seconds'
    values={s:{m:np.array([np.mean([r[m] for r in grouped[q,s]]) for q in frozen]) for m in ['recall','ndcg',latency]} for s in SYSTEMS}
    summary={s:{m:summarize(v,indices) for m,v in ms.items()} for s,ms in values.items()}
    paired=[]
    for a,b in combinations(SYSTEMS,2):
        for metric in ['recall','ndcg',latency]:
            av,bv=values[a][metric],values[b][metric]
            diff=av-bv
            paired.append({'comparison':a+' - '+b,'metric':metric,'mean_difference':float(diff.mean()),
                           'mean_difference_ci95':np.quantile([diff[ix].mean() for ix in indices],[.025,.975]).tolist(),
                           'median_difference':float(np.median(av)-np.median(bv)),
                           'median_difference_ci95':np.quantile([np.median(av[ix])-np.median(bv[ix]) for ix in indices],[.025,.975]).tolist(),
                           'p95_difference':float(np.quantile(av,.95)-np.quantile(bv,.95)),
                           'p95_difference_ci95':np.quantile([np.quantile(av[ix],.95)-np.quantile(bv[ix],.95) for ix in indices],[.025,.975]).tolist()})
    result={'source':str(source),'queries':60,'groups':len(set(groups)),'bootstrap_replicates':2000,'seed':2027,
            'unit':'article-group clusters; paired queries retained; retrieval repeats averaged within query',
            'summary':summary,'paired':paired,
            'limitations':'Exploratory percentile intervals, no multiplicity correction or formal hypothesis tests; no significance/equivalence claims. p95 depends on few observations; single-session variability is not cross-session reproducibility.'}
    (out/'statistics.json').write_text(json.dumps(result,indent=2))
    lines=['# Paired statistical validation','',f'Source: `{source}`. 60 paired questions from {len(set(groups))} article groups. Cluster percentile bootstrap: 2,000 resamples, seed 2027.','',
           '| Method | Mean seconds [95% CI] | Median seconds [95% CI] | p95 seconds [95% CI] |','|---|---:|---:|---:|']
    for s in SYSTEMS:
        stats=summary[s][latency]
        cells=[f"{stats[k]['estimate']:.4f} [{stats[k]['ci95'][0]:.4f}, {stats[k]['ci95'][1]:.4f}]" for k in ['mean','median','p95']]
        lines.append('| '+s+' | '+' | '.join(cells)+' |')
    lines+=['','## Paired mean differences','', '| Comparison | Metric | Difference | 95% interval |','|---|---|---:|---|']
    for r in paired:lines.append(f"| {r['comparison']} | {r['metric']} | {r['mean_difference']:.6f} | {r['mean_difference_ci95']} |")
    lines+=['',result['limitations']]
    (out/'statistics.md').write_text('\n'.join(lines)+'\n')
    if e2e:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig,axes=plt.subplots(1,3,figsize=(11,3.5))
        for ax,k in zip(axes,['mean','median','p95']):
            vv=[summary[s][latency][k] for s in SYSTEMS];yy=np.array([v['estimate'] for v in vv]);ci=np.array([v['ci95'] for v in vv])
            ax.bar(SYSTEMS,yy,color='gray');ax.errorbar(SYSTEMS,yy,yerr=[np.maximum(0,yy-ci[:,0]),np.maximum(0,ci[:,1]-yy)],fmt='none',ecolor='black',capsize=3)
            ax.set_ylabel('Direct end-to-end seconds');ax.set_title(k);ax.tick_params(axis='x',rotation=20)
        fig.tight_layout();fig.savefig(out/'latency.png',dpi=180);plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('--e2e',action='store_true');a=p.parse_args();analyze(a.source,a.output,a.e2e)
