from collections import Counter
import json
from pathlib import Path

import pyarrow.parquet as pq

from base import ARMS, OUT, now, require_compute, write_json


def read_json(name, default=None):
    path = OUT/name
    return json.loads(path.read_text()) if path.exists() else default


def read_rows(name):
    path=OUT/name
    return pq.read_table(path).to_pylist() if path.exists() else []


def main():
    require_compute()
    frames={a:read_json(f'frame_{a}.json', {}) for a in ARMS}
    state=read_json('selection_state.json', {})
    audit=read_json('audit.json', {})
    selected=read_rows('selection.parquet') if state.get('complete') else read_rows('selection.partial.parquet')
    rejected=read_rows('rejected.parquet')
    verification=[]
    if (OUT/'verify.jsonl').exists():
        verification=[json.loads(line) for line in (OUT/'verify.jsonl').read_text().splitlines()]
    usage_rows=[]
    if (OUT/'gemini_usage.jsonl').exists():
        usage_rows=[json.loads(line) for line in (OUT/'gemini_usage.jsonl').read_text().splitlines()]
    token_fields={'input':'promptTokenCount', 'output':'candidatesTokenCount', 'thinking':'thoughtsTokenCount'}
    tokens={name:sum(r.get('usageMetadata', {}).get(field,0) for r in usage_rows) for name,field in token_fields.items()}
    cost=(tokens['input']*0.75+(tokens['output']+tokens['thinking'])*3.75)/1_000_000
    fetched=Counter(); reused=Counter(); http_ok=Counter(); long_text=Counter()
    fetch_rows=[]
    for path in sorted((OUT/'fetch').glob('*.parquet')):
        r=pq.read_table(path,columns=['arm','candidate_id','http_status','visible_chars','reused_from','error']).to_pylist()[0]
        fetch_rows.append(r); a=r['arm']; fetched[a]+=1; reused[a]+=bool(r['reused_from'])
        if r['http_status'] is not None and 200<=r['http_status']<300:
            http_ok[a]+=1; long_text[a]+=r['visible_chars']>=100
    counts=Counter(r['arm'] for r in selected)
    funnels={}
    endpoints={}
    for a in ARMS:
        group=[r for r in selected if r['arm']==a]
        decisions=[r for r in rejected if r.get('arm')==a and r.get('stage')=='selection']
        vf=[r for r in verification if r.get('source')==a or r['id'].startswith(a+'-')]
        reasons=Counter(r['reason'] for r in decisions)
        frame_count=frames[a].get('counts', {}).get('candidates')
        funnels[a]=dict(candidates=frame_count, fetched=fetched[a], reused=reused[a], fetched_now=fetched[a]-reused[a],
            http_2xx=http_ok[a], visible_at_least_100_chars=long_text[a], verified=len(vf),
            verifier_labels=dict(Counter(r.get('label','error') for r in vf)),
            verifier_complete_policy_english=sum(r.get('label')=='complete_policy' and r.get('flags',{}).get('language','').lower()=='en' for r in vf),
            considered=len(group)+len(decisions), selected=len(group), rejection_reasons=dict(reasons),
            frame_exclusions=frames[a].get('counts',{}).get('excluded_organizations'),
            not_walked=frame_count-len(group)-len(decisions) if frame_count is not None else None)
        if group:
            endpoints[a]={tag:{k:r.get(k) for k in ('id','rank','organization_key','organization_name','size_proxy','size_proxy_name','app_title','web_domain')}
                          for tag,r in [('first',group[0]),('last',group[-1])]}
    metrics=sorted((json.loads(p.read_text()) for p in (OUT/'metrics').glob('*.json')), key=lambda r:r['started_at'])
    tranco=read_json('tranco/manifest.json',{})
    exclusions=read_json('exclusions.json',{})
    cross=read_rows('cross_arm_organizations.parquet')
    limitations=[
        'No authoritative PolicyIE website list was found under vldb/analysis or data, or in the referenced sanitized dataset. PolicyIE domain exclusions remain incomplete; no website was guessed.',
        'The requested shared LLM_CACHE is read-only for this run. Matching entries are copied on demand; new cache entries are written under corpus/testset/llm_cache to satisfy the explicit write boundary.',
        'The specification does not define an identity when no final-URL suffix occurs in Tranco. Such candidates are rejected as unresolved_final_registered_domain because domain distinctness cannot be established with the specified rule.',
    ]
    legacy_extra=frames['apple'].get('counts',{}).get('recovered_top_apps_with_preexisting_legacy_pilot_us_page',0)
    if legacy_extra:
        limitations.append(f'{legacy_extra} top Apple apps were recovered despite an existing US pilot page. The initial pilot parser required a storefront column that the legacy files lack. The finalization step recovered pilot provenance from explicit /us/ URLs, restored those pilot links, and retained the newly fetched pages. The extra requests stayed within the one-attempt-per-second cap.')
    summary=dict(generated_at=now(), selection_complete=state.get('complete',False), audit_valid=audit.get('valid',False),
        exclusion_coverage_complete=False, tranco=tranco, frames=frames, funnels=funnels, endpoints=endpoints,
        maximum_pairwise_jaccard=audit.get('maximum_pairwise_jaccard'), maximum_pair=audit.get('maximum_pair'),
        maximum_pair_intersection=audit.get('maximum_pair_intersection'), maximum_pair_union=audit.get('maximum_pair_union'),
        cross_arm_registered_domains=audit.get('cross_arm_registered_domains'),
        cross_arm_domains_selected=audit.get('cross_arm_domains_selected'),
        gemini=dict(api_responses_with_usage=len(usage_rows), input_tokens=tokens['input'], output_tokens=tokens['output'],
            thinking_tokens=tokens['thinking'], billed_output_tokens=tokens['output']+tokens['thinking'],
            cost_usd=cost, input_usd_per_million=0.75, output_usd_per_million=3.75,
            cached_verifier_calls=sum(r.get('usage',{}).get('cached',0) for r in verification)),
        resources=metrics, limitations=limitations, selection_state=state, run_status=read_json('run_status.json'),
        last_failed_attempt=read_json('failure.json'))
    write_json(OUT/'report.json',summary)
    lines=['# PolicyClaw evaluation set: Phase 1', '', f'Generated: {summary["generated_at"]}.', '',
           ('**600-policy selection complete; artifact checks passed. PolicyIE exclusion coverage remains unverified.**'
            if state.get('complete') and audit.get('valid') else '**Incomplete run. No complete evaluation set is claimed.**'), '',
           f'Tranco date: `{tranco.get("date", "not downloaded")}`; list ID: `{tranco.get("list_id", "not downloaded")}`; rows: {tranco.get("rows", "not computed")}.', '',
           '## Frame sizes', '', '| Arm | Parsed US apps / PrivaSeer rows | Organizations before exclusions | Excluded organizations | Candidate organizations |',
           '|---|---:|---:|---:|---:|']
    for a in ARMS:
        c=frames[a].get('counts',{})
        n=c.get({'web':'privaseer_rows','android':'unique_us_apps','apple':'unique_us_lookup_apps'}[a],'not computed')
        lines.append(f'| {a} | {n} | {c.get("organizations_before_exclusions","not computed")} | {c.get("excluded_organizations","not computed")} | {c.get("candidates","not computed")} |')
    lines+=['', '| Arm | Frame-construction counter | Count |', '|---|---|---:|']
    for a in ARMS:
        c=frames[a].get('counts',{})
        for key,value in c.items():
            lines.append(f'| {a} | {key} | {value} |')
        if a in ('android','apple'):
            total=c.get('unique_us_apps' if a=='android' else 'unique_us_lookup_apps')
            linked=c.get('unique_apps_with_policy_url' if a=='android' else 'unique_apps_with_us_page_policy_url')
            if total is not None and linked is not None:
                lines.append(f'| {a} | US apps outside the policy-link frame | {total-linked} |')
    lines+=['', 'Apps outside the policy-link frame include missing policy links and, for Apple, app pages not present in the frozen crawl. They are frame omissions, not verifier rejections.']
    lines+=['', 'Web rows are collapsed to the latest crawl per URL before choosing the maximum-fastText-score URL per domain. Exact ties use latest timestamp, shortest URL, then lexical URL. App ties not specified by DESIGN use app ID for deterministic ordering. Android and Apple app tables retain every parsed US app, including apps without a policy link.', '',
        'Apple policy URLs use the supplied full and pilot link tables, with the full table taking priority. Recovered US app pages override those mappings; parsed existing US pages fill missing mappings using apple_policy_links. Recovery targeted the top 3,000 lookup apps lacking a US app_page row in the first-pass index; the two legacy-pilot exceptions are detailed below. All request attempts, including retries, use the crawler limiter capped at one per second.', '',
        'Every frame counter and every skipped shard is recorded in frame_web.json, frame_android.json, and frame_apple.json. Source snapshots record file size, mtime, schema, and row count. Shards younger than 120 seconds, changed during reading, or unreadable are skipped.', '',
        '## Funnel', '', '| Arm | Fetched | Reused | Fetched now | HTTP 2xx | Visible >=100 | Verified | Complete and English | Walked | Selected | Not walked |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for a,f in funnels.items():
        lines.append('| '+a+' | '+' | '.join(str(f[k]) for k in ('fetched','reused','fetched_now','http_2xx','visible_at_least_100_chars','verified','verifier_complete_policy_english','considered','selected','not_walked'))+' |')
    lines+=['', 'Batches may fetch and verify more candidates than the round-robin walk consumes. Those candidates are not rejections. At each turn, an arm consumes rejected candidates until it selects its next eligible organization; an unresolved fetched/verifier candidate blocks that turn.', '',
            '| Arm | Stage | Rejection reason | Count |','|---|---|---|---:|']
    for a,f in funnels.items():
        lines.append(f'| {a} | frame | development_domain | {f["frame_exclusions"]} |')
        for reason,n in sorted(f['rejection_reasons'].items()): lines.append(f'| {a} | selection | {reason} | {n} |')
    lines+=['', 'Every rejected organization and its reason is in rejected.parquet and rejected.tsv. Frame-level missing links and missing organization IDs are accounted for in the frame counters; they do not enter the ranked organization frame.', '',
            '## First and last selected organizations', '', '| Arm | Position | ID | Candidate rank | Organization | Size proxy | Value |','|---|---|---|---:|---|---|---:|']
    for a,ends in endpoints.items():
        for pos,r in ends.items():
            name=(r.get('organization_name') or '').replace('|','\\|').replace('\n',' ')
            lines.append(f'| {a} | {pos} | {r["id"]} | {r["rank"]} | {name} | {r["size_proxy_name"]} | {r["size_proxy"]} |')
    lines+=['', '## Duplicate audit', '']
    if audit.get('valid'):
        lines += [f'Exact maximum pairwise five-word-shingle Jaccard: **{audit["maximum_pair_intersection"]}/{audit["maximum_pair_union"]} = {audit["maximum_pairwise_jaccard"]:.12f}**, between `{audit["maximum_pair"][0]}` and `{audit["maximum_pair"][1]}`.', '',
                  f'All {audit["pairs_total"]} pairs are covered: {audit["pairs_intersected"]} exact intersections and {audit["pairs_proven_below_current_max_by_size_bound"]} pairs proven unable to exceed the current maximum by the exact set-size upper bound. The maximum is below 0.5.', '']
    else: lines += ['Maximum pairwise Jaccard: not computed for a complete 600-policy set.', '']
    lines += [r'Tokens are lowercase Unicode `\w+` words. Each shingle is an exact tuple of five consecutive words. The score is intersection size divided by union size. There is no approximate hashing or MinHash. Final-domain identity uses only the longest suffix found in the pinned Tranco list.', '',
        '## Verification tokens and cost', '',
        f'- Input tokens: {tokens["input"]}.', f'- Answer output tokens: {tokens["output"]}.',
        f'- Thinking tokens: {tokens["thinking"]}.', f'- Billed output tokens: {tokens["output"]+tokens["thinking"]}.',
        f'- Cost: **${cost:.8f}**, at $0.75/M input and $3.75/M output including thinking.',
        f'- API responses with observed usage: {len(usage_rows)}.',
        f'- Cached verifier calls in retained records: {summary["gemini"]["cached_verifier_calls"]}.', '',
        'Usage comes from Gemini usageMetadata for every returned API response, including output-budget retries. Cache hits incur no new model tokens. HTTP failures without usageMetadata have no token count available and are not assigned an estimated cost. The original verifier uses prompt v1, Gemini 3.8 Flash, MEDIUM thinking, and flags.language == en for English.', '',
        '## Exclusions and deviations', '']
    for line in limitations: lines.append('- '+line)
    lines += ['', f'Known exclusion domains under the fixed Tranco rule: {exclusions.get("unique_registered_domains","not computed")}.']
    for source,data in exclusions.get('sources',{}).items():
        lines.append(f'{source}: {data["hosts"]} distinct normalized hosts, {data["registered_domains"]} matched registered domains, {len(data["unmatched_hosts"])} unmatched hosts. Unmatched hosts are listed in exclusions.json; no public-suffix fallback is used.')
    development_audit=read_json('development_sites_audit.json')
    if development_audit:
        lines.extend(['', 'Development-site source audit (DESIGN states 291 sites): `'+json.dumps(development_audit,ensure_ascii=False)+'`. Both url and domain fields were scanned.'])
    lines+=['', 'The source function corpus/rebuild_versions.py also skips noscript, template, and svg, in addition to script and style. This implementation imports that function unchanged. PDF and plain-text rules come directly from corpus/stores/text.py. Source and prompt SHA-256 hashes are in code_provenance.json.', '',
            'No .env file or API key was read by this implementation. Existing gcloud authentication is used by policyclaw.auth. No source, manuscript, classifier, store-crawl, or Contextual-Integrity data was modified. No git commit was made.', '',
            '## Organizations present in more than one arm', '',
            'Cross-arm identity is the specified policy registered domain, including final-URL identities observed in fetched batches. It is not a guessed corporate-parent mapping. The full key/name membership is in cross_arm_organizations.tsv and .parquet. An empty winner means that no policy with that identity was selected.', '',
            f'Cross-arm domains: {audit.get("cross_arm_registered_domains","not computed")}; represented in the selection: {audit.get("cross_arm_domains_selected","not computed")}.', '',
            '<details>', '<summary>Full cross-arm identity list</summary>', '',
            '| Registered domain | Arms containing the identity | Selected arm | Selected ID |','|---|---|---|---|']
    for row in cross:
        lines.append(f'| {row["registered_domain"]} | {row["arms"]} | {row["selected_arm"] or "none"} | {row["selected_id"] or ""} |')
    lines+=['', '</details>', '', '## Resources', '',
        'Each stage runs on a Slurm compute node. CPU is user plus system time for the command and reaped descendants. Process RSS is the OS high-water mark for a process in the tree. Tree RSS is the sum of resident memory sampled every 0.5 seconds; shared pages can be counted more than once. Both are reported so multiprocessing memory is not mistaken for parent-only memory.', '',
        '| Step | Slurm job | CPU seconds | Elapsed seconds | Peak process RSS MiB | Peak sampled tree RSS MiB | Exit |',
        '|---|---|---:|---:|---:|---:|---:|']
    for m in metrics:
        lines.append(f'| {m["step"]} | {m["slurm_job_id"]} | {m["cpu_user_s"]+m["cpu_system_s"]:.3f} | {m["elapsed_s"]:.3f} | {m["peak_process_rss_kib"]/1024:.3f} | {m["peak_tree_rss_bytes"]/1048576:.3f} | {m["exit_code"]} |')
    lines+=['<!-- REPORT_RESOURCE -->', '',
            'Slurm submission initially had intermittent controller connection failures. Successful workloads used the holder allocation or submitted sbatch jobs from its compute shell. Failed controller requests did not run data workloads on the login node. Exact stage commands are retained in metrics/*.json; logs are under logs/.', '']
    if not state.get('complete'):
        lines += ['Current selection state: `'+json.dumps(state)+'`.', '', 'Last recorded failure: `'+json.dumps(read_json('failure.json'))+'`.', '']
    (OUT/'report.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ('selection_complete','audit_valid','funnels','endpoints','maximum_pairwise_jaccard','gemini')},indent=2), flush=True)


if __name__ == '__main__':
    main()
