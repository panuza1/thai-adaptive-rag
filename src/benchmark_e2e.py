"""Direct warm request timing with paired frozen queries; never edits prior results."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import subprocess
import time
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from src.run import build_retriever
from src.generate import prompt
from src.core import metrics, exact_match


def request(query,system,retrieve,docs,tok,llm,clock=time.perf_counter):
    start=clock();cpu_start=time.process_time()
    ranking,detail=retrieve(query,system)
    text=tok.apply_chat_template(prompt(query,[docs[d] for d in ranking]),tokenize=False,add_generation_prompt=True)
    inputs=tok(text,return_tensors='pt',add_special_tokens=False);n=inputs['input_ids'].shape[1]
    if n+128>4096:raise ValueError('Fixed context budget exceeded')
    output=llm.generate(**inputs,max_new_tokens=128,do_sample=False,pad_token_id=tok.eos_token_id)
    generated=output[0,n:];answer=tok.decode(generated,skip_special_tokens=True)
    elapsed=clock()-start;cpu=time.process_time()-cpu_start
    return dict(ranking=ranking,answer=answer,end_to_end_seconds=elapsed,request_cpu_seconds=cpu,
                input_tokens=n,output_tokens=len(generated),**detail)


def main(output):
    out=Path(output);out.mkdir(parents=True,exist_ok=False)
    prior=Path('results/heldout_01');cfg=json.loads((prior/'config.json').read_text())
    gen=json.loads((prior/'generator_config.json').read_text())
    ids=json.loads(Path('experiments/heldout_query_ids.json').read_text())
    rng=random.Random(2028);query_order=ids.copy();rng.shuffle(query_order)
    systems=['B1','B2','B3','P1:none'];schedule=[]
    for i,q in enumerate(query_order):
        if i%4==0:base=systems.copy();rng.shuffle(base)
        order=base[i%4:]+base[:i%4]
        schedule.extend({'query_id':q,'system':s,'position':j} for j,s in enumerate(order))
    assert len(schedule)==240
    protocol={'retrieval':cfg,'generator':gen,'schedule_seed':2028,'schedule':schedule,'repetitions':1,
              'timing':'Single perf_counter interval from before query encoding through final answer decode; includes routing, retrieval, reranking, evidence assembly and generation. Excludes model/index setup, evaluation metrics and file logging.',
              'source_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('src').glob('*.py')}}
    (out/'config.json').write_text(json.dumps(protocol,indent=2))
    def status(state,**kw):(out/'status.json').write_text(json.dumps(dict(state=state,**kw),indent=2))
    status('loading')
    random.seed(cfg['seed']);np.random.seed(cfg['seed']);torch.manual_seed(cfg['seed']);torch.set_num_threads(cfg['threads'])
    data=Path(cfg['data_dir']);docs=[json.loads(s) for s in (data/'documents.jsonl').read_text().splitlines()]
    queries={q['id']:q for q in map(json.loads,(data/'queries.jsonl').read_text().splitlines())}
    assert all(queries[q]['split']=='test' for q in ids)
    start=time.perf_counter();retrieve,retrieval_setup=build_retriever(cfg,docs);docs={d['id']:d for d in docs}
    tok=AutoTokenizer.from_pretrained(gen['model'],revision=gen['revision'])
    llm=AutoModelForCausalLM.from_pretrained(gen['model'],revision=gen['revision']).to('cpu').eval()
    setup=time.perf_counter()-start
    metadata={'platform':platform.platform(),'python':platform.python_version(),'threads':torch.get_num_threads(),
              'setup_seconds':setup,'retrieval_setup_seconds':retrieval_setup,'generator_dtype':str(next(llm.parameters()).dtype),
              'lscpu':subprocess.check_output(['lscpu'],text=True),'api_cost_usd':0,
              'environment':{k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','HF_HUB_OFFLINE']}}
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2))
    gold={(r['query_id'],r['system']):r for r in map(json.loads,(prior/'generation.jsonl').read_text().splitlines())}
    warm=next(q for q in queries.values() if q['split']=='development')
    with torch.inference_mode():
        status('development_warmup')
        with (out/'warmup.jsonl').open('w') as f:
            for system in systems:
                r=request(warm['query'],system,retrieve,docs,tok,llm)
                f.write(json.dumps(dict(query_id=warm['id'],system=system,**r),ensure_ascii=False)+'\n');f.flush()
        with (out/'rows.jsonl').open('w') as f:
            for i,item in enumerate(schedule):
                status('running',completed=i,total=len(schedule),current=item)
                q=queries[item['query_id']];r=request(q['query'],item['system'],retrieve,docs,tok,llm)
                original=gold[(q['id'],item['system'])]
                row=dict(**item,group=q['group'],repeat=0,**r,**metrics(r['ranking'],set(q['relevant']),cfg['k']),
                         exact_match=exact_match(r['answer'],q['answers']),same_ranking_as_original=r['ranking']==original['ranking'],
                         same_answer_as_original=r['answer']==original['answer'])
                f.write(json.dumps(row,ensure_ascii=False)+'\n');f.flush()
                print('completed',i+1,'of',len(schedule),flush=True)
    status('complete',completed=len(schedule),total=len(schedule))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
