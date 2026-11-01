import collections, csv, glob, json, os, random, re

T = "/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset"
D = f"{T}/eval/conflicts"
GENUINE = ("contradiction", "unresolved")
SYSTEM = {"same_scope": "conflict", "incomparable": "deny", "allow_specific": "allow", "deny_specific": "deny",
          "exclusive": "no_overlap", "unresolved": "undecided"}
STRATA = tuple(SYSTEM)
norm = lambda s: re.sub(r"\s+", " ", s or "").strip().lower()


def labels(sub):
    out = {}
    for f in glob.glob(f"{D}/{sub}/*.jsonl"):
        for line in open(f):
            if line.strip():
                r = json.loads(line)
                out[r["item"]] = r
    return out


def pairs_part():
    key, lab = json.load(open(f"{D}/pair_key.json")), labels("pair_labels")
    print(f"== Part 1: {len(lab)} of {len(key)} pair items labeled")
    pop = collections.defaultdict(collections.Counter)
    for line in open(f"{T}/eval/conflict_pairs.jsonl"):
        r = json.loads(line)
        s = "exclusive" if r["outcome"] == "mutually_exclusive" else "unresolved" if r["outcome"] == "unresolved" else \
            {"same scope": "same_scope", "incomparable": "incomparable", "allow more specific": "allow_specific",
             "deny more specific": "deny_specific"}[r["relation"]]
        pop[s][r["policy"]] += 1
    cols = ("allow", "deny", "no_overlap", "contradiction", "unresolved", "different_practice", "extraction_error")
    print("stratum".ljust(15) + "system".ljust(11) + "pairs".rjust(7) + "labeled".rjust(8) + "".join(c[:12].rjust(13) for c in cols))
    for s in STRATA:
        its = [(i, k) for i, k in key.items() if s in k["strata"] and i in lab]
        c = collections.Counter(lab[i]["label"] for i, _ in its)
        print(s.ljust(15) + SYSTEM[s].ljust(11) + str(sum(pop[s].values())).rjust(7) + str(len(its)).rjust(8) +
              "".join(str(c[x]).rjust(13) for x in cols))
    print("\nper stratum: genuine share of labeled pairs; agreement where the text decides (allow or deny); "
          "estimated genuine pairs in the stratum (95% bootstrap interval)")
    rng = random.Random(1)
    for s in STRATA:
        its = [(lab[i]["label"], k["policy"]) for i, k in key.items() if s in k["strata"] and i in lab]
        if not its:
            continue
        g = sum(l in GENUINE for l, _ in its)
        dec = [l for l, _ in its if l in ("allow", "deny")]
        agree = sum(l == SYSTEM[s] for l in dec)
        line = f"{s:15s} genuine {g}/{len(its)} ({100 * g / len(its):.1f}%); agreement {agree}/{len(dec)}"
        if s != "same_scope":
            P, m = len(pop[s]), len(its)
            vals = [pop[s][p] * (l in GENUINE) for l, p in its]
            est = P / m * sum(vals)
            boot = sorted(P / m * sum(rng.choice(vals) for _ in vals) for _ in range(2000))
            line += f"; estimated {est:.0f} of {sum(pop[s].values())} pairs ({boot[50]:.0f} to {boot[1949]:.0f})"
        print(line)
    print("\ngenuine pairs (label, stratum, policy, reason):")
    for i, k in sorted(key.items()):
        if i in lab and lab[i]["label"] in GENUINE:
            print(f"  {i} {lab[i]['label']:13s} {'+'.join(k['strata']):15s} {k['policy']:12s} {lab[i]['reason']}")


def rule_index(pid):
    rows = [json.loads(l) for l in open(f"{T}/rules/{pid}.jsonl")]
    return rows


def matches(rows, pid, st, polarity):
    sec, q = f"{pid}#{st['located']}", norm(st["quote"])
    out = set()
    for r in rows:
        raw = r["raw"]
        if r["evidence"][0] != sec or r["polarity"] != polarity:
            continue
        data = norm((raw.get("data") or {}).get("text"))
        act = norm((raw.get("action") or {}).get("text")) or norm(raw.get("polarity_text"))
        if data and act and data in q and act in q:
            out.add(r["id"].rsplit(".", 1)[0])
    return out


def reading_part():
    if not os.path.exists(f"{D}/read_key.json"):
        return
    sample = json.load(open(f"{D}/read_key.json"))["sample"]
    read = {}
    for f in glob.glob(f"{D}/read_labels/*.jsonl"):
        for line in open(f):
            if line.strip():
                r = json.loads(line)
                read[r["policy"]] = r["conflicts"]
    arms = {x["policy"]: x["arm"] for x in sample}
    print(f"\n== Part 2: {len(read)} of {len(sample)} policies read")
    for arm in ("web", "android", "apple", None):
        ps = [p for p in read if arm in (None, arms[p])]
        n = [len(read[p]) for p in ps]
        print(f"{arm or 'all':8s} policies {len(ps)}, with a reported conflict {sum(x > 0 for x in n)}, conflicts {sum(n)}, "
              f"by kind {dict(collections.Counter(c.get('kind') for p in ps for c in read[p]))}")
    if not os.path.exists(f"{D}/verify_key.json"):
        return
    key, lab = json.load(open(f"{D}/verify_key.json")), labels("verify_labels")
    print(f"{len(lab)} of {len(key)} reported conflicts checked by a second annotator: "
          f"{dict(collections.Counter(l['label'] for l in lab.values()))}")
    kinds = collections.Counter((k["reader_kind"], lab[i]["label"]) for i, k in key.items() if i in lab)
    print("reader kind x second label:", dict(kinds))
    pairs = collections.defaultdict(list)
    for line in open(f"{T}/eval/conflict_pairs.jsonl"):
        r = json.loads(line)
        if r["policy"] in read:
            pairs[r["policy"]].append(r)
    confirmed = [(i, k) for i, k in sorted(key.items()) if i in lab and lab[i]["label"] in GENUINE]
    print(f"\nconfirmed conflicts: {len(confirmed)} in {len({k['policy'] for _, k in confirmed})} policies; what the system has:")
    outcome = collections.Counter()
    for i, k in confirmed:
        rows = rule_index(k["policy"])
        a, d = matches(rows, k["policy"], k["permit"], "ALLOW"), matches(rows, k["policy"], k["prohibit"], "DENY")
        if not a or not d:
            o = "no rule for " + " and ".join(s for s, m in (("permit", a), ("prohibit", d)) if not m)
        else:
            hit = [r for r in pairs[k["policy"]] if r["allow"].rsplit(".", 1)[0] in a and r["deny"].rsplit(".", 1)[0] in d]
            if not hit:
                o = "rules, no pair"
            else:
                rank = ("same scope", "unresolved", "incomparable", "allow more specific", "deny more specific",
                        "policy exception", "exclusive guards")
                best = min(hit, key=lambda r: rank.index("unresolved" if r["outcome"] == "unresolved" else r["relation"]))
                o = "pair: " + ("unresolved (untranslated text)" if best["outcome"] == "unresolved" else best["relation"])
        outcome[o] += 1
        print(f"  {i} {k['policy']:12s} {lab[i]['label']:13s} {o:40s} | {k['permit']['quote'][:90]!r} || {k['prohibit']['quote'][:90]!r}")
    print("system outcome for confirmed conflicts:", dict(outcome.most_common()))
    loose = collections.Counter()
    for i, k in confirmed:
        rows, pid = rule_index(k["policy"]), k["policy"]
        sa, sd = f"{pid}#{k['permit']['located']}", f"{pid}#{k['prohibit']['located']}"
        has_a = any(r["evidence"][0] == sa and r["polarity"] == "ALLOW" for r in rows)
        has_d = any(r["evidence"][0] == sd and r["polarity"] == "DENY" for r in rows)
        sec = lambda rid: rid.rsplit(".", 2)[0]
        hit = [r for r in pairs[pid] if sec(r["allow"]) == sa and sec(r["deny"]) == sd]
        if not (has_a and has_d):
            loose["section lacks an ALLOW or DENY rule"] += 1
        elif not hit:
            loose["rules in both sections, no pair between them"] += 1
        else:
            loose["a pair between the two sections: " + ", ".join(sorted({"unresolved" if r["outcome"] == "unresolved" else r["relation"] for r in hit}))] += 1
    print("section-level upper bound:", dict(loose.most_common()))


if __name__ == "__main__":
    pairs_part()
    reading_part()
