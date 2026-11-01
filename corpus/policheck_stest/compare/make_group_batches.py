import collections, glob, json, os, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
PER_BATCH, SEED = 60, 20261021
REAL = ("contradiction", "unresolved")
items = json.load(open(HERE / "key.json"))["items"]
lab = {json.loads(l)["item"]: json.loads(l) for f in glob.glob(str(HERE / "labels/*.jsonl")) for l in open(f) if l.strip()}
assert set(lab) == set(items), (len(lab), len(items))
by = collections.defaultdict(list)
for i in sorted(items):
    if lab[i]["label"] in REAL:
        by[items[i]["policy"]].append(i)
multi = sorted(p for p in by if len(by[p]) > 1)
random.Random(f"{SEED}:group").shuffle(multi)
os.makedirs(HERE / "group_batches", exist_ok=True)
batches, cur, size = [], [], 0
for p in multi:
    if cur and size + len(by[p]) > PER_BATCH:
        batches.append(cur)
        cur, size = [], 0
    cur.append(p)
    size += len(by[p])
if cur:
    batches.append(cur)
for b, pols in enumerate(batches, 1):
    with open(HERE / "group_batches" / f"group_{b:02d}.md", "w") as f:
        for p in pols:
            f.write(f"=== POLICY {p}\n")
            for i in by[p]:
                f.write(f"--- {i}\nstatement 1: {json.dumps(items[i]['permit'], ensure_ascii=False)}\n"
                        f"statement 2: {json.dumps(items[i]['prohibit'], ensure_ascii=False)}\n")
            f.write(f"=== END POLICY {p}\n\n")
json.dump({"batches": {f"{b:02d}": pols for b, pols in enumerate(batches, 1)},
           "single": {p: by[p] for p in by if len(by[p]) == 1}}, open(HERE / "group_key.json", "w"), indent=1)
print(f"{sum(map(len, by.values()))} real items in {len(by)} policies; {len(multi)} policies with several items in "
      f"{len(batches)} batches; {sum(len(by[p]) == 1 for p in by)} policies with one item")
