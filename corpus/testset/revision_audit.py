from collections import Counter, defaultdict
import json
import importlib.metadata
import platform

import pyarrow.parquet as pq

from base import ARMS, OUT, ROOT, Domains, require_compute, sha, write_json, write_table
from exclusions import POLICYIE_APPS, PolicyIE, exclusion_sources
from fetch_candidates import candidates
from revision_fetch import Backend, read_fetch
from revision_select import Selector
from select_candidates import jaccard, shingles, tsv


def main():
    require_compute()
    selected = pq.read_table(OUT/'selection.parquet').to_pylist()
    assert len(selected) == 600
    assert [r['arm'] for r in selected] == list(ARMS)*200
    domains, policyie = Domains(), PolicyIE()
    frames = {a:candidates(a) for a in ARMS}
    by_candidate = {r['candidate_id']:r for group in frames.values() for r in group}
    replay = Selector(Backend(offline=True), domains, exclusion_sources(), policyie)
    assert replay.walk(frames)
    keys = ('id', 'arm', 'rank', 'candidate_id', 'organization_key', 'policy_url', 'final_url',
            'visible_sha256', 'trafilatura_sha256', 'final_registered_domain', 'verifier_view_key',
            'home_final_url', 'chosen_link_url', 'chosen_link_anchor_text')
    assert [[r.get(k) for k in keys] for r in selected] == [[r.get(k) for k in keys] for r in replay.selected]
    rejected = [r for r in pq.read_table(OUT/'rejected.parquet').to_pylist() if r['stage'] == 'selection']
    rejection_keys = ('candidate_id', 'reason', 'duplicate_of', 'shared_domain', 'domain_conflicts', 'final_url', 'link_reasons')
    assert [[r.get(k) for k in rejection_keys] for r in rejected] == [[r.get(k) for k in rejection_keys] for r in replay.rejected]
    links = pq.read_table(OUT/'rejected_links.parquet').to_pylist()
    assert [[r.get(k) for k in rejection_keys] for r in links] == [[r.get(k) for k in rejection_keys] for r in replay.links]
    used, sets, containment = set(), [], []
    for row in selected:
        source = by_candidate[row['candidate_id']]
        for key, value in source.items():
            if row['arm'] == 'web' and key in ('policy_url', 'policy_registered_domain'):
                continue
            assert row[key] == value, (row['id'], key, 'candidate metadata mismatch')
        identities = {domains.registered(row['final_url'])}
        if row['arm'] == 'web':
            identities.add(row['web_domain'])
            assert row['size_proxy'] == domains.ranks[row['web_domain']]
        assert not identities & used
        used.update(identities)
        assert row.get('app_id') not in POLICYIE_APPS
        assert 200 <= row['status'] < 300 and row['visible_chars'] >= 100
        assert row['fetched_at'].startswith('2026-10-')
        assert row['verifier_label'] == 'complete_policy' and row['language'] == 'en'
        body = read_fetch(row['fetch_id'], raw=True)
        assert sha(body['body'] or b'') == row['body_sha256']
        assert body['final_url'] == row['final_url'] and body['http_status'] == row['status']
        for kind in ('visible', 'trafilatura'):
            text = (OUT/'texts'/f'{row["id"]}.{kind}.txt').read_bytes().decode('utf-8')
            assert len(text) == row[kind+'_chars'] and sha(text) == row[kind+'_sha256']
            assert text == body[kind+'_text']
        value = shingles(body['visible_text'])
        sets.append(value)
        match = policyie.maximum(value)
        assert match['policyie_containment'] < 0.5
        assert all(row[k] == v for k,v in match.items())
        containment.append(dict(id=row['id'], **match))
    max_value, pair, numerator, denominator, exact, bounded = -1, None, None, None, 0, 0
    for i, left in enumerate(sets):
        for j in range(i):
            right = sets[j]
            bound = min(len(left), len(right))/max(len(left), len(right)) if left or right else 1
            if bound <= max_value:
                bounded += 1
                continue
            value = jaccard(left, right)
            exact += 1
            if value > max_value:
                max_value, pair = value, [selected[j]['id'], selected[i]['id']]
                numerator = len(left & right)
                denominator = len(left | right)
    assert max_value < 0.5 and exact + bounded == 600*599//2
    overlap = defaultdict(lambda: defaultdict(set))
    for arm, rows in frames.items():
        assert [r['rank'] for r in rows] == list(range(1, len(rows)+1))
        assert len({r['organization_key'] for r in rows}) == len(rows)
        values = [r['size_proxy'] for r in rows if r['size_proxy'] is not None]
        assert values == sorted(values, reverse=arm != 'web')
        for row in rows:
            domain = row['web_domain'] if arm == 'web' else domains.registered(row['policy_url'])
            if domain:
                overlap[domain][arm].add((row['organization_key'], row['organization_name'] or ''))
    for row in replay.attempts:
        if row['registered_domain']:
            overlap[row['registered_domain']][row['arm']].add((row['organization_key'], row['organization_name'] or ''))
    cross = []
    for domain, arms in sorted(overlap.items()):
        if len(arms) < 2:
            continue
        winner = replay.used.get(domain)
        cross.append(dict(registered_domain=domain, arms=','.join(a for a in ARMS if a in arms),
            organizations=json.dumps({a:sorted(v) for a,v in arms.items()}, ensure_ascii=False),
            selected_arm=winner['arm'] if winner else None, selected_id=winner['id'] if winner else None))
    write_table(OUT/'cross_arm_organizations.parquet', cross)
    tsv(OUT/'cross_arm_organizations.tsv', cross)
    archive = json.loads((OUT/'v1/archive_manifest.json').read_text())
    for name, digest in archive['protected_files'].items():
        assert sha((OUT/name).read_bytes()) == digest, f'Protected file changed: {name}'
    maximum_containment = max(containment, key=lambda r:r['policyie_containment'])
    write_json(OUT/'audit.json', dict(revision=2, valid=True, selected=600,
        counts=dict(Counter(r['arm'] for r in selected)), maximum_pairwise_jaccard=max_value,
        maximum_pair=pair, maximum_pair_intersection=numerator, maximum_pair_union=denominator,
        pairs_total=exact+bounded, pairs_intersected=exact, pairs_proven_below_current_max_by_size_bound=bounded,
        maximum_policyie_containment=maximum_containment['policyie_containment'],
        maximum_policyie_match=maximum_containment, cross_arm_registered_domains=len(cross),
        cross_arm_domains_selected=sum(bool(r['selected_id']) for r in cross),
        checks=['600 rows; 200 per arm; round-robin order', 'offline replay of every walked candidate and privacy link',
            'final policy and web-site PSL identities are disjoint', '2xx; >=100 characters; English complete_policy',
            'October 2026 fetches; text hashes and lengths', 'PolicyIE ids, domains and exact containment',
            'rank order and unique organization keys', 'exact pairwise Jaccard maximum', 'protected files unchanged']))
    paths = [ROOT/'corpus/stores/common.py', ROOT/'corpus/stores/text.py', ROOT/'corpus/rebuild_versions.py',
             ROOT/'corpus/stores/meta.py', ROOT/'corpus/stores/links.py', ROOT/'policyclaw/llm.py',
             ROOT/'corpus/collect/verify.py', ROOT/'corpus/collect/rubric.md', ROOT/'policyclaw/prompts/verify_policy_page.txt']
    paths += sorted(OUT.glob('*.py')) + sorted(OUT.glob('*.sbatch')) + [OUT/'DESIGN.md']
    write_json(OUT/'code_provenance.json', {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths})
    write_json(OUT/'package_versions.json', dict(python=platform.python_version(), packages={
        name:importlib.metadata.version(name) for name in ('pyarrow', 'pandas', 'trafilatura', 'idna', 'lxml', 'requests', 'pypdf')}))
    print('PASS: offline replay and 600-policy audit', max_value, maximum_containment, flush=True)


if __name__ == '__main__':
    main()
