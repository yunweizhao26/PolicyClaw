from __future__ import annotations

import json
from typing import Dict, Iterable, List

from .extract import _slot, load_prompt
from .llm import LLM

RELATE = load_prompt("relate_terms.txt")


def relate_terms(llm: LLM, terms: Dict[str, List[str]], kind: str = "data") -> dict:
    names = sorted(terms)
    if len(names) < 2:
        return {"aliases": {}, "parents": {}}
    listing = "\n".join(f"- {t}: " + "; ".join(json.dumps(p, ensure_ascii=False) for p in terms[t][:2]) for t in names)
    out = llm.json(RELATE.format(kind=kind, terms=listing), max_tokens=8192)
    known = set(names)
    canon = {t: t for t in names}

    def find(t):
        while canon[t] != t:
            t = canon[t]
        return t
    for pair in out.get("same") or []:
        if isinstance(pair, list) and len(pair) == 2 and set(pair) <= known and pair[0] != pair[1]:
            a, b = find(pair[0]), find(pair[1])
            if a != b:
                canon[max(a, b)] = min(a, b)
    parents: Dict[str, set] = {}
    for pair in out.get("narrower") or []:
        if isinstance(pair, list) and len(pair) == 2 and set(pair) <= known:
            child, parent = find(pair[0]), find(pair[1])
            if child != parent:
                parents.setdefault(child, set()).add(parent)

    def reaches(a, b, seen=()):
        return a == b or any(reaches(p, b, seen + (a,)) for p in parents.get(a, ()) if p not in seen)
    for child in list(parents):
        for p in list(parents[child]):
            parents[child].discard(p)
            if not reaches(p, child):
                parents[child].add(p)
    return {"aliases": {t: find(t) for t in names if find(t) != t},
            "parents": {c: sorted(ps) for c, ps in parents.items() if ps}}


RELATED_SLOTS = ("data", "recipient", "source", "actor", "purpose")


def policy_terms(rows: Iterable[dict]) -> Dict[str, Dict[str, List[str]]]:
    out = {k: {} for k in RELATED_SLOTS}
    for r in rows:
        raw = r["raw"]
        pairs = [(k, _slot(raw, k)) for k in RELATED_SLOTS if k != "purpose"]
        pairs += [("purpose", (p.get("text", ""), p.get("name") or p.get("text", ""))) for p in raw.get("purpose") or []
                  if isinstance(p, dict)]
        for k, (text, name) in pairs:
            if name:
                phrases = out[k].setdefault(name, [])
                if text and text not in phrases:
                    phrases.append(text)
    return out


def relate_policy_terms(llm: LLM, rows: Iterable[dict]) -> Dict[str, dict]:
    return {k: relate_terms(llm, terms, k) for k, terms in policy_terms(rows).items()}
