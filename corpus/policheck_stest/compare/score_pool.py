import collections, glob, json, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REAL, LABELS = ("contradiction", "unresolved"), ("allow", "deny", "no_overlap", "contradiction", "unresolved",
                                                  "different_practice", "misread")


def wilson(k, n, z=1.96):
    if not n:
        return (float("nan"),) * 2
    p, d = k / n, 1 + z * z / n
    c, h = (p + z * z / (2 * n)) / d, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0, c - h), min(1, c + h)


key = json.load(open(HERE / "key.json"))
items, counts = key["items"], key["counts"]
lab = {}
for f in glob.glob(str(HERE / "labels/*.jsonl")):
    for line in open(f):
        if line.strip():
            r = json.loads(line)
            lab[r["item"]] = r
print(f"{len(lab)} of {len(items)} items labeled")
print("system".ljust(32) + "reports labeled " + " ".join(l[:9].rjust(9) for l in LABELS) +
      "   real (95% CI)          false positives   strict   est. real   policies")
for name in sorted(counts):
    its = [i for i, x in items.items() if name in x["systems"] and i in lab]
    c = collections.Counter(lab[i]["label"] for i in its)
    k, n = sum(c[l] for l in REAL), len(its)
    lo, hi = wilson(k, n)
    pols = len({items[i]["policy"] for i in its if lab[i]["label"] in REAL})
    print(name.ljust(32) + f"{counts[name]['reports']:7d} {n:7d} " + " ".join(f"{c[l]:9d}" for l in LABELS) +
          f"   {k:3d}/{n:<3d} {100 * k / n if n else 0:5.1f}% ({100 * lo:4.1f}-{100 * hi:4.1f})" +
          f"   {100 - 100 * k / n if n else 0:6.1f}%   {c['contradiction']:6d}   {k / n * counts[name]['reports'] if n else 0:8.1f}   {pols:6d}")
real = {i for i in lab if lab[i]["label"] in REAL}
by = collections.Counter(tuple(sorted(set(items[i]["systems"]))) for i in real)
print(f"\nreal items in the pool: {len(real)} in {len({items[i]['policy'] for i in real})} policies; found by:")
for systems, n in by.most_common():
    print(f"  {' + '.join(systems)}: {n}")
print("\nreal items:")
for i in sorted(real):
    x = items[i]
    print(f"  {i} {x['policy']} {lab[i]['label']:13s} {'+'.join(sorted(set(x['systems']))):45s} {lab[i]['reason']}")
