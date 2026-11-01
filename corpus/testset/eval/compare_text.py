import csv, re, statistics
from pathlib import Path

T = Path("/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset")
F01, F03 = "01_frozen_plaintext_pipeline_input.txt", "03_qwen_complement_verified_cleaned_pipeline_input.txt"
WORD = re.compile(r"\w+")


def shingles(text):
    w = WORD.findall(text.lower())
    return {tuple(w[i:i + 5]) for i in range(len(w) - 4)}


rows = []
with open(T / "selection.tsv", newline="", encoding="utf-8") as f:
    for s in csv.DictReader(f, delimiter="\t"):
        d = T / "prepared" / s["id"]
        if not (d / F03).exists():
            continue
        src, clean = (d / F01).read_text(encoding="utf-8"), (d / F03).read_text(encoding="utf-8")
        traf = (T / "texts" / f"{s['id']}.trafilatura.txt").read_text(encoding="utf-8")
        c, t = shingles(clean), shingles(traf)
        rows.append({"id": s["id"], "arm": s["arm"], "visible_chars": len(src), "cleaned_chars": len(clean),
                     "trafilatura_chars": len(traf), "kept_share": round(len(clean) / max(1, len(src)), 4),
                     "trafilatura_recall": round(len(c & t) / len(c), 4) if c else "",
                     "trafilatura_precision": round(len(c & t) / len(t), 4) if t else ""})
with open(T / "eval" / "compare_text.tsv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
    w.writeheader()
    w.writerows(rows)
for arm in ("web", "android", "apple", None):
    xs = [r for r in rows if arm is None or r["arm"] == arm]
    print(f"\n== {arm or 'all arms'}: {len(xs)} policies")
    for k in ("kept_share", "trafilatura_recall", "trafilatura_precision"):
        v = sorted(r[k] for r in xs if r[k] != "")
        if v:
            print(f"   {k}: median {statistics.median(v):.3f}, 10th percentile {v[len(v) // 10]:.3f}, "
                  f"below 0.95: {sum(x < 0.95 for x in v)} of {len(v)}")
