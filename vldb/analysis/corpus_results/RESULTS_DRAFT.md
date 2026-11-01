# Corpus results on the full-corpus rerun (draft)

Every number below comes from a script in the repository and the JSON file it writes. The scripts make no model calls. Run everything with `sbatch vldb/analysis/corpus_results/run_all.s` (about 4.5 minutes on 8 CPUs). The values here are from job 19040077.

| Script | Output | What it computes |
|---|---|---|
| `corpus/supersede_inconsistent.py` | `corpus/rules/.superseded/` with `MANIFEST.tsv` | sets aside the rules of texts whose shared sections were extracted with different results (run once, before the rerun of `corpus/extract_corpus.py`) |
| `corpus/reconcile.py` | `corpus/reconciled/<page>/<version>.jsonl`, `corpus/reconciled/report.json` | reconciled rules of every version, with carried, new, and dropped counts, before and after diffs, the check, and 5 examples |
| `corpus.py` | `out/corpus.json` | captures, versions, pages, unstable pages, reverts, revisions, silent revisions, order-only and date-only changes, versions per year |
| `rules.py` | `out/rules.json` | rule counts and shares over texts and over versions, operations, translation, deletion test, rejected records, model usage |
| `pairs.py` | `out/pairs.json`, `out/pairs_extracted.json`, `out/pair_records*.jsonl` | opposing pairs, solver outcomes, decision-procedure relations, deciles, guard placement, ablation, solver time |
| `history.py` | `out/history.json`, `out/history_extracted.json` | rule changes between consecutive versions, signature persistence, extraction checks |
| `queries.py` | `out/queries.json`, `out/queries_extracted.json` | redundancy, coverage, compliance candidates |
| `common.py` | | shared loaders, rule sources, the unstable-page rule |

Scripts without a folder are in `vldb/analysis/corpus_results/`, and `out/` is its output folder.

## Definitions

**Versions and rule sets.** A final version is one real policy version of one page (1,021 versions on 291 pages). Its reconciled rules (`corpus/reconcile.py`) are the rules of the previous version wherever the text is unchanged, plus the version's own extraction wherever the text changed. Its extracted rules are the rules of its text (`corpus/rules/<sha>.jsonl`), so a text that several versions share counts once per version.

**Reconciliation.** Each section is cut into sentences at `[.!?]` followed by whitespace (the cut of `policyclaw/prep/segment.py`) and at line breaks, the unit in which versions differ. A sentence of version k is unchanged when its normalized text (NFKC, whitespace collapsed, as in `corpus/final_versions.py`) occurs in version k-1. A quote lies in a sentence when its words occur there in order, compared as `policyclaw.extract._quoted` compares them. A quote that spans sentences lies in the sentences it overlaps. Version 0 keeps its extracted rules. Version k carries every rule of version k-1 whose quotes all lie in unchanged sentences, adds every extracted rule with a quote outside the unchanged sentences, and drops the other extracted rules.

**Unstable pages.** A page is unstable when more than half of its versions are reverts (`common.unstable_pages`). Three pages meet the rule: `skimlinks.com/privacy-policies` (79 of 92 versions are reverts), `forums.speedlife.net/privacy` (10 of 12), and `jansfoodsteps.com/disclosure-privacy-policy` (7 of 9). Longitudinal and pair statistics exclude them. The column "all pages" includes them.

**Columns.** "Main" is the reconciled rules on the stable pages (288 pages, 908 versions). "Extracted" is the extracted rules on the stable pages. "All pages" is the reconciled rules on all 291 pages. Corpus rows have no rules, so they give the stable pages and all pages. **Old values** come from `vldb/inventory/paper_numbers.md`. They describe E0 (an open-weight model, regex guard mapper) on 3,678 versions of 273 timelines, unless the row says otherwise.

## Corpus (abstract, introduction, setup)

| Paper row | Claim | Old value | Main: stable pages | All pages | Script and output | Note |
|---|---|---|---|---|---|---|
| abstract:2, intro:18, setup:23 | policies, timelines | 273 | 288 pages | 291 pages on 290 domains | `corpus.py`: `stable_pages.pages`, `pages`, `domains` | A page merges URLs that differ only in scheme, "www.", or a trailing slash. |
| intro:18, setup:23 | archived or distinct policy versions | 5,338 (5,378 measured) | 908 versions, 860 distinct texts | 1,021 versions, 877 distinct texts | `corpus.py`: `*.versions`, `*.distinct_texts` | A new version requires a change in the page's policy lines (`corpus/FINAL_VERSIONS.md`). For reference: 7,558 captures, 3,671 visible-text versions. |
| intro:18, setup:19, 7.4:56 | content revisions | 5,065 (5,105 measured) | 620 | 730 | `corpus.py`: `*.revisions.consecutive_pairs` | A revision is a pair of consecutive versions of one page. |
| intro:18, setup:19 | revisions with the same effective date (silent) | 4,050 (80.0%), obsolete | 288 of 620 (46.5%), or 63.7% of the 452 revisions in which both versions state an effective date | 307 of 730 (42.1%), or 65.2% of 471 | `corpus.py`: `*.revisions.by_effective_date_and_change.silent`, `silent_share_pct`, `silent_share_of_pairs_with_two_effective_dates_pct` | On stable pages, 252 of the 288 change policy text and 36 only reorder lines. 168 revisions lack an effective date on one side or both. |
| (FINDINGS §6) | silent revisions that change no prose line | 2,403 of 4,087 (58.8%) | 36 of 288 (12.5%) only reorder lines, and none changes only the date line | 36 of 307 (11.7%) | `corpus.py`: `*.by_effective_date_and_change.silent` | Versions differ in policy lines by construction, so markup-only changes no longer count as revisions. |
| (new) | revisions that change only lines carrying the date | none | 23 of 620, all with a changed effective date | 23 of 730 | `corpus.py`: `*.by_effective_date_and_change["date changed"]["date only"]` | A changed line counts when it contains a date line of the page (`date_line` in `corpus/versions.jsonl`). Such a line can carry other edits. |
| (new) | revisions that only reorder lines | none | 46 of 620 | 46 of 730 | `corpus.py`: `*.by_effective_date_and_change.all["order only"]` | Matches `corpus/FINAL_VERSIONS.md`. |
| (new) | reverts | none | 37 versions on 20 pages (33 of the form A, B, A) | 133 on 23 pages (128) | `corpus.py`: `*.reverts` | |
| setup:23 | first 25 versions per timeline, "near the 75th percentile" | 25 | no cap: median 2, 90th percentile 7, maximum 21 versions per page | maximum 92 | `corpus.py`: `*.versions_per_page` | 108 pages have one version. |
| setup:23, 7.2:16 | versions submitted to the pipeline | 3,836 (untraced) | 860 distinct texts | 877 distinct texts | `rules.py`: `distinct_texts.texts`; `corpus.py` | |
| setup:23, 7.2:16, 7.3:4 | versions with at least one rule | 3,678 | 899 of 908 | 1,006 of 1,021 | `rules.py`: `versions_reconciled.*.counts.units_with_rules` | Extracted rules: 898 and 1,005. One version's own extraction has no rule, but it carries rules of its predecessor. |
| intro:26 | evaluation size | 3,678 versions of 273 policies | 908 versions of 288 pages | 1,021 versions of 291 pages | `corpus.py` | |
| (new) | versions per year of first snapshot | none | 2019: 244, 2020: 86, 2021: 88, other years at most 65 | 2019: 247, 2020: 127, 2021: 138 | `corpus.py`: `*.versions_by_first_snapshot_year` | Revisions per year are in `revisions_by_year_of_later_version`. |
| setup:11 | Privaseer entries, URLs, domains, pages above score 0.9 | 3,967,487, 3,180,982, 2,892,490, 2,013,975 | no counterpart | | | Statistics of the external dataset, outside the corpus outputs. |
| setup:15, 7.3:36 | date classifier training set, accuracy | 1,001 sentences, 93%, 97% | no counterpart | | | Dates come from the crawl's `timeline.json`. No classifier output is stored in `corpus/`. |

## Rules (RQ2)

| Paper row | Claim | Old value | Main | Extracted | All pages | Script and output | Note |
|---|---|---|---|---|---|---|---|
| abstract:2, intro:18, 7.2:16 | extracted rules | 112,768 | 69,318 | 68,941 | 88,154 | `rules.py`: `versions_*.*.counts.rules` | Over the 877 distinct texts: 66,337 rules from 56,438 extraction records. A record with several purposes compiles to one rule per purpose. Main: 38,995 rules carried and 30,323 new (18,574 of them in version 0). |
| 7.2:18 | ALLOW and DENY rules | 100,895 and 11,873 | 63,766 (92.0%) and 5,552 (8.0%) | 63,275 (91.8%) and 5,666 (8.2%) | 81,673 (92.6%) and 6,481 (7.4%) | `rules.py`: `polarity ALLOW`, `polarity DENY` | Over texts: 60,946 and 5,391. |
| 7.2:18 | rules with explicit conditions | 45,265 (40.1%) | 43,667 (63.0%) with a condition or exception quote, 42,015 (60.6%) whose guard is not true | 43,851 (63.6%), 42,180 (61.2%) | 55,548 (63.0%), 53,611 (60.8%) | `rules.py`: `with conditions or exceptions`, `guard not true` | Main: conditions alone 38,389 (55.4%), exceptions 8,764 (12.6%), purpose 31,472 (45.4%). |
| 7.2:18 | rules with a recipient | 24.1% | 10,217 (14.7%) | 10,500 (15.2%) | 13,898 (15.8%) | `rules.py`: `with recipient` | |
| 7.2:62 to 67 | any ambiguity flag | 21,684 (19.2%) | no single counterpart | | | | The old flags came from the regex guard mapper. The rows below give the closest measures. |
| 7.2:63 | condition has no extracted predicate | 13,039 (11.6%) | 16,118 (23.3%) with an untranslated quote in the guard, 8,152 (11.8%) with only untranslated quotes | 16,384 (23.8%), 8,264 (12.0%) | 19,558 (22.2%), 8,520 (9.7%) | `rules.py`: `guard with a residual`, `guard only residuals` | |
| 7.2:64, 7.2:72 | condition points elsewhere, cross-reference flag | 2,943 (2.6%), 6.0% | 9,536 (13.8%) with a reference quote: to a law 4,711, a policy section 3,172, another document 2,547 | 9,402 (13.6%) | 13,302 (15.1%) | `rules.py`: `with references`, `with a reference to *` | The extractor assigns the target. |
| 7.2:65 | underspecified condition | 10,096 (9.0%) | no counterpart | | | | Category of the old regex mapper. |
| 7.2:66 | missing or implicit counterparty | 5,061 (4.5%) | 4,218 disclosure rules without a recipient (6.1% of rules, 30.4% of 13,882 disclosure rules) | 3,916 (5.7%, 28.8%) | 4,586 (5.2%, 25.7%) | `rules.py`: `disclosure without recipient` | A disclosure rule's action lies under the operation "disclosure" in the action network. |
| 7.2:67 | generic data attribute | 426 (0.4%) | no counterpart | | | | Needs a data hierarchy or a word list. |

Extraction statistics come from the per-text reports, so they exist for texts and for extracted rules only.

| Paper row | Claim | Old value | Distinct texts | Extracted, stable pages | Extracted, all pages | Script and output | Note |
|---|---|---|---|---|---|---|---|
| 7.2:16 | share of raw extractions removed by the filter | 21.9% | 1,966 of 58,404 extracted records rejected (3.4%) | 3.4% | 2.9% | `rules.py`: `shares_pct["rejected of extracted records"]`, `report rejected: *` | Different filter. Over texts: 880 records quote text not in the section, 827 lack polarity, action, or data, 259 name an operation outside the schema. Non-policy lines are removed before extraction. |
| (new) | qualifier quotes translated to formulas | none | 20,032 of 26,569 (75.4%) | 75.3% | 76.4% | `rules.py`: `report quotes`, `report residual_quotes` | Distinct quotes per section, from the reports. |
| (new) | unsatisfiable guards, qualifiers without effect | none | 75 and 2,078 | 75 and 2,223 | 75 and 2,316 | `rules.py`: `report unsatisfiable_guards`, `report qualifiers_without_effect` | Deletion test in `policyclaw/extract.py`. |
| (new) | operations chosen by the extractor | none | collection 19,657, use 14,515, disclosure by transmission 7,784, storage 6,653, processing 4,375, disclosure 3,756, erasure or destruction 1,810, sale 1,060, other (uncovered) 299 (0.45%) | | | `rules.py`: `distinct_texts.counts["extractor operation *"]` | The action network places the verbs of 1,238 rules (1.9%) under no operation. 981 distinct action nodes, 543 verbs. |

## Opposing pairs and solver outcomes (abstract, RQ2, RQ4)

Pairing as in `vldb/analysis/sampling/conflict_pairs.py`: one compiled rule per extraction record, and every ALLOW and DENY rule of a version's rule set that describe the same practice (`policyclaw.merge._same_practice`, lenient). Outcomes from `policyclaw.queries.pair_outcome`. Relations from the decision procedure's clash rules, as in `system_resolution.py`.

| Paper row | Claim | Old value | Main | Extracted | All pages | Script and output | Note |
|---|---|---|---|---|---|---|---|
| abstract:2, intro:18, 7.2:10, 7.2:21 | opposing pairs | 2,232 | 4,169 | 4,388 | 5,273 | `pairs.py`: `*.pairs` | Over distinct texts: 4,243 (`pairs_extracted.json`: `distinct_texts`). |
| abstract:2, intro:18, 7.2:21 | overlap candidates, mutually exclusive, unresolved | 424, 26, 1,782 | 2,609, 453, 1,107 | 2,595, 446, 1,347 | 3,529, 453, 1,291 | `pairs.py`: `*.outcomes` | |
| abstract:2 | unresolved share | 79.8% | 26.6% | 30.7% | 24.5% | `pairs.py`: `*.outcome_shares_pct.unresolved` | |
| abstract:2, intro:18, 7.2:21, 7.2:76 | pairs with a solver result | 450 (20.2%), 25.3% with all added predicates | 3,062 (73.5%) | 3,041 (69.3%) | 3,982 (75.5%) | `pairs.py`: `*.decided_share_pct` | |
| 7.2:29 to 38 | Table e0_outcomes | overlap 424 (19.0%), mutually exclusive 26 (1.2%), unresolved semantic 811 (36.3%), unresolved pipeline 971 (43.5%) | 2,609 (62.6%), 453 (10.9%), unresolved with partly translated guards 429 (10.3%), unresolved with a guard that is only untranslated quotes 678 (16.3%) | 2,595 (59.1%), 446 (10.2%), 571 (13.0%), 776 (17.7%) | 3,529 (66.9%), 453 (8.6%), 613 (11.6%), 678 (12.9%) | `pairs.py`: `*.outcomes`, `*.unresolved_blocking.a_guard_entirely_untranslated` | The old "pipeline" class had no usable extracted condition. |
| 7.2:23 | versions without a pair, with a pair, with an overlap candidate | 2,927, 751, 314 | 344 (of 899 with rules), 555, 416 | 360, 538, 394 | 359, 647, 508 | `pairs.py`: `*.versions_with_a_pair`, `*.versions_with` | |
| 7.3:15 | versions with a pair, overlap, mutually exclusive, unresolved | 751, 314, 8, 614 | 555, 416, 135, 336 | 538, 394, 127, 342 | 647, 508, 135, 428 | `pairs.py`: `*.versions_with` | |
| 7.3:15, 7.3:38 | share of versions with a pair, smallest and largest decile | 0.54%, 62.23% | 14.6%, 96.7% | 22.5%, 90.0% | 13.0%, 100.0% | `pairs.py`: `*.size_deciles` | Deciles of versions with rules by rule count, as in `analyze_rq4.py`. |
| 7.3:15 | pairs per version, smallest and largest decile | 0.0054, 2.2962 | 0.16, 13.50 | 0.29, 14.39 | 0.14, 14.81 | same | |
| fig_scaling | decile data | ten bins | ten bins | | | `pairs.py`: `*.size_deciles` | No figure script yet. |
| 7.3:19, 7.3:25 to 27 | overlap candidates: both unconditional, one, neither | 113 (26.7%), 268 (63.2%), 43 (10.1%) | both guards true 351 (13.5%), one 1,396 (53.5%), neither 862 (33.0%) | 367, 1,399, 829 | 627, 2,040, 862 | `pairs.py`: `*.overlap_guard_placement` | |
| 7.1:18 | overlap candidates with at least one unconditional rule | 381 of 424 | 1,747 of 2,609 (67.0%) | 1,766 of 2,595 (68.1%) | 2,667 of 3,529 (75.6%) | same | |
| 7.3:33 | most frequent actions in overlap candidates | collect 123, use 111, disclose 50, provide 45, process 42 | ALLOW rule's action: collect@collection 1,064, use@use 388, disclose@disclosure 156, obtain@collection 152, process@processing 134 | 1,106, 319, 197, 161, 146 | disclose@disclosure by transmission is second with 755 | `pairs.py`: `*.overlap_candidates_by_allow_action_top10`, `*.overlap_candidates_by_extractor_operation` | Main by operation: collection 1,414, use 415, disclosure by transmission 283, disclosure 231. |
| 7.3:33 | mutually exclusive pairs with conditions on both rules | 26 of 26 | 370 of 453 | 365 of 446 | 370 of 453 | `pairs.py`: `*.mutually_exclusive_guard_placement` | Main: 370 of the 453 are policy exceptions, a prohibition that holds "except as set forth in this Policy" (`policy.permits`). |
| 7.2:44 | all guards replaced by true | all 2,232 overlap, 26 and 1,782 change | all 4,169 overlap, 1,560 change | all 4,388, 1,793 change | all 5,273, 1,744 change | `pairs.py`: `*.ablation_all_guards_true` | With true guards the decision procedure finds 329 same-scope conflicts (main), against 13 with the guards. |
| 7.2:46, discussion:12 | pairs decided after adding legal, jurisdiction, and purpose predicates | 115, 79.8% to 74.7%, 1,667 | no counterpart | | | | The current schema already contains legal bases, places, and retention time. Removing variable families would need a new translation. |
| discussion:12 | unresolved pairs | 1,782 of 2,232 | 1,107 of 4,169 | 1,347 of 4,388 | 1,291 of 5,273 | `pairs.py`: `*.outcomes.unresolved` | |
| discussion:12 | pairs without a usable extracted condition | 971 | 678 | 776 | 678 | `pairs.py`: `*.unresolved_blocking.a_guard_entirely_untranslated` | |
| (new) | unresolved pairs blocked by residuals | none | all 1,107 (by definition): the permission's residuals 377, the prohibition's 464, both 266 | 454, 607, 286 | 561, 464, 266 | `pairs.py`: `*.unresolved_blocking` | |
| (new) | how the decision procedure resolves overlap candidates | none | incomparable, so the prohibition wins: 2,395. Prohibition more specific: 144. Permission more specific: 57. Same scope, a conflict: 13 | 2,364, 152, 62, 17 | 2,487, 144, 885, 13 | `pairs.py`: `*.relation_by_outcome.overlap_candidate` | Most "permission more specific" pairs in the all-pages column come from skimlinks.com. |
| (new) | versions with a same-scope conflict | none | 13 versions on 3 pages | 14 on 4 | 13 on 3 | `pairs.py`: `*.versions_with_a_same_scope_conflict`, `*.pages_with_a_same_scope_conflict` | The extracted rules' conflicts have both guards true and are purpose limitations ("only for" against "not to") or "May Share" against "do not share". |
| 7.5:29 | SMT time "approximately one second" | 1 s (untraced) | median 2.7 ms per pair (95th percentile 8.3 ms, maximum 16 ms), 16.9 s for all 5,273 pairs of the 1,021 reconciled rule sets | median 2.6 ms | | `pairs.py`: `solver_time` | Time of each `pair_outcome` call, including building the solver. The relation adds a median of 0.6 ms. The script takes 19 s on 8 CPUs. |

## Changes over time (RQ3 differencing)

| Paper row | Claim | Old value | Main | Extracted | All pages | Script and output | Note |
|---|---|---|---|---|---|---|---|
| 7.4:56 | adjacent transitions, versions, timelines | 3,405, 3,678, 273 | 620 revisions, 908 versions, 288 pages | same | 730, 1,021, 291 | `history.py`: `*.revisions.revisions`; `corpus.py` | |
| 7.4:56, 7.4:82 | rule additions, removals, guard changes, polarity flips | 58,153, 59,203, 18,966, 878 | 8,595, 5,856, 872, 21 | 18,072, 15,356, 2,883, 43 | 8,619, 5,878, 880, 21 | `history.py`: `*.revisions` | Rule key: polarity, canonical action node, normalized data, recipient, and source names, and the guard. Extracted, all pages: 20,258, 17,541, 3,401, 43. The totals agree with `corpus/reconciled/report.json`. |
| (new) | revisions with identical rule sets | none | 260 of 620 | 36 of 620 | 350 of 730 | `history.py`: `*.revisions["identical rule sets"]` | |
| 7.4:56, 7.4:84 | distinct overlap-candidate signatures, spanning 2 or more years, 5 or more | 1,407, 99, 27 | 692, 505, 246 | 956, 584, 233 | 699, 512, 246 | `history.py`: `*.signatures.overlap_candidate` | A signature is the page, the two practice keys, and the outcome. Its span runs from the first snapshot of its first version to the last snapshot of its last version. Main: 409 occur in 2 or more versions. |
| 7.4:56, 7.4:77 | persistence: at least 1, 2, 3, 5, 13 years | 1,407, 99, 80, 27, 1 | 692, 505, 428, 246, 2 | 956, 584, 403, 233, 0 | 699, 512, 435, 246, 2 | `history.py`: `*.signatures.overlap_candidate.span_years` | |
| 7.4:56 | longest span | 13 years | 13 years | 11 years | 13 years | `history.py`: `max_span_years` | |
| 7.4:60, 7.4:65 | worked example: an overlap candidate from 2015 through 2023 | adelaideoval.com.au | candidates: literaryguild.com/privacy-policy 2014 to 2026 (3 of 4 versions), www8.buyerpricer.com 2013 to 2023 (5 of 5), bodyrocfitlab.com 2016 to 2025 (6 of 6), deensgarage.co.uk 2008 to 2017 (9 of 14) | | | `history.py`: `*.signatures.overlap_candidate.longest_per_page_top5` | |
| (new) | same-scope conflict signatures | none | 3, each in 2 or more versions, spanning 7 to 8 years | 4 | 3 | `history.py`: `*.signatures["same scope conflict"]` | |

**Reconciliation** (`corpus/reconcile.py`, `corpus/reconciled/report.json`, all pages):

| Measure | Value |
|---|---:|
| Rules of version 0 of each page (kept) | 18,810 |
| Rules carried over in later versions | 57,568 |
| Newly extracted rules kept in later versions | 11,776 |
| Extracted rules dropped (all quotes in unchanged sentences) | 56,718 |
| Reconciled rules over all versions | 88,154 |
| Quote fragments that could not be located | 0 |
| Added or removed rules after reconciliation without a quote in a changed sentence (check) | 0 of 18,325 |

Rule changes per revision before and after reconciliation, with the totals of all pages: additions 20,258 to 8,619, removals 17,541 to 5,878, guard changes 3,401 to 880, polarity flips 43 to 21. The largest drop is on skimlinks.com, where additions fall from 2,061 to 3, because a one-line flip such as "om" no longer re-extracts the section. Among stable pages, swwiltshirelibdems.org.uk falls from 1,017 to 511 and dealroom.co from 614 to 252.

The 5 random revisions (seed 1, all pages) are in `report.json`, `examples`. Three change no rule before or after reconciliation (crowdbreaks.org versions 0 to 1, bikebox-rental.co.uk 2 to 3, helenamtrealestate.net 1 to 2). skimlinks.com versions 80 to 81 remove the line "om" and change 24 additions, 20 removals, and 4 guards to nothing. colombiatech.com versions 0 to 1 replace the quotation marks of 6 sentences, and reconciliation reduces 28 additions and 22 removals to 4 and 4: the rules of the 6 changed sentences are extracted again with other data names ("browser_version" becomes "browser software version").

What the extracted rules show about re-extraction (`history_extracted.json`, stable pages): of the 21,005 rule keys in the sections whose text changed, 2,933 (14.0%) were in the earlier version. For practice keys: 5,017 of 18,598 (27.0%). Reconciliation limits this variation to the changed sentences.

## Query families (RQ3)

| Paper row | Claim | Old value | Main | Extracted | All pages | Script and output | Note |
|---|---|---|---|---|---|---|---|
| 7.4:25 | redundant rule pairs, domains, distinct pairs | 30,750, 246, 14,996 | 20,593, 262, 7,811 | 20,690, 267, 11,422 | 24,830, 264, 7,855 | `queries.py`: `*.redundancy` | A duplicate has the same scope (`_same_scope`), a subsumed rule is strictly more specific than a broader rule of the same polarity (`_more_specific`). Distinct pairs count each pair of rule contents once per page. Main: 819 versions are affected. |
| intro:18, 7.4:28 | candidate redundant sentence pairs | 14,996 | 7,811 distinct redundant rule pairs | 11,422 | 7,855 | `queries.py`: `*.redundancy.distinct_pairs` | Carried rules are the same rows in every version, so reconciliation lowers the distinct count. |
| 7.4:25 | redundancy by kind | attribute 18,674, guard 4,896, duplicate 4,248, counterparty 2,931, action 1 | action 6,249, purpose 4,808, duplicate 2,864, recipient 2,287, guard 2,204, source 1,576, actor 605, data 0 | 6,176, 4,865, 2,972, 2,217, 2,268, 1,687, 505, 0 | 7,261, 5,820, 3,232, 3,023, 2,848, 2,036, 610, 0 | `queries.py`: `*.redundancy.by_kind` | The kind is the first field in which the general rule is broader, in the order data, recipient, source, actor, purpose, action, guard. Data subsumption needs per-policy data relations (a model call), which this run lacks. |
| 7.4:88, 7.4:101 | versions with collection and no retention or deletion rule | 1,478 of 3,678 (40.2%) | 77 of 899 (8.6%) | 63 of 898 (7.0%) | 83 of 1,006 (8.3%) | `queries.py`: `*.coverage["versions: collection without retention or erasure"]` | Collection, storage, and erasure are schema operations reached through the action network. Counting a retention time in a guard too: 74 (main). |
| 7.4:88 | unconditional third-party sharing rules | 1,085 | 1,501 when counting at most 3 per version, as the old script did. 3,728 rules in 613 versions | 1,498, 3,494, 621 | 1,786, 5,025, 714 | `queries.py`: `*.coverage["unconditional disclosure rules*"]` | ALLOW rules under "disclosure" with the guard true. Main: 2,786 name a recipient. The old check matched "third" in the recipient. |
| 7.4:32 | compliance: consent promise | 6,448 | 4,191 overlapping pairs of a consent promise and any ALLOW disclosure rule, in 148 versions. 195 pairs in 54 versions when the two rules describe the same practice | 3,729 in 153 versions, 216 in 55 | 4,191 in 148, 195 in 54 | `queries.py`: `*.compliance_rule_counts`, `*.compliance_requirement_versions` | A promise is a DENY disclosure rule whose fully translated guard uses `consent.*`, `opt_in.*`, or `user.parental_consent`. The decision procedure lets the prohibition win in all 195 same-practice overlaps (183 incomparable, 12 prohibition more specific). |
| 7.4:32 | compliance: child data without parental consent | 58 | 0 | 2 rules in 2 versions | 0 | `queries.py`: `child rules without parental consent` | ALLOW collection or disclosure rules whose guard implies an age under 13 (COPPA) and does not use `user.parental_consent`. Main: 2 such ALLOW rules exist, and both require parental consent. |
| 7.4:32 | compliance: GDPR scope without erasure | 186 | 22 versions | 25 | 31 | `queries.py`: `*.compliance_requirement_versions` | GDPR scope: a guard uses `basis.*` or `transfer.*`, or a place in the European Economic Area (391 versions, main). Erasure: a rule under "erasure or destruction". |
| 7.4:32 | compliance: sale without opt-out | 47 | 18 versions | 16 | 18 | same | ALLOW sale rules, and no sale rule that is a prohibition or uses `opt_out.*`. Main: 58 versions permit a sale. |
| intro:18, 7.4:50 | versions and domains with a compliance candidate | 750, 124 | 94 versions, 42 domains (187 and 77 with the old consent check over any disclosure rule) | 95, 47 (192, 84) | 103, 43 (196, 78) | `queries.py`: `*.versions_with_any_compliance_candidate*`, `*.domains_with_any_compliance_candidate*` | |
| (old coverage script, not in the paper) | sensitive data only in permissions | 22,502 | no counterpart | | | `queries.py`: `not_stated` | The schema has no data categories or sensitivity labels. |

What the compliance checks cannot state through the schema (`queries.py`, `not_stated`): child data found by the word "child" in a data name, GDPR found by the word "gdpr" in the text, deletion requests found by guard atoms named like deletion, and sensitive data.

## Rows without a new counterpart

| Paper rows | Old values | Reason |
|---|---|---|
| abstract:2 (26 confirmed, 500 pairs, 71.2%), intro:20, 7.1:8 to 7.1:20 except 7.1:18, 7.2:49, 7.4:28, 7.4:52, 7.4:84, 7.4:104, 7.4:106, conclusion:4 | E1 to E4 and downstream human labels | Human labels of E0 output. New labels of the new rules and pairs are needed. |
| abstract:2, intro:20, 7.5:8, 7.5:9, 7.5:31 | 100 policies, 25 pairs, PoliGraph 45, PolicyLint 6 | Comparison on the shared 100-policy sample with Claim IR v21 and two baselines, outside this corpus run. |
| setup:51, setup:55, setup:59, intro:20 | sample sizes and strata | Designs of the annotation samples. |
| 3.2_ontology:9, 5_imps:4, 7.5:13, 7.5:17 | five votes, three agreeing, ontology and rewrite labels | Steps of E0. The new action network records its own three-vote placements in `policyclaw/network.json`. |
| 7.5:21 | run-to-run stability (30 policies, three runs) | The corpus run is one pass. `history.py` shows that the cache makes repeated sections identical. |
| 7.5:25 | cross-model comparison | Not part of this run. |
| 7.5:29 | GPUs, host memory, extraction time per run, cost | The extractor is a hosted model. Usage over the whole extraction: 6,024 model calls, 10.65 million prompt tokens, 6.98 million completion tokens, and 31,665 thinking tokens. That sums the final reports (5,740 calls), the superseded reports of the 13 re-extracted texts (173), and earlier attempts of retried texts (111) (`rules.py`: `usage *`, `superseded_reports`). Cost needs a price table, which the repository does not hold. |
| discussion:12 to 17 | 1,816 conditions that reference outside context, four types | No such classification in the new run. The nearest measure is the reference quotes by target (Rules table, row 7.2:64). |

## Changes since the first draft

1. **Shared boilerplate.** 10 section texts carried different rules in different pages: 9 sections of one template on 11 pages and one section on 2 pages. The pages ran in parallel during extraction and probably missed the cache for the same section at the same moment. `corpus/supersede_inconsistent.py` moved the rules and reports of the 13 texts that contain such a section to `corpus/rules/.superseded/`. `corpus/extract_corpus.py` then extracted them again with the environment of `corpus/run_extract.s` and one thread. All 421 calls came from the cache, with no model call (`corpus/logs/rerun_superseded_202610021103.out`). The cross-page check now reports 0 of 3,190 section texts. Rules over texts went from 66,290 to 66,337.
2. **Unstable pages.** The rule above replaces the earlier exclusion of the page with the most versions. It excludes three pages.
3. **Reconciliation.** Version-level statistics now use the reconciled rules. The extracted rules remain as comparison columns.

## Checks

| Check | Result | Output |
|---|---|---|
| Final versions, reverts, and revisions agree with the per-page counts in `final_sites.jsonl` | pass | `corpus.json`: `checks` |
| Change sizes over all pages match `corpus/FINAL_VERSIONS.md` (730 changes: 162, 128, 101, 136, 133, 70 by size, 46 with the same set of lines, 128 of the form A, B, A) | pass | `corpus.json`: `all_pages.revisions.changed_lines`, `all_pages.reverts.a_b_a` |
| Extraction records equal the reports' accepted raw rules (56,438), and no final report has a failed call | pass | `rules.json`: `checks` |
| Every unresolved pair has a blocking residual, and the ablation makes every pair an overlap candidate | pass (both hold by definition) | `pairs*.json`: `checks` |
| A section whose text is unchanged between consecutive versions has identical extracted rules (3,033 sections) | pass, 0 differ | `history*.json`: `checks` |
| Every occurrence of a section text anywhere in the corpus has the same extracted rules (3,190 section texts) | pass, 0 differ (10 before the rerun) | `history*.json`: `checks` |
| Every rule added or removed after reconciliation has a quote in a changed sentence | pass, 0 of 18,325 | `corpus/reconciled/report.json`: `total` |
| Every quote of every reconciled rule can be located in its section | pass, 0 unlocated | same |
| The rule changes of `history.py` on the reconciled rules equal those of `corpus/reconcile.py` | pass (8,619, 5,878, 880, 21) | `history.json`, `report.json` |

One observation about `policyclaw/`, not fixed: `Vocabulary` keeps one namespace for all slots, so a data name that equals an operation or action node gets that node's parents (for example data "other" lies under "processing"). 7 rules have such data names. `queries.py` follows the system's behavior, and a run that ignored these parents gave the same redundancy counts.

## Run

Job 19040077 on partition `cs`, 8 CPUs, 32 GB. Elapsed time, CPU time (AveCPU), and the step's peak memory come from `out/sacct_19040077.txt`. sacct samples memory, so short peaks can be missed. Each JSON file also holds a run record.

| Step | Elapsed | CPU time | Peak memory |
|---|---:|---:|---:|
| `corpus/reconcile.py` | 49 s | 18 s | 1,091 MB |
| `corpus.py` | 15 s | 1 s | 30 MB |
| `rules.py` | 37 s | 14 s | 25 MB |
| `pairs.py --rules reconciled` | 20 s | 46 s | 354 MB |
| `history.py --rules reconciled` | 26 s | 8 s | 852 MB |
| `queries.py --rules reconciled` | 44 s | 273 s | 483 MB |
| `pairs.py --rules extracted` | 16 s | 29 s | 367 MB |
| `history.py --rules extracted` | 21 s | 5 s | 652 MB |
| `queries.py --rules extracted` | 29 s | 176 s | 451 MB |

The re-extraction of the 13 superseded texts took 18 s on the holder job (all calls from the cache).
