import json, multiprocessing as mp, os, random, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import z3
from reasoning import OUT, has_derived, load_rows, render
from policyclaw.queries import _Solver

SIZES = (128, 256, 512, 1024, 2048)
REPEATS = 3


def pooled(rows):
    seen = {}
    for u in sorted(rows):
        for r in rows[u]:
            g = r["guard"]
            if g.get("op") != "true" and not has_derived(g):
                seen.setdefault(render(g), g)
    return [seen[k] for k in sorted(seen)]


def run(args):
    k, seed, guards = args
    sv = _Solver(guards)
    zs = [sv.z(g) for g in guards]
    s = z3.Solver()
    s.add(*sv.axioms)
    t0 = time.perf_counter()
    found = 0
    for i in range(len(zs)):
        s.push()
        s.add(zs[i])
        for j in range(i + 1, len(zs)):
            s.push()
            s.add(zs[j])
            r = s.check()
            s.pop()
            if r == z3.unknown:
                raise RuntimeError("solver returned unknown")
            found += r == z3.unsat
        s.pop()
    secs = time.perf_counter() - t0
    return {"k": k, "seed": seed, "pairs": len(zs) * (len(zs) - 1) // 2, "excluded": found, "seconds": secs}


def main():
    pool_guards = pooled(load_rows())
    rnd = random.Random(1)
    tasks = [(k, n, rnd.sample(pool_guards, k)) for k in SIZES for n in range(REPEATS)]
    with mp.Pool(int(os.environ.get("WORKERS", 15))) as pool:
        out = pool.map(run, tasks, chunksize=1)
    res = {"distinct_guards": len(pool_guards), "runs": out}
    json.dump(res, open(OUT / "scale.json", "w"), indent=1)
    print(json.dumps(res))


if __name__ == "__main__":
    main()
