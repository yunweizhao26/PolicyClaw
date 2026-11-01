import collections, json, multiprocessing as mp, statistics, time

import common as C
from common import SCHEMA, TRUE
from policyclaw.guards import atoms, residuals
from policyclaw.merge import _same_practice
from policyclaw.queries import _more_specific, _same_scope, _Solver, pair_outcome

OUTCOMES = ("mutually_exclusive", "overlap_candidate", "unresolved")


def relation(vocab, a, d):
    sv = _Solver([a.guard, d.guard])
    if _same_scope(sv, vocab, a, d):
        return "same scope"
    if _more_specific(sv, vocab, a, d):
        return "allow more specific"
    if _more_specific(sv, vocab, d, a):
        return "deny more specific"
    return "incomparable"


def unit_pairs(u):
    all_rows = C.unit_rows(u)
    rows = C.one_per_record(all_rows)
    vocab = C.vocabulary(r["action"] for r in rows)
    allow = [r for r in rows if r["polarity"] == "ALLOW"]
    deny = [r for r in rows if r["polarity"] == "DENY"]
    out = []
    for a in allow:
        for d in deny:
            if not _same_practice(a["raw"], d["raw"], True):
                continue
            t0 = time.perf_counter()
            po = pair_outcome(a["guard"], d["guard"])
            rec = {"unit": u, "allow": a["id"], "deny": d["id"], "outcome": po["outcome"],
                   "z3_ms": round(1000 * (time.perf_counter() - t0), 3),
                   "true_guards": C.is_true(a["guard"]) + C.is_true(d["guard"]),
                   "same_section": C.section_id(a["id"]) == C.section_id(d["id"]), "operation": a["raw"].get("operation"), "action": a["action"]}
            A, D = C.rule(a), C.rule(d)
            if po["outcome"] == "mutually_exclusive":
                derived = any(x.get("var") in SCHEMA.derived_variables() for x in atoms(d["guard"]))
                rec["relation"] = "policy exception" if derived else "exclusive guards"
            else:
                t0 = time.perf_counter()
                rec["relation"] = relation(vocab, A, D)
                rec["relation_ms"] = round(1000 * (time.perf_counter() - t0), 3)
            if po["outcome"] == "unresolved":
                ids = {x["id"] for x in po["blocking"]}
                rec["blocking"] = len(ids)
                rec["blocking_in"] = "+".join(s for s, g in (("allow", a["guard"]), ("deny", d["guard"]))
                                              if ids & {x["id"] for x in residuals(g)})
                rec["untranslated_guard"] = any(C.variables(g) == {"residual"} for g in (a["guard"], d["guard"]))
            A.guard, D.guard = TRUE, TRUE
            rec["ablation_outcome"] = pair_outcome(TRUE, TRUE)["outcome"]
            rec["ablation_relation"] = relation(vocab, A, D)
            out.append(rec)
    return u, len(all_rows), out


def summarize(recs):
    c = collections.Counter(r["outcome"] for r in recs)
    n = len(recs)
    return {"pairs": n, "outcomes": {o: c[o] for o in OUTCOMES}, "outcome_shares_pct": {o: C.pct(c[o], n) for o in OUTCOMES},
            "decided_share_pct": C.pct(c["mutually_exclusive"] + c["overlap_candidate"], n),
            "relation_by_outcome": {o: dict(collections.Counter(r["relation"] for r in recs if r["outcome"] == o).most_common())
                                    for o in OUTCOMES},
            "overlap_guard_placement": {k: sum(r["true_guards"] == t for r in recs if r["outcome"] == "overlap_candidate")
                                        for k, t in (("both true", 2), ("one true", 1), ("neither true", 0))},
            "mutually_exclusive_guard_placement": {k: sum(r["true_guards"] == t for r in recs if r["outcome"] == "mutually_exclusive")
                                                   for k, t in (("both true", 2), ("one true", 1), ("neither true", 0))},
            "overlap_same_section": sum(r["same_section"] for r in recs if r["outcome"] == "overlap_candidate"),
            "unresolved_blocking": {"pairs_with_blocking_residuals": sum(r.get("blocking", 0) > 0 for r in recs if r["outcome"] == "unresolved"),
                                    "blocking_in": dict(collections.Counter(r["blocking_in"] for r in recs if r["outcome"] == "unresolved")),
                                    "a_guard_entirely_untranslated": sum(r.get("untranslated_guard", False) for r in recs),
                                    "blocking_residuals_per_pair_median": statistics.median(
                                        [r["blocking"] for r in recs if r["outcome"] == "unresolved"] or [0])},
            "ablation_all_guards_true": {"outcomes": dict(collections.Counter(r["ablation_outcome"] for r in recs)),
                                         "pairs_whose_outcome_changes": sum(r["ablation_outcome"] != r["outcome"] for r in recs),
                                         "relations": dict(collections.Counter(r["ablation_relation"] for r in recs).most_common())}}


def deciles(per):
    ordered, out = sorted([p for p in per if p["rules"]], key=lambda p: (p["rules"], p["key"])), []
    for i in range(10):
        g = ordered[i * len(ordered) // 10:(i + 1) * len(ordered) // 10]
        out.append({"decile": i + 1, "versions": len(g), "rules_min": g[0]["rules"], "rules_median": statistics.median(p["rules"] for p in g),
                    "rules_max": g[-1]["rules"], "pairs": sum(p["pairs"] for p in g),
                    "pairs_per_version": round(sum(p["pairs"] for p in g) / len(g), 4),
                    "versions_with_pair_pct": C.pct(sum(p["pairs"] > 0 for p in g), len(g)),
                    "overlap_candidates": sum(p.get("overlap_candidate", 0) for p in g)})
    return out


def version_stats(vs, rules, results):
    per, recs = [], []
    for v in vs:
        n, rs = results[C.unit(v, rules)]
        recs += rs
        c = collections.Counter(r["outcome"] for r in rs)
        per.append({"rules": n, "pairs": len(rs), "key": (v["site_id"], v["version_index"]),
                    "conflicts": sum(r["relation"] == "same scope" for r in rs if r["outcome"] == "overlap_candidate"), **c})
    return {"versions": len(vs), "versions_with_rules": sum(p["rules"] > 0 for p in per), **summarize(recs),
            "versions_with": {k: sum(p.get(k, 0) > 0 for p in per) for k in OUTCOMES},
            "versions_with_a_pair": sum(p["pairs"] > 0 for p in per),
            "versions_with_a_same_scope_conflict": sum(p["conflicts"] > 0 for p in per),
            "pages_with_a_same_scope_conflict": len({p["key"][0] for p in per if p["conflicts"]}),
            "overlap_candidates_by_extractor_operation": dict(collections.Counter(
                r["operation"] for r in recs if r["outcome"] == "overlap_candidate").most_common()),
            "overlap_candidates_by_allow_action_top10": dict(collections.Counter(
                r["action"] for r in recs if r["outcome"] == "overlap_candidate").most_common(10)),
            "size_deciles": deciles(per)}


def main():
    args = C.options(workers=True)
    vs = C.versions()
    units = sorted({C.unit(v, args.rules) for v in vs})
    t0 = time.time()
    with mp.Pool(args.workers) as pool:
        results = {u: (n, recs) for u, n, recs in pool.imap_unordered(unit_pairs, units, chunksize=4)}
    wall = time.time() - t0
    with open(C.OUT / C.out_name("pair_records", args.rules).replace(".json", ".jsonl"), "w") as f:
        for u in units:
            for r in results[u][1]:
                f.write(json.dumps(r) + "\n")
    recs = [r for u in units for r in results[u][1]]
    ms = [r["z3_ms"] for r in recs]
    rel_ms = [r["relation_ms"] for r in recs if "relation_ms" in r]
    res = {"rules": args.rules, "unstable_pages": C.unstable_pages(vs)}
    for name, scope in C.scopes(vs):
        res[name] = version_stats(scope, args.rules, results)
    if args.rules == "extracted":
        res["distinct_texts"] = {"texts": len(units), **summarize(recs)}
    res["solver_time"] = {"rule_sets": len(units), "workers": args.workers, "wall_s": round(wall, 1),
                          "pair_outcome_ms": {"pairs": len(ms), "median": statistics.median(ms), "p95": C.quantile(ms, 0.95),
                                              "max": max(ms), "total_s": round(sum(ms) / 1000, 2)},
                          "relation_ms": {"pairs": len(rel_ms), "median": statistics.median(rel_ms),
                                          "p95": C.quantile(rel_ms, 0.95), "max": max(rel_ms), "total_s": round(sum(rel_ms) / 1000, 2)}}
    res["checks"] = {"every_unresolved_pair_has_a_blocking_residual":
                     all(r.get("blocking", 0) > 0 for r in recs if r["outcome"] == "unresolved"),
                     "ablation_makes_every_pair_an_overlap": all(r["ablation_outcome"] == "overlap_candidate" for r in recs)}
    C.write(C.out_name("pairs", args.rules), res)


if __name__ == "__main__":
    main()
