import csv, json, os, random, textwrap

T = "/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset"
OUT = f"{T}/eval/conflicts/read_batches"
PER_ARM, MAX_CHARS, BATCH_CHARS, SEED = 20, 120_000, 160_000, 20261021


def wrap(text):
    return "\n".join(textwrap.fill(l, 1500, break_long_words=False, break_on_hyphens=False) if len(l) > 1500 else l
                     for l in (text or "").split("\n"))


def segments(pid):
    segs = json.load(open(f"{T}/final_text/{pid}.json"))
    return segs if isinstance(segs, list) else segs.get("segments", [])


with open(f"{T}/selection.tsv", newline="", encoding="utf-8") as f:
    arms = {r["id"]: r["arm"] for r in csv.DictReader(f, delimiter="\t")}
sample, skipped = [], []
for arm in ("web", "android", "apple"):
    ids = sorted(p for p in arms if arms[p] == arm)
    random.Random(f"{SEED}:read:{arm}").shuffle(ids)
    n = 0
    for pid in ids:
        if n == PER_ARM:
            break
        chars = sum(len(s["text"]) for s in segments(pid))
        if chars > MAX_CHARS:
            skipped.append({"policy": pid, "chars": chars})
            continue
        sample.append({"policy": pid, "arm": arm, "chars": chars})
        n += 1
order = sample[:]
random.Random(f"{SEED}:read:order").shuffle(order)
os.makedirs(OUT, exist_ok=True)
batches, cur, size = [], [], 0
for x in order:
    if cur and size + x["chars"] > BATCH_CHARS:
        batches.append(cur)
        cur, size = [], 0
    cur.append(x)
    size += x["chars"]
batches.append(cur)
for b, policies in enumerate(batches, 1):
    with open(f"{OUT}/read_{b:02d}.md", "w") as f:
        for x in policies:
            x["batch"] = b
            f.write(f"=== POLICY {x['policy']}\n")
            for s in segments(x["policy"]):
                f.write(f"[s{s['segment_id']}] {wrap(s['text'])}\n")
            f.write(f"=== END POLICY {x['policy']}\n\n")
json.dump({"sample": sample, "skipped_as_too_long": skipped, "per_arm": PER_ARM, "max_chars": MAX_CHARS, "seed": SEED},
          open(f"{T}/eval/conflicts/read_key.json", "w"), indent=1)
print(f"{len(sample)} policies in {len(batches)} batches; skipped as too long: {len(skipped)}; "
      f"policies per batch: {[len(b) for b in batches]}")
