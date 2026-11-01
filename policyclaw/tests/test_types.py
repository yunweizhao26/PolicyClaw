from policyclaw.extract import typed
from policyclaw.guards import GuardError
from policyclaw.queries import Rule, Scenario, Vocabulary, decide
from policyclaw.schema import SCHEMA

TYPED = bool(SCHEMA.value_sets)


def raises(fn, text):
    try:
        fn()
    except GuardError as e:
        assert text in str(e), str(e)
        return
    raise AssertionError(f"no GuardError mentioning {text!r}")


def eq(var, value):
    return {"op": "eq", "var": var, "value": value}


def days(cmp, value):
    return {"op": "cmp", "var": "retention.days", "cmp": cmp, "value": value}


def test_aliases_become_canonical_values():
    if not TYPED:
        return
    assert typed(eq("user.jurisdiction", "US"))["value"] == "United States"
    assert typed(eq("user.jurisdiction", "EEA"))["value"] == "European Economic Area"


def test_unknown_value_names_the_closest_values():
    if TYPED:
        raises(lambda: typed(eq("user.jurisdiction", "Californa")), "California")


def test_integer_bounds():
    if TYPED:
        raises(lambda: typed({"op": "cmp", "var": "user.age", "cmp": "<", "value": 200}), "outside")


def test_units_follow_the_quote():
    if not TYPED:
        return
    assert typed(days("<=", 180), "for 6 months after the decision")
    assert typed(days("<", 2555), "no longer than 7 years")
    raises(lambda: typed(days("<=", 6), "for 6 months"), "unit")
    assert typed(days("<=", 6), "as long as necessary")


def answer(guard_value, fact_value):
    rule = Rule("r", "DENY", "disclosure", "personal information", guard=eq("user.jurisdiction", guard_value))
    sc = Scenario("disclosure", "personal information", facts=[eq("user.jurisdiction", fact_value)])
    return decide([rule], sc, Vocabulary()).verdict


def test_a_place_lies_within_its_ancestors():
    if not TYPED:
        return
    assert answer("European Economic Area", "Germany") == "prohibited"
    assert answer("United States", "California") == "prohibited"


def test_places_outside_each_other_exclude_each_other():
    if not TYPED:
        return
    assert answer("European Economic Area", "United States") == "not_addressed"
    assert answer("California", "Texas") == "not_addressed"


def test_a_broader_place_leaves_the_narrower_open():
    if not TYPED:
        return
    assert answer("California", "United States") == "conditional"


def test_a_prohibition_except_as_set_forth_yields_to_the_policys_permissions():
    from policyclaw.queries import pair_outcome
    if "policy.permits" not in SCHEMA.derived_variables():
        return
    permits = {"op": "bool", "var": "policy.permits"}
    consent = {"op": "bool", "var": "consent.sharing"}
    deny = Rule("d", "DENY", "disclosure", "personal information", guard={"op": "not", "arg": permits})
    allow = Rule("a", "ALLOW", "disclosure", "personal information", guard=consent)
    with_consent = Scenario("disclosure", "personal information", facts=[consent])
    without = Scenario("disclosure", "personal information", facts=[{"op": "not", "arg": consent}])
    assert decide([deny, allow], with_consent, Vocabulary()).verdict == "permitted"
    assert decide([deny, allow], without, Vocabulary()).verdict == "prohibited"
    assert pair_outcome(allow.guard, deny.guard)["outcome"] == "mutually_exclusive"
