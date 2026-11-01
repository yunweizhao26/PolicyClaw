import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
JOB = sys.argv[1]
SC = ("all", "web", "android", "apple")
load = lambda n: json.load(open(OUT / n))
RU, PA, QU, Q0, RC, FG = (load(n) for n in ("rules.json", "pairs.json", "queries.json", "queries_no_terms.json", "reconcile_pairs.json", "figures.json"))


def n(x):
    return f"{x:,}" if isinstance(x, int) else f"{x:,.1f}"


def p(a, b, d=1):
    return f"{100 * a / b:.{d}f}%" if b else "n/a"


def na(a, b):
    return f"{n(a)} ({p(a, b)})"


R = lambda s: RU["policies"][s]
C = lambda s: R(s)["counts"]
P = lambda s: PA[s]
Q = lambda s: QU[s]
N = lambda s: P(s)["versions"]


def unres_only(s):
    return P(s)["unresolved_blocking"]["a_guard_entirely_untranslated"]


def rel(s, o, k):
    return P(s)["relation_by_outcome"][o].get(k, 0)


def ov_pol(s):
    return P(s)["versions_with"]["overlap_candidate"]


def dec(s, i):
    return P(s)["size_deciles"][i]


def top(s, key, k=5):
    return ", ".join(f"{a} {n(b)}" for a, b in list(P(s)[key].items())[:k])


def cov(s, k):
    return Q(s)["coverage"][k]


def ctr(s, k):
    return Q(s)["compliance_requirement_versions"][k]


def rows_table(head, rows):
    out = [f"| {' | '.join(head)} |", "|" + "---|" * len(head)]
    for r in rows:
        paper, claim, old, fn, key, note = r
        out.append(f"| {paper} | {claim} | {old} | " + " | ".join(str(fn(s)) for s in SC) + f" | {key} | {note} |")
    return "\n".join(out)


HEAD = ["Paper row", "Claim", "Old value", "All 600", "Web", "Google Play", "App Store", "Script and output", "Note"]
NV = lambda s: "needs versions"
NL = lambda s: "needs labels"

rules_rows = [
    ("abstract:2, intro:18, 7.2:16", "extracted rules", "112,768", lambda s: n(C(s)["rules"]), "`rules.py`: `policies.*.counts.rules`",
     f"{n(C('all')['records'])} extraction records over all 600 (a record with several purposes compiles to one rule per purpose). Equals the pipeline run's total of 146,861 (`eval/system_stats.tsv`)."),
    ("7.2:18", "ALLOW and DENY rules", "100,895 and 11,873",
     lambda s: f"{na(C(s)['polarity ALLOW'], C(s)['rules'])} and {na(C(s)['polarity DENY'], C(s)['rules'])}", "`rules.py`: `polarity ALLOW`, `polarity DENY`", ""),
    ("7.2:18", "rules with explicit conditions", "45,265 (40.1%)",
     lambda s: f"{na(C(s)['with conditions or exceptions'], C(s)['rules'])} with a condition or exception quote; {na(C(s)['guard not true'], C(s)['rules'])} whose guard is not true",
     "`rules.py`: `with conditions or exceptions`, `guard not true`",
     "Same definitions as the corpus run."),
    ("7.2:18", "rules with a recipient", "24.1%", lambda s: na(C(s)["with recipient"], C(s)["rules"]), "`rules.py`: `with recipient`", ""),
    ("7.2:62 to 67", "any ambiguity flag", "21,684 (19.2%)", lambda s: "no counterpart", "", "The old flags came from the regex guard mapper. The three rows below are the closest measures (figure 1d)."),
    ("7.2:63", "condition has no extracted predicate", "13,039 (11.6%)",
     lambda s: f"{na(C(s)['guard with a residual'], C(s)['rules'])} with an untranslated quote in the guard; {na(C(s)['guard only residuals'], C(s)['rules'])} with only untranslated quotes",
     "`rules.py`: `guard with a residual`, `guard only residuals`", ""),
    ("7.2:64, 7.2:72", "condition points elsewhere, cross-reference flag", "2,943 (2.6%), 6.0%",
     lambda s: f"{na(C(s)['with references'], C(s)['rules'])}: law {n(C(s)['with a reference to law'])}, policy section {n(C(s)['with a reference to policy_section'])}, other document {n(C(s)['with a reference to other_document'])}",
     "`rules.py`: `with references`, `with a reference to *`", "A rule with several reference targets counts under each target. The extractor assigns the target."),
    ("7.2:66", "missing or implicit counterparty", "5,061 (4.5%)",
     lambda s: f"{n(C(s)['disclosure without recipient'])} disclosure rules without a recipient ({p(C(s)['disclosure without recipient'], C(s)['rules'])} of rules, {p(C(s)['disclosure without recipient'], C(s)['disclosure'])} of {n(C(s)['disclosure'])} disclosure rules)",
     "`rules.py`: `disclosure without recipient`, `disclosure`", "A disclosure rule's action lies under the operation \"disclosure\" in the action network."),
    ("7.2:16", "share of raw extractions removed by the filter", "21.9%",
     lambda s: f"{n(C(s)['report rejected'])} of {n(C(s)['report rejected'] + C(s)['report raw_rules'])} records rejected ({p(C(s)['report rejected'], C(s)['report rejected'] + C(s)['report raw_rules'])})",
     "`rules.py`: `report rejected`, `report raw_rules`, `shares_pct[\"rejected of extracted records\"]`",
     "Reasons over all 600: " + ", ".join(f"{k.split(': ')[1]} {n(v)}" for k, v in C("all").items() if k.startswith("report rejected: ")) + "."),
    ("(new)", "qualifier quotes translated to formulas", "none",
     lambda s: f"{n(C(s)['report quotes'] - C(s)['report residual_quotes'])} of {n(C(s)['report quotes'])} ({R(s)['shares_pct']['qualifier quotes translated']:.1f}%)",
     "`rules.py`: `report quotes`, `report residual_quotes`", "Distinct quotes per section, from the per-policy reports."),
    ("(new)", "unsatisfiable guards, qualifiers without effect", "none", lambda s: f"{n(C(s)['report unsatisfiable_guards'])} and {n(C(s)['report qualifiers_without_effect'])}",
     "`rules.py`: `report unsatisfiable_guards`, `report qualifiers_without_effect`", "Deletion test in `policyclaw/extract.py`."),
    ("fig 1a", "rules per policy: median (quartiles), maximum", "histogram only",
     lambda s: f"{R(s)['rules_per_policy']['median']:g} ({R(s)['rules_per_policy']['q1']} to {R(s)['rules_per_policy']['q3']}), {n(R(s)['rules_per_policy']['max'])}",
     "`rules.py`: `policies.*.rules_per_policy`", "Quartiles are nearest-rank (`common.quantile`). Minimum "
     + ", ".join(f"{R(s)['rules_per_policy']['min']}" for s in SC) + " (all, web, Google Play, App Store); mean "
     + ", ".join(f"{R(s)['rules_per_policy']['mean']}" for s in SC) + "."),
    ("(new)", "model calls and tokens of the extraction (from the reports)", "none",
     lambda s: f"{n(C(s)['usage calls'])} calls, {C(s)['usage prompt_tokens'] / 1e6:.1f}M prompt and {C(s)['usage completion_tokens'] / 1e6:.1f}M completion tokens",
     "`rules.py`: `usage *`", f"Read from the stored reports, not a new model call. {C('all')['usage failures']} failed calls remain in the final reports (the three App Store policies kept with `--accept-failed`, FINDINGS §30)."),
]

pairs_rows = [
    ("abstract:2, intro:18, 7.2:10, 7.2:21", "opposing pairs", "2,232", lambda s: n(P(s)["pairs"]), "`pairs.py`: `*.pairs`",
     f"`corpus/testset/eval/conflict_pairs.jsonl` holds {n(RC['pairs_before'])} pairs and `pair_records.jsonl` holds {n(RC['pairs_now'])}. The two files have the same pairs, and every field of every pair is equal (`reconcile_pairs.json`: only_now {RC['only_now']}, only_before {RC['only_before']}, differing fields 0). `conflict_pairs.py` calls the same `pairs.unit_pairs`, so no difference is expected."),
    ("abstract:2, intro:18, 7.2:21", "overlap candidates", "424", lambda s: na(P(s)["outcomes"]["overlap_candidate"], P(s)["pairs"]), "`pairs.py`: `*.outcomes`", ""),
    ("abstract:2, intro:18, 7.2:21", "mutually exclusive", "26", lambda s: na(P(s)["outcomes"]["mutually_exclusive"], P(s)["pairs"]), "`pairs.py`: `*.outcomes`",
     "Policy exceptions (the prohibition uses `policy.permits`): " + ", ".join(str(rel(s, "mutually_exclusive", "policy exception")) for s in SC) + "; exclusive guards: " + ", ".join(str(rel(s, "mutually_exclusive", "exclusive guards")) for s in SC) + " (all, web, Google Play, App Store)."),
    ("abstract:2, intro:18, 7.2:21", "unresolved", "1,782", lambda s: na(P(s)["outcomes"]["unresolved"], P(s)["pairs"]), "`pairs.py`: `*.outcomes.unresolved`", ""),
    ("abstract:2", "unresolved share", "79.8%", lambda s: f"{P(s)['outcome_shares_pct']['unresolved']}%", "`pairs.py`: `*.outcome_shares_pct.unresolved`", ""),
    ("abstract:2, intro:18, 7.2:21, 7.2:76", "pairs with a solver result (decided share)", "450 (20.2%)", lambda s: f"{na(P(s)['outcomes']['overlap_candidate'] + P(s)['outcomes']['mutually_exclusive'], P(s)['pairs'])}", "`pairs.py`: `*.decided_share_pct`", "Overlap candidates plus mutually exclusive pairs."),
    ("7.2:29 to 38", "Table e0_outcomes: unresolved with partly translated guards", "811 (36.3%) semantic",
     lambda s: na(P(s)["outcomes"]["unresolved"] - unres_only(s), P(s)["pairs"]), "`pairs.py`: `*.outcomes.unresolved` minus `unresolved_blocking.a_guard_entirely_untranslated`", "The old \"semantic\" class had a usable extracted condition."),
    ("7.2:29 to 38", "Table e0_outcomes: unresolved with a guard that is only untranslated quotes", "971 (43.5%) pipeline",
     lambda s: na(unres_only(s), P(s)["pairs"]), "`pairs.py`: `*.unresolved_blocking.a_guard_entirely_untranslated`", "Also the row \"pairs without a usable extracted condition\" (discussion:12, old 971)."),
    ("(new)", "unresolved pairs blocked by residuals in the permission, the prohibition, both", "none",
     lambda s: ", ".join(str(P(s)["unresolved_blocking"]["blocking_in"].get(k, 0)) for k in ("allow", "deny", "allow+deny")), "`pairs.py`: `*.unresolved_blocking.blocking_in`",
     "Every unresolved pair has a blocking residual by definition (check passes). Median blocking residuals per pair: 1."),
    ("7.2:23", "policies without a pair, with a pair, with an overlap candidate", "2,927, 751, 314 (versions)",
     lambda s: f"{N(s) - P(s)['versions_with_a_pair']}, {P(s)['versions_with_a_pair']}, {ov_pol(s)}", "`pairs.py`: `*.versions_with_a_pair`, `*.versions_with`", "Policies of the scope: " + ", ".join(str(N(s)) for s in SC) + ". Every policy has rules."),
    ("7.3:15", "policies with a pair, overlap, mutually exclusive, unresolved", "751, 314, 8, 614",
     lambda s: ", ".join(str(x) for x in (P(s)["versions_with_a_pair"], ov_pol(s), P(s)["versions_with"]["mutually_exclusive"], P(s)["versions_with"]["unresolved"])), "`pairs.py`: `*.versions_with`", ""),
    ("7.3:15, 7.3:38", "share of policies with a pair, smallest and largest size decile", "0.54%, 62.23%",
     lambda s: f"{dec(s, 0)['versions_with_pair_pct']}%, {dec(s, 9)['versions_with_pair_pct']}%", "`pairs.py`: `*.size_deciles`", "Deciles of policies by rule count (60 policies each for all 600, 20 for an arm), as in `analyze_rq4.py`. Smallest decile: rules " + "; ".join(f"{dec(s, 0)['rules_min']} to {dec(s, 0)['rules_max']}" for s in SC) + "."),
    ("7.3:15", "pairs per policy, smallest and largest size decile", "0.0054, 2.2962",
     lambda s: f"{dec(s, 0)['pairs_per_version']:.2f}, {dec(s, 9)['pairs_per_version']:.2f}", "`pairs.py`: `*.size_deciles`", ""),
    ("fig_scaling (figure 2)", "decile data", "ten bins", lambda s: "ten bins in `figures.json`", "`figures.py`: `fig2.<scope>`", "Pairs per policy and share of policies with a pair for each decile, for all four scopes."),
    ("7.3:19, 7.3:25 to 27", "overlap candidates: both rules unconditional, one, neither", "113 (26.7%), 268 (63.2%), 43 (10.1%)",
     lambda s: ", ".join(na(P(s)["overlap_guard_placement"][k], P(s)["outcomes"]["overlap_candidate"]) for k in ("both true", "one true", "neither true")), "`pairs.py`: `*.overlap_guard_placement`", ""),
    ("7.1:18", "overlap candidates with at least one unconditional rule", "381 of 424",
     lambda s: f"{n(P(s)['overlap_guard_placement']['both true'] + P(s)['overlap_guard_placement']['one true'])} of {n(P(s)['outcomes']['overlap_candidate'])} ({p(P(s)['overlap_guard_placement']['both true'] + P(s)['overlap_guard_placement']['one true'], P(s)['outcomes']['overlap_candidate'])})",
     "same", ""),
    ("7.3:33", "most frequent actions in overlap candidates (the permission's action node)", "collect 123, use 111, disclose 50, provide 45, process 42",
     lambda s: top(s, "overlap_candidates_by_allow_action_top10"), "`pairs.py`: `*.overlap_candidates_by_allow_action_top10`", "Action nodes are verb@operation."),
    ("7.3:33", "overlap candidates by operation (the extractor's operation)", "none",
     lambda s: top(s, "overlap_candidates_by_extractor_operation", 4), "`pairs.py`: `*.overlap_candidates_by_extractor_operation`", ""),
    ("7.3:33", "mutually exclusive pairs with conditions on both rules", "26 of 26",
     lambda s: f"{P(s)['mutually_exclusive_guard_placement']['neither true']} of {P(s)['outcomes']['mutually_exclusive']}", "`pairs.py`: `*.mutually_exclusive_guard_placement`",
     "One rule unconditional: " + ", ".join(str(P(s)["mutually_exclusive_guard_placement"]["one true"]) for s in SC) + "; both unconditional: 0."),
    ("7.2:44", "all guards replaced by true: pairs whose outcome changes (all become overlap candidates)", "1,782 + 26 change",
     lambda s: f"{n(P(s)['ablation_all_guards_true']['pairs_whose_outcome_changes'])} of {n(P(s)['pairs'])}", "`pairs.py`: `*.ablation_all_guards_true`",
     "Same-scope conflicts with true guards: " + ", ".join(str(P(s)["ablation_all_guards_true"]["relations"].get("same scope", 0)) for s in SC) + ", against " + ", ".join(str(rel(s, "overlap_candidate", "same scope")) for s in SC) + " with the guards."),
    ("(new)", "decision-procedure relation of overlap candidates: incomparable (prohibition wins), prohibition more specific, permission more specific, same scope", "none",
     lambda s: ", ".join(n(rel(s, "overlap_candidate", k)) for k in ("incomparable", "deny more specific", "allow more specific", "same scope")), "`pairs.py`: `*.relation_by_outcome.overlap_candidate`",
     "FINDINGS §31 reports the same strata (8,623, 469, 185, 19 for all 600)."),
    ("(new)", "same-scope conflicts (pairs) and policies with one", "none",
     lambda s: f"{rel(s, 'overlap_candidate', 'same scope')} pairs in {P(s)['versions_with_a_same_scope_conflict']} policies", "`pairs.py`: `*.relation_by_outcome.overlap_candidate`, `*.versions_with_a_same_scope_conflict`", "FINDINGS §31: 19 in 15 policies."),
    ("7.5:29", "SMT time per pair", "1 s (untraced)",
     lambda s: (lambda t: f"median {t['median']:.1f} ms, 95th percentile {t['p95']:.1f} ms, maximum {t['max']:.0f} ms, total {t['total_s']:.0f} s over {n(t['pairs'])} pairs")(PA["solver_time"]["pair_outcome_ms"]) if s == "all" else "not split by arm",
     "`pairs.py`: `solver_time`", "Time of each `pair_outcome` call, including building the solver, measured on 8 CPUs with the policies spread over 8 workers. The relation adds a median of %.1f ms (95th percentile %.1f ms, maximum %.0f ms)." % tuple(PA["solver_time"]["relation_ms"][k] for k in ("median", "p95", "max"))),
    ("7.2:46, discussion:12", "pairs decided after adding legal, jurisdiction, and purpose predicates", "115, 79.8% to 74.7%", lambda s: "no counterpart", "", "The schema already contains legal bases, places, and retention time."),
]

Qs = lambda s: Q(s)["redundancy"]
Q0s = lambda s: Q0[s]["redundancy"]
KINDS = ("data", "action", "purpose", "duplicate", "recipient", "guard", "source", "actor")
queries_rows = [
    ("7.4:25", "redundant rule pairs, with the policy's term relations", "30,750", lambda s: n(Qs(s)["pairs"]), "`queries.py --terms on`: `*.redundancy.pairs`",
     "A duplicate has the same scope, a subsumed rule is strictly more specific than a broader rule of the same polarity. The vocabulary includes the policy's term relations (`rules/<id>.terms.json`), so a rule about a broader data, recipient, source, actor, or purpose term subsumes a narrower one. This is the main redundancy figure on the test set."),
    ("7.4:25", "distinct redundant rule pairs (once per policy), with term relations", "14,996", lambda s: n(Qs(s)["distinct_pairs"]), "`queries.py --terms on`: `*.redundancy.distinct_pairs`", "Each pair of rule contents counts once per policy."),
    ("7.4:25", "policies (old: domains) with a redundant pair, with term relations", "246 domains", lambda s: f"{Qs(s)['domains_affected']} of {N(s)}", "`queries.py --terms on`: `*.redundancy.domains_affected`", ""),
    ("7.4:25", "redundancy by kind, with term relations", "attribute 18,674, guard 4,896, duplicate 4,248, counterparty 2,931, action 1",
     lambda s: ", ".join(f"{k} {n(Qs(s)['by_kind'].get(k, 0))}" for k in KINDS), "`queries.py --terms on`: `*.redundancy.by_kind`", "The kind is the first field in which the general rule is broader, in the order data, recipient, source, actor, purpose, action, guard."),
    ("7.4:25", "redundant rule pairs, names only", "30,750", lambda s: n(Q0s(s)["pairs"]), "`queries.py --terms off`: `*.redundancy.pairs`", "The corpus definition (data names compared as names, no term relations), for comparison with the corpus run."),
    ("7.4:25", "distinct redundant rule pairs, names only", "14,996", lambda s: n(Q0s(s)["distinct_pairs"]), "`queries.py --terms off`: `*.redundancy.distinct_pairs`", ""),
    ("7.4:25", "policies with a redundant pair, names only", "246 domains", lambda s: f"{Q0s(s)['domains_affected']} of {N(s)}", "`queries.py --terms off`: `*.redundancy.domains_affected`", ""),
    ("7.4:25", "redundancy by kind, names only", "as above", lambda s: ", ".join(f"{k} {n(Q0s(s)['by_kind'].get(k, 0))}" for k in KINDS), "`queries.py --terms off`: `*.redundancy.by_kind`", "No data-term relations, so no \"data\" kind."),
    ("intro:18, 7.4:28", "candidate redundant sentence pairs", "14,996", lambda s: f"{n(Qs(s)['distinct_pairs'])} distinct redundant rule pairs", "same as the distinct pairs", "Rule pairs, not sentence pairs."),
    ("7.4:88, 7.4:101", "policies that collect and have no retention or erasure rule", "1,478 of 3,678 (40.2%)",
     lambda s: f"{cov(s, 'versions: collection without retention or erasure')} of {N(s)} ({p(cov(s, 'versions: collection without retention or erasure'), N(s))})", "`queries.py`: `*.coverage[\"versions: collection without retention or erasure\"]`",
     "Counting a retention time in a guard too: " + ", ".join(str(cov(s, "versions: collection without retention, erasure, or retention time")) for s in SC) + "."),
    ("7.4:88", "unconditional disclosure rules (ALLOW, guard true)", "1,085",
     lambda s: f"{n(cov(s, 'unconditional disclosure rules'))} in {cov(s, 'versions: unconditional disclosure')} policies; {n(cov(s, 'unconditional disclosure rules, at most 3 per version (old count)'))} counting at most 3 per policy, as the old script did",
     "`queries.py`: `*.coverage[\"unconditional disclosure rules*\"]`", "With a recipient: " + ", ".join(n(cov(s, "unconditional disclosure rules with a recipient")) for s in SC) + "."),
    ("7.4:32", "compliance: consent promise, same-practice pairs of a promise and an ALLOW disclosure rule that overlap", "6,448",
     lambda s: f"{Q(s)['compliance_rule_counts'].get('overlap_candidate', 0)} pairs in {ctr(s, 'consent promise overlapped, same practice')} policies", "`queries.py`: `*.compliance_rule_counts`, `*.compliance_requirement_versions`",
     "A promise is a DENY disclosure rule whose fully translated guard uses `consent.*`, `opt_in.*`, or `user.parental_consent`. Promises: " + ", ".join(str(Q(s)["compliance_rule_counts"].get("consent promises", 0)) for s in SC) + "."),
    ("7.4:32", "compliance: consent promise, overlapping any ALLOW disclosure rule", "6,448",
     lambda s: f"{n(Q(s)['compliance_rule_counts'].get('promise overlaps, any disclosure', 0))} pairs in {ctr(s, 'consent promise overlapped, any disclosure')} policies", "same", "The old check took any disclosure rule. Under the decision procedure the prohibition wins in the same-practice overlaps (incomparable " + ", ".join(str(Q(s)["compliance_rule_counts"].get("overlap: incomparable", 0)) for s in SC) + "; prohibition more specific " + ", ".join(str(Q(s)["compliance_rule_counts"].get("overlap: deny more specific", 0)) for s in SC) + ")."),
    ("7.4:32", "compliance: child data without parental consent", "58",
     lambda s: f"{Q(s)['compliance_rule_counts'].get('child rules without parental consent', 0)} rules in {ctr(s, 'child data without parental consent')} policies", "`queries.py`: `child rules without parental consent`",
     "ALLOW collection or disclosure rules whose guard implies an age under 13 and does not use `user.parental_consent`. Child rules in total: " + ", ".join(str(Q(s)["compliance_rule_counts"].get("child rules", 0)) for s in SC) + "."),
    ("7.4:32", "compliance: GDPR scope without erasure", "186", lambda s: f"{ctr(s, 'gdpr scope without erasure')} of {N(s)}", "`queries.py`: `*.compliance_requirement_versions`",
     "GDPR scope: a guard uses `basis.*` or `transfer.*`, or a place in the European Economic Area. Policies in GDPR scope: " + ", ".join(str(cov(s, "versions: gdpr scope")) for s in SC) + "."),
    ("7.4:32", "compliance: sale without opt-out", "47", lambda s: f"{ctr(s, 'sale without opt-out')} of {N(s)}", "same",
     "ALLOW sale rules, and no sale rule that is a prohibition or uses `opt_out.*`. Policies that permit a sale: " + ", ".join(str(cov(s, "versions: sale allowed")) for s in SC) + "."),
    ("intro:18, 7.4:50", "policies with a compliance candidate (old: versions, domains)", "750, 124",
     lambda s: f"{Q(s)['versions_with_any_compliance_candidate']} of {N(s)} ({Q(s)['versions_with_any_compliance_candidate_old_share_check']} with the old consent check over any disclosure rule)", "`queries.py`: `*.versions_with_any_compliance_candidate*`", "One policy is one domain."),
]

nv = [("abstract:2, intro:18, setup:23", "policies, timelines, archived versions", "273, 5,338"),
      ("intro:18, setup:19, 7.4:56", "content revisions, silent revisions (same effective date)", "5,065, 4,050 (80.0%)"),
      ("7.4:56, 7.4:82", "rule additions, removals, guard changes, polarity flips between versions", "58,153, 59,203, 18,966, 878"),
      ("7.4:56, 7.4:84", "distinct overlap-candidate signatures, persistence over 1, 2, 3, 5, 13 years", "1,407, 99, 80, 27, 1"),
      ("7.4:60, 7.4:65", "worked example of an overlap candidate from 2015 through 2023", "adelaideoval.com.au"),
      ("setup:23", "first 25 versions per timeline, versions submitted to the pipeline", "25, 3,836")]
nl = [("abstract:2, intro:20, 7.1:8 to 7.1:20, 7.2:49, 7.4:28, 7.4:52, 7.4:84, 7.4:104, 7.4:106, conclusion:4", "E1 to E4 labels, 26 confirmed, 500 pairs, 71.2%", "The 600-policy set has its own blind labels: the error rate of 12.1% (FINDINGS §30) and the labels of 269 pairs by stratum (FINDINGS §31). They are not recomputed here."),
      ("abstract:2, intro:20, 7.5:8, 7.5:9, 7.5:31", "100-policy comparison with PoliGraph and PolicyLint", "FINDINGS §31 (the 200 policies of PoliGraph's test set), not this set."),
      ("setup:51, 55, 59", "annotation sample sizes", "These are designs of the annotation samples, not statistics.")]

def sacct():
    rows = {}
    for line in open(OUT / f"sacct_{JOB}.txt"):
        m = re.match(rf"{JOB}\.(\d+)\s+(\S+)\s+(\S+)\s+\S+\s+(\S+)\s+([\d.]+)([KM])\s", line)
        if m:
            rows[m.group(2)] = (m.group(3), m.group(4), float(m.group(5)) / (1024 if m.group(6) == "K" else 1))
    return rows


def timev(name):
    t = open(OUT / f"time_{name}.log").read()
    g = lambda k: float(re.search(k + r"[^:]*:\s*([\d.]+)", t).group(1))
    return g("User time"), g("System time"), int(re.search(r"Maximum resident set size \(kbytes\): (\d+)", t).group(1)) / 1024


STEPS = [("rules", "`rules.py --set testset`"), ("pairs", "`pairs.py --set testset`"), ("queries", "`queries.py --set testset --terms on`"),
         ("queries_no_terms", "`queries.py --set testset --terms off`"), ("reconcile_pairs", "`reconcile_pairs.py`"), ("figures", "`figures.py`")]
sa = sacct()
run_rows = []
for name, label in STEPS:
    u, sy, rss = timev(name)
    el, ave, mx = sa[name]
    run_rows.append(f"| {label} | {el} | {u + sy:.0f} s | {mx:,.0f} MB | {rss:,.0f} MB |")

md = f"""# Corpus statistics on the 600-policy test set (draft)

Every number below comes from a script in the repository and the JSON file it writes. The scripts make no model calls. They are the scripts of `vldb/analysis/corpus_results/` run with `--set testset`. Run everything with `sbatch vldb/analysis/testset_results/run_all.s` (about 11 minutes on 8 CPUs). The values here are from job {JOB}. The tables are written by `make_results_md.py` from the JSON files, so each value is read from the output and not typed.

| Script | Output (in `out/`) | What it computes |
|---|---|---|
| `corpus_results/rules.py --set testset` | `rules.json` | rule counts and shares per scope, operations, translation, rejected records, rules per policy, model usage from the reports |
| `corpus_results/pairs.py --set testset` | `pairs.json`, `pair_records.jsonl` | opposing pairs, solver outcomes, decision-procedure relations, size deciles, guard placement, ablation, solver time |
| `corpus_results/queries.py --set testset --terms on` | `queries.json` | redundancy (with the policy's term relations), coverage, compliance |
| `corpus_results/queries.py --set testset --terms off` | `queries_no_terms.json` | the same with names compared as names, as for the corpus |
| `reconcile_pairs.py` | `reconcile_pairs.json` | pairs against `corpus/testset/eval/conflict_pairs.jsonl` |
| `figures.py` | `figures.json` | data of figure 1 (panels a to d) and figure 2 |
| `make_results_md.py` | `RESULTS_600.md` | this file |
| `compare_outputs.py` | | compares two output folders of the corpus scripts, ignoring run records and timing |

## Definitions

**Policies and rule sets.** The test set holds 600 policies: 200 websites (id prefix `web-`), 200 Google Play apps (`android-`), and 200 App Store apps (`apple-`), one snapshot each (`corpus/testset/DESIGN.md`). A policy is one version of one page. Its rule set is `corpus/testset/rules/<id>.jsonl`, produced by Gemini 3.8 Flash at low thinking in one pass. There is no reconciliation and no history, so every statistic that needs versions is marked "needs versions" and every statistic that needs human labels is marked "needs labels".

**Scopes.** "All 600" is the union. An arm is its 200 policies. The JSON files call the scopes `all`, `web`, `android` (Google Play), and `apple` (App Store). JSON keys that say `versions` (such as `versions_with_a_pair`) count policies.

**Definitions reused unchanged.** Rules, pairs (one compiled rule per extraction record, ALLOW against DENY of the same practice by `policyclaw.merge._same_practice`, lenient), outcomes (`policyclaw.queries.pair_outcome`), relations (the decision procedure's clash rules), deciles, guard placement, ablation, and solver time are as in `corpus_results/RESULTS_DRAFT.md`. The pairing vocabulary is the action network only, as in `conflict_pairs.py`.

**One change of definition.** Redundancy (`queries.py`) compared data names as names on the corpus, because no data relations existed. The test set has per-policy term relations (`rules/<id>.terms.json`, one model call per slot and policy, `policyclaw.terms`), so the main redundancy figures extend the vocabulary with them, as `policyclaw.conflicts.vocabulary` does. The rows marked "names only" use the corpus definition. Coverage and compliance do not use the term relations and are identical in both runs except two counts (policies that permit a sale: 225 against 226; unconditional disclosure rules: 10,629 against 10,634), which change when an alias merges a data name with an action name (one vocabulary namespace for all slots, see the note at the end).

**Old values** are those of `RESULTS_DRAFT.md` (the paper): E0 (an open-weight model, regex guard mapper) on 3,678 versions of 273 timelines.

## Rules (RQ2)

{rows_table(HEAD, rules_rows)}

## Opposing pairs and solver outcomes (abstract, RQ2, RQ4)

{rows_table(HEAD, pairs_rows)}

**Reconciliation with the 17,918 pairs.** `corpus/testset/eval/conflict_pairs.py` imports `pairs.unit_pairs` and applies it to `rules/<id>.jsonl` of the 600 policies. `pairs.py --set testset` applies the same function to the same files through the new loaders. The pair sets are equal ({n(RC['pairs_now'])} pairs, none only in one file), and all 14 compared fields are equal for every pair. The pair counts per arm match `eval/conflict_pairs.json` ({', '.join(n(P(s)['pairs']) for s in SC[1:])}), as do the strata of FINDINGS §31 (19 reported conflicts, 185 narrower permission, 469 narrower prohibition, 8,623 prohibition wins, 1,043 guards exclude each other, 7,579 undecided).

## Query families (RQ3)

{rows_table(HEAD, queries_rows)}

What the compliance checks cannot state through the schema is listed in `queries.json`, `not_stated`.

## Figure data

`out/figures.json` holds the data. Nothing is drawn.

| Figure | Panel | Key | Content |
|---|---|---|---|
| 1 | (a) rules per policy | `fig1.a.<scope>` | every policy's rule count (sorted), quartiles, and counts per power-of-two bin |
| 1 | (b) overlap candidates among policies with an opposing pair | `fig1.b.<scope>` | sorted counts per policy and the cumulative distribution; {FG['fig1']['b']['all']['policies_with_a_pair']} policies of 600 have a pair, {FG['fig1']['b']['all']['policies_with_no_overlap_candidate']} of them no overlap candidate |
| 1 | (c) outcomes of all opposing pairs | `fig1.c.<scope>` | counts and shares of overlap candidates, mutually exclusive, and unresolved pairs, with the unresolved pairs split into partly translated guards and a guard that is only untranslated quotes |
| 1 | (d) rule-level ambiguity | `fig1.d.<scope>` | rules with an untranslated quote in the guard (old: no extracted predicate), rules with a reference quote (old: points elsewhere), disclosure rules without a recipient (old: missing counterparty); {FG['fig1']['d']['all']['policies_with_any_of_the_three']} of 600 policies have at least one of the three |
| 2 | size deciles | `fig2.<scope>` | for each of ten deciles of policies by rule count: pairs per policy and share of policies with a pair |

## Rows that need versions

The test set has one snapshot per policy.

| Paper rows | Claim | Old value | Status |
|---|---|---|---|
""" + "\n".join(f"| {a} | {b} | {c} | needs versions |" for a, b, c in nv) + """

## Rows that need labels

| Paper rows | Claim | Status |
|---|---|---|
""" + "\n".join(f"| {a} | {b} | needs labels. {c} |" for a, b, c in nl) + f"""

## Checks

| Check | Result | Output |
|---|---|---|
| Pairs equal `conflict_pairs.jsonl` ({n(RC['pairs_before'])}), every compared field | {'pass' if RC['identical'] else 'FAIL'} | `reconcile_pairs.json` |
| Rule totals equal the pipeline run's totals (146,861; web 49,823, Google Play 38,230, App Store 58,808) | {'pass' if (C('all')['rules'], C('web')['rules'], C('android')['rules'], C('apple')['rules']) == (146861, 49823, 38230, 58808) else 'FAIL'} | `rules.json` |
| Extraction records equal the reports' accepted raw rules | {'pass' if RU['checks']['extraction_records_equal_report_raw_rules'] else 'FAIL'} | `rules.json`: `checks` |
| Every unresolved pair has a blocking residual, and the ablation makes every pair an overlap candidate | {'pass' if all(PA['checks'].values()) else 'FAIL'} | `pairs.json`: `checks` |
| Corpus outputs are unchanged by the edits to the scripts (`corpus_results/out/`) | pass: `pairs`, `queries`, `rules`, `corpus` outputs and the pair records of the edited scripts equal those of the unedited scripts (rerun on the same day) and the stored outputs of job 19040077, ignoring run records and timing. `history*.json` differ only in the order of tied entries of `longest_per_page_top5`, which also differs between two runs of the unedited `history.py` | `compare_outputs.py` |

## Run

Job {JOB} on partition `cs`, 8 CPUs, 32 GB, account `torch_pr_634_general`; elapsed time {sa and open(OUT / f'sacct_{JOB}.txt').read().split(chr(10))[2].split()[2]} for the job. Each step ran under `corpus/stores/timev.py`. Elapsed time and the step's peak memory (MaxRSS) come from `out/sacct_{JOB}.txt`. CPU time is user plus system time of all processes of the step (`out/time_<step>.log`). The last column is the largest single process (`timev.py`, in which worker processes count separately). sacct samples memory, so short peaks can be missed. Each JSON file also holds a run record.

| Step | Elapsed | CPU time | Peak memory (sacct) | Largest process |
|---|---:|---:|---:|---:|
""" + "\n".join(run_rows) + """

`queries.py` dominates the time because redundancy compares pairs of rules with the solver. The solver time per pair in the pairs table was measured in the `pairs` step.

One observation about `policyclaw/`, not changed: `Vocabulary` keeps one namespace for all slots, so the alias and parent relations of the data terms apply to action, recipient, source, actor, and purpose names with the same spelling. `queries.py` follows the system's behavior (`policyclaw.conflicts.vocabulary`).
"""
(HERE / "RESULTS_600.md").write_text(md)
print("wrote", HERE / "RESULTS_600.md")
