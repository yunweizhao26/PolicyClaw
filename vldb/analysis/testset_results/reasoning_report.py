import collections, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out/reasoning"
load = lambda n: json.load(open(OUT / n))
SCORES, JOINS, BATCH, SCALE, READ, SEM, CHECK = (load(f"{n}.json") for n in ("scores", "join_scores", "batch_scores", "scale", "read_usage", "semantics", "prompt_check"))
lines = ["# RQ3 results", ""]
lines += ["Answers recomputed from the prompt text alone with a separate parser and encoding, against the solver answers.", ""]
for k, v in CHECK.items():
    if k.endswith("_items"):
        lines.append(f"- {k}: {v['agree']} of {v['items']} agree")
lines.append(f"- join answers that change when values differing in case or punctuation are merged: {CHECK['spelling']['changed']} of {CHECK['spelling']['answers']}")
lines.append("")
for k in ("one_value", "residual_identity"):
    lines += [f"Share of join answers that need {k}: " + json.dumps({q: v["share"] for q, v in CHECK[k].items()}), ""]


def table(head, rows):
    lines.append("| " + " | ".join(head) + " |")
    lines.append("|" + " --- |" * len(head))
    lines.extend("| " + " | ".join(str(c) for c in r) + " |" for r in rows)
    lines.append("")


lines += ["Semantics on the 17,918 opposing pairs.", ""]
table(("measure", "value"), [(k, json.dumps(v)) for k, v in SEM.items()])
lines += ["Single pairs against the solver.", ""]
table(("level", "stratum", "pairs", "accuracy", "all seeds agree"),
      [(lv, k, x["n"], x["accuracy"], x["all_seeds_agree"]) for lv, v in SCORES.items() for k, x in v["pairs"].items()])
lines += ["Rule status against the solver.", ""]
table(("level", "k", "rule accuracy", "query correct", "all seeds agree", "majority rule accuracy"),
      [(lv, k, x["rule_accuracy"], x["query_correct"], x["all_seeds_agree"], x["majority_rule_accuracy"]) for lv, v in SCORES.items() for k, x in v["many"].items()])
lines += ["Joins over the guards of one policy.", ""]
table(("level", "query/k", "mean answers", "median answers", "policies", "precision", "recall", "recall 95% CI", "median query recall", "whole set", "seeds agree", "model s", "solver s"),
      [(lv, k, x["truth_per_query"], x["truth_median"], x["policies"], x["precision"], x["recall"], x["recall_ci"], x["median_query_recall"], x["exact_sets"], x["seeds_agree"], x["model_s"], x["solver_s"])
       for lv in ("LOW", "HIGH") for k, x in JOINS[lv].items()])
lines += ["Low-level calls at 128 guards by reported thinking: " + json.dumps(JOINS["low_thinking"]), ""]
lines += ["Dollars per query.", ""]
table(("query/k", "low", "high"), [(k, JOINS["dollars_per_query"]["LOW"][k], JOINS["dollars_per_query"]["HIGH"][k]) for k in JOINS["dollars_per_query"]["LOW"]])
lines += ["Joins restricted to the policies with at least 128 guards.", ""]
table(("query/k", "mean answers", "policies", "precision", "recall", "recall 95% CI", "whole set", "model s"),
      [(k, x["truth_per_query"], x["policies"], x["precision"], x["recall"], x["recall_ci"], x["exact_sets"], x["model_s"]) for k, x in BATCH["tail"].items()])
lines += [f"Batched plan: {BATCH['batch_calls']} calls, {BATCH['batch_failures']} failures, ${BATCH['batch_dollars']}, {BATCH['batch_seconds']} s of summed latency.", ""]
for name in ("batch", "single_LOW", "single_HIGH"):
    lines += [name, ""]
    table(("query/k", "mean answers", "policies", "precision", "recall", "recall 95% CI", "whole set", "model s"),
          [(k, x["truth_per_query"], x["policies"], x["precision"], x["recall"], x["recall_ci"], x["exact_sets"], x["model_s"]) for k, x in BATCH[name].items()])
lines += ["Solver scaling on pooled guards, exclusion join.", ""]
runs = collections.defaultdict(list)
for r in SCALE["runs"]:
    runs[r["k"]].append(r)
table(("k", "pairs", "seconds", "ms per pair"),
      [(k, v[0]["pairs"], [round(x["seconds"], 1) for x in v], round(1000 * sum(x["seconds"] for x in v) / sum(x["pairs"] for x in v), 3)) for k, v in sorted(runs.items())])
lines += [f"Whole-policy model reads on {READ['calls']} test policies, mean {READ['mean_chars']} characters: ${READ['dollars']}, ${READ['dollars_per_read']} per read.", ""]
(HERE / "RESULTS_RQ3.md").write_text("\n".join(lines))
