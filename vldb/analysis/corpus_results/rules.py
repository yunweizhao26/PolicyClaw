import collections, statistics

import common as C
from common import SCHEMA

QUALIFIERS = ("conditions", "exceptions", "purpose", "references")
SLOT_FIELDS = ("actor", "recipient", "source")


def operation(vocab, action):
    best = None
    for op in list(SCHEMA.operations) + [SCHEMA.uncovered["label"]]:
        if C.under(vocab, op, action) and (best is None or C.under(vocab, best, op)):
            best = op
    return best


def rule_counts(rows, vocab, ops):
    c = collections.Counter(rules=len(rows), records=len({C.record_id(r["id"]) for r in rows}), units_with_rules=bool(rows))
    for r in rows:
        if "reconcile" in r:
            c[f"reconcile {r['reconcile']['status']}"] += 1
        raw, guard = r["raw"], r["guard"]
        c[f"polarity {r['polarity']}"] += 1
        for k in QUALIFIERS:
            c[f"with {k}"] += bool(raw.get(k))
        c["with conditions or exceptions"] += bool(raw.get("conditions") or raw.get("exceptions"))
        c["with any qualifier"] += any(raw.get(k) for k in QUALIFIERS)
        for t in {x.get("target") or "no target" for x in raw.get("references") or [] if isinstance(x, dict)}:
            c[f"with a reference to {t}"] += 1
        for k in SLOT_FIELDS:
            c[f"with {k}"] += bool(r[k])
        c["guard not true"] += not C.is_true(guard)
        used = C.variables(guard)
        c["guard with a residual"] += "residual" in used
        c["guard translated, no residual"] += bool(used) and "residual" not in used
        c["guard only residuals"] += used == {"residual"}
        for v in used:
            c[f"variable {v}"] += 1
        op = ops.setdefault(r["action"], operation(vocab, r["action"]))
        c[f"operation {op or 'none: the network places the verb under no operation'}"] += 1
        c[f"extractor operation {raw.get('operation')}"] += 1
        c["disclosure without recipient"] += C.under(vocab, "disclosure", r["action"]) and not r["recipient"]
        c["disclosure"] += C.under(vocab, "disclosure", r["action"])
    return c


def report_counts(rep):
    c, x = collections.Counter(), rep["report"]
    for k in ("quotes", "residual_quotes", "unsatisfiable_guards", "qualifiers_without_effect", "raw_rules",
              "compile_failures", "fixed_structurally", "fixed_by_call", "sections"):
        c[f"report {k}"] += x.get(k, 0)
    c["report rejected"] += len(x["rejected"])
    for rj in x["rejected"]:
        c[f"report rejected: {rj.get('reason')}"] += 1
    for k, v in rep["usage"].items():
        c[f"usage {k}"] += v
    for u in rep.get("previous_usage", []):
        for k, v in u.items():
            c[f"usage of earlier attempts {k}"] += v
    return c


def shares(c):
    n, q = c["rules"], c["report quotes"]
    out = {k: C.pct(c[k], n) for k in ("polarity ALLOW", "polarity DENY", "with conditions", "with exceptions",
                                        "with conditions or exceptions", "with purpose", "with references", "with recipient",
                                        "with source", "with actor", "guard not true", "guard with a residual",
                                        "guard translated, no residual", "guard only residuals")}
    out["qualifier quotes translated"] = C.pct(q - c["report residual_quotes"], q)
    out["qualifier quotes residual"] = C.pct(c["report residual_quotes"], q)
    out["rejected of extracted records"] = C.pct(c["report rejected"], c["report rejected"] + c["report raw_rules"])
    out["disclosure without recipient, of disclosures"] = C.pct(c["disclosure without recipient"], c["disclosure"])
    out["disclosure without recipient, of rules"] = C.pct(c["disclosure without recipient"], n)
    return out


def main_testset():
    vs = C.versions()
    rows = {v["site_id"]: C.rule_rows(v["site_id"]) for v in vs}
    vocab = C.vocabulary(r["action"] for rs in rows.values() for r in rs)
    ops = {}
    by_policy = {u: rule_counts(rs, vocab, ops) + report_counts(C.report(u)) for u, rs in rows.items()}
    res = {"policies": {}}
    for name, scope in C.scopes(vs):
        c = sum((by_policy[v["site_id"]] for v in scope), collections.Counter(policies=len(scope)))
        n = [by_policy[v["site_id"]]["rules"] for v in scope]
        res["policies"][name] = {
            "counts": dict(sorted(c.items())), "shares_pct": shares(c),
            "rules_per_policy": {"policies": len(n), "policies_with_rules": sum(x > 0 for x in n), "min": min(n),
                                 "q1": C.quantile(n, 0.25), "median": statistics.median(n), "q3": C.quantile(n, 0.75),
                                 "max": max(n), "mean": round(statistics.mean(n), 1)}}
    res["per_policy"] = {u: {"arm": v["arm"], "rules": c["rules"], "guard with a residual": c["guard with a residual"],
                             "guard only residuals": c["guard only residuals"], "with references": c["with references"],
                             "disclosure": c["disclosure"], "disclosure without recipient": c["disclosure without recipient"]}
                         for v in vs for u, c in [(v["site_id"], by_policy[v["site_id"]])]}
    actions = {r["action"] for rs in rows.values() for r in rs}
    net = C.ActionNetwork()
    res["action_nodes"] = {"distinct": len(actions), "placed_by_network": len(actions & net.placed),
                           "verbs": len({a.split("@")[0] for a in actions if "@" in a})}
    tot = res["policies"]["all"]["counts"]
    res["checks"] = {"extraction_records_equal_report_raw_rules": tot["records"] == tot["report raw_rules"],
                     "failed_model_calls_in_reports": tot.get("usage failures", 0)}
    C.write("rules.json", res)


def main():
    if C.options().set == "testset":
        return main_testset()
    vs = C.versions()
    shas = sorted({v["cleaned_sha256"] for v in vs})
    vocab = C.vocabulary(r["action"] for s in shas for r in C.rule_rows(s))
    ops, by_text = {}, {}
    for s in shas:
        by_text[s] = rule_counts(C.rule_rows(s), vocab, ops) + report_counts(C.report(s))
    texts = sum(by_text.values(), collections.Counter())
    superseded = collections.Counter()
    for p in sorted((C.CORPUS / "rules/.superseded").glob("*.report.json")):
        superseded.update(report_counts(C.json.load(open(p))))
    res = {"distinct_texts": {"texts": len(shas), "counts": dict(sorted(texts.items())), "shares_pct": shares(texts),
                              "superseded_reports": {k: v for k, v in sorted(superseded.items()) if k.startswith("usage")}}}
    for rules in ("reconciled", "extracted"):
        res[f"versions_{rules}"] = {}
        for name, scope in C.scopes(vs):
            c = collections.Counter(versions=len(scope))
            for v in scope:
                c.update(by_text[v["cleaned_sha256"]] if rules == "extracted"
                         else rule_counts(C.unit_rows(C.unit(v, rules)), vocab, ops))
            res[f"versions_{rules}"][name] = {"counts": dict(sorted(c.items())), "shares_pct": shares(c)}
    actions = {r["action"] for s in shas for r in C.rule_rows(s)}
    net = C.ActionNetwork()
    res["action_nodes"] = {"distinct": len(actions), "placed_by_network": len(actions & net.placed),
                           "verbs": len({a.split("@")[0] for a in actions if "@" in a})}
    res["checks"] = {"extraction_records_equal_report_raw_rules": texts["records"] == texts["report raw_rules"],
                     "failed_model_calls_in_final_reports": texts["usage failures"]}
    C.write("rules.json", res)


if __name__ == "__main__":
    main()
