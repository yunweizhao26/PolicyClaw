from functools import lru_cache
import json

import pyarrow as pa
import pyarrow.parquet as pq

from base import OUT, Domains, require_compute, write_json, write_table
from exclusions import POLICYIE_APPS, exclusion_reason, exclusion_sources


def main():
    require_compute()
    domains, sources = Domains(), exclusion_sources()
    registered = lru_cache(maxsize=500000)(domains.registered)
    for arm in ('android', 'apple'):
        df = pq.read_table(OUT/f'apps_{arm}.parquet').to_pandas()
        report = json.loads((OUT/'v1'/f'frame_{arm}.json').read_text())
        if arm == 'android':
            key, name, proxy, own = 'developerId', 'developer', 'realInstalls', 'developerWebsite'
            order, ascending, link = ['realInstalls', 'minInstalls', 'ratings', 'app_id'], [False, False, False, True], 'privacyPolicy'
            title, genre = 'title', 'genre'
        else:
            key, name, proxy, own = 'artistId', 'artistName', 'userRatingCount', 'sellerUrl'
            order, ascending, link = ['userRatingCount', 'app_id'], [False, True], 'policy_url'
            title, genre = 'trackName', 'primaryGenreName'
        linked = df[df[link].fillna('').str.strip().ne('')].copy()
        linked = linked.sort_values(order, ascending=ascending, na_position='last', kind='stable')
        linked = linked[linked[key].fillna('').ne('')].drop_duplicates(key, keep='first')
        rows, rejected = [], []
        for frame_rank, item in enumerate(pa.Table.from_pandas(linked, preserve_index=False).to_pylist(), 1):
            row = dict(item, arm=arm, frame_rank=frame_rank, organization_key=item[key], organization_name=item[name],
                size_proxy=item[proxy], size_proxy_name=proxy, app_title=item[title], app_genre=item[genre],
                policy_url=item[link].strip())
            row['policy_registered_domain'] = registered(row['policy_url'])
            row['organization_domain'] = registered(item.get(own))
            reason = ('policyie_test_app_id' if row['app_id'] in POLICYIE_APPS else
                      exclusion_reason([row['policy_registered_domain']], sources))
            if reason:
                rejected.append(dict(row, stage='frame', reason=reason))
            else:
                rows.append(dict(row, rank=len(rows)+1, candidate_id=f'{arm}-v2-c{len(rows)+1:07d}'))
        write_table(OUT/f'candidates_{arm}.parquet', rows)
        write_table(OUT/f'frame_rejected_{arm}.parquet', rejected)
        report['counts'].update(organizations_before_exclusions=len(linked), excluded_organizations=len(rejected), candidates=len(rows))
        report.update(revision=2, psl_sha256=json.loads((OUT/'psl/manifest.json').read_text())['sha256'],
                      app_metadata_source=f'apps_{arm}.parquet (frozen first-run parsed universe)')
        write_json(OUT/f'frame_{arm}.json', report)
        print(arm, report['counts'], flush=True)


if __name__ == '__main__':
    main()
