import collections, glob, json, os, random, sys

D = os.path.dirname(os.path.abspath(__file__))
T = "/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset"
sys.path.insert(0, D)
import score_conflicts as S  # noqa: E402

REAL = S.GENUINE
record = lambda rid: rid.rsplit(".", 1)[0]
section = lambda rid: rid.rsplit(".", 2)[0]

NAME = sys.argv[1] if len(sys.argv) > 1 else "conflicts"
pairs = [json.loads(l) for l in open(f"{T}/eval/{NAME}.jsonl")]
summary = json.load(open(f"{T}/eval/{NAME}.json"))
print("== Reports of the conflict check")
for arm in ("web", "android", "apple", "all"):
    s = summary[arm]
    print(f"{arm:8s} policies {s['policies']}, with term relations {s['policies_with_term_relations']}, compared pairs "
          f"{s['pairs']}, kinds {s['kinds']}, policies with a contradiction {s['policies_with_a_contradiction']}")
reported = collections.Counter(p["policy"] for p in pairs if p["kind"] == "contradiction")

if os.path.exists(f"{D}/v2_key.json"):
    key = json.load(open(f"{D}/v2_key.json"))
    lab = S.labels("v2_labels")
    first = S.labels("pair_labels")
    got = {}
    for i, k in key.items():
        l = first.get(k["reused"]) if k["reused"] else lab.get(i)
        if l:
            got[k["policy"]] = (l["label"], k)
    print(f"\n== False positives: {len(got)} of {len(key)} sampled policies labeled")
    c = collections.Counter(l for l, _ in got.values())
    print("labels:", dict(c.most_common()))
    vals = [(k["reports_in_policy"], l in REAL) for l, k in got.values()]
    if vals:
        m, P, total = len(vals), len(reported), sum(reported.values())
        share = lambda vs: P / len(vs) * sum(n * y for n, y in vs) / total
        rng = random.Random(1)
        boot = sorted(share([rng.choice(vals) for _ in vals]) for _ in range(2000))
        k = sum(y for _, y in vals)
        print(f"real per sampled policy: {k}/{m} ({100 * k / m:.1f}%); real share of all {total} reports "
              f"{100 * share(vals):.1f}% ({100 * boot[50]:.1f} to {100 * boot[1949]:.1f}); "
              f"strictly contradiction {c['contradiction']}/{m}")
        print("by arm:", {arm: f"{sum(l in REAL for l, kk in got.values() if kk['arm'] == arm)}/"
                                f"{sum(kk['arm'] == arm for _, kk in got.values())}" for arm in ("web", "android", "apple")})
    for l, k in sorted(got.values(), key=lambda x: x[1]["policy"]):
        lb = first.get(k["reused"]) if k["reused"] else lab.get(next(i for i, kk in key.items() if kk is k))
        print(f"  {k['policy']:12s} {l:18s} {k['relation']:30s} {lb.get('reason', '')[:150]}")

print("\n== Misses: confirmed conflicts of the independent reading")
vkey, vlab = json.load(open(f"{D}/verify_key.json")), S.labels("verify_labels")
confirmed = [(i, k) for i, k in sorted(vkey.items()) if i in vlab and vlab[i]["label"] in REAL]
by = collections.defaultdict(list)
for p in pairs:
    by[p["policy"]].append(p)
strict, loose = collections.Counter(), collections.Counter()
for i, k in confirmed:
    pid = k["policy"]
    rows = S.rule_index(pid)
    a, d = S.matches(rows, pid, k["permit"], "ALLOW"), S.matches(rows, pid, k["prohibit"], "DENY")
    hit = [p for p in by[pid] if record(p["allow"]) in a and record(p["deny"]) in d]
    strict[("no rule" if not (a and d) else "contradiction" if any(p["kind"] == "contradiction" for p in hit)
            else ("pair: " + ", ".join(sorted({p["relation"] for p in hit}))) if hit else "rules, no pair")] += 1
    sa, sd = f"{pid}#{k['permit']['located']}", f"{pid}#{k['prohibit']['located']}"
    hit = [p for p in by[pid] if section(p["allow"]) == sa and section(p["deny"]) == sd]
    loose[("contradiction" if any(p["kind"] == "contradiction" for p in hit)
           else ("pair: " + ", ".join(sorted({p["relation"] for p in hit}))) if hit else "no pair between the sections")] += 1
print(f"{len(confirmed)} confirmed conflicts")
print("matched by quoted words:", dict(strict.most_common()))
print("matched by section (upper bound):", dict(loose.most_common()))
