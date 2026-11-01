import json, sys
from pathlib import Path

DROP = {"run", "wall_s", "solver_time", "z3_ms", "relation_ms"}


def clean(x):
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items() if k not in DROP}
    if isinstance(x, list):
        return [clean(v) for v in x]
    return x


def load(p):
    if p.suffix == ".jsonl":
        return [clean(json.loads(l)) for l in open(p) if l.strip()]
    return clean(json.load(open(p)))


a, b = Path(sys.argv[1]), Path(sys.argv[2])
bad = 0
for p in sorted(a.glob("*.json*")):
    q = b / p.name
    if not q.exists():
        print("MISSING", p.name); bad += 1; continue
    same = load(p) == load(q)
    print("same     " if same else "DIFFERENT", p.name)
    bad += not same
sys.exit(1 if bad else 0)
