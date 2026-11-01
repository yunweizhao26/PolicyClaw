from collections import Counter
import csv
import json
from pathlib import Path
import re

import pyarrow.parquet as pq

from base import ARMS, OUT, Domains, load_exclusions, require_compute, sha, write_json, write_table
from fetch_candidates import candidates


def shingles(text):
    words = re.findall(r'\w+', text.lower(), flags=re.UNICODE)
    return {tuple(words[i:i+5]) for i in range(len(words)-4)}


def jaccard(left, right):
    intersection = len(left & right)
    union = len(left) + len(right) - intersection
    return intersection / union if union else 1.0


def first_duplicate(value, selected):
    for i, other in enumerate(selected):
        if min(len(value), len(other))*2 < max(len(value), len(other)):
            continue
        similarity = jaccard(value, other)
        if similarity >= 0.5:
            return i, similarity
    return None


def walk(frames, fetch, verify, domains, excluded, target=200):
    selected, rejected, sets, used_domains = [], [], [], {}
    counts, positions = Counter(), dict.fromkeys(ARMS, 0)
    while any(counts[a] < target and positions[a] < len(frames[a]) for a in ARMS):
        for arm in ARMS:
            if counts[arm] >= target: continue
            while positions[arm] < len(frames[arm]):
                candidate = frames[arm][positions[arm]]
                body = fetch(candidate['candidate_id'])
                if body is None:
                    return selected, rejected, dict(counts), dict(arm=arm, rank=candidate['rank'], reason='not_fetched')
                result = verify.get(candidate['candidate_id'])
                reason, detail, match_id, similarity = None, None, None, None
                if body['http_status'] is None or not 200 <= body['http_status'] < 300:
                    reason = 'http_not_2xx'; detail = str(body['http_status'])
                elif body['visible_chars'] < 100:
                    reason = 'visible_text_under_100_chars'; detail = body.get('extraction_error')
                elif result is None or 'error' in result:
                    return selected, rejected, dict(counts), dict(arm=arm, rank=candidate['rank'], reason='verifier_unresolved')
                elif result['label'] != 'complete_policy':
                    reason = 'verifier_'+result['label']
                elif result['flags']['language'].lower() != 'en':
                    reason = 'not_english'; detail = result['flags']['language']
                domain = domains.registered(body.get('final_url') or candidate['policy_url'])
                if reason is None:
                    if domain is None:
                        reason = 'unresolved_final_registered_domain'
                    elif domain in excluded:
                        reason = 'development_final_domain'
                    elif domain in used_domains:
                        reason = 'duplicate_final_registered_domain'; match_id = used_domains[domain]
                    else:
                        text_set = shingles(body['visible_text'])
                        duplicate = first_duplicate(text_set, sets)
                        if duplicate:
                            reason = 'duplicate_visible_text_jaccard_ge_0.5'
                            match_id, similarity = selected[duplicate[0]]['id'], duplicate[1]
                positions[arm] += 1
                if reason:
                    rejected.append(dict(candidate_id=candidate['candidate_id'], arm=arm, rank=candidate['rank'],
                        frame_rank=candidate.get('frame_rank'), organization_key=candidate['organization_key'],
                        organization_name=candidate.get('organization_name'), policy_url=candidate['policy_url'],
                        final_url=body.get('final_url'), registered_domain=domain, stage='selection', reason=reason,
                        detail=detail, duplicate_of=match_id, jaccard=similarity))
                    continue
                counts[arm] += 1
                identity = f'{arm}-{counts[arm]:03d}'
                fields = {k:v for k,v in body.items() if k not in ('body', 'visible_text', 'trafilatura_text', 'arm', 'candidate_id')}
                selected.append(dict(candidate, **fields, id=identity, selection_order=len(selected)+1,
                    final_registered_domain=domain, status=body['http_status'], verifier_label=result['label'],
                    language=result['flags']['language'], evidence=result['evidence'], verifier_reason=result['reason'],
                    evidence_in_view=result.get('evidence_in_view'), multiple_orgs=result['flags']['multiple_orgs']))
                sets.append(text_set); used_domains[domain] = identity
                break
    return selected, rejected, dict(counts), None


def fetch_record(identity):
    path = OUT/'fetch'/f'{identity}.parquet'
    if not path.exists(): return None
    cols = [c for c in pq.ParquetFile(path).schema_arrow.names if c != 'body']
    return pq.read_table(path, columns=cols).to_pylist()[0]


def tsv(path, rows):
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with Path(path).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=keys, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow({k:json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k,v in row.items()})


def main():
    require_compute()
    plan = json.loads((OUT/'active_plan.json').read_text())
    frames = {a:candidates(a, plan[a]+1) for a in ARMS}
    verification = {}
    if (OUT/'verify.jsonl').exists():
        for line in (OUT/'verify.jsonl').read_text().splitlines():
            row = json.loads(line); verification[row['id']] = row
    prepared = {c['candidate_id'] for arm, rows in frames.items() for c in rows if c['rank'] <= plan[arm]}
    chosen, rejected, counts, blocked = walk(frames, lambda identity: fetch_record(identity) if identity in prepared else None,
                                            verification, Domains(), load_exclusions())
    if blocked and blocked['rank'] > plan[blocked['arm']]:
        blocked['reason'] = 'outside_prepared_batch'
    frame_rejected = []
    for arm in ARMS:
        for r in pq.read_table(OUT/f'frame_rejected_{arm}.parquet').to_pylist():
            frame_rejected.append({k:r.get(k) for k in ('arm', 'frame_rank', 'organization_key', 'organization_name', 'policy_url', 'stage', 'reason')})
    write_table(OUT/'rejected.parquet', frame_rejected+rejected)
    tsv(OUT/'rejected.tsv', frame_rejected+rejected)
    complete = all(counts.get(a, 0) == 200 for a in ARMS)
    dest = OUT/('selection.parquet' if complete else 'selection.partial.parquet')
    write_table(dest, chosen)
    tsv(dest.with_suffix('.tsv'), chosen)
    if complete:
        textdir = OUT/'texts'; textdir.mkdir(exist_ok=True)
        for row in chosen:
            fetched = fetch_record(row['candidate_id'])
            for kind in ('visible', 'trafilatura'):
                value = fetched[kind+'_text']
                assert sha(value) == row[kind+'_sha256']
                (textdir/f'{row["id"]}.{kind}.txt').write_text(value, encoding='utf-8')
    write_json(OUT/'selection_state.json', dict(complete=complete, selected=counts, rejected_considered=len(rejected),
        blocked=blocked, exhausted_arms=[a for a in ARMS if counts.get(a,0)<200 and not blocked]))
    print(dict(complete=complete, selected=counts, blocked=blocked), flush=True)


if __name__ == '__main__':
    main()
