from __future__ import annotations

import argparse, json, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify import render_view  # noqa: E402

V = HERE / "validation"
A = V / "adjudication"
BATCH = 9


def read_jsonl(path: Path) -> dict:
    return {r["id"]: r for r in (json.loads(l) for l in path.read_text().splitlines() if l.strip())}


def labeler_labels() -> dict:
    out = {}
    for path in sorted((V / "labels").glob("*.jsonl")):
        out.update(read_jsonl(path))
    return out


def batches(runs: list[str]):
    import csv
    rows = {r["id"]: r for r in csv.DictReader((V / "sample.tsv").open(), delimiter="\t")}
    human = labeler_labels()
    verifier = {name: read_jsonl(V / name) for name in runs}
    chosen = sorted(i for i in rows if any(verifier[n][i]["label"] != human[i]["label"] for n in runs))
    rng = np.random.default_rng(20261003)
    key, files = {"runs": runs, "pages": {}, "batches": {}}, []
    for b, start in enumerate(range(0, len(chosen), BATCH), 1):
        name, blocks = f"adj_{b:02d}", []
        for i in chosen[start:start + BATCH]:
            opinions = {human[i]["label"]: (human[i].get("reason", ""), ["labelers"])}
            for n in runs:
                label, reason = verifier[n][i]["label"], verifier[n][i].get("reason", "")
                if label in opinions:
                    opinions[label][1].append(n)
                else:
                    opinions[label] = (reason, [n])
            order = list(opinions)
            rng.shuffle(order)
            text = Path(rows[i]["text_path"] if Path(rows[i]["text_path"]).is_absolute()
                        else V / rows[i]["text_path"]).read_text(encoding="utf-8", errors="replace")
            view, _ = render_view(text, rows[i]["url"])
            blocks += [f"======== PAGE {i} ========", view, f"======== END OF PAGE {i} ========", "",
                       f"Opinions on page {i}:"]
            blocks += [f"- Opinion {k}: {lab}. {' '.join(opinions[lab][0].split())}" for k, lab in enumerate(order, 1)]
            blocks.append("")
            key["pages"][i] = {f"opinion_{k}": {"label": lab, "from": opinions[lab][1]} for k, lab in enumerate(order, 1)}
        key["batches"][name] = chosen[start:start + BATCH]
        files.append((name, "\n".join([f"# {name}", "", f"{len(key['batches'][name])} pages.", ""] + blocks)))
    (A / "batches").mkdir(parents=True, exist_ok=True)
    (A / "labels").mkdir(exist_ok=True)
    for name, body in files:
        (A / "batches" / f"{name}.md").write_text(body + "\n")
    (A / "key.json").write_text(json.dumps(key, indent=1) + "\n")
    print(f"pages={len(chosen)} batches={len(files)}")


def merge():
    adjudicated = {}
    for path in sorted((A / "labels").glob("*.jsonl")):
        adjudicated.update(read_jsonl(path))
    key = json.loads((A / "key.json").read_text())
    missing = sorted(set(key["pages"]) - set(adjudicated))
    if missing:
        raise SystemExit(f"not adjudicated: {missing}")
    out = V / "labels_adjudicated"
    out.mkdir(exist_ok=True)
    changed = 0
    for path in sorted((V / "labels").glob("*.jsonl")):
        lines = []
        for rec in read_jsonl(path).values():
            if rec["id"] in adjudicated:
                adj = adjudicated[rec["id"]]
                changed += adj["label"] != rec["label"]
                rec = {**rec, "labeler_label": rec["label"], "label": adj["label"],
                       "flags": adj.get("flags", rec.get("flags")), "reason": adj.get("reason", ""), "adjudicated": True}
            lines.append(json.dumps(rec, ensure_ascii=False))
        (out / path.name).write_text("\n".join(lines) + "\n")
    print(f"adjudicated={len(adjudicated)} labels changed={changed}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("step", choices=["batches", "merge"])
    parser.add_argument("--runs", nargs="+", default=["verifier.jsonl", "verifier_v1_medium.jsonl"])
    parser.add_argument("--dir", default="validation")
    args = parser.parse_args()
    global V, A
    V, A = HERE / args.dir, HERE / args.dir / "adjudication"
    batches(args.runs) if args.step == "batches" else merge()


if __name__ == "__main__":
    main()
