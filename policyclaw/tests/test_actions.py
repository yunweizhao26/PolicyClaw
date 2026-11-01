import json, os, tempfile

from policyclaw.actions import ActionNetwork
from policyclaw.queries import Rule, Scenario, decide

NODES = [
    {"lemma": "share", "operation": "disclosure", "relation": "same"},
    {"lemma": "sell", "operation": "sale", "relation": "same"},
    {"lemma": "rent", "operation": "sale", "relation": "narrower"},
    {"lemma": "publish", "operation": "dissemination or otherwise making available", "relation": "narrower"},
    {"lemma": "provide", "operation": "disclosure by transmission", "relation": "same"},
    {"lemma": "provide", "operation": "collection", "relation": "narrower"},
    {"lemma": "monetize", "operation": "other", "relation": "narrower", "placed_under": "sale"},
]
PARENTS = {"email address": ["personal information"]}


def network():
    path = os.path.join(tempfile.mkdtemp(), "network.json")
    json.dump(NODES, open(path, "w"))
    return ActionNetwork(path)


def test_general_verb_covers_sale_and_publication():
    v = network().vocabulary(extra_parents=PARENTS)
    share = Rule("a", "ALLOW", "share@disclosure", "personal information")
    no_share = Rule("d", "DENY", "share@disclosure", "personal information")
    for verb in ("rent@sale", "publish@dissemination or otherwise making available", "sell@sale"):
        d = decide([share], Scenario(verb, "email address"), v)
        assert (d.verdict, d.basis) == ("permitted", "general statement")
        assert decide([no_share], Scenario(verb, "email address"), v).verdict == "prohibited"
    no_sell = Rule("s", "DENY", "sell@sale", "personal information")
    assert decide([no_sell], Scenario("publish@dissemination or otherwise making available", "email address"), v).verdict == "not_addressed"


def test_the_same_verb_differs_by_operation():
    v = network().vocabulary(extra_parents=PARENTS)
    assert v.covers("disclosure", "provide@disclosure by transmission")
    assert not v.covers("disclosure", "provide@collection")
    assert v.covers("processing", "provide@collection")


def test_uncovered_verb_can_be_placed_and_unplaced_verb_stays_narrow():
    v = network().vocabulary(["frobnicate@disclosure"], PARENTS)
    assert v.covers("sale", "monetize@other")
    frob = Rule("f", "ALLOW", "frobnicate@disclosure", "personal information")
    assert decide([frob], Scenario("rent@sale", "email address"), v).verdict == "not_addressed"
    assert v.covers("disclosure", "frobnicate@disclosure")


def test_clash_records_describe_the_resolution():
    v = network().vocabulary(extra_parents=PARENTS)
    share = Rule("a", "ALLOW", "share@disclosure", "personal information", recipient="partners")
    no_sell = Rule("d", "DENY", "sell@sale", "personal information")
    d = decide([share, no_sell], Scenario("rent@sale", "email address", recipient="partners"), v)
    assert d.verdict == "prohibited" and len(d.clashes) == 1
    c = d.clashes[0]
    assert c["relation"] == "incomparable"
    assert c["permission_narrower_in"] == ["recipient"] and c["prohibition_narrower_in"] == ["action"]
    assert c["resolution"] == "prohibition over a permission of incomparable scope"
