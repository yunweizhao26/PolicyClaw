from collections import Counter
import json
from pathlib import Path
import os

import pyarrow.parquet as pq

OUT=Path(__file__).resolve().parent
assert os.environ.get('SLURM_JOB_ID')
for name in ('android','web','apple'):
    path=OUT/f'frame_{name}.json'
    if path.exists(): print('frame',name,json.loads(path.read_text())['counts'])
paths=sorted((OUT/'apple_pages').glob('*.parquet'))
print('apple_recovered_pages',len(paths))
print('fetched_candidates',len(list((OUT/'fetch').glob('*.parquet'))))
if (OUT/'verify.jsonl').exists():
    records=[json.loads(s) for s in (OUT/'verify.jsonl').read_text().splitlines()]
    print('verified_records',len(records),dict(Counter(r.get('label','error') for r in records)))
for path in sorted((OUT/'verify_batches').glob('*.jsonl')):
    print('verification_batch',path.name,len(path.read_text().splitlines()))
for name in ('selection_state.json','failure.json'):
    path=OUT/name
    if path.exists(): print(name,json.loads(path.read_text()))
