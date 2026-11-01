import collections, json, multiprocessing as mp, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parents[2])]
import z3
from policyclaw.guards import atoms, certain_part

OUT = HERE / "out" / "reasoning"
SAME_SPELLING = [False]
MODE = [None]


def spelled(g):
    op = g["op"]
    if op == "eq":
        return {**g, "value": " ".join(re.findall(r"[^\W_]+", g["value"].lower()))}
    if op in ("and", "or"):
        return {**g, "args": [spelled(a) for a in g["args"]]}
    if op == "not":
        return {**g, "arg": spelled(g["arg"])}
    return g


def parse(s):
    s = s.strip()
    g, i = expr(s, 0)
    if i != len(s):
        raise ValueError("trailing: " + s[i:i + 60] + " in " + s[:80])
    return spelled(g) if SAME_SPELLING[0] else g
def expr(s, i):
    if s.startswith("(", i):
        args = []; op = None; i += 1
        while True:
            a, i = expr(s, i); args.append(a)
            if s.startswith(")", i):
                return ({"op": op, "args": args} if op else args[0]), i + 1
            m = re.compile(r" (AND|OR) ").match(s, i)
            if not m:
                raise ValueError("sep: " + s[i:i + 40])
            o = m.group(1).lower()
            if op and op != o:
                raise ValueError("mixed")
            op = o; i = m.end()
    if s.startswith("NOT ", i):
        a, i = expr(s, i + 4)
        return {"op": "not", "arg": a}, i
    if s.startswith("[untranslated: ", i):
        j = i + 15
        m = re.compile(r"\](?= AND | OR |\)|$)", re.S).search(s, j)
        text = s[j:m.start()]
        return {"op": "residual", "id": " ".join(re.findall(r"[^\W_]+", text.lower()))}, m.end()
    m = re.compile(r"[^\s()]+").match(s, i)
    name = m.group(0); i = m.end()
    c = re.compile(r" (<=|>=|==|!=|<|>) (-?\d+)").match(s, i)
    if c:
        return {"op": "cmp", "var": name, "cmp": c.group(1), "value": int(c.group(2))}, c.end()
    if s.startswith(" = ", i):
        j = i + 3
        k = j; depth = 0
        while k < len(s):
            if s[k] == "(":
                depth += 1
            elif s[k] == ")":
                if depth == 0:
                    break
                depth -= 1
            elif depth == 0 and (s.startswith(" AND ", k) or s.startswith(" OR ", k)):
                break
            k += 1
        return {"op": "eq", "var": name, "value": s[j:k]}, k
    if name in ("true", "false"):
        return {"op": name}, i
    return {"op": "bool", "var": name}, i
def Z(g):
    op = g["op"]
    if op == "true": return z3.BoolVal(True)
    if op == "false": return z3.BoolVal(False)
    if op == "and": return z3.And([Z(a) for a in g["args"]])
    if op == "or": return z3.Or([Z(a) for a in g["args"]])
    if op == "not": return z3.Not(Z(g["arg"]))
    if op == "bool": return z3.Bool("b:" + g["var"])
    if op == "cmp":
        v = z3.Int("i:" + g["var"]); c = g["value"]
        return {"<": v < c, "<=": v <= c, ">": v > c, ">=": v >= c, "==": v == c, "!=": v != c}[g["cmp"]]
    if op == "eq": return z3.Bool(f"e:{g['var']}={g['value']}")
    if op == "residual": return z3.Bool("r:" + g["id"])
    raise ValueError(op)
def theory(formulas, ax_lines, derived=()):
    facts = [parse(l) for l in ax_lines]
    related = set()
    for f in facts:
        vals = [(a["var"], a["value"]) for a in atoms(f) if a["op"] == "eq"]
        for x in vals:
            for y in vals:
                related.add((x, y))
    vals = collections.defaultdict(set)
    for f in list(formulas) + facts:
        for a in atoms(f):
            if a["op"] == "eq":
                vals[a["var"]].add(a["value"])
    T = [Z(f) for f in facts]
    for v, vs in vals.items():
        if MODE[0] == "several":
            continue
        vs = sorted(vs)
        for i, a in enumerate(vs):
            for b in vs[i + 1:]:
                if ((v, a), (v, b)) not in related:
                    T.append(z3.Not(z3.And(Z({"op": "eq", "var": v, "value": a}), Z({"op": "eq", "var": v, "value": b}))))
    return T
def sat(T, *x):
    s = z3.Solver(); s.add(*T, *x)
    r = s.check()
    assert r != z3.unknown
    return r == z3.sat
def axlines(p, end):
    body = p.split("Background facts:\n", 1)[1].split(end, 1)[0]
    return [l[2:] for l in re.split(r"(?m)^(?=- )", body) if l.startswith("- ") and l[2:].strip() != "none"]
def pair(it):
    p = it["prompt"]
    m = re.search(r"Permission condition: (.*)\nProhibition condition: (.*?)\n\nEach condition", p, re.S)
    a, b = parse(m.group(1)), parse(m.group(2))
    lines = axlines(p, "\n\nChoose one")
    der = [l for l in lines if "holds exactly when" in l]
    plain = [l for l in lines if "holds exactly when" not in l]
    T = theory([a, b], plain)
    for l in der:
        T.append(z3.Bool("b:" + l.split(" holds exactly")[0]) == Z(a))
    if not sat(T, Z(a), Z(b)):
        ans = "IMPOSSIBLE"
    elif sat(T, Z(certain_part(a)), Z(certain_part(b))):
        ans = "CERTAIN"
    else:
        ans = "DEPENDS"
    return it["id"], ans == it["truth"], [ans, it["truth"], m.group(1)[:200], m.group(2)[:200], der]
def many(it):
    p = it["prompt"]
    rs = re.split(r"(?m)^R(\d+): ", p.split("one kind of data practice.\n\n", 1)[1].split("\n\nKnown facts", 1)[0])
    gs = [parse(rs[i + 1]) for i in range(1, len(rs), 2)]
    fb = p.split("current situation:\n", 1)[1].split("\n\nEach condition", 1)[0]
    fs = [parse(l[2:]) for l in re.split(r"(?m)^(?=- )", fb) if l.startswith("- ")]
    T = theory(gs + fs, axlines(p, "\n\nFor each rule"))
    T = T + [Z(f) for f in fs]
    got = []
    for g in gs:
        z = Z(g)
        got.append("APPLIES" if not sat(T, z3.Not(z)) else "EXCLUDED" if not sat(T, z) else "DEPENDS")
    return it["id"], got == it["truth"], [got, it["truth"]]
def join(it):
    p = it["prompt"]
    body = p.split("rule conditions.\n\n", 1)[1].split("\n\nEach condition is a formula", 1)[0]
    ps = re.split(r"(?m)^(\d+): ", body)
    gs = [parse(ps[i + 1]) for i in range(1, len(ps), 2)]
    if MODE[0] == "identity":
        gs = [own(g, n) for n, g in enumerate(gs)]
    T = theory(gs, axlines(p, "\n\nList every"))
    s = z3.Solver(); s.add(*T)
    zs = [Z(g) for g in gs]
    def ok(*x):
        s.push(); s.add(*x); r = s.check(); s.pop(); return r == z3.sat
    n = len(zs)
    if it["query"] == "exclusion":
        got = [[i + 1, j + 1] for i in range(n) for j in range(i + 1, n) if not ok(zs[i], zs[j])]
    else:
        got = [[i + 1, j + 1] for i in range(n) for j in range(n) if i != j and not ok(zs[i], z3.Not(zs[j]))]
    w = {tuple(x) for x in it["truth"]}; g = {tuple(x) for x in got}
    return it["id"], g == w, [sorted(g - w)[:3], sorted(w - g)[:3], len(g ^ w), len(w - g)]
def own(g, n):
    op = g["op"]
    if op == "residual":
        return {**g, "id": f"{g['id']}#{n}"}
    if op in ("and", "or"):
        return {**g, "args": [own(a, n) for a in g["args"]]}
    if op == "not":
        return {**g, "arg": own(g["arg"], n)}
    return g


def lost(it):
    _, _, diff = join(it)
    return it["query"], it["size"], len(it["truth"]), diff[3]


def assumption(mode, items):
    MODE[0] = mode
    with mp.Pool(16) as pool:
        found = pool.map(lost, items, chunksize=4)
    MODE[0] = None
    out = collections.defaultdict(lambda: [0, 0])
    for q, k, n, m in found:
        out[f"{q}/{k}"][0] += m
        out[f"{q}/{k}"][1] += n
    return {k: {"decided": v[0], "answers": v[1], "share": round(100 * v[0] / max(v[1], 1), 1)} for k, v in sorted(out.items())}


def spelling(it):
    _, _, diff = join(it)
    return len(it["truth"]), diff[2]


def safe(a):
    f, it = a
    try:
        return f(it)
    except Exception as e:
        return it["id"], None, repr(e)[:300]
def main():
    res = {}
    SAME_SPELLING[0] = False
    for name, f in (("pair_items", pair), ("many_items", many), ("join_items", join), ("tail_items", join)):
        items = json.load(open(OUT / f"{name}.json"))
        with mp.Pool(16) as pool:
            found = pool.map(safe, [(f, it) for it in items], chunksize=4)
        res[name] = {"items": len(items), "agree": sum(r[1] is True for r in found), "differ": [r[:3] for r in found if r[1] is not True][:5]}
    SAME_SPELLING[0] = True
    items = json.load(open(OUT / "join_items.json"))
    with mp.Pool(16) as pool:
        found = pool.map(spelling, items, chunksize=4)
    res["spelling"] = {"answers": sum(x[0] for x in found), "changed": sum(x[1] for x in found)}
    SAME_SPELLING[0] = False
    res["one_value"] = assumption("several", items)
    res["residual_identity"] = assumption("identity", items)
    json.dump(res, open(OUT / "prompt_check.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
