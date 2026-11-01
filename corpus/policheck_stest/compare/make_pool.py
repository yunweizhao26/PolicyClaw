import collections, csv, json, os, random, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
T = HERE.parent
PER_BATCH, SEED, WINDOW = 20, 20261021, 900
norm = lambda s: re.sub(r"\s+", " ", s or "").strip().lower()
SENT = re.compile(r"(?<=[.!?;:])\s+|\n+")


def text(pid):
    return (T / "texts" / f"{pid}.visible.txt").read_text(encoding="utf-8")


def window(body, statement):
    flat = re.sub(r"\s+", " ", body)
    spans = []
    for line in filter(None, (l.strip() for l in statement.split("\n"))):
        i = flat.lower().find(norm(line)[:200])
        if i >= 0:
            spans.append([max(0, i - WINDOW), min(len(flat), i + len(line) + WINDOW)])
    if not spans:
        return None
    spans.sort()
    merged = [spans[0]]
    for a, b in spans[1:]:
        if a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return "\n[...]\n".join(("... " if a else "") + flat[a:b] + (" ..." if b < len(flat) else "") for a, b in merged)


def rule_sentence(pid, row, sections):
    sec = sections.get(row["evidence"][0], "")
    raw = row["raw"]
    words = [norm((raw.get(k) or {}).get("text")) for k in ("action", "data")] + [norm(raw.get("polarity_text"))]
    words = [w for w in words if w]
    for s in SENT.split(sec):
        if words and all(w in norm(s) for w in words[:2]):
            return s.strip()
    for s in SENT.split(sec):
        if words and words[-1] in norm(s):
            return s.strip()
    return sec.strip()


def policyclaw():
    out = collections.defaultdict(list)
    rules, secs = {}, {}
    reports = [("policyclaw", r) for r in map(json.loads, open(T / "eval/conflicts.jsonl")) if r["kind"] == "contradiction"]
    reports += [("policyclaw_before", r) for r in map(json.loads, open(T / "eval/conflict_pairs.jsonl"))
                if r["outcome"] == "overlap_candidate" and r["relation"] == "same scope"]
    reports += [("policyclaw_verified", r) for r in map(json.loads, open(T / "eval/conflicts_verified.jsonl"))
                if r["verify_label"] in ("contradiction", "unresolved")]
    for name, r in reports:
        pid = r["policy"]
        if pid not in rules:
            rules[pid] = {json.loads(l)["id"]: json.loads(l) for l in open(T / "rules" / f"{pid}.jsonl")}
            segs = json.load(open(T / "final_text" / f"{pid}.json"))
            segs = segs if isinstance(segs, list) else segs.get("segments", [])
            secs[pid] = {f"{pid}#s{s['segment_id']}": s["text"] for s in segs}
        out[name].append({"policy": pid, "permit": rule_sentence(pid, rules[pid][r["allow"]], secs[pid]),
                          "prohibit": rule_sentence(pid, rules[pid][r["deny"]], secs[pid]),
                          "source": {"allow": r["allow"], "deny": r["deny"], "relation": r["relation"]}})
    return out


def baseline(path, name, keep=lambda r: True):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    side = lambda r, s: r.get(f"{s}_sentence_visible") or r[f"{s}_sentence"]
    return {name: [{"policy": r["policy_id"], "permit": side(r, "positive"), "prohibit": side(r, "negative"),
                    "source": {k: v for k, v in r.items() if not k.endswith(("_sentence", "_sentence_visible"))}}
                   for r in rows if keep(r)]}


def direct():
    out = []
    for f in sorted((T / "direct").glob("*.json")):
        r = json.load(open(f))
        out += [{"policy": r["policy"], "permit": str(c["permit"]), "prohibit": str(c["prohibit"]),
                 "source": {k: c.get(k) for k in ("kind", "confidence")}} for c in r["conflicts"]]
    return {"direct_llm": out}


def gather():
    reports = {**policyclaw(), **direct(),
               **baseline(T / "baselines/policylint/contradictions.csv", "policylint", lambda r: r["type"].startswith("C")),
               **baseline(T / "baselines/poligraph/contradictions_normalized.csv", "poligraph")}
    out = {}
    for name, rs in reports.items():
        distinct = {}
        for r in rs:
            distinct.setdefault((r["policy"], norm(r["permit"]), norm(r["prohibit"])), r)
        out[name] = list(distinct.values())
    return out


def write_item(f, iid, x):
    body = text(x["policy"])
    wa, wd = window(body, x["permit"]), window(body, x["prohibit"])
    f.write(f"=== ITEM {iid}\nstatement 1: {json.dumps(x['permit'], ensure_ascii=False)}\n"
            f"statement 2: {json.dumps(x['prohibit'], ensure_ascii=False)}\n"
            f"--- policy text around statement 1\n{wa or x['permit']}\n"
            f"--- policy text around statement 2\n{wd or x['prohibit']}\n=== END ITEM {iid}\n\n")
    return wa, wd


def main():
    CAP = int(sys.argv[1])
    items, key, counts = {}, {}, {}
    for name, rs in sorted(gather().items()):
        rng = random.Random(f"{SEED}:{name}")
        picked = rng.sample(rs, min(CAP, len(rs)))
        counts[name] = {"reports": len(rs), "labeled": len(picked)}
        for r in picked:
            k = (r["policy"], norm(r["permit"]), norm(r["prohibit"]))
            x = items.setdefault(k, {"policy": r["policy"], "permit": r["permit"], "prohibit": r["prohibit"], "systems": [], "sources": []})
            x["systems"].append(name)
            x["sources"].append({"system": name, **r["source"]})
    order = sorted(items.values(), key=lambda x: (x["policy"], norm(x["permit"]), norm(x["prohibit"])))
    random.Random(f"{SEED}:pool").shuffle(order)
    os.makedirs(HERE / "batches", exist_ok=True)
    missing = 0
    for b in range(0, len(order), PER_BATCH):
        with open(HERE / "batches" / f"pool_{b // PER_BATCH + 1:02d}.md", "w") as f:
            for j, x in enumerate(order[b:b + PER_BATCH]):
                iid = f"x{b + j + 1:04d}"
                wa, wd = write_item(f, iid, x)
                missing += (wa is None) + (wd is None)
                key[iid] = {**x, "context_found": [wa is not None, wd is not None]}
    json.dump({"counts": counts, "items": key}, open(HERE / "key.json", "w"), indent=1, ensure_ascii=False)
    print(f"{len(order)} items in {(len(order) + PER_BATCH - 1) // PER_BATCH} batches; reports {counts}; "
          f"items reported by several systems: {sum(len(set(x['systems'])) > 1 for x in order)}; statements without context: {missing}")


if __name__ == "__main__":
    main()
