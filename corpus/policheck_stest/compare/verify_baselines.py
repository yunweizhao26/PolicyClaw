import concurrent.futures as cf, json, os, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hybrids as H
import score_f1 as S

BASELINES = ("policylint", "poligraph")


def main():
    items = S.items
    ids = {b: sorted(i for i, x in items.items() if b in x["systems"]) for b in BASELINES}
    every = sorted(set().union(*ids.values()))
    with cf.ThreadPoolExecutor(int(os.environ.get("THREADS", 8))) as ex:
        done = dict(zip(every, ex.map(lambda i: H.gemini_check(i, items[i]), every)))
    out = {"labels": {i: done[i]["label"] for i in every}}
    for b in BASELINES:
        kept = [i for i in ids[b] if done[i]["label"] in H.REAL]
        for i in kept:
            items[i]["systems"].append(f"{b}_verified")
    per, gold, _ = S.tables(H.REAL)
    rng = random.Random(1)
    boots = [[rng.choice(S.policies) for _ in S.policies] for _ in range(2000)]
    for b in BASELINES:
        name = f"{b}_verified"
        P, Rc, F, rep, tp, found, total = S.scores(per, gold, S.policies, name)
        rows = [S.scores(per, gold, pols, name)[:3] for pols in boots]
        ci = [sorted(v[k] for v in rows) for k in range(3)]
        out[name] = {"reports": rep, "real": tp, "found": found, "total": total, "precision": round(100 * P, 1), "recall": round(100 * Rc, 1), "f1": round(100 * F, 1),
                     "precision_ci": [round(100 * ci[0][50], 1), round(100 * ci[0][1949], 1)]}
    rows = [S.scores(per, gold, pols, "policyclaw_verified")[0] for pols in boots]
    rows.sort()
    out["policyclaw_verified_precision_ci"] = [round(100 * rows[50], 1), round(100 * rows[1949], 1)]
    json.dump(out, open(HERE / "baselines_verified.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "labels"}, indent=1))


if __name__ == "__main__":
    main()
