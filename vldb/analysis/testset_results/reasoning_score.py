import collections, json, math, random
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out" / "reasoning"
PAIR = ("CERTAIN", "IMPOSSIBLE", "DEPENDS")
RULE = ("APPLIES", "EXCLUDED", "DEPENDS")
PRICE_IN, PRICE_OUT = 0.75, 3.75


def replies(tag, level, seed):
    path = OUT / f"{tag}_{level}_seed{seed}.jsonl"
    return {r["id"]: r for r in map(json.loads, open(path))} if path.exists() else None


def pair_answer(reply):
    a = str((reply.get("out") or {}).get("answer", "")).strip().upper()
    return a if a in PAIR else "NONE"


def rule_answers(reply, n):
    out = reply.get("out") or {}
    got = [str(out.get(f"R{i + 1}", "")).strip().upper() for i in range(n)]
    return [a if a in RULE else "NONE" for a in got]


def ci(hits, n, trials=2000):
    rnd = random.Random(1)
    vals = sorted(sum(rnd.random() < hits / n for _ in range(n)) / n for _ in range(trials))
    return round(100 * vals[int(0.025 * trials)], 1), round(100 * vals[int(0.975 * trials)], 1)


def pct(a, b):
    return round(100 * a / b, 1) if b else None


def score_pairs(items, level, seeds):
    runs = [replies("pairs", level, s) for s in seeds]
    runs = [r for r in runs if r]
    res = {}
    groups = collections.defaultdict(list)
    for it in items:
        groups[it["stratum"]].append(it)
    groups["all"] = items
    for name, its in groups.items():
        right = [sum(pair_answer(r[it["id"]]) == it["truth"] for it in its) for r in runs]
        conf = collections.Counter((it["truth"], pair_answer(r[it["id"]])) for r in runs for it in its)
        stable = sum(len({pair_answer(r[it["id"]]) for r in runs}) == 1 for it in its)
        res[name] = {"n": len(its), "accuracy_by_seed": [pct(x, len(its)) for x in right],
                     "accuracy": pct(sum(right), len(its) * len(runs)),
                     "all_seeds_agree": pct(stable, len(its)),
                     "answers": {f"{a}->{b}": v for (a, b), v in sorted(conf.items())}}
    return res


def score_many(items, level, seeds):
    runs = [replies("many", level, s) for s in seeds]
    runs = [r for r in runs if r]
    res = {}
    for k in sorted({it["size"] for it in items}):
        its = [it for it in items if it["size"] == k]
        rules = whole = stable = 0
        conf = collections.Counter()
        for r in runs:
            for it in its:
                got = rule_answers(r[it["id"]], k)
                rules += sum(a == b for a, b in zip(got, it["truth"]))
                whole += got == it["truth"]
                conf.update(zip(it["truth"], got))
        for it in its:
            stable += len({tuple(rule_answers(r[it["id"]], k)) for r in runs}) == 1
        total = sum(len(it["truth"]) for it in its) * len(runs)
        res[str(k)] = {"queries": len(its), "rule_accuracy": pct(rules, total), "query_correct": pct(whole, len(its) * len(runs)),
                       "all_seeds_agree": pct(stable, len(its)),
                       "answers": {f"{a}->{b}": v for (a, b), v in sorted(conf.items())},
                       "majority_rule_accuracy": pct(max(collections.Counter(x for it in its for x in it["truth"]).values()), total / len(runs))}
    return res


def cost(level):
    path = OUT / f"usage_{level}.json"
    if not path.exists():
        return None
    u = json.load(open(path))
    out = {}
    for name, v in u.items():
        d = (v["prompt_tokens"] * PRICE_IN + (v["completion_tokens"] + v["thinking_tokens"]) * PRICE_OUT) / 1e6
        out[name] = {"dollars": round(d, 3), "calls": v["calls"], "cached": v["cached"], "failures": v["failures"],
                     "dollars_per_call": round(d / max(v["calls"], 1), 6), "seconds_per_call": round(v["seconds"] / max(v["calls"], 1), 2)}
    return out


def main():
    pairs = json.load(open(OUT / "pair_items.json"))
    many = json.load(open(OUT / "many_items.json"))
    res = {}
    for level, seeds in (("LOW", (1, 2, 3)), ("HIGH", (1,))):
        if not (OUT / f"pairs_{level}_seed1.jsonl").exists():
            continue
        res[level] = {"pairs": score_pairs(pairs, level, seeds), "many": score_many(many, level, seeds), "cost": cost(level)}
    json.dump(res, open(OUT / "scores.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
