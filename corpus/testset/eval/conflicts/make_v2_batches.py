import collections, json, os, random, sys, textwrap

T = "/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset"
D = f"{T}/eval/conflicts"
sys.path.insert(0, "/scratch/yz5944/nlp+privacy/PolicyClaw/vldb/analysis/error_rate")
from estimate_error import render  # noqa: E402

N, PER_BATCH, SEED = int(sys.argv[1]), 25, 20261021
record = lambda rid: rid.rsplit(".", 1)[0]


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


reported = collections.defaultdict(list)
for line in open(f"{T}/eval/conflicts.jsonl"):
    r = json.loads(line)
    if r["kind"] == "contradiction":
        reported[r["policy"]].append(r)
old = {(record(k["allow"]), record(k["deny"])): i for i, k in json.load(open(f"{D}/pair_key.json")).items()}
rng = random.Random(f"{SEED}:v2")
pols = rng.sample(sorted(reported), min(N, len(reported)))
key, new = {}, []
for pid in pols:
    p = rng.choice(reported[pid])
    x = {"policy": pid, "arm": p["arm"], "allow": p["allow"], "deny": p["deny"], "relation": p["relation"],
         "reports_in_policy": len(reported[pid]), "reused": old.get((record(p["allow"]), record(p["deny"])))}
    if x["reused"] is None:
        new.append(x)
    else:
        key[f"r-{pid}"] = x
random.Random(f"{SEED}:v2:order").shuffle(new)
os.makedirs(f"{D}/v2_batches", exist_ok=True)
for b in range(0, len(new), PER_BATCH):
    with open(f"{D}/v2_batches/v2_{b // PER_BATCH + 1:02d}.md", "w") as f:
        for j, x in enumerate(new[b:b + PER_BATCH]):
            iid = f"q{b + j + 1:04d}"
            key[iid] = x
            rows = {json.loads(l)["id"]: json.loads(l) for l in open(f"{T}/rules/{x['policy']}.jsonl")}
            segs = json.load(open(f"{T}/final_text/{x['policy']}.json"))
            segs = segs if isinstance(segs, list) else segs.get("segments", [])
            sections = {f"{x['policy']}#s{s['segment_id']}": s["text"] for s in segs}
            a, d = rows[x["allow"]], rows[x["deny"]]
            sa, sd = a["evidence"][0], d["evidence"][0]
            f.write(f"=== ITEM {iid}\nrule 1: {json.dumps(claim(a), ensure_ascii=False)}\nrule 2: {json.dumps(claim(d), ensure_ascii=False)}\n"
                    f"--- section of rule 1{' and rule 2' if sa == sd else ''}\n{wrap(sections.get(sa, ''))}\n")
            if sa != sd:
                f.write(f"--- section of rule 2\n{wrap(sections.get(sd, ''))}\n")
            f.write(f"=== END ITEM {iid}\n\n")
json.dump(key, open(f"{D}/v2_key.json", "w"), indent=1)
print(f"{len(reported)} policies with a reported contradiction, {sum(map(len, reported.values()))} reports; sampled "
      f"{len(pols)} policies: {len(new)} new items in {(len(new) + PER_BATCH - 1) // PER_BATCH} batches, "
      f"{len(pols) - len(new)} reuse first-round labels")
