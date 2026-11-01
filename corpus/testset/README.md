# PolicyClaw evaluation-set selection

[DESIGN.md](DESIGN.md) is the specification. The revised entry point is
`run_revision.sbatch`. It uses the frozen app metadata, PrivaSeer snapshots,
Tranco list, stored responses, and verifier cache from the first run.

## Run the revision

Every workload, including self-checks, runs through Slurm with
`/scratch/yz5944/miniconda3/envs/llm/bin/python -B`. From the repository root:

```bash
sbatch corpus/testset/run_revision.sbatch
```

Or use the holder allocation, if it has sufficient memory:

```bash
srun --jobid=20291367 --overlap --nodes=1 --ntasks=1 --cpus-per-task=8 \
  --output=corpus/testset/logs/revision-holder-%J.log \
  bash corpus/testset/run_revision.sbatch
```

The job requests account `torch_pr_634_general`, partition `cs`, 8 CPUs, 64 GiB,
and 24 hours. It holds `.fetch.lock`, runs regression checks, then archives the
first selection before rebuilding any frame. The first-run source files are
already copied under `v1/code/`; selection outputs move during the archive step.
No first-run selection results are claimed as revision results.

Stages, in order:

1. `revision_selfcheck.py`: syntax and focused PSL, homepage, PolicyIE, duplicate,
   and ranked-turn regression checks.
2. `archive_revision.py`: move `selection.*`, `texts/`, `rejected.*`, report outputs,
   `audit.json`, `cross_arm_organizations.*`, and replaced frame/provenance outputs
   into `v1/`. SHA-256 manifests verify preservation and support interrupted moves.
3. `psl.py`: download one full PSL into `psl/public_suffix_list.dat`; pin download
   date, upstream version, and SHA-256 in `psl/manifest.json`.
4. `exclusions.py`: development domains and the six named PolicyIE tests; load
   every PolicyIE text directory in numeric filename order. OPP-115 is absent.
5. `rebuild_app_frames.py`, `web.py`: rebuild rankings with PSL identities. App
   organization keys and size proxies are unchanged. The frozen App Store metadata
   retains the first run's US-page recovery and supplied-link alignment.
6. `revision_select.py`: walk web, Android, Apple in turns until 200 each.
7. `revision_audit.py`: replay every decision offline and calculate exact maxima.
8. `revision_report.py`: write the report and review lists, including partial status
   if an earlier stage fails.

`measure.py` records CPU time, elapsed time, peak process RSS, and sampled process-tree
RSS for each stage in `metrics/v2_*.json`; prior measurements are retained. Slurm
logs are under `logs/`. An already completed revised selection is not overwritten.
An interrupted run can use the same command; fetches and successful verifier views
are reused. Verifier errors stop the current ranked turn rather than reject it.

## Selection rules and cache joins

`base.Domains` implements longest PSL matching, wildcards, exceptions, the default
`*` rule, IDNA lowercase hosts, and IP identities. Both ICANN and private sections
are used. Tranco is consulted only for the entry equal to the PSL registered domain.
A hostname consisting only of a public suffix retains that hostname as its identity.
There is no unresolved-domain rejection.

The web frame includes every PSL registered domain with a PrivaSeer URL and an
exact Tranco entry. The best available fastText score chooses metadata only;
missing scores do not exclude otherwise qualifying domains. `privaseer_url`,
`fasttext_score`, and original PrivaSeer text remain in the candidate table.

Each website starts at `https://<registered domain>/`, follows the shared crawler's
redirects, and examines final-page `a[href]` elements in document order. Anchor text
or href must contain `privacy`, ignoring case. Absolute URLs are deduplicated before
limiting to three. Each link is fetched and checked in order; the first fully eligible
link wins, including exclusion, domain, and text-duplicate checks.

Stored responses are joined by requested URL, never by a candidate's new rank.
New fetch IDs are SHA-256 URL identities. Verifier reuse matches the complete
rendered v1 prompt, model, rubric, and MEDIUM variant. The existing local/shared LLM
cache is preserved; shared-cache reads produce only local writes. New API usage is
recorded separately in `gemini_usage_v2.jsonl`, including returned retry responses.
Reported rates remain $0.75/M input and $3.75/M answer plus thinking, as in v1.
Missing usage and API failures are disclosed without assigning estimated tokens.

PolicyIE containment and policy-policy Jaccard use the same lowercase Unicode
`\w+` tokens and exact sets of consecutive five-word tuples. PolicyIE containment
is intersection divided by the PolicyIE set size; a value >=0.5 excludes a candidate.
Jaccard is intersection divided by union; a value >=0.5 duplicates a selected policy.
The final policy domain and, for a website, its site domain are reserved across arms.

## Outputs and review

- `selection.parquet`, `selection.tsv`, `texts/`: complete revised set; partial runs
  use `selection.partial.*`.
- `report.md`, `report.json`, `audit.json`: computed funnel, reasons, endpoints,
  overlap maxima, new verification usage/cost, resource measurements, and validation.
- `selected_web_policies.tsv`: all selected sites, Tranco ranks, final homepages,
  chosen anchors and links, and final policy URLs.
- `duplicate_registered_domains.tsv`: every domain-duplicate rejection, including
  failed web links, both organization names, both final URLs, and the shared domain.
- `policy_domain_mismatches.tsv`: selected policies whose final domain differs from
  the site, developerWebsite, or sellerUrl domain when present.
- `cross_arm_organizations.tsv`: the full cross-arm table, omitted from report prose.
- `rejected.*`, `rejected_links.*`, `selection_attempts.*`: organization decisions,
  per-link reasons, and every policy-link attempt.
- `verify.jsonl`: join `selection.verifier_id` to `id`;
  `fetch/<selection.fetch_id>.parquet` contains the retained response and texts.
- `v1/archive_manifest.json`: first-run output hashes and protected-file hashes.

The original entry points and their original semantics are preserved in `v1/code/`.
Use the revised entry point above. Do not run the original phase1 or audit scripts
against revised artifacts.

The implementation writes only inside `corpus/testset/`; source corpora remain
read-only. It does not read `.env` files or keys, change `policyclaw/`, or commit.
`DESIGN.md`, `pipeline_inputs.py`, and `run_pipeline.s` remain user-owned and unchanged.
