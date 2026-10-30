"""Online retrieval timing includes query embedding and routing; no cached query results."""
import argparse
import hashlib
import json
import platform
import random
import subprocess
import time
from pathlib import Path
import numpy as np
import torch
from huggingface_hub import model_info
from pythainlp.tokenize import word_tokenize
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder
from src.core import metrics, query_features, route, rrf


def tokens(text):
    return word_tokenize(text.lower(),engine='newmm',keep_whitespace=False)


def main(config_path, output):
    cfg=json.loads(Path(config_path).read_text()); out=Path(output); out.mkdir(parents=True,exist_ok=False)
    data_dir=Path(cfg.get('data_dir','data/processed'))
    source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('src').glob('*.py')}
    if not (cfg['candidate_k'] >= cfg['k'] > 0 and cfg['repeats'] > 0):
        raise ValueError('Require candidate_k >= k > 0 and repeats > 0')
    random.seed(cfg['seed']); np.random.seed(cfg['seed']); torch.manual_seed(cfg['seed']); torch.set_num_threads(cfg['threads'])
    docs=[json.loads(s) for s in (data_dir/'documents.jsonl').read_text().splitlines()]
    queries=[json.loads(s) for s in (data_dir/'queries.jsonl').read_text().splitlines()]
    queries=sorted((q for q in queries if q['split']==cfg['split']),key=lambda q:hashlib.sha256((str(cfg['seed'])+q['id']).encode()).hexdigest())
    if cfg['query_limit']: queries=queries[:cfg['query_limit']]
    if not queries: raise ValueError('No evaluation queries')
    for key in ['embedding','reranker']:
        if key+'_revision' not in cfg:
            cfg[key+'_revision']=model_info(cfg[key+'_model']).sha
    (out/'config.json').write_text(json.dumps(cfg,indent=2))
    start=time.perf_counter()
    encoder=SentenceTransformer(cfg['embedding_model'],revision=cfg['embedding_revision'],device=cfg['device'])
    encoder.max_seq_length=512
    reranker=CrossEncoder(cfg['reranker_model'],revision=cfg['reranker_revision'],device=cfg['device'],max_length=512)
    bm25=BM25Okapi([tokens(d['text']) for d in docs])
    vectors=encoder.encode(['passage: '+d['text'] for d in docs],normalize_embeddings=True,batch_size=16,show_progress_bar=True)
    setup_seconds=time.perf_counter()-start
    def retrieve(query,system):
        start=time.perf_counter(); cpu_start=time.process_time()
        vector=encoder.encode(['query: '+query],normalize_embeddings=True)[0]
        scores=vectors@vector; dense=np.argsort(-scores,kind='stable')[:cfg['candidate_k']].tolist()
        routing_start=time.perf_counter()
        features=query_features(query,tokens(query),scores[dense]) if system.startswith('P1') else {}
        ablation=system.split(':')[1] if ':' in system else 'none'
        strategy=route(features,cfg,ablation) if system.startswith('P1') else {'B1':'A','B2':'B','B3':'C'}[system]
        routing_seconds=time.perf_counter()-routing_start
        ranked=dense
        if strategy in ['B','C'] and ablation!='hybrid':
            sparse=np.argsort(-bm25.get_scores(tokens(query)),kind='stable')[:cfg['candidate_k']].tolist()
            ranked=rrf([dense,sparse])[:cfg['candidate_k']]
        pairs=0
        if strategy=='C':
            pairs=len(ranked)
            values=reranker.predict([(query,docs[i]['text']) for i in ranked],batch_size=16,show_progress_bar=False)
            ranked=[ranked[i] for i in np.argsort(-np.asarray(values).reshape(-1),kind='stable')]
        return [docs[i]['id'] for i in ranked[:cfg['k']]], {'strategy':strategy,'features':features,
            'retrieval_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu_start,
            'router_seconds':routing_seconds if system.startswith('P1') else 0,'reranked_pairs':pairs}
    systems=['B1','B2','B3']+['P1:'+a for a in cfg['ablations']]
    for system in systems: retrieve(queries[0]['query'],system)
    with (out/'rows.jsonl').open('w') as f:
        for repeat in range(cfg['repeats']):
            for q in queries:
                order=systems.copy(); random.shuffle(order)
                for system in order:
                    ranking,detail=retrieve(q['query'],system)
                    row={'query_id':q['id'],'group':q['group'],'system':system,'repeat':repeat,'ranking':ranking,
                         **detail,**metrics(ranking,set(q['relevant']),cfg['k'])}
                    f.write(json.dumps(row,ensure_ascii=False)+'\n'); f.flush()
                print('completed',repeat,q['id'],flush=True)
    metadata={'platform':platform.platform(),'python':platform.python_version(),'processor':platform.processor(),
              'setup_seconds':setup_seconds,'data_manifest':json.loads((data_dir/'manifest.json').read_text()),
              'api_cost_usd':0,'generation_status':'not run',
              'source_hashes':source_hashes}
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2))
    (out/'requirements.lock.txt').write_text(subprocess.check_output(['.venv/bin/pip','freeze'],text=True))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--config',default='experiments/pilot.json'); p.add_argument('--output',required=True)
    a=p.parse_args(); main(a.config,a.output)
