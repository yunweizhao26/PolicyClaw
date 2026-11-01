# Label statistics, 600-policy test set

Script: `labels_600.py` (writes `labels_600.json`); figures: `draw_figures.py`. Blind labels only, no model calls. Intervals are 95% bootstrap intervals (2,000 samples): Part A resamples policies within each arm (seed 0, as `corpus/testset/eval/score.py`), Part B resamples pairs within strata (seed 1). The 100 E1 check items are excluded.

## Part A. Rule fidelity (1,200 rules, 2 per policy)

| Label | All (1,200) | Web (400) | Android (400) | Apple (400) |
|---|---|---|---|---|
| full | 818 (68.2%) | 280 (70.0%) | 272 (68.0%) | 266 (66.5%) |
| minor | 235 (19.6%) | 75 (18.8%) | 78 (19.5%) | 82 (20.5%) |
| substantial | 12.1% [10.2, 13.8] | 10.8% [8.0, 13.8] | 12.5% [9.5, 15.8] | 13.0% [10.0, 16.2] |
| source_ambiguous | 2 (0.2%) | 2 (0.5%) | 0 (0.0%) | 0 (0.0%) |

Substantial rate by polarity (count/rules, share [interval]):

| Polarity | All | Web | Android | Apple |
|---|---|---|---|---|
| ALLOW | 132/1116, 11.8% [10.1, 13.7] | 41/382, 10.7% [7.9, 14.0] | 45/356, 12.6% [9.4, 16.0] | 46/378, 12.2% [9.0, 15.5] |
| DENY | 13/84, 15.5% [8.3, 23.5] | 2/18, 11.1% [0.0, 27.8] | 5/44, 11.4% [2.9, 20.8] | 6/22, 27.3% [10.5, 45.5] |

Error types among the 145 substantial errors (all arms). A rule can carry several types. Share of all 1,200 rules, and counts by polarity (ALLOW 132 substantial, DENY 13):

| Error type | Count | Share of 1,200 rules [interval] | ALLOW | DENY |
|---|---|---|---|---|
| hallucinated_condition | 59 | 4.9% [3.8, 6.1] | 58 | 1 |
| missing_condition | 45 | 3.8% [2.8, 4.8] | 38 | 7 |
| actor_entity_extraction | 24 | 2.0% [1.2, 2.8] | 21 | 3 |
| other | 15 | 1.2% [0.7, 1.9] | 14 | 1 |
| condition_polarity | 13 | 1.1% [0.5, 1.7] | 10 | 3 |
| operation_extraction | 9 | 0.8% [0.3, 1.2] | 8 | 1 |
| referential_ambiguity | 8 | 0.7% [0.2, 1.2] | 7 | 1 |
| segmentation_context_loss | 7 | 0.6% [0.2, 1.1] | 7 | 0 |
| data_type_extraction | 7 | 0.6% [0.2, 1.0] | 7 | 0 |
| recipient_extraction | 7 | 0.6% [0.2, 1.1] | 6 | 1 |
| allow_deny_polarity | 1 | 0.1% [0.0, 0.2] | 0 | 1 |

Per-polarity shares of that polarity's rules are in `labels_600.json` (`error_types_by_polarity_share_of_polarity_rules`).

Substantial errors that involve a condition field (condition fields only plus flow and condition fields):

| Scope | Condition only | Flow and condition | Flow only | Involving a condition |
|---|---|---|---|---|
| all | 94 | 19 | 32 | 113/145 (77.9%) |
| web | 29 | 6 | 8 | 35/43 (81.4%) |
| android | 34 | 2 | 14 | 36/50 (72.0%) |
| apple | 31 | 11 | 10 | 42/52 (80.8%) |

## Part B. Opposing pairs (269 labeled)

Stratum mapping checked against `RESULTS_600.md` and `score_conflicts.py`: it matches (same_scope 19, allow_specific 185, deny_specific 469, incomparable 8,623, exclusive 1,043, unresolved 7,579; first four sum to 9,296). `score_conflicts.py` names the misread label `extraction_error`.

Label counts per stratum:

| Stratum | Pairs | Labeled | allow | deny | no_overlap | contradiction | unresolved | different_practice | extraction_error |
|---|---|---|---|---|---|---|---|---|---|
| Reported conflict (same scope) | 19 | 19 | 0 | 14 | 0 | 2 | 0 | 3 | 0 |
| Narrower permission wins | 185 | 50 | 8 | 15 | 2 | 6 | 2 | 10 | 7 |
| Narrower prohibition wins | 469 | 50 | 0 | 48 | 1 | 0 | 0 | 1 | 0 |
| Prohibition wins (incomparable) | 8,623 | 50 | 3 | 31 | 0 | 0 | 0 | 13 | 3 |
| Guards exclude each other | 1,043 | 50 | 17 | 16 | 10 | 0 | 0 | 7 | 0 |
| Undecided (untranslated text) | 7,579 | 50 | 4 | 29 | 4 | 0 | 0 | 13 | 0 |

Label shares by solver class, weighted by stratum size, with 95% bootstrap intervals:

| Share | Overlap candidates (9,296) | Mutually exclusive (1,043) | Unresolved (7,579) | All pairs (17,918) |
|---|---|---|---|---|
| allow | 5.9% [0.3, 13.2] | 34.0% [22.0, 46.0] | 8.0% [2.0, 16.0] | 8.4% [4.2, 13.1] |
| contradiction | 0.3% [0.1, 0.5] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 0.1% [0.1, 0.2] |
| deny | 63.1% [50.2, 74.5] | 32.0% [20.0, 46.0] | 58.0% [44.0, 70.0] | 59.1% [50.4, 67.9] |
| different_practice | 24.6% [13.5, 35.8] | 14.0% [4.0, 24.0] | 26.0% [14.0, 38.0] | 24.6% [17.3, 32.4] |
| extraction_error | 5.8% [0.3, 13.2] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 3.0% [0.1, 6.9] |
| no_overlap | 0.2% [0.0, 0.4] | 20.0% [10.0, 32.0] | 8.0% [2.0, 16.0] | 4.6% [1.7, 8.1] |
| unresolved | 0.1% [0.0, 0.2] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.1] |
| real_conflict (contradiction or unresolved) | 0.3% [0.1, 0.6] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 0.2% [0.1, 0.3] |
| should_not_be_paired (different_practice) | 24.6% [13.6, 35.9] | 14.0% [6.0, 24.0] | 26.0% [14.0, 38.0] | 24.6% [17.0, 32.4] |
| extraction_error (misread) | 5.8% [0.3, 11.6] | 0.0% [0.0, 0.0] | 0.0% [0.0, 0.0] | 3.0% [0.1, 6.9] |

Real conflict means contradiction or unresolved (FINDINGS section 31). Misread is the `extraction_error` label. Only the 19 same-scope pairs are fully labeled, so the mutually exclusive and unresolved classes rest on 50 pairs each, and the overlap-candidate class on 50 pairs in each of three strata.
