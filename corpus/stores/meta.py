#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

LOOKUP_BATCH = 200
BASE = [
    ("store", pa.string()), ("app_id", pa.string()), ("kind", pa.string()), ("storefront", pa.string()),
    ("request_url", pa.string()), ("final_url", pa.string()), ("http_status", pa.int32()), ("fetched_at", pa.string()),
    ("content_type", pa.string()), ("response_headers", pa.string()), ("error", pa.string()),
    ("attempts", pa.int32()), ("elapsed_ms", pa.int64()), ("page_html", pa.string()),
]
RATE_DEFAULTS = {"android": dict(start=60.0, floor=5.0, ceiling=200.0, workers=64),
                 "apple": dict(start=2.5, floor=0.5, ceiling=5.0, workers=8)}
HREF_RE = re.compile(r"hreflang=['\"][A-Za-z]{2,3}-([A-Za-z]{2})['\"]")
APPLE_SF_RE = re.compile(r"https?://apps\.apple\.com/([a-z]{2})/")


def schema_for(store):
    raw = pa.list_(pa.string()) if store == "android" else pa.string()
    return pa.schema(BASE + [("data_raw", raw), ("data_raw_sha256", pa.string()), ("data_raw_bytes", pa.int64())])


def alt_storefront(store, entry_xml):
    rx = HREF_RE if store == "android" else APPLE_SF_RE
    for m in rx.finditer(entry_xml or ""):
        code = m.group(1).upper()
        if code != "US":
            return code
    return None


def request_url(store, kind, app_id, sf):
    if store == "android":
        page = "details" if kind == "details" else "datasafety"
        return f"https://play.google.com/store/apps/{page}?id={app_id}&hl=en&gl={sf}"
    return f"https://apps.apple.com/{sf.lower()}/app/id{app_id}"


def base_row(store, app_id, kind, sf, url, res):
    return {
        "store": store, "app_id": app_id, "kind": kind, "storefront": sf, "request_url": url,
        "final_url": res["final_url"], "http_status": res["status"], "fetched_at": C.now_iso(),
        "content_type": res["content_type"], "response_headers": json.dumps(res["headers"], ensure_ascii=False),
        "error": res["error"], "attempts": res["attempts"], "elapsed_ms": res["elapsed_ms"], "page_html": None,
        "data_raw": None, "data_raw_sha256": None, "data_raw_bytes": None,
    }


def set_payload(row, data):
    row["data_raw"] = data
    row["data_raw_sha256"] = C.sha256_payload(data)
    row["data_raw_bytes"] = C.payload_bytes(data)


def fetch_page(task, store, mode):
    app_id, kind, sf = task
    url = request_url(store, kind, app_id, sf)
    res = C.fetch(url, timeout=30, max_attempts=4, max_bytes=60_000_000)
    row = base_row(store, app_id, kind, sf, url, res)
    if res["content"] and res["status"] == 200:
        html = C.decode_html(res["content"])
        if mode == "full":
            if kind == "datasafety":
                row["page_html"] = html
            else:
                set_payload(row, C.google_af_args(html) if store == "android" else C.apple_serialized_data(html))
        else:
            if mode != "pilot_no_html":
                row["page_html"] = html
            set_payload(row, C.google_af_args(html) if store == "android" else C.apple_serialized_data(html))
    return [row]


def fetch_lookup(ids, sf, store):
    url = f"https://itunes.apple.com/lookup?id={','.join(ids)}&country={sf.lower()}"
    res = C.fetch(url, timeout=60, max_attempts=4, max_bytes=100_000_000, headers={"Accept": "application/json"})
    by_id = {}
    if res["status"] == 200 and res["content"]:
        text = res["content"].decode("utf-8", errors="replace")
        try:
            for raw in C.raw_json_objects(text, "results"):
                tid = json.loads(raw).get("trackId")
                if tid is not None:
                    by_id[str(tid)] = raw
        except Exception as e:
            res["error"] = f"lookup parse {type(e).__name__}: {e}"[:500]
    rows = []
    for i in ids:
        row = base_row(store, i, "lookup", sf, url, res)
        set_payload(row, by_id.get(i))
        rows.append(row)
    return rows


def enc(status, error, has_payload):
    return (status or 0) * 4 + (2 if has_payload else 0) + (1 if error else 0)


def v_status(v): return v >> 2
def v_has(v): return bool(v & 2)


def load_alt(entries_dir, needed, store):
    out, left = {}, set(needed)
    for p in C.list_shards(entries_dir):
        if not left:
            break
        for b in pq.ParquetFile(p).iter_batches(batch_size=2000, columns=["app_id", "entry_xml"]):
            for i, e in zip(b.column("app_id").to_pylist(), b.column("entry_xml").to_pylist()):
                if i in left:
                    left.discard(i)
                    sf = alt_storefront(store, e)
                    if sf:
                        out[i] = sf
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("store", choices=C.STORES)
    ap.add_argument("ids_parquet", help="table with an app_id column (file or folder of shards), e.g. <store>/ids or <store>/sample")
    ap.add_argument("--full", action="store_true", help="one payload per kind (see above); default is pilot mode")
    ap.add_argument("--no-page-html", action="store_true", help="pilot mode without page_html")
    ap.add_argument("--no-other-storefronts", action="store_true", help="skip the non-US retries")
    ap.add_argument("--entries", default=None, help="ids table with entry_xml (default <data-dir>/<store>/ids)")
    ap.add_argument("--workers", type=int, default=None, help="threads (default android 64, apple 8)")
    ap.add_argument("--rate-start", type=float, default=None, help="requests/s at start (android 60, apple 2.5)")
    ap.add_argument("--rate-floor", type=float, default=None, help="lowest rate (android 5, apple 0.5)")
    ap.add_argument("--rate-ceiling", type=float, default=None, help="highest rate (android 200, apple 5)")
    ap.add_argument("--rate-window", type=int, default=200, help="attempts per rate decision")
    ap.add_argument("--rate-threshold", type=float, default=0.01, help="share of 429s in a window that cuts the rate")
    ap.add_argument("--shuffle-seed", type=int, default=None, help="visit ids in a seeded random order, so partial results are a random sample")
    ap.add_argument("--zstd-level", type=int, default=9)
    ap.add_argument("--flush-seconds", type=float, default=600)
    ap.add_argument("--limit", type=int, default=None, help="smoke test: only the first K ids")
    ap.add_argument("--no-retry-failed", action="store_true", help="treat failed rows as finished")
    ap.add_argument("--log-every", type=int, default=500, help="progress line every K responses")
    C.add_data_dir(ap)
    a = ap.parse_args()
    t0 = time.time()
    store = a.store
    d = RATE_DEFAULTS[store]
    workers = a.workers or d["workers"]
    lim = C.set_limiter(a.rate_start or d["start"], a.rate_floor or d["floor"], a.rate_ceiling or d["ceiling"], a.rate_window,
                        a.rate_threshold)
    C.ZSTD_LEVEL = a.zstd_level
    C.install_stop_handlers()
    mode = "full" if a.full else ("pilot_no_html" if a.no_page_html else "pilot")
    sdir = C.store_dir(a.data_dir, store)
    out_dir = sdir / "meta"
    entries_dir = a.entries or (sdir / "ids")
    ids = list(dict.fromkeys(C.column_values(a.ids_parquet, "app_id")))
    if a.shuffle_seed is not None:
        import random
        random.Random(a.shuffle_seed).shuffle(ids)
    if a.limit:
        ids = ids[: a.limit]

    latest: dict = {}
    cols = ["app_id", "kind", "storefront", "http_status", "error", "data_raw_sha256"]
    for _, t in C.read_columns(out_dir, cols):
        for i, k, sf, s, e, h in zip(*(t.column(c).to_pylist() for c in cols)):
            latest[(i, k, sf or "US")] = enc(s, e, h is not None)
    C.log(f"{store}: {len(ids)} ids, {len(latest)} rows already present, mode {mode}, workers {workers}, "
          f"rate {lim.rate}/s (floor {lim.floor}, ceiling {lim.ceiling})")

    def finished(i, k, sf):
        v = latest.get((i, k, sf))
        if v is None:
            return False
        if a.no_retry_failed:
            return True
        st = v_status(v)
        return not ((v & 1) or st == 0 or st in C.RETRY_STATUS)

    writer = C.ShardWriter(out_dir, schema_for(store), level=a.zstd_level)
    stats, state = Counter(), {"responses": 0, "ok": 0}
    t_start = time.time()

    def fn(task):
        kind, payload = task
        return fetch_lookup(*payload, store) if kind == "lookup" else fetch_page(payload, store, mode)

    def handle(task, res):
        if isinstance(res, Exception):
            stats[f"worker_exception:{type(res).__name__}"] += 1
            C.log(f"worker exception on {task[0]}: {res!r}")
            return
        for row in res:
            writer.add(row)
            latest[(row["app_id"], row["kind"], row["storefront"])] = enc(
                row["http_status"], row["error"], row["data_raw_sha256"] is not None)
            tag = row["http_status"] if row["http_status"] is not None else (row["error"] or "error").split(":")[0]
            stats[f"{row['kind']}/{row['storefront'] if row['storefront'] != 'US' else 'US'}:{tag}"] += 1
        state["responses"] += 1
        state["ok"] += res[0]["http_status"] == 200
        if state["responses"] % a.log_every == 0:
            el = time.time() - t_start
            w = C.window_delta()
            C.log(f"responses {state['responses']} (ok {state['ok']}), {state['responses'] / el:.2f} req/s, "
                  f"limiter rate {C.current_rate()}/s; last window attempts {w['total']}: 429={w['429']} "
                  f"5xx={w['5xx']} conn_err={w['error']}; status counts {dict(stats)}")

    def tick():
        writer.flush_if_stale(a.flush_seconds)

    def run(tasks, label):
        if C.STOP.is_set():
            return
        C.log(f"{store} phase {label}: {len(tasks)} requests")
        C.run_window(tasks, fn, workers, handle, tick=tick)

    def non_us_rows(kind, want_payload=False):
        out = defaultdict(list)
        for (i, k, sf), v in latest.items():
            if k == kind and sf != "US" and (not want_payload or v_has(v)):
                out[i].append(sf)
        return out

    if store == "android":
        run([("page", (i, "details", "US")) for i in ids if not finished(i, "details", "US")], "details US")
        if not a.no_other_storefronts:
            have_alt = non_us_rows("details")
            need = [i for i in ids if v_status(latest.get((i, "details", "US"), 0)) == 404 and i not in have_alt]
            alt = load_alt(entries_dir, need, store) if need and not C.STOP.is_set() else {}
            for i in need:
                if i in alt:
                    have_alt[i] = [alt[i]]
            run([("page", (i, "details", sf)) for i in ids if i in have_alt for sf in have_alt[i]
                 if v_status(latest.get((i, "details", "US"), 0)) == 404 and not finished(i, "details", sf)],
                f"details non-US ({len(need)} US 404s, {len(alt)} with a region)")
        ok_sf = {}
        for (i, k, sf), v in latest.items():
            if k == "details" and v_status(v) == 200 and (sf == "US" or i not in ok_sf):
                ok_sf[i] = sf
        run([("page", (i, "datasafety", ok_sf[i])) for i in ids
             if i in ok_sf and not finished(i, "datasafety", ok_sf[i])], "datasafety (details 200 only, same region)")
    else:
        pend = [i for i in ids if not finished(i, "lookup", "US")]
        run([("lookup", (pend[j:j + LOOKUP_BATCH], "US")) for j in range(0, len(pend), LOOKUP_BATCH)], "lookup US")
        if not a.no_other_storefronts:
            have_alt = non_us_rows("lookup")
            need = [i for i in ids if (i, "lookup", "US") in latest and v_status(latest[(i, "lookup", "US")]) == 200
                    and not v_has(latest[(i, "lookup", "US")]) and i not in have_alt]
            alt = load_alt(entries_dir, need, store) if need and not C.STOP.is_set() else {}
            by_sf = defaultdict(list)
            for i in ids:
                sfs = [alt[i]] if i in alt else have_alt.get(i, [])
                for sf in sfs:
                    if (i, "lookup", "US") in latest and not v_has(latest[(i, "lookup", "US")]) \
                            and v_status(latest[(i, "lookup", "US")]) == 200 and not finished(i, "lookup", sf):
                        by_sf[sf].append(i)
            run([("lookup", (v[j:j + LOOKUP_BATCH], sf)) for sf, v in sorted(by_sf.items())
                 for j in range(0, len(v), LOOKUP_BATCH)],
                f"lookup non-US ({len(need)} US misses, {len(alt)} with a storefront, {len(by_sf)} countries)")
        hit_sf = {}
        for (i, k, sf), v in latest.items():
            if k == "lookup" and v_has(v) and (sf == "US" or i not in hit_sf):
                hit_sf[i] = sf
        run([("page", (i, "app_page", hit_sf[i])) for i in ids
             if i in hit_sf and not finished(i, "app_page", hit_sf[i])], "app_page (lookup hits only, same storefront)")
    writer.close()

    el = time.time() - t_start
    extra = {}
    if store == "apple":
        looked = [latest[(i, "lookup", "US")] for i in ids if (i, "lookup", "US") in latest and v_status(latest[(i, "lookup", "US")]) == 200]
        miss = sum(1 for v in looked if not v_has(v))
        extra = {"ids_with_us_lookup_response": len(looked), "ids_missing_from_us_lookup": miss,
                 "share_missing_from_us_lookup": round(miss / len(looked), 4) if looked else None}
    C.write_step_report(sdir, "meta", t0, {
        "ids": len(ids), "mode": mode, "rows_written": writer.written_rows, "responses_this_run": state["responses"],
        "status_counts": dict(stats), "requests_per_second": round(state["responses"] / el, 3) if el else None,
        "http_attempts": dict(C.ATTEMPTS), "workers": workers, "limiter": lim.summary(), "zstd_level": a.zstd_level,
        "interrupted": C.STOP.is_set(), "limit": a.limit,
        "request_headers_sent": C.sent_headers() | {"(lookup extra)": "Accept: application/json"}, **extra,
    })
    if C.STOP.is_set():
        sys.exit(143)


if __name__ == "__main__":
    main()
