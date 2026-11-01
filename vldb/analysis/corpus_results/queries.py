import collections, json, multiprocessing as mp

import common as C
from common import SCHEMA
from policyclaw.guards import atoms
from policyclaw.queries import SLOTS, _more_specific, _same_scope, _Solver, pair_outcome

import z3

from policyclaw.conflicts import vocabulary as vocabulary_with_relations

USE_TERMS = False

CHILD = {"op": "cmp", "var": "user.age", "cmp": "<", "value": 13}
CONSENT = ("consent.*", "opt_in.*", "user.parental_consent")
GDPR_SCOPE = ("basis.*", "transfer.*")
PLACES = ("user.jurisdiction", "processing.location")
EEA = "European Economic Area"
COMPLIANCE = ("child data without parental consent", "gdpr scope without erasure", "sale without opt-out",
              "consent promise overlapped, same practice")
FIELD_ORDER = ("data", "recipient", "source", "actor", "purpose", "action", "guard")
for v in CONSENT + GDPR_SCOPE + PLACES + (CHILD["var"],):
    assert SCHEMA.variable(v), v
assert SCHEMA.canonical_value(PLACES[0], EEA) == EEA


def eea_scope(guard):
    return any(a["op"] == "eq" and a["var"] in PLACES and EEA in [a["value"]] + SCHEMA.ancestors(a["var"], a["value"])
               for a in atoms(guard))


def entails(g, h):
    sv = _Solver([g, h])
    return not sv.sat(sv.z(g), z3.Not(sv.z(h)), with_facts=False)


def broader_fields(vocab, a, b):
    out = [s for s in SLOTS if not vocab.covers(getattr(b, s), getattr(a, s))]
    return out + (["guard"] if not entails(a.guard, b.guard) else [])


def above(vocab, name):
    seen, stack = {""}, [vocab.canon(name)]
    while stack:
        x = stack.pop()
        if x not in seen:
            seen.add(x)
            stack.extend(vocab.parents.get(x, ()))
    return seen


def redundancy(rules, vocab):
    out, groups = [], collections.defaultdict(list)
    for i, r in enumerate(rules):
        groups[(r.polarity, vocab.canon(r.data))].append((i, r))
    for j, b in enumerate(rules):
        for i, a in (x for d in above(vocab, b.data) for x in groups.get((b.polarity, d), [])):
            if i == j or C.record_id(a.id) == C.record_id(b.id):
                continue
            if not all(vocab.covers(getattr(a, s), getattr(b, s)) for s in SLOTS):
                continue
            sv = _Solver([a.guard, b.guard])
            if _same_scope(sv, vocab, a, b):
                if i < j:
                    out.append(("duplicate", a, b, []))
            elif _more_specific(sv, vocab, b, a):
                out.append(("subsumed", a, b, broader_fields(vocab, a, b)))
    return out


def unit_queries(u):
    rows = C.unit_rows(u)
    rules = [C.rule(r) for r in rows]
    if USE_TERMS:
        path = C.TESTSET / "rules" / f"{u}.terms.json"
        vocab = vocabulary_with_relations(rules, json.load(open(path))["relations"] if path.exists() else {})
    else:
        vocab = C.vocabulary(r["action"] for r in rows)
    under = lambda op, r: C.under(vocab, op, r.action)
    uses = lambda r, names: bool(C.variables(r.guard) & set(names))
    res = {"rules": len(rules), "data names that are vocabulary nodes": sum(bool(vocab.parents.get(vocab.canon(r.data))) for r in rules)}
    res["redundant"] = [(k, a.id, b.id, f) for k, a, b, f in redundancy(rules, vocab)]
    res["collection"] = any(r.polarity == "ALLOW" and under("collection", r) for r in rules)
    res["retention or erasure"] = any(under("storage", r) or under("erasure or destruction", r) for r in rules)
    res["retention or erasure or retention time"] = res["retention or erasure"] or any(uses(r, ["retention.days"]) for r in rules)
    shares = [r for r in rules if r.polarity == "ALLOW" and under("disclosure", r) and C.is_true(r.guard)]
    res["unconditional disclosures"] = len(shares)
    res["unconditional disclosures with a recipient"] = sum(bool(r.recipient) for r in shares)
    child = [r for r in rules if r.polarity == "ALLOW" and (under("collection", r) or under("disclosure", r))
             and uses(r, [CHILD["var"]]) and entails(r.guard, CHILD)]
    res["child rules without parental consent"] = sum(not uses(r, ["user.parental_consent"]) for r in child)
    res["child rules"] = len(child)
    res["gdpr scope"] = any(uses(r, GDPR_SCOPE) or eea_scope(r.guard) for r in rules)
    res["erasure"] = any(under("erasure or destruction", r) for r in rules)
    sale = [r for r in rules if under("sale", r)]
    res["sale allowed"] = any(r.polarity == "ALLOW" for r in sale)
    res["sale opt-out or prohibition"] = any(r.polarity == "DENY" or uses(r, ["opt_out.*"]) for r in sale)
    promises = [r for r in rules if r.polarity == "DENY" and under("disclosure", r) and uses(r, CONSENT) and not uses(r, ["residual"])]
    allows = [r for r in rules if r.polarity == "ALLOW" and under("disclosure", r)]
    res["consent promises"] = len(promises)
    res["promise overlaps, any disclosure"] = sum(pair_outcome(a.guard, p.guard)["outcome"] == "overlap_candidate"
                                                  for p in promises for a in allows)
    res["promise ids"] = [p.id for p in promises]
    res["content"] = {r["id"]: content(r) for r in rows}
    return u, res


def content(row):
    return json.dumps({k: v for k, v in row.items() if k not in ("id", "evidence", "reconcile")}, sort_keys=True)


def scope_counts(vs, rules, out, same_practice, sites):
    red, kinds, fields, distinct = collections.Counter(), collections.Counter(), collections.Counter(), set()
    cov, comp, affected = collections.Counter(), collections.Counter(), collections.defaultdict(set)
    for v in vs:
        u, site = C.unit(v, rules), v["site_id"]
        r, key, dom = out[u], (site, v["version_index"]), sites[site]["domain"]
        for kind, a, b, f in r["redundant"]:
            red["pairs"] += 1
            kinds[kind if kind == "duplicate" else next(x for x in FIELD_ORDER if x in f)] += 1
            fields.update(f)
            distinct.add((site, r["content"][a], r["content"][b]))
        if r["redundant"]:
            affected["redundancy versions"].add(key)
            affected["redundancy domains"].add(dom)
        cov["versions with rules"] += r["rules"] > 0
        red["data names that are vocabulary nodes"] += r["data names that are vocabulary nodes"]
        for name, hit in (("collection without retention or erasure", r["collection"] and not r["retention or erasure"]),
                          ("collection without retention, erasure, or retention time",
                           r["collection"] and not r["retention or erasure or retention time"]),
                          ("child data without parental consent", r["child rules without parental consent"] > 0),
                          ("gdpr scope without erasure", r["gdpr scope"] and not r["erasure"]),
                          ("sale without opt-out", r["sale allowed"] and not r["sale opt-out or prohibition"]),
                          ("consent promise overlapped, same practice", same_practice[u]["overlap_candidate"] > 0),
                          ("consent promise overlapped, any disclosure", r["promise overlaps, any disclosure"] > 0),
                          ("unconditional disclosure", r["unconditional disclosures"] > 0)):
            cov[f"versions: {name}"] += hit
            if hit:
                affected[name].add(dom)
            for variant, names in (("", COMPLIANCE), (" (old share check)", COMPLIANCE[:3] + ("consent promise overlapped, any disclosure",))):
                if hit and name in names:
                    affected[f"any compliance versions{variant}"].add(key)
                    affected[f"any compliance domains{variant}"].add(dom)
        cov["unconditional disclosure rules"] += r["unconditional disclosures"]
        cov["unconditional disclosure rules, at most 3 per version (old count)"] += min(3, r["unconditional disclosures"])
        cov["unconditional disclosure rules with a recipient"] += r["unconditional disclosures with a recipient"]
        cov["versions: gdpr scope"] += r["gdpr scope"]
        cov["versions: sale allowed"] += r["sale allowed"]
        for k in ("child rules", "child rules without parental consent", "consent promises", "promise overlaps, any disclosure"):
            comp[k] += r[k]
        comp.update(same_practice[u])
    n = cov["versions with rules"]
    return {"versions": len(vs),
            "redundancy": {"pairs": red["pairs"], "by_kind": dict(kinds), "by_broader_field": dict(fields), "distinct_pairs": len(distinct),
                           "versions_affected": len(affected["redundancy versions"]),
                           "domains_affected": len(affected["redundancy domains"]),
                           "rules_whose_data_name_is_an_action_node": red["data names that are vocabulary nodes"]},
            "coverage": dict(cov),
            "coverage_shares_pct": {k: C.pct(v, n) for k, v in cov.items() if k.startswith("versions:")},
            "compliance_requirement_versions": {k: cov[f"versions: {k}"] for k in COMPLIANCE + ("consent promise overlapped, any disclosure",)},
            "compliance_rule_counts": dict(comp),
            "domains_affected": {k: len(v) for k, v in affected.items() if not k.startswith(("redundancy", "any"))},
            "versions_with_any_compliance_candidate": len(affected["any compliance versions"]),
            "domains_with_any_compliance_candidate": len(affected["any compliance domains"]),
            "versions_with_any_compliance_candidate_old_share_check": len(affected["any compliance versions (old share check)"]),
            "domains_with_any_compliance_candidate_old_share_check": len(affected["any compliance domains (old share check)"])}


def main():
    global USE_TERMS
    args = C.options(workers=True)
    USE_TERMS = C.SET == "testset" and args.terms == "on"
    vs, sites = C.versions(), C.sites()
    units = sorted({C.unit(v, args.rules) for v in vs})
    with mp.Pool(args.workers) as pool:
        out = dict(pool.imap_unordered(unit_queries, units, chunksize=4))
    same_practice = collections.defaultdict(collections.Counter)
    for p in C.jsonl(C.OUT / C.out_name("pair_records", args.rules).replace(".json", ".jsonl")):
        if p["deny"] in set(out[p["unit"]]["promise ids"]):
            same_practice[p["unit"]][p["outcome"]] += 1
            if p["outcome"] == "overlap_candidate":
                same_practice[p["unit"]][f"overlap: {p['relation']}"] += 1
    res = {"rules": args.rules, "unstable_pages": C.unstable_pages(vs)}
    if C.SET == "testset":
        res["term_relations"] = USE_TERMS
    for name, scope in C.scopes(vs):
        res[name] = scope_counts(scope, args.rules, out, same_practice, sites)
    res["not_stated"] = NOT_STATED
    C.write("queries_no_terms.json" if C.SET == "testset" and not USE_TERMS else C.out_name("queries", args.rules), res)


NOT_STATED = {
    "child data by data name": "the old check also took rules whose data name contains 'child'; data names are open text without a hierarchy in the schema",
    "GDPR named in the text": "the old check also searched the condition and sentence for 'gdpr'; the schema states GDPR scope only through legal bases, transfer safeguards, and places in the European Economic Area",
    "deletion requests in guards": "the old check also took guard atoms named like deletion or erasure; request.* names are chosen by the translator, so only the erasure operation counts",
    "sensitive data only permitted": "the old coverage check needs a sensitivity label per data item; the schema has no data categories",
    "data subsumption": "redundancy by a broader data item needs the policy's data relations (policyclaw/terms.py, one model call per policy), which this corpus run does not have, so data names are compared as names"}


if __name__ == "__main__":
    main()
