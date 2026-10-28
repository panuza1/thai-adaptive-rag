"""Pure retrieval policy and evaluation utilities; no model downloads."""
import math
import re
import unicodedata
from collections import Counter


def normalize(text):
    return ' '.join(unicodedata.normalize('NFC', text).replace('\u200b', '').split())


def chunks(text, size=600, overlap=100):
    if not 0 <= overlap < size:
        raise ValueError('Require 0 <= overlap < size')
    # shortcut: character windows can cut Thai words; assess token-window chunking before final experiments.
    for start in range(0, len(text), size-overlap):
        yield start, min(start+size, len(text)), text[start:start+size]
        if start+size >= len(text):
            break


def rrf(rankings, constant=60):
    scores = Counter()
    for ranking in rankings:
        for rank, doc in enumerate(dict.fromkeys(ranking), 1):
            scores[doc] += 1/(constant+rank)
    return sorted(scores, key=lambda doc: (-scores[doc], doc))


def route(features, config, ablation='none'):
    complex_query = ablation != 'complexity' and features['length'] >= config['complexity_length']
    uncertain = ablation != 'confidence' and features['margin'] < config['margin_threshold']
    exact = ablation != 'keyword' and features['exact']
    strategy = 'C' if complex_query or uncertain else ('B' if exact else 'A')
    if ablation == 'hybrid' and strategy == 'B':
        strategy = 'A'
    if ablation == 'reranking' and strategy == 'C':
        strategy = 'B'
    return strategy


def metrics(ranking, relevant, k):
    if not relevant or k <= 0 or len(ranking) != len(set(ranking)):
        raise ValueError('Nonempty relevance, positive k, unique ranking required')
    hits = [int(d in relevant) for d in ranking[:k]]
    dcg = sum(h/math.log2(i+2) for i,h in enumerate(hits))
    ideal = sum(1/math.log2(i+2) for i in range(min(k,len(relevant))))
    return {'recall': sum(hits)/len(relevant),
            'mrr': next((1/(i+1) for i,h in enumerate(hits) if h),0),
            'ndcg': dcg/ideal}


def exact_match(answer, references):
    return float(any(normalize(answer) == normalize(r) for r in references))


def query_features(query, tokens, scores):
    return {'length': len(tokens), 'exact': bool(re.search(r'[0-9๐-๙A-Za-z]|["“”]',query)),
            'margin': float(scores[0]-scores[1]) if len(scores)>1 else 0.0}
