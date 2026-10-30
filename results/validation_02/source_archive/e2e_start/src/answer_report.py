"""Summarize measured generation; export blinded, unfilled annotation packets."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.analyze import bootstrap
from src.score_answers import score


def report(path):
    out=Path(path)
    read=lambda p:[json.loads(s) for s in p.read_text().splitlines()]
    rows=read(out/'generation.jsonl'); retrieval=read(out/'rows.jsonl')
    config=json.loads((out/'generator_config.json').read_text())
    expected={(q,s) for q in config['query_ids'] for s in ['B1','B2','B3','P1:none']}
    assert len(rows)==len(expected) and {(r['query_id'],r['system']) for r in rows}==expected, 'Generation is incomplete'
    summary=score(rows)
    for system,s in summary.items():
        rs=[r for r in rows if r['system']==system]
        rr=[r for r in retrieval if r['system']==system]
        s.update(total_input_tokens=sum(r['input_tokens'] for r in rs),
                 total_output_tokens=sum(r['output_tokens'] for r in rs),
                 mean_generation_seconds=float(np.mean([r['generation_seconds'] for r in rs])),
                 mean_generation_cpu_seconds=float(np.mean([r['generation_cpu_seconds'] for r in rs])),
                 mean_retrieval_cpu_seconds=float(np.mean([r['cpu_seconds'] for r in rr])),
                 mean_estimated_request_cpu_seconds=float(np.mean([r['cpu_seconds']+r['generation_cpu_seconds'] for r in rs])),
                 token_cap_responses=sum(r['output_tokens']==config['max_new_tokens'] for r in rs),
                 exact_abstention_responses=sum(r['answer'].strip()=='ไม่พบข้อมูลเพียงพอ' for r in rs),
                 api_cost_usd=sum(r['api_cost_usd'] for r in rs))
    (out/'answer_summary.json').write_text(json.dumps(summary,indent=2))
    with (out/'answer_summary.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=['system']+list(next(iter(summary.values()))))
        writer.writeheader();writer.writerows(dict(system=s,**v) for s,v in summary.items())
    paired=[]
    adaptive={r['query_id']:r for r in rows if r['system']=='P1:none'}
    for base in ['B1','B2','B3']:
        b={r['query_id']:r for r in rows if r['system']==base}
        for metric in ['exact_match','estimated_end_to_end_seconds','input_tokens','output_tokens']:
            delta=[adaptive[q][metric]-b[q][metric] for q in adaptive]
            paired.append({'comparison':'P1:none - '+base,'metric':metric,'mean_delta':float(np.mean(delta)),
                           'ci95':bootstrap(delta,[adaptive[q]['group'] for q in adaptive])})
    (out/'answer_paired_bootstrap.json').write_text(json.dumps(paired,indent=2))
    data=Path(json.loads((out/'config.json').read_text())['data_dir'])
    docs={d['id']:d for d in read(data/'documents.jsonl')};queries={q['id']:q for q in read(data/'queries.jsonl')}
    packets=[];mapping=[]
    for r in rows:
        rid=hashlib.sha256(('annotation2027'+r['query_id']+r['system']).encode()).hexdigest()[:16]
        packets.append({'response_id':rid,'question':queries[r['query_id']]['query'],'reference_answers':r['references'],
                        'answer':r['answer'],'evidence':[{'id':d,'text':docs[d]['text']} for d in r['ranking']],
                        'human_correctness':None,'claims':None,'rationale':None})
        mapping.append({'response_id':rid,'query_id':r['query_id'],'system':r['system']})
    packets.sort(key=lambda r:r['response_id'])
    assert len({r['response_id'] for r in packets})==len(packets)
    (out/'annotation_packet.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in packets))
    (out/'annotation_mapping_private.json').write_text(json.dumps(mapping,indent=2))
    totals={'retrieval_rows':len(retrieval),'generation_rows':len(rows),
            'measured_retrieval_wall_seconds_all_repeats_and_ablations':sum(r['retrieval_seconds'] for r in retrieval),
            'measured_retrieval_process_cpu_seconds_all_repeats_and_ablations':sum(r['cpu_seconds'] for r in retrieval),
            'measured_generation_wall_seconds':sum(r['generation_seconds'] for r in rows),
            'measured_generation_process_cpu_seconds':sum(r['generation_cpu_seconds'] for r in rows),
            'shared_index_setup_wall_seconds':json.loads((out/'metadata.json').read_text())['setup_seconds'],
            'input_tokens':sum(r['input_tokens'] for r in rows),'output_tokens':sum(r['output_tokens'] for r in rows),
            'api_cost_usd':0,'energy_kwh':None,'hardware_cost_usd':None,
            'note':'Wall segments are measured separately. Loading/download/analysis/idle time is excluded; this is not a direct full-request benchmark or total financial cost.'}
    (out/'computational_cost.json').write_text(json.dumps(totals,indent=2))
    names=['B1','B2','B3','P1:none'];fig,axes=plt.subplots(1,3,figsize=(11,3.6))
    for ax,key,label in zip(axes,['exact_match','mean_estimated_end_to_end_seconds','mean_input_tokens'],['Strict exact match','Estimated request latency (s)','Mean input tokens']):
        ax.bar(names,[summary[s][key] for s in names],color='gray');ax.set_ylabel(label);ax.tick_params(axis='x',rotation=20)
    fig.tight_layout();fig.savefig(out/'answer_comparison.png',dpi=180);plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path');report(p.parse_args().path)
