import collections, csv, glob, json, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SYSTEMS = ("policylint", "poligraph", "policyclaw_before", "policyclaw", "policyclaw_verified", "direct_llm")
key = json.load(open(HERE / "key.json"))
items = key["items"]
lab = {json.loads(l)["item"]: json.loads(l)["label"] for f in glob.glob(str(HERE / "labels/*.jsonl")) for l in open(f) if l.strip()}
assert set(lab) == set(items)
groups = json.load(open(HERE / "group_key.json"))
cluster = {}
for p, ids in groups["single"].items():
    cluster[ids[0]] = (p, 0)
for f in glob.glob(str(HERE / "group_labels/*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        for n, g in enumerate(r["groups"]):
            for i in g:
                cluster[i] = (r["policy"], n)
with open(HERE.parent / "selection.tsv", newline="", encoding="utf-8") as f:
    policies = [r["id"] for r in csv.DictReader(f, delimiter="\t")]


def tables(real_labels):
    real = {i for i in items if lab[i] in real_labels}
    missing = real - set(cluster)
    assert not missing, f"real items without a group: {sorted(missing)[:5]}"
    per = {p: collections.defaultdict(lambda: [0, 0, set()]) for p in policies}
    gold = collections.defaultdict(set)
    gold_pool = collections.defaultdict(set)
    for i, x in items.items():
        p = x["policy"]
        if i in real:
            gold[p].add(cluster[i])
            if set(x["systems"]) - {"readers"}:
                gold_pool[p].add(cluster[i])
        for s in x["systems"]:
            per[p][s][0] += 1
            if i in real:
                per[p][s][1] += 1
                per[p][s][2].add(cluster[i])
    return per, gold, gold_pool


def scores(per, gold, pols, system):
    rep = sum(per[p][system][0] for p in pols)
    tp = sum(per[p][system][1] for p in pols)
    found = sum(len(per[p][system][2] & gold[p]) for p in pols)
    total = sum(len(gold[p]) for p in pols)
    P = tp / rep if rep else 0.0
    R = found / total if total else 0.0
    return P, R, (2 * P * R / (P + R) if P + R else 0.0), rep, tp, found, total


def report(name, real_labels):
    per, gold, gold_pool = tables(real_labels)
    for ref_name, ref in (("all sources", gold), ("systems' pool only", gold_pool)):
        rng = random.Random(1)
        boots = [[rng.choice(policies) for _ in policies] for _ in range(2000)]
        print(f"\n== {name}; reference: {ref_name}: {sum(map(len, ref.values()))} contradictions in "
              f"{sum(bool(v) for v in ref.values())} policies")
        print("system".ljust(22) + "reports  real  found   precision            recall               F1")
        for s in SYSTEMS + (("readers",) if ref is gold else ()):
            P, R, F, rep, tp, found, total = scores(per, ref, policies, s)
            bs = [scores(per, ref, pols, s)[:3] for pols in boots]
            ci = [sorted(v[k] for v in bs) for k in range(3)]
            fmt = lambda v, c: f"{100 * v:5.1f} ({100 * c[50]:4.1f}-{100 * c[1949]:4.1f})"
            print(s.ljust(22) + f"{rep:7d} {tp:5d} {found:6d}   " + "   ".join(fmt(v, c) for v, c in zip((P, R, F), ci)))


if __name__ == "__main__":
    report("real = contradiction or unresolved", ("contradiction", "unresolved"))
    report("strict: real = contradiction", ("contradiction",))
