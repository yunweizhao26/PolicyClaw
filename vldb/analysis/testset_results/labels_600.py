import collections, glob, json, random, re
from pathlib import Path

R = Path("/scratch/yz5944/nlp+privacy/PolicyClaw")
E = R / "corpus/testset/eval"
D = E / "conflicts"
HERE = Path(__file__).resolve().parent
ARMS = ("web", "android", "apple")
COND = {"condition", "condition_predicate"}
FIDEL = ("full", "minor", "substantial", "source_ambiguous")
N_BOOT = 2000


def ci(xs):
    xs = sorted(xs)
    return [round(xs[50], 4), round(xs[1949], 4)]


key = json.load(open(E / "batches/key.json"))
lab = {json.loads(l)["record_id"]: json.loads(l) for f in glob.glob(f"{E}/labels/*.jsonl") for l in open(f) if l.strip()}
pol = {}
for f in sorted(glob.glob(f"{E}/batches/batch_*.md")):
    txt = open(f).read()
    for m in re.finditer(r'"record_id": "(item_\d+)",\s*"polarity": "(\w+)"', txt):
        pol[m.group(1)] = m.group(2)
items = [(i, k) for i, k in key.items() if k["set"] in ARMS and i in lab]
assert len(items) == 1200 and all(i in pol for i, _ in items), (len(items), len(pol))


def kind(slots):
    s = set(slots or []) - {"none"}
    if not s:
        return "no field named"
    if s <= COND:
        return "condition fields only"
    if s <= {"polarity", "actor", "action", "attribute", "counterparty"}:
        return "flow fields only"
    return "flow and condition fields"


rng = random.Random(0)


def stat_block(arms, pred_n, pred_k):
    per = {a: collections.defaultdict(lambda: [0, 0]) for a in arms}
    for i, k in items:
        if k["set"] in arms:
            c = per[k["set"]][k["policy"]]
            c[0] += bool(pred_k(i))
            c[1] += bool(pred_n(i))
    s = sum(c[0] for a in arms for c in per[a].values())
    n = sum(c[1] for a in arms for c in per[a].values())
    boot = []
    for _ in range(N_BOOT):
        bs = bn = 0
        for a in arms:
            ps = list(per[a])
            for p in (rng.choice(ps) for _ in ps):
                bs += per[a][p][0]
                bn += per[a][p][1]
        boot.append(bs / bn if bn else 0)
    return {"count": s, "of": n, "share": round(s / n, 4) if n else None, "ci95": ci(boot)}


A = {}
types = sorted({t for l in lab.values() for t in (l.get("error_types") or [])})
for name, arms in [("all", ARMS)] + [(a, (a,)) for a in ARMS]:
    f = lambda i: lab[i]["fidelity"]
    sel = lambda i: True
    blk = {"rules": stat_block(arms, sel, sel)["of"]}
    blk["fidelity"] = {x: stat_block(arms, sel, lambda i, x=x: f(i) == x) for x in FIDEL}
    blk["substantial_by_polarity"] = {
        p: stat_block(arms, lambda i, p=p: pol[i] == p, lambda i, p=p: pol[i] == p and f(i) == "substantial") for p in ("ALLOW", "DENY")}
    sub = lambda i: f(i) == "substantial"
    blk["error_types_share_of_all_rules"] = {
        t: stat_block(arms, sel, lambda i, t=t: sub(i) and t in (lab[i].get("error_types") or [])) for t in types}
    blk["error_types_by_polarity_share_of_polarity_rules"] = {
        p: {t: stat_block(arms, lambda i, p=p: pol[i] == p,
                          lambda i, p=p, t=t: pol[i] == p and sub(i) and t in (lab[i].get("error_types") or [])) for t in types}
        for p in ("ALLOW", "DENY")}
    S = [i for i, k in items if k["set"] in arms and sub(i)]
    ct = collections.Counter(t for i in S for t in (lab[i].get("error_types") or []))
    blk["error_types_count_among_substantial"] = dict(ct.most_common())
    blk["error_types_count_among_substantial_by_polarity"] = {
        p: dict(collections.Counter(t for i in S if pol[i] == p for t in (lab[i].get("error_types") or [])).most_common())
        for p in ("ALLOW", "DENY")}
    kinds = collections.Counter(kind(lab[i].get("wrong_slots")) for i in S)
    blk["substantial_by_fields_wrong"] = dict(kinds)
    cond_n = kinds["condition fields only"] + kinds["flow and condition fields"]
    blk["substantial_involving_condition_field"] = {"count": cond_n, "of_substantial": len(S),
                                                    "share": round(cond_n / len(S), 4)}
    A[name] = blk

pkey = json.load(open(D / "pair_key.json"))
plab = {}
for f in glob.glob(f"{D}/pair_labels/*.jsonl"):
    for l in open(f):
        if l.strip():
            r = json.loads(l)
            plab[r["item"]] = r["label"]
SIZE = {"same_scope": 19, "allow_specific": 185, "deny_specific": 469, "incomparable": 8623, "exclusive": 1043, "unresolved": 7579}
CLASS = {"overlap_candidate": ("same_scope", "allow_specific", "deny_specific", "incomparable"),
         "mutually_exclusive": ("exclusive",), "unresolved": ("unresolved",), "all_pairs": tuple(SIZE)}
LABELS = sorted(set(plab.values()))
by_stratum = {s: [plab[i] for i, k in pkey.items() if s in k["strata"] and i in plab] for s in SIZE}
assert all(len(v) == (19 if s == "same_scope" else 50) for s, v in by_stratum.items())
GEN = ("contradiction", "unresolved")
metrics = {**{l: (lambda x, l=l: x == l) for l in LABELS},
           "real_conflict (contradiction or unresolved)": lambda x: x in GEN,
           "should_not_be_paired (different_practice)": lambda x: x == "different_practice",
           "extraction_error (misread)": lambda x: x == "extraction_error"}
rngb = random.Random(1)
B = {"strata": {s: {"pairs": SIZE[s], "labeled": len(v), "counts": dict(collections.Counter(v))} for s, v in by_stratum.items()},
     "classes": {}}
for c, ss in CLASS.items():
    tot = sum(SIZE[s] for s in ss)
    out = {"pairs": tot}
    for m, pred in metrics.items():
        est = sum(SIZE[s] * sum(map(pred, by_stratum[s])) / len(by_stratum[s]) for s in ss) / tot
        boot = []
        for _ in range(N_BOOT):
            v = 0
            for s in ss:
                xs = by_stratum[s]
                v += SIZE[s] * sum(pred(rngb.choice(xs)) for _ in xs) / len(xs)
            boot.append(v / tot)
        out[m] = {"share": round(est, 4), "ci95": ci(boot)}
    B["classes"][c] = out
json.dump({"A_fidelity": A, "B_pairs": B}, open(HERE / "labels_600.json", "w"), indent=1)
print("wrote", HERE / "labels_600.json")
