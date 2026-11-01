from __future__ import annotations

import re
from typing import List

QUALIFIERS = ("conditions", "exceptions", "purpose", "references")
FIELDS = ("data", "recipient", "source", "actor")


def _name(r: dict, k: str) -> set:
    v = r.get(k) or {}
    text = " ".join(str(v.get(x) or "") for x in ("name", "text")) if isinstance(v, dict) else str(v)
    return set(re.findall(r"[^\W_]+", text.lower()))


def _similar(a: set, b: set, empty_matches: bool = False) -> bool:
    if not a and not b:
        return True
    if not a or not b:
        return empty_matches
    return len(a & b) / len(a | b) >= 0.5 or a <= b or b <= a


def _same_practice(a: dict, b: dict, lenient: bool = False) -> bool:
    return a.get("operation") == b.get("operation") and _similar(_name(a, "data"), _name(b, "data")) and \
        all(_similar(_name(a, k), _name(b, k), lenient) for k in FIELDS if k != "data")


def _text(x) -> str:
    return x.get("text", "") if isinstance(x, dict) else str(x)


def merge_samples(samples: List[List[dict]], min_votes: int = 1, lenient: bool = False, qualifier_votes: int = 1) -> List[dict]:
    groups = []
    for i, rules in enumerate(samples):
        for r in rules:
            g = next((g for g in groups if g["rules"][0][1].get("polarity") == r.get("polarity")
                      and _same_practice(g["rules"][0][1], r, lenient) and i not in g["votes"]), None)
            if g is None:
                groups.append({"rules": [(i, r)], "votes": {i}})
            else:
                g["rules"].append((i, r))
                g["votes"].add(i)
    kept = [g for g in groups if len(g["votes"]) >= min_votes]
    out = []
    for g in kept:
        opposite = [h for h in kept if h is not g and h["rules"][0][1].get("polarity") != g["rules"][0][1].get("polarity")
                    and _same_practice(h["rules"][0][1], g["rules"][0][1], lenient)]
        if any(len(h["votes"]) > len(g["votes"]) for h in opposite):
            continue
        first = min(g["rules"], key=lambda x: x[0])[1]
        rule = dict(first)
        for k in QUALIFIERS:
            support = {}
            for i, r in g["rules"]:
                for q in r.get(k) or []:
                    support.setdefault(_text(q), [q, set()])[1].add(i)
            own = {_text(q) for q in first.get(k) or []}
            rule[k] = list(first.get(k) or []) + [q for t, (q, votes) in support.items()
                                                   if t not in own and len(votes) >= qualifier_votes]
        rule["samples"] = len(g["votes"])
        out.append(rule)
    return out
