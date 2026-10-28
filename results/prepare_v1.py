"""Prepare article-disjoint custom splits from the upstream training partition only."""
import argparse
import hashlib
import json
from pathlib import Path
from src.core import chunks, normalize

REVISION = '644a29c59bac62d5b15b9e9b06c55bba00708eca'


def prepare(raw, output):
    rows = [json.loads(line) for line in Path(raw).read_text().splitlines()]
    article_contexts = {}
    for r in rows:
        previous = article_contexts.setdefault(r['article_id'], r['context'])
        if previous != r['context']:
            raise ValueError('Multiple contexts per article: implement article union grouping before splitting')
    docs, queries, excluded, seen_questions = {}, [], [], set()
    for r in rows:
        context = r['context']
        # Group identical contexts even when upstream article IDs differ.
        group = hashlib.sha256(normalize(context).encode()).hexdigest()
        split_value = int(group[:8],16)%10
        split = 'development' if split_value < 6 else ('validation' if split_value < 8 else 'test')
        spans = list(chunks(context))
        for start,end,text in spans:
            did = f'{group}:{start}'
            docs[did] = {'id':did, 'group':group, 'text':normalize(text)}
        valid = [(s,t) for s,t in zip(r['answers']['answer_start'],r['answers']['text'])
                 if t and context[s:s+len(t)] == t]
        relevant = [f'{group}:{start}' for start,end,_ in spans
                    if any(start <= s and s+len(t) <= end for s,t in valid)]
        qnorm = normalize(r['question'])
        if not relevant or qnorm in seen_questions:
            excluded.append(r['question_id'])
            continue
        seen_questions.add(qnorm)
        queries.append({'id':r['question_id'], 'group':group, 'split':split,
                        'query':qnorm, 'answers':[t for _,t in valid], 'relevant':relevant})
    out=Path(output); out.mkdir(parents=True,exist_ok=True)
    for name,items in [('documents',list(docs.values())),('queries',queries)]:
        (out/f'{name}.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in items))
    manifest={'source_revision':REVISION,'source_sha256':hashlib.sha256(Path(raw).read_bytes()).hexdigest(),
              'source_partition':'train only', 'documents':len(docs),'queries':len(queries),
              'split_counts':{s:sum(q['split']==s for q in queries) for s in ['development','validation','test']},
              'excluded_ids':excluded,'chunk_size_chars':600,'overlap_chars':100}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)); print(json.dumps(manifest | {'excluded_ids':len(excluded)},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--raw',default='data/raw/train.jsonl'); p.add_argument('--output',default='data/processed')
    a=p.parse_args(); prepare(a.raw,a.output)
