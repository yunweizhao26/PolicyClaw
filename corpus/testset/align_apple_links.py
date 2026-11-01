from collections import Counter
import json

import pyarrow as pa
import pyarrow.parquet as pq

from base import OUT, Domains, load_exclusions, require_compute, unchanged, write_json, write_table
from apple import page_index, PAGE_SCHEMA, is_us_row

METHOD = 'Supplied full/pilot link tables first; recovered US pages override; parsed US pages fill missing mappings'


def main():
    require_compute()
    report=json.loads((OUT/'frame_apple.json').read_text())
    if report.get('policy_url_method')==METHOD:
        return
    df=pq.read_table(OUT/'apps_apple.parquet').to_pandas()
    df['parsed_us_page_policy_url']=df.policy_url
    recovered={p.stem.removeprefix('part-') for p in (OUT/'apple_pages').glob('*.parquet')}
    pilot_pages={}
    pilot_rows=0
    snap=json.loads((OUT/'snapshots/apple_meta.json').read_text())
    for entry in snap['files']:
        if '/data/apple/meta/' not in entry['path']:
            continue
        unchanged(entry)
        columns=[c for c in ('app_id','kind','storefront','request_url','final_url','http_status','fetched_at','data_raw')
                 if c in entry['columns']]
        for batch in pq.ParquetFile(entry['path']).iter_batches(columns=columns,batch_size=128):
            for row in batch.to_pylist():
                if row['kind']!='app_page':
                    continue
                if not is_us_row(row):
                    continue
                pilot_rows+=1
                indexed=page_index(row,entry['path'])
                old=pilot_pages.get(row['app_id'])
                if old is None or (indexed['policy_url'] and not old['policy_url']) or (
                    bool(indexed['policy_url'])==bool(old['policy_url']) and indexed['page_fetched_at']>=old['page_fetched_at']):
                    pilot_pages[row['app_id']]=indexed
        unchanged(entry)
    write_table(OUT/'apple_pilot_pages.parquet',list(pilot_pages.values()),PAGE_SCHEMA)
    before_links=int(df.policy_url.fillna('').ne('').sum())
    df['has_us_app_page']=df.has_us_app_page | df.app_id.isin(pilot_pages)
    pilot_urls=df.app_id.map({k:r['policy_url'] for k,r in pilot_pages.items()})
    fallback=df.policy_url.isna() & pilot_urls.notna() & ~df.app_id.isin(recovered)
    df.loc[fallback,'policy_url']=pilot_urls[fallback]
    use_table=(df.links_table_policy_url.notna() & df.has_us_app_page & ~df.app_id.isin(recovered))
    changed=int((use_table & (df.policy_url.fillna('')!=df.links_table_policy_url.fillna(''))).sum())
    df.loc[use_table,'policy_url']=df.loc[use_table,'links_table_policy_url']
    write_table(OUT/'apps_apple.parquet',pa.Table.from_pandas(df,preserve_index=False))
    linked=df[df.policy_url.fillna('').ne('')].copy()
    counts=report['counts']
    counts['unique_apps_with_us_page_policy_url']=len(linked)
    counts['apps_missing_artistId']=int(linked.artistId.fillna('').eq('').sum())
    counts['policy_urls_from_supplied_link_tables']=int(use_table.sum())
    counts['policy_urls_changed_by_supplied_table_priority']=changed
    counts['pilot_us_app_page_rows_recovered_from_legacy_schema']=pilot_rows
    counts['pilot_us_apps_recovered_from_legacy_schema']=len(pilot_pages)
    counts['apps_with_links_added_by_pilot_and_table_alignment']=len(linked)-before_links
    counts['recovered_top_apps_with_preexisting_legacy_pilot_us_page']=len(recovered & set(pilot_pages))
    for skipped in report.get('skipped',[]):
        if '/data/apple/meta/' in skipped.get('source','') and 'storefront' in skipped.get('skipped',''):
            skipped['resolved_by']='apple_link_priority: explicit US request URL in legacy pilot schema'
    linked=linked.sort_values(['userRatingCount','app_id'],ascending=[False,True],na_position='last',kind='stable')
    linked=linked[linked.artistId.fillna('').ne('')].drop_duplicates('artistId',keep='first')
    domains,excluded=Domains(),load_exclusions()
    rows,rejected=[],[]
    for frame_rank,r in enumerate(pa.Table.from_pandas(linked,preserve_index=False).to_pylist(),1):
        row=dict(r,arm='apple',frame_rank=frame_rank,organization_key=r['artistId'],organization_name=r['artistName'],
                 size_proxy=r['userRatingCount'],size_proxy_name='userRatingCount',app_title=r['trackName'],app_genre=r['primaryGenreName'])
        row['policy_registered_domain']=domains.registered(row['policy_url'])
        if row['policy_registered_domain'] in excluded:
            rejected.append(dict(row,stage='frame',reason='development_domain'))
        else:
            rows.append(dict(row,rank=len(rows)+1,candidate_id=f'apple-c{len(rows)+1:07d}'))
    write_table(OUT/'candidates_apple.parquet',rows)
    write_table(OUT/'frame_rejected_apple.parquet',rejected)
    counts.update(organizations_before_exclusions=len(linked),excluded_organizations=len(rejected),candidates=len(rows))
    report['policy_url_method']=METHOD
    write_json(OUT/'frame_apple.json',report)
    print('Apple link-table priority:',changed,'URLs changed;',int(use_table.sum()),'provided mappings used;',len(rows),'candidate organizations',flush=True)


if __name__=='__main__':
    main()
