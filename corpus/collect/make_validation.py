from __future__ import annotations

import argparse, csv, json, sys
from datetime import date
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sources  # noqa: E402
from verify import ROOT, render_view  # noqa: E402

PER_STRATUM, N_GPLAY, N_APPSTORE, N_OPP115, BATCH = 100, 100, 50, 25, 10
STAGE2 = ROOT / "corpus" / "stage2" / "out"
COLUMNS = ["id", "source", "stratum", "ref", "url", "domain", "pp_probability", "words", "has_effective_date",
           "text_path"]


def batch_markdown(name: str, pages: list[tuple[str, str]]) -> str:
    header_lines = 7 + len(pages)
    body, starts, line = [], [], header_lines + 1
    for pid, view in pages:
        block = [f"======== PAGE {pid} ========", *view.split("\n"), f"======== END OF PAGE {pid} ========", ""]
        starts.append((pid, line, line + len(block) - 2))
        body += block
        line += len(block)
    header = [f"# {name}", "",
              f"{len(pages)} pages. Label every page with corpus/collect/rubric.md, following "
              f"corpus/collect/validation/instructions.md.", "",
              "| Page | Lines |", "|---|---|", *[f"| {pid} | {a}-{b} |" for pid, a, b in starts], ""]
    assert len(header) == header_lines
    return "\n".join(header + body)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", type=int, default=20261002)
    parser.add_argument("--out", type=Path, default=HERE / "validation")
    parser.add_argument("--force", action="store_true", help="overwrite an existing sample")
    args = parser.parse_args()
    out = args.out
    if (out / "sample.tsv").exists() and not args.force:
        raise SystemExit(f"{out / 'sample.tsv'} exists; labels may depend on it (use --force to rebuild)")
    if STAGE2.exists():
        raise SystemExit(f"{STAGE2} exists: add has_effective_date for the sampled rows before building")
    rng = np.random.default_rng(args.seed)
    meta = {"seed": args.seed, "built": date.today().isoformat()}

    index = sources.privaseer_index()
    meta["privaseer"] = {"files": len(sources.privaseer_files()), "rows": int(len(index)),
                         "strata": sources.stratum_counts(index)}
    ps = sources.sample_privaseer(index, PER_STRATUM, rng)
    texts = sources.privaseer_texts(ps)
    print(f"privaseer index {len(index)} rows, sampled {len(ps)}", flush=True)
    pages = [{"source": "privaseer", "stratum": r.stratum, "ref": f"{Path(r.file).name}:{r.row}:{r.policy_id}",
              "url": r.url or "", "domain": r.domain, "pp_probability": r.probability,
              "policy_id": r.policy_id, "text": texts[(r.file, r.row)]} for r in ps.itertuples()]

    seen_urls = {p["url"] for p in pages if p["url"]}
    for store, n in (("gplay", N_GPLAY), ("appstore", N_APPSTORE)):
        picks, stats = sources.sample_apps(store, n, rng, sources.app_urls(store), exclude_urls=seen_urls)
        meta[store] = stats
        seen_urls |= {p["url"] for p in picks if p["url"]}
        pages += [{"source": store, "stratum": store, "ref": p["app"], "url": p["url"], "domain": p["app"],
                   "pp_probability": "", "text": Path(p["path"]).read_text(encoding="utf-8", errors="replace")}
                  for p in picks]
        print(f"{store}: {stats}", flush=True)

    opp = sources.sample_opp115(N_OPP115, rng)
    meta["opp115"] = {"zip": str(sources.OPP115_ZIP), "source_url": sources.OPP115_URL, "policies": len(opp)}
    pages += [{"source": "opp115", "stratum": "opp115", "ref": p["name"], "url": p["url"], "domain": p["uid"],
               "pp_probability": "", "text": p["text"]} for p in opp]

    meta["effective_date"] = "corpus/stage2/out absent at sampling time; has_effective_date left empty"
    order = rng.permutation(len(pages))
    pages = [pages[i] for i in order]
    width = len(str(len(pages)))
    (out / "text").mkdir(parents=True, exist_ok=True)
    (out / "labels").mkdir(exist_ok=True)
    (out / "batches").mkdir(exist_ok=True)
    rows, views = [], []
    for i, p in enumerate(pages, 1):
        pid = f"v{i:0{width}d}"
        (out / "text" / f"{pid}.txt").write_text(p["text"], encoding="utf-8")
        view, info = render_view(p["text"], p["url"])
        views.append((pid, view))
        prob = p["pp_probability"]
        rows.append({"id": pid, "source": p["source"], "stratum": p["stratum"], "ref": p["ref"], "url": p["url"],
                     "domain": p["domain"], "pp_probability": "" if prob == "" else f"{prob:g}",
                     "words": info["words"], "has_effective_date": "", "text_path": f"text/{pid}.txt"})
    with (out / "sample.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, COLUMNS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    batches = {}
    for b in range(0, len(views), BATCH):
        name = f"batch_{b // BATCH + 1:02d}"
        batches[name] = [pid for pid, _ in views[b:b + BATCH]]
        (out / "batches" / f"{name}.md").write_text(batch_markdown(name, views[b:b + BATCH]) + "\n", encoding="utf-8")
    batch_of = {pid: name for name, ids in batches.items() for pid in ids}
    key = {"seed": args.seed, "batches": batches,
           "pages": {r["id"]: {"batch": batch_of[r["id"]], "source": r["source"], "stratum": r["stratum"],
                               "ref": r["ref"], "url": r["url"]} for r in rows}}
    (out / "key.json").write_text(json.dumps(key, indent=1) + "\n")
    meta["composition"] = {s: sum(1 for r in rows if r["stratum"] == s)
                           for s in dict.fromkeys(r["stratum"] for r in rows)}
    meta["batches"] = len(batches)
    (out / "sample_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
