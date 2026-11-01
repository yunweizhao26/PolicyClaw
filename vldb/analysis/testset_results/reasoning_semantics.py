import collections, itertools, json, multiprocessing as mp, re, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from reasoning import DERIVED, OUT, canon_guard, has_derived, nontrivial, render
import common as C
import z3
from policyclaw.guards import atoms, binate_residuals, drop_residual_literals, nnf, residuals, set_residuals
from policyclaw.merge import _same_practice
from policyclaw.queries import _Solver, derived_facts, pair_outcome
from policyclaw.schema import SCHEMA

LIMIT = 14


def rename(g, suffix):
    op = g["op"]
    if op == "residual":
        return {**g, "id": g["id"] + suffix}
    if op in ("and", "or"):
        return {"op": op, "args": [rename(a, suffix) for a in g["args"]]}
    if op == "not":
        return {"op": "not", "arg": rename(g["arg"], suffix)}
    return g


def several_values(g):
    op = g["op"]
    if op == "eq" and not SCHEMA.value_set(g["var"]):
        return {"op": "bool", "var": f"free::{g['var']}={g['value']}"}
    if op in ("and", "or"):
        return {**g, "args": [several_values(a) for a in g["args"]]}
    if op == "not":
        return {**g, "arg": several_values(g["arg"])}
    return g


def same_spelling(g):
    op = g["op"]
    if op == "eq" and not SCHEMA.value_set(g["var"]):
        return {**g, "value": " ".join(re.findall(r"[^\W_]+", g["value"].lower()))}
    if op in ("and", "or"):
        return {**g, "args": [same_spelling(a) for a in g["args"]]}
    if op == "not":
        return {**g, "arg": same_spelling(g["arg"])}
    return g


def kleene_outcome(a, d):
    sv = _Solver([a, d], derived_facts([d], [a]))
    true_part = [drop_residual_literals(nnf(g)) for g in (a, d)]
    false_part = [drop_residual_literals(nnf({"op": "not", "arg": g})) for g in (a, d)]
    if sv.sat(*[sv.z(g) for g in true_part]):
        return "overlap_candidate"
    if not sv.sat(*[z3.Not(sv.z(g)) for g in false_part]):
        return "mutually_exclusive"
    return "unresolved"


def fixed(a, d, value):
    env = {x["id"]: value for x in residuals(a) + residuals(d)}
    a2, d2 = set_residuals(a, env), set_residuals(d, env)
    sv = _Solver([a2, d2], derived_facts([d2], [a2]))
    return "overlap_candidate" if sv.sat(sv.z(a2), sv.z(d2)) else "mutually_exclusive"


def constant_certain(g, h):
    ids = sorted({x["id"] for x in residuals(g) + residuals(h)})
    if len(ids) > LIMIT:
        return None
    for bits in itertools.product((False, True), repeat=len(ids)):
        vals = dict(zip(ids, bits))
        g2, h2 = set_residuals(g, vals), set_residuals(h, vals)
        sv = _Solver([g2, h2], derived_facts([h2], [g2]))
        if not sv.sat(sv.z(g2), sv.z(h2)):
            return False
    return True


def oracle(a, d):
    rids = sorted({x["id"] for x in residuals(a) + residuals(d)})
    sv = _Solver([a, d], derived_facts([d], [a]))
    rs = [z3.Bool(f"residual:{i}") for i in rids]
    pa, pd = sv.z(a), sv.z(d)
    body = z3.And(pa, pd)
    for v in DERIVED:
        if any(x.get("var") == v for x in atoms(d)):
            grants = not any(x.get("var") == v for x in atoms(a))
            body = z3.substitute(body, (z3.Bool(v), pa if grants else z3.BoolVal(False)))
    s = z3.Solver()
    s.set("timeout", 20000)
    s.add(*sv.axioms)
    s.add(z3.ForAll(rs, body) if rs else body)
    r = s.check()
    return "overlap_candidate" if r == z3.sat else "not_certain" if r == z3.unsat else "unknown"


def unit_pairs(u):
    rows = C.one_per_record(C.unit_rows(u))
    allow = [r for r in rows if r["polarity"] == "ALLOW"]
    deny = [r for r in rows if r["polarity"] == "DENY"]
    out = []
    for a in allow:
        for d in deny:
            if not _same_practice(a["raw"], d["raw"], True):
                continue
            g, h = a["guard"], d["guard"]
            outcome = pair_outcome(g, h)["outcome"]
            ra, rd = {x["id"] for x in residuals(g)}, {x["id"] for x in residuals(h)}
            h2 = rename(h, "_d")
            alone = _Solver([g, h2], derived_facts([h2], [g]))
            rec = {"unit": u, "outcome": outcome, "residual": bool(ra | rd), "kleene": kleene_outcome(g, h),
                   "binate": bool(binate_residuals(g) or binate_residuals(h)),
                   "derived_plus": has_derived(g), "derived_minus": has_derived(h),
                   "unconditional": g["op"] == "true" or h["op"] == "true",
                   "identity": outcome == "mutually_exclusive" and alone.sat(alone.z(g), alone.z(h2)),
                   "several": pair_outcome(several_values(g), several_values(h))["outcome"],
                   "spelling": pair_outcome(same_spelling(g), same_spelling(h))["outcome"],
                   "oracle": oracle(g, h)}
            if outcome == "unresolved":
                rec["true"] = fixed(g, h, True)
                rec["false"] = fixed(g, h, False)
                rec["constant"] = constant_certain(g, h)
            out.append(rec)
    return out


def heads(u):
    by_op, by_data = collections.defaultdict(set), collections.defaultdict(set)
    for r in C.one_per_record(C.unit_rows(u)):
        g = canon_guard(r["guard"])
        if g["op"] != "true" and not has_derived(g):
            by_op[r["raw"].get("operation")].add(render(g))
            by_data[(r["raw"].get("operation"), str(r["raw"].get("data")))].add(render(g))
    return [len(v) for v in by_op.values()], [len(v) for v in by_data.values()]


def guard_stats(u):
    seen, kept = {}, {}
    for r in C.one_per_record(C.unit_rows(u)):
        g = canon_guard(r["guard"])
        if g["op"] != "true" and not has_derived(g):
            seen.setdefault(render(g), g)
    trivial = 0
    for s, g in seen.items():
        if nontrivial(g):
            kept[s] = g
        else:
            trivial += 1
    return u, [len(atoms(g)) for g in kept.values()], trivial, heads(u)


def main():
    C.use_testset()
    units = sorted({C.unit(v, "reconciled") for v in C.versions()})
    with mp.Pool(16) as pool:
        recs = [r for part in pool.imap_unordered(unit_pairs, units, chunksize=4) for r in part]
        stats = pool.map(guard_stats, units, chunksize=4)
    by = lambda f: dict(collections.Counter(f(r) for r in recs))
    definite = [r for r in recs if r["residual"] and r["outcome"] != "unresolved"]
    plain = [r for r in definite if not (r["outcome"] == "mutually_exclusive" and r["derived_minus"])]
    opened = [r for r in recs if r["outcome"] == "unresolved"]
    sizes = sorted(len(x[1]) for x in stats)
    flat = sorted(n for x in stats for n in x[1])
    res = {"pairs": len(recs), "outcomes": by(lambda r: r["outcome"]),
           "with_residual": sum(r["residual"] for r in recs), "binate_pairs": sum(r["binate"] for r in recs),
           "definite_with_residual": dict(collections.Counter(r["outcome"] for r in definite)),
           "definite_policies": len({r["unit"] for r in definite}),
           "definite_derived_exclusions": len(definite) - len(plain),
           "definite_without_derived": len(plain), "definite_without_derived_policies": len({r["unit"] for r in plain}),
           "derived_minus": dict(collections.Counter(r["outcome"] for r in recs if r["derived_minus"])),
           "derived_both": dict(collections.Counter(r["outcome"] for r in recs if r["derived_plus"] and r["derived_minus"])),
           "kleene_changes": dict(collections.Counter(f'{r["outcome"]} -> {r["kleene"]}' for r in recs if r["outcome"] != r["kleene"])),
           "kleene_derived": sum(r["outcome"] != r["kleene"] and r["derived_minus"] for r in recs),
           "kleene_identity": sum(r["outcome"] != r["kleene"] and r["identity"] and not r["derived_minus"] for r in recs),
           "kleene_plain": {"missed": sum(r["outcome"] != r["kleene"] and not r["derived_minus"] for r in recs), "impossible": sum(r["outcome"] == "mutually_exclusive" and not r["derived_minus"] for r in recs)},
           "identity_exclusions": sum(r["identity"] for r in recs),
           "several_values_changes": dict(collections.Counter(f'{r["outcome"]} -> {r["several"]}' for r in recs if r["outcome"] != r["several"])),
           "spelling_changes": dict(collections.Counter(f'{r["outcome"]} -> {r["spelling"]}' for r in recs if r["outcome"] != r["spelling"])),
           "derived_plus_only": sum(r["derived_plus"] and not r["derived_minus"] for r in recs),
           "oracle": dict(collections.Counter(f'{r["outcome"]} / {r["oracle"]}' for r in recs)),
           "open_true": dict(collections.Counter(r["true"] for r in opened)), "open_false": dict(collections.Counter(r["false"] for r in opened)),
           "open_readings_disagree": sum(r["true"] != r["false"] for r in opened),
           "open_constant_certain": dict(collections.Counter(str(r["constant"]) for r in opened)),
           "open_unconditional": sum(r["unconditional"] for r in opened),
           "guards_per_policy": {"median": statistics.median(sizes), "at_least": {str(k): sum(s >= k for s in sizes) for k in (8, 16, 32, 64, 128)}},
           "trivial_guards": sum(x[2] for x in stats), "kept_guards": len(flat),
           "atoms": {"median": flat[len(flat) // 2], "p95": flat[int(len(flat) * .95)], "max": flat[-1]}}
    for i, name in enumerate(("by_operation", "by_operation_and_data")):
        found = sorted(n for x in stats for n in x[3][i])
        res[name] = {"groups": len(found), "median": found[len(found) // 2], "p95": found[int(len(found) * .95)], "max": found[-1], "at_least_128": sum(n >= 128 for n in found)}
    json.dump(res, open(OUT / "semantics.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
