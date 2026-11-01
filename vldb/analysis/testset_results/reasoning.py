import collections, concurrent.futures as cf, json, os, random, statistics, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parents[2]
sys.path[:0] = [str(R), str(R / "vldb/analysis/corpus_results"), str(R / "vldb/analysis/error_rate")]
import common as C
from estimate_error import render
from policyclaw.guards import Signature, atoms, residuals
from policyclaw.llm import make_llm
from policyclaw.queries import _Solver, derived_facts, pair_outcome, rule_status
from policyclaw.schema import SCHEMA

import z3

OUT = HERE / "out" / "reasoning"
DERIVED = set(SCHEMA.derived_variables())
SEEDS = (1, 2, 3)
SIZES = (2, 4, 8, 16, 32)
PER_STRATUM = 100
PER_SIZE = 100
ANSWERS = {"overlap_candidate": "CERTAIN", "mutually_exclusive": "IMPOSSIBLE", "unresolved": "DEPENDS"}
STATUS = {"applies": "APPLIES", "excluded": "EXCLUDED", "open": "DEPENDS"}

COMMON = """Each condition is a formula over variables.
The background facts hold in every situation. A variable may take any value they allow.
A name that stands alone, such as event.signup or law.required, is a Boolean variable. Each such name is its own variable, a shared prefix before the dot relates nothing, and any two of them can hold together unless a background fact relates them.
A name compared with = holds one value in each situation, and two values with different text exclude each other unless a background fact relates them. Integer variables have no bounds beyond the background facts.
Text marked [untranslated: ...] has no known meaning. Treat it as a proposition with an arbitrary truth value in each situation. It may hold in every situation, in some situations, or in no situation, and it may relate to the variables in any way. Ignore what the words suggest. Two texts with the same words, ignoring case and punctuation, are the same proposition.
"""

PAIR = """Two rules of a privacy policy have these conditions.

Permission condition: {plus}
Prohibition condition: {minus}

""" + COMMON + """
Background facts:
{axioms}

Choose one answer.
CERTAIN: whatever the untranslated text means, there is a situation in which both conditions hold.
IMPOSSIBLE: whatever the untranslated text means, no situation satisfies both conditions.
DEPENDS: neither of the above.

Return JSON: {{"answer": "CERTAIN" or "IMPOSSIBLE" or "DEPENDS"}}"""

MANY = """A privacy policy has these rules about one kind of data practice.

{rules}

Known facts about the current situation:
{facts}

""" + COMMON + """Variables that the known facts leave open may take any value.

Background facts:
{axioms}

For each rule, choose one answer.
APPLIES: its condition holds in every situation that fits the known facts, whatever the untranslated text means.
EXCLUDED: its condition holds in no situation that fits the known facts, whatever the untranslated text means.
DEPENDS: neither of the above.

Return JSON with one key per rule, for example {{"R1": "APPLIES", "R2": "DEPENDS"}}."""


def axioms_of(guards, facts=()):
    guards, facts = list(guards), list(facts)
    names = Signature(facts + guards).types
    values = {(a["var"], SCHEMA.canonical_value(a["var"], a["value"]) or a["value"])
              for g in facts + guards for a in atoms(g) if a["op"] == "eq"}
    lines = sorted({render(g) for g in SCHEMA.axioms(names) + SCHEMA.value_axioms(values)})
    return "\n".join(f"- {x}" for x in lines) or "- none"


def canon_guard(g):
    op = g["op"]
    if op == "eq":
        return {**g, "value": SCHEMA.canonical_value(g["var"], g["value"]) or g["value"]}
    if op in ("and", "or"):
        return {**g, "args": [canon_guard(a) for a in g["args"]]}
    if op == "not":
        return {**g, "arg": canon_guard(g["arg"])}
    return g


def nontrivial(g):
    sv = _Solver([g])
    z = sv.z(g)
    return sv.sat(z) and sv.sat(z3.Not(z))


def has_derived(g):
    return any(a.get("var") in DERIVED for a in atoms(g))


def load_rows():
    C.use_testset()
    rows = {}
    for v in C.versions():
        u = C.unit(v, "reconciled")
        rows[u] = [dict(r, guard=canon_guard(r["guard"])) for r in C.one_per_record(C.unit_rows(u))]
    return rows


def pair_items(rows, rnd):
    index = {r["id"]: r for rs in rows.values() for r in rs}
    strata = collections.defaultdict(dict)
    for p in map(json.loads, open(C.TESTSET_OUT / "pair_records.jsonl")):
        g, h = index[p["allow"]]["guard"], index[p["deny"]]["guard"]
        kind = "with residual" if residuals(g) + residuals(h) else "no residual"
        if p["outcome"] == "unresolved":
            kind = "untranslated" if p.get("untranslated_guard") else "partly translated"
        strata[(p["outcome"], kind)].setdefault((render(g), render(h)), (p, g, h))
    items = []
    for key in sorted(strata):
        pool = sorted(strata[key])
        for sig in rnd.sample(pool, min(PER_STRATUM, len(pool))):
            p, g, h = strata[key][sig]
            extra = ""
            if has_derived(h):
                extra = "".join(f"\n- {v} holds exactly when the permission condition holds" for v in DERIVED if any(a.get("var") == v for a in atoms(h)))
            text = PAIR.format(plus=render(g), minus=render(h), axioms=axioms_of([g, h]) + extra)
            items.append({"id": f"{p['allow']}|{p['deny']}", "stratum": " / ".join(key), "truth": ANSWERS[pair_outcome(g, h)["outcome"]], "prompt": text})
    return items, {" / ".join(k): len(v) for k, v in strata.items()}


def literal(var, kind, atoms_of_var, rnd):
    if kind == "bool":
        b = {"op": "bool", "var": var}
        return b if rnd.random() < 0.5 else {"op": "not", "arg": b}
    if kind == "cmp":
        v = rnd.choice(atoms_of_var)["value"] + rnd.choice((-1, 0, 1))
        return {"op": "cmp", "var": var, "cmp": "==", "value": v}
    return {"op": "eq", "var": var, "value": rnd.choice(atoms_of_var)["value"]}


def many_items(rows, rnd):
    groups = collections.defaultdict(dict)
    for u in sorted(rows):
        for r in rows[u]:
            g = r["guard"]
            if g.get("op") == "true" or has_derived(g):
                continue
            groups[(u, r["raw"].get("operation"))].setdefault(render(g), g)
    items = []
    for k in SIZES:
        pool = sorted(key for key, v in groups.items() if len(v) >= k)
        n = 0
        while n < PER_SIZE:
            key = rnd.choice(pool)
            guards = [groups[key][s] for s in rnd.sample(sorted(groups[key]), k)]
            by_var = collections.defaultdict(list)
            for g in guards:
                for a in atoms(g):
                    if a["op"] != "residual":
                        by_var[(a["var"], a["op"])].append(a)
            facts = []
            for (var, kind), found in sorted(by_var.items()):
                if rnd.random() < 0.3:
                    continue
                f = literal(var, kind, found, rnd)
                if _Solver(guards, facts + [f]).sat():
                    facts.append(f)
            if not facts:
                continue
            sv = _Solver(guards, facts)
            truth = [STATUS[rule_status(sv, None, g).status] for g in guards]
            lines = "\n".join(f"R{i + 1}: {render(g)}" for i, g in enumerate(guards))
            items.append({"id": f"{key[0]}|{key[1]}|{k}|{n}", "size": k, "truth": truth, "facts": len(facts),
                          "prompt": MANY.format(rules=lines, facts="\n".join(f"- {render(f)}" for f in facts), axioms=axioms_of(guards, facts))})
            n += 1
    return items


def ask(llm, item, budget):
    t0 = time.time()
    try:
        out = llm.json(item["prompt"], max_tokens=budget)
    except Exception as e:
        return {"error": str(e)[:200], "seconds": time.time() - t0}
    return {"out": out, "seconds": time.time() - t0}


def run(items, seed, tag, budget):
    llm = make_llm(os.environ["LLM_MODEL_NAME"], str(OUT / "llm_cache"), seed=seed)
    with cf.ThreadPoolExecutor(int(os.environ.get("THREADS", 16))) as pool:
        replies = list(pool.map(lambda it: ask(llm, it, budget), items))
    path = OUT / f"{tag}_{os.environ.get('GEMINI_THINKING_LEVEL', 'LOW')}_seed{seed}.jsonl"
    with open(path, "w") as f:
        for it, r in zip(items, replies):
            f.write(json.dumps({"id": it["id"], **r}) + "\n")
    return replies, llm.usage.as_dict()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    rnd = random.Random(20261101)
    pairs, sizes = pair_items(rows, rnd)
    many = many_items(rows, rnd)
    json.dump(pairs, open(OUT / "pair_items.json", "w"))
    json.dump(many, open(OUT / "many_items.json", "w"))
    json.dump(sizes, open(OUT / "strata.json", "w"), indent=1)
    print("strata", sizes)
    print("many truth", collections.Counter(x for it in many for x in it["truth"]))
    if len(sys.argv) > 1 and sys.argv[1] == "sample":
        print(pairs[0]["prompt"][:1500])
        print(many[0]["prompt"][:1500])
        return
    usage = {}
    for seed in SEEDS[: int(os.environ.get("N_SEEDS", 3))]:
        usage[f"pairs{seed}"] = run(pairs, seed, "pairs", 8192)[1]
        usage[f"many{seed}"] = run(many, seed, "many", 16384)[1]
    json.dump(usage, open(OUT / f"usage_{os.environ.get('GEMINI_THINKING_LEVEL', 'LOW')}.json", "w"), indent=1)
    print(json.dumps(usage))


if __name__ == "__main__":
    main()
