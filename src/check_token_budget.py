"""Corpus/query token lengths only; never reads gold answers for evaluation."""
import argparse
import json
from pathlib import Path
from transformers import AutoTokenizer


def main(config):
    cfg=json.loads(Path(config).read_text())
    docs=[json.loads(s) for s in Path('data/processed/documents.jsonl').read_text().splitlines()]
    qs=[json.loads(s) for s in Path('data/processed/queries.jsonl').read_text().splitlines()]
    report={}
    for key in ['embedding','reranker']:
        t=AutoTokenizer.from_pretrained(cfg[key+'_model'],revision=cfg[key+'_revision'])
        lengths=[len(t.encode(('passage: ' if key=='embedding' else '')+d['text'],add_special_tokens=False)) for d in docs]
        qlengths=[len(t.encode(('query: ' if key=='embedding' else '')+q['query'],add_special_tokens=False)) for q in qs]
        upper=max(lengths)+max(qlengths)+t.num_special_tokens_to_add(pair=True)
        report[key]={'max_document_tokens_without_specials':max(lengths),'max_query_tokens_without_specials':max(qlengths),
                     'pair_token_upper_bound':upper,'pair_exceeds_512':upper>512}
        assert max(lengths)>0 and max(qlengths)>0
    Path('results/tokenizer_audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('config');main(p.parse_args().config)
