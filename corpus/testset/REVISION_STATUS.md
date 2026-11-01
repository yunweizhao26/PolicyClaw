# Revision status: prepared; execution blocked

The revised implementation and Slurm entry point are written. No revised selection
or validation result has been produced in this session. Existing `report.md`,
`report.json`, `selection.*`, and `audit.json` still describe the first run.

Slurm access attempts:

- Holder `20291367`: `Unable to contact slurm controller (connect failure)`;
  command exited 124 under its timeout.
- Holder regression-check step: timed out and was killed (exit 137); no execution
  log or `metrics/v2_selfcheck.json` appeared.
- `sbatch --parsable corpus/testset/run_revision.sbatch`: timed out (exit 124),
  without returning a job ID.
- Queue check for job name `testset-v2`: timed out (exit 124). Submission state
  could not be independently confirmed; check for an existing job before resubmission.

No Python or data workload was run on the login node. No new Gemini calls or
tokens were observed; no new verification cost was incurred by confirmed work.
No revision resource measurements are available.

The first-run source files and README are copied under `v1/code/`. Moving the
selection outputs into `v1/` is implemented as the measured archive stage and has
not run. It precedes every frame rebuild. Fetches and LLM caches stay in place.
The PSL download, exclusion rebuild, frame rebuild, selection, regression checks,
artifact audit, and report generation remain pending.

From the repository root, inspect any pending submission, then run:

```bash
squeue --user=yz5944 --name=testset-v2
sbatch corpus/testset/run_revision.sbatch
```

The holder alternative and stage descriptions are in [README.md](README.md).

For all three arms, revised funnel counts and rejection counts, first/last selected
organizations and size proxies are **not computed**. Maximum Jaccard and maximum
PolicyIE containment are **not computed**. No first-run number is substituted.

The revised report will include the three requested lists and create these TSVs:

- `corpus/testset/selected_web_policies.tsv`
- `corpus/testset/duplicate_registered_domains.tsv`
- `corpus/testset/policy_domain_mismatches.tsv`

The complete organization overlap table will be in
`corpus/testset/cross_arm_organizations.tsv`, outside the report prose. Per-link
rejection evidence will be in `corpus/testset/rejected_links.tsv`.

`DESIGN.md`, `pipeline_inputs.py`, `run_pipeline.s`, `policyclaw/`, and source corpora
remain unchanged. No `.env` files or keys were read. No git commit was made.
