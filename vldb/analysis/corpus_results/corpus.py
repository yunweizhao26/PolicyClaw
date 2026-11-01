import collections, importlib.util, statistics

import common as C

_spec = importlib.util.spec_from_file_location("final_versions", C.CORPUS / "final_versions.py")
FV = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(FV)
SIZE_BINS = ((1, 1), (2, 2), (3, 5), (6, 20), (21, 100), (101, None))
PAGE_BINS = ((1, 1), (2, 5), (6, 10), (11, 20), (21, 50), (51, None))


def binned(xs, bins):
    return {f"{lo}" if lo == hi else f"{lo}+" if hi is None else f"{lo}-{hi}":
            sum(lo <= x and (hi is None or x <= hi) for x in xs) for lo, hi in bins}


def identity(sha):
    return FV.first_occurrences(FV.normalize(open(C.CORPUS / "final_text" / f"{sha}.txt", encoding="utf-8").read())).split("\n")


def effective(v):
    return v["policy_date"] if v["policy_date_source"] == "effective" else None


def page_stats(vs):
    per_page = [len(x) for x in C.pages(vs).values()]
    reverts = collections.Counter(v["site_id"] for v in vs if v["revert_of"] is not None)
    return {"pages": len(per_page), "versions": len(vs), "distinct_texts": len({v["cleaned_sha256"] for v in vs}),
            "pages_with_2_or_more_versions": sum(n >= 2 for n in per_page),
            "versions_per_page": {"mean": round(statistics.mean(per_page), 2), "median": statistics.median(per_page),
                                  "p90": statistics.quantiles(per_page, n=10, method="inclusive")[-1], "max": max(per_page),
                                  "histogram": binned(per_page, PAGE_BINS)},
            "reverts": {"versions": sum(reverts.values()), "pages_with_a_revert": len(reverts),
                        "a_b_a": sum(v["revert_of"] is not None and v["revert_of"] == v["version_index"] - 2 for v in vs)},
            "versions_by_first_snapshot_year": dict(sorted(collections.Counter(C.year(v["first_snapshot_ts"]) for v in vs).items()))}


def revision_stats(vs, date_lines):
    kinds, sizes, by_year, examples = collections.Counter(), [], collections.Counter(), collections.defaultdict(list)
    for site, pvs in C.pages(vs).items():
        for a, b in zip(pvs, pvs[1:]):
            la, lb = identity(a["cleaned_sha256"]), identity(b["cleaned_sha256"])
            _, changed = FV.line_diff(la, lb)
            sizes.append(len(changed))
            ea, eb = effective(a), effective(b)
            dated = "silent" if ea and ea == eb else "date changed" if ea and eb else "no effective date on one or both"
            order = set(la) == set(lb)
            date_only = bool(changed) and not order and all(any(k in x for k in date_lines[site]) for x in changed)
            change = "order only" if order else "date only" if date_only else "other text"
            for group in ("all", dated):
                kinds[(group, change)] += 1
                kinds[(group, "revisions")] += 1
            by_year[C.year(b["first_snapshot_ts"])] += 1
            if change != "other text" and len(examples[change]) < 3:
                examples[change].append({"site_id": site, "from": a["version_index"], "to": b["version_index"],
                                         "changed_lines": [x[:160] for x in changed[:4]]})
    table = collections.defaultdict(dict)
    for (group, change), n in sorted(kinds.items()):
        table[group][change] = n
    silent, n_rev = kinds[("silent", "revisions")], kinds[("all", "revisions")]
    return {"consecutive_pairs": n_rev, "by_effective_date_and_change": table, "silent_share_pct": C.pct(silent, n_rev),
            "silent_share_of_pairs_with_two_effective_dates_pct": C.pct(silent, silent + kinds[("date changed", "revisions")]),
            "changed_lines": {"median": statistics.median(sizes), "histogram": binned(sizes, SIZE_BINS)},
            "revisions_by_year_of_later_version": dict(sorted(by_year.items())), "examples": examples,
            "every_revision_changes_a_line": all(n > 0 for n in sizes)}


def main():
    vs, sites = C.versions(), C.sites()
    by_page = C.pages(vs)
    rows = C.jsonl(C.CORPUS / "versions.jsonl")
    folder_page = {f: s for s, x in sites.items() for f in x["url_folders"]}
    date_lines = collections.defaultdict(set)
    for r in rows:
        if r.get("date_line") and FV.line_key(r["date_line"]):
            date_lines[folder_page[r["url_folder"]]].add(FV.line_key(r["date_line"]))
    unstable = C.unstable_pages(vs)
    res = {"captures": sum(s["n_captures"] for s in sites.values()),
           "captures_without_policy_body": sum(s["n_captures_no_body"] for s in sites.values()),
           "visible_text_versions": len(rows), "distinct_visible_texts": len({r["text_sha256"] for r in rows}),
           "pages": len(sites), "domains": len({s["domain"] for s in sites.values()}), "pages_with_a_version": len(by_page),
           "unstable_pages": [{"site_id": s, "versions": len(by_page[s]),
                               "reverts": sum(v["revert_of"] is not None for v in by_page[s])} for s in unstable]}
    for name, scope in C.scopes(vs):
        res[name] = {**page_stats(scope), "revisions": revision_stats(scope, date_lines)}
    res["versions_by_effective_date_year"] = dict(sorted(collections.Counter(
        C.year(effective(v)) if effective(v) else "none" for v in vs).items(), key=lambda kv: str(kv[0])))
    res["date_lines"] = {"pages_with_a_date_line": len(date_lines),
                         "versions_with_effective_date": sum(bool(effective(v)) for v in vs),
                         "of_these_text_contains_a_date_line_of_its_page": sum(
                             bool(effective(v)) and any(k in x for x in identity(v["cleaned_sha256"]) for k in date_lines[v["site_id"]])
                             for v in vs)}
    a = res["all_pages"]
    res["checks"] = {"versions_equal_sum_over_pages": len(vs) == sum(s["n_final_versions"] for s in sites.values()),
                     "reverts_equal_sum_over_pages": a["reverts"]["versions"] == sum(s["n_reverts"] for s in sites.values()),
                     "revisions_equal_versions_minus_pages": a["revisions"]["consecutive_pairs"] == len(vs) - len(by_page),
                     "every_revision_changes_a_line": a["revisions"]["every_revision_changes_a_line"]}
    C.write("corpus.json", res)


if __name__ == "__main__":
    main()
