import collections, glob, json, re, sys

import spacy

R = "/scratch/yz5944/nlp+privacy/PolicyClaw"
A = f"{R}/vldb/analysis"
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
SKIP = {"may", "might", "will", "would", "can", "could", "shall", "should", "must", "do", "does", "did", "not", "never",
        "be", "is", "are", "been", "have", "has", "also", "only", "automatically", "we", "you"}


def head_lemmas(phrases):
    out = {}
    for text, doc in zip(phrases, nlp.pipe(phrases, batch_size=512)):
        toks = [t for t in doc if t.lower_ not in SKIP and not t.is_punct]
        verbs = [t for t in toks if t.pos_ in ("VERB", "AUX")] or toks
        head = verbs[0] if verbs else None
        if head is None:
            out[text] = ""
            continue
        particle = next((t.lower_ for t in doc if t.dep_ == "prt" and t.head.i == head.i), "")
        out[text] = (head.lemma_.lower() + (" " + particle if particle else "")).strip()
    return out


def norm(s):
    return " ".join((s or "").lower().split())


def report(name, actions, names=None):
    counts = collections.Counter(norm(a) for a in actions if norm(a))
    heads = head_lemmas(list(counts))
    by_head = collections.Counter()
    for a, n in counts.items():
        by_head[heads[a]] += n
    total = sum(counts.values())
    compound = sum(n for a, n in counts.items() if re.search(r"\b(and|or)\b|,|/", a))
    print(f"\n=== {name}: {total:,} rules, {len(counts):,} distinct action strings, {len(by_head):,} distinct head verbs")
    print(f"  action strings with 'and', 'or', ',' or '/': {compound:,} rules ({100 * compound / total:.1f}%)")
    ranked = by_head.most_common()
    for k in (6, 10, 20, 50, 100):
        print(f"  top {k:3d} head verbs cover {100 * sum(n for _, n in ranked[:k]) / total:5.1f}% of rules")
    print("  most frequent head verbs:", ", ".join(f"{h} {n}" for h, n in ranked[:40]))
    singles = sum(1 for _, n in ranked if n == 1)
    print(f"  head verbs seen once: {singles:,}")
    if names:
        per = collections.defaultdict(collections.Counter)
        for a, nm in zip(actions, names):
            if norm(a):
                per[nm][heads[norm(a)]] += 1
        for nm, c in sorted(per.items(), key=lambda x: -sum(x[1].values())):
            print(f"  six-verb name '{nm}' ({sum(c.values())} rules) absorbs: " + ", ".join(f"{h} {n}" for h, n in c.most_common(18)))


e0 = []
for p in glob.glob(f"{R}/data/longitudinal_edges/rounds/round_*/shard_*/artifacts/edges.jsonl"):
    e0 += [json.loads(l).get("action", "") for l in open(p)]
report("E0 rules (old extractor, free-form action)", e0)

for label, path in (("new extractor on corpus windows (E1 recheck, Gemini 3.8 Flash)", f"{A}/e1_recheck/runs/flash38_low_v2/predictions.jsonl"),
                    ("new extractor on PolicyIE (Gemini 3.8 Flash)", f"{A}/extraction_eval/runs/flash38_low_v2/predictions.jsonl")):
    seen, quotes, names = set(), [], []
    for line in open(path):
        for r in json.loads(line)["rules"]:
            key = json.dumps(r, sort_keys=True)
            if key in seen:
                continue
            seen.add(key)
            act = r.get("action") or {}
            quotes.append(act.get("text", "") if isinstance(act, dict) else str(act))
            names.append((act.get("name", "") if isinstance(act, dict) else "").lower())
    report(label, quotes, names)
