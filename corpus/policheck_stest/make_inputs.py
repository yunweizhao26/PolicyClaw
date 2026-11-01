import csv, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "corpus/stores")]
from corpus.rebuild_versions import visible_text  # noqa: E402
import text as T  # noqa: E402

hashes = sorted(p.name for p in (HERE / "input/s_test").iterdir())
assert len(hashes) == 200, len(hashes)
B = HERE / "baseline_corpus"
for d in (HERE / "texts", B / "plaintext_policies", B / "html_policies", B / "policy_dirs"):
    d.mkdir(parents=True, exist_ok=True)
rows = []
for n, h in enumerate(hashes, 1):
    pid, src = f"pg-{n:03d}", (HERE / "input/s_test" / h).resolve()
    html = (src / "cleaned.html").read_bytes()
    text = T.clean(visible_text(html))
    (HERE / "texts" / f"{pid}.visible.txt").write_text(text, encoding="utf-8")
    (B / "plaintext_policies" / f"{pid}.txt").write_text(text, encoding="utf-8")
    (B / "html_policies" / f"{pid}.html").write_bytes(html)
    link = B / "policy_dirs" / pid
    if not link.exists():
        os.symlink(src, link)
    rows.append({"id": pid, "hash": h, "visible_chars": len(text)})
with open(HERE / "selection.tsv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
    w.writeheader()
    w.writerows(rows)
with open(B / "manifest.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["policy_id", "hash", "plaintext_path", "html_path", "policy_dir"])
    w.writeheader()
    for r in rows:
        w.writerow({"policy_id": r["id"], "hash": r["hash"], "plaintext_path": f"plaintext_policies/{r['id']}.txt",
                    "html_path": f"html_policies/{r['id']}.html", "policy_dir": f"policy_dirs/{r['id']}"})
(HERE / "prepare.tsv").write_text("".join(f"{r['id']}\t{HERE / 'texts' / (r['id'] + '.visible.txt')}\n" for r in rows))
chars = sorted(r["visible_chars"] for r in rows)
print(f"{len(rows)} policies; visible characters: min {chars[0]}, median {chars[len(chars) // 2]}, max {chars[-1]}, "
      f"total {sum(chars)}; empty: {sum(c == 0 for c in chars)}")
