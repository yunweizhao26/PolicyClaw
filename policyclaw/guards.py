from __future__ import annotations

import itertools
import json
from typing import Dict, Iterable, List

import z3

TRUE = {"op": "true"}
FALSE = {"op": "false"}
_CMP = {"<", "<=", ">", ">=", "==", "!="}


class GuardError(ValueError):
    pass


def key(g: dict) -> str:
    return json.dumps(g, sort_keys=True)


def is_atom(g: dict) -> bool:
    return g["op"] in ("bool", "cmp", "eq", "residual")


def validate(g: dict) -> None:
    op = g.get("op")
    if op in ("true", "false"):
        return
    if op in ("and", "or"):
        if not isinstance(g.get("args"), list):
            raise GuardError(f"{op} needs a list of args: {g}")
        for a in g["args"]:
            validate(a)
    elif op == "not":
        validate(g["arg"])
    elif op == "bool":
        _need(g, "var")
    elif op == "cmp":
        _need(g, "var", "cmp", "value")
        if g["cmp"] not in _CMP or not isinstance(g["value"], int) or isinstance(g["value"], bool):
            raise GuardError(f"bad comparison: {g}")
    elif op == "eq":
        _need(g, "var", "value")
        if not isinstance(g["value"], str):
            raise GuardError(f"categorical value must be a string: {g}")
    elif op == "residual":
        _need(g, "id")
    else:
        raise GuardError(f"unknown op: {g}")


def _need(g: dict, *fields: str) -> None:
    for f in fields:
        if f not in g:
            raise GuardError(f"missing {f}: {g}")


def atoms(g: dict) -> List[dict]:
    out: Dict[str, dict] = {}

    def walk(h: dict) -> None:
        if is_atom(h):
            out.setdefault(key(h), h)
        elif h["op"] in ("and", "or"):
            for a in h["args"]:
                walk(a)
        elif h["op"] == "not":
            walk(h["arg"])

    walk(g)
    return list(out.values())


class Signature:

    def __init__(self, guards: Iterable[dict] = ()):
        self.types: Dict[str, str] = {}
        for g in guards:
            self.add(g)

    def add(self, g: dict) -> None:
        validate(g)
        for a in atoms(g):
            if a["op"] == "residual":
                continue
            t = {"bool": "bool", "cmp": "int", "eq": "cat"}[a["op"]]
            prev = self.types.setdefault(a["var"], t)
            if prev != t:
                raise GuardError(f"variable {a['var']} used as {prev} and {t}")

    def z3var(self, name: str):
        t = self.types[name]
        if t == "bool":
            return z3.Bool(name)
        if t == "int":
            return z3.Int(name)
        return z3.String(name)


def to_z3(g: dict, sig: Signature):
    op = g["op"]
    if op == "true":
        return z3.BoolVal(True)
    if op == "false":
        return z3.BoolVal(False)
    if op == "and":
        return z3.And([to_z3(a, sig) for a in g["args"]]) if g["args"] else z3.BoolVal(True)
    if op == "or":
        return z3.Or([to_z3(a, sig) for a in g["args"]]) if g["args"] else z3.BoolVal(False)
    if op == "not":
        return z3.Not(to_z3(g["arg"], sig))
    if op == "bool":
        return sig.z3var(g["var"])
    if op == "cmp":
        v, c = sig.z3var(g["var"]), g["value"]
        return {"<": v < c, "<=": v <= c, ">": v > c, ">=": v >= c, "==": v == c, "!=": v != c}[g["cmp"]]
    if op == "eq":
        from .schema import SCHEMA
        if SCHEMA.value_set(g["var"]):
            return z3.Bool(f"{g['var']} = {SCHEMA.canonical_value(g['var'], g['value']) or g['value']}")
        return sig.z3var(g["var"]) == z3.StringVal(g["value"])
    if op == "residual":
        return z3.Bool(f"residual:{g['id']}")
    raise GuardError(f"unknown op: {g}")


def nnf(g: dict, neg: bool = False) -> dict:
    op = g["op"]
    if op == "true":
        return FALSE if neg else TRUE
    if op == "false":
        return TRUE if neg else FALSE
    if op == "not":
        return nnf(g["arg"], not neg)
    if op in ("and", "or"):
        flip = {"and": "or", "or": "and"}[op] if neg else op
        return {"op": flip, "args": [nnf(a, neg) for a in g["args"]]}
    return {"op": "not", "arg": g} if neg else g


def drop_residual_literals(g: dict) -> dict:
    op = g["op"]
    if op == "residual" or (op == "not" and g["arg"]["op"] == "residual"):
        return FALSE
    if op in ("and", "or"):
        return {"op": op, "args": [drop_residual_literals(a) for a in g["args"]]}
    return g


def residuals(g: dict) -> List[dict]:
    return [a for a in atoms(g) if a["op"] == "residual"]


def set_residuals(g: dict, values: Dict[str, bool]) -> dict:
    op = g["op"]
    if op == "residual":
        return dict(TRUE if values[g["id"]] else FALSE) if g["id"] in values else g
    if op in ("and", "or"):
        return {"op": op, "args": [set_residuals(a, values) for a in g["args"]]}
    if op == "not":
        return {"op": "not", "arg": set_residuals(g["arg"], values)}
    return g


def binate_residuals(g: dict) -> List[str]:
    pos, neg = set(), set()

    def walk(h: dict) -> None:
        if h["op"] == "residual":
            pos.add(h["id"])
        elif h["op"] == "not" and h["arg"]["op"] == "residual":
            neg.add(h["arg"]["id"])
        elif h["op"] in ("and", "or"):
            for a in h["args"]:
                walk(a)

    walk(nnf(g))
    return sorted(pos & neg)


def certain_part(g: dict) -> dict:
    both = binate_residuals(g)
    parts = [drop_residual_literals(nnf(set_residuals(g, dict(zip(both, bits)))))
             for bits in itertools.product((False, True), repeat=len(both))]
    return parts[0] if len(parts) == 1 else {"op": "and", "args": parts}
