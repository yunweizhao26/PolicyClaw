import argparse, collections, csv, json, multiprocessing as mp, os, sys, time
from pathlib import Path

R = Path("/scratch/yz5944/nlp+privacy/PolicyClaw")
sys.path.insert(0, str(R / "vldb/analysis/corpus_results"))
import common as C  # noqa: E402
import pairs as P  # noqa: E402

T = R / "corpus/testset"


def rows(pid):
    path = T / "rules" / f"{pid}.jsonl"
    return C.jsonl(path) if path.exists() else []


C.unit_rows = rows


def summary(recs, policies):
    by = collections.defaultdict(list)
    for r in recs:
        by[r["unit"]].append(r)
    conflict = lambda r: r["outcome"] == "overlap_candidate" and r["relation"] == "same scope"
    return {"policies": len(policies), "policies_with_a_pair": sum(bool(by[p]) for p in policies),
            "policies_with_an_overlap_candidate": sum(any(r["outcome"] == "overlap_candidate" for r in by[p]) for p in policies),
            "policies_with_a_same_scope_conflict": sum(any(conflict(r) for r in by[p]) for p in policies),
            "same_scope_conflicts": sum(map(conflict, recs)), **P.summarize(recs)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=len(os.sched_getaffinity(0)))
    ap.add_argument("--dir", type=Path, default=R / "corpus/testset")
    args = ap.parse_args()
    global T
    T = args.dir.resolve()
    (T / "eval").mkdir(exist_ok=True)
    with open(T / "selection.tsv", newline="", encoding="utf-8") as f:
        arms = {r["id"]: r.get("arm", "all") for r in csv.DictReader(f, delimiter="\t")}
    t0 = time.time()
    with mp.Pool(args.workers) as pool:
        results = {u: recs for u, _, recs in pool.imap_unordered(P.unit_pairs, sorted(arms), chunksize=2)}
    recs = [dict(r, arm=arms[u], policy=u) for u in sorted(arms) for r in results[u]]
    with open(T / "eval/conflict_pairs.jsonl", "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    names = sorted(set(arms.values()) - {"all"})
    res = {arm or "all": summary([r for r in recs if arm in (None, r["arm"])], [p for p in arms if arm in (None, arms[p])])
           for arm in names + [None]}
    res["solver_wall_s"] = round(time.time() - t0, 1)
    res["run"] = C.run_record()
    (T / "eval/conflict_pairs.json").write_text(json.dumps(res, indent=1) + "\n")
    for k in names + ["all"]:
        s = res[k]
        print(k, s["pairs"], s["outcomes"], "same-scope conflicts", s["same_scope_conflicts"],
              "in", s["policies_with_a_same_scope_conflict"], "policies;", s["relation_by_outcome"]["overlap_candidate"])
    print("run", res["run"])


if __name__ == "__main__":
    main()
