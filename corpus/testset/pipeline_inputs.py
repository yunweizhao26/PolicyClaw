import csv, hashlib, json, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEGMENTS = "05_segments_v15_exact.json"


def ids():
    with open(HERE / "selection.tsv", newline="", encoding="utf-8") as f:
        return [r["id"] for r in csv.DictReader(f, delimiter="\t")]


def prep():
    with open(HERE / "prepare.tsv", "w", encoding="utf-8") as f:
        for i in ids():
            path = HERE / "texts" / f"{i}.visible.txt"
            assert path.exists(), path
            f.write(f"{i}\t{path}\n")


def extract():
    out = HERE / "final_text"
    out.mkdir(exist_ok=True)
    empty = []
    with open(HERE / "versions.jsonl", "w", encoding="utf-8") as f:
        for i in ids():
            seg = HERE / "prepared" / i / SEGMENTS
            if not seg.exists():
                empty.append(i)
                continue
            shutil.copyfile(seg, out / f"{i}.json")
            text = (HERE / "texts" / f"{i}.visible.txt").read_bytes()
            f.write(json.dumps({"site_id": i, "version_index": 0, "cleaned_sha256": i,
                                "text_sha256": hashlib.sha256(text).hexdigest()}) + "\n")
    (HERE / "empty_after_prep.txt").write_text("".join(f"{i}\n" for i in empty))
    print(f"{len(ids()) - len(empty)} policies with segments, {len(empty)} empty after preparation")


if __name__ == "__main__":
    {"prep": prep, "extract": extract}[sys.argv[1]]()
