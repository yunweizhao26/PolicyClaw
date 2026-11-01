from __future__ import annotations

import argparse, csv, json, sys
from datetime import date
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sources  # noqa: E402
from make_validation import BATCH, COLUMNS, batch_markdown  # noqa: E402
from verify import ROOT, render_view  # noqa: E402

N_PRIVASEER, N_GPLAY, N_APPSTORE = 300, 125, 75
VALIDATION = HERE / "validation"
STAGE2 = ROOT / "corpus" / "stage2" / "out"


def host(name: str) -> str:
    name = (name or "").strip().lower()
    return name[4:] if name.startswith("www.") else name


def excluded() -> tuple[set, set, set]:
    rows = list(csv.DictReader((VALIDATION / "sample.tsv").open(), delimiter="\t"))
    hosts = {host(r["domain"]) for r in rows if r["source"] == "privaseer"}
    hosts |= {host(json.loads(l)["domain"]) for l in (ROOT / "corpus" / "final_sites.jsonl").read_text().splitlines()
              if l.strip()}
    apps = {r["ref"] for r in rows if r["source"] in ("gplay", "appstore")}
    urls = {r["url"] for r in rows if r["url"]}
    return hosts, apps, urls


def sample_privaseer_uniform(index, n: int, rng: np.random.Generator, exclude_hosts: set):
    hosts, used, picks = index.domain.map(host).to_numpy(), set(exclude_hosts), []
    for i in rng.permutation(len(index)):
        if not hosts[i] or hosts[i] in used:
            continue
        used.add(hosts[i])
        picks.append(i)
        if len(picks) == n:
            break
    return index.iloc[picks].copy()


def privaseer_dates(sample) -> dict:
    out = {}
    for path, part in sample.groupby("file"):
        table = pq.read_table(STAGE2 / "privaseer" / Path(path).name, columns=["gid", "has_effective_date"])
        found = dict(zip(table.column("gid").to_pylist(), table.column("has_effective_date").to_pylist()))
        out.update({str(pid): found.get(str(pid)) for pid in part.policy_id})
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", type=int, default=20261004)
    parser.add_argument("--out", type=Path, default=HERE / "confirmation")
    args = parser.parse_args()
    out = args.out
    if (out / "sample.tsv").exists():
        raise SystemExit(f"{out / 'sample.tsv'} exists; labels may depend on it")
    rng = np.random.default_rng(args.seed)
    ex_hosts, ex_apps, ex_urls = excluded()
    meta = {"seed": args.seed, "built": date.today().isoformat(),
            "excluded": {"hosts": len(ex_hosts), "apps": len(ex_apps), "urls": len(ex_urls)}}

    index = sources.privaseer_index()
    ps = sample_privaseer_uniform(index, N_PRIVASEER, rng, ex_hosts)
    texts, dated = sources.privaseer_texts(ps), privaseer_dates(ps)
    meta["privaseer"] = {"rows": int(len(index)), "sampled": int(len(ps))}
    pages = [{"source": "privaseer", "stratum": sources.stratum_of(r.probability),
              "ref": f"{Path(r.file).name}:{r.row}:{r.policy_id}", "url": r.url or "", "domain": r.domain,
              "pp_probability": r.probability, "dated": dated.get(str(r.policy_id)),
              "text": texts[(r.file, r.row)]} for r in ps.itertuples()]

    app_dates = {(r["store"], r["app_id"]): r["has_effective_date"] == "True"
                 for r in csv.DictReader((STAGE2 / "apps.csv").open())}
    seen_urls = set(ex_urls) | {p["url"] for p in pages if p["url"]}
    for store, n in (("gplay", N_GPLAY), ("appstore", N_APPSTORE)):
        picks, stats = sources.sample_apps(store, n, rng, sources.app_urls(store), exclude_apps=ex_apps,
                                           exclude_urls=seen_urls)
        meta[store] = stats
        seen_urls |= {p["url"] for p in picks if p["url"]}
        pages += [{"source": store, "stratum": store, "ref": p["app"], "url": p["url"], "domain": p["app"],
                   "pp_probability": "", "dated": app_dates.get((store, p["app"])),
                   "text": Path(p["path"]).read_text(encoding="utf-8", errors="replace")} for p in picks]

    pages = [pages[i] for i in rng.permutation(len(pages))]
    width = len(str(len(pages)))
    for sub in ("text", "labels", "batches"):
        (out / sub).mkdir(parents=True, exist_ok=True)
    rows, views = [], []
    for i, p in enumerate(pages, 1):
        pid = f"c{i:0{width}d}"
        (out / "text" / f"{pid}.txt").write_text(p["text"], encoding="utf-8")
        view, info = render_view(p["text"], p["url"])
        views.append((pid, view))
        prob = p["pp_probability"]
        rows.append({"id": pid, "source": p["source"], "stratum": p["stratum"], "ref": p["ref"], "url": p["url"],
                     "domain": p["domain"], "pp_probability": "" if prob == "" else f"{prob:g}",
                     "words": info["words"], "has_effective_date": "" if p["dated"] is None else str(bool(p["dated"])),
                     "text_path": f"text/{pid}.txt"})
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
    instructions = (VALIDATION / "instructions.md").read_text()
    (out / "instructions.md").write_text(instructions.replace("validation/", f"{out.name}/"))
    meta["composition"] = {s: sum(1 for r in rows if r["source"] == s) for s in ("privaseer", "gplay", "appstore")}
    meta["privaseer_strata"] = {s: sum(1 for r in rows if r["stratum"] == s)
                                for s in dict.fromkeys(r["stratum"] for r in rows if r["source"] == "privaseer")}
    meta["batches"] = len(batches)
    (out / "sample_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
