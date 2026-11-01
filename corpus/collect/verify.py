from __future__ import annotations

import argparse, csv, functools, json, os, re, statistics, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from policyclaw.llm import make_llm  # noqa: E402

PROMPT_PATHS = {"v1": ROOT / "policyclaw" / "prompts" / "verify_policy_page.txt",
                "v2": ROOT / "policyclaw" / "prompts" / "verify_policy_page_v2.txt"}
RUBRIC_PATH = ROOT / "corpus" / "collect" / "rubric.md"
DEFAULT_CACHE = ROOT / "corpus" / "collect" / "llm_cache"

HEAD_WORDS, TAIL_WORDS = 1500, 300
HEAD_CHARS, TAIL_CHARS = 12000, 2400
WRAP = 1000
MAX_EVIDENCE = 3

LABELS = ["complete_policy", "partial_policy", "cookie_only", "other_legal", "not_policy"]
SCHEMA = {
    "type": "object",
    "properties": {
        "evidence": {"type": "array", "items": {"type": "string"}, "maxItems": MAX_EVIDENCE},
        "reason": {"type": "string"},
        "label": {"type": "string", "enum": LABELS},
        "flags": {"type": "object",
                  "properties": {"multiple_orgs": {"type": "boolean"}, "language": {"type": "string"}},
                  "required": ["multiple_orgs", "language"]},
    },
    "required": ["evidence", "reason", "label", "flags"],
}
ITEMS = ["organization", "collection", "use_or_sharing", "rights_retention_contact"]
REQUIRED_ITEMS = ITEMS[1:]
SCHEMA_V2 = {
    "type": "object",
    "properties": {
        "items": {"type": "object", "properties": {k: {"type": "string"} for k in ITEMS}, "required": ITEMS},
        "reason": SCHEMA["properties"]["reason"],
        "label": SCHEMA["properties"]["label"],
        "flags": SCHEMA["properties"]["flags"],
    },
    "required": ["items", "reason", "label", "flags"],
}
SCHEMAS = {"v1": SCHEMA, "v2": SCHEMA_V2}



def normalize(text: str) -> str:
    lines, out = text.replace("\r\n", "\n").replace("\r", "\n").split("\n"), []
    for line in lines:
        line = line.rstrip()
        if line.strip() or (out and out[-1] != ""):
            out.append(line if line.strip() else "")
    return "\n".join(out).strip("\n")


def wrap(text: str) -> str:
    out = []
    for line in text.split("\n"):
        while len(line) > WRAP:
            cut = line.rfind(" ", 0, WRAP + 1)
            cut = cut if cut > 0 else WRAP
            out.append(line[:cut].rstrip())
            line = line[cut:].lstrip()
        out.append(line)
    return "\n".join(out)


def render_view(text: str, url: str = "") -> tuple[str, dict]:
    text = normalize(text or "")
    spans = [m.span() for m in re.finditer(r"\S+", text)]
    n = len(spans)
    if n > HEAD_WORDS + TAIL_WORDS:
        head_end, tail_start = spans[HEAD_WORDS - 1][1], spans[n - TAIL_WORDS][0]
    else:
        head_end, tail_start = len(text), 0
    head_end, tail_start = min(head_end, HEAD_CHARS), max(tail_start, len(text) - TAIL_CHARS)
    info = {"words": n, "chars": len(text)}
    if tail_start <= head_end:
        body = wrap(text) if text else "(no text)"
        info.update(truncated=False, shown_words=n, omitted_words=0)
        header = f"Words: {n:,} (whole page shown)"
    else:
        head_words = sum(1 for s, _ in spans if s < head_end)
        tail_words = sum(1 for _, e in spans if e > tail_start)
        omitted = n - head_words - tail_words + sum(1 for s, e in spans if s < head_end and e > tail_start)
        omitted = max(omitted, 0)
        marker = f"[... {omitted:,} words ({tail_start - head_end:,} characters) omitted ...]"
        body = wrap(text[:head_end].rstrip()) + f"\n\n{marker}\n\n" + wrap(text[tail_start:].lstrip())
        info.update(truncated=True, shown_words=head_words + tail_words, omitted_words=omitted)
        header = (f"Words: {n:,} (cut: the first {head_words:,} and the last {tail_words:,} words are shown, "
                  f"{omitted:,} words omitted)")
    return f"URL: {url or 'unknown'}\n{header}\n\n{body}", info


@functools.lru_cache(maxsize=None)
def _template(version: str = "v1") -> str:
    return PROMPT_PATHS[version].read_text().replace("<<RUBRIC>>", RUBRIC_PATH.read_text().strip())


def build_prompt(view: str, version: str = "v1") -> str:
    return _template(version).replace("<<PAGE>>", view)



def read_rows(tsv: Path) -> list[dict]:
    with tsv.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        if not row.get("id"):
            raise SystemExit(f"{tsv}: a row has no id")
        if not row.get("text_path") and not (row.get("parquet") and row.get("row")):
            raise SystemExit(f"{tsv}: row {row['id']} has neither text_path nor parquet and row")
    return rows


def load_parquet_texts(rows: list[dict], text_column: str, threads: int) -> dict:
    import pyarrow.parquet as pq
    by_file: dict[str, set] = {}
    for row in rows:
        if not row.get("text_path"):
            by_file.setdefault(row["parquet"], set()).add(int(row["row"]))

    def read(path):
        pf = pq.ParquetFile(path)
        columns = [text_column] + (["url"] if "url" in pf.schema_arrow.names else [])
        out, start = {}, 0
        for rg in range(pf.metadata.num_row_groups):
            size = pf.metadata.row_group(rg).num_rows
            wanted = sorted(r for r in by_file[path] if start <= r < start + size)
            if wanted:
                table = pf.read_row_group(rg, columns=columns).take([r - start for r in wanted]).to_pylist()
                for r, rec in zip(wanted, table):
                    out[(path, r)] = (rec[text_column] or "", rec.get("url") or "")
            start += size
        return out

    texts = {}
    with ThreadPoolExecutor(threads) as pool:
        for part in pool.map(read, sorted(by_file)):
            texts.update(part)
    return texts


def page_input(row: dict, base: Path, parquet_texts: dict) -> tuple[str, str]:
    if row.get("text_path"):
        path = Path(row["text_path"])
        path = path if path.is_absolute() else base / path
        return path.read_text(encoding="utf-8", errors="replace"), row.get("url", "")
    text, url = parquet_texts[(row["parquet"], int(row["row"]))]
    return text, row.get("url") or url



def _squash(s: str) -> str:
    return " ".join(s.split())


def parse_reply(text: str, version: str = "v1") -> dict:
    out = json.loads(text)
    if out.get("label") not in LABELS:
        raise ValueError(f"label {out.get('label')!r}")
    flags = out.get("flags") or {}
    if not isinstance(flags.get("multiple_orgs"), bool) or not isinstance(flags.get("language"), str):
        raise ValueError("flags")
    if not isinstance(out.get("reason"), str):
        raise ValueError("reason")
    parsed = {"label": out["label"], "flags": {"multiple_orgs": flags["multiple_orgs"], "language": flags["language"]},
              "reason": out["reason"]}
    if version == "v2":
        items = out.get("items")
        if not isinstance(items, dict) or not all(isinstance(items.get(k), str) for k in ITEMS):
            raise ValueError("items")
        parsed["items"] = {k: items[k] for k in ITEMS}
        parsed["evidence"] = [items[k] for k in ITEMS if items[k].strip()]
    else:
        if not isinstance(out.get("evidence"), list):
            raise ValueError("evidence")
        parsed["evidence"] = [str(e) for e in out["evidence"]][:MAX_EVIDENCE]
    return parsed


def verify_view(view: str, model: str, cache: str, seed: int = 42, version: str = "v1",
                truncated: bool = False) -> dict:
    llm = make_llm(model, cache, seed=seed)
    prompt, error = build_prompt(view, version), ""
    for attempt in (llm, replace(llm, seed=seed + 1, usage=llm.usage)):
        reply = attempt.complete(prompt, 2048, SCHEMAS[version])
        try:
            out = parse_reply(reply, version)
            break
        except (ValueError, TypeError, AttributeError, json.JSONDecodeError) as e:
            error = f"unusable reply ({e}): {reply[:300]}"
    else:
        out = {"error": error}
    page = _squash(view)
    if "evidence" in out:
        out["evidence_in_view"] = [bool(_squash(e)) and _squash(e) in page for e in out["evidence"]]
    if "items" in out:
        found = {k: bool(_squash(q)) and _squash(q) in page for k, q in out["items"].items()}
        out["items_in_view"] = found
        if out["label"] == "complete_policy" and not truncated and not all(found[k] for k in REQUIRED_ITEMS):
            out["model_label"], out["label"] = out["label"], "partial_policy"
    u = llm.usage
    out["usage"] = {"calls": u.calls, "cached": u.cached, "failures": u.failures, "prompt_tokens": u.prompt_tokens,
                    "completion_tokens": u.completion_tokens, "thinking_tokens": u.thinking_tokens,
                    "seconds": round(u.seconds, 2)}
    out["model"], out["variant"] = llm.model, llm.variant
    return out



def summarize(records: list[dict]) -> dict:
    fresh = [r["usage"] for r in records if r.get("usage", {}).get("calls")]
    total = {k: sum(u.get(k, 0) for u in (r.get("usage", {}) for r in records))
             for k in ("calls", "cached", "failures", "prompt_tokens", "completion_tokens", "thinking_tokens", "seconds")}
    per_page = {}
    for key in ("prompt_tokens", "completion_tokens", "thinking_tokens"):
        values = [u[key] for u in fresh]
        if values:
            q = statistics.quantiles(values, n=20) if len(values) > 1 else values * 19
            per_page[key] = {"mean": round(statistics.mean(values), 1), "median": statistics.median(values),
                             "p95": round(q[18], 1), "max": max(values)}
    labels = {}
    for r in records:
        key = r.get("label", "error")
        labels[key] = labels.get(key, 0) + 1
    return {"pages": len(records), "errors": sum(1 for r in records if "error" in r), "labels": labels,
            "pages_with_model_calls": len(fresh), "totals": total, "per_page_with_model_calls": per_page,
            "truncated_pages": sum(1 for r in records if r.get("truncated"))}


def run(rows: list[dict], base: Path, out_path: Path, threads: int, resume: bool, text_column: str = "text",
        model: str | None = None, cache: str | None = None, version: str = "v1") -> list[dict]:
    model = model or os.environ.get("LLM_MODEL_NAME")
    if not model:
        raise SystemExit("LLM_MODEL_NAME is required")
    cache = cache or os.environ.get("LLM_CACHE") or str(DEFAULT_CACHE)
    done = {}
    if resume and out_path.exists():
        for line in out_path.read_text().splitlines():
            rec = json.loads(line)
            if "error" not in rec:
                done[rec["id"]] = rec
    todo = [r for r in rows if r["id"] not in done]
    print(f"pages={len(rows)} kept={len(done)} to_verify={len(todo)} model={model} cache={cache}", flush=True)
    parquet_texts = load_parquet_texts(todo, text_column, threads) if any(not r.get("text_path") for r in todo) else {}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lock, results = threading.Lock(), dict(done)
    with out_path.open("w") as handle:
        for rec in done.values():
            handle.write(json.dumps(rec, ensure_ascii=False) + "\n")
        handle.flush()

        def one(row):
            text, url = page_input(row, base, parquet_texts)
            view, info = render_view(text, url)
            rec = {"id": row["id"], **{k: row[k] for k in ("source", "stratum") if row.get(k)}, "url": url, **info}
            try:
                rec.update(verify_view(view, model, cache, version=version, truncated=info["truncated"]))
            except Exception as e:
                rec["error"] = f"{type(e).__name__}: {e}"[:500]
            with lock:
                handle.write(json.dumps(rec, ensure_ascii=False) + "\n")
                handle.flush()
            return rec

        t0 = time.time()
        with ThreadPoolExecutor(threads) as pool:
            for i, future in enumerate(as_completed([pool.submit(one, r) for r in todo]), 1):
                rec = future.result()
                results[rec["id"]] = rec
                if "error" in rec:
                    print(f"FAILED {rec['id']}: {rec['error']}", flush=True)
                if i % 50 == 0 or i == len(todo):
                    print(f"{i}/{len(todo)} done, {time.time() - t0:.0f}s", flush=True)
    records = [results[r["id"]] for r in rows if r["id"] in results]
    summary = summarize(records)
    summary.update(model=model, prompt=version, thinking_level=os.environ.get("GEMINI_THINKING_LEVEL", ""), input_rows=len(rows),
                   threads=threads, wall_seconds=round(time.time() - t0, 1))
    Path(str(out_path) + ".usage.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tsv", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--threads", type=int, default=int(os.environ.get("THREADS", 16)))
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="verify only the first N rows")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--prompt", choices=sorted(PROMPT_PATHS), default="v1")
    args = parser.parse_args()
    rows = read_rows(args.tsv)
    if args.limit:
        rows = rows[:args.limit]
    records = run(rows, args.tsv.resolve().parent, args.out, args.threads, args.resume, args.text_column,
                  version=args.prompt)
    sys.exit(1 if any("error" in r for r in records) else 0)


if __name__ == "__main__":
    main()
