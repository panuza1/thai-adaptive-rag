import json
from src.prepare import prepare


def test_split_and_evidence(tmp_path):
    row={'article_id':'a','question_id':'1','context':'กขคงจฉ','question':'อะไร','answers':{'text':['คง'],'answer_start':[2]}}
    raw=tmp_path/'raw.jsonl'; raw.write_text(json.dumps(row)+'\n'+json.dumps(row|{'question_id':'2','question':'ที่ไหน'})+'\n')
    out=tmp_path/'out'; prepare(raw,out)
    qs=[json.loads(s) for s in (out/'queries.jsonl').read_text().splitlines()]
    assert len(qs)==2 and qs[0]['split']==qs[1]['split']
    assert qs[0]['relevant']==qs[1]['relevant']


def test_same_title_variant_contexts_stay_together(tmp_path):
    row={'article_id':'a','title':'บทความ','question_id':'1','context':'กขคงจฉ','question':'อะไร','answers':{'text':['คง'],'answer_start':[2]}}
    other=row|{'article_id':'b','question_id':'2','context':'กขคงจฉ เพิ่มเติม','question':'ที่ไหน'}
    raw=tmp_path/'raw';raw.write_text(json.dumps(row)+'\n'+json.dumps(other))
    prepare(raw,tmp_path/'out')
    qs=[json.loads(s) for s in (tmp_path/'out'/'queries.jsonl').read_text().splitlines()]
    assert qs[0]['group']==qs[1]['group'] and qs[0]['split']==qs[1]['split']


def test_normalized_context_variants_do_not_overwrite_chunks(tmp_path):
    row={'article_id':'a','title':'บทความ','question_id':'1','context':'ก ขคง','question':'อะไร','answers':{'text':['คง'],'answer_start':[3]}}
    other=row|{'article_id':'b','question_id':'2','context':'ก  ขคง','question':'ที่ไหน','answers':{'text':['คง'],'answer_start':[4]}}
    raw=tmp_path/'raw';raw.write_text(json.dumps(row)+'\n'+json.dumps(other))
    prepare(raw,tmp_path/'out')
    qs=[json.loads(s) for s in (tmp_path/'out'/'queries.jsonl').read_text().splitlines()]
    docs=[json.loads(s) for s in (tmp_path/'out'/'documents.jsonl').read_text().splitlines()]
    assert len(docs)==2 and qs[0]['group']==qs[1]['group']
    assert qs[0]['relevant']!=qs[1]['relevant']
