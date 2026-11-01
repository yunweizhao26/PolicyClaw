from collections import Counter
import json

import pyarrow.parquet as pq

from base import ARMS, OUT, Domains, require_compute, sha, write_json, write_table
from exclusions import PolicyIE, exclusion_reason, exclusion_sources
from fetch_candidates import candidates
from revision_fetch import Backend, privacy_links, read_fetch
from select_candidates import first_duplicate, shingles, tsv


class Selector:
    def __init__(self, backend, domains, sources, policyie):
        self.backend, self.domains, self.sources, self.policyie = backend, domains, sources, policyie
        self.selected, self.rejected, self.links, self.attempts, self.sets = [], [], [], [], []
        self.used, self.counts = {}, Counter()

    def consider(self, candidate, url):
        body = self.backend.fetch(url, candidate['arm'])
        domain = self.domains.registered(body.get('final_url') or url)
        info = dict(candidate_id=candidate['candidate_id'], arm=candidate['arm'], rank=candidate['rank'],
            frame_rank=candidate['frame_rank'], organization_key=candidate['organization_key'],
            organization_name=candidate['organization_name'], policy_url=url, final_url=body.get('final_url'),
            registered_domain=domain, fetch_id=body['fetch_id'], stage='selection', http_status=body['http_status'],
            visible_chars=body['visible_chars'], fetch_reused_from=body.get('reused_from'),
            fetch_reused=not body['fetch_id'].startswith('url-v2-') or bool(body.get('reused_from')))
        reason = None
        if body['http_status'] is None or not 200 <= body['http_status'] < 300:
            reason = 'http_not_2xx'
            info['detail'] = body.get('error') or str(body['http_status'])
        elif body['visible_chars'] < 100:
            reason = 'visible_text_under_100_chars'
            info['detail'] = body.get('extraction_error')
        if reason:
            info['reason'] = reason
            self.attempts.append(info)
            return None, info
        result = self.backend.verify(body, candidate['arm'])
        info.update(verifier_label=result['label'], language=result['flags']['language'], verifier_id=result['id'])
        if result['label'] != 'complete_policy':
            reason = 'verifier_' + result['label']
        elif result['flags']['language'] != 'en':
            reason = 'not_english'
        else:
            reason = exclusion_reason([domain, self.domains.registered(url)], self.sources)
        text_set = shingles(body['visible_text'])
        containment = self.policyie.maximum(text_set)
        info.update(containment)
        if reason is None and containment['policyie_containment'] >= 0.5:
            reason = 'policyie_containment_ge_0.5'
        identities = {domain}
        if candidate['arm'] == 'web':
            identities.add(candidate['web_domain'])
        if reason is None:
            assert domain, f'A successful fetched URL has no host: {body.get("final_url")}'
            shared = sorted(identities & self.used.keys())
            if shared:
                reason = 'duplicate_registered_domain'
                winner = self.used[shared[0]]
                info.update(shared_domain=shared[0], shared_domains=shared, duplicate_of=winner['id'],
                    duplicate_organization_name=winner['organization_name'], duplicate_final_url=winner['final_url'])
                info['domain_conflicts'] = json.dumps([dict(shared_domain=d, duplicate_of=self.used[d]['id'],
                    duplicate_organization_name=self.used[d]['organization_name'],
                    duplicate_final_url=self.used[d]['final_url']) for d in shared], ensure_ascii=False)
            else:
                duplicate = first_duplicate(text_set, self.sets)
                if duplicate:
                    reason = 'duplicate_visible_text_jaccard_ge_0.5'
                    winner = self.selected[duplicate[0]]
                    info.update(duplicate_of=winner['id'], jaccard=duplicate[1],
                        duplicate_organization_name=winner['organization_name'], duplicate_final_url=winner['final_url'])
        info['reason'] = reason or 'selected'
        self.attempts.append(info)
        if reason:
            return None, info
        fields = {k:v for k,v in body.items() if k not in ('body', 'visible_text', 'trafilatura_text', 'arm', 'candidate_id')}
        row = dict(candidate)
        row.update(fields)
        row.update(policy_url=url, policy_registered_domain=self.domains.registered(url),
            final_registered_domain=domain, status=body['http_status'], verifier_id=result['id'],
            verifier_label=result['label'], language=result['flags']['language'], evidence=result['evidence'],
            verifier_reason=result['reason'], evidence_in_view=result.get('evidence_in_view'),
            multiple_orgs=result['flags']['multiple_orgs'], verifier_view_key=result['view_key'], **containment)
        return (row, text_set, identities), info

    def next_organization(self, candidate):
        if candidate['arm'] != 'web':
            chosen, info = self.consider(candidate, candidate['policy_url'])
            if chosen is None:
                self.rejected.append(info)
            return chosen
        home_url = f'https://{candidate["web_domain"]}/'
        home = self.backend.fetch(home_url, 'web', raw=True)
        metadata = dict(home_url=home_url, home_final_url=home.get('final_url'), home_fetch_id=home['fetch_id'],
                        home_http_status=home['http_status'], home_fetched_at=home['fetched_at'],
                        organization_domain=candidate['web_domain'])
        reject = dict(candidate_id=candidate['candidate_id'], arm='web', rank=candidate['rank'],
            frame_rank=candidate['frame_rank'], organization_key=candidate['organization_key'],
            organization_name=candidate['organization_name'], stage='selection', **metadata)
        if home['http_status'] is None or not 200 <= home['http_status'] < 300 or not home.get('body'):
            self.rejected.append(dict(reject, reason='home_page_not_fetched',
                detail=home.get('error') or str(home['http_status'])))
            return None
        links = privacy_links(home['body'], home['final_url'] or home_url)
        if not links:
            self.rejected.append(dict(reject, reason='no_privacy_link'))
            return None
        failed = []
        for index, link in enumerate(links[:3], 1):
            chosen, info = self.consider(candidate, link['url'])
            info.update(link_number=index, anchor_text=link['anchor_text'], **metadata)
            if chosen:
                chosen[0].update(**metadata, chosen_link_number=index, chosen_link_anchor_text=link['anchor_text'],
                    chosen_link_url=link['url'], home_privacy_links=len(links),
                    previous_link_rejections=json.dumps(failed, ensure_ascii=False))
                return chosen
            detail = dict(info, stage='web_link')
            failed.append(detail)
            self.links.append(detail)
        self.rejected.append(dict(reject, reason='no_eligible_link_among_first_three',
            link_reasons=json.dumps(failed, ensure_ascii=False)))
        return None

    def walk(self, frames, target=200, checkpoint=None):
        positions = dict.fromkeys(ARMS, 0)
        while any(self.counts[a] < target and positions[a] < len(frames[a]) for a in ARMS):
            for arm in ARMS:
                if self.counts[arm] >= target:
                    continue
                while positions[arm] < len(frames[arm]):
                    candidate = frames[arm][positions[arm]]
                    chosen = self.next_organization(candidate)
                    positions[arm] += 1
                    if chosen is None:
                        continue
                    row, value, identities = chosen
                    self.counts[arm] += 1
                    row.update(id=f'{arm}-{self.counts[arm]:03d}', selection_order=len(self.selected)+1)
                    self.selected.append(row)
                    self.sets.append(value)
                    for domain in identities:
                        self.used[domain] = row
                    if checkpoint:
                        checkpoint(self)
                    break
        return all(self.counts[a] == target for a in ARMS)


def save(selector, complete=False, error=None):
    frame_rejected = []
    for arm in ARMS:
        path = OUT/f'frame_rejected_{arm}.parquet'
        if path.exists():
            frame_rejected.extend({k:r.get(k) for k in ('arm', 'frame_rank', 'organization_key', 'organization_name',
                'app_id', 'policy_url', 'policy_registered_domain', 'stage', 'reason')}
                for r in pq.read_table(path).to_pylist())
    for name, rows in [('rejected', frame_rejected+selector.rejected), ('rejected_links', selector.links),
                       ('selection_attempts', selector.attempts)]:
        write_table(OUT/f'{name}.parquet', rows)
        tsv(OUT/f'{name}.tsv', rows)
    dest = 'selection' if complete else 'selection.partial'
    write_table(OUT/f'{dest}.parquet', selector.selected)
    tsv(OUT/f'{dest}.tsv', selector.selected)
    if complete:
        textdir = OUT/'texts'
        textdir.mkdir(exist_ok=True)
        for row in selector.selected:
            body = read_fetch(row['fetch_id'])
            for kind in ('visible', 'trafilatura'):
                value = body[kind+'_text']
                assert sha(value) == row[kind+'_sha256']
                (textdir/f'{row["id"]}.{kind}.txt').write_text(value, encoding='utf-8')
    write_json(OUT/'selection_state.json', dict(revision=2, complete=complete, selected=dict(selector.counts),
        rejected_considered=len(selector.rejected), rejected_links=len(selector.links), error=error))


def main():
    require_compute()
    selector = Selector(Backend(), Domains(), exclusion_sources(), PolicyIE())
    frames = {a:candidates(a) for a in ARMS}
    def checkpoint(value):
        if len(value.selected) % 30 == 0:
            save(value)
            print('Selected', dict(value.counts), 'rejected', len(value.rejected), flush=True)
    try:
        complete = selector.walk(frames, checkpoint=checkpoint)
    except Exception as error:
        save(selector, error=f'{type(error).__name__}: {error}')
        raise
    save(selector, complete)
    if not complete:
        raise RuntimeError('An arm exhausted its frozen frame before reaching 200')


if __name__ == '__main__':
    main()
