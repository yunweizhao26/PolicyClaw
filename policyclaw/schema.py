from __future__ import annotations

import difflib, json, os, re
from typing import Dict, Iterable, List, Optional

DEFAULT = os.environ.get("POLICYCLAW_SCHEMA") or os.path.join(os.path.dirname(__file__), "schema.json")
KIND_OP = {"int": "cmp", "category": "eq", "bool": "bool"}


class Schema:
    def __init__(self, path: str = DEFAULT):
        s = json.load(open(path))
        self.operations: Dict[str, dict] = s["operations"]
        self.uncovered: dict = s["uncovered"]
        self.variables: List[dict] = s["variables"]
        self.closed_world_note: str = s.get("closed_world_note", "")
        self._axioms: List[dict] = s.get("axioms", [])
        self.value_sets: Dict[str, dict] = s.get("value_sets", {})
        self.units: Dict[str, dict] = s.get("units", {})
        self._canon: Dict[str, Dict[str, str]] = {}
        for name, vs in self.value_sets.items():
            m = self._canon.setdefault(name, {})
            for value, v in vs["values"].items():
                for form in [value] + v.get("aliases", []):
                    m[_key(form)] = value

    def variable(self, name: str) -> Optional[dict]:
        for v in self.variables:
            pat = v["name"]
            if pat == name or (pat.endswith(".*") and name.startswith(pat[:-1]) and len(name) > len(pat) - 1):
                return v
        return None

    def admits(self, name: str, op: str) -> bool:
        v = self.variable(name)
        return v is not None and KIND_OP[v["kind"]] == op

    def closed_world(self, name: str) -> bool:
        v = self.variable(name)
        return bool(v and v.get("closed_world"))

    def value_set(self, name: str) -> Optional[dict]:
        v = self.variable(name)
        return self.value_sets.get(v["value_set"]) if v and v.get("value_set") else None

    def canonical_value(self, name: str, value: str) -> Optional[str]:
        v = self.variable(name)
        return self._canon[v["value_set"]].get(_key(value)) if v and v.get("value_set") else value

    def close_values(self, name: str, value: str, n: int = 5) -> List[str]:
        vs = self.value_set(name)
        return difflib.get_close_matches(value, list(vs["values"]), n=n, cutoff=0.5) if vs else []

    def ancestors(self, name: str, value: str) -> List[str]:
        vs, out = self.value_set(name), []
        while vs and value in vs["values"] and vs["values"][value].get("parent"):
            value = vs["values"][value]["parent"]
            out.append(value)
        return out

    def value_axioms(self, pairs: Iterable[tuple]) -> List[dict]:
        out, by_var = [], {}
        for var, value in pairs:
            if self.value_set(var):
                by_var.setdefault(var, set()).add(value)
        atom = lambda var, value: {"op": "eq", "var": var, "value": value}
        for var, values in by_var.items():
            values = sorted(values)
            for i, a in enumerate(values):
                for b in values[i + 1:]:
                    if b in self.ancestors(var, a):
                        out.append({"op": "or", "args": [{"op": "not", "arg": atom(var, a)}, atom(var, b)]})
                    elif a in self.ancestors(var, b):
                        out.append({"op": "or", "args": [{"op": "not", "arg": atom(var, b)}, atom(var, a)]})
                    else:
                        out.append({"op": "not", "arg": {"op": "and", "args": [atom(var, a), atom(var, b)]}})
        return out

    def bounds(self, name: str) -> tuple:
        v = self.variable(name) or {}
        return v.get("min"), v.get("max")

    def unit_values(self, name: str, text: str) -> Optional[set]:
        v = self.variable(name) or {}
        unit = self.units.get(v.get("unit", ""))
        numbers = [int(x) for x in re.findall(r"\d+", text or "")]
        if not unit or not numbers:
            return None
        low = (text or "").lower()
        named = [u for u, forms in unit["words"].items() if any(re.search(rf"\b{re.escape(f)}\b", low) for f in forms)]
        if not named:
            return None
        return {n * unit["factors"][u] + d for n in numbers for u in named for d in (-1, 0, 1)}

    def derived_variables(self) -> List[str]:
        return [v["name"] for v in self.variables if v.get("derived")]

    def int_variables(self) -> List[str]:
        return [v["name"] for v in self.variables if v["kind"] == "int"]

    def operation_parent(self, op: str) -> Optional[str]:
        if op == self.uncovered["label"]:
            return self.uncovered["parent"]
        return self.operations[op].get("parent")

    def is_operation(self, op: str) -> bool:
        return op in self.operations or op == self.uncovered["label"]

    def axioms(self, names: Iterable[str]) -> List[dict]:
        names = set(names)
        out = []
        for ax in self._axioms:
            if "scope_of" not in ax:
                out.append(ax["formula"])
                continue
            prefixes = [p[:-1] for p in ax["scope_of"]]
            scopes = {n[len(p):] for n in names for p in prefixes if n.startswith(p) and len(n) > len(p)}
            text = json.dumps(ax["formula"])
            out += [json.loads(text.replace("{x}", x)) for x in sorted(scopes)]
        return out

    def variables_prompt(self) -> str:
        form = {"int": "integer", "category": "a value", "bool": "true or false"}

        def kind(v):
            if v.get("value_set"):
                return f"one {v['value_set']} from the schema's list, by its common English name"
            if v.get("unit"):
                return f"integer, in {v['unit']}"
            return form[v["kind"]]
        return "\n".join(f"- {v['name'].replace('*', 'NAME')} ({kind(v)}): {v['gloss']}" for v in self.variables)

    def operations_prompt(self) -> str:
        lines = []

        def walk(op: str, depth: int) -> None:
            lines.append(f"{'  ' * depth}- {op}: {self.operations[op]['gloss']}")
            for child, v in self.operations.items():
                if v.get("parent") == op:
                    walk(child, depth + 1)

        for op, v in self.operations.items():
            if not v.get("parent"):
                walk(op, 0)
        lines.append(f"- {self.uncovered['label']}: {self.uncovered['gloss']}")
        return "\n".join(lines)


def _key(s: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", (s or "").lower()))


SCHEMA = Schema()
