import collections, concurrent.futures as cf, itertools, json, multiprocessing as mp, os, random, re, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from reasoning import OUT, load_rows
from reasoning_join import ASK, PRICE_IN, PRICE_OUT, PROMPT, ask, draw, guard_pools, one
from policyclaw.llm import make_llm

TAIL = 128
TAIL_SIZES = (8, 16, 32, 64)
PER_SIZE = 30
GROUP = 8
QUERIES = 20
SEEDS = (1, 2, 3)


def canon(query, p):
    return tuple(sorted(p)) if query == "exclusion" else tuple(p)


def tail_items():
    path = OUT / "tail_items.json"
    if path.exists():
        return json.load(open(path))
    rnd = random.Random(20261103)
    pools = {u: v for u, v in guard_pools(load_rows()).items() if len(v) >= TAIL}
    tasks = []
    for k in TAIL_SIZES:
        for n, u in enumerate(draw(sorted(pools), PER_SIZE, rnd)):
            names = rnd.sample(sorted(pools[u]), k)
            tasks.append((u, k, n, names, [pools[u][s] for s in names]))
    with mp.Pool(int(os.environ.get("WORKERS", 16))) as pool:
        items = [x for part in pool.imap(one, tasks, chunksize=2) for x in part]
    json.dump(items, open(path, "w"))
    return items


def run_tail(items):
    usage = {}
    for seed in SEEDS:
        llm = make_llm(os.environ["LLM_MODEL_NAME"], str(OUT / "llm_cache"), seed=seed)
        with cf.ThreadPoolExecutor(int(os.environ.get("THREADS", 16))) as pool:
            replies = list(pool.map(lambda it: ask(llm, it), items))
        with open(OUT / f"tail_LOW_seed{seed}.jsonl", "w") as f:
            for it, r in zip(items, replies):
                f.write(json.dumps({"id": it["id"], **r}) + "\n")
        usage[f"tail{seed}"] = llm.usage.as_dict()
    json.dump(usage, open(OUT / "tail_usage_LOW.json", "w"), indent=1)


def split_prompt(item):
    m = re.search(r"rule conditions\.\n\n(.*?)\n\nEach condition is a formula", item["prompt"], re.S)
    parts = re.split(r"(?m)^(\d+): ", m.group(1))[1:]
    lines = {parts[i]: parts[i + 1].rstrip("\n") for i in range(0, len(parts), 2)}
    ax = re.search(r"Background facts:\n(.*)\n\nList every", item["prompt"], re.S).group(1)
    return lines, ax


def batch_calls(items):
    rnd = random.Random(20261104)
    calls = []
    for it in items:
        lines, ax = split_prompt(it)
        order = sorted(lines, key=int)
        rnd.shuffle(order)
        groups = [order[i:i + GROUP] for i in range(0, len(order), GROUP)]
        for a, b in itertools.combinations(range(len(groups)), 2):
            members = groups[a] + groups[b]
            text = "\n".join(f"{i + 1}: {lines[m]}" for i, m in enumerate(members))
            calls.append({"id": it["id"], "members": [int(m) for m in members],
                          "prompt": PROMPT.format(conditions=text, axioms=ax, ask=ASK[it["query"]].format())})
    return calls


def run_batch(items):
    calls = batch_calls(items)
    llm = make_llm(os.environ["LLM_MODEL_NAME"], str(OUT / "llm_cache"), seed=1)
    with cf.ThreadPoolExecutor(int(os.environ.get("THREADS", 32))) as pool:
        replies = list(pool.map(lambda c: ask(llm, c), calls))
    found = collections.defaultdict(set)
    seconds = collections.Counter()
    for c, r in zip(calls, replies):
        seconds[c["id"]] += r["seconds"]
        n = len(c["members"])
        for a, b in r["pairs"]:
            if 1 <= a <= n and 1 <= b <= n and a != b:
                found[c["id"]].add((c["members"][a - 1], c["members"][b - 1]))
    with open(OUT / "batch_LOW_seed1.jsonl", "w") as f:
        for it in items:
            f.write(json.dumps({"id": it["id"], "pairs": sorted(found[it["id"]]), "seconds": seconds[it["id"]]}) + "\n")
    json.dump({"batch1": llm.usage.as_dict(), "calls": len(calls)}, open(OUT / "batch_usage_LOW.json", "w"), indent=1)


def tally(items, runs):
    out = {}
    groups = collections.defaultdict(list)
    for it in items:
        groups[(it["query"], it["size"])].append(it)
    for (q, k), its in sorted(groups.items()):
        tp = fp = fn = exact = 0
        by_policy = collections.defaultdict(lambda: [0, 0])
        for r in runs:
            for it in its:
                got = {canon(q, p) for p in r[it["id"]]["pairs"]}
                want = {canon(q, p) for p in it["truth"]}
                tp += len(got & want)
                fp += len(got - want)
                fn += len(want - got)
                exact += got == want
                cell = by_policy[it["id"].split("|")[0]]
                cell[0] += len(got & want)
                cell[1] += len(want)
        rnd = random.Random(1)
        cells = list(by_policy.values())
        boot = sorted(100 * sum(c[0] for c in picks) / max(sum(c[1] for c in picks), 1) for picks in (rnd.choices(cells, k=len(cells)) for _ in range(2000)))
        out[f"{q}/{k}"] = {"queries": len(its), "truth_per_query": round((tp + fn) / len(its) / len(runs), 1),
                           "precision": round(100 * tp / max(tp + fp, 1), 1), "recall": round(100 * tp / max(tp + fn, 1), 1),
                           "policies": len(cells), "recall_ci": [round(boot[50], 1), round(boot[1949], 1)], "exact_sets": round(100 * exact / len(its) / len(runs), 1),
                           "model_s": round(sum(r[i["id"]]["seconds"] for r in runs for i in its) / len(its) / len(runs), 1)}
    return out


def score():
    res = {}
    p = OUT / "tail_items.json"
    if p.exists() and (OUT / "tail_LOW_seed3.jsonl").exists():
        items = json.load(open(p))
        runs = [{r["id"]: r for r in map(json.loads, open(OUT / f"tail_LOW_seed{s}.jsonl"))} for s in SEEDS]
        res["tail"] = tally(items, runs)
    if (OUT / "batch_LOW_seed1.jsonl").exists():
        run = {r["id"]: r for r in map(json.loads, open(OUT / "batch_LOW_seed1.jsonl"))}
        items = [i for i in json.load(open(OUT / "join_items.json")) if i["id"] in run]
        res["batch"] = tally(items, [run])
        res["single_LOW"] = tally(items, [{r["id"]: r for r in map(json.loads, open(OUT / f"join_LOW_seed{s}.jsonl"))} for s in SEEDS])
        res["single_HIGH"] = tally(items, [{r["id"]: r for r in map(json.loads, open(OUT / "join_HIGH_seed1.jsonl"))}])
        u = json.load(open(OUT / "batch_usage_LOW.json"))
        v = u["batch1"]
        res["batch_calls"] = u["calls"]
        res["batch_failures"] = v["failures"]
        res["batch_dollars"] = round((v["prompt_tokens"] * PRICE_IN + (v["completion_tokens"] + v["thinking_tokens"]) * PRICE_OUT) / 1e6, 3)
        res["batch_seconds"] = round(v["seconds"], 1)
    json.dump(res, open(OUT / "batch_scores.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "score":
        return score()
    items = tail_items()
    if not (OUT / "tail_LOW_seed3.jsonl").exists():
        run_tail(items)
    print("tail done", flush=True)
    joined = json.load(open(OUT / "join_items.json"))
    chosen = []
    for q in ASK:
        chosen += [i for i in joined if i["query"] == q and i["size"] == TAIL][:QUERIES]
    run_batch(chosen)
    print("batch done", flush=True)
    score()


if __name__ == "__main__":
    main()
