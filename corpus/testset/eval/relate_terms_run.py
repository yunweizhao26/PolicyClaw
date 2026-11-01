import argparse, concurrent.futures as cf, csv, json, os, sys, time
from pathlib import Path

R = Path("/scratch/yz5944/nlp+privacy/PolicyClaw")
sys.path.insert(0, str(R))
from policyclaw.llm import Usage, make_llm  # noqa: E402
from policyclaw.terms import relate_policy_terms  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--dir", type=Path, required=True)
args = ap.parse_args()
D = args.dir.resolve()
with open(D / "selection.tsv", newline="", encoding="utf-8") as f:
    ids = [r["id"] for r in csv.DictReader(f, delimiter="\t")]
todo = [i for i in ids if (D / "rules" / f"{i}.jsonl").exists() and not (D / "rules" / f"{i}.terms.json").exists()]


def run(pid):
    t0 = time.time()
    rows = [json.loads(l) for l in open(D / "rules" / f"{pid}.jsonl")]
    llm = make_llm(os.environ["LLM_MODEL_NAME"], str(D / "relate_cache"), seed=42)
    rel = relate_policy_terms(llm, rows)
    out = {"relations": rel, "usage": llm.usage.as_dict(), "seconds": round(time.time() - t0, 1)}
    (D / "rules" / f"{pid}.terms.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    return pid, out


t0, total, done = time.time(), Usage(), 0
with cf.ThreadPoolExecutor(int(os.environ.get("THREADS", 8))) as ex:
    for fut in cf.as_completed([ex.submit(run, p) for p in todo]):
        pid, out = fut.result()
        done += 1
        for k, v in out["usage"].items():
            if hasattr(total, k):
                setattr(total, k, getattr(total, k) + v)
        rel = out["relations"]
        print(f"{done}/{len(todo)} {pid}: " + ", ".join(f"{k} {len(v['aliases'])}a/{sum(map(len, v['parents'].values()))}p"
                                                       for k, v in rel.items()), flush=True)
print(json.dumps({"policies": len(todo), "usage": total.as_dict(), "elapsed_s": round(time.time() - t0, 1)}), flush=True)
