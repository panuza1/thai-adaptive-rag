"""Offline API smoke check, not an accuracy experiment."""
import json
from pathlib import Path
import numpy as np
import torch
from sentence_transformers import CrossEncoder

cfg=json.loads(Path('experiments/pilot.json').read_text())
torch.set_num_threads(4)
model=CrossEncoder(cfg['reranker_model'],revision=cfg['reranker_revision'],device='cpu',max_length=512,local_files_only=True)
pairs=[('ประเทศไทยมีเมืองหลวงชื่ออะไร','กรุงเทพมหานครเป็นเมืองหลวงของประเทศไทย'),
       ('ประเทศไทยมีเมืองหลวงชื่ออะไร','แมวเป็นสัตว์เลี้ยงลูกด้วยนม')]
scores=np.asarray(model.predict(pairs)).reshape(-1)
assert scores.shape==(2,) and np.isfinite(scores).all()
Path('results/reranker_api_check.json').write_text(json.dumps({'purpose':'synthetic API smoke check only','model':cfg['reranker_model'],'revision':cfg['reranker_revision'],'scores':scores.tolist(),'finite':True},indent=2))
print('Reranker loaded offline; two finite scores returned. No benchmark claim.')
