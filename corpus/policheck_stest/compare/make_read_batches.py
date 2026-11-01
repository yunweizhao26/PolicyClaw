import csv, json, os, random, textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
T = HERE.parent
BATCH_CHARS, SEED = 150_000, 20261021


def wrap(text):
    return "\n".join(textwrap.fill(l, 1500, break_long_words=False, break_on_hyphens=False) if len(l) > 1500 else l
                     for l in text.split("\n"))


with open(T / "selection.tsv", newline="", encoding="utf-8") as f:
    ids = [r["id"] for r in csv.DictReader(f, delimiter="\t")]
random.Random(f"{SEED}:read").shuffle(ids)
texts = {p: (T / "texts" / f"{p}.visible.txt").read_text(encoding="utf-8") for p in ids}
batches, cur, size = [], [], 0
for p in ids:
    if cur and size + len(texts[p]) > BATCH_CHARS:
        batches.append(cur)
        cur, size = [], 0
    cur.append(p)
    size += len(texts[p])
batches.append(cur)
os.makedirs(HERE / "read_batches", exist_ok=True)
for b, pols in enumerate(batches, 1):
    with open(HERE / "read_batches" / f"read_{b:02d}.md", "w") as f:
        for p in pols:
            f.write(f"=== POLICY {p}\n{wrap(texts[p])}\n=== END POLICY {p}\n\n")
json.dump({"batches": {f"{b:02d}": pols for b, pols in enumerate(batches, 1)}, "seed": SEED, "batch_chars": BATCH_CHARS},
          open(HERE / "read_key.json", "w"), indent=1)
print(f"{len(ids)} policies in {len(batches)} batches; policies per batch {[len(b) for b in batches]}; "
      f"largest batch {max(sum(len(texts[p]) for p in b) for b in batches)} characters")
