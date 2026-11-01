import collections, json, math, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "analysis/corpus_results"))
import common as C  # noqa: E402

C.use_testset()
SCOPES = ("all",) + C.ARMS


def main():
    rules, pairs = json.load(open(C.OUT / "rules.json")), json.load(open(C.OUT / "pairs.json"))
    recs = C.jsonl(C.OUT / "pair_records.jsonl")
    per = rules["per_policy"]
    members = {s: [u for u, p in per.items() if s == "all" or p["arm"] == s] for s in SCOPES}
    overlap = collections.Counter(r["unit"] for r in recs if r["outcome"] == "overlap_candidate")
    npairs = collections.Counter(r["unit"] for r in recs)
    out = {"scopes": {"all": "600 policies", "web": "200 websites", "android": "200 Google Play apps", "apple": "200 App Store apps"},
           "fig1": {"a": {}, "b": {}, "c": {}, "d": {}}, "fig2": {}}
    for s in SCOPES:
        us = members[s]
        n = sorted(per[u]["rules"] for u in us)
        bins = collections.Counter(int(math.log2(x)) for x in n)
        out["fig1"]["a"][s] = {"policies": len(n), "rules_per_policy_sorted": n, "min": n[0], "q1": C.quantile(n, .25),
                               "median": statistics.median(n), "q3": C.quantile(n, .75), "max": n[-1],
                               "log2_bins": [{"from": 2 ** k, "to_exclusive": 2 ** (k + 1), "policies": bins[k]} for k in range(min(bins), max(bins) + 1)]}
        withpair = [u for u in us if npairs[u]]
        counts = sorted(overlap[u] for u in withpair)
        out["fig1"]["b"][s] = {"policies_with_a_pair": len(withpair), "overlap_candidates_per_policy_sorted": counts,
                               "policies_with_no_overlap_candidate": sum(c == 0 for c in counts),
                               "cdf": [{"overlap_candidates_at_most": x, "fraction_of_policies": round(sum(c <= x for c in counts) / len(counts), 4)}
                                       for x in sorted(set(counts))]}
        p = pairs[s]
        un = p["outcomes"]["unresolved"]
        only = p["unresolved_blocking"]["a_guard_entirely_untranslated"]
        out["fig1"]["c"][s] = {"pairs": p["pairs"], "outcomes": p["outcomes"], "outcome_shares_pct": p["outcome_shares_pct"],
                               "unresolved_partly_translated": un - only, "unresolved_a_guard_only_untranslated_quotes": only,
                               "decided_share_pct": p["decided_share_pct"]}
        c = rules["policies"][s]["counts"]
        sh = rules["policies"][s]["shares_pct"]
        out["fig1"]["d"][s] = {"rules": c["rules"], "guard_with_untranslated_quote": c["guard with a residual"],
                               "guard_with_untranslated_quote_pct": sh["guard with a residual"],
                               "guard_only_untranslated_quotes": c["guard only residuals"], "guard_only_untranslated_quotes_pct": sh["guard only residuals"],
                               "rules_with_a_reference": c["with references"], "rules_with_a_reference_pct": sh["with references"],
                               "disclosure_rules": c["disclosure"], "disclosure_without_recipient": c["disclosure without recipient"],
                               "disclosure_without_recipient_pct_of_rules": sh["disclosure without recipient, of rules"],
                               "disclosure_without_recipient_pct_of_disclosures": sh["disclosure without recipient, of disclosures"],
                               "policies_with_any_of_the_three": sum(bool(per[u]["guard with a residual"] or per[u]["with references"]
                                                                          or per[u]["disclosure without recipient"]) for u in us)}
        out["fig2"][s] = [{"decile": d["decile"], "policies": d["versions"], "rules_min": d["rules_min"], "rules_median": d["rules_median"],
                           "rules_max": d["rules_max"], "pairs": d["pairs"], "pairs_per_policy": d["pairs_per_version"],
                           "policies_with_pair_pct": d["versions_with_pair_pct"]} for d in p["size_deciles"]]
    (C.OUT / "figures.json").write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", C.OUT / "figures.json")


if __name__ == "__main__":
    main()
