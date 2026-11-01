from policyclaw.conflicts import find_conflicts
from policyclaw.queries import Rule, Vocabulary


def b(var):
    return {"op": "bool", "var": var}


def neg(g):
    return {"op": "not", "arg": g}


VOCAB = Vocabulary(parents={"location": ["personal information"], "email address": ["personal information"],
                            "health data": ["personal information"], "sell": ["share"],
                            "advertisers": ["third parties"], "law enforcement": ["third parties"]})


def pair(rules):
    found = find_conflicts(rules, VOCAB)
    assert len(found) <= 1
    return found[0] if found else None


def test_blanket_prohibition_and_a_narrower_permission_contradict():
    p = pair([Rule("d", "DENY", "collect", "personal information"), Rule("a", "ALLOW", "collect", "location")])
    assert p["relation"] == "permission inside prohibition" and p["contradiction"]


def test_carve_out_from_a_general_permission_is_consistent():
    child = {"op": "cmp", "var": "user.age", "cmp": "<", "value": 13}
    p = pair([Rule("a", "ALLOW", "collect", "personal information"), Rule("d", "DENY", "collect", "personal information", guard=child)])
    assert p["relation"] == "prohibition inside permission" and not p["contradiction"]


def test_stated_exception_keeps_the_rules_apart():
    law = b("context.required_by_law")
    p = pair([Rule("d", "DENY", "disclose", "email address", recipient="third parties", guard=neg(law)),
              Rule("a", "ALLOW", "disclose", "personal information", recipient="law enforcement", guard=law)])
    assert p["outcome"] == "mutually_exclusive" and not p["contradiction"]


def test_incomparable_scopes_are_consistent():
    p = pair([Rule("a", "ALLOW", "share", "personal information", recipient="advertisers"),
              Rule("d", "DENY", "sell", "email address")])
    assert p["relation"] == "incomparable" and not p["contradiction"]


def test_unrelated_data_are_not_compared():
    assert pair([Rule("d", "DENY", "collect", "health data"), Rule("a", "ALLOW", "collect", "location")]) is None
