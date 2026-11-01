import collections, json, os, random, sys, textwrap

T = "/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset"
D = f"{T}/eval/conflicts"
sys.path.insert(0, "/scratch/yz5944/nlp+privacy/PolicyClaw/vldb/analysis/error_rate")
from estimate_error import render  # noqa: E402

N, CAP = int(sys.argv[1]), int(sys.argv[2])
PER_BATCH, SEED = 25, 20261021


def stratum(r):
    if r["outcome"] == "mutually_exclusive":
        return "exclusive"
    if r["outcome"] == "unresolved":
        return "unresolved"
    return {"same scope": "same_scope", "incomparable": "incomparable", "allow more specific": "allow_specific",
            "deny more specific": "deny_specific"}[r["relation"]]


def claim(row):
    raw = row["raw"]
    cond = "; ".join(raw.get("conditions") or [])
    if raw.get("exceptions"):
        cond += ("; " if cond else "") + "unless " + "; ".join(raw["exceptions"])
    field = lambda k: (raw.get(k) or {}).get("text", "") if isinstance(raw.get(k), dict) else ""
    return {"polarity": row["polarity"], "actor": field("actor"), "action": f"{field('action')} (operation: {raw.get('operation', '')})",
            "data": field("data"), "recipient": field("recipient"), "source": field("source"),
            "purpose": "; ".join(p.get("text", "") for p in raw.get("purpose") or [] if isinstance(p, dict)),
            "condition": cond, "condition_predicate": render(row["guard"])}


def wrap(text):
    return "\n".join(textwrap.fill(l, 1500, break_long_words=False, break_on_hyphens=False) if len(l) > 1500 else l
                     for l in (text or "").split("\n"))


_cache = {}


def policy(pid):
    if pid not in _cache:
        rows = {json.loads(l)["id"]: json.loads(l) for l in open(f"{T}/rules/{pid}.jsonl")}
        segs = json.load(open(f"{T}/final_text/{pid}.json"))
        segs = segs if isinstance(segs, list) else segs.get("segments", [])
        _cache.clear()
        _cache[pid] = rows, {f"{pid}#s{s['segment_id']}": s["text"] for s in segs}
    return _cache[pid]


by = collections.defaultdict(lambda: collections.defaultdict(list))
for l in open(f"{T}/eval/conflict_pairs.jsonl"):
    r = json.loads(l)
    by[stratum(r)][r["policy"]].append(r)
chosen = []
for s in ("same_scope", "incomparable", "allow_specific", "deny_specific", "unresolved", "exclusive"):
    rng = random.Random(f"{SEED}:{s}")
    if s == "same_scope":
        pool = [r for p in sorted(by[s]) for r in by[s][p]]
        picks = rng.sample(pool, min(CAP, len(pool)))
    else:
        pols = rng.sample(sorted(by[s]), min(N, len(by[s])))
        picks = [rng.choice(by[s][p]) for p in pols]
    chosen += [(s, r) for r in picks]
items, seen = [], {}
for s, r in sorted(chosen, key=lambda x: x[1]["policy"]):
    rows, sections = policy(r["policy"])
    a, d = rows[r["allow"]], rows[r["deny"]]
    k = json.dumps([r["policy"], claim(a), claim(d)], sort_keys=True)
    if k in seen:
        seen[k]["strata"].append(s)
        continue
    x = {"strata": [s], "policy": r["policy"], "arm": r["arm"], "allow": r["allow"], "deny": r["deny"],
         "text": (claim(a), claim(d), a["evidence"][0], d["evidence"][0], sections.get(a["evidence"][0], ""),
                  sections.get(d["evidence"][0], ""))}
    seen[k] = x
    items.append(x)
random.Random(f"{SEED}:pairs").shuffle(items)
os.makedirs(f"{D}/pair_batches", exist_ok=True)
key = {}
for b in range(0, len(items), PER_BATCH):
    with open(f"{D}/pair_batches/pair_{b // PER_BATCH + 1:02d}.md", "w") as f:
        for j, x in enumerate(items[b:b + PER_BATCH]):
            iid = f"p{b + j + 1:04d}"
            ca, cd, sa, sd, ta, td = x.pop("text")
            key[iid] = x
            f.write(f"=== ITEM {iid}\nrule 1: {json.dumps(ca, ensure_ascii=False)}\nrule 2: {json.dumps(cd, ensure_ascii=False)}\n"
                    f"--- section of rule 1{' and rule 2' if sa == sd else ''}\n{wrap(ta)}\n")
            if sa != sd:
                f.write(f"--- section of rule 2\n{wrap(td)}\n")
            f.write(f"=== END ITEM {iid}\n\n")
json.dump(key, open(f"{D}/pair_key.json", "w"), indent=1)
print(f"{len(items)} items in {(len(items) + PER_BATCH - 1) // PER_BATCH} batches;",
      dict(collections.Counter(s for x in key.values() for s in x["strata"])),
      "pairs per stratum:", {s: sum(map(len, by[s].values())) for s in by}, "policies per stratum:", {s: len(by[s]) for s in by})
