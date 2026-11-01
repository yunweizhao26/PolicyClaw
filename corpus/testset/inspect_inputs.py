import json, os, time
from pathlib import Path
import pyarrow.parquet as pq
root = Path(__file__).resolve().parents[2]
assert os.environ.get('SLURM_JOB_ID'), 'Compute allocation required'
for relative in ['corpus/stores/data_full/android/meta', 'corpus/stores/data_full/apple/meta', 'corpus/stores/data_full/apple/links', 'corpus/stores/data/apple/links', 'corpus/stores/data_full/shared/policies', 'corpus/stores/data/shared/policies', 'corpus/classify/final/web.parquet', '../Contextual-Integrity/ci_policy/data/policy_corpus/privaseer']:
    folder = root / relative
    paths = [folder] if folder.is_file() else sorted(folder.glob('*.parquet'))
    paths = [p for p in paths if time.time() - p.stat().st_mtime >= 120]
    print(relative, 'stable_files', len(paths), flush=True)
    if not paths: continue
    pf = pq.ParquetFile(paths[0]); print(pf.schema_arrow, flush=True)
    row = next(pf.iter_batches(batch_size=1)).to_pylist()[0]
    print({k: (str(v)[:600] if k not in ('body', 'page_html', 'text') else f'{len(v or "")} chars/bytes') for k,v in row.items()}, flush=True)
