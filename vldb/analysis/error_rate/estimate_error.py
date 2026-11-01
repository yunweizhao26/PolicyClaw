import argparse, collections, concurrent.futures as cf, csv, hashlib, json, os, random, re, sys

sys.path.insert(0, "/scratch/yz5944/nlp+privacy/PolicyClaw")
from policyclaw.extract import extract_policy
from policyclaw.llm import make_llm

R = "/scratch/yz5944/nlp+privacy/PolicyClaw"
HR = f"{R}/local_runs/full100/human_readable"
FINAL = f"{R}/experiments/frozen_e0/annotations/final"
RUBRIC = open(f"{R}/experiments/frozen_e0/e1_rule_validation/e1_prompt_v5.txt").read()
FORMAT = """

Claim to audit, as JSON:
{claim}

Return only JSON: {{"record_id": "...", "fidelity": "full" or "minor" or "substantial" or "source_ambiguous", "wrong_slots": [...], "error_types": [...], "reason": "..."}}"""
csv.field_size_limit(10**9)


def norm(s):
    return " ".join((s or "").lower().split())


def render(g):
    op = g.get("op")
    if op in ("true", "false"):
        return op
    if op in ("and", "or"):
        parts = [render(a) for a in g["args"]]
        return parts[0] if len(parts) == 1 else "(" + f" {op.upper()} ".join(parts) + ")" if parts else "true"
    if op == "not":
        return f"NOT {render(g['arg'])}"
    if op == "cmp":
        return f"{g['var']} {g['cmp']} {g['value']}"
    if op == "eq":
        return f"{g['var']} = {g['value']}"
    if op == "residual":
        return f"[untranslated: {g.get('text', '')}]"
    return g.get("var", "")


def judge(llm, claim):
    out = llm.json(RUBRIC + FORMAT.format(claim=json.dumps(claim, ensure_ascii=False)), max_tokens=4096)
    return {"fidelity": out.get("fidelity"), "error_types": out.get("error_types") or [], "wrong_slots": out.get("wrong_slots") or [],
            "reason": out.get("reason", "")}


def policies(n, hr=HR):
    pilot = {json.loads(l)["policy"] for l in open(f"{R}/vldb/analysis/pilot/out_v2/answers.jsonl")}
    out = []
    for d in sorted(os.listdir(hr)):
        f = os.path.join(hr, d, "05_segments_v15_exact.json")
        if d in pilot or not os.path.exists(f):
            continue
        segs = json.load(open(f))
        segs = segs if isinstance(segs, list) else segs.get("segments", [])
        if segs:
            out.append((hashlib.sha256(("err" + d).encode()).hexdigest(), d, [(f"{d}#s{s['segment_id']}", s["text"]) for s in segs]))
    return [(d, segs) for _, d, segs in sorted(out)[:n]]


def section_of(span, segs):
    s = norm(span)[:150]
    for sid, text in segs:
        if s and s in norm(text):
            return text
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--policies", type=int, default=30)
    ap.add_argument("--hr", default=HR, metavar="DIR")
    ap.add_argument("--skip", type=int, default=0)
    ap.add_argument("--per-system", type=int, default=1000)
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    judge_llm = make_llm(os.environ["JUDGE_MODEL"], os.path.join(args.out, "judge_cache"), seed=42)
    if hasattr(judge_llm, "thinking_level"):
        judge_llm.thinking_level = os.environ.get("JUDGE_THINKING", "MEDIUM")
    extract_llm = make_llm(os.environ["LLM_MODEL_NAME"], os.path.join(args.out, "extract_cache"), seed=42)
    rng = random.Random(0)
    items = []

    for r in csv.DictReader(open(f"{FINAL}/review/e1_ann.csv")):
        rec = json.loads(r["record"])
        items.append({"set": "calibration", "id": r["record_id"], "policy": r["policy_name"], "human": r["fidelity"],
                      "claim": {"record_id": r["record_id"], **{k: rec.get(k, "") for k in
                                ("polarity", "actor", "action", "attribute", "counterparty", "condition", "condition_predicate")},
                                "source_segment": r["source_segment"],
                                "policy_context": "" if os.environ.get("CALIBRATION_VIEW") == "section" else r["policy_context"]}})

    pols = policies(args.policies, args.hr)[args.skip:]
    ranks = {int(re.match(r"r(\d+)_", d).group(1)): (d, segs) for d, segs in pols}
    old = []
    for line in open(f"{R}/data/longitudinal_edges/rounds/round_000/shard_00/artifacts/edges.jsonl"):
        e = json.loads(line)
        if int(e["policy_rank"]) in ranks:
            d, segs = ranks[int(e["policy_rank"])]
            text = section_of(e.get("source_segment", ""), segs)
            old.append({"set": "old", "policy": d, "context_found": bool(text), "claim": {
                "polarity": "ALLOW" if e.get("permission") not in (False, "False", "false") else "DENY",
                **{k: e.get(k, "") for k in ("actor", "action", "attribute", "counterparty", "condition", "condition_predicate")},
                "source_segment": text or e.get("source_segment", ""), "policy_context": ""}})
    with cf.ThreadPoolExecutor(int(os.environ.get("THREADS", 8))) as ex:
        extracted = list(ex.map(lambda p: extract_policy(extract_llm, p[1]), pols))
    checks = collections.Counter()
    for _, rep in extracted:
        checks.update({k: v for k, v in rep.items() if isinstance(v, int)})
        checks.update({f"completeness {k}": v for k, v in (rep.get("completeness") or {}).items()})
    new = []
    for (d, segs), (rules, _) in zip(pols, extracted):
        text_of = dict(segs)
        for r in rules:
            raw = json.loads(r.evidence[2])
            cond = "; ".join(raw.get("conditions") or [])
            if raw.get("exceptions"):
                cond += ("; " if cond else "") + "unless " + "; ".join(raw["exceptions"])
            if raw.get("purpose"):
                cond += ("; " if cond else "") + "purpose: " + "; ".join(p.get("text", "") for p in raw["purpose"])
            act = raw.get("action") or {}
            new.append({"set": "new", "policy": d, "samples": raw.get("samples"), "claim": {
                "polarity": r.polarity, "actor": (raw.get("actor") or {}).get("text", "") or r.actor,
                "action": f"{act.get('text', '')} (operation: {raw['operation']})" if raw.get("operation") else act.get("text", ""),
                "attribute": (raw.get("data") or {}).get("text", ""),
                "counterparty": (raw.get("recipient") or {}).get("text", "") or
                                ("from " + raw["source"]["text"] if isinstance(raw.get("source"), dict) and raw["source"].get("text") else ""),
                "condition": cond, "condition_predicate": render(r.guard),
                "source_segment": text_of.get(r.evidence[0], ""), "policy_context": ""}})
    new = list({json.dumps(x["claim"], sort_keys=True): x for x in new}.values())
    for group in (old, new):
        rng.shuffle(group)
        items += group[:args.per_system]
    for i, x in enumerate(items):
        x.setdefault("id", f"{x['set']}_{i}")
        x["claim"]["record_id"] = x["id"]

    with cf.ThreadPoolExecutor(int(os.environ.get("THREADS", 8))) as ex:
        verdicts = list(ex.map(lambda x: judge(judge_llm, x["claim"]), items))
    suffix = f"_{args.tag}" if args.tag else ""
    with open(os.path.join(args.out, f"judged{suffix}.jsonl"), "w") as f:
        for x, v in zip(items, verdicts):
            f.write(json.dumps({**x, "judge": v}, ensure_ascii=False) + "\n")
    json.dump({"judge": judge_llm.usage.as_dict(), "extract": extract_llm.usage.as_dict(),
               "policies": [d for d, _ in pols], "old_rules": len(old), "new_rules": len(new), "checks": dict(checks)},
              open(os.path.join(args.out, f"usage{suffix}.json"), "w"), indent=1)
    report(args.out, args.tag)


def report(out, tag=""):
    rows = [json.loads(l) for l in open(os.path.join(out, f"judged_{tag}.jsonl" if tag else "judged.jsonl"))]
    w = {r["record_id"]: float(r["sample_weight"]) for r in csv.DictReader(open(f"{FINAL}/e1/source.csv"))}
    cal = [r for r in rows if r["set"] == "calibration" and r["judge"]["fidelity"]]
    if os.environ.get("REFERENCE", "final") == "final":
        ref = {r["record_id"]: r["fidelity"] for r in csv.DictReader(open(f"{R}/vldb/labels/e1_final_labels.csv"))}
        cal = [dict(r, human=ref[r["id"]]) for r in cal]
        print("reference labels: final E1 labels (vldb/labels/e1_final_labels.csv)")
    else:
        print("reference labels: the paper's human labels")
    sub = lambda f: f == "substantial"
    tp = sum(sub(r["human"]) and sub(r["judge"]["fidelity"]) for r in cal)
    fn = sum(sub(r["human"]) and not sub(r["judge"]["fidelity"]) for r in cal)
    tn = sum(not sub(r["human"]) and not sub(r["judge"]["fidelity"]) for r in cal)
    fp = sum(not sub(r["human"]) and sub(r["judge"]["fidelity"]) for r in cal)
    sens, spec = tp / max(1, tp + fn), tn / max(1, tn + fp)
    wsum = lambda xs, pred: sum(w[x["id"]] for x in xs if pred(x)) / sum(w[x["id"]] for x in xs)
    human_rate = wsum(cal, lambda x: sub(x["human"]))
    judge_rate = wsum(cal, lambda x: sub(x["judge"]["fidelity"]))
    agree = sum(r["human"] == r["judge"]["fidelity"] for r in cal) / len(cal)
    print(f"calibration on {len(cal)} E1 rules: sensitivity {sens:.3f}, specificity {spec:.3f}, exact fidelity agreement {agree:.3f}")
    print(f"  weighted substantial rate: human {human_rate:.3f}, judge {judge_rate:.3f}")

    correct = lambda p, se, sp: min(1.0, max(0.0, (p + sp - 1) / (se + sp - 1))) if se + sp > 1 else float("nan")
    rng = random.Random(1)
    res = {}
    for s in ("old", "new"):
        xs = [r for r in rows if r["set"] == s and r["judge"]["fidelity"]]
        by_pol = collections.defaultdict(list)
        for x in xs:
            by_pol[x["policy"]].append(sub(x["judge"]["fidelity"]))
        obs = sum(sum(v) for v in by_pol.values()) / len(xs)
        res[s] = (by_pol, obs)
        types = collections.Counter(t for x in xs if sub(x["judge"]["fidelity"]) for t in x["judge"]["error_types"])
        fid = collections.Counter(x["judge"]["fidelity"] for x in xs)
        found = sum(x.get("context_found", True) for x in xs)
        print(f"\n{s} extractor: {len(xs)} rules from {len(by_pol)} policies ({found} with their section found); judge labels {dict(fid)}")
        print(f"  observed substantial {obs:.3f}, corrected {correct(obs, sens, spec):.3f}")
        print(f"  error types among substantial: {dict(types.most_common(10))}")
    pols = sorted(set(res["old"][0]) & set(res["new"][0]))
    diffs, olds, news = [], [], []
    for _ in range(2000):
        ps = [rng.choice(pols) for _ in pols]
        cs = [rng.choice(cal) for _ in cal]
        se = sum(sub(c["human"]) and sub(c["judge"]["fidelity"]) for c in cs) / max(1, sum(sub(c["human"]) for c in cs))
        sp = sum(not sub(c["human"]) and not sub(c["judge"]["fidelity"]) for c in cs) / max(1, sum(not sub(c["human"]) for c in cs))
        rate = lambda s: sum(sum(res[s][0][p]) for p in ps) / max(1, sum(len(res[s][0][p]) for p in ps))
        o, n = correct(rate("old"), se, sp), correct(rate("new"), se, sp)
        olds.append(o); news.append(n); diffs.append(n - o)
    q = lambda xs: (sorted(xs)[50], sorted(xs)[1949])
    print(f"\ncorrected substantial rate, 95% interval over policies and calibration items:")
    print(f"  old {correct(res['old'][1], sens, spec):.3f} {q(olds)}   new {correct(res['new'][1], sens, spec):.3f} {q(news)}   "
          f"new minus old {correct(res['new'][1], sens, spec) - correct(res['old'][1], sens, spec):+.3f} {q(diffs)}")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "--report":
        report(sys.argv[1], sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--tag" else "")
    else:
        main()
