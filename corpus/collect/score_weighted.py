from __future__ import annotations

import argparse, csv, json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from score_verifier import POSITIVE, wilson  # noqa: E402

STRATUM_ROWS = {"p_lt_0.6": 142314, "p_0.6_0.9": 1811191, "p_0.9_0.99": 2012890, "p_ge_0.99": 1085}


def read_labels(folder: Path) -> dict:
    out = {}
    for path in sorted(folder.glob("*.jsonl")):
        for line in path.read_text().splitlines():
            if line.strip():
                rec = json.loads(line)
                out[rec["id"]] = rec["label"]
    return out


def weighted(pairs: list[tuple[float, bool, bool]], use_pred: bool) -> str:
    chosen = [(w, h if use_pred else v) for w, v, h in pairs if (v if use_pred else h)]
    if not chosen:
        return "n/a"
    total, hit = sum(w for w, _ in chosen), sum(w for w, ok in chosen if ok)
    n_eff = total ** 2 / sum(w * w for w, _ in chosen)
    p = hit / total
    lo, hi = wilson(round(p * n_eff), round(n_eff)) if n_eff >= 1 else (math.nan, math.nan)
    misses = sum(1 for _, ok in chosen if not ok)
    return f"{100 * p:.1f}% (95% CI {100 * lo:.1f} to {100 * hi:.1f}; {misses} errors in {len(chosen)} pages)"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dir", default="confirmation")
    parser.add_argument("--verifier", default="verifier_v1_medium.jsonl")
    parser.add_argument("--labels", default="labels")
    args = parser.parse_args()
    d = HERE / args.dir
    rows = list(csv.DictReader((d / "sample.tsv").open(), delimiter="\t"))
    ref = read_labels(d / args.labels)
    ver = {json.loads(l)["id"]: json.loads(l).get("label") for l in (d / args.verifier).read_text().splitlines() if l.strip()}
    total_rows = sum(STRATUM_ROWS.values())
    ps = [r for r in rows if r["source"] == "privaseer"]
    in_sample = {s: sum(1 for r in ps if r["stratum"] == s) for s in STRATUM_ROWS}
    weight = {s: (STRATUM_ROWS[s] / total_rows) / (in_sample[s] / len(ps)) if in_sample[s] else 0 for s in STRATUM_ROWS}
    print(f"PrivaSeer stratum counts in sample: {in_sample}; weights: { {s: round(w, 3) for s, w in weight.items()} }")
    if any(in_sample[s] == 0 and STRATUM_ROWS[s] > 10000 for s in STRATUM_ROWS):
        print("warning: a large stratum has no sampled page")
    pairs = [(weight[r["stratum"]], ver[r["id"]] == POSITIVE, ref[r["id"]] == POSITIVE) for r in ps]
    print(f"privaseer (post-stratified): precision {weighted(pairs, True)}; recall {weighted(pairs, False)}")
    for src in ("gplay", "appstore"):
        sub = [(1.0, ver[r["id"]] == POSITIVE, ref[r["id"]] == POSITIVE) for r in rows if r["source"] == src]
        if sub:
            print(f"{src}: precision {weighted(sub, True)}; recall {weighted(sub, False)}")
    apps = [(1.0, ver[r["id"]] == POSITIVE, ref[r["id"]] == POSITIVE) for r in rows if r["source"] != "privaseer"]
    print(f"apps together: precision {weighted(apps, True)}; recall {weighted(apps, False)}")
    complete = {src: sum(1 for r in rows if r["source"] == src and ref[r["id"]] == POSITIVE) for src in ("privaseer", "gplay", "appstore")}
    print(f"reference complete_policy counts: {complete}")


if __name__ == "__main__":
    main()
