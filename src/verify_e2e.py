"""Read-only integrity checks for a complete frozen direct benchmark."""
import hashlib
import json
import math
from pathlib import Path


def verify():
    base=Path('results/e2e_01');cfg=json.loads((base/'config.json').read_text())
    rows=[json.loads(s) for s in (base/'rows.jsonl').read_text().splitlines()]
    ids=set(json.loads(Path('experiments/heldout_query_ids.json').read_text()))
    expected={(q,s) for q in ids for s in ['B1','B2','B3','P1:none']}
    assert len(rows)==240 and {(r['query_id'],r['system']) for r in rows}==expected
    assert [(r['query_id'],r['system'],r['position']) for r in rows]==[(r['query_id'],r['system'],r['position']) for r in cfg['schedule']]
    for r in rows:
        for key in ['end_to_end_seconds','request_cpu_seconds','retrieval_seconds','cpu_seconds','router_seconds','recall','ndcg']:
            assert isinstance(r[key],(int,float)) and math.isfinite(r[key]) and r[key]>=0,(r['query_id'],key)
        assert r['end_to_end_seconds']>=r['retrieval_seconds']>0
        assert 0<=r['recall']<=1 and 0<=r['ndcg']<=1
        assert len(r['ranking'])==len(set(r['ranking']))==5
        assert r['input_tokens']>0 and 0<r['output_tokens']<=128
    prior=Path('results/heldout_01')
    assert cfg['retrieval']==json.loads((prior/'config.json').read_text())
    assert cfg['generator']==json.loads((prior/'generator_config.json').read_text())
    metadata=json.loads((base/'metadata.json').read_text())
    assert metadata['threads']==cfg['retrieval']['threads']==4
    assert cfg['retrieval']['device']=='cpu' and metadata['generator_dtype']=='torch.bfloat16'
    hashes=json.loads(Path('results/validation_02/original_output_hashes.json').read_text())
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in hashes.items())
    return {'requests':240,'unique_pairs':240,'queries_per_method':60,'finite_measurements':True,'schedule_consistency':True,'configuration_consistency':True,'original_outputs_unchanged':True,'hardware_metadata':metadata}
