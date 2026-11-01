from collections import Counter
import json

import pyarrow.parquet as pq

from base import ARMS, OUT, now, require_compute, write_json
from select_candidates import tsv


def data(name, default=None):
    path = OUT/name
    return json.loads(path.read_text()) if path.exists() else default


def rows(name):
    path = OUT/name
    return pq.read_table(path).to_pylist() if path.exists() else []


def jsonlines(name):
    path = OUT/name
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def markdown_table(records, columns):
    def cell(value):
        return str(value if value is not None else '').replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')
    return ['| ' + ' | '.join(title for _,title in columns) + ' |',
            '| ' + ' | '.join('---' for _ in columns) + ' |'] + [
        '| ' + ' | '.join(cell(row.get(key)) for key,_ in columns) + ' |' for row in records]


def main():
    require_compute()
    state = data('selection_state.json', {})
    audit = data('audit.json', {})
    selected = rows('selection.parquet') if state.get('complete') else rows('selection.partial.parquet')
    rejected, links, attempts = rows('rejected.parquet'), rows('rejected_links.parquet'), rows('selection_attempts.parquet')
    frames = {a:data(f'frame_{a}.json', {}) for a in ARMS}
    funnels, endpoints, reasons = {}, {}, []
    for arm in ARMS:
        group = [r for r in selected if r['arm'] == arm]
        decisions = [r for r in rejected if r.get('arm') == arm and r.get('stage') == 'selection']
        frame_rejected = [r for r in rejected if r.get('arm') == arm and r.get('stage') == 'frame']
        if not frame_rejected:
            frame_rejected = rows(f'frame_rejected_{arm}.parquet')
        tries = [r for r in attempts if r['arm'] == arm]
        counts = frames[arm].get('counts', {})
        frame_count = counts.get('candidates')
        funnels[arm] = dict(organizations_before_exclusions=counts.get('organizations_before_exclusions'),
            frame_excluded=len(frame_rejected), candidates=frame_count,
            walked=len(group)+len(decisions), selected=len(group),
            not_walked=frame_count-len(group)-len(decisions) if frame_count is not None else None,
            policy_link_attempts=len(tries), unique_fetches=len({r['fetch_id'] for r in tries}),
            reused_fetches=len({r['fetch_id'] for r in tries if r['fetch_reused']}),
            fetched_now=len({r['fetch_id'] for r in tries if not r['fetch_reused']}),
            http_2xx=sum(r.get('http_status') is not None and 200 <= r['http_status'] < 300 for r in tries),
            visible_at_least_100=sum(r.get('http_status') is not None and 200 <= r['http_status'] < 300
                                      and r['visible_chars'] >= 100 for r in tries),
            verified=sum(bool(r.get('verifier_label')) for r in tries),
            complete_english=sum(r.get('verifier_label') == 'complete_policy' and r.get('language') == 'en' for r in tries),
            frame_rejection_reasons=dict(Counter(r['reason'] for r in frame_rejected)),
            rejection_reasons=dict(Counter(r['reason'] for r in decisions)),
            link_rejection_reasons=dict(Counter(r['reason'] for r in links if r['arm'] == arm)))
        if arm == 'web':
            funnels[arm]['home_attempts'] = len(group)+len(decisions)
            funnels[arm]['home_http_2xx'] = sum(r.get('home_http_status') is not None
                and 200 <= r['home_http_status'] < 300 for r in group+decisions)
        for stage, values in [('frame', frame_rejected), ('selection', decisions),
                              ('web_link', [r for r in links if r['arm'] == arm])]:
            for reason, count in sorted(Counter(r['reason'] for r in values).items()):
                reasons.append(dict(arm=arm, stage=stage, reason=reason, count=count))
        if group:
            endpoints[arm] = {position:{k:r.get(k) for k in ('id', 'rank', 'organization_name', 'size_proxy_name', 'size_proxy')}
                for position,r in [('first', group[0]), ('last', group[-1])]}
    web = [{k:r.get(k) for k in ('id', 'web_domain', 'size_proxy', 'home_final_url', 'chosen_link_anchor_text',
                                 'chosen_link_url', 'final_url')} for r in selected if r['arm'] == 'web']
    duplicates = []
    for row in rejected+links:
        if row.get('reason') == 'duplicate_registered_domain':
            for conflict in json.loads(row['domain_conflicts']):
                duplicates.append({k:row.get(k) for k in ('arm', 'rank', 'organization_name', 'final_url',
                    'link_number', 'candidate_id')} | conflict)
    mismatches = [{k:r.get(k) for k in ('id', 'arm', 'organization_name', 'organization_domain',
        'final_registered_domain', 'final_url', 'developerWebsite', 'sellerUrl')}
        for r in selected if r.get('organization_domain') and r['organization_domain'] != r['final_registered_domain']]
    for name, values in [('selected_web_policies', web), ('duplicate_registered_domains', duplicates),
                         ('policy_domain_mismatches', mismatches)]:
        tsv(OUT/f'{name}.tsv', values)
    usage = jsonlines('gemini_usage_v2.jsonl')
    errors = jsonlines('gemini_errors_v2.jsonl')
    tokens = {key:sum(r.get('usageMetadata', {}).get(field, 0) for r in usage)
        for key,field in [('input_tokens','promptTokenCount'), ('output_tokens','candidatesTokenCount'), ('thinking_tokens','thoughtsTokenCount')]}
    missing = sum('promptTokenCount' not in r.get('usageMetadata', {}) for r in usage)
    cost = (tokens['input_tokens']*0.75 + (tokens['output_tokens']+tokens['thinking_tokens'])*3.75)/1_000_000
    gemini = dict(**tokens, billed_output_tokens=tokens['output_tokens']+tokens['thinking_tokens'],
        api_responses=len(usage), responses_missing_usage=missing, api_errors_without_usage=len(errors),
        observed_cost_usd=cost, cost_usd=cost if not missing and not errors else None,
        input_usd_per_million=0.75, output_usd_per_million=3.75,
        rate_basis='Same configured rates as v1; thinking is billed as output',
        cache_reuses=sum(r.get('usage', {}).get('cached', 0) for r in jsonlines('verify.jsonl')))
    metrics = sorted((json.loads(p.read_text()) for p in (OUT/'metrics').glob('v2_*.json')), key=lambda r:r['started_at'])
    tranco, psl = data('tranco/manifest.json', {}), data('psl/manifest.json', {})
    summary = dict(revision=2, generated_at=now(), selection_complete=state.get('complete', False),
        audit_valid=audit.get('valid', False), frames=frames, funnels=funnels, endpoints=endpoints,
        maximum_pairwise_jaccard=audit.get('maximum_pairwise_jaccard'), maximum_pair=audit.get('maximum_pair'),
        maximum_policyie_containment=audit.get('maximum_policyie_containment'),
        maximum_policyie_match=audit.get('maximum_policyie_match'), gemini=gemini, resources=metrics,
        tranco=tranco, psl=psl, state=state, failure=data('revision_failure.json'),
        review_lists=dict(web='selected_web_policies.tsv', duplicates='duplicate_registered_domains.tsv',
            mismatches='policy_domain_mismatches.tsv', cross_arm='cross_arm_organizations.tsv', links='rejected_links.tsv'))
    write_json(OUT/'report.json', summary)
    lines = ['# PolicyClaw evaluation set: revised selection', '',
        '**600 policies; audit passed.**' if summary['selection_complete'] and summary['audit_valid'] else
        '**Incomplete or not yet validated. No revised 600-policy result is claimed.**', '',
        f'Tranco: {tranco.get("list_id")} ({tranco.get("date")}). PSL: {psl.get("date", "not downloaded")}; SHA-256 `{psl.get("sha256", "unavailable")}`.', '',
        'The first selection is preserved in `v1/`. App metadata and stored policy fetches are reused. '
        'Web policies come from the first eligible privacy link among the first three on the final homepage. '
        'All domain identities use the pinned PSL, including private rules. OPP-115 is not excluded.', '',
        '## Funnel', '']
    lines += markdown_table([dict(arm=a, **f) for a,f in funnels.items()], [
        ('arm','Arm'), ('organizations_before_exclusions','Organizations'), ('frame_excluded','Excluded'),
        ('candidates','Candidates'), ('walked','Walked'), ('policy_link_attempts','Policy links'),
        ('http_2xx','2xx'), ('visible_at_least_100','>=100 chars'), ('verified','Verified'),
        ('complete_english','Complete/en'), ('selected','Selected'), ('not_walked','Not walked')])
    lines += ['', 'Policy-link counts include failed alternatives for websites; web-link rejections are nested within organization decisions. '
        'Full frame counters are in `report.json` and `frame_*.json`.', '']
    lines += markdown_table(reasons, [('arm','Arm'), ('stage','Stage'), ('reason','Reason'), ('count','Count')])
    lines += ['', '## First and last selected', '']
    lines += markdown_table([dict(arm=a, position=p, **r) for a,ends in endpoints.items() for p,r in ends.items()],
        [('arm','Arm'), ('position','Position'), ('rank','Rank'), ('organization_name','Organization'),
         ('size_proxy_name','Size proxy'), ('size_proxy','Value')])
    lines += ['', '## Checks and new verification cost', '',
        f'Maximum pairwise Jaccard: {audit.get("maximum_pairwise_jaccard", "not computed")}; pair: {audit.get("maximum_pair", "unavailable")}. '
        f'Maximum PolicyIE containment: {audit.get("maximum_policyie_containment", "not computed")}; '
        f'match: `{json.dumps(audit.get("maximum_policyie_match"))}`.', '',
        r'Both use lowercase Unicode `\w+` tokens and exact 5-word shingle sets. Containment divides by the PolicyIE set size; both rejection thresholds are >=0.5.', '',
        f'New Gemini responses: {len(usage)}; input tokens: {tokens["input_tokens"]}; answer tokens: {tokens["output_tokens"]}; '
        f'thinking tokens: {tokens["thinking_tokens"]}; observed cost: ${cost:.8f}. '
        'Rates retained from v1: $0.75/M input, $3.75/M answer plus thinking. '
        f'Responses missing usage: {missing}; API errors without usage: {len(errors)}. '
        'Only the v2 usage ledger is counted. Cache reuse adds no model tokens.', '',
        'Cross-arm organizations: `cross_arm_organizations.tsv`. Per-link reasons: `rejected_links.tsv`. '
        'Raw bodies and both texts: `fetch/`; selected texts: `texts/`; provenance: `audit.json`, `code_provenance.json`, and `policyie_source_audit.json`.', '',
        '## Resources', '',
        'CPU includes reaped descendants. Peak process RSS is the process high-water mark; tree RSS is sampled every 0.5 seconds. '
        'All workloads require Slurm. Per-step commands and measurements are in `metrics/v2_*.json`.', '']
    lines += markdown_table([dict(step=m['step'], job=m['slurm_job_id'],
        cpu=round(m['cpu_user_s']+m['cpu_system_s'], 3), elapsed=round(m['elapsed_s'], 3),
        process_mib=round(m['peak_process_rss_kib']/1024, 3), tree_mib=round(m['peak_tree_rss_bytes']/1048576, 3),
        exit=m['exit_code']) for m in metrics], [('step','Step'), ('job','Job'), ('cpu','CPU s'), ('elapsed','Elapsed s'),
        ('process_mib','Process MiB'), ('tree_mib','Tree MiB'), ('exit','Exit')])
    lines += ['<!-- REPORT_RESOURCE -->', '', '## Selected web policies', '', '`selected_web_policies.tsv`', '']
    lines += markdown_table(web, [('web_domain','Site'), ('size_proxy','Tranco rank'), ('home_final_url','Final homepage'),
        ('chosen_link_anchor_text','Anchor text'), ('chosen_link_url','Chosen link'), ('final_url','Final policy')])
    lines += ['', '## Duplicate registered-domain rejections', '', '`duplicate_registered_domains.tsv`; includes failed web links even if a later link was selected.', '']
    lines += markdown_table(duplicates, [('arm','Arm'), ('organization_name','Rejected organization'), ('final_url','Rejected final URL'),
        ('duplicate_organization_name','Selected organization'), ('duplicate_final_url','Selected final URL'), ('shared_domain','Shared domain')])
    lines += ['', '## Policy domain differs from organization domain', '',
        '`policy_domain_mismatches.tsv`; organization domain is the site, developerWebsite, or sellerUrl when present.', '']
    lines += markdown_table(mismatches, [('id','ID'), ('organization_name','Organization'), ('organization_domain','Organization domain'),
        ('final_registered_domain','Policy domain'), ('final_url','Final policy URL')])
    if not summary['selection_complete'] or not summary['audit_valid']:
        lines += ['', 'Incomplete status: `'+json.dumps(dict(state=state, failure=summary['failure']))+'`.', '']
    (OUT/'report.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k:summary[k] for k in ('selection_complete','audit_valid','funnels','endpoints',
        'maximum_pairwise_jaccard','maximum_policyie_containment','gemini')}, indent=2), flush=True)


if __name__ == '__main__':
    main()
