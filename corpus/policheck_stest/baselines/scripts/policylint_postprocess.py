#!/usr/bin/env python3
import collections, csv, importlib.util, json, sqlite3
from pathlib import Path

BL = Path(__file__).resolve().parents[1]
EXT = BL / "work/policylint/ext"
CHECK = BL / "work/policylint/ext_utf8check"
OUT = BL / "policylint"
E3 = Path("/scratch/yz5944/nlp+privacy/PolicyClaw/experiments/frozen_e0/e3_shared_input/hpc/e3_hpc.py")

spec = importlib.util.spec_from_file_location("e3_hpc", E3)
e3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e3)

db_path = EXT / "output/db/consistency_results_1.db"
with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as db:
    rows = e3.policylint_rows(db)
    raw_contradictions = db.execute("SELECT COUNT(*) FROM Contradiction").fetchone()[0]
    apps_with_statements = sorted(r[0] for r in db.execute("SELECT DISTINCT appId FROM AppPolicySentences"))
    statements = db.execute("SELECT COUNT(*) FROM AppPolicySentences").fetchone()[0]
rows = [{k: "" if v is None else str(v) for k, v in r.items()} for r in rows]
OUT.mkdir(parents=True, exist_ok=True)
with open(OUT / "policylint_results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=e3.POLICYLINT_FIELDS)
    w.writeheader()
    w.writerows(rows)


def keyed(rs):
    return collections.Counter(
        tuple(frozenset(r[k].split("||")) if k in ("policySentences", "contradictionSentences") else r[k]
              for k in e3.POLICYLINT_FIELDS) for r in rs)


checks = {}
for name, path in (("official_unchanged", EXT / "policylint_results.csv"),
                   ("official_utf8_default_encoding", CHECK / "policylint_results.csv")):
    if path.is_file():
        official = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
        checks[name] = {"rows": len(official), "equal_to_port": keyed(official) == keyed(rows)}
    else:
        checks[name] = "no output (the official script did not finish)"

merged = {}
for n, r in enumerate(rows, 1):
    pol = (r["policyEntity"], r["policyAction"], r["policyData"], r["policySentences"])
    con = (r["contradictoryEntity"], r["contradictoryAction"], r["contradictoryData"], r["contradictionSentences"])
    assert {pol[1], con[1]} == {"collect", "not_collect"}, r
    pos, neg = (pol, con) if pol[1] == "collect" else (con, pol)
    key = (r["packageName"], r["contradictionNum"], pos, neg)
    if key in merged:
        merged[key]["results_rows"].append(n)
        continue
    merged[key] = {"policy_id": r["packageName"], "type": r["contradictionNum"],
                   "positive_sentence": "\n".join(pos[3].split("||")), "negative_sentence": "\n".join(neg[3].split("||")),
                   "n_positive_sentences": len(pos[3].split("||")), "n_negative_sentences": len(neg[3].split("||")),
                   "positive_entity": pos[0], "positive_action": pos[1], "positive_data": pos[2],
                   "negative_entity": neg[0], "negative_action": neg[1], "negative_data": neg[2],
                   "results_rows": [n]}
norm = sorted(merged.values(), key=lambda x: (x["policy_id"], x["results_rows"][0]))
for x in norm:
    x["results_rows"] = ";".join(map(str, x["results_rows"]))
with open(OUT / "contradictions.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(norm[0]) if norm else ["policy_id", "type", "positive_sentence", "negative_sentence"])
    w.writeheader()
    w.writerows(norm)

summary = {
    "result_db_contradiction_rows": raw_contradictions,
    "policylint_results_rows": len(rows),
    "policylint_results_by_type": dict(sorted(collections.Counter(r["contradictionNum"] for r in rows).items())),
    "contradictions": len(norm),
    "contradictions_by_type": dict(sorted(collections.Counter(x["type"] for x in norm).items())),
    "policies_with_contradictions": len({x["policy_id"] for x in norm}),
    "contradictions_with_several_sentences_on_a_side": sum(x["n_positive_sentences"] > 1 or x["n_negative_sentences"] > 1 for x in norm),
    "policies_with_policy_statements": len(apps_with_statements),
    "policy_statement_sentence_rows": statements,
    "checks": checks,
}
json.dump(summary, open(OUT / "summary.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
