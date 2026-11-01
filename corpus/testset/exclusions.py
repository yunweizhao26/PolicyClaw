from collections import defaultdict
import json
from pathlib import PurePosixPath
import re
import zipfile

import pyarrow as pa

from base import OUT, ROOT, Domains, hostname, require_compute, sha, write_json, write_table

POLICYIE = ROOT.parent/'Contextual-Integrity/policy-ie/data/sanitized_split.zip'
POLICYIE_APPS = {'co.happybits.marcopolo', 'com.apps.go.clean.boost.master', 'com.blackout.word'}
POLICYIE_SITES = {'codecademy.com', 'digg.com', 'entrepreneur.com'}


def policy_members(names):
    groups = defaultdict(list)
    for name in names:
        path = PurePosixPath(name)
        if path.suffix.lower() != '.txt' or '__MACOSX' in path.parts:
            continue
        if not any(p in ('train', 'test') or re.fullmatch(r'week\w*', p) for p in path.parts[:-1]):
            continue
        groups[str(path.parent)].append(name)
    def numeric(name):
        numbers = tuple(int(n) for n in re.findall(r'\d+', PurePosixPath(name).stem))
        if not numbers:
            raise ValueError(f'PolicyIE text filename has no numeric order: {name}')
        return numbers, name
    return {key: sorted(values, key=numeric) for key, values in sorted(groups.items())}


def policyie_texts():
    with zipfile.ZipFile(POLICYIE) as archive:
        groups = policy_members(archive.namelist())
        assert groups, 'No PolicyIE text policies found'
        result = []
        for policy, members in groups.items():
            text = '\n'.join(archive.read(name).decode('utf-8-sig') for name in members)
            assert text.strip(), f'Empty PolicyIE policy: {policy}'
            result.append(dict(policy=policy, members=members, text=text, sha256=sha(text)))
        return result


class PolicyIE:
    def __init__(self):
        from select_candidates import shingles
        self.policies = [(r['policy'], shingles(r['text'])) for r in policyie_texts()]
        assert all(s for _, s in self.policies), 'A PolicyIE policy has no 5-word shingles'

    def maximum(self, value):
        matches = [(len(value & other), len(other), name) for name, other in self.policies]
        intersection, denominator, name = max(matches, key=lambda r: r[0]/r[1])
        return dict(policyie_containment=intersection/denominator, policyie_policy=name,
                    policyie_intersection=intersection, policyie_denominator=denominator)


def exclusion_sources():
    import pyarrow.parquet as pq
    result = defaultdict(set)
    for row in pq.read_table(OUT/'exclusions.parquet').to_pylist():
        result[row['registered_domain']].add(row['source'])
    return result


def exclusion_reason(domains, sources):
    matched = set().union(*(sources.get(d, set()) for d in domains if d))
    if 'development' in matched:
        return 'development_domain'
    if 'PolicyIE_test_site' in matched:
        return 'policyie_test_site_domain'
    return None


def main():
    require_compute()
    domains, rows, sites = Domains(), [], set()
    dev = ROOT/'corpus/versions.jsonl'
    for i, line in enumerate(dev.open(), 1):
        record = json.loads(line)
        if record.get('domain'):
            sites.add(hostname(record['domain']).removeprefix('www.'))
        for field in ('url', 'domain'):
            value = record.get(field)
            if value:
                domain = domains.registered(value)
                assert domain, f'Invalid development {field} at line {i}'
                rows.append(dict(source='development', value=value, host=hostname(value),
                    registered_domain=domain, reference=f'{dev}:{i}:{field}'))
    for site in sorted(POLICYIE_SITES):
        rows.append(dict(source='PolicyIE_test_site', value=site, host=hostname(site),
            registered_domain=domains.registered(site), reference='DESIGN.md: Organizations'))
    rows = list({(r['source'], r['value']): r for r in rows}.values())
    write_table(OUT/'exclusions.parquet', rows, pa.schema([(k, pa.string()) for k in
        ('source', 'value', 'host', 'registered_domain', 'reference')]))
    from select_candidates import shingles
    policies = policyie_texts()
    audit = dict(source=str(POLICYIE), source_sha256=sha(POLICYIE.read_bytes()),
        policies=[{k:v for k,v in r.items() if k != 'text'} | {'shingles':len(shingles(r['text']))} for r in policies],
        policy_count=len(policies), test_app_ids=sorted(POLICYIE_APPS), test_sites=sorted(POLICYIE_SITES),
        concatenation='Numeric filename order within each policy directory, joined by newline',
        containment='Exact intersection / distinct PolicyIE 5-word shingles; reject >= 0.5')
    assert all(r['shingles'] for r in audit['policies'])
    write_json(OUT/'policyie_source_audit.json', audit)
    stats = {source: dict(values=len(group), registered_domains=len({r['registered_domain'] for r in group}))
        for source in ('development', 'PolicyIE_test_site')
        for group in [[r for r in rows if r['source'] == source]]}
    write_json(OUT/'exclusions.json', dict(sources=stats, normalized_development_sites=len(sites),
        unique_registered_domains=len({r['registered_domain'] for r in rows}),
        policyie=audit, development_sha256=sha(dev.read_bytes()), opp115_excluded=False))
    assert len(sites) == 290, f'Expected 290 development sites; found {len(sites)}'


if __name__ == '__main__':
    main()
