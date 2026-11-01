from __future__ import annotations

import json, os
from typing import Dict, Iterable, List, Optional

from .queries import Vocabulary
from .schema import SCHEMA


DEFAULT_NETWORK = os.path.join(os.path.dirname(__file__), "network.json")


class ActionNetwork:

    def __init__(self, network_path: Optional[str] = DEFAULT_NETWORK):
        self.aliases: Dict[str, str] = {}
        self.parents: Dict[str, List[str]] = {op: [p] for op in SCHEMA.operations if (p := SCHEMA.operation_parent(op))}
        self.parents[SCHEMA.uncovered["label"]] = [SCHEMA.uncovered["parent"]]
        self.placed = set()
        for x in json.load(open(network_path)) if network_path else []:
            node, placed_op, rel = f"{x['lemma']}@{x['operation']}", x.get("placed_under") or x["operation"], x.get("relation")
            if not SCHEMA.is_operation(x["operation"]):
                continue
            self.placed.add(node)
            if rel == "same" and placed_op in SCHEMA.operations:
                self.aliases[node] = placed_op
            elif rel == "narrower" and SCHEMA.is_operation(placed_op):
                self.parents[node] = [placed_op]

    def vocabulary(self, actions: Iterable[str] = (), extra_parents: Optional[Dict[str, List[str]]] = None,
                   extra_aliases: Optional[Dict[str, str]] = None) -> Vocabulary:
        parents = {k: list(v) for k, v in self.parents.items()}
        for a in actions:
            if "@" in a and a not in self.placed and a not in parents and SCHEMA.is_operation(a.rsplit("@", 1)[1]):
                parents[a] = [a.rsplit("@", 1)[1]]
        for k, v in (extra_parents or {}).items():
            parents.setdefault(k, []).extend(v)
        return Vocabulary(aliases={**self.aliases, **(extra_aliases or {})}, parents=parents)
