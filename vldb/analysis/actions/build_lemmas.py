import collections, json

import spacy

A = "/scratch/yz5944/nlp+privacy/PolicyClaw/vldb/analysis"
SOURCES = [f"{A}/e1_recheck/runs/flash38_low_v2/predictions.jsonl", f"{A}/extraction_eval/runs/flash38_low_v2/predictions.jsonl"]
SKIP = {"may", "might", "will", "would", "can", "could", "shall", "should", "must", "do", "does", "did", "not", "never",
        "be", "is", "are", "been", "have", "has", "also", "only", "automatically", "we", "you"}
nlp = spacy.load("en_core_web_sm", disable=["ner"])

rules, seen = [], set()
for path in SOURCES:
    for line in open(path):
        for r in json.loads(line)["rules"]:
            key = json.dumps(r, sort_keys=True)
            if key not in seen:
                seen.add(key)
                rules.append(r)

quotes = [((r.get("action") or {}).get("text") or "").strip() for r in rules]
lemmas_per_rule = []
for doc in nlp.pipe([q.lower() for q in quotes], batch_size=512):
    toks = [t for t in doc if t.lower_ not in SKIP and not t.is_punct]
    verbs = [t for t in toks if t.pos_ in ("VERB", "AUX")] or toks[:1]
    heads = verbs[:1] + [t for t in verbs[1:] if t.dep_ == "conj"]
    out = []
    for h in heads:
        prt = next((t.lower_ for t in doc if t.dep_ == "prt" and t.head.i == h.i), "")
        out.append((h.lemma_.lower() + (" " + prt if prt else "")).strip())
    lemmas_per_rule.append(out)

DIRECTION = {"sell": "share"}
info = collections.defaultdict(lambda: {"count": 0, "classes": collections.Counter(), "examples": []})
quote_map = {}
for r, q, ls in zip(rules, quotes, lemmas_per_rule):
    cls = ((r.get("action") or {}).get("name") or "").lower()
    cls = DIRECTION.get(cls, cls)
    data = (r.get("data") or {}).get("text", "")
    rec = (r.get("recipient") or {}).get("text", "")
    quote_map[q.lower()] = ls
    for l in ls:
        if not l:
            continue
        d = info[(l, cls)]
        d["count"] += 1
        d["classes"][cls] += 1
        ex = f"\"{q}\" data=\"{data}\"" + (f" recipient=\"{rec}\"" if rec else "")
        if len(d["examples"]) < 4 and ex not in d["examples"]:
            d["examples"].append(ex)

out = sorted(({"lemma": l, "direction": c, "count": d["count"], "classes": dict(d["classes"]), "examples": d["examples"]}
              for (l, c), d in info.items()), key=lambda x: -x["count"])
json.dump(out, open(f"{A}/actions/lemmas.json", "w"), indent=1, ensure_ascii=False)
json.dump(quote_map, open(f"{A}/actions/quote_lemmas.json", "w"), ensure_ascii=False)
print(f"{len(rules)} rules, {len(out)} verb-direction nodes; top 20: " + ", ".join(f"{x['lemma']}@{x['direction']} {x['count']}" for x in out[:20]))
dirs = collections.defaultdict(dict)
for x in out:
    dirs[x["lemma"]][x["direction"]] = x["count"]
multi = sorted(((l, d) for l, d in dirs.items() if len(d) > 1), key=lambda t: -sum(t[1].values()))
print(f"{len(dirs)} verbs; {len(multi)} used in more than one direction, most frequent: "
      + "; ".join(f"{l} {d}" for l, d in multi[:15]))
