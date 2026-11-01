# RQ3 results

Answers recomputed from the prompt text alone with a separate parser and encoding, against the solver answers.

- pair_items: 600 of 600 agree
- many_items: 500 of 500 agree
- join_items: 600 of 600 agree
- tail_items: 240 of 240 agree
- join answers that change when values differing in case or punctuation are merged: 204 of 19579

Share of join answers that need one_value: {"exclusion/128": 51.3, "exclusion/16": 42.0, "exclusion/32": 32.9, "exclusion/64": 37.9, "exclusion/8": 30.0, "implication/128": 1.1, "implication/16": 0.0, "implication/32": 0.3, "implication/64": 0.9, "implication/8": 0.0}

Share of join answers that need residual_identity: {"exclusion/128": 0.1, "exclusion/16": 1.4, "exclusion/32": 2.6, "exclusion/64": 0.2, "exclusion/8": 0.0, "implication/128": 6.5, "implication/16": 16.0, "implication/32": 14.0, "implication/64": 11.1, "implication/8": 26.7}

Semantics on the 17,918 opposing pairs.

| measure | value |
| --- | --- |
| pairs | 17918 |
| outcomes | {"overlap_candidate": 9296, "unresolved": 7579, "mutually_exclusive": 1043} |
| with_residual | 8795 |
| binate_pairs | 9 |
| definite_with_residual | {"overlap_candidate": 754, "mutually_exclusive": 462} |
| definite_policies | 252 |
| definite_derived_exclusions | 289 |
| definite_without_derived | 927 |
| definite_without_derived_policies | 224 |
| derived_minus | {"mutually_exclusive": 666, "unresolved": 38, "overlap_candidate": 36} |
| derived_both | {"mutually_exclusive": 8, "overlap_candidate": 1} |
| kleene_changes | {"mutually_exclusive -> unresolved": 196} |
| kleene_derived | 185 |
| kleene_identity | 10 |
| kleene_plain | {"missed": 11, "impossible": 377} |
| identity_exclusions | 10 |
| several_values_changes | {"mutually_exclusive -> unresolved": 14, "mutually_exclusive -> overlap_candidate": 46, "unresolved -> overlap_candidate": 2} |
| spelling_changes | {"mutually_exclusive -> overlap_candidate": 2} |
| derived_plus_only | 188 |
| oracle | {"overlap_candidate / overlap_candidate": 9296, "unresolved / not_certain": 7579, "mutually_exclusive / not_certain": 1043} |
| open_true | {"overlap_candidate": 5391, "mutually_exclusive": 2188} |
| open_false | {"mutually_exclusive": 6429, "overlap_candidate": 1150} |
| open_readings_disagree | 6541 |
| open_constant_certain | {"False": 7579} |
| open_unconditional | 2654 |
| guards_per_policy | {"median": 50.0, "at_least": {"8": 579, "16": 547, "32": 445, "64": 190, "128": 30}} |
| trivial_guards | 199 |
| kept_guards | 34905 |
| atoms | {"median": 2, "p95": 5, "max": 31} |
| by_operation | {"groups": 6987, "median": 3, "p95": 20, "max": 243, "at_least_128": 5} |
| by_operation_and_data | {"groups": 60189, "median": 1, "p95": 2, "max": 19, "at_least_128": 0} |

Single pairs against the solver.

| level | stratum | pairs | accuracy | all seeds agree |
| --- | --- | --- | --- | --- |
| LOW | mutually_exclusive / no residual | 100 | 100.0 | 100.0 |
| LOW | mutually_exclusive / with residual | 100 | 100.0 | 100.0 |
| LOW | overlap_candidate / no residual | 100 | 100.0 | 100.0 |
| LOW | overlap_candidate / with residual | 100 | 100.0 | 100.0 |
| LOW | unresolved / partly translated | 100 | 100.0 | 100.0 |
| LOW | unresolved / untranslated | 100 | 100.0 | 100.0 |
| LOW | all | 600 | 100.0 | 100.0 |
| HIGH | mutually_exclusive / no residual | 100 | 100.0 | 100.0 |
| HIGH | mutually_exclusive / with residual | 100 | 100.0 | 100.0 |
| HIGH | overlap_candidate / no residual | 100 | 100.0 | 100.0 |
| HIGH | overlap_candidate / with residual | 100 | 100.0 | 100.0 |
| HIGH | unresolved / partly translated | 100 | 100.0 | 100.0 |
| HIGH | unresolved / untranslated | 100 | 100.0 | 100.0 |
| HIGH | all | 600 | 100.0 | 100.0 |

Rule status against the solver.

| level | k | rule accuracy | query correct | all seeds agree | majority rule accuracy |
| --- | --- | --- | --- | --- | --- |
| LOW | 2 | 99.7 | 99.3 | 99.0 | 48.5 |
| LOW | 4 | 100.0 | 100.0 | 100.0 | 47.0 |
| LOW | 8 | 100.0 | 99.7 | 99.0 | 46.4 |
| LOW | 16 | 99.6 | 97.0 | 97.0 | 45.3 |
| LOW | 32 | 99.8 | 94.7 | 91.0 | 52.0 |
| HIGH | 2 | 100.0 | 100.0 | 100.0 | 48.5 |
| HIGH | 4 | 100.0 | 100.0 | 100.0 | 47.0 |
| HIGH | 8 | 100.0 | 100.0 | 100.0 | 46.4 |
| HIGH | 16 | 100.0 | 100.0 | 100.0 | 45.3 |
| HIGH | 32 | 100.0 | 100.0 | 100.0 | 52.0 |

Joins over the guards of one policy.

| level | query/k | mean answers | median answers | policies | precision | recall | recall 95% CI | median query recall | whole set | seeds agree | model s | solver s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LOW | exclusion/8 | 0.3 | 0 | 60 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 100.0 | 100.0 | 4.8 | 0.025 |
| LOW | exclusion/16 | 1.2 | 0 | 60 | 100.0 | 99.0 | [97.1, 100.0] | 100.0 | 99.4 | 98.3 | 5.7 | 0.033 |
| LOW | exclusion/32 | 5.2 | 2 | 60 | 99.3 | 89.4 | [75.2, 97.7] | 100.0 | 86.1 | 80.0 | 7.7 | 0.076 |
| LOW | exclusion/64 | 42.8 | 30 | 60 | 99.0 | 89.2 | [84.9, 92.9] | 100.0 | 52.2 | 30.0 | 13.8 | 0.304 |
| LOW | exclusion/128 | 172.1 | 133 | 30 | 98.7 | 61.9 | [51.4, 73.4] | 83.0 | 13.3 | 3.3 | 26.8 | 1.37 |
| LOW | implication/8 | 0.5 | 0 | 60 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 100.0 | 100.0 | 4.8 | 0.033 |
| LOW | implication/16 | 1.3 | 1 | 60 | 99.6 | 99.6 | [98.8, 100.0] | 100.0 | 98.9 | 96.7 | 5.3 | 0.063 |
| LOW | implication/32 | 6.1 | 5 | 60 | 99.1 | 95.1 | [92.2, 97.6] | 100.0 | 81.1 | 71.7 | 5.9 | 0.165 |
| LOW | implication/64 | 21.2 | 21 | 60 | 96.2 | 77.9 | [72.6, 83.2] | 85.7 | 25.0 | 8.3 | 9.1 | 0.738 |
| LOW | implication/128 | 75.6 | 72 | 30 | 94.7 | 58.2 | [52.4, 63.4] | 53.8 | 1.7 | 0.0 | 15.7 | 3.295 |
| HIGH | exclusion/8 | 0.3 | 0 | 60 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 100.0 | 100.0 | 19.3 | 0.025 |
| HIGH | exclusion/16 | 1.1 | 0 | 60 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 100.0 | 100.0 | 38.2 | 0.033 |
| HIGH | exclusion/32 | 5.2 | 2 | 60 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 100.0 | 100.0 | 72.6 | 0.076 |
| HIGH | exclusion/64 | 42.8 | 30 | 60 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 100.0 | 100.0 | 150.9 | 0.304 |
| HIGH | exclusion/128 | 172.1 | 133 | 30 | 100.0 | 99.9 | [99.8, 100.0] | 100.0 | 91.7 | 100.0 | 266.1 | 1.37 |
| HIGH | implication/8 | 0.5 | 0 | 60 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 100.0 | 100.0 | 17.9 | 0.033 |
| HIGH | implication/16 | 1.4 | 1 | 60 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 100.0 | 100.0 | 29.5 | 0.063 |
| HIGH | implication/32 | 6.1 | 5 | 60 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 100.0 | 100.0 | 64.6 | 0.165 |
| HIGH | implication/64 | 21.2 | 21 | 60 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 100.0 | 100.0 | 156.9 | 0.738 |
| HIGH | implication/128 | 75.7 | 72 | 30 | 100.0 | 99.6 | [99.0, 100.0] | 100.0 | 88.3 | 100.0 | 232.0 | 3.295 |

Low-level calls at 128 guards by reported thinking: {"exclusion/none": {"calls": 72, "recall": 31.7}, "exclusion/thinking": {"calls": 108, "recall": 85.4}, "implication/none": {"calls": 127, "recall": 47.8}, "implication/thinking": {"calls": 53, "recall": 85.4}}

Dollars per query.

| query/k | low | high |
| --- | --- | --- |
| exclusion/8 | 0.0017 | 0.0101 |
| exclusion/16 | 0.0028 | 0.0222 |
| exclusion/32 | 0.0048 | 0.0457 |
| exclusion/64 | 0.0094 | 0.0993 |
| exclusion/128 | 0.0193 | 0.1629 |
| implication/8 | 0.0019 | 0.0092 |
| implication/16 | 0.003 | 0.018 |
| implication/32 | 0.004 | 0.0418 |
| implication/64 | 0.0053 | 0.096 |
| implication/128 | 0.0126 | 0.1571 |

Joins restricted to the policies with at least 128 guards.

| query/k | mean answers | policies | precision | recall | recall 95% CI | whole set | model s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| exclusion/8 | 0.7 | 30 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 5.0 |
| exclusion/16 | 2.5 | 30 | 100.0 | 98.2 | [93.2, 100.0] | 97.8 | 5.6 |
| exclusion/32 | 9.4 | 30 | 100.0 | 98.5 | [96.6, 99.7] | 93.3 | 7.5 |
| exclusion/64 | 43.3 | 30 | 99.3 | 74.5 | [57.5, 89.5] | 57.8 | 17.2 |
| implication/8 | 0.2 | 30 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 5.1 |
| implication/16 | 1.5 | 30 | 97.8 | 98.5 | [96.2, 100.0] | 94.4 | 5.7 |
| implication/32 | 4.4 | 30 | 99.0 | 95.0 | [89.4, 99.2] | 85.6 | 6.4 |
| implication/64 | 17.9 | 30 | 96.1 | 74.7 | [65.7, 82.6] | 28.9 | 8.3 |

Batched plan: 4800 calls, 0 failures, $22.806, 31810.6 s of summed latency.

batch

| query/k | mean answers | policies | precision | recall | recall 95% CI | whole set | model s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| exclusion/128 | 197.2 | 20 | 99.3 | 99.3 | [98.8, 99.6] | 35.0 | 795.2 |
| implication/128 | 73.8 | 20 | 99.2 | 98.0 | [96.7, 99.1] | 40.0 | 798.5 |

single_LOW

| query/k | mean answers | policies | precision | recall | recall 95% CI | whole set | model s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| exclusion/128 | 197.2 | 20 | 97.7 | 57.9 | [43.9, 70.2] | 8.3 | 29.6 |
| implication/128 | 73.9 | 20 | 94.7 | 54.7 | [45.9, 63.7] | 1.7 | 11.6 |

single_HIGH

| query/k | mean answers | policies | precision | recall | recall 95% CI | whole set | model s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| exclusion/128 | 197.2 | 20 | 100.0 | 100.0 | [100.0, 100.0] | 100.0 | 238.2 |
| implication/128 | 73.8 | 20 | 100.0 | 99.6 | [98.8, 100.0] | 90.0 | 211.8 |

Solver scaling on pooled guards, exclusion join.

| k | pairs | seconds | ms per pair |
| --- | --- | --- | --- |
| 128 | 8128 | [1.0, 1.1, 0.9] | 0.123 |
| 256 | 32640 | [4.9, 4.5, 4.5] | 0.143 |
| 512 | 130816 | [24.5, 21.4, 22.5] | 0.174 |
| 1024 | 523776 | [134.5, 129.6, 131.5] | 0.252 |
| 2048 | 2096128 | [769.5, 738.3, 799.7] | 0.367 |

Whole-policy model reads on 40 test policies, mean 36404 characters: $0.2505, $0.00626 per read.
