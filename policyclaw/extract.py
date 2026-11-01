from __future__ import annotations

import bisect, hashlib, json, os, re
from dataclasses import replace
from typing import Dict, List, Optional, Tuple

from .guards import TRUE, GuardError, Signature, validate
from .llm import LLM
from .merge import merge_samples
from .queries import Rule, satisfiable, without_effect
from .schema import SCHEMA

DEFAULT_PROMPTS = os.path.join(os.path.dirname(__file__), "prompts")
PROMPTS = os.environ.get("POLICYCLAW_PROMPTS") or DEFAULT_PROMPTS


def load_prompt(name: str) -> str:
    path = os.path.join(PROMPTS, name)
    return open(path if os.path.exists(path) else os.path.join(DEFAULT_PROMPTS, name)).read()


_read = load_prompt
EXTRACT = _read("extract.txt")

EXTRACT_SINGLE = (EXTRACT.split("- purpose:")[0]
                  + "- conditions: list of verbatim quotes of everything in the section that limits the practice: when, "
                    "for whom, why, in which circumstances, except when, or how the user can stop it.\n\n"
                  + "Section:" + EXTRACT.split("\nSection:")[1])

TRANSLATE = _read("translate.txt")
REPAIR = _read("repair.txt")
COMPLETE = _read("complete.txt").replace("<<FIELDS>>", EXTRACT.split("Fields of a rule:\n")[1].split("\n\nSection:")[0])

OPERATION_FIELD = "{operations}" in EXTRACT
SLOTS = ("actor", "action", "data", "recipient", "source")
QUALIFIERS = ("conditions", "exceptions", "purpose", "references")
MIN_GAP = 4


def _words(s: str) -> str:
    return " " + " ".join(re.findall(r"[^\W_]+", (s or "").lower())) + " "


def _quoted(section: str, text: str) -> bool:
    hay, at = _words(section), 0
    for frag in re.split(r"\.\.\.|…", text or ""):
        w = _words(frag)
        if w.strip():
            at = hay.find(w, at)
            if at < 0:
                return False
            at += len(w) - 1
    return True


def typed(g: dict, quote: str = "") -> dict:
    op = g["op"]
    if op in ("and", "or"):
        return {**g, "args": [typed(a, quote) for a in g["args"]]}
    if op == "not":
        return {**g, "arg": typed(g["arg"], quote)}
    if op not in ("bool", "cmp", "eq"):
        return g
    var = g["var"]
    if not SCHEMA.admits(var, op):
        raise GuardError(f"variable {var} cannot be used with {op}")
    if op == "eq" and SCHEMA.value_set(var):
        value = SCHEMA.canonical_value(var, g["value"])
        if value is None:
            raise GuardError(f"{var} has no value {g['value']!r}; the closest values are {SCHEMA.close_values(var, g['value'])}")
        return {**g, "value": value}
    if op == "cmp":
        lo, hi = SCHEMA.bounds(var)
        if (lo is not None and g["value"] < lo) or (hi is not None and g["value"] > hi):
            raise GuardError(f"{var} = {g['value']} lies outside its range {lo} to {hi}")
        allowed = SCHEMA.unit_values(var, quote)
        if allowed is not None and g["value"] not in allowed:
            unit = (SCHEMA.variable(var) or {}).get("unit")
            raise GuardError(f"{var} is in {unit}, and {g['value']} does not match the number and unit of the quote")
    return g


def check_vars(g: dict) -> None:
    typed(g)


def _text(x) -> str:
    while isinstance(x, dict):
        x = x.get("text", "")
    return x if isinstance(x, str) else ("" if x is None else str(x))


def _slot(r: dict, k: str) -> Tuple[str, str]:
    v = r.get(k) or {}
    if not isinstance(v, dict):
        return _text(v), _text(v)
    return _text(v.get("text")), _text(v.get("name")) or _text(v.get("text"))


def _shape(r: dict) -> dict:
    r = dict(r)
    for k in ("conditions", "exceptions"):
        r[k] = [t for t in map(_text, r.get(k) or []) if t]
    for k in ("purpose", "references"):
        items = r.get(k) or []
        r[k] = [{"text": _text(x), "name": _text(x.get("name")) if isinstance(x, dict) else _text(x),
                 **({"target": x.get("target")} if isinstance(x, dict) and x.get("target") else {})}
                for x in (items if isinstance(items, list) else [items])]
    for k in SLOTS:
        v = r.get(k)
        if isinstance(v, dict):
            r[k] = {**v, "text": _text(v.get("text")), **({"name": _text(v.get("name"))} if "name" in v else {})}
    r["polarity_text"] = _text(r.get("polarity_text"))
    r["operation"] = str(r.get("operation") or "").strip().lower()
    return r


def _quotes(r: dict) -> List[str]:
    qs = [r.get("polarity_text", "")] + [_slot(r, k)[0] for k in SLOTS]
    qs += [_text(p) for p in r.get("purpose", []) or []]
    qs += [_text(q) for q in (r.get("conditions") or []) + (r.get("exceptions") or [])]
    qs += [_text(x) for x in r.get("references", []) or []]
    return [q for q in qs if q]


def _reject_reason(section: str, r: dict) -> Optional[dict]:
    if r.get("polarity") not in ("ALLOW", "DENY") or not _slot(r, "action")[0] or not _slot(r, "data")[0]:
        return {"reason": "missing polarity, action, or data"}
    if OPERATION_FIELD and not SCHEMA.is_operation(r["operation"]):
        return {"reason": "operation not in the schema"}
    missing = [q for q in _quotes(r) if not _quoted(section, q)]
    if missing:
        return {"reason": "quote not in section", "quotes": missing}
    return None


def action_node(r: dict) -> str:
    verb = " ".join(str((r.get("action") or {}).get("verb", "") if isinstance(r.get("action"), dict) else "").lower().split())
    if not r.get("operation"):
        return verb
    return f"{verb}@{r['operation']}" if verb else r["operation"]


def _accept(section: str, rules) -> Tuple[List[dict], List[dict]]:
    accepted, rejected = [], []
    for r in rules if isinstance(rules, list) else []:
        if not isinstance(r, dict):
            continue
        r = _shape(r)
        why = _reject_reason(section, r)
        if why:
            rejected.append({"rule": r, **why})
        else:
            accepted.append(r)
    return accepted, rejected


def coverage_gaps(section: str, rules: List[dict], min_gap: int = MIN_GAP) -> List[dict]:
    toks = [(m.group().lower(), m.start(), m.end()) for m in re.finditer(r"[^\W_]+", section)]
    words = [t[0] for t in toks]
    ends = [m.end() for m in re.finditer(r"[.!?](?=\s)|\n", section)]
    unit = [bisect.bisect_right(ends, s) for _, s, _ in toks]
    covered = [False] * len(toks)

    def occurrences(frag: List[str]) -> List[int]:
        n = len(frag)
        return [i for i in range(len(words) - n + 1) if words[i:i + n] == frag] if n else []

    def fragments(q: str) -> List[List[str]]:
        return [f for f in (re.findall(r"[^\W_]+", x.lower()) for x in re.split(r"\.\.\.|…", q)) if f]

    for r in rules:
        anchor = {unit[i] for f in fragments(_slot(r, "data")[0]) for i in occurrences(f)}
        for q in _quotes(r):
            for f in fragments(q):
                for i in occurrences(f):
                    if len(f) > 2 or not anchor or unit[i] in anchor:
                        covered[i:i + len(f)] = [True] * len(f)
    gaps, i = [], 0
    while i < len(toks):
        j = i
        while j < len(toks) and not covered[j] and unit[j] == unit[i]:
            j += 1
        if j > i:
            members = [k for k in range(len(toks)) if unit[k] == unit[i]]
            whole = not any(covered[k] for k in members)
            if (whole and j - i >= 2) or j - i >= min_gap:
                u0, u1 = toks[members[0]][1], toks[members[-1]][2]
                gaps.append({"text": section[toks[i][1]:toks[j - 1][2]], "sentence": "" if whole else section[u0:u1],
                             "words": j - i})
            i = j
        else:
            i += 1
    return gaps


def _render_rules(rules: List[dict]) -> str:
    lines = []
    for i, r in enumerate(rules):
        slots = " ".join(f'{k}="{_slot(r, k)[0]}"' for k in ("actor", "data", "recipient", "source") if _slot(r, k)[0])
        quals = " ".join(f"{k}={json.dumps([_text(x) for x in r.get(k) or []], ensure_ascii=False)}"
                         for k in QUALIFIERS if r.get(k))
        lines.append(f'r{i + 1}: {r["polarity"]} "{_slot(r, "action")[0]}" ({r["operation"]}) {slots} {quals}'.rstrip())
    return "\n".join(lines) or "(none)"


def complete_section(llm: LLM, section: str, rules: List[dict], report: Optional[dict] = None) -> Tuple[List[dict], List[dict]]:
    gaps = coverage_gaps(section, rules)
    rep = {"calls": 0, "gaps": len(gaps), "gap_words": sum(g["words"] for g in gaps), "attached": 0,
           "attached_from_gaps": 0, "new_rules": 0, "declared_none": 0, "unanswered": 0, "invalid_attachments": 0}
    new, rejected = [], []
    shared = len(rules) > 1 and any(r.get(k) for r in rules for k in QUALIFIERS)
    if gaps or shared:
        rep["calls"] = 1
        ids = {f"g{i + 1}": g for i, g in enumerate(gaps)}
        passages = "\n".join(f'{gid}: "{g["text"]}"' + (f' (in: "{g["sentence"]}")' if g["sentence"] else "")
                             for gid, g in ids.items()) or "(none)"
        out = llm.json(COMPLETE.format(rules=_render_rules(rules), passages=passages, section=section,
                                       operations=SCHEMA.operations_prompt()), max_tokens=8192)
        answers = out.get("passages") if isinstance(out.get("passages"), dict) else {}
        by_id = {f"r{i + 1}": r for i, r in enumerate(rules)}
        for gid in list(ids) + ["q"]:
            a = answers.get(gid) if isinstance(answers.get(gid), dict) else None
            if a is None:
                rep["unanswered"] += gid != "q"
                continue
            does = a.get("does") if isinstance(a.get("does"), list) else [a.get("does")]
            rep["declared_none"] += "none" in does and not a.get("attach") and not a.get("rules")
            for x in a.get("attach") or []:
                if not isinstance(x, dict):
                    continue
                r, field, text = by_id.get(str(x.get("rule"))), x.get("field"), _text(x.get("text"))
                if r is None or field not in QUALIFIERS or not text or not _quoted(section, text):
                    rep["invalid_attachments"] += 1
                    continue
                present = [_text(v) for v in r.get(field) or []]
                if text in present:
                    continue
                item = text if field in ("conditions", "exceptions") else \
                    {"text": text, "name": text, **({"target": x["target"]} if field == "references" and x.get("target") else {})}
                r[field] = list(r.get(field) or []) + [item]
                r["added"] = r.get("added", []) + [field]
                rep["attached"] += 1
                rep["attached_from_gaps"] += gid != "q"
            acc, rej = _accept(section, a.get("rules"))
            for r in acc:
                r["added_by"] = "completeness"
            new += acc
            rejected += rej
        for x in out.get("detach") or [] if isinstance(out.get("detach"), list) else []:
            if not isinstance(x, dict):
                continue
            r, field, text = by_id.get(str(x.get("rule"))), x.get("field"), _text(x.get("text"))
            if r is None or field not in QUALIFIERS:
                continue
            kept = [v for v in r.get(field) or [] if _text(v) != text]
            if len(kept) < len(r.get(field) or []):
                r[field] = kept
                r["detached"] = r.get("detached", []) + [text]
                rep["detached"] = rep.get("detached", 0) + 1
        rep["new_rules"] = len(new)
    if report is not None:
        report.update(rep)
    return new, rejected


def extract_section(llm: LLM, section: str, report: Optional[dict] = None) -> Tuple[List[dict], List[dict]]:
    template = EXTRACT_SINGLE if os.environ.get("EXTRACT_VARIANT") == "single" else EXTRACT
    prompt = template.format(section=section, operations=SCHEMA.operations_prompt())
    k = int(os.environ.get("SAMPLES", "1"))
    if k == 1:
        accepted, rejected = _accept(section, llm.json(prompt, max_tokens=8192).get("rules"))
    else:
        samples, rejected = [], []
        for i in range(k):
            acc, rej = _accept(section, replace(llm, seed=llm.seed + i, usage=llm.usage).json(prompt, max_tokens=8192).get("rules"))
            samples.append(acc)
            rejected += rej
        accepted = merge_samples(samples, int(os.environ.get("MIN_VOTES", "1")), os.environ.get("LENIENT", "1") == "1",
                                 int(os.environ.get("QUALIFIER_VOTES", "1")))
    if os.environ.get("COMPLETE") == "1":
        new, rej = complete_section(llm, section, accepted, report)
        accepted, rejected = accepted + new, rejected + rej
    elif report is not None:
        gaps = coverage_gaps(section, accepted)
        report.update({"gaps": len(gaps), "gap_words": sum(g["words"] for g in gaps)})
    return accepted, rejected


KNOWN_OPS = {"true", "false", "and", "or", "not", "bool", "cmp", "eq", "residual"}


def _structural_fix(g):
    if not isinstance(g, dict):
        return g
    op = g.get("op")
    if op in ("and", "or") and isinstance(g.get("args"), list):
        return {**g, "args": [_structural_fix(a) for a in g["args"]]}
    if op == "not":
        return {**g, "arg": _structural_fix(g.get("arg"))}
    if op not in KNOWN_OPS:
        for v in (g.get("var"), op):
            if isinstance(v, str) and SCHEMA.admits(v, "bool"):
                return {"op": "bool", "var": v}
    return g


def _compile(g, sig: Signature, quote: str = "") -> dict:
    validate(g)
    g = typed(g, quote)
    sig.add(g)
    return _key_residuals(g)


def translate_section(llm: LLM, section: str, rules: List[dict], report: Optional[dict] = None) -> Dict[str, dict]:
    texts = sorted({q for r in rules for q in (r.get("conditions") or []) + (r.get("exceptions") or [])})
    if not texts:
        return {}
    mode = os.environ.get("REPAIR", "call")
    ids = {f"q{i + 1}": t for i, t in enumerate(texts)}
    out = llm.json(TRANSLATE.format(section=section, variables=SCHEMA.variables_prompt(),
                                    quotes=json.dumps(ids, ensure_ascii=False, indent=1)))
    formulas = out.get("formulas", {}) if isinstance(out.get("formulas"), dict) else {}
    rep = {"translated_quotes": len(ids), "compile_failures": 0, "fixed_structurally": 0, "fixed_by_call": 0}
    result, sig, failed = {}, Signature(), {}
    for qid, text in ids.items():
        g = formulas.get(qid)
        try:
            result[text] = _compile(g, sig, text)
            continue
        except (GuardError, TypeError, KeyError, AttributeError) as e:
            rep["compile_failures"] += 1
            error = str(e) or type(e).__name__
        if mode in ("structural", "call"):
            try:
                result[text] = _compile(_structural_fix(g), sig, text)
                rep["fixed_structurally"] += 1
                continue
            except (GuardError, TypeError, KeyError, AttributeError) as e:
                error = str(e) or type(e).__name__
        failed[qid] = (g, error)
    if failed and mode == "call":
        listing = "\n".join(f"{qid}: {json.dumps(ids[qid], ensure_ascii=False)}\n  formula: {json.dumps(g, ensure_ascii=False)}\n  error: {err}"
                             for qid, (g, err) in failed.items())
        fixed = llm.json(REPAIR.format(section=section, variables=SCHEMA.variables_prompt(), failed=listing))
        fixed = fixed.get("formulas", {}) if isinstance(fixed.get("formulas"), dict) else {}
        for qid in list(failed):
            try:
                result[ids[qid]] = _compile(_structural_fix(fixed.get(qid)), sig, ids[qid])
                rep["fixed_by_call"] += 1
                del failed[qid]
            except (GuardError, TypeError, KeyError, AttributeError):
                pass
    for qid in failed:
        result[ids[qid]] = _residual(ids[qid])
    if report is not None:
        for k, v in rep.items():
            report[k] = report.get(k, 0) + v
    return result


def _residual(text: str) -> dict:
    return {"op": "residual", "id": "r" + hashlib.sha1(_words(text).encode()).hexdigest()[:12], "text": text}


def _key_residuals(g: dict) -> dict:
    if g["op"] == "residual":
        return _residual(_text(g.get("text")) or str(g.get("id")))
    if g["op"] in ("and", "or"):
        return {**g, "args": [_key_residuals(a) for a in g["args"]]}
    if g["op"] == "not":
        return {**g, "arg": _key_residuals(g["arg"])}
    return g


def compile_rules(section_id: str, section: str, raw: List[dict], formulas: Dict[str, dict]) -> List[Rule]:
    rules = []
    for i, r in enumerate(raw):
        conds = [formulas[q] for q in r.get("conditions") or [] if q in formulas and formulas[q] != TRUE]
        excs = [{"op": "not", "arg": formulas[q]} for q in r.get("exceptions") or [] if q in formulas and formulas[q] != TRUE]
        guard = {"op": "and", "args": conds + excs} if conds or excs else {"op": "true"}
        purposes = [p.get("name") or p.get("text") for p in r.get("purpose") or [] if isinstance(p, dict)] or [""]
        for j, purpose in enumerate(purposes):
            rules.append(Rule(
                id=f"{section_id}.{i}.{j}", polarity=r["polarity"],
                actor=_slot(r, "actor")[1], action=action_node(r), data=_slot(r, "data")[1],
                recipient=_slot(r, "recipient")[1], source=_slot(r, "source")[1], purpose=purpose or "", guard=guard,
                evidence=(section_id, r.get("polarity_text", ""), json.dumps(r, ensure_ascii=False))))
    return rules


def deletion_test(rules: List[Rule]) -> Dict[str, list]:
    out = {"unsatisfiable": [], "without_effect": []}
    seen = set()
    for r in rules:
        k = json.dumps(r.guard, sort_keys=True) + r.id.rsplit(".", 1)[0]
        if k in seen or r.guard.get("op") != "and":
            continue
        seen.add(k)
        try:
            if not satisfiable(r.guard):
                out["unsatisfiable"].append(r.id)
            out["without_effect"] += [(r.id, r.guard["args"][i]) for i in without_effect(r.guard["args"])]
        except (GuardError, ValueError):
            continue
    return out


def extract_policy(llm: LLM, sections: List[Tuple[str, str]]) -> Tuple[List[Rule], dict]:
    rules, report = [], {"sections": 0, "raw_rules": 0, "rejected": [], "residual_quotes": 0, "quotes": 0,
                         "completeness": {}, "unsatisfiable_guards": 0, "qualifiers_without_effect": 0}
    for sid, text in sections:
        cov = {}
        raw, rejected = extract_section(llm, text, cov)
        formulas = translate_section(llm, text, raw, report)
        compiled = compile_rules(sid, text, raw, formulas)
        rules += compiled
        dt = deletion_test(compiled)
        report["sections"] += 1
        report["raw_rules"] += len(raw)
        report["rejected"] += [dict(x, section=sid) for x in rejected]
        report["quotes"] += len(formulas)
        report["residual_quotes"] += sum(g["op"] == "residual" for g in formulas.values())
        report["unsatisfiable_guards"] += len(dt["unsatisfiable"])
        report["qualifiers_without_effect"] += len(dt["without_effect"])
        for k, v in cov.items():
            report["completeness"][k] = report["completeness"].get(k, 0) + v
    return rules, report
