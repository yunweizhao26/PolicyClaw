import collections, csv, glob, json, random, sys

R = "/scratch/yz5944/nlp+privacy/PolicyClaw"
E = f"{R}/corpus/testset/eval"
BATCH, LABELS = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else (f"{E}/batches", f"{E}/labels")
FLOW = {"polarity", "actor", "action", "attribute", "counterparty"}
COND = {"condition", "condition_predicate"}
ARMS = ("web", "android", "apple")
key = json.load(open(f"{BATCH}/key.json"))
lab = {json.loads(l)["record_id"]: json.loads(l) for f in glob.glob(f"{LABELS}/*.jsonl") for l in open(f) if l.strip()}
print(f"labels for {len(lab)} of {len(key)} items")
sub = lambda f: f == "substantial"


def kind(slots):
    s = set(slots or []) - {"none"}
    if not s:
        return "no field named"
    if s <= COND:
        return "condition fields only"
    if s <= FLOW:
        return "flow fields only"
    return "flow and condition fields"


by_arm = collections.defaultdict(list)
for item, k in key.items():
    if item in lab:
        by_arm[k["set"]].append((k, lab[item]))
per = {a: collections.defaultdict(lambda: [0, 0]) for a in ARMS}
for a in ARMS:
    for k, l in by_arm[a]:
        per[a][k["policy"]][0] += sub(l["fidelity"])
        per[a][k["policy"]][1] += 1

rng = random.Random(0)
for name, arms in [(a, [a]) for a in ARMS] + [("all arms", list(ARMS))]:
    xs = [x for a in arms for x in by_arm[a]]
    if not xs:
        continue
    boot = []
    for _ in range(2000):
        s = n = 0
        for a in arms:
            pols = list(per[a])
            for p in (rng.choice(pols) for _ in pols):
                s += per[a][p][0]
                n += per[a][p][1]
        boot.append(s / n)
    boot.sort()
    S = [l for _, l in xs if sub(l["fidelity"])]
    n = len(xs)
    print(f"\n== {name}: {n} rules from {sum(len(per[a]) for a in arms)} policies; "
          f"fidelity {dict(collections.Counter(l['fidelity'] for _, l in xs))}")
    print(f"   substantial {len(S) / n:.3f} [{boot[50]:.3f}, {boot[1949]:.3f}]")
    comp = collections.Counter(kind(l.get("wrong_slots")) for l in S)
    print("   substantial, share of all rules by fields wrong:", {k: f"{v / n:.3f}" for k, v in comp.most_common()})
    print("   error types among substantial:",
          dict(collections.Counter(t for l in S for t in (l.get("error_types") or [])).most_common(10)))

final = {r["record_id"]: r for r in csv.DictReader(open(f"{R}/vldb/labels/e1_final_labels.csv"))}
xs = by_arm.get("e1", [])
if xs:
    F = [final[k["source_id"]]["fidelity"] for k, _ in xs]
    L = [l["fidelity"] for _, l in xs]
    pos = [l for f, l in zip(F, L) if sub(f)]
    neg = [l for f, l in zip(F, L) if not sub(f)]
    print(f"\nE1 check ({len(xs)} rules): exact agreement with the final labels {sum(f == l for f, l in zip(F, L)) / len(xs):.3f}; "
          f"substantial rate final {sum(map(sub, F)) / len(F):.3f}, this labeling {sum(map(sub, L)) / len(L):.3f}; "
          f"sensitivity {sum(map(sub, pos)) / max(1, len(pos)):.3f} ({len(pos)}), "
          f"specificity {sum(not sub(l) for l in neg) / max(1, len(neg)):.3f} ({len(neg)})")
