"""Independent BM25 sanity baseline; never substitute for neural A/B/C results."""
import argparse
import hashlib
import json
import time
from pathlib import Path
import numpy as np
from pythainlp.tokenize import word_tokenize
from rank_bm25 import BM25Okapi
from src.core import metrics


def main(output,data_dir):
    out=Path(output); out.mkdir(parents=True,exist_ok=False)
    docs=[json.loads(s) for s in (Path(data_dir)/'documents.jsonl').read_text().splitlines()]
    qs=[q for q in map(json.loads,(Path(data_dir)/'queries.jsonl').read_text().splitlines()) if q['split']=='development']
    qs=sorted(qs,key=lambda q:hashlib.sha256(('2027'+q['id']).encode()).hexdigest())[:30]
    tokenize=lambda t:word_tokenize(t.lower(),engine='newmm',keep_whitespace=False)
    start=time.perf_counter(); index=BM25Okapi([tokenize(d['text']) for d in docs]); setup=time.perf_counter()-start
    index.get_scores(tokenize(qs[0]['query']))
    rows=[]
    for q in qs:
        start=time.perf_counter(); scores=index.get_scores(tokenize(q['query']))
        ids=[docs[i]['id'] for i in np.argsort(-scores,kind='stable')[:5]]
        elapsed=time.perf_counter()-start
        rows.append({'query_id':q['id'],'group':q['group'],'ranking':ids,'retrieval_seconds':elapsed,**metrics(ids,set(q['relevant']),5)})
    (out/'rows.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
    summary={'system':'BM25-only sanity baseline','split':'development','n':len(rows),'corpus_chunks':len(docs),'setup_seconds':setup,
             **{key:float(np.mean([r[key] for r in rows])) for key in ['recall','mrr','ndcg','retrieval_seconds']}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
    from src.analyze import bootstrap
    import matplotlib.pyplot as plt
    keys=['recall','mrr','ndcg']
    ci={key:bootstrap([r[key] for r in rows],[r['group'] for r in rows]) for key in keys}
    (out/'bootstrap.json').write_text(json.dumps(ci,indent=2))
    means=[summary[key] for key in keys]
    fig,ax=plt.subplots(figsize=(6,4))
    ax.bar(['Recall@5','MRR@5','nDCG@5'],means,color='lightgray',edgecolor='black')
    ax.errorbar(range(3),means,yerr=[[means[i]-ci[k][0] for i,k in enumerate(keys)],
                [ci[k][1]-means[i] for i,k in enumerate(keys)]],fmt='none',color='black',capsize=5)
    ax.set(ylim=(0,1.05),ylabel='Score',title='BM25 only: 30 development queries\nArticle-cluster bootstrap 95% intervals')
    fig.tight_layout();fig.savefig(out/'metrics.png',dpi=180);plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='results/lexical_pilot');p.add_argument('--data-dir',default='data/processed_v2');a=p.parse_args();main(a.output,a.data_dir)
