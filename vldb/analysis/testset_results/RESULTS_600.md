# Corpus statistics on the 600-policy test set (draft)

Every number below comes from a script in the repository and the JSON file it writes. The scripts make no model calls. They are the scripts of `vldb/analysis/corpus_results/` run with `--set testset`. Run everything with `sbatch vldb/analysis/testset_results/run_all.s` (about 11 minutes on 8 CPUs). The values here are from job 20734572. The tables are written by `make_results_md.py` from the JSON files, so each value is read from the output and not typed.

| Script | Output (in `out/`) | What it computes |
|---|---|---|
| `corpus_results/rules.py --set testset` | `rules.json` | rule counts and shares per scope, operations, translation, rejected records, rules per policy, model usage from the reports |
| `corpus_results/pairs.py --set testset` | `pairs.json`, `pair_records.jsonl` | opposing pairs, solver outcomes, decision-procedure relations, size deciles, guard placement, ablation, solver time |
| `corpus_results/queries.py --set testset --terms on` | `queries.json` | redundancy (with the policy's term relations), coverage, compliance |
| `corpus_results/queries.py --set testset --terms off` | `queries_no_terms.json` | the same with names compared as names, as for the corpus |
| `reconcile_pairs.py` | `reconcile_pairs.json` | pairs against `corpus/testset/eval/conflict_pairs.jsonl` |
| `figures.py` | `figures.json` | data of figure 1 (panels a to d) and figure 2 |
| `make_results_md.py` | `RESULTS_600.md` | this file |
| `compare_outputs.py` | | compares two output folders of the corpus scripts, ignoring run records and timing |

## Definitions

**Policies and rule sets.** The test set holds 600 policies: 200 websites (id prefix `web-`), 200 Google Play apps (`android-`), and 200 App Store apps (`apple-`), one snapshot each (`corpus/testset/DESIGN.md`). A policy is one version of one page. Its rule set is `corpus/testset/rules/<id>.jsonl`, produced by Gemini 3.8 Flash at low thinking in one pass. There is no reconciliation and no history, so every statistic that needs versions is marked "needs versions" and every statistic that needs human labels is marked "needs labels".

**Scopes.** "All 600" is the union. An arm is its 200 policies. The JSON files call the scopes `all`, `web`, `android` (Google Play), and `apple` (App Store). JSON keys that say `versions` (such as `versions_with_a_pair`) count policies.

**Definitions reused unchanged.** Rules, pairs (one compiled rule per extraction record, ALLOW against DENY of the same practice by `policyclaw.merge._same_practice`, lenient), outcomes (`policyclaw.queries.pair_outcome`), relations (the decision procedure's clash rules), deciles, guard placement, ablation, and solver time are as in `corpus_results/RESULTS_DRAFT.md`. The pairing vocabulary is the action network only, as in `conflict_pairs.py`.

**One change of definition.** Redundancy (`queries.py`) compared data names as names on the corpus, because no data relations existed. The test set has per-policy term relations (`rules/<id>.terms.json`, one model call per slot and policy, `policyclaw.terms`), so the main redundancy figures extend the vocabulary with them, as `policyclaw.conflicts.vocabulary` does. The rows marked "names only" use the corpus definition. Coverage and compliance do not use the term relations and are identical in both runs except two counts (policies that permit a sale: 225 against 226; unconditional disclosure rules: 10,629 against 10,634), which change when an alias merges a data name with an action name (one vocabulary namespace for all slots, see the note at the end).

**Old values** are those of `RESULTS_DRAFT.md` (the paper): E0 (an open-weight model, regex guard mapper) on 3,678 versions of 273 timelines.

## Rules (RQ2)

| Paper row | Claim | Old value | All 600 | Web | Google Play | App Store | Script and output | Note |
|---|---|---|---|---|---|---|---|---|
| abstract:2, intro:18, 7.2:16 | extracted rules | 112,768 | 146,861 | 49,823 | 38,230 | 58,808 | `rules.py`: `policies.*.counts.rules` | 117,462 extraction records over all 600 (a record with several purposes compiles to one rule per purpose). Equals the pipeline run's total of 146,861 (`eval/system_stats.tsv`). |
| 7.2:18 | ALLOW and DENY rules | 100,895 and 11,873 | 138,341 (94.2%) and 8,520 (5.8%) | 46,920 (94.2%) and 2,903 (5.8%) | 35,790 (93.6%) and 2,440 (6.4%) | 55,631 (94.6%) and 3,177 (5.4%) | `rules.py`: `polarity ALLOW`, `polarity DENY` |  |
| 7.2:18 | rules with explicit conditions | 45,265 (40.1%) | 94,365 (64.3%) with a condition or exception quote; 91,145 (62.1%) whose guard is not true | 31,667 (63.6%) with a condition or exception quote; 30,589 (61.4%) whose guard is not true | 25,511 (66.7%) with a condition or exception quote; 24,805 (64.9%) whose guard is not true | 37,187 (63.2%) with a condition or exception quote; 35,751 (60.8%) whose guard is not true | `rules.py`: `with conditions or exceptions`, `guard not true` | Same definitions as the corpus run. |
| 7.2:18 | rules with a recipient | 24.1% | 26,467 (18.0%) | 8,621 (17.3%) | 5,973 (15.6%) | 11,873 (20.2%) | `rules.py`: `with recipient` |  |
| 7.2:62 to 67 | any ambiguity flag | 21,684 (19.2%) | no counterpart | no counterpart | no counterpart | no counterpart |  | The old flags came from the regex guard mapper. The three rows below are the closest measures (figure 1d). |
| 7.2:63 | condition has no extracted predicate | 13,039 (11.6%) | 34,548 (23.5%) with an untranslated quote in the guard; 16,157 (11.0%) with only untranslated quotes | 11,785 (23.7%) with an untranslated quote in the guard; 5,521 (11.1%) with only untranslated quotes | 9,389 (24.6%) with an untranslated quote in the guard; 4,160 (10.9%) with only untranslated quotes | 13,374 (22.7%) with an untranslated quote in the guard; 6,476 (11.0%) with only untranslated quotes | `rules.py`: `guard with a residual`, `guard only residuals` |  |
| 7.2:64, 7.2:72 | condition points elsewhere, cross-reference flag | 2,943 (2.6%), 6.0% | 29,779 (20.3%): law 14,267, policy section 11,579, other document 6,807 | 10,822 (21.7%): law 5,473, policy section 4,074, other document 2,297 | 7,460 (19.5%): law 3,782, policy section 2,472, other document 1,845 | 11,497 (19.6%): law 5,012, policy section 5,033, other document 2,665 | `rules.py`: `with references`, `with a reference to *` | A rule with several reference targets counts under each target. The extractor assigns the target. |
| 7.2:66 | missing or implicit counterparty | 5,061 (4.5%) | 7,944 disclosure rules without a recipient (5.4% of rules, 24.2% of 32,868 disclosure rules) | 2,403 disclosure rules without a recipient (4.8% of rules, 22.9% of 10,516 disclosure rules) | 2,008 disclosure rules without a recipient (5.3% of rules, 26.5% of 7,571 disclosure rules) | 3,533 disclosure rules without a recipient (6.0% of rules, 23.9% of 14,781 disclosure rules) | `rules.py`: `disclosure without recipient`, `disclosure` | A disclosure rule's action lies under the operation "disclosure" in the action network. |
| 7.2:16 | share of raw extractions removed by the filter | 21.9% | 6,740 of 124,202 records rejected (5.4%) | 2,127 of 42,189 records rejected (5.0%) | 1,686 of 32,853 records rejected (5.1%) | 2,927 of 49,160 records rejected (6.0%) | `rules.py`: `report rejected`, `report raw_rules`, `shares_pct["rejected of extracted records"]` | Reasons over all 600: missing polarity, action, or data 2,046, operation not in the schema 1,289, quote not in section 3,405. |
| (new) | qualifier quotes translated to formulas | none | 39,428 of 53,095 (74.3%) | 13,715 of 19,014 (72.1%) | 10,878 of 14,505 (75.0%) | 14,835 of 19,576 (75.8%) | `rules.py`: `report quotes`, `report residual_quotes` | Distinct quotes per section, from the per-policy reports. |
| (new) | unsatisfiable guards, qualifiers without effect | none | 328 and 6,286 | 79 and 1,590 | 118 and 2,052 | 131 and 2,644 | `rules.py`: `report unsatisfiable_guards`, `report qualifiers_without_effect` | Deletion test in `policyclaw/extract.py`. |
| fig 1a | rules per policy: median (quartiles), maximum | histogram only | 197 (121 to 301), 5,748 | 193 (123 to 301), 5,748 | 159.5 (90 to 245), 1,215 | 242.5 (159 to 339), 2,906 | `rules.py`: `policies.*.rules_per_policy` | Quartiles are nearest-rank (`common.quantile`). Minimum 7, 10, 7, 21 (all, web, Google Play, App Store); mean 244.8, 249.1, 191.2, 294.0. |
| (new) | model calls and tokens of the extraction (from the reports) | none | 19,748 calls, 35.3M prompt and 24.0M completion tokens | 6,997 calls, 12.8M prompt and 8.5M completion tokens | 5,526 calls, 9.6M prompt and 6.4M completion tokens | 7,225 calls, 12.9M prompt and 9.1M completion tokens | `rules.py`: `usage *` | Read from the stored reports, not a new model call. 3 failed calls remain in the final reports (the three App Store policies kept with `--accept-failed`, FINDINGS §30). |

## Opposing pairs and solver outcomes (abstract, RQ2, RQ4)

| Paper row | Claim | Old value | All 600 | Web | Google Play | App Store | Script and output | Note |
|---|---|---|---|---|---|---|---|---|
| abstract:2, intro:18, 7.2:10, 7.2:21 | opposing pairs | 2,232 | 17,918 | 7,027 | 3,663 | 7,228 | `pairs.py`: `*.pairs` | `corpus/testset/eval/conflict_pairs.jsonl` holds 17,918 pairs and `pair_records.jsonl` holds 17,918. The two files have the same pairs, and every field of every pair is equal (`reconcile_pairs.json`: only_now 0, only_before 0, differing fields 0). `conflict_pairs.py` calls the same `pairs.unit_pairs`, so no difference is expected. |
| abstract:2, intro:18, 7.2:21 | overlap candidates | 424 | 9,296 (51.9%) | 3,156 (44.9%) | 1,836 (50.1%) | 4,304 (59.5%) | `pairs.py`: `*.outcomes` |  |
| abstract:2, intro:18, 7.2:21 | mutually exclusive | 26 | 1,043 (5.8%) | 399 (5.7%) | 255 (7.0%) | 389 (5.4%) | `pairs.py`: `*.outcomes` | Policy exceptions (the prohibition uses `policy.permits`): 666, 280, 137, 249; exclusive guards: 377, 119, 118, 140 (all, web, Google Play, App Store). |
| abstract:2, intro:18, 7.2:21 | unresolved | 1,782 | 7,579 (42.3%) | 3,472 (49.4%) | 1,572 (42.9%) | 2,535 (35.1%) | `pairs.py`: `*.outcomes.unresolved` |  |
| abstract:2 | unresolved share | 79.8% | 42.3% | 49.41% | 42.92% | 35.07% | `pairs.py`: `*.outcome_shares_pct.unresolved` |  |
| abstract:2, intro:18, 7.2:21, 7.2:76 | pairs with a solver result (decided share) | 450 (20.2%) | 10,339 (57.7%) | 3,555 (50.6%) | 2,091 (57.1%) | 4,693 (64.9%) | `pairs.py`: `*.decided_share_pct` | Overlap candidates plus mutually exclusive pairs. |
| 7.2:29 to 38 | Table e0_outcomes: unresolved with partly translated guards | 811 (36.3%) semantic | 2,992 (16.7%) | 1,134 (16.1%) | 611 (16.7%) | 1,247 (17.3%) | `pairs.py`: `*.outcomes.unresolved` minus `unresolved_blocking.a_guard_entirely_untranslated` | The old "semantic" class had a usable extracted condition. |
| 7.2:29 to 38 | Table e0_outcomes: unresolved with a guard that is only untranslated quotes | 971 (43.5%) pipeline | 4,587 (25.6%) | 2,338 (33.3%) | 961 (26.2%) | 1,288 (17.8%) | `pairs.py`: `*.unresolved_blocking.a_guard_entirely_untranslated` | Also the row "pairs without a usable extracted condition" (discussion:12, old 971). |
| (new) | unresolved pairs blocked by residuals in the permission, the prohibition, both | none | 2264, 3741, 1574 | 815, 1827, 830 | 445, 791, 336 | 1004, 1123, 408 | `pairs.py`: `*.unresolved_blocking.blocking_in` | Every unresolved pair has a blocking residual by definition (check passes). Median blocking residuals per pair: 1. |
| 7.2:23 | policies without a pair, with a pair, with an overlap candidate | 2,927, 751, 314 (versions) | 85, 515, 451 | 24, 176, 149 | 44, 156, 138 | 17, 183, 164 | `pairs.py`: `*.versions_with_a_pair`, `*.versions_with` | Policies of the scope: 600, 200, 200, 200. Every policy has rules. |
| 7.3:15 | policies with a pair, overlap, mutually exclusive, unresolved | 751, 314, 8, 614 | 515, 451, 178, 444 | 176, 149, 58, 149 | 156, 138, 60, 133 | 183, 164, 60, 162 | `pairs.py`: `*.versions_with` |  |
| 7.3:15, 7.3:38 | share of policies with a pair, smallest and largest size decile | 0.54%, 62.23% | 40.0%, 100.0% | 55.0%, 100.0% | 35.0%, 100.0% | 45.0%, 100.0% | `pairs.py`: `*.size_deciles` | Deciles of policies by rule count (60 policies each for all 600, 20 for an arm), as in `analyze_rq4.py`. Smallest decile: rules 7 to 60; 10 to 55; 7 to 43; 21 to 79. |
| 7.3:15 | pairs per policy, smallest and largest size decile | 0.0054, 2.2962 | 1.15, 148.92 | 1.15, 197.35 | 0.75, 61.00 | 1.10, 174.25 | `pairs.py`: `*.size_deciles` |  |
| fig_scaling (figure 2) | decile data | ten bins | ten bins in `figures.json` | ten bins in `figures.json` | ten bins in `figures.json` | ten bins in `figures.json` | `figures.py`: `fig2.<scope>` | Pairs per policy and share of policies with a pair for each decile, for all four scopes. |
| 7.3:19, 7.3:25 to 27 | overlap candidates: both rules unconditional, one, neither | 113 (26.7%), 268 (63.2%), 43 (10.1%) | 1,593 (17.1%), 4,153 (44.7%), 3,550 (38.2%) | 744 (23.6%), 1,489 (47.2%), 923 (29.2%) | 287 (15.6%), 794 (43.2%), 755 (41.1%) | 562 (13.1%), 1,870 (43.4%), 1,872 (43.5%) | `pairs.py`: `*.overlap_guard_placement` |  |
| 7.1:18 | overlap candidates with at least one unconditional rule | 381 of 424 | 5,746 of 9,296 (61.8%) | 2,233 of 3,156 (70.8%) | 1,081 of 1,836 (58.9%) | 2,432 of 4,304 (56.5%) | same |  |
| 7.3:33 | most frequent actions in overlap candidates (the permission's action node) | collect 123, use 111, disclose 50, provide 45, process 42 | collect@collection 2,803, use@use 1,349, disclose@disclosure 1,106, share@disclosure 716, process@processing 590 | collect@collection 737, use@use 473, disclose@disclosure 303, process@processing 277, share@disclosure 215 | collect@collection 653, use@use 330, process@processing 174, disclose@disclosure 120, share@disclosure 92 | collect@collection 1,413, disclose@disclosure 683, use@use 546, share@disclosure 409, sell@sale 233 | `pairs.py`: `*.overlap_candidates_by_allow_action_top10` | Action nodes are verb@operation. |
| 7.3:33 | overlap candidates by operation (the extractor's operation) | none | collection 3,587, disclosure 1,935, use 1,734, processing 719 | collection 1,133, use 733, disclosure 572, processing 370 | collection 776, use 360, disclosure 225, processing 183 | collection 1,678, disclosure 1,138, use 641, disclosure by transmission 340 | `pairs.py`: `*.overlap_candidates_by_extractor_operation` |  |
| 7.3:33 | mutually exclusive pairs with conditions on both rules | 26 of 26 | 792 of 1043 | 332 of 399 | 209 of 255 | 251 of 389 | `pairs.py`: `*.mutually_exclusive_guard_placement` | One rule unconditional: 251, 67, 46, 138; both unconditional: 0. |
| 7.2:44 | all guards replaced by true: pairs whose outcome changes (all become overlap candidates) | 1,782 + 26 change | 8,622 of 17,918 | 3,871 of 7,027 | 1,827 of 3,663 | 2,924 of 7,228 | `pairs.py`: `*.ablation_all_guards_true` | Same-scope conflicts with true guards: 1387, 455, 355, 577, against 19, 4, 4, 11 with the guards. |
| (new) | decision-procedure relation of overlap candidates: incomparable (prohibition wins), prohibition more specific, permission more specific, same scope | none | 8,623, 469, 185, 19 | 2,939, 157, 56, 4 | 1,688, 90, 54, 4 | 3,996, 222, 75, 11 | `pairs.py`: `*.relation_by_outcome.overlap_candidate` | FINDINGS §31 reports the same strata (8,623, 469, 185, 19 for all 600). |
| (new) | same-scope conflicts (pairs) and policies with one | none | 19 pairs in 15 policies | 4 pairs in 3 policies | 4 pairs in 4 policies | 11 pairs in 8 policies | `pairs.py`: `*.relation_by_outcome.overlap_candidate`, `*.versions_with_a_same_scope_conflict` | FINDINGS §31: 19 in 15 policies. |
| 7.5:29 | SMT time per pair | 1 s (untraced) | median 2.5 ms, 95th percentile 5.7 ms, maximum 412 ms, total 54 s over 17,918 pairs | not split by arm | not split by arm | not split by arm | `pairs.py`: `solver_time` | Time of each `pair_outcome` call, including building the solver, measured on 8 CPUs with the policies spread over 8 workers. The relation adds a median of 0.5 ms (95th percentile 4.3 ms, maximum 38 ms). |
| 7.2:46, discussion:12 | pairs decided after adding legal, jurisdiction, and purpose predicates | 115, 79.8% to 74.7% | no counterpart | no counterpart | no counterpart | no counterpart |  | The schema already contains legal bases, places, and retention time. |

**Reconciliation with the 17,918 pairs.** `corpus/testset/eval/conflict_pairs.py` imports `pairs.unit_pairs` and applies it to `rules/<id>.jsonl` of the 600 policies. `pairs.py --set testset` applies the same function to the same files through the new loaders. The pair sets are equal (17,918 pairs, none only in one file), and all 14 compared fields are equal for every pair. The pair counts per arm match `eval/conflict_pairs.json` (7,027, 3,663, 7,228), as do the strata of FINDINGS §31 (19 reported conflicts, 185 narrower permission, 469 narrower prohibition, 8,623 prohibition wins, 1,043 guards exclude each other, 7,579 undecided).

## Query families (RQ3)

| Paper row | Claim | Old value | All 600 | Web | Google Play | App Store | Script and output | Note |
|---|---|---|---|---|---|---|---|---|
| 7.4:25 | redundant rule pairs, with the policy's term relations | 30,750 | 212,245 | 95,280 | 34,875 | 82,090 | `queries.py --terms on`: `*.redundancy.pairs` | A duplicate has the same scope, a subsumed rule is strictly more specific than a broader rule of the same polarity. The vocabulary includes the policy's term relations (`rules/<id>.terms.json`), so a rule about a broader data, recipient, source, actor, or purpose term subsumes a narrower one. This is the main redundancy figure on the test set. |
| 7.4:25 | distinct redundant rule pairs (once per policy), with term relations | 14,996 | 160,781 | 77,198 | 27,971 | 55,612 | `queries.py --terms on`: `*.redundancy.distinct_pairs` | Each pair of rule contents counts once per policy. |
| 7.4:25 | policies (old: domains) with a redundant pair, with term relations | 246 domains | 595 of 600 | 198 of 200 | 197 of 200 | 200 of 200 | `queries.py --terms on`: `*.redundancy.domains_affected` |  |
| 7.4:25 | redundancy by kind, with term relations | attribute 18,674, guard 4,896, duplicate 4,248, counterparty 2,931, action 1 | data 57,480, action 36,275, purpose 43,583, duplicate 18,036, recipient 23,960, guard 12,135, source 17,844, actor 2,932 | data 16,882, action 21,625, purpose 27,168, duplicate 4,637, recipient 10,008, guard 3,959, source 9,990, actor 1,011 | data 14,230, action 4,893, purpose 4,849, duplicate 2,745, recipient 3,862, guard 2,016, source 1,609, actor 671 | data 26,368, action 9,757, purpose 11,566, duplicate 10,654, recipient 10,090, guard 6,160, source 6,245, actor 1,250 | `queries.py --terms on`: `*.redundancy.by_kind` | The kind is the first field in which the general rule is broader, in the order data, recipient, source, actor, purpose, action, guard. |
| 7.4:25 | redundant rule pairs, names only | 30,750 | 99,071 | 48,706 | 14,759 | 35,606 | `queries.py --terms off`: `*.redundancy.pairs` | The corpus definition (data names compared as names, no term relations), for comparison with the corpus run. |
| 7.4:25 | distinct redundant rule pairs, names only | 14,996 | 76,073 | 41,176 | 12,095 | 22,802 | `queries.py --terms off`: `*.redundancy.distinct_pairs` |  |
| 7.4:25 | policies with a redundant pair, names only | 246 domains | 587 of 600 | 195 of 200 | 194 of 200 | 198 of 200 | `queries.py --terms off`: `*.redundancy.domains_affected` |  |
| 7.4:25 | redundancy by kind, names only | as above | data 0, action 25,151, purpose 24,846, duplicate 15,735, recipient 13,373, guard 8,934, source 9,804, actor 1,228 | data 0, action 14,009, purpose 15,710, duplicate 4,044, recipient 6,455, guard 2,770, source 5,264, actor 454 | data 0, action 4,036, purpose 3,108, duplicate 2,471, recipient 2,120, guard 1,518, source 1,175, actor 331 | data 0, action 7,106, purpose 6,028, duplicate 9,220, recipient 4,798, guard 4,646, source 3,365, actor 443 | `queries.py --terms off`: `*.redundancy.by_kind` | No data-term relations, so no "data" kind. |
| intro:18, 7.4:28 | candidate redundant sentence pairs | 14,996 | 160,781 distinct redundant rule pairs | 77,198 distinct redundant rule pairs | 27,971 distinct redundant rule pairs | 55,612 distinct redundant rule pairs | same as the distinct pairs | Rule pairs, not sentence pairs. |
| 7.4:88, 7.4:101 | policies that collect and have no retention or erasure rule | 1,478 of 3,678 (40.2%) | 8 of 600 (1.3%) | 2 of 200 (1.0%) | 4 of 200 (2.0%) | 2 of 200 (1.0%) | `queries.py`: `*.coverage["versions: collection without retention or erasure"]` | Counting a retention time in a guard too: 8, 2, 4, 2. |
| 7.4:88 | unconditional disclosure rules (ALLOW, guard true) | 1,085 | 10,629 in 548 policies; 1,546 counting at most 3 per policy, as the old script did | 3,451 in 184 policies; 518 counting at most 3 per policy, as the old script did | 2,070 in 174 policies; 480 counting at most 3 per policy, as the old script did | 5,108 in 190 policies; 548 counting at most 3 per policy, as the old script did | `queries.py`: `*.coverage["unconditional disclosure rules*"]` | With a recipient: 8,895, 3,049, 1,692, 4,154. |
| 7.4:32 | compliance: consent promise, same-practice pairs of a promise and an ALLOW disclosure rule that overlap | 6,448 | 498 pairs in 53 policies | 50 pairs in 14 policies | 41 pairs in 15 policies | 407 pairs in 24 policies | `queries.py`: `*.compliance_rule_counts`, `*.compliance_requirement_versions` | A promise is a DENY disclosure rule whose fully translated guard uses `consent.*`, `opt_in.*`, or `user.parental_consent`. Promises: 271, 74, 80, 117. |
| 7.4:32 | compliance: consent promise, overlapping any ALLOW disclosure rule | 6,448 | 18,783 pairs in 116 policies | 3,198 pairs in 32 policies | 2,023 pairs in 35 policies | 13,562 pairs in 49 policies | same | The old check took any disclosure rule. Under the decision procedure the prohibition wins in the same-practice overlaps (incomparable 462, 46, 41, 375; prohibition more specific 36, 4, 0, 32). |
| 7.4:32 | compliance: child data without parental consent | 58 | 87 rules in 26 policies | 12 rules in 6 policies | 50 rules in 12 policies | 25 rules in 8 policies | `queries.py`: `child rules without parental consent` | ALLOW collection or disclosure rules whose guard implies an age under 13 and does not use `user.parental_consent`. Child rules in total: 106, 16, 53, 37. |
| 7.4:32 | compliance: GDPR scope without erasure | 186 | 4 of 600 | 1 of 200 | 1 of 200 | 2 of 200 | `queries.py`: `*.compliance_requirement_versions` | GDPR scope: a guard uses `basis.*` or `transfer.*`, or a place in the European Economic Area. Policies in GDPR scope: 480, 167, 157, 156. |
| 7.4:32 | compliance: sale without opt-out | 47 | 14 of 600 | 2 of 200 | 5 of 200 | 7 of 200 | same | ALLOW sale rules, and no sale rule that is a prohibition or uses `opt_out.*`. Policies that permit a sale: 225, 64, 49, 112. |
| intro:18, 7.4:50 | policies with a compliance candidate (old: versions, domains) | 750, 124 | 89 of 600 (149 with the old consent check over any disclosure rule) | 23 of 200 (41 with the old consent check over any disclosure rule) | 29 of 200 (47 with the old consent check over any disclosure rule) | 37 of 200 (61 with the old consent check over any disclosure rule) | `queries.py`: `*.versions_with_any_compliance_candidate*` | One policy is one domain. |

What the compliance checks cannot state through the schema is listed in `queries.json`, `not_stated`.

## Figure data

`out/figures.json` holds the data. Nothing is drawn.

| Figure | Panel | Key | Content |
|---|---|---|---|
| 1 | (a) rules per policy | `fig1.a.<scope>` | every policy's rule count (sorted), quartiles, and counts per power-of-two bin |
| 1 | (b) overlap candidates among policies with an opposing pair | `fig1.b.<scope>` | sorted counts per policy and the cumulative distribution; 515 policies of 600 have a pair, 64 of them no overlap candidate |
| 1 | (c) outcomes of all opposing pairs | `fig1.c.<scope>` | counts and shares of overlap candidates, mutually exclusive, and unresolved pairs, with the unresolved pairs split into partly translated guards and a guard that is only untranslated quotes |
| 1 | (d) rule-level ambiguity | `fig1.d.<scope>` | rules with an untranslated quote in the guard (old: no extracted predicate), rules with a reference quote (old: points elsewhere), disclosure rules without a recipient (old: missing counterparty); 598 of 600 policies have at least one of the three |
| 2 | size deciles | `fig2.<scope>` | for each of ten deciles of policies by rule count: pairs per policy and share of policies with a pair |

## Rows that need versions

The test set has one snapshot per policy.

| Paper rows | Claim | Old value | Status |
|---|---|---|---|
| abstract:2, intro:18, setup:23 | policies, timelines, archived versions | 273, 5,338 | needs versions |
| intro:18, setup:19, 7.4:56 | content revisions, silent revisions (same effective date) | 5,065, 4,050 (80.0%) | needs versions |
| 7.4:56, 7.4:82 | rule additions, removals, guard changes, polarity flips between versions | 58,153, 59,203, 18,966, 878 | needs versions |
| 7.4:56, 7.4:84 | distinct overlap-candidate signatures, persistence over 1, 2, 3, 5, 13 years | 1,407, 99, 80, 27, 1 | needs versions |
| 7.4:60, 7.4:65 | worked example of an overlap candidate from 2015 through 2023 | adelaideoval.com.au | needs versions |
| setup:23 | first 25 versions per timeline, versions submitted to the pipeline | 25, 3,836 | needs versions |

## Rows that need labels

| Paper rows | Claim | Status |
|---|---|---|
| abstract:2, intro:20, 7.1:8 to 7.1:20, 7.2:49, 7.4:28, 7.4:52, 7.4:84, 7.4:104, 7.4:106, conclusion:4 | E1 to E4 labels, 26 confirmed, 500 pairs, 71.2% | needs labels. The 600-policy set has its own blind labels: the error rate of 12.1% (FINDINGS §30) and the labels of 269 pairs by stratum (FINDINGS §31). They are not recomputed here. |
| abstract:2, intro:20, 7.5:8, 7.5:9, 7.5:31 | 100-policy comparison with PoliGraph and PolicyLint | needs labels. FINDINGS §31 (the 200 policies of PoliGraph's test set), not this set. |
| setup:51, 55, 59 | annotation sample sizes | needs labels. These are designs of the annotation samples, not statistics. |

## Checks

| Check | Result | Output |
|---|---|---|
| Pairs equal `conflict_pairs.jsonl` (17,918), every compared field | pass | `reconcile_pairs.json` |
| Rule totals equal the pipeline run's totals (146,861; web 49,823, Google Play 38,230, App Store 58,808) | pass | `rules.json` |
| Extraction records equal the reports' accepted raw rules | pass | `rules.json`: `checks` |
| Every unresolved pair has a blocking residual, and the ablation makes every pair an overlap candidate | pass | `pairs.json`: `checks` |
| Corpus outputs are unchanged by the edits to the scripts (`corpus_results/out/`) | pass: `pairs`, `queries`, `rules`, `corpus` outputs and the pair records of the edited scripts equal those of the unedited scripts (rerun on the same day) and the stored outputs of job 19040077, ignoring run records and timing. `history*.json` differ only in the order of tied entries of `longest_per_page_top5`, which also differs between two runs of the unedited `history.py` | `compare_outputs.py` |

## Run

Job 20734572 on partition `cs`, 8 CPUs, 32 GB, account `torch_pr_634_general`; elapsed time 00:11:13 for the job. Each step ran under `corpus/stores/timev.py`. Elapsed time and the step's peak memory (MaxRSS) come from `out/sacct_20734572.txt`. CPU time is user plus system time of all processes of the step (`out/time_<step>.log`). The last column is the largest single process (`timev.py`, in which worker processes count separately). sacct samples memory, so short peaks can be missed. Each JSON file also holds a run record.

| Step | Elapsed | CPU time | Peak memory (sacct) | Largest process |
|---|---:|---:|---:|---:|
| `rules.py --set testset` | 00:00:19 | 10 s | 1,334 MB | 1,045 MB |
| `pairs.py --set testset` | 00:00:37 | 144 s | 482 MB | 105 MB |
| `queries.py --set testset --terms on` | 00:06:34 | 1726 s | 712 MB | 269 MB |
| `queries.py --set testset --terms off` | 00:03:28 | 901 s | 668 MB | 240 MB |
| `reconcile_pairs.py` | 00:00:04 | 0 s | 104 MB | 98 MB |
| `figures.py` | 00:00:01 | 0 s | 54 MB | 55 MB |

`queries.py` dominates the time because redundancy compares pairs of rules with the solver. The solver time per pair in the pairs table was measured in the `pairs` step.

One observation about `policyclaw/`, not changed: `Vocabulary` keeps one namespace for all slots, so the alias and parent relations of the data terms apply to action, recipient, source, actor, and purpose names with the same spelling. `queries.py` follows the system's behavior (`policyclaw.conflicts.vocabulary`).
