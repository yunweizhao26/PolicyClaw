from collections import Counter, defaultdict
import json
import importlib.metadata
import platform

import pyarrow.parquet as pq

from base import ARMS, OUT, ROOT, Domains, hostname, load_exclusions, require_compute, sha, write_json, write_table
from select_candidates import jaccard, shingles, tsv
from fetch_candidates import candidates


def main():
    require_compute()
    development = [json.loads(line) for line in (ROOT/'corpus/versions.jsonl').read_text().splitlines()]
    raw_domains = {r.get('domain') for r in development if r.get('domain')}
    normalized = defaultdict(list)
    for domain in sorted(raw_domains): normalized[hostname(domain)].append(domain)
    write_json(OUT/'development_sites_audit.json', dict(records=len(development), raw_domain_values=len(raw_domains),
        normalized_domain_values=len(normalized), collisions={k:v for k,v in normalized.items() if len(v)>1}))
    selected = pq.read_table(OUT/'selection.parquet').to_pylist()
    verification = {r['id']:r for r in (json.loads(line) for line in (OUT/'verify.jsonl').read_text().splitlines())}
    tsv(OUT/'verify_input.tsv', [dict(id=identity, text_path=str(OUT/'fetch/texts'/f'{identity}.visible.txt'),
        url=record['url'], source=record.get('source')) for identity,record in verification.items()])
    counts = Counter(r['arm'] for r in selected)
    assert len(selected) == 600 and all(counts[a] == 200 for a in ARMS)
    for arm in ARMS:
        group = [r for r in selected if r['arm'] == arm]
        source = {r['candidate_id']:r for r in candidates(arm, max(r['rank'] for r in group))}
        for row in group:
            for key, value in source[row['candidate_id']].items():
                assert row[key] == value, (row['id'], key, 'candidate metadata mismatch')
    assert [r['arm'] for r in selected] == list(ARMS)*200
    assert len({r['final_registered_domain'] for r in selected}) == 600
    assert all(r['final_registered_domain'] for r in selected)
    excluded, domains = load_exclusions(), Domains()
    texts, shingle_sets = [], []
    for row in selected:
        assert 200 <= row['status'] < 300 and row['visible_chars'] >= 100
        assert row['fetched_at'].startswith('2026-10-')
        assert row['verifier_label'] == 'complete_policy' and row['language'].lower() == 'en'
        verified = verification[row['candidate_id']]
        assert row['verifier_label'] == verified['label'] and row['language'] == verified['flags']['language']
        assert row['evidence'] == verified['evidence']
        assert sha((OUT/'fetch/texts'/f'{row["candidate_id"]}.visible.txt').read_bytes()) == row['visible_sha256']
        assert domains.registered(row['final_url']) == row['final_registered_domain']
        assert row['final_registered_domain'] not in excluded
        assert domains.registered(row['policy_url']) not in excluded
        for kind in ('visible', 'trafilatura'):
            value = (OUT/'texts'/f'{row["id"]}.{kind}.txt').read_bytes().decode('utf-8')
            assert len(value) == row[kind+'_chars'] and sha(value) == row[kind+'_sha256']
            if kind == 'visible': texts.append(value); shingle_sets.append(shingles(value))
    max_value, max_pair, calculated, bounded = -1.0, None, 0, 0
    for i, left in enumerate(shingle_sets):
        for j in range(i):
            right = shingle_sets[j]
            bound = min(len(left), len(right))/max(len(left), len(right)) if left or right else 1.0
            if bound <= max_value:
                bounded += 1; continue
            value = jaccard(left, right); calculated += 1
            if value > max_value:
                max_value, max_pair = value, [selected[j]['id'], selected[i]['id']]
        if (i+1) % 100 == 0: print(f'Exact pairwise maximum: {i+1}/600, maximum={max_value}', flush=True)
    assert max_value < 0.5
    assert calculated + bounded == 600*599//2
    by_id = {row['id']:i for i,row in enumerate(selected)}
    max_left, max_right = (shingle_sets[by_id[identity]] for identity in max_pair)
    max_intersection = len(max_left & max_right)
    max_union = len(max_left) + len(max_right) - max_intersection
    frame_stats = {}
    overlap = defaultdict(lambda:defaultdict(list))
    for arm in ARMS:
        seen, expected_rank, previous = set(), 1, None
        path = OUT/f'candidates_{arm}.parquet'
        order = pq.read_table(path, columns=['rank', 'organization_key', 'size_proxy']).sort_by('rank').to_pylist()
        for row in order:
            assert row['rank'] == expected_rank; expected_rank += 1
            assert row['organization_key'] not in seen; seen.add(row['organization_key'])
            value = row['size_proxy']
            if previous is not None and value is not None:
                assert value >= previous if arm == 'web' else value <= previous
            previous = value
        frame_stats[arm] = dict(organizations=len(order), rank_and_unique_key_checks=True)
        for batch in pq.ParquetFile(path).iter_batches(columns=['policy_registered_domain', 'organization_key', 'organization_name'], batch_size=20000):
            for row in batch.to_pylist():
                domain = row['policy_registered_domain']
                if domain:
                    overlap[domain][arm].append((row['organization_key'], row['organization_name']))
    winners = {r['final_registered_domain']:r for r in selected}
    for path in sorted((OUT/'fetch').glob('*.parquet')):
        row = pq.read_table(path, columns=['arm', 'candidate_id', 'final_url']).to_pylist()[0]
        domain = domains.registered(row['final_url'] or '')
        if domain and row['arm'] not in overlap[domain]:
            overlap[domain][row['arm']].append((row['candidate_id'], '(identity from final URL)'))
    cross = []
    for domain, arms in sorted(overlap.items()):
        if len(arms) < 2: continue
        winner = winners.get(domain)
        cross.append(dict(registered_domain=domain, arms=','.join(a for a in ARMS if a in arms),
            organization_keys=json.dumps({a:[x[0] for x in arms[a]] for a in ARMS if a in arms}),
            organization_names=json.dumps({a:sorted({x[1] or '' for x in arms[a]}) for a in ARMS if a in arms}, ensure_ascii=False),
            selected_arm=winner['arm'] if winner else None, selected_id=winner['id'] if winner else None))
    write_table(OUT/'cross_arm_organizations.parquet', cross)
    tsv(OUT/'cross_arm_organizations.tsv', cross)
    write_json(OUT/'audit.json', dict(valid=True, selected=len(selected), counts=dict(counts), frames=frame_stats,
        maximum_pairwise_jaccard=max_value, maximum_pair=max_pair, pairs_total=600*599//2,
        maximum_pair_intersection=max_intersection, maximum_pair_union=max_union,
        pairs_intersected=calculated, pairs_proven_below_current_max_by_size_bound=bounded,
        cross_arm_registered_domains=len(cross), cross_arm_domains_selected=sum(bool(r['selected_arm']) for r in cross),
        shingle_definition=r'Lowercase Unicode regex \w+ word tokens; sets of consecutive 5-token tuples; exact set Jaccard',
        checks=['600 rows and 200 per arm', 'web/android/apple turn sequence', 'unique final registered domains',
                '2xx, >=100 visible characters, English complete_policy', 'October 2026 fetch dates',
                'exclusion-domain checks', 'both text hashes and lengths', 'verifier input hash, label, language, and evidence joins',
                'every selected metadata field matches its frozen candidate row', 'rank ordering and unique organization keys',
                'exact pairwise shingle Jaccard maximum']))
    source_paths = [ROOT/'corpus/testset/DESIGN.md', ROOT/'corpus/stores/common.py', ROOT/'corpus/stores/meta.py',
                   ROOT/'corpus/stores/links.py', ROOT/'corpus/stores/text.py', ROOT/'corpus/rebuild_versions.py',
                   ROOT/'corpus/collect/verify.py', ROOT/'corpus/collect/rubric.md', ROOT/'policyclaw/prompts/verify_policy_page.txt',
                   ROOT/'policyclaw/llm.py'] + sorted(OUT.glob('*.py')) + sorted(OUT.glob('*.sbatch'))
    write_json(OUT/'code_provenance.json', {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in source_paths})
    write_json(OUT/'package_versions.json', dict(python=platform.python_version(), packages={name:importlib.metadata.version(name)
        for name in ('pyarrow', 'pandas', 'trafilatura', 'google-play-scraper', 'requests', 'pypdf')}))
    print('PASS: 600-policy artifact audit; exact maximum Jaccard', max_value, max_pair, flush=True)


if __name__ == '__main__':
    main()
