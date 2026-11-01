import csv, json, statistics
from pathlib import Path

T = Path("/scratch/yz5944/nlp+privacy/PolicyClaw/corpus/testset")
F03 = "03_qwen_complement_verified_cleaned_pipeline_input.txt"


def cost(u):
    return (u.get("prompt_tokens", 0) * 0.75 + (u.get("completion_tokens", 0) + u.get("thinking_tokens", 0)) * 3.75) / 1e6


rows = []
with open(T / "selection.tsv", newline="", encoding="utf-8") as f:
    for s in csv.DictReader(f, delimiter="\t"):
        i = s["id"]
        prep = json.loads((T / "prepared" / i / "cleanup_audit.json").read_text())["usage"]
        rep = json.loads((T / "rules" / f"{i}.report.json").read_text())
        ext = rep["usage"]
        rows.append({"id": i, "arm": s["arm"], "cleaned_chars": len((T / "prepared" / i / F03).read_text(encoding="utf-8")),
                     "sections": rep["sections"], "rules": rep["rules"] if isinstance(rep["rules"], int) else len(rep["rules"]),
                     "failed_calls": ext.get("failures", 0),
                     "prep_usd": round(cost(prep), 5), "extract_usd": round(cost(ext), 5),
                     "prep_model_s": round(prep.get("seconds", 0), 1), "extract_model_s": round(ext.get("seconds", 0), 1)})
with open(T / "eval" / "system_stats.tsv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
    w.writeheader()
    w.writerows(rows)
cols = ("cleaned_chars", "sections", "rules", "prep_usd", "extract_usd", "extract_model_s")
print("arm\tpolicies\t" + "\t".join(f"median_{c}" for c in cols) + "\ttotal_rules\ttotal_prep_usd\ttotal_extract_usd\tfailed_calls")
for arm in ("web", "android", "apple", None):
    xs = [r for r in rows if arm is None or r["arm"] == arm]
    print(f"{arm or 'all'}\t{len(xs)}\t" + "\t".join(f"{statistics.median(r[c] for r in xs):.4g}" for c in cols) +
          f"\t{sum(r['rules'] for r in xs)}\t{sum(r['prep_usd'] for r in xs):.2f}\t{sum(r['extract_usd'] for r in xs):.2f}"
          f"\t{sum(r['failed_calls'] for r in xs)}")
top = sorted(rows, key=lambda r: -r["extract_usd"])[:5]
print("most expensive extractions:", [(r["id"], r["rules"], round(r["extract_usd"], 2)) for r in top])
