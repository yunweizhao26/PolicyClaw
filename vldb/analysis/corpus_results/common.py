import argparse, collections, json, math, os, resource, sys, time
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from policyclaw.actions import ActionNetwork  # noqa: E402
from policyclaw.guards import TRUE, atoms  # noqa: E402
from policyclaw.queries import Rule, _norm  # noqa: E402
from policyclaw.schema import SCHEMA  # noqa: E402

CORPUS = ROOT / "corpus"
OUT = Path(__file__).resolve().parent / "out"
TESTSET = CORPUS / "testset"
TESTSET_OUT = ROOT / "vldb/analysis/testset_results/out"
ARMS = ("web", "android", "apple")
SET = "corpus"
_T0 = time.time()


def use_testset():
    global SET, OUT
    SET, OUT = "testset", TESTSET_OUT
    OUT.mkdir(parents=True, exist_ok=True)


def jsonl(path):
    return [json.loads(line) for line in open(path) if line.strip()]


def versions():
    if SET == "testset":
        import csv
        with open(TESTSET / "selection.tsv", newline="", encoding="utf-8") as f:
            return sorted(({"site_id": r["id"], "version_index": 0, "cleaned_sha256": r["id"], "revert_of": None, "arm": r["arm"]}
                           for r in csv.DictReader(f, delimiter="\t")), key=lambda v: v["site_id"])
    return sorted(jsonl(CORPUS / "final_versions.jsonl"), key=lambda v: (v["site_id"], v["version_index"]))


def pages(vs):
    out = collections.defaultdict(list)
    for v in vs:
        out[v["site_id"]].append(v)
    return out


def unstable_pages(vs):
    n, reverts = collections.Counter(), collections.Counter()
    for v in vs:
        n[v["site_id"]] += 1
        reverts[v["site_id"]] += v["revert_of"] is not None
    return sorted(s for s in n if 2 * reverts[s] > n[s]) if SET == "corpus" else []


def scopes(vs):
    if SET == "testset":
        return (("all", vs),) + tuple((a, [v for v in vs if v["arm"] == a]) for a in ARMS)
    unstable = set(unstable_pages(vs))
    return (("stable_pages", [v for v in vs if v["site_id"] not in unstable]), ("all_pages", vs))


def options(workers=False):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", choices=("reconciled", "extracted"), default="reconciled")
    ap.add_argument("--set", choices=("corpus", "testset"), default="corpus", help="the final versions of the corpus, or the 600-policy evaluation set")
    ap.add_argument("--terms", choices=("on", "off"), default="on",
                    help="testset only: extend the vocabulary of queries.py with the policy's term relations (rules/<id>.terms.json)")
    if workers:
        ap.add_argument("--workers", type=int, default=len(os.sched_getaffinity(0)))
    args = ap.parse_args()
    if args.set == "testset":
        use_testset()
    return args


def out_name(name, rules):
    return f"{name}.json" if rules == "reconciled" else f"{name}_extracted.json"


def unit(v, rules):
    if SET == "testset":
        return v["site_id"]
    return f"{v['site_id']}#{v['version_index']}" if rules == "reconciled" else v["cleaned_sha256"]


def unit_rows(u):
    if SET == "testset":
        return rule_rows(u)
    if "#" in u:
        site, idx = u.rsplit("#", 1)
        return jsonl(CORPUS / "reconciled" / quote(site, safe="") / f"{idx}.jsonl")
    return rule_rows(u)


def sites():
    if SET == "testset":
        return {v["site_id"]: {"domain": v["site_id"]} for v in versions()}
    return {s["site_id"]: s for s in jsonl(CORPUS / "final_sites.jsonl")}


def rule_rows(sha):
    return jsonl((TESTSET if SET == "testset" else CORPUS) / "rules" / f"{sha}.jsonl")


def report(sha):
    return json.load(open((TESTSET if SET == "testset" else CORPUS) / "rules" / f"{sha}.report.json"))


def sections(sha):
    segs = json.load(open(CORPUS / "final_text" / f"{sha}.json"))
    segs = segs if isinstance(segs, list) else segs.get("segments", [])
    return {f"{sha}#s{s['segment_id']}": s["text"] for s in segs}


def rule(row):
    return Rule(row["id"], row["polarity"], row["action"], row["data"], actor=row["actor"], recipient=row["recipient"],
                source=row["source"], purpose=row["purpose"], guard=row["guard"], evidence=tuple(row["evidence"]))


def record_id(rule_id):
    return rule_id.rsplit(".", 1)[0]


def section_id(rule_id):
    return rule_id.rsplit(".", 2)[0]


def one_per_record(rows):
    first = {}
    for r in rows:
        first.setdefault(record_id(r["id"]), r)
    return list(first.values())


def vocabulary(actions):
    return ActionNetwork().vocabulary(sorted(set(actions)))


def under(vocab, operation, action):
    assert SCHEMA.is_operation(operation), operation
    return vocab.covers(operation, action)


def is_true(guard):
    return guard == TRUE


def variables(guard):
    out = set()
    for a in atoms(guard):
        if a["op"] == "residual":
            out.add("residual")
        else:
            v = SCHEMA.variable(a["var"])
            out.add(v["name"] if v else a["var"])
    return out


def practice(vocab, r):
    return (r["polarity"], vocab.canon(r["action"]), _norm(r["data"]), _norm(r["recipient"]), _norm(r["source"]))


def year(ts):
    return int(str(ts)[:4])


def quantile(xs, p):
    xs = sorted(xs)
    return xs[max(0, math.ceil(p * len(xs)) - 1)] if xs else None


def pct(a, b):
    return round(100 * a / b, 2) if b else None


def run_record():
    me, kids = resource.getrusage(resource.RUSAGE_SELF), resource.getrusage(resource.RUSAGE_CHILDREN)
    return {"elapsed_s": round(time.time() - _T0, 1), "cpu_s": round(me.ru_utime + me.ru_stime + kids.ru_utime + kids.ru_stime, 1),
            "peak_rss_mb_self": round(me.ru_maxrss / 1024, 1), "peak_rss_mb_largest_child": round(kids.ru_maxrss / 1024, 1),
            "cpus": len(os.sched_getaffinity(0)), "slurm_job": os.environ.get("SLURM_JOB_ID"),
            "slurm_step": os.environ.get("SLURM_STEP_ID")}


def write(name, result):
    OUT.mkdir(parents=True, exist_ok=True)
    result["run"] = run_record()
    path = OUT / name
    path.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {path.relative_to(ROOT)}; run {result['run']}")
