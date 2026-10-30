"""Finalize only a complete direct benchmark; preserve original experiment files."""
import hashlib
import json
from pathlib import Path
from src.validate_statistics import analyze
from src.verify_e2e import verify
import numpy as np


def main():
    out=Path('results/validation_02');source=Path('results/e2e_01')
    status=json.loads((source/'status.json').read_text());assert status['state']=='complete' and status['completed']==240
    (out/'integrity_checks.json').write_text(json.dumps(verify(),indent=2))
    original=json.loads((out/'original_output_hashes.json').read_text())
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in original.items())
    analyze(source,out/'end_to_end',e2e=True)
    rows=[json.loads(s) for s in (source/'rows.jsonl').read_text().splitlines()]
    stats=json.loads((out/'end_to_end/statistics.json').read_text());metric='end_to_end_seconds'
    summary=stats['summary'];p1=summary['P1:none'][metric]['mean']['estimate'];b3=summary['B3'][metric]['mean']['estimate']
    # All paired records use a single directly measured request interval.
    lines=['### Direct end-to-end latency validation','',
           'The integrated benchmark completed 240 requests on the same 60 frozen questions, with one request per method/question and balanced within-query execution positions. The reported interval starts before dense query encoding and ends after final answer decoding. No separate stage durations are added to obtain this measurement.','',
           '| Method | Mean (s) | Median (s) | p95 (s) | SD (s) |','|---|---:|---:|---:|---:|']
    deviations={}
    for s in ['B1','B2','B3','P1:none']:
        v=summary[s][metric];sd=float(np.std([r[metric] for r in rows if r['system']==s],ddof=1));deviations[s]=sd
        lines.append('| '+('P1' if s=='P1:none' else s)+' | '+' | '.join(f"{v[k]['estimate']:.3f}" for k in ['mean','median','p95'])+f' | {sd:.3f} |')
    (out/'end_to_end/standard_deviation.json').write_text(json.dumps({'ddof':1,'seconds':deviations},indent=2))
    lines+=['','Mean latency 95% article-cluster bootstrap intervals are '+ '; '.join(s.replace(':none','')+f" [{summary[s][metric]['mean']['ci95'][0]:.3f}, {summary[s][metric]['mean']['ci95'][1]:.3f}] seconds" for s in ['B1','B2','B3','P1:none'])+'.',
            '',f'P1 versus B3 has an observed direct mean latency reduction of {100*(1-p1/b3):.2f}% (negative means slower). This comparison measures the complete warm request and should not be confused with the 80.85% retrieval-only reduction.']
    for c in stats['paired']:
        if c['metric']==metric and c['comparison']=='B3 - P1:none':
            lines+=['',f"The P1-minus-B3 mean difference is {-c['mean_difference']:.4f} seconds, with 95% interval [{-c['mean_difference_ci95'][1]:.4f}, {-c['mean_difference_ci95'][0]:.4f}]. No formal significance or equivalence test is claimed."]
    lines+=['',f"Rankings match the original run on {sum(r['same_ranking_as_original'] for r in rows)}/240 requests, and decoded answers match on {sum(r['same_answer_as_original'] for r in rows)}/240 requests. Model revisions, thresholds, CPU thread count, prompt and generation budget remain fixed. The generator's recorded dtype is bfloat16 on CPU. The workstation was not isolated from other activity; the benchmark quantifies this session, not guaranteed production latency.",
            '', 'Median and p95 intervals and all six pairwise comparisons are retained in the supplementary statistical output. The p95 is sensitive to a few observations and only one request was timed per query/method.']
    text='\n'.join(lines)+'\n';(out/'end_to_end/report.md').write_text(text)
    (out/'experiment_report.md').write_text('# Final validation report\n\n'+text+'\nIndependent semantic correctness and faithfulness: pending (no human raters). Automated strict exact match and qualitative evidence cases remain in the original report and routing analysis. No hallucination-reduction claim.\n')
    paper=Path('paper/draft.md');s=paper.read_text();start='<!-- DIRECT_BENCHMARK_START -->';end='<!-- DIRECT_BENCHMARK_END -->'
    if start in s:s=s[:s.index(start)]+start+'\n'+text+end+s[s.index(end)+len(end):]
    else:s=s.replace('## 6. Discussion',start+'\n'+text+end+'\n\n## 6. Discussion')
    s=s.replace('Generation dominates runtime, and estimated request latency does not improve.','Direct request latency is measured separately from retrieval, with session-specific uncertainty.')
    s=s.replace('direct full-request wall timing and electricity/hardware monetary cost have not been measured.','direct full-request timing is reported below; electricity/hardware monetary cost remains unmeasured.')
    paper.write_text(s)
    update='''\n### Validation continuation — task 1 and direct task 3 complete\n\nThe integrated benchmark completed all 240 paired requests. Each elapsed duration is one perf_counter interval from before query encoding through final decoded answer; it includes router, retrieval, reranking, evidence assembly, tokenization and generation. Warmup uses a development query; loading/index setup is separate. Balanced method positions and frozen model/prompt/router settings are saved in `results/e2e_01/config.json`. Mean, median, p95 and article-cluster bootstrap intervals, plus all six pairwise quality/latency comparisons, are in `results/validation_02/end_to_end/`. No significance/equivalence claim. Original held-out artifacts remain byte-identical.\n\n'''+text+'\nNext: independent human annotation remains unavailable. Finish final manuscript render/visual checks and retain missing affiliation/advisor/submission materials as pending.\n'
    progress=Path('progress.md');progress.write_text(progress.read_text()+update)
    (out/'completion.json').write_text(json.dumps({'direct_requests':240,'original_files_unchanged':True,'ranking_parity':sum(r['same_ranking_as_original'] for r in rows),'answer_parity':sum(r['same_answer_as_original'] for r in rows),'human_evaluation':'pending; raters unavailable'},indent=2))

if __name__=='__main__':main()
