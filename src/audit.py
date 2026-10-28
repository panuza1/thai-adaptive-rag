"""Corpus-only duplicate audit: does not evaluate held-out queries."""
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from src.core import normalize


def main():
    queries=[json.loads(s) for s in Path('data/processed/queries.jsonl').read_text().splitlines()]
    group_split={}
    for q in queries:
        assert group_split.setdefault(q['group'],q['split'])==q['split'], 'Group leakage'
    assert len({q['query'] for q in queries})==len(queries),'Duplicate query leakage'
    raw=[json.loads(s) for s in Path('data/raw/train.jsonl').read_text().splitlines()]
    contexts=sorted(set(normalize(r['context']) for r in raw))
    import hashlib
    groups=[hashlib.sha256(t.encode()).hexdigest() for t in contexts]
    vectorizer=TfidfVectorizer(analyzer='char',ngram_range=(5,5),min_df=2,max_features=50000)
    x=vectorizer.fit_transform(contexts); similarities=(x@x.T).tocoo()
    pairs=[]
    for i,j,value in zip(similarities.row,similarities.col,similarities.data):
        if i<j and value>=.9 and groups[i] in group_split and groups[j] in group_split and group_split[groups[i]]!=group_split[groups[j]]:
            pairs.append({'group_a':groups[i],'group_b':groups[j],'cosine':float(value)})
    report={'exact_group_disjoint':True,'unique_queries':len(queries),'unique_contexts':len(contexts),
            'cross_split_near_duplicate_candidates':pairs,'method':'char 5gram TF-IDF cosine >=0.9, min_df=2, max_features=50000',
            'limitation':'heuristic candidates; not proof that no semantic duplicates exist'}
    Path('results/data_audit.json').write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))

if __name__=='__main__':main()
