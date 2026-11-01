# E1 labels

**Use `e1_final_labels.csv`.** It holds one label for each of the 1,000 E1 rules. Every script under
`vldb/analysis/` reads it by default. Set `E1_LABELS=human` (E1 recheck) or `REFERENCE=human` (error-rate
judge) only to reproduce a number computed with the labels of the S&P submission.

## How the final labels were made

1. **Human labels.** One annotator labeled all 1,000 rules after seeing five model prelabels. These are the
   labels of the S&P submission (39.0% substantial).
2. **Blind relabel.** A language model labeled all 1,000 rules with the same rubric and the same text, without
   the human label or the prelabels. That model produced none of the prelabels.
3. **Adjudication.** The two labels give the same fidelity on 511 rules, and those keep the human label. On the
   other 489 rules, a separate instance of that model saw both labels as A and B in random order, without knowing which
   was human, read the policy text, and gave the label. It followed `analysis/label_audit/adjudication_guide.txt`.
   That guide applies the rubric equally to both labels, and it counts an omitted condition that limits when the
   practice applies as substantial.
4. **Manual check.** 20 adjudicated rules were checked by hand against the policy text. The check agreed on 18.
   The two disagreements are omitted conditions that the checker would call minor.

## Result

| Fidelity | Rules |
|---|---:|
| full | 539 |
| minor | 183 |
| substantial | 275 |
| source ambiguous | 3 |

The E1 sample is self-weighting, so weighted and unweighted rates are equal. The substantial rate is 27.5%
(95% interval 24.8% to 30.1%, bootstrap over rules), against 39.0% with the human labels. Condition-only
substantial errors are 15.6% (13.3% to 18.0%). These labels come from a model, checked by a second blind pass
and by hand. A second human annotator is still needed.

## Columns of `e1_final_labels.csv`

| Column | Meaning |
|---|---|
| `fidelity`, `wrong_slots`, `error_types`, `downstream_impact` | the final label. For an adjudicated rule, the downstream impact follows from the wrong slots as the rubric defines it |
| `condition_only_error` | substantial, with only the condition fields wrong |
| `omitted_qualifier` | for a condition-only error, the omitted text: from the second reading of condition errors (`analysis/condition_errors/labels.jsonl`), else the adjudicator's evidence quote |
| `label_source` | `agreed` (human and relabel give the same fidelity) or `adjudicated` |
| `human_fidelity`, `relabel_fidelity` | the two inputs, for tracing |
| `adjudicator_confidence`, `adjudicator_reason` | for adjudicated rules |
| `design_stratum`, `sample_weight` | from the E1 sampling design |

## Other E1 label files, and what they are

| File | What it is | Use |
|---|---|---|
| `experiments/frozen_e0/annotations/final/e1/sol_{1,2}.jsonl` | prelabels by a second language model, two runs | history only |
| `experiments/frozen_e0/annotations/final/e1/qwen_{1,2,3}.jsonl` | prelabels by Qwen3.8-27B, three runs | history only |
| `experiments/frozen_e0/annotations/final/e1/consensus.jsonl` | majority of the five prelabels | history only |
| `experiments/frozen_e0/annotations/final/review/e1_review.csv` | annotation worksheet with the prelabels side by side | history only |
| `experiments/frozen_e0/annotations/final/review/e1_ann.csv` | human labels of the S&P submission | input to the final labels |
| `vldb/analysis/condition_errors/labels.jsonl` | second reading of the human condition errors: which qualifier was omitted and where it is | source of `omitted_qualifier` |
| `vldb/analysis/label_audit/labels/` | blind relabel | input to the final labels |
| `vldb/analysis/label_audit/adjudicated/`, `adjudicated_other/` | adjudicator decisions (disagreements about substantial, and the rest) | input to the final labels |

Rebuild the final file with `python vldb/analysis/label_audit/make_final.py`.
