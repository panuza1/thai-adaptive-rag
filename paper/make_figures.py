"""Publication figures derived from immutable observed retrieval data."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
rs={r['system']:r for r in csv.DictReader((ROOT.parent/'results/heldout_01/summary.csv').open())}
plt.rcParams.update({'font.size':10,'font.family':'DejaVu Serif'})
fig,ax=plt.subplots(figsize=(4,3))
for name,marker in zip(['B1','B2','B3','P1:none'],['o','s','^','x']):
 r=rs[name];x=float(r['retrieval_seconds'])*1000;y=float(r['ndcg'])
 ax.scatter(x,y,c='black',marker=marker);ax.annotate('P1' if name=='P1:none' else name,(x,y),xytext=(4,5),textcoords='offset points')
ax.set_xscale('log');ax.set_xlabel('Mean retrieval latency (ms, log scale)');ax.set_ylabel('nDCG@5');ax.margins(x=.25,y=.25)
fig.tight_layout();fig.savefig(ROOT/'qa/retrieval_figure.png',dpi=250);plt.close(fig)
fig,ax=plt.subplots(figsize=(4,3))
keys=['complexity','keyword','confidence','hybrid','reranking'];base=float(rs['P1:none']['ndcg'])
ax.bar(['Length','Exact','Margin','Hybrid','Rerank'],[float(rs['P1:'+k]['ndcg'])-base for k in keys],color='gray')
ax.axhline(0,color='black',linewidth=.6);ax.set_xlabel('Removed component');ax.set_ylabel('Change in nDCG@5');ax.tick_params(axis='x',rotation=25)
fig.tight_layout();fig.savefig(ROOT/'qa/ablation_figure.png',dpi=250);plt.close(fig)
