import collections, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "corpus_results"))
import common as C  # noqa: E402

C.use_testset()
KEYS = ("unit", "allow", "deny", "outcome", "relation", "true_guards", "same_section", "operation", "action", "blocking", "blocking_in",
        "untranslated_guard", "ablation_outcome", "ablation_relation")


def main():
    new = {(r["allow"], r["deny"]): r for r in C.jsonl(C.OUT / "pair_records.jsonl")}
    old_rows = C.jsonl(C.TESTSET / "eval/conflict_pairs.jsonl")
    old = {(r["allow"], r["deny"]): r for r in old_rows}
    diff = collections.Counter()
    for k in set(new) & set(old):
        for f in KEYS:
            diff[f] += new[k].get(f) != old[k].get(f)
    res = {"pairs_now": len(new), "pairs_before": len(old_rows), "distinct_keys_before": len(old),
           "only_now": len(set(new) - set(old)), "only_before": len(set(old) - set(new)),
           "records_with_a_different_field": dict(diff), "identical": not (set(new) ^ set(old)) and not any(diff.values())}
    C.write("reconcile_pairs.json", res)
    print(res)


if __name__ == "__main__":
    main()
