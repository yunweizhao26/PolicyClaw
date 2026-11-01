import glob, json, os, random, re, textwrap

T = "/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset"
D = f"{T}/eval/conflicts"
PER_BATCH, SEED = 20, 20261021
norm = lambda s: re.sub(r"\s+", " ", s or "").strip().lower()


def wrap(text):
    return "\n".join(textwrap.fill(l, 1500, break_long_words=False, break_on_hyphens=False) if len(l) > 1500 else l
                     for l in (text or "").split("\n"))


def sections(pid):
    segs = json.load(open(f"{T}/final_text/{pid}.json"))
    segs = segs if isinstance(segs, list) else segs.get("segments", [])
    return {f"s{s['segment_id']}": s["text"] for s in segs}


def locate(secs, st):
    q, named = norm(st.get("quote")), "s" + str(st.get("section", "")).strip("[]s ")
    if q and q in norm(secs.get(named)):
        return named, "named"
    other = next((k for k, t in secs.items() if q and q in norm(t)), None)
    return (other, "other") if other else (named, "missing")


items = []
for f in sorted(glob.glob(f"{D}/read_labels/read_*.jsonl")):
    for line in open(f):
        if not line.strip():
            continue
        row = json.loads(line)
        secs = sections(row["policy"])
        for n, c in enumerate(row["conflicts"]):
            (sp, fp), (sd, fd) = locate(secs, c["permit"]), locate(secs, c["prohibit"])
            items.append({"policy": row["policy"], "finding": n, "reader_kind": c.get("kind"), "reader_confidence": c.get("confidence"),
                          "permit": {**c["permit"], "located": sp, "found": fp}, "prohibit": {**c["prohibit"], "located": sd, "found": fd},
                          "text": (secs.get(sp, ""), secs.get(sd, ""))})
random.Random(f"{SEED}:verify").shuffle(items)
os.makedirs(f"{D}/verify_batches", exist_ok=True)
key = {}
for b in range(0, len(items), PER_BATCH):
    with open(f"{D}/verify_batches/verify_{b // PER_BATCH + 1:02d}.md", "w") as f:
        for j, x in enumerate(items[b:b + PER_BATCH]):
            iid = f"v{b + j + 1:04d}"
            ta, td = x.pop("text")
            key[iid] = x
            same = x["permit"]["located"] == x["prohibit"]["located"]
            f.write(f"=== ITEM {iid}\nstatement 1: {json.dumps(x['permit']['quote'], ensure_ascii=False)}\n"
                    f"statement 2: {json.dumps(x['prohibit']['quote'], ensure_ascii=False)}\n"
                    f"--- section of statement 1{' and statement 2' if same else ''}\n{wrap(ta)}\n")
            if not same:
                f.write(f"--- section of statement 2\n{wrap(td)}\n")
            f.write(f"=== END ITEM {iid}\n\n")
json.dump(key, open(f"{D}/verify_key.json", "w"), indent=1)
found = [x[s]["found"] for x in key.values() for s in ("permit", "prohibit")]
print(f"{len(items)} items in {(len(items) + PER_BATCH - 1) // PER_BATCH} batches; quotes found:",
      {k: found.count(k) for k in ("named", "other", "missing")})
