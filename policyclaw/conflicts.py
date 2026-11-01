from __future__ import annotations

from typing import Dict, Iterable, List

from .actions import ActionNetwork
from .guards import atoms
from .queries import SLOTS, Rule, Vocabulary, _more_specific, _same_scope, _Solver, _serialized, pair_outcome, satisfiable
from .schema import SCHEMA


def vocabulary(rules: Iterable[Rule], relations: Dict[str, dict] = None, network: ActionNetwork = None) -> Vocabulary:
    parents, aliases = {}, {}
    for rel in (relations or {}).values():
        for k, v in rel.get("parents", {}).items():
            parents.setdefault(k, []).extend(v)
        aliases.update(rel.get("aliases", {}))
    return (network or ActionNetwork()).vocabulary(sorted({r.action for r in rules}), parents, aliases)


def overlap(vocab: Vocabulary, a: Rule, b: Rule) -> bool:
    return all(vocab.covers(getattr(a, s), getattr(b, s)) or vocab.covers(getattr(b, s), getattr(a, s)) for s in SLOTS)


@_serialized
def relation(vocab: Vocabulary, allow: Rule, deny: Rule) -> str:
    sv = _Solver([allow.guard, deny.guard])
    if _same_scope(sv, vocab, allow, deny):
        return "same scope"
    if _more_specific(sv, vocab, allow, deny):
        return "permission inside prohibition"
    if _more_specific(sv, vocab, deny, allow):
        return "prohibition inside permission"
    return "incomparable"


def find_conflicts(rules: List[Rule], vocab: Vocabulary) -> List[dict]:
    derived = set(SCHEMA.derived_variables())
    out = []
    for a in (r for r in rules if r.polarity == "ALLOW"):
        for d in (r for r in rules if r.polarity == "DENY"):
            if not overlap(vocab, a, d):
                continue
            outcome = pair_outcome(a.guard, d.guard)["outcome"]
            if outcome == "mutually_exclusive":
                rel = "policy exception" if any(x.get("var") in derived for x in atoms(d.guard)) else "exclusive guards"
            else:
                rel = relation(vocab, a, d)
            out.append({"allow": a.id, "deny": d.id, "outcome": outcome, "relation": rel,
                        "contradiction": rel in ("same scope", "permission inside prohibition") and satisfiable(a.guard)})
    return out
