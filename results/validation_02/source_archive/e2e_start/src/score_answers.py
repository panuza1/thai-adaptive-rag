"""Score adjudicated annotations; missing annotations stay missing."""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def score(rows):
    grouped=defaultdict(list)
    for r in rows:
        for key in ['human_correctness','abstention_correct']:
            if r.get(key) is not None and r[key] not in [0,1]:
                raise ValueError('Adjudicated binary labels must be 0, 1 or null')
        grouped[r['system']].append(r)
    result={}
    for system,rs in grouped.items():
        def mean(key):
            values=[r[key] for r in rs if r.get(key) is not None]
            return sum(values)/len(values) if values else None
        labeled=[r for r in rs if r.get('supported_claims') is not None and r.get('unsupported_claims') is not None]
        for r in labeled:
            for key in ['supported_claims','unsupported_claims']:
                if not isinstance(r[key],int) or r[key]<0: raise ValueError('Claim counts must be nonnegative integers')
        supported=sum(r['supported_claims'] for r in labeled)
        unsupported=sum(r['unsupported_claims'] for r in labeled)
        total=supported+unsupported
        factual=[r for r in labeled if r['supported_claims']+r['unsupported_claims']>0]
        result[system]={'responses':len(rs),'claim_labeled_responses':len(labeled),
                        'exact_match':mean('exact_match'),'human_correctness':mean('human_correctness'),
                        'faithfulness_micro':supported/total if total else None,
                        'unsupported_claim_rate_micro':unsupported/total if total else None,
                        'hallucination_rate_factual_responses':sum(r['unsupported_claims']>0 for r in factual)/len(factual) if factual else None,
                        'abstention_accuracy':mean('abstention_correct'),
                        'mean_input_tokens':mean('input_tokens'),'mean_output_tokens':mean('output_tokens'),
                        'mean_estimated_end_to_end_seconds':mean('estimated_end_to_end_seconds')}
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('annotations');a=p.parse_args()
    print(json.dumps(score([json.loads(s) for s in Path(a.annotations).read_text().splitlines()]),indent=2))
