import pytest
from src.core import chunks, metrics, normalize, route, rrf, exact_match


def test_metrics():
    m=metrics(['x','a','b'],{'a','b'},2)
    assert m['recall']==.5 and m['mrr']==.5
    assert m['ndcg']==pytest.approx((1/1.584962500721156)/(1+1/1.584962500721156))
    assert metrics(['x'],{'a'},5)=={'recall':0,'mrr':0,'ndcg':0}
    with pytest.raises(ValueError): metrics(['a','a'],{'a'},2)


def test_chunk_spans():
    text='กขคงจฉชซฌญ'
    spans=list(chunks(text,6,2))
    assert spans==[(0,6,text[:6]),(4,10,text[4:])]
    with pytest.raises(ValueError): list(chunks(text,2,2))


def test_policy_and_ablations():
    c={'complexity_length':24,'margin_threshold':.02}
    f={'length':5,'margin':.1,'exact':False}
    assert route(f,c)=='A'
    assert route(f|{'exact':True},c)=='B'
    assert route(f|{'margin':0},c)=='C'
    assert route(f|{'length':24},c)=='C'
    assert route(f|{'margin':0},c,'confidence')=='A'
    assert route(f|{'length':24},c,'complexity')=='A'
    assert route(f|{'exact':True},c,'keyword')=='A'
    assert route(f|{'exact':True},c,'hybrid')=='A'
    assert route(f|{'margin':0},c,'reranking')=='B'


def test_fusion_and_normalization():
    assert rrf([['b','a'],['a','c']])[0]=='a'
    assert normalize('ไทย\u200b  ภาษา')=='ไทย ภาษา'
    assert exact_match(' ไทย ',['ไทย'])==1


def test_span_relevance_rejects_invalid_offsets(tmp_path):
    import json
    from src.prepare import prepare
    raw=tmp_path/'raw'; raw.write_text(json.dumps({'article_id':'a','question_id':'1','context':'ภาษาไทย','question':'อะไร','answers':{'text':['ไทย'],'answer_start':[0]}}))
    prepare(raw,tmp_path/'out')
    assert not (tmp_path/'out'/'queries.jsonl').read_text()


def test_thai_bm25_actual_library():
    import numpy as np
    from pythainlp.tokenize import word_tokenize
    from rank_bm25 import BM25Okapi
    docs=['แมวกินปลา','รถไฟวิ่งเร็ว','ดวงอาทิตย์ส่องแสง']
    tokens=[word_tokenize(d,engine='newmm',keep_whitespace=False) for d in docs]
    assert np.argmax(BM25Okapi(tokens).get_scores(word_tokenize('รถไฟ',engine='newmm')))==1
