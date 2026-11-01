# PolicyLint and PoliGraph contradictions on PoliGraph's test set

This directory holds the official PolicyLint and PoliGraph contradiction detectors run on the 200 policies of
`../baseline_corpus/` (s_test of the PoliCheck dataset, crawled 2023-03-28, numbered pg-001 to pg-200). Both tools
processed all 200 policies, and no policy failed. The outputs feed the blind precision comparison in `../compare/`.

## Outputs

| File | Content |
|---|---|
| `policylint/contradictions.csv` | One row per PolicyLint contradiction (105 rows), normalized. |
| `policylint/policylint_results.csv` | PolicyLint's contradiction export with the official header (123 rows). |
| `policylint/official_ext/` | Official PolicyLint outputs: `output/db/consistency_results_1.db` (raw result database), `output/policy/` and `output/analytics/` (per-policy extraction pickles), `output/log_data/`, the partial `combined_tables/`, `datasets/`, `input/`, and the `Skipped*.log` files. |
| `policylint/summary.json` | PolicyLint counts and cross-check results. |
| `poligraph/contradictions.csv` | Official output of `get-poligraph-contradictions.py`, as written (112 rows). |
| `poligraph/contradictions_normalized.csv` | The same 112 rows with policy_id, positive_sentence, negative_sentence, and the official fields. |
| `poligraph/policylint_reclassified.csv` | Official output of `reclassify-policylint-contradictions.py` (35 rows). |
| `poligraph/summary.json` | PoliGraph counts. |
| `scripts/` | Every script and Slurm file used. |
| `work/` | Staged code, containers, inputs, PoliGraph work directories (documents and graphs), and logs. |

## Software

| Component | Version |
|---|---|
| PolicyLint | `PrivacyPolicyAnalysis` commit `6c0c16300118ee17547ad7b9ecaf047aa674f463`, `DockerImage/code` and `ext/data` copied unchanged (verified with `diff -r`) to `work/policylint/`, with the pretrained `ext/NlpFinalModel`. `run_config` is `policylint`. |
| PolicyLint runtime | Apptainer 1.5.3 running `docker://python:2.7` (digest `sha256:cfa62318c459b1fde9e0841c619906d15ada5910d625176e24bf692cf8a2601d`, `work/containers/python_2.7.sif`) with a copy of the earlier run's package overlay (`work/containers/policylint_py27_fakeroot_overlay_v2.img`, mounted read-only): Python 2.7.18, spaCy 2.0.12, networkx 2.2, pandas 0.24.2, numpy 1.16.6, dill 0.2.9, lxml 5.0.2, enum34. |
| PoliGraph | Commit `e93771156e223f902c3e5f42ea8d877d8fb239ef`, copied with its extra-data models to `work/PoliGraph` (`git status` clean, extra-data identical by `diff -r`). Imported through `PYTHONPATH`. |
| PoliGraph runtime | Conda env `/scratch/yz5944/miniconda3/envs/poligraph`: Python 3.10, spaCy 3.5.3, en_core_web_trf 3.5.0, torch 1.12.1, rapidfuzz 3.0.0. Run on CPU. |

The files under `/scratch/yz5944/nlp+privacy/Contextual-Integrity` were only read. No working-tree file there changed. The
only side effect was `git log`/`git status` updating the mtime of the two `.git` directories.

## Inputs

- PolicyLint read `work/policylint/ext/plaintext_policies/pg-NNN.txt`, byte-identical copies of
  `../baseline_corpus/plaintext_policies/` (verified with `diff -r`).
- PoliGraph read `work/poligraph/workdirs/pg-NNN/`, made by `scripts/stage_poligraph_workdirs.py`. It copies
  `cleaned.html`, `accessibility_tree.json`, and `readability.json` from each `policy_dirs/pg-NNN` and checks that the
  Blake2s hash of `cleaned.html` equals the manifest hash (the PoliCheck dedup directory name) and that `cleaned.html`
  equals `html_policies/pg-NNN.html`. All 200 checks passed (`work/poligraph/staged_workdirs.csv` lists the SHA-256 of
  every copied file). PoliGraph names a policy by its directory basename, so the copies are named pg-NNN. Passing the
  `policy_dirs` symlinks would have named each policy by its PoliCheck hash.

## PolicyLint

### Commands (`scripts/run_policylint.sbatch`, job 20568677)

```bash
mkdir -p work/policylint/ext/output/log
apptainer exec --fakeroot --overlay work/containers/policylint_py27_fakeroot_overlay_v2.img:ro --no-mount bind-paths \
  --bind work/policylint/code:/src --bind work/policylint/ext:/ext work/containers/python_2.7.sif \
  bash -c 'cd /src && ./main.sh'
# cross-check: the official postprocessor on a copy of the result database, with Python 2's default codec set to UTF-8
APPTAINERENV_PYTHONPATH=/utf8site apptainer exec ... --bind work/policylint/ext_utf8check:/ext \
  --bind work/policylint/utf8_site:/utf8site work/containers/python_2.7.sif \
  bash -c 'cd /src && python2 RemoveSameSentenceContradictions.py 1'
python3 -I scripts/policylint_postprocess.py
```

`main.sh` is the official entry point. It runs `PatternExtractionNotebook.py 1` (policy extraction),
`ConsistencyAnalysis.py 1` (contradiction analysis), `RemoveSameSentenceContradictions.py 1` (postprocessing), and
`DisclosureClassification.py` (PoliCheck flow classification). Log: `work/logs/policylint_main_20568677.log`.

### Resources

| Step | Elapsed | CPU time | Peak memory |
|---|---|---|---|
| Job 20568677 (`cs`, 8 CPUs, 32 GB requested) | 19:09 | 1:35:52 | 3.08 GiB (sacct MaxRSS) |
| `main.sh` (timev) | 18:56 | 2,237 s user + 3,512 s system | 1.95 GB (largest process) |
| Python 3 postprocessing (timev) | 0.17 s | 0.04 s | 18 MB |

### Policies processed and failed

- Extraction parsed all 200 policies and wrote 200 policy pickles. No sentence raised the RuntimeError that the
  extractor logs and skips (`output/log/` is empty).
- Contradiction analysis loaded all 200 policies ("Starting" 200 times in `output/log_data/1.log`). 132 policies
  produced at least one policy statement (526 sentence rows in `AppPolicySentences`).
- All 200 policies are listed in `SkippedAppsNoFlows_1.log`. This affects only PoliCheck's flow analysis, because
  `flows.csv` holds the PoliCheck apps' network flows, keyed by Android package name.
- `RemoveSameSentenceContradictions.py` stopped with `UnicodeEncodeError: 'ascii' codec can't encode character
  u'™'` while dumping `AppPolicySentences` to `combined_tables/PolicySentences.csv`, before it wrote
  `policylint_results.csv`. `DisclosureClassification.py` then stopped because the CSV tables it reads were missing.
  The second failure has no effect on contradictions.

### Contradictions

| Type | Rows in `policylint_results.csv` | Contradictions in `contradictions.csv` |
|---|---:|---:|
| C1 | 36 | 18 |
| C2 | 5 | 5 |
| C3 | 15 | 15 |
| C4 | 42 | 42 |
| C5 | 0 | 0 |
| C6 | 2 | 2 |
| C7 | 4 | 4 |
| N1 | 8 | 8 |
| N2 | 11 | 11 |
| N3, N4 | 0 | 0 |
| Total | 123 | 105 |

The 105 contradictions come from 28 policies. The result database holds 123 Contradiction rows. The same-sentence
filter removed none of them, so all 123 reach `policylint_results.csv`.

C6 and C7 are labels from PolicyLint's own label map (`contradictionMap` in `RemoveSameSentenceContradictions.py`). They
belong to `checkContradiction4` and `checkContradiction8` in `Consistency.py`, where the two data terms are
semantically approximate in the data ontology (`isApprox`) and the entities are equal (C6) or the positive entity is
subsumed under the negative one (C7). The PolicyLint paper's nine types (C1 to C5, N1 to N4) do not include them. All
six rows are in pg-153 (5) and pg-183 (1). `../compare/make_pool.py` keeps types starting with "C", so it includes them.

### Postprocessing

`scripts/policylint_postprocess.py` imports `policylint_rows` unchanged from
`experiments/frozen_e0/e3_shared_input/hpc/e3_hpc.py` (the Python 3 UTF-8 port used for E3). The port reads the
Contradiction, Policy, and AppPolicySentences tables directly from the result database and applies the official
contradiction label map and the official filter, which drops a contradiction when either side has no sentence, both
sides have the same sentences, or one side's sentences are a subset of the other's. It writes
`policylint/policylint_results.csv` with the official header.

Cross-check: the unchanged official `RemoveSameSentenceContradictions.py`, run on a copy of the database with Python 2's
default codec set to UTF-8 (`work/policylint/utf8_site/sitecustomize.py`), finished and wrote 123 rows. They equal the
port's 123 rows field by field, with each side's sentences compared as a set (`checks` in `policylint/summary.json`).

### Normalization (`policylint/contradictions.csv`)

- `positive_*` is the statement whose action is `collect`, and `negative_*` the `not_collect` statement.
- `positive_sentence` and `negative_sentence` are PolicyLint's sentence texts for each side (the official
  `policySentences` and `contradictionSentences`, split at `||`), joined with a newline. All are verbatim substrings of
  the plaintext policy. 19 of 105 contradictions have more than one sentence on a side (`n_positive_sentences`,
  `n_negative_sentences`).
- PolicyLint checks every ordered pair of statements, and only the C1 test is symmetric, so every C1 contradiction
  appears twice, as (A,B) and (B,A). Rows with the same policy, type, positive tuple, and negative tuple are merged, as
  PoliGraph's reclassifier does. `results_rows` lists the merged data rows of `policylint_results.csv`.

## PoliGraph

### Commands

`scripts/run_poligraph.sbatch` (job array 20568679, tasks 0 to 3) runs `scripts/poligraph_shard.py SHARD 4`. Each shard
calls the official modules once on its 50 work directories, in this order:

```bash
python -m poligrapher.scripts.init_document  DIRS...
python -m poligrapher.scripts.run_annotators DIRS...
python -m poligrapher.scripts.build_graph --variant extended DIRS...
```

Policies are sorted by plaintext size and dealt round-robin to the shards (`work/poligraph/shards/shard_NN/status.json`
lists each shard's policies). The wrapper would have restarted a step after a failing policy, but no step failed, so
each module ran once per shard. Logs: `work/poligraph/shards/shard_NN/*.log`.

`scripts/run_poligraph_contradictions.sbatch` (job 20568866, started after both runs) then runs:

```bash
for d in work/poligraph/workdirs/pg-*; do ln -sfn graph-extended.yml "$d/graph.yml"; done
python work/PoliGraph/analyses/contradictions/get-poligraph-contradictions.py \
  -o poligraph/contradictions.csv work/poligraph/workdirs/pg-001 ... pg-200
python work/PoliGraph/analyses/contradictions/reclassify-policylint-contradictions.py \
  -r policylint -o poligraph/policylint_reclassified.csv work/poligraph/workdirs/pg-001 ... pg-200
python scripts/poligraph_finish.py normalize
```

### Resources

| Step | Elapsed | CPU time | Peak memory |
|---|---|---|---|
| Shard 0, job 20568679_0 (`cs`, 8 CPUs, 64 GB requested) | 7:05 | 40:21 | 4.20 GiB |
| Shard 1, job 20568679_1 | 7:17 | 42:01 | 4.20 GiB |
| Shard 2, job 20568679_2 | 8:19 | 49:16 | 4.89 GiB |
| Shard 3, job 20568679_3 | 8:17 | 47:38 | 4.19 GiB |
| `init_document`, per shard (timev) | 5:34, 5:48, 6:41, 6:29 | 2,292 to 2,827 s | 3.1 to 4.1 GB |
| `run_annotators`, per shard | 0:39 to 0:45 | 29 to 33 s | 3.1 GB |
| `build_graph --variant extended`, per shard | 0:49 to 1:03 | 92 to 116 s | 3.3 GB |
| Job 20568866 (`cs`, 4 CPUs, 16 GB requested) | 0:47 | 7.5 s | 0.49 GiB |
| `get-poligraph-contradictions.py` | 11.0 s | 2.0 s | 0.31 GB |
| `reclassify-policylint-contradictions.py` | 8.6 s | 1.8 s | 0.31 GB |

Times are from sacct and from `timev.py` logs (`*.time` next to each log). CPU time is user plus system.

### Policies processed and failed

All 200 policies completed `init_document`, `run_annotators`, and `build_graph --variant extended`, and all 200
extended graphs entered both analyses. No policy failed.

### Contradictions

- `get-poligraph-contradictions.py` reported 112 rows (conflicting positive and negative edges) in 47 policies. The
  rows contain 95 distinct (policy, positive text, negative text) combinations, because several edge pairs can rest on
  the same sentences.
- The reclassifier considered 86 unique PolicyLint tuples of types C1 to C7 (it keeps rows whose type starts with "C"
  and merges the two orders). It mapped 32 of them to PoliGraph edges in 17 policies and wrote 35 rows. It printed the
  other 54 as unmapped. Labels per row: DIFF_ACTIONS 20, ONTOLOGY 7, DIFF_PURPOSES 5, DIFF_ACTIONS with DIFF_PURPOSES
  2, CONFLICT 1 (pg-048, third party / pii), INVALID 0.

### Normalization (`poligraph/contradictions_normalized.csv`)

- Every official row is kept in order (`official_row`), with the official fields `app_id`, `pos_edge`, `neg_edge`,
  `pos_text`, `neg_text`, and `policy_id` = `app_id`.
- `positive_sentence` and `negative_sentence` are the edge texts from `graph-extended.yml`. Each official `pos_edge` and
  `neg_edge` string was matched to the one graph edge that formats to it, and `"\n".join` of that edge's texts equals the
  official `pos_text`/`neg_text` for all 112 rows. Each text is stripped of surrounding whitespace, a text repeated with
  a leading newline is dropped, and the texts are joined with a newline. 45 of 112 rows have more than one text on a
  side.
- PoliGraph's texts are its own sentence texts, not verbatim policy text. Its `SegmentExtractor` applies `unidecode`
  (for example, the mojibake `donâ€™t` in the visible text becomes `donaEUR(tm)t`), rewrites a few spellings (e-mail to
  email, wi-fi to WiFi, id to ID), prefixes a list item with its heading, and joins some list lead-ins and items with
  `: `. To show reviewers the policy's own words, `positive_sentence_visible` and `negative_sentence_visible` give the
  span of the visible text (`plaintext_policies/pg-NNN.txt`) that each text came from, and `*_visible_match` records
  how each was found (exact, exact_lines, fuzzy:score, none; see `scripts/poligraph_finish.py`). Of the 360 text
  occurrences in the 112 rows, 314 were found whole, 11 line by line, 2 by fuzzy match, and 33 were not found. The 33
  are 18 distinct texts (pg-092: 12, pg-113: 5, pg-130: 1), mostly list lead-ins joined to an item with `: `. In 57 of
  112 rows, at least one side's PoliGraph text differs from the visible text or was not located.

## Deviations from the official pipelines

1. PolicyLint ran in Apptainer, because Docker is not available on the cluster. The image is `python:2.7`, the
   Dockerfile's base, plus the overlay of packages built for the earlier run. The Dockerfile installs spaCy 2.0.12 and
   unpinned `networkx`, `lxml`, `pandas`, and `enum34`. The overlay has spaCy 2.0.12 and pinned Python 2 versions of
   the others (listed under Software). The Dockerfile also downloads spaCy's `en` and `en_core_web_lg` models. They are not installed, because the code loads
   only `/ext/NlpFinalModel` (`spacy.load` appears only with that path).
2. `/ext/output/log/` was created before `main.sh`. The extractor writes sentences that raise RuntimeError there, but
   `main.sh` never creates the directory, so the first such sentence would have stopped extraction for all later
   policies. No sentence raised RuntimeError, so the directory stayed empty and the step had no effect.
3. PolicyLint's postprocessing (`RemoveSameSentenceContradictions.py`) stopped on non-ASCII text. Its contradiction export
   was produced by the Python 3 UTF-8 port reused from E3. The port joins multiple sentences in sorted order (the
   official script joins a Python 2 set in arbitrary order) and reads the database directly instead of through pandas.
   The official script, run with UTF-8 as Python 2's default codec, produced the same 123 rows.
4. PoliCheck's `DisclosureClassification.py` failed after the postprocessing failure. It classifies data flows, and no
   policy had flows, so it does not affect contradictions.
5. PoliGraph ran on CPU. Its README recommends a GPU for speed and says it can run without one. `spacy.prefer_gpu()`
   returned False, so all models ran on CPU.
6. `get-poligraph-contradictions.py` reads `graph.yml`, but `build_graph --variant extended` writes
   `graph-extended.yml`. The script's file name predates commit 286d2b6, which renamed the variant outputs, and
   PoliGraph's artifact guide (experiment E4) defines the contradiction analysis on the extended graph. Each work
   directory therefore has `graph.yml` as a symlink to `graph-extended.yml`. The reclassifier reads
   `graph-extended.yml` itself.
7. The reclassifier read `policylint/policylint_results.csv` from deviation 3, because the official file was not
   produced.
8. Each shard passed its 50 directories to one call of each official module instead of all 200 to one call. The
   modules process directories independently, so the outputs do not depend on the grouping.

The normalized tables add columns and merge PolicyLint's C1 duplicates (described above). The official files are kept
unchanged next to them.

## Notes for the blind comparison

- Six PolicyLint contradictions have types C6 or C7, outside the paper's C1 to C5. `make_pool.py` includes them.
- Sides with several sentences are joined with a newline: 19 of 105 PolicyLint rows and 45 of 112 PoliGraph rows.
  `make_pool.py` searches for the whole joined string in the policy text, so these statements will often appear without
  context.
- PoliGraph's `positive_sentence`/`negative_sentence` carry `unidecode` and rewrite artifacts in 57 of 112 rows. A
  reviewer can recognize them, and `make_pool.py` will not find them in the policy text. The `*_sentence_visible`
  columns give the policy's own words where the text was located.

## Other jobs

Holder job 20568027 (`cs`, 4 CPUs, 16 GB) ran the short steps: copying the official code, models, and overlay into
`work/`, pulling the `python:2.7` image, testing the container and the PoliGraph steps on two copied policies (in a
scratch directory, not in `work/`), staging the work directories, and auditing the outputs.
