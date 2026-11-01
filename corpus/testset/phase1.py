import json
from pathlib import Path
import subprocess
import sys

import pyarrow.parquet as pq

from base import ARMS, OUT, PYTHON, require_compute, write_json


def run(step, script, *args):
    subprocess.run([PYTHON, '-B', str(OUT/'measure.py'), step, PYTHON, '-B', str(OUT/script), *map(str,args)], check=True)


def main():
    require_compute()
    write_json(OUT/'run_status.json', dict(status='running'))
    run('selfcheck', 'selfcheck.py')
    for arm in ARMS:
        if not (OUT/f'candidates_{arm}.parquet').exists():
            raise RuntimeError(f'Missing {arm} frame; run the frame jobs first')
    run('apple_link_priority', 'align_apple_links.py')
    run('reuse_index', 'fetch_candidates.py', 'index')
    folder = OUT/'plans'; folder.mkdir(exist_ok=True)
    sizes = {a:pq.ParquetFile(OUT/f'candidates_{a}.parquet').metadata.num_rows for a in ARMS}
    paths = sorted(folder.glob('batch-*.json'))
    active = {a:0 for a in ARMS}
    if not paths:
        path = folder/'batch-0001.json'; write_json(path, {a:min(400,sizes[a]) for a in ARMS}); paths=[path]
    index = 0
    while index < len(paths):
        path = paths[index]; plan=json.loads(path.read_text())
        active.update(plan); write_json(OUT/'active_plan.json', active)
        run(path.stem+'_fetch_text', 'fetch_candidates.py', path)
        run(path.stem+'_verify', 'verify_candidates.py', path)
        run(path.stem+'_select', 'select_candidates.py')
        state = json.loads((OUT/'selection_state.json').read_text())
        if state['complete']:
            run('audit', 'audit.py')
            write_json(OUT/'run_status.json', dict(status='complete'))
            return
        if not state['blocked']:
            raise RuntimeError('Candidate frame exhausted before reaching 200 per arm')
        if state['blocked']['reason'] not in ('not_fetched', 'outside_prepared_batch'):
            raise RuntimeError('Unresolved verification blocks the next ranked turn')
        index += 1
        if index < len(paths): continue
        arm = state['blocked']['arm']
        end = min(active[arm]+400, sizes[arm])
        if end <= active[arm]: raise RuntimeError(f'{arm} frame exhausted')
        path = folder/f'batch-{index+1:04d}.json'; write_json(path, {arm:end}); paths.append(path)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        write_json(OUT/'failure.json', dict(error=f'{type(e).__name__}: {e}'))
        write_json(OUT/'run_status.json', dict(status='failed', error=f'{type(e).__name__}: {e}'))
        raise
