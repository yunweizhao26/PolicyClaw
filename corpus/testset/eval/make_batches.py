import csv, glob, json, os, random, sys, textwrap

R = "/scratch/yz5944/nlp+privacy/PolicyClaw"
T = f"{R}/corpus/testset"
sys.path.insert(0, f"{R}/vldb/analysis/error_rate")
from estimate_error import render  # noqa: E402  (the guard rendering the earlier rounds used)

LAST = "--last" in sys.argv
args = [a for a in sys.argv[1:] if a != "--last"]
OUT = args[0] if args else f"{T}/eval/batches"
RULES_PER_POLICY, N_E1, PER_BATCH, SEED = 2, 100, 50, 20261021
FIELDS = ("polarity", "actor", "action", "attribute", "counterparty", "condition", "condition_predicate")
csv.field_size_limit(10**9)


def claim(row, sections):
    raw = row["raw"]
    cond = "; ".join(raw.get("conditions") or [])
    if raw.get("exceptions"):
        cond += ("; " if cond else "") + "unless " + "; ".join(raw["exceptions"])
    if raw.get("purpose"):
        cond += ("; " if cond else "") + "purpose: " + "; ".join(p.get("text", "") for p in raw["purpose"])
    act = raw.get("action") or {}
    src = raw.get("source")
    return {"polarity": row["polarity"], "actor": (raw.get("actor") or {}).get("text", "") or row["actor"],
            "action": f"{act.get('text', '')} (operation: {raw['operation']})" if raw.get("operation") else act.get("text", ""),
            "attribute": (raw.get("data") or {}).get("text", ""),
            "counterparty": (raw.get("recipient") or {}).get("text", "") or
                            ("from " + src["text"] if isinstance(src, dict) and src.get("text") else ""),
            "condition": cond, "condition_predicate": render(row["guard"]),
            "source_segment": sections.get(row["evidence"][0], "")}


def wrap(text):
    return "\n".join(textwrap.fill(l, 1500, break_long_words=False, break_on_hyphens=False) if len(l) > 1500 else l
                     for l in (text or "").split("\n"))


os.makedirs(OUT, exist_ok=True)
key = json.load(open(f"{OUT}/key.json")) if os.path.exists(f"{OUT}/key.json") else {}
sample = json.load(open(f"{OUT}/sample.json")) if os.path.exists(f"{OUT}/sample.json") else \
    {"distinct_claims_per_policy": {}, "rules_per_policy": RULES_PER_POLICY, "seed": SEED, "waves": []}
done = {k["policy"] for k in key.values() if k["set"] != "e1"}
used_e1 = {k["source_id"] for k in key.values() if k["set"] == "e1"}
with open(f"{T}/selection.tsv", newline="", encoding="utf-8") as f:
    arms = {r["id"]: r["arm"] for r in csv.DictReader(f, delimiter="\t")}
items, counts = [], sample["distinct_claims_per_policy"]
policies = [p for p in sorted(arms) if os.path.exists(f"{T}/rules/{p}.jsonl") and p not in done]
for pid in policies:
    segs = json.load(open(f"{T}/final_text/{pid}.json"))
    segs = segs if isinstance(segs, list) else segs.get("segments", [])
    sections = {f"{pid}#s{s['segment_id']}": s["text"] for s in segs}
    distinct = {}
    for n, line in enumerate(open(f"{T}/rules/{pid}.jsonl")):
        c = claim(json.loads(line), sections)
        distinct.setdefault(json.dumps(c, sort_keys=True), (n, c))
    counts[pid] = len(distinct)
    rng = random.Random(f"{SEED}:{pid}")
    for n, c in rng.sample(sorted(distinct.values(), key=lambda x: x[0]), min(RULES_PER_POLICY, len(distinct))):
        items.append({"set": arms[pid], "source_id": f"{pid}:{n}", "policy": pid, "claim": c})
final = {r["record_id"]: r for r in csv.DictReader(open(f"{R}/vldb/labels/e1_final_labels.csv"))}
review = {r["record_id"]: r for r in csv.DictReader(open(f"{R}/experiments/frozen_e0/annotations/final/review/e1_review.csv"))}
e1 = [k for k in random.Random(SEED).sample(sorted(final), N_E1) if k not in used_e1]
n_e1 = len(e1) if LAST else min(len(e1), round(N_E1 * (len(done) + len(policies)) / len(arms)) - len(used_e1))
for k in e1[:max(0, n_e1)]:
    r = review[k]
    items.append({"set": "e1", "source_id": k, "policy": r["policy_name"],
                  "claim": {**{c: r[c] for c in FIELDS}, "source_segment": r["source_segment"]}})
wave = len(sample["waves"]) + 1
random.Random(f"{SEED}:wave{wave}").shuffle(items)
first_batch = len(glob.glob(f"{OUT}/batch_*.md")) + 1
for i, x in enumerate(items):
    x["item_id"] = f"item_{len(key) + i + 1:04d}"
key.update({x["item_id"]: {k: x[k] for k in ("set", "source_id", "policy")} for x in items})
batches = []
for b in range(0, len(items), PER_BATCH):
    chunk = items[b:b + PER_BATCH]
    name = f"batch_{first_batch + b // PER_BATCH:02d}"
    batches.append(name)
    with open(f"{OUT}/{name}.md", "w") as f:
        for j, x in enumerate(chunk):
            c = {"record_id": x["item_id"], **{k: x["claim"].get(k, "") for k in FIELDS}}
            f.write(f"=== ITEM {j + 1} of {len(chunk)}\nclaim: {json.dumps(c, ensure_ascii=False, indent=1)}\n"
                    f"--- source_segment\n{wrap(x['claim']['source_segment'])}\n=== END ITEM {j + 1}\n\n")
sample["waves"].append({"wave": wave, "policies": len(policies), "items": len(items), "batches": batches,
                        "e1_items": sum(x["set"] == "e1" for x in items)})
json.dump(key, open(f"{OUT}/key.json", "w"), indent=1)
json.dump(sample, open(f"{OUT}/sample.json", "w"), indent=1)
print(f"wave {wave}: {len(items)} items in batches {batches[0] if batches else '-'}..{batches[-1] if batches else '-'}; "
      f"{sum(1 for x in items if x['set'] != 'e1')} rules from {len(policies)} policies; "
      f"{sum(x['set'] == 'e1' for x in items)} E1 rules")
