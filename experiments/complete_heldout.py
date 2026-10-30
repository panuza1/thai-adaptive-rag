"""Run the frozen held-out protocol after existing downloads; preserve prior outputs."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from huggingface_hub import constants

os.chdir(Path(__file__).resolve().parents[1])
status=Path('results/heldout_status.json')
def record(state, **detail): status.write_text(json.dumps({'state':state,**detail},indent=2))
env=os.environ.copy();env.pop('PYTHONPATH',None)
env.update(HF_HUB_OFFLINE='1',OPENBLAS_NUM_THREADS='4',OMP_NUM_THREADS='4')
def run(*args): subprocess.run([sys.executable,*args],env=env,check=True)
try:
    record('waiting_for_existing_e5_job')
    for _ in range(360):
        s=json.loads(Path('results/resume_status.json').read_text())
        if s['state']=='retrieval_pilot_complete': break
        if s['state']=='failed': raise RuntimeError(s.get('error','E5 job failed'))
        time.sleep(5)
    else: raise TimeoutError('Existing E5 job has not completed')
    record('heldout_retrieval')
    run('-m','src.run','--config','experiments/heldout.json','--output','results/heldout_01')
    run('-m','src.analyze','results/heldout_01')
    c=json.loads(Path('experiments/generator.json').read_text())
    partial=Path('data/models/generator.safetensors.part')
    for attempt in range(1,41):
        record('downloading_generator',attempt=attempt,bytes=partial.stat().st_size if partial.exists() else 0)
        result=subprocess.run(['curl','--fail','--location','--connect-timeout','15','--max-time','50','--continue-at','-',
            f'https://huggingface.co/{c["model"]}/resolve/{c["revision"]}/model.safetensors','-o',str(partial)])
        if result.returncode==0: break
    else: raise RuntimeError('Generator download incomplete; partial bytes retained')
    h=hashlib.sha256()
    with partial.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    if h.hexdigest()!=c['sha256']: raise ValueError('Generator integrity check failed')
    snapshot=Path(constants.HF_HUB_CACHE)/('models--'+c['model'].replace('/','--'))/'snapshots'/c['revision']
    target=snapshot/'model.safetensors'
    if not target.exists(): os.link(partial,target)
    record('development_end_to_end_smoke',generator_sha256=h.hexdigest())
    run('-m','src.generate','results/pilot_04','--model',c['model'],'--revision',c['revision'],'--limit','1')
    smoke=[json.loads(s) for s in Path('results/pilot_04/generation.jsonl').read_text().splitlines()]
    assert len(smoke)==4 and all(r['output_tokens']>0 and r['input_tokens']>0 for r in smoke)
    record('heldout_generation')
    run('-m','src.generate','results/heldout_01','--model',c['model'],'--revision',c['revision'])
    with Path('results/heldout_01/answer_summary.json').open('w') as f:
        subprocess.run([sys.executable,'-m','src.score_answers','results/heldout_01/generation.jsonl'],env=env,stdout=f,check=True)
    record('automatic_experiments_complete',faithfulness='pending evidence annotation',human_correctness='pending')
except Exception as error:
    record('failed',error=str(error));raise
