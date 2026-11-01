from collections import Counter, defaultdict
from functools import lru_cache
import json
from pathlib import Path
import sqlite3

import pyarrow as pa
import pyarrow.parquet as pq

from base import OUT, ROOT, Domains, load_exclusions, require_compute, snapshot, unchanged, write_json, write_table
from exclusions import exclusion_sources, exclusion_reason

PRIVASEER = ROOT.parent/'Contextual-Integrity/ci_policy/data/policy_corpus/privaseer'
SCHEMA = pa.schema([
    ('arm', pa.string()), ('rank', pa.int64()), ('frame_rank', pa.int64()), ('candidate_id', pa.string()),
    ('organization_key', pa.string()), ('organization_name', pa.string()), ('size_proxy', pa.int64()),
    ('size_proxy_name', pa.string()), ('web_domain', pa.string()), ('policy_url', pa.string()),
    ('policy_registered_domain', pa.string()), ('privaseer_url', pa.string()), ('privaseer_policy_id', pa.string()),
    ('industry', pa.string()), ('year', pa.string()), ('privaseer_timestamp', pa.string()),
    ('fasttext_score', pa.float64()), ('fasttext_page_id', pa.string()), ('source_shard', pa.string()),
    ('source_row', pa.int64()), ('privaseer_text', pa.large_string())])


def main():
    require_compute()
    domains, excluded, counts = Domains(), load_exclusions(), Counter()
    sources = exclusion_sources()
    registered = lru_cache(maxsize=500000)(domains.registered)
    score_snap = snapshot('web_scores', [ROOT/'corpus/classify/final/web.parquet'])
    scores = {}
    for entry in score_snap['files']:
        unchanged(entry)
        for batch in pq.ParquetFile(entry['path']).iter_batches(columns=['url', 'score', 'page_id'], batch_size=20000):
            for row in batch.to_pylist():
                counts['classifier_rows'] += 1
                score = row['score']
                if score is None or score != score:
                    continue
                old = scores.get(row['url'])
                if old is None or score > old[0]:
                    scores[row['url']] = (float(score), str(row['page_id']))
        unchanged(entry)
    counts['classifier_unique_urls'] = len(scores)
    snap = snapshot('privaseer', [PRIVASEER])
    dbpath = OUT/'parsed/web_urls_psl_v2.sqlite'
    dbpath.parent.mkdir(exist_ok=True)
    db = sqlite3.connect(dbpath)
    db.execute('PRAGMA journal_mode=WAL')
    db.execute('PRAGMA cache_size=-262144')
    db.execute('CREATE TABLE IF NOT EXISTS urls (url TEXT PRIMARY KEY, timestamp TEXT, domain TEXT, metadata TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS shards (path TEXT PRIMARY KEY, counts TEXT)')
    for i, entry in enumerate(snap['files'], 1):
        done = db.execute('SELECT counts FROM shards WHERE path=?', (entry['path'],)).fetchone()
        if done:
            counts.update(json.loads(done[0])); continue
        local, data, offset = Counter(), [], 0
        unchanged(entry)
        pf = pq.ParquetFile(entry['path'])
        for batch in pf.iter_batches(columns=['policy_id', 'url', 'timestamp', 'industry', 'year'], batch_size=10000):
            for j, row in enumerate(batch.to_pylist()):
                local['privaseer_rows'] += 1
                domain = registered(row['url'])
                if domain not in domains.ranks:
                    local['rows_without_tranco_domain'] += 1; continue
                local['rows_with_tranco_domain'] += 1
                metadata = dict(policy_url=row['url'], web_domain=domain,
                    privaseer_policy_id=row['policy_id'], industry=row['industry'], year=row['year'],
                    privaseer_timestamp=row['timestamp'] or '', source_shard=entry['path'], source_row=offset+j)
                data.append((row['url'], row['timestamp'] or '', domain, json.dumps(metadata)))
            offset += len(batch)
            db.executemany('INSERT INTO urls VALUES (?,?,?,?) ON CONFLICT(url) DO UPDATE SET '
                'timestamp=excluded.timestamp,domain=excluded.domain,metadata=excluded.metadata '
                'WHERE excluded.timestamp >= urls.timestamp', data)
            data = []
        unchanged(entry)
        db.execute('INSERT INTO shards VALUES (?,?)', (entry['path'], json.dumps(dict(local))))
        db.commit(); counts.update(local)
        if i % 20 == 0: print(f'PrivaSeer shards {i}/{len(snap["files"])}', flush=True)
    counts['latest_urls_with_tranco_domain'] = db.execute('SELECT count(*) FROM urls').fetchone()[0]
    best = {}
    for url, metadata in db.execute('SELECT url,metadata FROM urls'):
        if url not in scores:
            counts['latest_urls_without_fasttext_score'] += 1
        else:
            counts['latest_urls_with_fasttext_score'] += 1
        row = json.loads(metadata)
        row['fasttext_score'], row['fasttext_page_id'] = scores.get(url, (None, None))
        domain = row['web_domain']
        old = best.get(domain)
        key = (row['fasttext_score'] if row['fasttext_score'] is not None else float('-inf'), row['privaseer_timestamp'], -len(url))
        old_key = (old['fasttext_score'] if old['fasttext_score'] is not None else float('-inf'), old['privaseer_timestamp'], -len(old['policy_url'])) if old else None
        if old is None or key > old_key or (key == old_key and url < old['policy_url']):
            best[domain] = row
    db.close()
    rows, rejected = [], []
    for frame_rank, domain in enumerate(sorted(best, key=domains.ranks.__getitem__), 1):
        row = dict(best[domain], arm='web', frame_rank=frame_rank, organization_key=domain,
                   organization_name=domain, size_proxy=domains.ranks[domain], size_proxy_name='Tranco rank',
                   policy_registered_domain=None)
        row['privaseer_url'] = row.pop('policy_url')
        row['policy_url'] = None
        if domain in excluded:
            rejected.append(dict(row, stage='frame', reason=exclusion_reason([domain], sources)))
        else:
            rows.append(dict(row, rank=len(rows)+1, candidate_id=f'web-v2-c{len(rows)+1:07d}'))
    by_file = defaultdict(dict)
    for row in rows: by_file[row['source_shard']][row['source_row']] = row
    dest = OUT/'candidates_web.parquet'
    tmp = dest.with_suffix('.parquet.tmp')
    with pq.ParquetWriter(tmp, SCHEMA, compression='zstd') as writer:
        for i, (source, wanted) in enumerate(sorted(by_file.items()), 1):
            entry = next(e for e in snap['files'] if e['path'] == source)
            unchanged(entry)
            pf, offset = pq.ParquetFile(source), 0
            for group in range(pf.num_row_groups):
                n = pf.metadata.row_group(group).num_rows
                indexes = sorted(k for k in wanted if offset <= k < offset+n)
                if indexes:
                    texts = pf.read_row_group(group, columns=['text']).take([k-offset for k in indexes]).to_pylist()
                    chunk = [dict(wanted[k], privaseer_text=t['text']) for k,t in zip(indexes, texts)]
                    writer.write_table(pa.Table.from_pylist(chunk, schema=SCHEMA))
                offset += n
            unchanged(entry)
            if i % 50 == 0: print(f'PrivaSeer text metadata {i}/{len(by_file)}', flush=True)
    tmp.replace(dest)
    write_table(OUT/'frame_rejected_web.parquet', rejected)
    counts.update(organizations_before_exclusions=len(best), excluded_organizations=len(rejected), candidates=len(rows))
    write_json(OUT/'frame_web.json', dict(counts=dict(counts), shards=len(snap['files']), skipped=snap['skipped'],
        score_rule='Metadata only: maximum available score per URL; latest crawl per URL, then max score per PSL domain, latest timestamp, shortest URL, lexical URL. Missing scores do not exclude domains.',
        policy_url_method='First eligible privacy link among the first three on the final current homepage',
        psl_sha256=json.loads((OUT/'psl/manifest.json').read_text())['sha256']))
    print(dict(counts), flush=True)


if __name__ == '__main__':
    main()
