import concurrent.futures as cf, io, json, os, random, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
T = HERE.parent
R = T.parents[1]
sys.path[:0] = [str(R), str(R / "vldb/analysis/corpus_results"), str(HERE)]
import common as C  # noqa: E402
import score_f1 as S  # noqa: E402
from make_pool import SENT, norm, write_item  # noqa: E402
from policyclaw.conflicts import overlap, relation, vocabulary  # noqa: E402
from policyclaw.llm import Usage, make_llm  # noqa: E402
from policyclaw.queries import pair_outcome  # noqa: E402

PRICE_IN, PRICE_OUT = 0.75, 3.75
REAL = ("contradiction", "unresolved")
CONTRADICTION_RELATIONS = ("same scope", "permission inside prohibition")
INSTRUCTION = ('Return only JSON: {"label": one of allow, deny, no_overlap, contradiction, unresolved, '
               'different_practice, misread, "reason": at most 40 words}')
items, lab = S.items, S.lab
_policy = {}


def policy(pid):
    if pid not in _policy:
        path = T / "rules" / f"{pid}.jsonl"
        rules = [C.rule(r) for r in C.jsonl(path)] if path.exists() else []
        terms = T / "rules" / f"{pid}.terms.json"
        relations = json.load(open(terms))["relations"] if terms.exists() else {}
        segs = json.load(open(T / "final_text" / f"{pid}.json"))
        segs = segs if isinstance(segs, list) else segs.get("segments", [])
        secs = {f"{pid}#s{s['segment_id']}": norm(s["text"]) for s in segs}
        _policy[pid] = rules, vocabulary(rules, relations), secs
    return _policy[pid]


def locate(secs, statement):
    s = norm(statement)
    hit = [k for k, v in secs.items() if s and s in v]
    if hit:
        return hit, "full"
    sentences = [norm(x) for x in SENT.split(statement) if norm(x)]
    if sentences:
        longest = max(sentences, key=len)
        hit = [k for k, v in secs.items() if longest in v]
        if hit:
            return hit, "longest sentence"
    return [], "none"


def filter_item(x):
    rules, vocab, secs = policy(x["policy"])
    sec_a, how_a = locate(secs, x["permit"])
    sec_d, how_d = locate(secs, x["prohibit"])
    allow = [r for r in rules if r.polarity == "ALLOW" and r.evidence[0] in sec_a]
    deny = [r for r in rules if r.polarity == "DENY" and r.evidence[0] in sec_d]
    pairs = []
    for a in allow:
        for d in deny:
            ov = overlap(vocab, a, d)
            outcome = pair_outcome(a.guard, d.guard)["outcome"]
            rel = relation(vocab, a, d) if ov else None
            pairs.append({"allow": a.id, "deny": d.id, "overlap": ov, "outcome": outcome, "relation": rel})
    live = [p for p in pairs if p["overlap"] and p["outcome"] != "mutually_exclusive"]
    return {"sections_permit": sec_a, "sections_prohibit": sec_d, "found_permit": how_a, "found_prohibit": how_d,
            "statements_located": (how_a != "none") + (how_d != "none"), "allow_rules": len(allow), "deny_rules": len(deny),
            "pairs": len(pairs), "live_pairs": len(live),
            "lenient_keep": not (allow and deny and not live), "strict_keep": bool(live),
            "contradiction_keep": any(p["relation"] in CONTRADICTION_RELATIONS for p in live), "candidate_pairs": pairs}


def gemini_check(iid, x):
    buf = io.StringIO()
    write_item(buf, iid, x)
    prompt = (S.HERE / "pool_guide.txt").read_text() + "\n" + buf.getvalue() + "\n" + INSTRUCTION
    llm = make_llm(os.environ["LLM_MODEL_NAME"], str(HERE / "llm_cache"), seed=42)
    out = llm.json(prompt, max_tokens=2048)
    return {"label": out.get("label"), "reason": out.get("reason"), "usage": llm.usage.as_dict()}


def main():
    t0 = time.time()
    direct = sorted(i for i, x in items.items() if "direct_llm" in x["systems"])
    verified = sorted(i for i, x in items.items() if "policyclaw_verified" in x["systems"])
    print(f"direct_llm items {len(direct)}, policyclaw_verified items {len(verified)}", flush=True)

    details_b = {i: filter_item(items[i]) for i in direct}
    n_both = sum(d["statements_located"] == 2 for d in details_b.values())
    n_rules = sum(bool(d["allow_rules"] and d["deny_rules"]) for d in details_b.values())
    n_live = sum(d["strict_keep"] for d in details_b.values())
    b_counts = {"direct_llm_items": len(direct), "both_statements_located": n_both,
                "at_least_one_statement_located": sum(d["statements_located"] >= 1 for d in details_b.values()),
                "full_statement_found": sum((d["found_permit"] == "full") + (d["found_prohibit"] == "full") for d in details_b.values()),
                "longest_sentence_fallback": sum((d["found_permit"] == "longest sentence") + (d["found_prohibit"] == "longest sentence") for d in details_b.values()),
                "rules_on_both_sides": n_rules, "with_overlapping_nonexclusive_pair": n_live,
                "kept_lenient": sum(d["lenient_keep"] for d in details_b.values()),
                "kept_strict": n_live, "kept_contradiction": sum(d["contradiction_keep"] for d in details_b.values())}
    print("B matching:", json.dumps(b_counts), flush=True)

    with cf.ThreadPoolExecutor(int(os.environ.get("THREADS", 8))) as ex:
        res = list(ex.map(lambda i: gemini_check(i, items[i]), direct))
    details_c, total = {}, Usage()
    for i, r in zip(direct, res):
        for k, v in r.pop("usage").items():
            if hasattr(total, k):
                setattr(total, k, getattr(total, k) + v)
        details_c[i] = r
    cost = {"usage": total.as_dict(), "input_tokens": total.prompt_tokens,
            "output_tokens": total.completion_tokens + total.thinking_tokens,
            "dollars": (total.prompt_tokens * PRICE_IN + (total.completion_tokens + total.thinking_tokens) * PRICE_OUT) / 1e6}
    print("C usage:", json.dumps(cost), flush=True)
    c_ids = [i for i in direct if details_c[i]["label"] in REAL]

    variants = {"A": sorted(set(direct) | set(verified)),
                "B_lenient": [i for i in direct if details_b[i]["lenient_keep"]],
                "B_strict": [i for i in direct if details_b[i]["strict_keep"]],
                "B_contradiction": [i for i in direct if details_b[i]["contradiction_keep"]],
                "C": c_ids, "D": sorted(set(c_ids) | set(verified))}
    for name, ids in variants.items():
        assert set(ids) <= set(lab), name
        print(f"{name}: {len(ids)} items", flush=True)
    json.dump({"variants": variants, "details_B": details_b, "details_C": details_c, "B_counts": b_counts, "C_cost": cost},
              open(HERE / "hybrids_items.json", "w"), indent=1, ensure_ascii=False)

    for name, ids in variants.items():
        for i in ids:
            items[i]["systems"].append(name)
    systems = ("policylint", "poligraph", "policyclaw", "policyclaw_verified", "direct_llm") + tuple(variants)
    out = {}
    for name, labels in (("real = contradiction or unresolved", REAL), ("strict: real = contradiction", ("contradiction",))):
        per, gold, gold_pool = S.tables(labels)
        for ref_name, ref in (("all sources", gold), ("systems' pool only", gold_pool)):
            rng = random.Random(1)
            boots = [[rng.choice(S.policies) for _ in S.policies] for _ in range(2000)]
            head = f"{name}; reference: {ref_name}: {sum(map(len, ref.values()))} contradictions in {sum(bool(v) for v in ref.values())} policies"
            print(f"\n== {head}")
            print("system".ljust(22) + "reports  real  found   precision            recall               F1")
            table = {}
            for s in systems:
                P, Rc, F, rep, tp, found, total_gold = S.scores(per, ref, S.policies, s)
                bs = [S.scores(per, ref, pols, s)[:3] for pols in boots]
                ci = [sorted(v[k] for v in bs) for k in range(3)]
                fmt = lambda v, c: f"{100 * v:5.1f} ({100 * c[50]:4.1f}-{100 * c[1949]:4.1f})"
                print(s.ljust(22) + f"{rep:7d} {tp:5d} {found:6d}   " + "   ".join(fmt(v, c) for v, c in zip((P, Rc, F), ci)))
                table[s] = {"reports": rep, "real": tp, "found": found, "total": total_gold,
                            **{k: {"value": v, "ci95": [c[50], c[1949]]} for k, v, c in zip(("precision", "recall", "f1"), (P, Rc, F), ci)}}
            out[head] = table
    json.dump(out, open(HERE / "hybrids_scores.json", "w"), indent=1)
    print(f"\nelapsed {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
