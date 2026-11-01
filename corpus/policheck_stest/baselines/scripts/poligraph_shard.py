#!/usr/bin/env python3
import csv, json, os, re, subprocess, sys, time
from pathlib import Path

BL = Path(__file__).resolve().parents[1]
WORK = BL / "work"
DIRS = WORK / "poligraph/workdirs"
CORPUS = BL.parent / "baseline_corpus"
TIMEV = BL.parents[1] / "stores/timev.py"
ENV = Path("/scratch/yz5944/miniconda3/envs/poligraph")
STEPS = [("init_document", []), ("run_annotators", []), ("build_graph", ["--variant", "extended"])]
OUTPUT = {"init_document": "document.pickle", "run_annotators": "document.pickle", "build_graph": "graph-extended.yml"}

shard, nshards = int(sys.argv[1]), int(sys.argv[2])
rows = list(csv.DictReader(open(CORPUS / "manifest.csv", newline="", encoding="utf-8")))
size = {r["policy_id"]: (CORPUS / r["plaintext_path"]).stat().st_size for r in rows}
order = sorted(size, key=lambda p: (-size[p], p))
mine = sorted(order[shard::nshards])
out = WORK / "poligraph/shards" / f"shard_{shard:02d}"
out.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PATH=f"{ENV}/bin:{os.environ['PATH']}", PYTHONPATH=str(WORK / "PoliGraph"),
           PYTHONDONTWRITEBYTECODE="1")
status = {p: {"failed_step": None} for p in mine}
calls = []
for step, extra in STEPS:
    remaining = [p for p in mine if status[p]["failed_step"] is None]
    attempt = 0
    while remaining:
        attempt += 1
        log, tlog = out / f"{step}_{attempt}.log", out / f"{step}_{attempt}.time"
        cmd = [str(ENV / "bin/python"), "-m", f"poligrapher.scripts.{step}", *extra, *[str(DIRS / p) for p in remaining]]
        t0 = time.time()
        with open(log, "w") as f:
            rc = subprocess.call([sys.executable, "-I", str(TIMEV), str(tlog), "--", *cmd], stdout=f, stderr=subprocess.STDOUT,
                                 env=env, cwd=str(WORK))
        calls.append({"step": step, "attempt": attempt, "policies": len(remaining), "rc": rc,
                      "seconds": round(time.time() - t0, 1), "time_log": tlog.name})
        print(json.dumps(calls[-1]), flush=True)
        if rc == 0:
            break
        text = log.read_text(errors="replace")
        started = re.findall(r"\[INFO\] (?:<\S+> )?Processing (\S+) \.\.\.", text)
        if not started:
            sys.exit(f"shard {shard}: {step} failed before processing any policy; see {log}")
        bad = Path(started[-1]).name
        status[bad].update(failed_step=step, rc=rc, log=log.name, tail=text.strip().splitlines()[-15:])
        remaining = remaining[remaining.index(bad) + 1:]
    for p in mine:
        if status[p]["failed_step"] is None:
            assert (DIRS / p / OUTPUT[step]).is_file(), (p, step)
json.dump({"shard": shard, "nshards": nshards, "policies": mine, "calls": calls,
           "failed": {p: s for p, s in status.items() if s["failed_step"]}},
          open(out / "status.json", "w"), indent=1)
print(f"shard {shard}: {len(mine)} policies, {sum(s['failed_step'] is None for s in status.values())} completed all steps")
