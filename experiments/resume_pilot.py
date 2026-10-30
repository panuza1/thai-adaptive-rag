"""Resume the pinned E5 download, verify bytes, then run the development pilot."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from huggingface_hub import hf_hub_download, constants

root=Path(__file__).resolve().parents[1]
os.chdir(root)
status=Path('results/resume_status.json')
def record(state, **details):
    status.write_text(json.dumps({'state':state,**details},indent=2))

try:
    cfg=json.loads(Path('experiments/pilot.json').read_text())
    revision=cfg['embedding_revision']
    expected='1a55775f53449dac10a2bcbc312469fac40b96d53198c407081a831f81c98477'
    partial=Path('data/models/e5.safetensors.part')
    for attempt in range(1,31):
        record('downloading',attempt=attempt,bytes=partial.stat().st_size if partial.exists() else 0)
        result=subprocess.run(['curl','--fail','--location','--connect-timeout','15','--max-time','50','--continue-at','-',
            f'https://huggingface.co/{cfg["embedding_model"]}/resolve/{revision}/model.safetensors','-o',str(partial)])
        if result.returncode==0: break
    else: raise RuntimeError('Download did not finish within 30 bounded attempts; partial bytes retained')
    digest=hashlib.file_digest(partial.open('rb'),'sha256').hexdigest() if sys.version_info>=(3,11) else hashlib.sha256(partial.read_bytes()).hexdigest()
    if digest!=expected: raise ValueError('E5 SHA256 mismatch; refusing to load')
    snapshot=Path(constants.HF_HUB_CACHE)/'models--intfloat--multilingual-e5-small'/'snapshots'/revision
    target=snapshot/'model.safetensors'
    if not target.exists(): os.link(partial,target)
    hf_hub_download(cfg['embedding_model'],'1_Pooling/config.json',revision=revision)
    record('running_retrieval',sha256=digest)
    env=os.environ.copy();env.pop('PYTHONPATH',None)
    env.update(HF_HUB_OFFLINE='1',OPENBLAS_NUM_THREADS='4',OMP_NUM_THREADS='4')
    output='results/pilot_04'
    subprocess.run([sys.executable,'-m','src.run','--config','experiments/pilot.json','--output',output],env=env,check=True)
    record('analyzing')
    subprocess.run([sys.executable,'-m','src.analyze',output],env=env,check=True)
    record('retrieval_pilot_complete',output=output,generation='pending model download and annotation')
except Exception as error:
    record('failed',error=str(error));raise
