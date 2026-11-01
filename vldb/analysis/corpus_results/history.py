import collections, json

import common as C

FLIP = {"ALLOW": "DENY", "DENY": "ALLOW"}
KINDS = (("overlap_candidate", lambda s: s[2] == "overlap_candidate"),
         ("same scope conflict", lambda s: s[2] == "overlap_candidate" and s[3] == "same scope"),
         ("mutually_exclusive", lambda s: s[2] == "mutually_exclusive"),
         ("unresolved", lambda s: s[2] == "unresolved"))


def content(r):
    return json.dumps({**{k: v for k, v in r.items() if k not in ("id", "evidence", "reconcile")}, "quote": r["evidence"][1]},
                      sort_keys=True)


def rule_set(rows, vocab):
    guards = collections.defaultdict(set)
    for r in rows:
        guards[C.practice(vocab, r)].add(json.dumps(r["guard"], sort_keys=True))
    return {"rules": {(p, g) for p, gs in guards.items() for g in gs}, "guards": guards, "by_id": {r["id"]: r for r in rows}}


def text_sections(sha, vocab):
    by_section = collections.defaultdict(list)
    for r in C.rule_rows(sha):
        by_section[C.section_id(r["id"])].append(r)
    contents, keys = collections.defaultdict(list), collections.defaultdict(set)
    for sid, text in C.sections(sha).items():
        rs = by_section.get(sid, [])
        contents[text].append(sorted(content(r) for r in rs))
        keys[text] |= {(C.practice(vocab, r), json.dumps(r["guard"], sort_keys=True)) for r in rs}
    return {"contents": contents, "keys": keys}


def diff(a, b):
    pa, pb = set(a["guards"]), set(b["guards"])
    added_p, removed_p = pb - pa, pa - pb
    return {"rules added": len(b["rules"] - a["rules"]), "rules removed": len(a["rules"] - b["rules"]),
            "practices added": len(added_p), "practices removed": len(removed_p),
            "guard changes": sum(a["guards"][p] != b["guards"][p] for p in pa & pb),
            "polarity flips": len({p[1:] for p in removed_p if (FLIP[p[0]],) + p[1:] in added_p}),
            "identical rule sets": a["rules"] == b["rules"]}


def changed_sections(a, b, sa, sb):
    changed = set().union(*[k for t, k in sb["keys"].items() if t not in sa["keys"]])
    return {"rules of changed sections": len(changed),
            "rules of changed sections already in the earlier version": len(changed & a["rules"]),
            "practices of changed sections": len({p for p, _ in changed}),
            "practices of changed sections already in the earlier version": len({p for p, _ in changed} & set(a["guards"]))}


def persistence(sigs, vs):
    out, spans, longest = collections.Counter(), [], None
    for sig, idx in sigs.items():
        first, last = C.year(min(vs[i]["first_snapshot_ts"] for i in idx)), C.year(max(vs[i]["last_snapshot_ts"] for i in idx))
        span = last - first + 1
        spans.append(span)
        if longest is None or span > longest["span_years"]:
            longest = {"site_id": vs[0]["site_id"], "allow": sig[0], "deny": sig[1], "outcome": sig[2], "first_year": first,
                       "last_year": last, "span_years": span, "versions": len(idx), "of_page_versions": len(vs)}
        out["signatures"] += 1
        out["in 2 or more versions"] += len(idx) >= 2
        out["reappears after a version without it"] += max(idx) - min(idx) + 1 > len(idx)
    return out, spans, longest


def scope_stats(vs, rules, sets, sections, pairs):
    totals, sig_stats = collections.Counter(), collections.defaultdict(collections.Counter)
    spans, longest = collections.defaultdict(list), collections.defaultdict(list)
    for site, pvs in C.pages(vs).items():
        for a, b in zip(pvs, pvs[1:]):
            ua, ub = C.unit(a, rules), C.unit(b, rules)
            totals.update(diff(sets[ua], sets[ub]))
            totals["revisions"] += 1
            if rules == "extracted":
                totals.update(changed_sections(sets[ua], sets[ub], sections[ua], sections[ub]))
        for kind, keep in KINDS:
            sigs = collections.defaultdict(set)
            for i, v in enumerate(pvs):
                for s in pairs[C.unit(v, rules)]:
                    if keep(s):
                        sigs[s[:3]].add(i)
            c, sp, lg = persistence(sigs, pvs)
            sig_stats[kind].update(c)
            spans[kind] += sp
            if lg:
                longest[kind].append(lg)
    return {"revisions": dict(totals),
            "signatures": {k: {**sig_stats[k], "span_years": dict(sorted(collections.Counter(spans[k]).items())),
                               "span_2_or_more_years": sum(s >= 2 for s in spans[k]),
                               "span_3_or_more_years": sum(s >= 3 for s in spans[k]),
                               "span_5_or_more_years": sum(s >= 5 for s in spans[k]),
                               "max_span_years": max(spans[k], default=0),
                               "longest_per_page_top5": sorted(longest[k], key=lambda x: (-x["span_years"], x["site_id"]))[:5]}
                           for k, _ in KINDS}}


def checks(vs, sections):
    c = collections.Counter()
    for pvs in C.pages(vs).values():
        for a, b in zip(pvs, pvs[1:]):
            sa, sb = sections[a["cleaned_sha256"]]["contents"], sections[b["cleaned_sha256"]]["contents"]
            for text in sa.keys() & sb.keys():
                c["unchanged sections between consecutive versions"] += 1
                c["unchanged sections with different rules"] += sa[text][0] != sb[text][0]
    occurrences = collections.defaultdict(set)
    for x in sections.values():
        for text, occ in x["contents"].items():
            occurrences[text].update(json.dumps(o) for o in occ)
    c["distinct section texts"] = len(occurrences)
    c["distinct section texts with different rules in different occurrences"] = sum(len(o) > 1 for o in occurrences.values())
    return dict(c)


def main():
    args = C.options()
    vs = C.versions()
    shas = sorted({v["cleaned_sha256"] for v in vs})
    vocab = C.vocabulary(r["action"] for s in shas for r in C.rule_rows(s))
    sections = {s: text_sections(s, vocab) for s in shas}
    units = sorted({C.unit(v, args.rules) for v in vs})
    sets = {u: rule_set(C.unit_rows(u), vocab) for u in units}
    pairs = collections.defaultdict(set)
    for p in C.jsonl(C.OUT / C.out_name("pair_records", args.rules).replace(".json", ".jsonl")):
        by_id = sets[p["unit"]]["by_id"]
        pairs[p["unit"]].add((C.practice(vocab, by_id[p["allow"]]), C.practice(vocab, by_id[p["deny"]]), p["outcome"], p["relation"]))
    res = {"rules": args.rules, "unstable_pages": C.unstable_pages(vs)}
    for name, scope in C.scopes(vs):
        res[name] = scope_stats(scope, args.rules, sets, sections, pairs)
    res["checks"] = checks(vs, sections)
    C.write(C.out_name("history", args.rules), res)


if __name__ == "__main__":
    main()
