#!/usr/bin/env python3
import csv, hashlib, json, shutil
from pathlib import Path

BL = Path(__file__).resolve().parents[1]
CORPUS = BL.parent / "baseline_corpus"
OUT = BL / "work/poligraph/workdirs"
FILES = ("cleaned.html", "accessibility_tree.json", "readability.json")

rows = list(csv.DictReader(open(CORPUS / "manifest.csv", newline="", encoding="utf-8")))
assert len(rows) == 200 and len({r["policy_id"] for r in rows}) == 200
OUT.mkdir(parents=True, exist_ok=True)
staged = []
for r in rows:
    src = (CORPUS / r["policy_dir"]).resolve()
    dst = OUT / r["policy_id"]
    dst.mkdir(exist_ok=True)
    for name in FILES:
        shutil.copyfile(src / name, dst / name)
    html = (dst / "cleaned.html").read_bytes()
    assert hashlib.blake2s(html).hexdigest() == r["hash"] == src.name, r["policy_id"]
    assert html == (CORPUS / r["html_path"]).read_bytes(), r["policy_id"]
    for name in FILES:
        assert (dst / name).read_bytes() == (src / name).read_bytes(), (r["policy_id"], name)
    staged.append({"policy_id": r["policy_id"], "hash": r["hash"], "source_dir": str(src), "workdir": str(dst),
                   **{f"{n}_sha256": hashlib.sha256((dst / n).read_bytes()).hexdigest() for n in FILES}})
with open(OUT.parent / "staged_workdirs.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(staged[0]))
    w.writeheader()
    w.writerows(staged)
print(json.dumps({"staged": len(staged), "out": str(OUT)}))
