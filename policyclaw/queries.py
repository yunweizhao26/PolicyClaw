from __future__ import annotations

import functools, threading
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set

import z3

_Z3_LOCK = threading.Lock()


def _serialized(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with _Z3_LOCK:
            return fn(*args, **kwargs)
    return wrapper

from .guards import TRUE, Signature, atoms, certain_part, key, residuals, to_z3
from .schema import SCHEMA

SLOTS = ("actor", "action", "data", "recipient", "source", "purpose")


@dataclass
class Rule:
    id: str
    polarity: str
    action: str
    data: str
    actor: str = ""
    recipient: str = ""
    source: str = ""
    purpose: str = ""
    guard: dict = field(default_factory=lambda: dict(TRUE))
    evidence: tuple = ()


@dataclass
class Scenario:
    action: str
    data: str
    actor: str = ""
    recipient: str = ""
    source: str = ""
    purpose: str = ""
    facts: List[dict] = field(default_factory=list)


def _norm(s: str) -> str:
    return " ".join((s or "").replace("_", " ").lower().split())


class Vocabulary:

    def __init__(self, aliases: Optional[Dict[str, str]] = None,
                 parents: Optional[Dict[str, Iterable[str]]] = None):
        self.aliases = {_norm(k): _norm(v) for k, v in (aliases or {}).items()}
        self.parents: Dict[str, Set[str]] = {}
        for child, ps in (parents or {}).items():
            self.parents.setdefault(self.canon(child), set()).update(self.canon(p) for p in ps)

    def canon(self, s: str) -> str:
        n = _norm(s)
        return self.aliases.get(n, n)

    def covers(self, general: str, specific: str) -> bool:
        g, s = self.canon(general), self.canon(specific)
        if not g:
            return True
        if not s:
            return False
        seen, stack = set(), [s]
        while stack:
            x = stack.pop()
            if x == g:
                return True
            if x not in seen:
                seen.add(x)
                stack.extend(self.parents.get(x, ()))
        return False


def slot_atom(slot: str, value: str) -> dict:
    return {"op": "bool", "var": f"scenario.{slot} is {value}"}


def effective_guard(rule: Rule, sc: Scenario, vocab: Vocabulary) -> Optional[dict]:
    extra = []
    for slot in SLOTS:
        r, s = getattr(rule, slot), getattr(sc, slot)
        if vocab.covers(r, s):
            continue
        if not vocab.canon(s) or vocab.covers(s, r):
            extra.append(slot_atom(slot, vocab.canon(r)))
        else:
            return None
    return {"op": "and", "args": extra + [rule.guard]} if extra else rule.guard


class _Solver:
    def __init__(self, guards: Iterable[dict], facts: Iterable[dict] = ()):
        self.facts = list(facts)
        guards = list(guards)
        names = Signature(self.facts + guards).types
        values = {(a["var"], SCHEMA.canonical_value(a["var"], a["value"]) or a["value"])
                  for g in self.facts + guards for a in atoms(g) if a["op"] == "eq"}
        axioms = SCHEMA.axioms(names) + SCHEMA.value_axioms(values)
        self.sig = Signature(axioms + self.facts + guards)
        self.axioms = [to_z3(g, self.sig) for g in axioms]
        self.base = self.axioms + [to_z3(g, self.sig) for g in self.facts]

    def sat(self, *extra, with_facts: bool = True) -> bool:
        s = z3.Solver()
        s.add(*(self.base if with_facts else self.axioms), *extra)
        r = s.check()
        if r == z3.unknown:
            raise RuntimeError("solver returned unknown")
        return r == z3.sat

    def z(self, g: dict):
        return to_z3(g, self.sig)


@dataclass
class RuleStatus:
    rule: Rule
    status: str
    needed: List[dict] = field(default_factory=list)


@dataclass
class Decision:
    verdict: str
    statuses: List[RuleStatus]
    basis: str = ""
    resolution: str = ""
    clashes: List[dict] = field(default_factory=list)

    def ids(self, status: str, polarity: str) -> List[str]:
        return [s.rule.id for s in self.statuses if s.status == status and s.rule.polarity == polarity]


def rule_status(sv: _Solver, rule: Rule, guard: dict) -> RuleStatus:
    phi = sv.z(guard)
    if not sv.sat(z3.Not(phi)):
        return RuleStatus(rule, "applies")
    if not sv.sat(phi):
        return RuleStatus(rule, "excluded")
    needed = [a for a in atoms(guard) if sv.sat(sv.z(a)) and sv.sat(z3.Not(sv.z(a)))]
    return RuleStatus(rule, "open", needed)


def _same_scope(sv: _Solver, vocab: Vocabulary, a: Rule, b: Rule) -> bool:
    if not all(vocab.covers(getattr(a, s), getattr(b, s)) and vocab.covers(getattr(b, s), getattr(a, s)) for s in SLOTS):
        return False
    return not sv.sat(sv.z(a.guard), z3.Not(sv.z(b.guard)), with_facts=False) and \
        not sv.sat(sv.z(b.guard), z3.Not(sv.z(a.guard)), with_facts=False)


def _more_specific(sv: _Solver, vocab: Vocabulary, a: Rule, b: Rule) -> bool:
    if not all(vocab.covers(getattr(b, s), getattr(a, s)) for s in SLOTS):
        return False
    guard_entails = not sv.sat(sv.z(a.guard), z3.Not(sv.z(b.guard)), with_facts=False)
    if not guard_entails:
        return False
    flow_equal = all(vocab.covers(getattr(a, s), getattr(b, s)) for s in SLOTS)
    guard_equal = not sv.sat(sv.z(b.guard), z3.Not(sv.z(a.guard)), with_facts=False)
    return not (flow_equal and guard_equal)


def _clash_record(sv: _Solver, vocab: Vocabulary, allow: Rule, deny: Rule) -> dict:
    def narrower(a: Rule, b: Rule) -> List[str]:
        fields = [s for s in SLOTS if vocab.covers(getattr(b, s), getattr(a, s)) and not vocab.covers(getattr(a, s), getattr(b, s))]
        a_g, b_g = sv.z(a.guard), sv.z(b.guard)
        if not sv.sat(a_g, z3.Not(b_g), with_facts=False) and sv.sat(b_g, z3.Not(a_g), with_facts=False):
            fields.append("guard")
        return fields

    if _same_scope(sv, vocab, allow, deny):
        relation = "same scope"
    elif _more_specific(sv, vocab, allow, deny):
        relation = "permission more specific"
    elif _more_specific(sv, vocab, deny, allow):
        relation = "prohibition more specific"
    else:
        relation = "incomparable"
    rule = lambda r: {"id": r.id, **{s: getattr(r, s) for s in SLOTS}, "guard": r.guard,
                      "evidence": list(r.evidence[:2]) if r.evidence else []}
    return {"relation": relation, "contradiction": relation in ("same scope", "permission more specific"),
            "permission_narrower_in": narrower(allow, deny),
            "prohibition_narrower_in": narrower(deny, allow), "permission": rule(allow), "prohibition": rule(deny)}


def closed_world_facts(guards: Iterable[dict], facts: List[dict]) -> List[dict]:
    stated = {a["var"] for f in facts for a in atoms(f) if "var" in a}
    used = {a["var"] for g in guards for a in atoms(g) if a["op"] == "bool"}
    return [{"op": "not", "arg": {"op": "bool", "var": v}} for v in sorted(used - stated) if SCHEMA.closed_world(v)]


@_serialized
def decide(rules: Iterable[Rule], sc: Scenario, vocab: Optional[Vocabulary] = None,
           precedence: str = "specific", closed_world: bool = True) -> Decision:
    vocab = vocab or Vocabulary()
    relevant = [(r, g) for r in rules if (g := effective_guard(r, sc, vocab)) is not None]
    direct = lambda r: vocab.canon(r.action) == vocab.canon(sc.action) or not vocab.canon(sc.action)
    return _decide(relevant, sc.facts, vocab, precedence, closed_world, direct)


@_serialized
def decide_relevant(relevant: List[tuple], facts: List[dict], precedence: str = "specific",
                    vocab: Optional[Vocabulary] = None, direct_ids: Optional[Set[str]] = None) -> Decision:
    direct = (lambda r: r.id in direct_ids) if direct_ids is not None else None
    return _decide(relevant, facts, vocab or Vocabulary(), precedence, False, direct)


def derived_facts(guards: Iterable[dict], permissions: Iterable[dict]) -> List[dict]:
    out = []
    for v in SCHEMA.derived_variables():
        if not any(a.get("var") == v for g in guards for a in atoms(g)):
            continue
        p = {"op": "bool", "var": v}
        grants = [g for g in permissions if not any(a.get("var") == v for a in atoms(g))]
        out.append({"op": "or", "args": [{"op": "not", "arg": p}] + grants})
        out += [{"op": "or", "args": [{"op": "not", "arg": g}, p]} for g in grants]
    return out


def _decide(relevant, facts, vocab, precedence, closed_world, is_direct=None) -> Decision:
    guards = [g for _, g in relevant] + [r.guard for r, _ in relevant]
    derived = derived_facts(guards, [g for r, g in relevant if r.polarity == "ALLOW"])
    sv = _Solver(guards, list(facts) + derived + (closed_world_facts(guards, facts) if closed_world else []))
    if not sv.sat():
        raise ValueError("scenario facts are inconsistent with the background theory")
    statuses = [rule_status(sv, r, g) for r, g in relevant]
    if not statuses:
        return Decision("not_addressed", statuses)

    applying = [s for s in statuses if s.status == "applies"]
    resolution = ""
    pairs = [(a.rule, d.rule) for a in applying if a.rule.polarity == "ALLOW" for d in applying if d.rule.polarity == "DENY"]
    clashes = [_clash_record(sv, vocab, a, d) for a, d in pairs]
    if precedence == "specific":
        kept = [s for s in applying
                if not any(t.rule.polarity != s.rule.polarity and _more_specific(sv, vocab, t.rule, s.rule) for t in applying)]
        if len(kept) < len(applying):
            resolution = "more specific rule"
        denies = [s for s in kept if s.rule.polarity == "DENY"]
        final = [s for s in kept if s.rule.polarity == "DENY" or not denies
                 or any(_same_scope(sv, vocab, s.rule, d.rule) for d in denies)]
        if len(final) < len(kept):
            resolution = "prohibition over a permission of incomparable scope"
        applying = final
    live = applying + [s for s in statuses if s.status == "open"]
    allow_applies = any(s.rule.polarity == "ALLOW" for s in applying)
    deny_applies = any(s.rule.polarity == "DENY" for s in applying)
    allow_live = any(s.rule.polarity == "ALLOW" for s in live)
    deny_live = any(s.rule.polarity == "DENY" for s in live)

    if allow_applies and deny_applies:
        verdict = "conflict"
    elif allow_applies and not deny_live:
        verdict = "permitted"
    elif deny_applies and not allow_live:
        verdict = "prohibited"
    elif live:
        verdict = "conditional"
    else:
        verdict = "not_addressed"
    basis = ""
    if verdict == "permitted" and is_direct is not None:
        allowing = [s.rule for s in applying if s.rule.polarity == "ALLOW"]
        basis = "direct" if any(is_direct(r) for r in allowing) else "general statement"
    survivors = {id(s.rule) for s in applying}
    for c, (a, d) in zip(clashes, pairs):
        c["verdict"] = verdict
        if id(a) in survivors and id(d) in survivors:
            c["resolution"] = "kept as conflict"
        elif id(d) in survivors:
            c["resolution"] = "more specific rule" if c["relation"] == "prohibition more specific" \
                else "prohibition over a permission of incomparable scope"
        elif id(a) in survivors:
            c["resolution"] = "more specific rule"
        else:
            c["resolution"] = "both overridden by other rules"
    return Decision(verdict, statuses, basis, resolution if verdict in ("permitted", "prohibited") else "", clashes)


@_serialized
def pair_outcome(phi_plus: dict, phi_minus: dict) -> dict:
    sv = _Solver([phi_plus, phi_minus], derived_facts([phi_minus], [phi_plus]))
    if not sv.sat(sv.z(phi_plus), sv.z(phi_minus)):
        return {"outcome": "mutually_exclusive", "blocking": []}
    if sv.sat(*[sv.z(certain_part(g)) for g in (phi_plus, phi_minus)]):
        return {"outcome": "overlap_candidate", "blocking": []}
    blocking = {key(a): a for g in (phi_plus, phi_minus) for a in residuals(g)}
    return {"outcome": "unresolved", "blocking": list(blocking.values())}


@_serialized
def without_effect(conjuncts: List[dict]) -> List[int]:
    sv = _Solver(conjuncts)
    zs = [sv.z(c) for c in conjuncts]
    return [i for i, c in enumerate(conjuncts) if c.get("op") != "true"
            and not sv.sat(*(zs[:i] + zs[i + 1:]), z3.Not(zs[i]), with_facts=False)]


@_serialized
def satisfiable(guard: dict) -> bool:
    sv = _Solver([guard])
    return sv.sat(sv.z(guard), with_facts=False)
