from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import replace
from typing import Dict, List, Optional

from .actions import ActionNetwork
from .extract import load_prompt, typed
from .guards import GuardError, atoms, validate
from .llm import LLM
from .queries import SLOTS, Decision, Rule, Scenario, Vocabulary, decide, decide_relevant
from .schema import SCHEMA

ANSWERS = ("permitted", "prohibited", "conditional", "conflict", "not_addressed")

TRANSLATE_SCENARIO = load_prompt("translate_scenario.txt")

DIRECT = load_prompt("direct.txt")

GENERATE = load_prompt("generate.txt")

JUDGE = load_prompt("judge.txt")


def policy_vocabulary(rules: List[Rule]) -> Dict[str, object]:
    terms = {s: sorted({getattr(r, s) for r in rules if getattr(r, s)}) for s in SLOTS}
    examples = defaultdict(set)
    for r in rules:
        raw = json.loads(r.evidence[2]) if len(r.evidence) > 2 else {}
        quotes = (raw.get("conditions") or []) + (raw.get("exceptions") or [])
        for a in atoms(r.guard):
            if "var" in a:
                examples[a["var"]].update(q for q in quotes[:2])
    return {"terms": terms, "variables": {v: sorted(q)[:3] for v, q in examples.items()}}


def _valid_facts(items) -> tuple:
    facts, dropped = [], []
    for f in items or []:
        try:
            validate(f)
            facts.append(typed(f))
        except (GuardError, TypeError, KeyError, AttributeError):
            dropped.append(f)
    return facts, dropped


def translate_scenario(llm: LLM, text: str, rules: List[Rule], network=None) -> tuple:
    voc = policy_vocabulary(rules)
    out = llm.json(TRANSLATE_SCENARIO.format(
        vocab=json.dumps(voc["terms"], ensure_ascii=False, indent=1),
        variables=json.dumps(voc["variables"], ensure_ascii=False, indent=1), scenario=text,
        operations=SCHEMA.operations_prompt(), standard=SCHEMA.variables_prompt()))
    flow = out.get("flow") if isinstance(out.get("flow"), dict) else {}
    verb, op = str(flow.get("verb") or "").strip().lower(), str(flow.get("operation") or "").strip().lower()
    action = (f"{verb}@{op}" if verb else op) if SCHEMA.is_operation(op) else ""
    covers = out.get("covers") if isinstance(out.get("covers"), dict) else {}
    covers = {s: [str(x) for x in (v if isinstance(v, list) else [v]) if x] for s, v in covers.items()}
    facts, dropped = _valid_facts(out.get("facts"))
    sc = Scenario(action=action, **{s: str(flow.get(s, "") or "") for s in SLOTS if s != "action"}, facts=facts)
    parents = {getattr(sc, s): covers.get(s) or [] for s in SLOTS if getattr(sc, s)}
    vocab = (network or ActionNetwork()).vocabulary([r.action for r in rules] + [sc.action], parents)
    return sc, vocab, {"raw": out, "dropped_facts": dropped}


def _result(d: Decision, extra: dict) -> dict:
    return {"answer": d.verdict, "basis": d.basis, "resolution": d.resolution, "clashes": d.clashes,
            "applies": [s.rule.id for s in d.statuses if s.status == "applies"],
            "open": [s.rule.id for s in d.statuses if s.status == "open"],
            "evidence": sorted({json.loads(s.rule.evidence[2]).get("polarity_text", "")
                                for s in d.statuses if s.status in ("applies", "open") and len(s.rule.evidence) > 2}),
            **extra}


def answer_policyclaw(llm: LLM, text: str, rules: List[Rule], network=None, precedence: str = "specific") -> dict:
    sc, vocab, info = translate_scenario(llm, text, rules, network)
    try:
        d: Decision = decide(rules, sc, vocab, precedence=precedence)
    except (ValueError, GuardError) as e:
        return {"answer": "error", "error": str(e), "scenario": sc.__dict__, **info}
    needed = sorted({json.dumps(a, sort_keys=True) for s in d.statuses for a in s.needed})
    return _result(d, {"scenario": sc.__dict__, "missing_facts": [json.loads(a) for a in needed], **info})


def _render(g: dict, ids: Dict[str, str]) -> str:
    op = g["op"]
    if op in ("true", "false"):
        return op
    if op in ("and", "or"):
        parts = [_render(a, ids) for a in g["args"]]
        return "true" if not parts else parts[0] if len(parts) == 1 else "(" + f" {op} ".join(parts) + ")"
    if op == "not":
        return f"not {_render(g['arg'], ids)}"
    return ids[json.dumps(g, sort_keys=True)]


def _describe(a: dict) -> str:
    if a["op"] == "cmp":
        return f"{a['var']} {a['cmp']} {a['value']}"
    if a["op"] == "eq":
        return f"{a['var']} is {a['value']}"
    if a["op"] == "residual":
        return f"\"{a.get('text', '')}\""
    return a["var"]


def _eq_as_bool(g: dict) -> dict:
    op = g["op"]
    if op in ("and", "or"):
        return {"op": op, "args": [_eq_as_bool(a) for a in g["args"]]}
    if op == "not":
        return {"op": "not", "arg": _eq_as_bool(g["arg"])}
    if op == "eq":
        return {"op": "bool", "var": f"{g['var']} is {g['value']}"}
    return g


def answer_policyclaw_judged(llm: LLM, text: str, rules: List[Rule], network=None, precedence: str = "specific") -> dict:
    rules = [replace(r, guard=_eq_as_bool(r.guard)) for r in rules]
    ids, lines, conds = {}, [], []
    for r in rules:
        for a in atoms(r.guard):
            k = json.dumps(a, sort_keys=True)
            if k not in ids:
                ids[k] = f"c{len(ids) + 1}"
                conds.append(f"{ids[k]}: {_describe(a)}")
    short = {f"r{i + 1}": r for i, r in enumerate(rules)}
    for sid, r in short.items():
        lines.append(f"{sid}: {r.polarity} {r.action} data=\"{r.data}\" recipient=\"{r.recipient or '-'}\" source=\"{r.source or '-'}\" "
                     f"purpose=\"{r.purpose or '-'}\" if {_render(r.guard, ids)}")
    ints = SCHEMA.int_variables()
    out = llm.json(JUDGE.format(rules="\n".join(lines), conditions="\n".join(conds) or "(none)", scenario=text,
                                closed_world=SCHEMA.closed_world_note, int_variables=", ".join(ints) or "(none)"),
                   max_tokens=8192)
    rel = out.get("rules") if isinstance(out.get("rules"), dict) else {}
    vals = out.get("conditions") if isinstance(out.get("conditions"), dict) else {}
    by_id = {v: json.loads(k) for k, v in ids.items()}
    facts = [a if vals.get(c) is True else {"op": "not", "arg": a}
             for c, a in by_id.items() if isinstance(vals.get(c), bool)]
    values = out.get("values") if isinstance(out.get("values"), dict) else {}
    facts += [{"op": "cmp", "var": v, "cmp": "==", "value": values[v]} for v in ints
              if isinstance(values.get(v), int) and not isinstance(values.get(v), bool)]
    relevant = []
    for sid, r in short.items():
        if rel.get(sid) in ("states", "covers"):
            relevant.append((r, r.guard))
        elif rel.get(sid) == "broader":
            relevant.append((r, {"op": "and", "args": [{"op": "bool", "var": f"scenario.within {sid}"}, r.guard]}))
    direct_ids = {r.id for sid, r in short.items() if rel.get(sid) == "states"}
    vocab = (network or ActionNetwork()).vocabulary([r.action for r in rules])
    try:
        d = decide_relevant(relevant, facts, precedence=precedence, vocab=vocab, direct_ids=direct_ids)
    except (ValueError, GuardError) as e:
        return {"answer": "error", "error": str(e), "judgments": out}
    return _result(d, {"judgments": out, "missing_facts": sorted({_describe(a) for s in d.statuses for a in s.needed})})


NORMALIZE = load_prompt("normalize.txt")


def normalize_scenario(llm: LLM, text: str, rules: List[Rule], network=None) -> tuple:
    by_op = defaultdict(set)
    for r in rules:
        op = r.action.rsplit("@", 1)[-1]
        by_op[op].add(r.action)
    actions = "\n".join(f"- {op}: {', '.join(sorted(a))}" for op, a in sorted(by_op.items()))
    used = sorted({a["var"] for r in rules for a in atoms(r.guard) if "var" in a} | set(SCHEMA.int_variables()))
    variables = "\n".join(f"- {v}: {(SCHEMA.variable(v) or {}).get('gloss', '')}" for v in used) or "(none)"
    terms = lambda slot: json.dumps(sorted({getattr(r, slot) for r in rules if getattr(r, slot)}), ensure_ascii=False)
    out = llm.json(NORMALIZE.format(actions=actions or "(none)", tree=SCHEMA.operations_prompt(), actors=terms("actor"), data=terms("data"),
                                    recipients=terms("recipient"), sources=terms("source"), purposes=terms("purpose"), variables=variables,
                                    scenario=text, closed_world=SCHEMA.closed_world_note))
    known = {r.action for r in rules} | set(SCHEMA.operations)
    action = str(out.get("action") or "")
    facts, dropped = _valid_facts([f for f in out.get("facts") or [] if isinstance(f, dict)])
    fields = {s: str(out.get(s) or "") for s in ("data", "recipient", "source", "purpose")}
    actor = str(out.get("actor") or "")
    sc = Scenario(action=action if action in known else "", actor=actor if actor in {r.actor for r in rules} else "", facts=facts, **fields)
    parents = {fields[s]: [str(x) for x in out.get(f"{s}_covered_by") or [] if x] for s in fields if fields[s]}
    vocab = (network or ActionNetwork()).vocabulary([r.action for r in rules] + [sc.action], parents)
    return sc, vocab, {"raw": out, "interpretation": out.get("interpretation", ""), "action_known": action in known,
                       "dropped_facts": dropped}


def answer_policyclaw_normalized(llm: LLM, text: str, rules: List[Rule], network=None, precedence: str = "specific") -> dict:
    sc, vocab, info = normalize_scenario(llm, text, rules, network)
    if not sc.action:
        return {"answer": "not_addressed", "basis": "", "resolution": "", "clashes": [], "applies": [], "open": [],
                "evidence": [], "scenario": sc.__dict__, "missing_facts": [], **info}
    try:
        d = decide(rules, sc, vocab, precedence=precedence)
    except (ValueError, GuardError) as e:
        return {"answer": "error", "error": str(e), "scenario": sc.__dict__, **info}
    needed = sorted({json.dumps(a, sort_keys=True) for s in d.statuses for a in s.needed})
    return _result(d, {"scenario": sc.__dict__, "missing_facts": [json.loads(a) for a in needed], **info})


def answer_direct(llm: LLM, policy: str, text: str) -> dict:
    out = llm.json(DIRECT.format(policy=policy, scenario=text), max_tokens=2048)
    if out.get("answer") not in ANSWERS:
        out["answer"] = "error"
    return out


def generate_scenarios(llm: LLM, policy: str, k: int = 10) -> List[dict]:
    out = llm.json(GENERATE.format(policy=policy, k=k), max_tokens=6000)
    return [s for s in out.get("scenarios", []) if isinstance(s, dict) and s.get("text")]
