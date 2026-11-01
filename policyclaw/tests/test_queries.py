from policyclaw.guards import TRUE
from policyclaw.queries import Rule, Scenario, Vocabulary, decide, pair_outcome


def b(var):
    return {"op": "bool", "var": var}


def neg(g):
    return {"op": "not", "arg": g}


def conj(*gs):
    return {"op": "and", "args": list(gs)}


def age(cmp, value):
    return {"op": "cmp", "var": "user.age", "cmp": cmp, "value": value}


def eq(var, value):
    return {"op": "eq", "var": var, "value": value}


VOCAB = Vocabulary(parents={"email address": ["contact information", "personal information"],
                            "contact information": ["personal information"],
                            "advertisers": ["third parties"],
                            "law enforcement": ["third parties"]})

CHILDREN = Rule("r1", "DENY", "collect", "personal information",
                guard=conj(age("<", 13), neg(b("user.parental_consent"))))
REVEAL = Rule("r2", "DENY", "disclose", "email address", recipient="third parties",
              guard=conj(neg(b("context.required_by_law")), neg(b("user.consented"))))
LAW = Rule("r3", "ALLOW", "disclose", "personal information", recipient="law enforcement",
           guard=b("context.required_by_law"))
SELL = Rule("r4", "DENY", "sell", "personal information", recipient="third parties", purpose="marketing")


def test_child_rule_uses_age_arithmetic():
    assert decide([CHILDREN], Scenario("collect", "email address", facts=[age("==", 10)]), VOCAB).verdict == "conditional"
    assert decide([CHILDREN], Scenario("collect", "email address", facts=[age("==", 10)])).verdict == "not_addressed"
    assert decide([CHILDREN], Scenario("collect", "email address",
                                       facts=[age("==", 10), neg(b("user.parental_consent"))]), VOCAB).verdict == "prohibited"
    assert decide([CHILDREN], Scenario("collect", "email address", facts=[age("==", 15)]), VOCAB).verdict == "not_addressed"


def test_unstated_age_is_named_as_the_missing_fact():
    d = decide([CHILDREN], Scenario("collect", "email address", facts=[age("<", 18)]), VOCAB)
    assert d.verdict == "conditional"
    needed = {a.get("var") for s in d.statuses for a in s.needed}
    assert needed == {"user.age", "user.parental_consent"}


def test_exception_and_hierarchy():
    court = Scenario("disclose", "email address", recipient="law enforcement",
                     facts=[b("context.required_by_law")])
    assert decide([REVEAL, LAW], court, VOCAB).verdict == "permitted"
    ads = Scenario("disclose", "email address", recipient="advertisers",
                   facts=[neg(b("context.required_by_law")), neg(b("user.consented"))])
    assert decide([REVEAL, LAW], ads, VOCAB).verdict == "prohibited"


def test_purpose_limits_a_prohibition():
    assert decide([SELL], Scenario("sell", "email address", recipient="advertisers", purpose="marketing"),
                  VOCAB).verdict == "prohibited"
    assert decide([SELL], Scenario("sell", "email address", recipient="advertisers", purpose="analytics"),
                  VOCAB).verdict == "not_addressed"
    d = decide([SELL], Scenario("sell", "email address", recipient="advertisers"), VOCAB)
    assert d.verdict == "conditional" and d.statuses[0].needed[0]["var"] == "scenario.purpose is marketing"


def test_conflict_and_specific_precedence():
    share = Rule("a", "ALLOW", "share", "email address", recipient="partners")
    no_share = Rule("d", "DENY", "share", "email address", recipient="partners", guard=neg(b("user.consented")))
    sc = Scenario("share", "email address", recipient="partners", facts=[neg(b("user.consented"))])
    assert decide([share, no_share], sc, precedence="none").verdict == "conflict"
    assert decide([share, no_share], sc).verdict == "prohibited"


ACTIONS = Vocabulary(parents={"sell": ["share"], "rent": ["sell"], "email address": ["personal information"]})


def test_permission_and_prohibition_inherit_down_the_action_hierarchy():
    share = Rule("a", "ALLOW", "share", "personal information", recipient="partners")
    no_share = Rule("d", "DENY", "share", "personal information", recipient="partners")
    rent = Scenario("rent", "email address", recipient="partners")
    d = decide([share], rent, ACTIONS)
    assert (d.verdict, d.basis) == ("permitted", "general statement")
    d = decide([share], Scenario("share", "email address", recipient="partners"), ACTIONS)
    assert (d.verdict, d.basis) == ("permitted", "direct")
    assert decide([no_share], rent, ACTIONS).verdict == "prohibited"


def test_share_but_never_sell():
    share = Rule("a", "ALLOW", "share", "personal information", recipient="partners")
    no_sell = Rule("d", "DENY", "sell", "personal information")
    sell = Scenario("sell", "email address", recipient="partners")
    d = decide([share, no_sell], sell, ACTIONS)
    assert (d.verdict, d.resolution) == ("prohibited", "prohibition over a permission of incomparable scope")
    assert decide([share, no_sell], sell, ACTIONS, precedence="none").verdict == "conflict"
    no_share = Rule("x", "DENY", "share", "personal information", recipient="partners")
    assert decide([share, no_share], Scenario("share", "email address", recipient="partners"), ACTIONS).verdict == "conflict"
    d = decide([share, no_sell], Scenario("share", "email address", recipient="partners"), ACTIONS)
    assert d.verdict == "conditional" and d.statuses[1].needed[0]["var"] == "scenario.action is sell"


def test_unmentioned_events_count_as_absent_but_attributes_stay_unknown():
    unless_law = Rule("d", "DENY", "share", "email address", guard=neg(b("law.required")))
    assert decide([unless_law], Scenario("share", "email address")).verdict == "prohibited"
    assert decide([unless_law], Scenario("share", "email address", facts=[b("law.required")])).verdict == "not_addressed"
    kids = Rule("k", "DENY", "collect", "email address", guard=age("<", 13))
    assert decide([kids], Scenario("collect", "email address")).verdict == "conditional"


def test_opt_out_axiom_decides_a_pair():
    assert pair_outcome(b("opt_in.newsletter"), b("opt_out.newsletter"))["outcome"] == "mutually_exclusive"
    assert pair_outcome(b("opt_in.newsletter"), b("opt_out.cookies"))["outcome"] == "overlap_candidate"
    assert pair_outcome(b("opt_in.newsletter"), neg(b("consent.newsletter")))["outcome"] == "mutually_exclusive"
    assert pair_outcome(age("<", 13), age(">=", 18))["outcome"] == "mutually_exclusive"
    assert pair_outcome(age("<", 18), age("<", 13))["outcome"] == "overlap_candidate"


def test_residuals_decide_only_when_meaning_does_not_matter():
    law = {"op": "residual", "id": "law", "text": "as permitted by applicable law"}
    assert pair_outcome(conj(b("user.consented"), law), neg(b("user.consented")))["outcome"] == "mutually_exclusive"
    assert pair_outcome({"op": "or", "args": [b("user.consented"), law]}, b("user.consented"))["outcome"] == "overlap_candidate"
    out = pair_outcome(law, neg(b("user.consented")))
    assert out["outcome"] == "unresolved" and out["blocking"] == [law]
    assert pair_outcome(eq("user.jurisdiction", "California"), eq("user.jurisdiction", "Texas"))["outcome"] == "mutually_exclusive"


def test_a_residual_with_both_polarities_in_one_guard():
    law = {"op": "residual", "id": "law", "text": "as permitted by applicable law"}
    either = lambda *gs: {"op": "or", "args": list(gs)}
    assert pair_outcome(either(law, neg(law)), TRUE)["outcome"] == "overlap_candidate"
    split = either(conj(law, b("user.consented")), conj(neg(law), b("user.consented")))
    assert pair_outcome(split, b("user.consented"))["outcome"] == "overlap_candidate"
    assert pair_outcome(split, neg(b("user.consented")))["outcome"] == "mutually_exclusive"
    assert pair_outcome(either(law, b("user.consented")), either(neg(law), neg(b("user.consented"))))["outcome"] == "unresolved"
    assert pair_outcome(law, neg(law))["outcome"] == "mutually_exclusive"
