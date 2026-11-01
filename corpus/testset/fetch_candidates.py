from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import fcntl
from pathlib import Path
import sqlite3
import sys
import threading
import time

import pyarrow as pa
import pyarrow.parquet as pq

from base import ARMS, OUT, ROOT, hostname, now, require_compute, sha, snapshot, unchanged, write_json, write_table
import common as C
import text as T
from corpus.rebuild_versions import visible_text

FETCH_SCHEMA = pa.schema([(k, pa.string()) for k in
    ('candidate_id', 'arm', 'policy_url', 'final_url', 'fetched_at', 'content_type', 'headers', 'redirect_chain',
     'error', 'body_sha256', 'reused_from', 'visible_text', 'trafilatura_text', 'visible_sha256',
     'trafilatura_sha256', 'extractor', 'extractor_settings', 'extraction_error')] +
    [(k, pa.int64()) for k in ('http_status', 'body_bytes', 'visible_chars', 'trafilatura_chars', 'attempts', 'elapsed_ms')] +
    [('body', pa.binary())])


def candidates(arm, max_rank=None):
    path = OUT/f'candidates_{arm}.parquet'
    columns = [c for c in pq.ParquetFile(path).schema_arrow.names if c != 'privaseer_text']
    filters = [('rank', '<=', max_rank)] if max_rank is not None else None
    return sorted(pq.read_table(path, columns=columns, filters=filters).to_pylist(), key=lambda r:r['rank'])


def index_reuse():
    path = OUT/'reuse.sqlite'
    if (OUT/'reuse_index.json').exists(): return
    snap = snapshot('stored_policies', [ROOT/'corpus/stores/data/shared/policies', ROOT/'corpus/stores/data_full/shared/policies'])
    db = sqlite3.connect(path)
    db.execute('PRAGMA journal_mode=WAL')
    db.execute('PRAGMA cache_size=-131072')
    db.execute('CREATE TABLE IF NOT EXISTS policies '
               '(url TEXT PRIMARY KEY, fetched_at TEXT, status INTEGER, file TEXT, rg INTEGER, offset INTEGER)')
    db.execute('CREATE TABLE IF NOT EXISTS files (path TEXT PRIMARY KEY, count INTEGER)')
    counts, skipped = Counter(), []
    for i, entry in enumerate(snap['files'], 1):
        if db.execute('SELECT 1 FROM files WHERE path=?', (entry['path'],)).fetchone(): continue
        try:
            unchanged(entry)
            pf = pq.ParquetFile(entry['path'])
            n = 0
            for rg in range(pf.num_row_groups):
                table = pf.read_row_group(rg, columns=['policy_url', 'fetched_at', 'http_status'])
                values = [(r['policy_url'], r['fetched_at'] or '', r['http_status'], entry['path'], rg, offset)
                          for offset, r in enumerate(table.to_pylist())]
                n += len(values)
                db.executemany('INSERT INTO policies VALUES (?,?,?,?,?,?) ON CONFLICT(url) DO UPDATE SET '
                    'fetched_at=excluded.fetched_at,status=excluded.status,file=excluded.file,rg=excluded.rg,offset=excluded.offset '
                    'WHERE excluded.fetched_at >= policies.fetched_at', values)
            unchanged(entry)
            db.execute('INSERT INTO files VALUES (?,?)', (entry['path'], n)); db.commit()
        except Exception as e:
            db.rollback()
            skipped.append(dict(path=entry['path'], reason=f'{type(e).__name__}:{e}'))
        if i % 50 == 0: print(f'Policy index shards {i}/{len(snap["files"])}', flush=True)
    counts['stored_rows'] = db.execute('SELECT coalesce(sum(count),0) FROM files').fetchone()[0]
    counts['indexed_files'] = db.execute('SELECT count(*) FROM files').fetchone()[0]
    counts['latest_urls'] = db.execute('SELECT count(*) FROM policies').fetchone()[0]
    counts['latest_urls_2xx'] = db.execute('SELECT count(*) FROM policies WHERE status>=200 AND status<300').fetchone()[0]
    db.close()
    write_json(OUT/'reuse_index.json', dict(counts=dict(counts), skipped=snap['skipped']+skipped))


_LOCK = threading.Lock()
_HOSTS = {}


def limited_once(original):
    def wrapped(url, *args, **kwargs):
        host = hostname(url)
        with _LOCK:
            lock, state = _HOSTS.setdefault(host, (threading.Lock(), {'last': 0.0}))
        with lock:
            delay = state['last'] + 1.0 - time.monotonic()
            if delay > 0: time.sleep(delay)
            state['last'] = time.monotonic()
            return original(url, *args, **kwargs)
    return wrapped


def extract(row):
    body = row['body'] or b''
    derived = T.work((row['policy_url'], row['content_type'], row['http_status'], body))
    trafi = derived['text'] or ''
    visible = ''
    if row['http_status'] is not None and 200 <= row['http_status'] < 300:
        kind = T.kind_of(row['content_type'], body)
        if kind == 'html': visible = visible_text(body)
        elif kind in ('pdf', 'plain'): visible = trafi
    visible = T.clean(visible)
    return dict(row, visible_text=visible, trafilatura_text=trafi, visible_sha256=sha(visible),
        trafilatura_sha256=sha(trafi), visible_chars=len(visible), trafilatura_chars=len(trafi),
        extractor=derived['extractor'], extractor_settings=derived['settings'], extraction_error=derived['skipped_reason'])


def fetch_one(candidate, source_manifest):
    dest = OUT/'fetch'/f'{candidate["candidate_id"]}.parquet'
    if dest.exists():
        return dict(candidate_id=candidate['candidate_id'], resumed=True)
    url, source, row = candidate['policy_url'], None, None
    if candidate['arm'] != 'web':
        with sqlite3.connect(f'file:{OUT / "reuse.sqlite"}?mode=ro', uri=True) as db:
            source = db.execute('SELECT fetched_at,status,file,rg,offset FROM policies WHERE url=?', (url,)).fetchone()
        if source and source[1] is not None and 200 <= source[1] < 300 and source[0].startswith('2026-10-'):
            try:
                unchanged(source_manifest[source[2]])
                row = pq.ParquetFile(source[2]).read_row_group(source[3]).slice(source[4], 1).to_pylist()[0]
                unchanged(source_manifest[source[2]])
                assert row['policy_url'] == url
                row['reused_from'] = f'{source[2]}:row_group={source[3]}:row={source[4]}'
            except Exception:
                row = None
    if row is None:
        response = C.fetch(url, timeout=20, max_attempts=4, max_bytes=20_000_000, deadline_s=120)
        row = dict(policy_url=url, final_url=response['final_url'], fetched_at=now(),
                   http_status=response['status'], content_type=response['content_type'],
                   headers=json.dumps(response['headers']), redirect_chain=json.dumps(response['history']),
                   body=response['content'], error=response['error'], attempts=response['attempts'],
                   elapsed_ms=response['elapsed_ms'], reused_from=None)
    row.update(candidate_id=candidate['candidate_id'], arm=candidate['arm'],
               body_sha256=sha(row['body'] or b''), body_bytes=len(row['body'] or b''))
    row = extract(row)
    write_table(dest, [row], FETCH_SCHEMA)
    textpath = OUT/'fetch/texts'/f'{candidate["candidate_id"]}.visible.txt'
    textpath.parent.mkdir(exist_ok=True)
    textpath.write_text(row['visible_text'], encoding='utf-8')
    return dict(candidate_id=candidate['candidate_id'], reused=bool(row['reused_from']),
                status=row['http_status'], visible_chars=row['visible_chars'])


def main():
    require_compute()
    if sys.argv[1] == 'index':
        index_reuse(); return
    plan = json.loads(Path(sys.argv[1]).read_text())
    folder = OUT/'fetch'
    folder.mkdir(exist_ok=True)
    (folder/'texts').mkdir(exist_ok=True)
    manifest = {e['path']: e for e in json.loads((OUT/'snapshots/stored_policies.json').read_text())['files']}
    todo = []
    for arm, end_rank in plan.items():
        todo.extend(c for c in candidates(arm, end_rank) if c['rank'] <= end_rank
                    and not (folder/f'{c["candidate_id"]}.parquet').exists())
    C._once = limited_once(C._once)
    C.set_limiter(4, 4, 4)
    results = []
    with ThreadPoolExecutor(8) as pool:
        futures = [pool.submit(fetch_one, c, manifest) for c in todo]
        for i, future in enumerate(as_completed(futures), 1):
            results.append(future.result())
            if i % 25 == 0: print(f'Policy fetch/text {i}/{len(todo)}', flush=True)
    write_json(OUT/'fetch'/f'{Path(sys.argv[1]).stem}-summary.json',
               dict(results=results, http_attempts=dict(C.ATTEMPTS), host_limit='one active original-host request; at least 1 second between attempts',
                    global_request_attempts_per_second=4, workers=8))


if __name__ == '__main__':
    with (OUT/'.fetch.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        main()
