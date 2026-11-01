from __future__ import annotations

import argparse, csv, json, sys
from datetime import date
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sources  # noqa: E402
import verify  # noqa: E402

COLUMNS = ["id", "source", "stratum", "ref", "url", "domain", "pp_probability", "words", "text_path"]


def allocate(total: int, caps: dict) -> dict:
    counts, left = {k: 0 for k in caps}, total
    open_ = [k for k in caps if caps[k] > 0]
    while left > 0 and open_:
        share, extra = divmod(left, len(open_))
        for i, k in enumerate(open_):
            add = min(share + (1 if i < extra else 0), caps[k] - counts[k])
            counts[k] += add
            left -= add
        open_ = [k for k in open_ if counts[k] < caps[k]]
    return counts


def build_sample(args) -> list[dict]:
    rng = np.random.default_rng(args.seed)
    with (HERE / "validation" / "sample.tsv").open(newline="") as handle:
        held_out = list(csv.DictReader(handle, delimiter="\t"))
    exclude_domains = {r["domain"] for r in held_out if r["source"] == "privaseer"}
    exclude_apps = {r["ref"] for r in held_out if r["source"] in ("gplay", "appstore")}
    exclude_urls = {r["url"] for r in held_out if r["url"]}
    meta = {"seed": args.seed, "built": date.today().isoformat(),
            "held_out": {"domains": len(exclude_domains), "apps": len(exclude_apps), "urls": len(exclude_urls)}}

    index = sources.privaseer_index(args.threads)
    meta["privaseer"] = {"rows": int(len(index)), "strata": sources.stratum_counts(index)}
    caps = {name: int(index.domain[(index.probability >= lo) & (index.probability < hi)
                                   & ~index.domain.isin(exclude_domains)].nunique())
            for name, lo, hi in sources.STRATA}
    counts = allocate(args.privaseer_n, caps)
    meta["privaseer"]["requested"] = counts
    part = sources.sample_privaseer(index, counts, rng, exclude_domains, strict=False)
    texts = sources.privaseer_texts(part, args.threads)
    pages = [{"id": f"ps-{Path(r.file).stem}-{r.row}", "source": "privaseer", "stratum": r.stratum,
              "ref": f"{Path(r.file).name}:{r.row}:{r.policy_id}", "url": r.url or "", "domain": r.domain,
              "pp_probability": f"{r.probability:g}", "text": texts[(r.file, r.row)]} for r in part.itertuples()]
    print(f"privaseer: {len(pages)} pages", flush=True)

    urls_seen = exclude_urls | {p["url"] for p in pages if p["url"]}
    for store, n, prefix in (("gplay", args.gplay_n, "gp"), ("appstore", args.appstore_n, "as")):
        if n == 0:
            continue
        picks, stats = sources.sample_apps(store, n, rng, sources.app_urls(store), exclude_apps, urls_seen)
        meta[store] = stats
        urls_seen |= {p["url"] for p in picks if p["url"]}
        pages += [{"id": f"{prefix}-{p['app']}", "source": store, "stratum": store, "ref": p["app"], "url": p["url"],
                   "domain": p["app"], "pp_probability": "",
                   "text": Path(p["path"]).read_text(encoding="utf-8", errors="replace")} for p in picks]
        print(f"{store}: {stats}", flush=True)

    out = args.out
    (out / "text").mkdir(parents=True, exist_ok=True)
    rows = []
    for p in pages:
        (out / "text" / f"{p['id']}.txt").write_text(p["text"], encoding="utf-8")
        rows.append({**{k: p[k] for k in COLUMNS if k in p}, "words": verify.render_view(p["text"])[1]["words"],
                     "text_path": f"text/{p['id']}.txt"})
    if len({r["id"] for r in rows}) != len(rows):
        raise SystemExit("duplicate ids")
    with (out / "sample.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, COLUMNS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    meta["composition"] = {s: sum(1 for r in rows if r["stratum"] == s) for s in dict.fromkeys(r["stratum"] for r in rows)}
    (out / "sample_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--privaseer-n", type=int, default=5000)
    parser.add_argument("--gplay-n", type=int, default=800)
    parser.add_argument("--appstore-n", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20261003)
    parser.add_argument("--out", type=Path, default=HERE / "training")
    parser.add_argument("--threads", type=int, default=16)
    parser.add_argument("--sample-only", action="store_true", help="write the sample and stop before the verifier")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    tsv = args.out / "sample.tsv"
    if tsv.exists():
        print(f"reusing {tsv}", flush=True)
    else:
        build_sample(args)
    if args.sample_only:
        return
    records = verify.run(verify.read_rows(tsv), args.out.resolve(), args.out / "labels.jsonl", args.threads, args.resume)
    sys.exit(1 if any("error" in r for r in records) else 0)


if __name__ == "__main__":
    main()
