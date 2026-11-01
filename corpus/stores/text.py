#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import signal
import sys
import time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

import pyarrow as pa

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

SETTINGS = {"include_comments": False, "include_tables": True, "favor_recall": True, "output_format": "txt"}
MAX_CHARS_IN = 8_000_000
SCHEMA = pa.schema([
    ("policy_url", pa.string()), ("extractor", pa.string()), ("settings", pa.string()), ("text", pa.string()),
    ("text_chars", pa.int64()), ("extract_ms", pa.int64()), ("skipped_reason", pa.string()),
])
HTML_TYPES = ("html", "xhtml")
HTML_STARTS = (b"<!doctype html", b"<html", b"<head", b"<body")
PDF_MAX_PAGES = 200
REDO_REASONS = ("no body", "http status", "non-HTML content type")
SURROGATES = re.compile("[\ud800-\udfff]")


def clean(s: str) -> str:
    return SURROGATES.sub("�", s)


def worker_init():
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def charset_of(content_type):
    m = re.search(r"charset\s*=\s*['\"]?([\w.:-]+)", content_type or "", re.I)
    return m.group(1) if m else None


def decode(body: bytes, content_type):
    import codecs
    cs = charset_of(content_type)
    if cs:
        try:
            codecs.lookup(cs)
            return body.decode(cs, errors="replace")
        except (LookupError, UnicodeError):
            pass
    return body.decode("utf-8", errors="replace")


def kind_of(content_type, body: bytes):
    ct = (content_type or "").lower()
    if any(t in ct for t in HTML_TYPES) or body.lstrip()[:200].lower().startswith(HTML_STARTS):
        return "html"
    if body[:5] == b"%PDF-" or "application/pdf" in ct:
        return "pdf"
    if "text/plain" in ct:
        return "plain"
    return None


def extractable(status, ctype, body) -> bool:
    return bool(body) and status is not None and 200 <= status < 300 and kind_of(ctype, body) is not None


def pdf_text(body: bytes) -> str:
    import io, logging
    import pypdf
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    pages = pypdf.PdfReader(io.BytesIO(body)).pages[:PDF_MAX_PAGES]
    return "\n".join(p.extract_text() or "" for p in pages).strip()


def work(args):
    import trafilatura
    url, ctype, status, body = args
    ext = f"trafilatura {trafilatura.__version__}"
    base = {"policy_url": url, "extractor": ext, "settings": json.dumps(SETTINGS), "text": None,
            "text_chars": None, "extract_ms": 0, "skipped_reason": None}
    if body is None or not len(body):
        base["skipped_reason"] = "no body" + (f" (http {status})" if status else "")
        return base
    if status is None or not 200 <= status < 300:
        base["skipped_reason"] = f"http status {status}"
        return base
    kind = kind_of(ctype, body)
    if kind is None:
        base["skipped_reason"] = f"non-HTML content type: {ctype}"
        return base
    t0 = time.perf_counter()
    try:
        if kind == "html":
            text = trafilatura.extract(decode(body, ctype)[:MAX_CHARS_IN], **SETTINGS) or ""
        elif kind == "plain":
            base.update(extractor="decoded text/plain body", settings="{}")
            text = decode(body, ctype)[:MAX_CHARS_IN].strip()
        else:
            import pypdf
            base.update(extractor=f"pypdf {pypdf.__version__}", settings=json.dumps({"max_pages": PDF_MAX_PAGES}))
            text = pdf_text(body)
    except Exception as e:
        base["skipped_reason"] = clean(f"extract error {type(e).__name__}: {e}"[:300])
        return base
    text = clean(text)
    base.update(text=text, text_chars=len(text), extract_ms=int((time.perf_counter() - t0) * 1000))
    return base


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("store", nargs="?", default="shared", choices=C.SETS, help="set holding policies/ (default shared)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--no-resume", action="store_true", help="re-extract everything into a fresh text folder")
    ap.add_argument("--zstd-level", type=int, default=9)
    ap.add_argument("--flush-seconds", type=float, default=600)
    C.add_data_dir(ap)
    a = ap.parse_args()
    t0 = time.time()
    C.ZSTD_LEVEL = a.zstd_level
    C.install_stop_handlers()
    sdir = C.store_dir(a.data_dir, a.store)
    out_dir = sdir / "text"
    if a.no_resume and out_dir.exists():
        import shutil
        shutil.rmtree(out_dir)
    done, redo = set(), set()
    for _, t in C.read_columns(out_dir, ["policy_url", "text_chars", "skipped_reason"]):
        for u, n, why in zip(*(t.column(c).to_pylist() for c in ("policy_url", "text_chars", "skipped_reason"))):
            if n is None and (why or "").startswith(REDO_REASONS) and u not in done:
                redo.add(u)
            else:
                done.add(u)
                redo.discard(u)

    def gen():
        for _, t in C.read_columns(sdir / "policies", ["policy_url", "content_type", "http_status", "body"]):
            for u, ctype, status, body in zip(*(t.column(c).to_pylist() for c in ("policy_url", "content_type", "http_status", "body"))):
                if u in done or (u in redo and not extractable(status, ctype, body)):
                    continue
                yield u, ctype, status, body

    writer = C.ShardWriter(out_dir, SCHEMA, level=a.zstd_level)
    stats, n = Counter(), 0
    with Pool(a.workers, maxtasksperchild=500, initializer=worker_init) as pool:
        for res in pool.imap_unordered(work, gen(), chunksize=4):
            writer.add(res)
            writer.flush_if_stale(a.flush_seconds)
            if C.STOP.is_set():
                break
            n += 1
            stats["skipped" if res["text"] is None else ("under_100_chars" if res["text_chars"] < 100 else "ok")] += 1
            if n % 500 == 0:
                C.log(f"text done {n}, {dict(stats)}")
    writer.close()
    C.write_step_report(sdir, "text", t0, {"processed_this_run": n, "stats": dict(stats), "workers": a.workers,
                                           "interrupted": C.STOP.is_set()})
    if C.STOP.is_set():
        sys.exit(143)


if __name__ == "__main__":
    main()
