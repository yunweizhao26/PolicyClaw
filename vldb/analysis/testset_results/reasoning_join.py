import collections, concurrent.futures as cf, hashlib, json, multiprocessing as mp, os, random, statistics, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from reasoning import COMMON, OUT, axioms_of, has_derived, load_rows, nontrivial, render
from policyclaw.llm import make_llm
from policyclaw.queries import _Solver

import z3

SIZES = (8, 16, 32, 64, 128)
PER_SIZE = 60
SEEDS = (1, 2, 3)
PRICE_IN, PRICE_OUT = 0.75, 3.75
BUDGET = {"HIGH": 65536}

ASK = {
    "exclusion": "List every pair of conditions that can never hold in the same situation, whatever the untranslated text means.\nReturn JSON: {{\"pairs\": [[i, j], ...]}} with i < j, where i and j are condition numbers. Return {{\"pairs\": []}} if there are none.",
    "implication": "List every ordered pair (i, j) with i != j such that, in every situation and whatever the untranslated text means, if condition i holds then condition j holds.\nReturn JSON: {{\"pairs\": [[i, j], ...]}}, where i and j are condition numbers. Return {{\"pairs\": []}} if there are none."}

PROMPT = """A privacy policy has these rule conditions.

{conditions}

""" + COMMON + """
Background facts:
{axioms}

{ask}"""


def truth(guards):
    sv = _Solver(guards)
    zs = [sv.z(g) for g in guards]
    s = z3.Solver()
    s.add(*sv.axioms)

    def sat(*extra):
        s.push()
        s.add(*extra)
        r = s.check()
        s.pop()
        if r == z3.unknown:
            raise RuntimeError("solver returned unknown")
        return r == z3.sat

    t0 = time.perf_counter()
    excl = [[i + 1, j + 1] for i in range(len(zs)) for j in range(i + 1, len(zs)) if not sat(zs[i], zs[j])]
    t1 = time.perf_counter()
    impl = [[i + 1, j + 1] for i in range(len(zs)) for j in range(len(zs)) if i != j and not sat(zs[i], z3.Not(zs[j]))]
    t2 = time.perf_counter()
    return {"exclusion": excl, "implication": impl}, {"exclusion": t1 - t0, "implication": t2 - t1}


def one(args):
    u, k, n, names, guards = args
    sets, secs = truth(guards)
    text = "\n".join(f"{i + 1}: {s}" for i, s in enumerate(names))
    ax = axioms_of(guards)
    return [{"id": f"{u}|{k}|{n}|{query}", "size": k, "query": query, "truth": sets[query], "solver_s": secs[query],
             "prompt": PROMPT.format(conditions=text, axioms=ax, ask=ASK[query].format())} for query in ASK]


def clean_pool(args):
    u, rs = args
    found = {}
    for r in rs:
        g = r["guard"]
        if g.get("op") != "true" and not has_derived(g):
            found.setdefault(render(g), g)
    kept = {s: g for s, g in found.items() if nontrivial(g)}
    return u, kept, len(found) - len(kept)


def guard_pools(rows):
    with mp.Pool(int(os.environ.get("WORKERS", 16))) as pool:
        done = pool.map(clean_pool, sorted(rows.items()), chunksize=4)
    print("guards", sum(len(d[1]) for d in done), "trivial guards removed", sum(d[2] for d in done), flush=True)
    return {u: kept for u, kept, _ in done}


def draw(pool, n, rnd):
    order = rnd.sample(pool, len(pool))
    return [order[i % len(order)] for i in range(n)]


def build(rows, rnd):
    pools = guard_pools(rows)
    tasks = []
    for k in SIZES:
        pool = sorted(u for u, v in pools.items() if len(v) >= k)
        for n, u in enumerate(draw(pool, PER_SIZE, rnd)):
            names = rnd.sample(sorted(pools[u]), k)
            tasks.append((u, k, n, names, [pools[u][s] for s in names]))
    with mp.Pool(int(os.environ.get("WORKERS", 16))) as pool:
        items = [x for part in pool.imap(one, tasks, chunksize=2) for x in part]
    return items, {str(k): sum(len(v) >= k for v in pools.values()) for k in SIZES}


def ask(llm, item):
    t0 = time.time()
    try:
        out = llm.json(item["prompt"], max_tokens=BUDGET.get(os.environ.get("GEMINI_THINKING_LEVEL"), 32768))
        pairs = out.get("pairs") or []
        return {"pairs": [[int(a), int(b)] for a, b in pairs], "seconds": time.time() - t0}
    except Exception as e:
        return {"pairs": [], "error": str(e)[:200], "seconds": time.time() - t0}


def run(items, seed, level):
    llm = make_llm(os.environ["LLM_MODEL_NAME"], str(OUT / "llm_cache"), seed=seed)
    with cf.ThreadPoolExecutor(int(os.environ.get("THREADS", 16))) as pool:
        replies = list(pool.map(lambda it: ask(llm, it), items))
    with open(OUT / f"join_{level}_seed{seed}.jsonl", "w") as f:
        for it, r in zip(items, replies):
            f.write(json.dumps({"id": it["id"], **r}) + "\n")
    return llm.usage.as_dict()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    level = os.environ.get("GEMINI_THINKING_LEVEL", "LOW")
    path = OUT / "join_items.json"
    if path.exists():
        items = json.load(open(path))
    else:
        items, counts = build(load_rows(), random.Random(20261102))
        json.dump(items, open(path, "w"))
        print("policies per size", counts)
    print("truth sizes", {f"{q}/{k}": sum(len(i["truth"]) for i in items if i["size"] == k and i["query"] == q) / PER_SIZE
                          for q in ASK for k in SIZES})
    if len(sys.argv) > 1 and sys.argv[1] == "sample":
        return
    usage = {}
    for seed in SEEDS[: int(os.environ.get("N_SEEDS", 3))]:
        usage[f"join{seed}"] = run(items, seed, level)
    json.dump(usage, open(OUT / f"join_usage_{level}.json", "w"), indent=1)
    print(json.dumps(usage))


def cached(model, prompt, seed):
    base = [model, prompt, 32768, seed]
    for b in (base, base + ["thinking=LOW"]):
        h = hashlib.sha256(json.dumps(b).encode()).hexdigest()
        p = OUT / "llm_cache" / h[:2] / f"{h}.json"
        if p.exists():
            e = json.load(open(p))
            if e.get("variant") == "thinking=LOW":
                return e
    raise KeyError(prompt[:60])


def low_thinking(items):
    model = "gemini-3.8-flash"
    cells = collections.defaultdict(lambda: [0, 0, 0])
    for s in SEEDS:
        run = {r["id"]: r for r in map(json.loads, open(OUT / f"join_LOW_seed{s}.jsonl"))}
        for it in items:
            if it["size"] != 128:
                continue
            canon = (lambda p: tuple(sorted(p))) if it["query"] == "exclusion" else tuple
            want = {canon(p) for p in it["truth"]}
            got = {canon(p) for p in run[it["id"]]["pairs"]}
            kind = "thinking" if cached(model, it["prompt"], s)["usage"].get("thinking_tokens", 0) else "none"
            c = cells[(it["query"], kind)]
            c[0] += 1
            c[1] += len(got & want)
            c[2] += len(want)
    return {f"{q}/{k}": {"calls": c[0], "recall": round(100 * c[1] / max(c[2], 1), 1)} for (q, k), c in sorted(cells.items())}


def query_dollars(items):
    kinds = {i["prompt"]: f'{i["query"]}/{i["size"]}' for i in items}
    spent = collections.Counter()
    for p in (OUT / "llm_cache").glob("*/*.json"):
        e = json.load(open(p))
        if e.get("prompt") in kinds:
            u = e["usage"]
            level = "HIGH" if "HIGH" in str(e.get("variant", "")) else "LOW"
            spent[(level, kinds[e["prompt"]])] += u.get("prompt_tokens", 0) * PRICE_IN + (u.get("completion_tokens", 0) + u.get("thinking_tokens", 0)) * PRICE_OUT
    runs = {"LOW": len(SEEDS), "HIGH": 1}
    return {level: {f"{q}/{k}": round(spent[(level, f"{q}/{k}")] / 1e6 / PER_SIZE / runs[level], 4) for q in ASK for k in SIZES} for level in runs}


def score():
    items = json.load(open(OUT / "join_items.json"))
    res = {"dollars_per_query": query_dollars(items), "low_thinking": low_thinking(items)}
    for level, seeds in (("LOW", SEEDS), ("HIGH", (1,))):
        runs = [p for s in seeds if (p := OUT / f"join_{level}_seed{s}.jsonl").exists()]
        if not runs:
            continue
        runs = [{r["id"]: r for r in map(json.loads, open(p))} for p in runs]
        table = {}
        for query in ASK:
            for k in SIZES:
                its = [i for i in items if i["query"] == query and i["size"] == k]
                tp = fp = fn = exact = fails = 0
                canon = (lambda p: tuple(sorted(p))) if query == "exclusion" else tuple
                by_policy = collections.defaultdict(lambda: [0, 0])
                for r in runs:
                    for it in its:
                        got = {canon(p) for p in r[it["id"]]["pairs"]}
                        want = {canon(p) for p in it["truth"]}
                        tp += len(got & want)
                        fp += len(got - want)
                        fn += len(want - got)
                        exact += got == want
                        fails += "error" in r[it["id"]]
                        cell = by_policy[it["id"].split("|")[0]]
                        cell[0] += len(got & want)
                        cell[1] += len(want)
                stable = sum(len({frozenset(canon(p) for p in r[it["id"]]["pairs"]) for r in runs}) == 1 for it in its)
                rnd = random.Random(1)
                cells = list(by_policy.values())
                boot = []
                for _ in range(2000):
                    picks = rnd.choices(cells, k=len(cells))
                    boot.append(100 * sum(c[0] for c in picks) / max(sum(c[1] for c in picks), 1))
                boot.sort()
                sizes = sorted(len(i["truth"]) for i in its)
                shares = sorted(100 * len({canon(p) for p in r[i["id"]]["pairs"]} & {canon(p) for p in i["truth"]}) / len(i["truth"]) for r in runs for i in its if i["truth"])
                table[f"{query}/{k}"] = {"truth_per_query": round((tp + fn) / len(its) / len(runs), 1), "truth_median": sizes[len(sizes) // 2],
                                         "policies": len(cells), "median_query_recall": round(shares[len(shares) // 2], 1) if shares else None, "recall_ci": [round(boot[50], 1), round(boot[1949], 1)],
                                         "precision": round(100 * tp / max(tp + fp, 1), 1), "recall": round(100 * tp / max(tp + fn, 1), 1),
                                         "exact_sets": round(100 * exact / len(its) / len(runs), 1), "seeds_agree": round(100 * stable / len(its), 1),
                                         "model_s": round(statistics.mean(x for x in (r[i["id"]]["seconds"] for r in runs for i in its) if x >= 0.1), 1),
                                         "solver_s": round(sum(i["solver_s"] for i in its) / len(its), 3), "failures": fails}
        res[level] = table
        usage = OUT / f"join_usage_{level}.json"
        if usage.exists():
            u = json.load(open(usage))
            res[f"{level}_dollars"] = {n: round((v["prompt_tokens"] * PRICE_IN + (v["completion_tokens"] + v["thinking_tokens"]) * PRICE_OUT) / 1e6, 3) for n, v in u.items()}
    json.dump(res, open(OUT / "join_scores.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    score() if len(sys.argv) > 1 and sys.argv[1] == "score" else main()
