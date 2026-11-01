#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import html
import json
import re
import shutil
import sys
import threading
import time
from concurrent.futures import ProcessPoolExecutor, FIRST_COMPLETED, wait
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

INDEXES = {
    "android": ["https://play.google.com/sitemaps/sitemaps-index-0.xml",
                "https://play.google.com/sitemaps/sitemaps-index-1.xml"],
    "apple": ["https://apps.apple.com/sitemaps_apps_index_app_1.xml"],
}
LOC_RE = re.compile(r"<loc>\s*([^<]+?)\s*</loc>")
URL_RE = re.compile(r"<url>[\s\S]*?</url>")
PLAY_ID_RE = re.compile(r"/store/apps/details\?(?:[^#]*?&)?id=([A-Za-z0-9._]+)")
APPLE_ID_RE = re.compile(r"/id(\d+)(?=[/?#]|$)")

ENTRY_SCHEMA = pa.schema([("app_id", pa.string()), ("first_sitemap", pa.string()), ("entry_xml", pa.string())])
OCC_SCHEMA = pa.schema([("app_id", pa.string()), ("sitemap_url", pa.string())])
IDS_SCHEMA = pa.schema([("store", pa.string()), ("app_id", pa.string()),
                        ("sitemap_urls", pa.list_(pa.string())), ("entry_xml", pa.string())])


def fetch_index(store: str) -> list[str]:
    urls = []
    for u in INDEXES[store]:
        r = C.fetch(u, timeout=60, max_attempts=4, deadline_s=300)
        if r["status"] != 200:
            raise SystemExit(f"index {u} failed: {r['status']} {r['error']}")
        urls += [html.unescape(x) for x in LOC_RE.findall(r["content"].decode("utf-8", "replace"))]
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def parse_sitemap(store: str, xml: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in URL_RE.finditer(xml):
        entry = m.group(0)
        loc = LOC_RE.search(entry)
        if not loc:
            continue
        loc = html.unescape(loc.group(1))
        if store == "android":
            mm = PLAY_ID_RE.search(loc)
        else:
            mm = APPLE_ID_RE.search(loc)
        if mm and mm.group(1) not in out:
            out[mm.group(1)] = entry
    return out


def _init_worker():
    C._local = threading.local()


def work(args):
    store, url = args
    r = C.fetch(url, timeout=60, max_attempts=4, deadline_s=300, max_bytes=400_000_000)
    if r["status"] != 200:
        return url, None, 0, f"status={r['status']} error={r['error']}"
    b = r["content"]
    try:
        b = gzip.decompress(b)
    except OSError:
        pass
    try:
        xml = b.decode("utf-8", "replace")
        return url, parse_sitemap(store, xml), xml.count("<url>"), None
    except Exception as e:
        return url, None, 0, f"parse {type(e).__name__}: {e}"


def finalize(sdir: Path, wdir: Path) -> int:
    log = C.log
    sources: dict[str, list[str]] = {}
    for p in sorted(wdir.glob("occ-*.parquet")):
        if not (wdir / f"done-{p.stem.split('-')[1]}.json").exists():
            continue
        t = pq.read_table(p)
        for a, s in zip(t.column("app_id").to_pylist(), t.column("sitemap_url").to_pylist()):
            sources.setdefault(a, []).append(s)
    new = sdir / "ids.new"
    if new.exists():
        shutil.rmtree(new)
    w = C.ShardWriter(new, IDS_SCHEMA, prefix="part")
    store = sdir.name
    for p in sorted(wdir.glob("entries-*.parquet")):
        if not (wdir / f"done-{p.stem.split('-')[1]}.json").exists():
            continue
        t = pq.read_table(p)
        for a, e in zip(t.column("app_id").to_pylist(), t.column("entry_xml").to_pylist()):
            w.add({"store": store, "app_id": a, "sitemap_urls": sources.get(a, []), "entry_xml": e})
    w.close()
    old = sdir / "ids"
    if old.exists():
        shutil.rmtree(old)
    new.rename(old)
    log(f"finalized ids table: {len(sources)} ids")
    return len(sources)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("store", choices=C.STORES)
    ap.add_argument("--max-sitemaps", type=int, default=None, help="smoke test only: use the first K sub-sitemaps")
    ap.add_argument("--workers", type=int, default=16)
    C.add_data_dir(ap)
    a = ap.parse_args()
    t0 = time.time()
    sdir = C.store_dir(a.data_dir, a.store)
    wdir = sdir / "_sitemaps_work"
    wdir.mkdir(exist_ok=True)

    subs = fetch_index(a.store)
    total_listed = len(subs)
    if a.max_sitemaps:
        subs = subs[: a.max_sitemaps]
    C.log(f"{a.store}: {total_listed} sub-sitemaps listed, processing {len(subs)}")

    done_sm: set[str] = set()
    for p in sorted(wdir.glob("done-*.json")):
        done_sm.update(json.loads(p.read_text())["sitemaps"])
    seen: set[str] = set()
    for p in sorted(wdir.glob("entries-*.parquet")):
        if (wdir / f"done-{p.stem.split('-')[1]}.json").exists():
            seen.update(pq.read_table(p, columns=["app_id"]).column("app_id").to_pylist())
    todo = [u for u in subs if u not in done_sm]
    C.log(f"resume: {len(done_sm)} sub-sitemaps done, {len(seen)} ids known, {len(todo)} to do")

    idx = len([*wdir.glob("done-*.json")])
    ew = C.ShardWriter(wdir, ENTRY_SCHEMA, prefix="entries")
    ow = C.ShardWriter(wdir, OCC_SCHEMA, prefix="occ", max_rows=10**9, max_bytes=10**12)
    buf_done: list[str] = []
    failures: list[dict] = []
    urls_seen_total = 0
    stats = {"processed": 0, "new_ids": 0}

    def flush():
        nonlocal buf_done, idx
        if not buf_done:
            return
        ew.index = ow.index = idx
        ew.flush()
        ow.flush()
        for pref, wr in (("entries", ew), ("occ", ow)):
            f = wdir / f"{pref}-{idx:05d}.parquet"
            if not f.exists():
                pq.write_table(pa.Table.from_pylist([], schema=wr.schema), f, compression="zstd")
        (wdir / f"done-{idx:05d}.json").write_text(json.dumps({"sitemaps": buf_done}))
        idx += 1
        buf_done = []

    ex = ProcessPoolExecutor(max_workers=a.workers, initializer=_init_worker)
    it = iter(todo)
    pending = set()
    last_log = time.time()
    try:
        while True:
            while len(pending) < a.workers * 2:
                u = next(it, None)
                if u is None:
                    break
                pending.add(ex.submit(work, (a.store, u)))
            if not pending:
                break
            done, pending = wait(pending, return_when=FIRST_COMPLETED)
            for f in done:
                try:
                    url, ids, nurl, err = f.result()
                except Exception as e:
                    failures.append({"url": "?", "error": f"worker {type(e).__name__}: {e}"})
                    continue
                if err:
                    failures.append({"url": url, "error": err})
                    continue
                urls_seen_total += nurl
                for aid, entry in ids.items():
                    ow.rows.append({"app_id": aid, "sitemap_url": url})
                    if aid not in seen:
                        seen.add(aid)
                        ew.rows.append({"app_id": aid, "first_sitemap": url, "entry_xml": entry})
                        ew.bytes += len(entry)
                        stats["new_ids"] += 1
                buf_done.append(url)
                stats["processed"] += 1
                if len(ew.rows) >= C.SHARD_MAX_ROWS or ew.bytes >= C.SHARD_MAX_BYTES:
                    flush()
            if time.time() - last_log > 30:
                last_log = time.time()
                C.log(f"sitemaps done {stats['processed']}/{len(todo)}, ids {len(seen)}, failures {len(failures)}")
        flush()
    finally:
        ex.shutdown(wait=True, cancel_futures=True)

    n_ids = finalize(sdir, wdir) if (stats["processed"] or not (sdir / "ids").exists()) else len(seen)
    C.write_step_report(sdir, "sitemaps", t0, {
        "sub_sitemaps_listed_in_index": total_listed, "sub_sitemaps_processed_total": len(done_sm) + stats["processed"],
        "sub_sitemaps_failed": len(failures), "failures": failures[:50],
        "ids_found": n_ids, "url_elements_seen_this_run": urls_seen_total,
        "max_sitemaps": a.max_sitemaps, "workers": a.workers,
    })
    if failures:
        C.log(f"WARNING: {len(failures)} sub-sitemaps failed; rerun to retry them")


if __name__ == "__main__":
    main()
