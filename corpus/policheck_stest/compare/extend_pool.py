import glob, json, random, shutil
from pathlib import Path

import make_pool as MP

HERE = Path(__file__).resolve().parent
key = json.load(open(HERE / "key.json"))
items = key["items"]
if not (HERE / "key_before_extend.json").exists():
    shutil.copy(HERE / "key.json", HERE / "key_before_extend.json")
index = {(x["policy"], MP.norm(x["permit"]), MP.norm(x["prohibit"])): i for i, x in items.items()}
reports = MP.gather()
reports["readers"] = [{"policy": r["policy"], "permit": str(c["permit"]), "prohibit": str(c["prohibit"]),
                       "source": {k: c.get(k) for k in ("kind", "confidence")}}
                      for f in sorted(glob.glob(str(HERE / "read_labels/*.jsonl"))) for line in open(f) if line.strip()
                      for r in [json.loads(line)] for c in r["conflicts"] if c.get("permit") and c.get("prohibit")]
distinct = {}
for r in reports["readers"]:
    distinct.setdefault((r["policy"], MP.norm(r["permit"]), MP.norm(r["prohibit"])), r)
reports["readers"] = list(distinct.values())
new = {}
for name, rs in sorted(reports.items()):
    key["counts"][name] = {"reports": len(rs), "labeled": len(rs)}
    for r in rs:
        k = (r["policy"], MP.norm(r["permit"]), MP.norm(r["prohibit"]))
        x = items[index[k]] if k in index else new.setdefault(
            k, {"policy": r["policy"], "permit": r["permit"], "prohibit": r["prohibit"], "systems": [], "sources": []})
        if name not in x["systems"]:
            x["systems"].append(name)
            x["sources"].append({"system": name, **r["source"]})
order = sorted(new.values(), key=lambda x: (x["policy"], MP.norm(x["permit"]), MP.norm(x["prohibit"])))
random.Random(f"{MP.SEED}:extend").shuffle(order)
first_id, first_batch = len(items) + 1, len(glob.glob(str(HERE / "batches/pool_*.md"))) + 1
missing = 0
for b in range(0, len(order), MP.PER_BATCH):
    with open(HERE / "batches" / f"pool_{first_batch + b // MP.PER_BATCH:02d}.md", "w") as f:
        for j, x in enumerate(order[b:b + MP.PER_BATCH]):
            iid = f"x{first_id + b + j:04d}"
            wa, wd = MP.write_item(f, iid, x)
            missing += (wa is None) + (wd is None)
            items[iid] = {**x, "context_found": [wa is not None, wd is not None]}
json.dump(key, open(HERE / "key.json", "w"), indent=1, ensure_ascii=False)
print(f"{len(order)} new items (x{first_id:04d} onward) in batches pool_{first_batch:02d} to "
      f"pool_{first_batch + (len(order) - 1) // MP.PER_BATCH:02d}; counts {key['counts']}; statements without context: {missing}")
