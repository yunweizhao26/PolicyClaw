from collections import Counter
import json
from multiprocessing import Pool
from pathlib import Path
from urllib.parse import urlsplit

import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from base import OUT, ROOT, Domains, load_exclusions, require_compute, snapshot, unchanged, write_json, write_table
import common as C
import links as L
import meta as M

FIELDS = ('trackId trackName artistId artistName sellerName sellerUrl userRatingCount averageUserRating '
          'primaryGenreName releaseDate currentVersionReleaseDate languageCodesISO2A').split()
APP_SCHEMA = pa.schema([('app_id', pa.string()), ('metadata_fetched_at', pa.string()), ('source_shard', pa.string())] +
    [(f, pa.int64() if f == 'userRatingCount' else pa.float64() if f == 'averageUserRating' else
      pa.list_(pa.string()) if f == 'languageCodesISO2A' else pa.string()) for f in FIELDS])
PAGE_SCHEMA = pa.schema([(k, pa.string()) for k in ('app_id', 'page_fetched_at', 'source_shard', 'policy_url', 'parse_error')]
                       + [('page_http_status', pa.int32())])


def is_us_row(row):
    if row.get('storefront') is not None:
        return row['storefront'] == 'US'
    return any(urlsplit(row.get(k) or '').hostname == 'apps.apple.com'
               and urlsplit(row.get(k) or '').path.startswith('/us/') for k in ('request_url', 'final_url'))


def page_index(row, source):
    url, error = None, None
    if row['http_status'] == 200 and row.get('data_raw'):
        try:
            found = L.apple_policy_links(row['data_raw'])
            url = found[0][0].strip() if found else None
        except Exception as e:
            error = f'{type(e).__name__}:{e}'
    return dict(app_id=row['app_id'], page_fetched_at=row['fetched_at'], page_http_status=row['http_status'],
                source_shard=source, policy_url=url, parse_error=error)


def parse_shard(entry):
    folder = OUT/'parsed/apple'
    prefix = ('pilot-' if '/data/' in entry['path'] else 'full-') + Path(entry['path']).stem
    stat_path = folder/f'{prefix}.json'
    if stat_path.exists():
        previous = json.loads(stat_path.read_text())
        if 'storefront' not in previous.get('skipped', ''):
            return previous
    apps, pages, counts = [], [], Counter()
    try:
        unchanged(entry)
        pf = pq.ParquetFile(entry['path'])
        has_storefront = 'storefront' in pf.schema_arrow.names
        cols = ['app_id', 'kind', 'http_status', 'fetched_at', 'data_raw']
        cols += ['storefront'] if has_storefront else [c for c in ('request_url', 'final_url') if c in pf.schema_arrow.names]
        for batch in pf.iter_batches(batch_size=128, columns=cols, use_threads=False):
            counts['raw_rows'] += len(batch)
            filtered = batch.filter(pc.equal(batch['storefront'], 'US')) if has_storefront else batch
            for row in filtered.to_pylist():
                if not has_storefront and not is_us_row(row):
                    continue
                if row['kind'] == 'app_page':
                    pages.append(page_index(row, entry['path']))
                    counts['us_app_page_rows'] += 1
                elif row['kind'] == 'lookup' and '/data_full/' in entry['path']:
                    counts['us_lookup_rows'] += 1
                    if not row['data_raw']:
                        counts['us_lookup_without_payload'] += 1
                        continue
                    try:
                        raw = json.loads(row['data_raw'])
                        records = raw['results'] if 'results' in raw else [raw]
                        for record in records:
                            if not record.get('trackId'):
                                continue
                            parsed = {}
                            for field in FIELDS:
                                value = record.get(field)
                                if value is not None:
                                    if field == 'userRatingCount': value = int(value)
                                    elif field == 'averageUserRating': value = float(value)
                                    elif field == 'languageCodesISO2A': value = list(map(str, value))
                                    else: value = str(value)
                                parsed[field] = value
                            apps.append(dict(app_id=str(record['trackId']), metadata_fetched_at=row['fetched_at'],
                                             source_shard=entry['path'], **parsed))
                            counts['us_lookup_app_records'] += 1
                    except Exception as e:
                        counts[f'lookup_parse_error:{type(e).__name__}'] += 1
        unchanged(entry)
        app_path, page_path = folder/f'{prefix}-apps.parquet', folder/f'{prefix}-pages.parquet'
        write_table(app_path, apps, APP_SCHEMA)
        write_table(page_path, pages, PAGE_SCHEMA)
        result = dict(source=entry['path'], counts=dict(counts), apps=str(app_path), pages=str(page_path))
    except Exception as e:
        result = dict(source=entry['path'], skipped=f'{type(e).__name__}:{e}')
    write_json(stat_path, result)
    return result


def main():
    require_compute()
    (OUT/'parsed/apple').mkdir(parents=True, exist_ok=True)
    snap = snapshot('apple_meta', [ROOT/'corpus/stores/data_full/apple/meta', ROOT/'corpus/stores/data/apple/meta'])
    stats, results = Counter(), []
    with Pool(8, maxtasksperchild=30) as pool:
        for i, result in enumerate(pool.imap_unordered(parse_shard, snap['files']), 1):
            results.append(result)
            stats.update(result.get('counts', {}))
            if i % 50 == 0:
                print(f'Apple shards {i}/{len(snap["files"])}', flush=True)
    df = pd.concat([pq.read_table(r['apps']).to_pandas() for r in results if 'apps' in r], ignore_index=True)
    df = df.sort_values(['metadata_fetched_at', 'source_shard'], ascending=[False, False], kind='stable')
    df = df.drop_duplicates('app_id').sort_values(['userRatingCount', 'app_id'], ascending=[False, True],
                                                 na_position='last', kind='stable')
    stats['unique_us_lookup_apps'] = len(df)
    pages = {}
    for result in sorted(results, key=lambda r:r['source']):
        if 'pages' not in result: continue
        for row in pq.read_table(result['pages']).to_pylist():
            old = pages.get(row['app_id'])
            if old is None or (row['page_fetched_at'] or '') >= (old['page_fetched_at'] or ''):
                pages[row['app_id']] = row
    link_snap = snapshot('apple_links', [ROOT/'corpus/stores/data/apple/links', ROOT/'corpus/stores/data_full/apple/links'])
    link_map = {}
    for entry in link_snap['files']:
        try:
            unchanged(entry)
            for row in pq.read_table(entry['path'], columns=['app_id', 'policy_url']).to_pylist():
                link_map[row['app_id']] = row['policy_url']
        except Exception as e:
            stats[f'links_skipped:{type(e).__name__}'] += 1
    folder = OUT/'apple_pages'
    folder.mkdir(exist_ok=True)
    top = df.head(3000).app_id.tolist()
    missing = [app for app in top if app not in pages]
    stats['top3000_apps'] = len(top)
    stats['top3000_without_us_app_page_at_snapshot'] = len(missing)
    C.set_limiter(1.0, 1.0, 1.0)
    for i, app in enumerate(missing, 1):
        dest = folder/f'part-{app}.parquet'
        if dest.exists():
            raw_row = pq.read_table(dest).to_pylist()[0]
        else:
            raw_row = M.fetch_page((app, 'app_page', 'US'), 'apple', 'full')[0]
            write_table(dest, [raw_row], M.schema_for('apple'))
        pages[app] = page_index(raw_row, str(dest))
        stats['recovery_http_'+str(raw_row['http_status'])] += 1
        if i % 25 == 0:
            print(f'Apple missing app pages {i}/{len(missing)}', flush=True)
    C.LIMITER = None
    write_table(OUT/'apple_page_index.parquet', list(pages.values()), PAGE_SCHEMA)
    df['has_us_app_page'] = df.app_id.map(lambda app: app in pages)
    df['policy_url'] = df.app_id.map(lambda app: pages.get(app, {}).get('policy_url'))
    df['links_table_policy_url'] = df.app_id.map(link_map)
    write_table(OUT/'apps_apple.parquet', pa.Table.from_pandas(df, preserve_index=False))
    linked = df[df.policy_url.fillna('').ne('')].copy()
    stats['unique_apps_with_us_page_policy_url'] = len(linked)
    stats['apps_missing_artistId'] = int(linked.artistId.fillna('').eq('').sum())
    linked = linked[linked.artistId.fillna('').ne('')].drop_duplicates('artistId', keep='first')
    domains, excluded = Domains(), load_exclusions()
    rows, rejected = [], []
    for frame_rank, r in enumerate(pa.Table.from_pandas(linked, preserve_index=False).to_pylist(), 1):
        row = dict(r, arm='apple', frame_rank=frame_rank, organization_key=r['artistId'],
                   organization_name=r['artistName'], size_proxy=r['userRatingCount'], size_proxy_name='userRatingCount',
                   app_title=r['trackName'], app_genre=r['primaryGenreName'])
        row['policy_registered_domain'] = domains.registered(row['policy_url'])
        if row['policy_registered_domain'] in excluded:
            rejected.append(dict(row, stage='frame', reason='development_domain'))
        else:
            rows.append(dict(row, rank=len(rows)+1, candidate_id=f'apple-c{len(rows)+1:07d}'))
    write_table(OUT/'candidates_apple.parquet', rows)
    write_table(OUT/'frame_rejected_apple.parquet', rejected)
    stats.update(organizations_before_exclusions=len(linked), excluded_organizations=len(rejected), candidates=len(rows))
    write_json(OUT/'frame_apple.json', dict(counts=dict(stats), shards=len(snap['files']),
        skipped=snap['skipped']+[r for r in results if r.get('skipped')],
        policy_url_method='US app_page raw JSON parsed with apple_policy_links; provided link tables retained as cross-check',
        recovery_request_limiter='1 request attempt per second, including retries',
        recovery_http_attempts=dict(C.ATTEMPTS)))
    print(dict(stats), flush=True)


if __name__ == '__main__':
    main()
