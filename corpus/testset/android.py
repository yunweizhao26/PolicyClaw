from collections import Counter
import json
from multiprocessing import Pool
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from base import OUT, ROOT, Domains, load_exclusions, require_compute, snapshot, unchanged, write_json, write_table

FIELDS = ('title developer developerId developerWebsite developerEmail developerAddress realInstalls '
          'minInstalls installs ratings score genre released updated privacyPolicy containsAds').split()
INTEGER = {'realInstalls', 'minInstalls', 'ratings', 'updated'}
SCHEMA = pa.schema([('app_id', pa.string()), ('metadata_fetched_at', pa.string()), ('source_shard', pa.string()),
                    ('parse_errors', pa.string())] +
                   [(f, pa.int64() if f in INTEGER else pa.float64() if f == 'score' else
                     pa.bool_() if f == 'containsAds' else pa.string()) for f in FIELDS])


def decode_details(raw):
    from google_play_scraper.constants.element import ElementSpecs
    from google_play_scraper.constants.regex import Regex
    wanted = {f'ds:{ElementSpecs.Detail[f].ds_num}' for f in FIELDS}
    dataset, errors = {}, []
    for arg in raw or []:
        key = Regex.KEY.findall(arg)
        if not key or key[0] not in wanted:
            continue
        val = Regex.VALUE.findall('AF_initDataCallback(' + arg + ');</script')
        if val:
            try:
                dataset[key[0]] = json.loads(val[0])
            except (ValueError, TypeError) as e:
                errors.append(f'{key[0]}:{type(e).__name__}')
    out = {}
    for field in FIELDS:
        try:
            value = ElementSpecs.Detail[field].extract_content(dataset)
            if value is not None:
                if field in INTEGER:
                    value = int(value)
                elif field == 'score':
                    value = float(value)
                elif field == 'containsAds':
                    value = bool(value)
                else:
                    value = str(value)
            out[field] = value
        except Exception as e:
            errors.append(f'{field}:{type(e).__name__}')
            out[field] = None
    out['parse_errors'] = json.dumps(errors) if errors else None
    return out


def parse_shard(entry):
    folder = OUT / 'parsed/android'
    dest = folder / Path(entry['path']).name
    stat_path = dest.with_suffix('.json')
    if dest.exists() and stat_path.exists():
        return json.loads(stat_path.read_text())
    counts, rows = Counter(), []
    try:
        unchanged(entry)
        pf = pq.ParquetFile(entry['path'])
        cols = ['app_id', 'kind', 'storefront', 'http_status', 'fetched_at', 'data_raw']
        for batch in pf.iter_batches(batch_size=32, columns=cols, use_threads=False):
            counts['raw_rows'] += len(batch)
            mask = pc.and_(pc.and_(pc.equal(batch['kind'], 'details'), pc.equal(batch['storefront'], 'US')),
                           pc.equal(batch['http_status'], 200))
            for row in batch.filter(mask).to_pylist():
                counts['us_details_200_rows'] += 1
                parsed = decode_details(row['data_raw'])
                counts['rows_with_parse_errors'] += bool(parsed['parse_errors'])
                rows.append(dict(app_id=row['app_id'], metadata_fetched_at=row['fetched_at'],
                                 source_shard=entry['path'], **parsed))
        unchanged(entry)
        write_table(dest, rows, SCHEMA)
        result = dict(source=entry['path'], counts=dict(counts), output=str(dest))
    except Exception as e:
        result = dict(source=entry['path'], skipped=f'{type(e).__name__}:{e}')
    write_json(stat_path, result)
    return result


def main():
    require_compute()
    (OUT/'parsed/android').mkdir(parents=True, exist_ok=True)
    snap = snapshot('android_meta', [ROOT/'corpus/stores/data_full/android/meta'])
    stats, results = Counter(), []
    with Pool(12, maxtasksperchild=20) as pool:
        for i, result in enumerate(pool.imap_unordered(parse_shard, snap['files'], chunksize=1), 1):
            results.append(result)
            stats.update(result.get('counts', {}))
            if i % 100 == 0:
                print(f'Android shards {i}/{len(snap["files"])}; parsed {stats["us_details_200_rows"]}', flush=True)
    paths = sorted(r['output'] for r in results if r.get('output'))
    if not paths:
        raise RuntimeError('No Android shards parsed')
    df = pd.concat([pq.read_table(p).to_pandas() for p in paths], ignore_index=True)
    df = df.sort_values(['metadata_fetched_at', 'source_shard'], ascending=[False, False], kind='stable')
    df = df.drop_duplicates('app_id', keep='first')
    write_table(OUT/'apps_android.parquet', pa.Table.from_pandas(df, preserve_index=False, schema=SCHEMA))
    stats['unique_us_apps'] = len(df)
    linked = df[df.privacyPolicy.fillna('').str.strip().ne('')].copy()
    stats['unique_apps_with_policy_url'] = len(linked)
    linked = linked.sort_values(['realInstalls', 'minInstalls', 'ratings', 'app_id'],
                                ascending=[False, False, False, True], na_position='last', kind='stable')
    invalid = linked[linked.developerId.fillna('').eq('')]
    stats['apps_missing_developerId'] = len(invalid)
    linked = linked[linked.developerId.fillna('').ne('')].drop_duplicates('developerId', keep='first')
    domains, excluded = Domains(), load_exclusions()
    rows, rejected = [], []
    for frame_rank, r in enumerate(pa.Table.from_pandas(linked, preserve_index=False, schema=SCHEMA).to_pylist(), 1):
        row = dict(r, arm='android', frame_rank=frame_rank, organization_key=r['developerId'],
                   organization_name=r['developer'], size_proxy=r['realInstalls'], size_proxy_name='realInstalls',
                   app_title=r['title'], app_genre=r['genre'], policy_url=r['privacyPolicy'].strip())
        row['policy_registered_domain'] = domains.registered(row['policy_url'])
        if row['policy_registered_domain'] in excluded:
            rejected.append(dict(row, stage='frame', reason='development_domain'))
        else:
            rows.append(dict(row, rank=len(rows)+1, candidate_id=f'android-c{len(rows)+1:07d}'))
    write_table(OUT/'candidates_android.parquet', rows)
    write_table(OUT/'frame_rejected_android.parquet', rejected)
    stats.update(organizations_before_exclusions=len(linked), excluded_organizations=len(rejected), candidates=len(rows))
    write_json(OUT/'frame_android.json', dict(counts=dict(stats), shards=len(snap['files']),
               skipped=snap['skipped']+[r for r in results if r.get('skipped')]))
    print(dict(stats), flush=True)


if __name__ == '__main__':
    main()
