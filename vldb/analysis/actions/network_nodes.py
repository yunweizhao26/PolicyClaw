import collections, json, sys

out_path, paths = sys.argv[1], sys.argv[2:]
info = collections.defaultdict(lambda: {"count": 0, "examples": []})
seen = set()
for path in paths:
    for line in open(path):
        for r in json.loads(line)["rules"]:
            key = json.dumps(r, sort_keys=True)
            if key in seen:
                continue
            seen.add(key)
            act = r.get("action") if isinstance(r.get("action"), dict) else {}
            verb = " ".join(str(act.get("verb") or "").lower().split())
            d = r.get("operation", "")
            if not verb or not d:
                continue
            x = info[(verb, d)]
            x["count"] += 1
            ex = f"\"{act.get('text', '')}\" data=\"{(r.get('data') or {}).get('text', '')}\"" + \
                 (f" recipient=\"{(r.get('recipient') or {}).get('text', '')}\"" if (r.get("recipient") or {}).get("text") else "")
            if len(x["examples"]) < 4 and ex not in x["examples"]:
                x["examples"].append(ex)
nodes = sorted(({"lemma": v, "operation": d, **x} for (v, d), x in info.items()), key=lambda n: -n["count"])
json.dump(nodes, open(out_path, "w"), indent=1, ensure_ascii=False)
verbs = collections.Counter(n["lemma"] for n in nodes)
ops = collections.Counter()
for n in nodes:
    ops[n["operation"]] += n["count"]
print(f"{len(seen)} rules, {len(nodes)} verb-operation nodes, {len(verbs)} verbs, "
      f"{sum(1 for v in verbs.values() if v > 1)} verbs under more than one operation")
print("rules per operation:", ", ".join(f"{o} {c} ({100 * c / sum(ops.values()):.1f}%)" for o, c in ops.most_common()))
print("most frequent:", ", ".join(f"{n['lemma']}@{n['operation']} {n['count']}" for n in nodes[:25]))
