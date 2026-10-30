import numpy as np
import pytest
from src.validate_statistics import cluster_indices,summarize
from src.benchmark_e2e import request


def test_cluster_resampling_retains_article_members():
    indices=cluster_indices(['a','a','b'],n=30)
    assert all(list(ix).count(0)==list(ix).count(1) for ix in indices)
    stats=summarize([2,2,2],indices)
    assert all(v['estimate']==2 and v['ci95']==[2,2] for v in stats.values())


def test_direct_timer_surrounds_whole_request():
    events=[]
    def clock():events.append('clock');return 10 if len(events)==1 else 17
    def retrieve(q,s):events.append('retrieve');return ['d'],{'retrieval_seconds':1}
    class Tokenizer:
        eos_token_id=0
        def apply_chat_template(self,*a,**k):events.append('template');return 'prompt'
        def __call__(self,*a,**k):events.append('tokenize');return {'input_ids':np.array([[1,2]])}
        def decode(self,*a,**k):events.append('decode');return 'answer'
    class Model:
        def generate(self,**k):events.append('generate');return np.array([[1,2,3]])
    r=request('q','B1',retrieve,{'d':{'id':'d','text':'evidence'}},Tokenizer(),Model(),clock)
    assert r['end_to_end_seconds']==7
    assert events==['clock','retrieve','template','tokenize','generate','decode','clock']
