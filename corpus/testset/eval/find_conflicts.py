import argparse, collections, csv, json, multiprocessing as mp, os, sys, time
from pathlib import Path

R = Path("/scratch/yz5944/nlp+privacy/PolicyClaw")
sys.path[:0] = [str(R), str(R / "vldb/analysis/corpus_results")]
import common as C  # noqa: E402
from policyclaw.conflicts import find_conflicts, vocabulary  # noqa: E402

D = None
RANK = ("contradiction", "other")


def run(pid):
    t0 = time.time()
    path = D / "rules" / f"{pid}.jsonl"
    rows = C.jsonl(path) if path.exists() else []
    terms = D / "rules" / f"{pid}.terms.json"
    relations = json.load(open(terms))["relations"] if terms.exists() else {}
    rules = [C.rule(r) for r in rows]
    found = find_conflicts(rules, vocabulary(rules, relations))
    best = {}
    for p in found:
        k = (C.record_id(p["allow"]), C.record_id(p["deny"]))
        kind = "contradiction" if p["contradiction"] else "other"
        if k not in best or RANK.index(kind) < RANK.index(best[k][0]):
            best[k] = (kind, p)
    return pid, [dict(p, kind=kind, policy=pid) for kind, p in best.values()], round(time.time() - t0, 1), bool(relations)


def main():
    global D
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=len(os.sched_getaffinity(0)))
    args = ap.parse_args()
    D = args.dir.resolve()
    with open(D / "selection.tsv", newline="", encoding="utf-8") as f:
        arms = {r["id"]: r.get("arm", "all") for r in csv.DictReader(f, delimiter="\t")}
    t0 = time.time()
    with mp.Pool(args.workers) as pool:
        results = {pid: (recs, s, rel) for pid, recs, s, rel in pool.imap_unordered(run, sorted(arms), chunksize=1)}
    (D / "eval").mkdir(exist_ok=True)
    with open(D / "eval/conflicts.jsonl", "w") as f:
        for pid in sorted(results):
            for r in results[pid][0]:
                f.write(json.dumps(dict(r, arm=arms[pid])) + "\n")
    res = {}
    for arm in sorted(set(arms.values()) - {"all"}) + [None]:
        pids = [p for p in arms if arm in (None, arms[p])]
        recs = [r for p in pids for r in results[p][0]]
        kinds = collections.Counter(r["kind"] for r in recs)
        res[arm or "all"] = {"policies": len(pids), "policies_with_term_relations": sum(results[p][2] for p in pids),
                             "pairs": len(recs), "kinds": dict(kinds),
                             "relations": dict(collections.Counter(r["relation"] for r in recs).most_common()),
                             "outcomes": dict(collections.Counter(r["outcome"] for r in recs)),
                             "policies_with_a_contradiction": len({r["policy"] for r in recs if r["kind"] == "contradiction"})}
    slow = sorted(results.items(), key=lambda x: -x[1][1])[:5]
    res["slowest_policies_s"] = {p: v[1] for p, v in slow}
    res["wall_s"] = round(time.time() - t0, 1)
    res["run"] = C.run_record()
    (D / "eval/conflicts.json").write_text(json.dumps(res, indent=1) + "\n")
    for k, v in res.items():
        if isinstance(v, dict) and "pairs" in v:
            print(k, v["pairs"], "pairs;", v["kinds"], "; policies with a contradiction:", v["policies_with_a_contradiction"])
    print("run", res["run"], "slowest", res["slowest_policies_s"])


if __name__ == "__main__":
    main()
