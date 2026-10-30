"""Finalize a complete active benchmark; no experiment reruns or partial analyses."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

os.chdir(Path(__file__).resolve().parents[1])
status=Path('results/validation_02/status.json')
def record(state,**detail):status.write_text(json.dumps(dict(state=state,**detail),indent=2))
env=os.environ.copy();env.pop('PYTHONPATH',None);env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
try:
    for _ in range(600):
        s=json.loads(Path('results/e2e_01/status.json').read_text());record('waiting_for_direct_benchmark',benchmark=s)
        if s['state']=='complete':break
        os.kill(int(sys.argv[1]),0)
        time.sleep(30)
    else:raise TimeoutError('Benchmark not completed within watcher limit')
    record('analyzing_complete_benchmark')
    subprocess.run([sys.executable,'-m','experiments.finalize_validation'],check=True,env=env)
    python='/home/panu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python'
    subprocess.run([python,'paper/build_manuscript.py'],check=True)
    subprocess.run([python,'paper/qa/render_with_system_lo.py','paper/aucc2027_manuscript.docx','--output_dir','paper/qa/manuscript_final','--emit_pdf'],check=True,env=dict(env,PATH='/usr/bin:/bin'))
    record('awaiting_final_visual_inspection',human_evaluation='pending independent raters')
except Exception as e:
    record('failed',error=str(e));raise
