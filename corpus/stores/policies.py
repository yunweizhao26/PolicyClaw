#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import Counter, deque
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit

import pyarrow as pa

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

BODY_CAP = 20 * 1024 * 1024
BIG_HOSTS = ("sites.google.com,docs.google.com,drive.google.com,github.com,www.termsfeed.com,"
             "www.freeprivacypolicy.com,www.privacypolicies.com,www.iubenda.com,doc-hosting.flycricket.io,"
             "www.notion.so,privacy-policy.courses.store,telegra.ph")
PERMANENT_MARKERS = ("NameResolutionError", "gaierror", "Name or service not known", "Temporary failure in name resolution",
                     "SSLError", "CERTIFICATE_VERIFY_FAILED", "certificate verify failed", "InvalidURL", "not an absolute")
SCHEMA = pa.schema([
    ("policy_url", pa.string()), ("final_url", pa.string()), ("redirect_chain", pa.string()),
    ("http_status", pa.int32()), ("content_type", pa.string()), ("headers", pa.string()),
    ("fetched_at", pa.string()), ("body", pa.binary()), ("body_bytes", pa.int64()), ("body_sha256", pa.string()),
    ("error", pa.string()),
    ("attempts", pa.int32()), ("elapsed_ms", pa.int64()),
])


def host_of(url: str) -> str:
    try:
        return (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def download(url: str) -> dict:
    row = {"policy_url": url, "final_url": None, "redirect_chain": "[]", "http_status": None, "content_type": None,
           "headers": "{}", "fetched_at": C.now_iso(), "body": None, "body_bytes": None, "body_sha256": None, "error": None,
           "attempts": 0, "elapsed_ms": 0}
    if urlsplit(url).scheme not in ("http", "https") or not host_of(url):
        row["error"] = "not an absolute http(s) URL"
        return row
    r = C.fetch(url, timeout=20, max_attempts=4, conn_attempts=2, retry_dns=False, max_bytes=BODY_CAP, deadline_s=90,
                headers={"Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8"})
    row.update({
        "final_url": r["final_url"], "redirect_chain": json.dumps(r["history"] + ([r["final_url"]] if r["final_url"] else [])),
        "http_status": r["status"], "content_type": r["content_type"],
        "headers": json.dumps(r["headers"], ensure_ascii=False), "body": r["content"],
        "body_bytes": len(r["content"]), "body_sha256": C.sha256_payload(r["content"]), "error": r["error"], "attempts": r["attempts"], "elapsed_ms": r["elapsed_ms"],
    })
    return row


def needs_retry(status, error):
    if status in C.RETRY_STATUS:
        return True
    return status is None and bool(error) and not any(m in error for m in PERMANENT_MARKERS)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("links", nargs="+", help="links tables (folders or files), e.g. data/android/links data/apple/links")
    ap.add_argument("--workers", type=int, default=256, help="global concurrency (threads)")
    ap.add_argument("--per-host", type=int, default=4, help="concurrent requests per host")
    ap.add_argument("--per-host-big", type=int, default=16, help="concurrent requests per host listed in --big-hosts")
    ap.add_argument("--big-hosts", default=BIG_HOSTS, help="comma-separated hosts that get --per-host-big")
    ap.add_argument("--zstd-level", type=int, default=9)
    ap.add_argument("--flush-seconds", type=float, default=600)
    ap.add_argument("--limit", type=int, default=None, help="smoke test: only the first K distinct URLs")
    ap.add_argument("--no-retry-failed", action="store_true")
    ap.add_argument("--retry-max-fetches", type=int, default=3, help="fetch a failing URL at most this many times in all")
    ap.add_argument("--retry-min-hours", type=float, default=12, help="refetch a failing URL only when its last fetch is this old")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--log-every", type=int, default=500)
    C.add_data_dir(ap)
    a = ap.parse_args()
    t0 = time.time()
    C.ZSTD_LEVEL = a.zstd_level
    C.install_stop_handlers()
    big = {h.strip().lower() for h in a.big_hosts.split(",") if h.strip()}
    sdir = C.store_dir(a.data_dir, "shared")
    out_dir = sdir / "policies"

    per_table = [[u for u in C.column_values(l, "policy_url") if u] for l in a.links]
    all_urls = [u for t in per_table for u in t]
    in_several = sum(1 for u, n in Counter(x for t in per_table for x in set(t)).items() if n > 1)
    urls = list(dict.fromkeys(all_urls))
    if a.limit:
        urls = urls[: a.limit]
    last, n_fetches = {}, Counter()
    for _, t in C.read_columns(out_dir, ["policy_url", "http_status", "error", "fetched_at"]):
        for u, s, e, ts in zip(*(t.column(c).to_pylist() for c in ("policy_url", "http_status", "error", "fetched_at"))):
            n_fetches[u] += 1
            if u not in last or (ts or "") >= last[u][2]:
                last[u] = (s, e, ts or "")
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=a.retry_min_hours)).isoformat(timespec="seconds")
    done = {u for u, (s, e, ts) in last.items()
            if a.no_retry_failed or not needs_retry(s, e) or n_fetches[u] >= a.retry_max_fetches or ts > cutoff}
    n_retry = sum(1 for u in urls if u in last and u not in done)
    todo = [u for u in urls if u not in done]
    random.Random(a.seed).shuffle(todo)
    C.log(f"{len(all_urls)} links, {len(urls)} distinct policy URLs, {len(done & set(urls))} finished, {len(todo)} to fetch "
          f"({n_retry} of them refetches of failed URLs)")

    queues: dict[str, deque] = {}
    for u in todo:
        queues.setdefault(host_of(u), deque()).append(u)
    hosts = deque(queues)
    in_host: Counter = Counter()
    writer = C.ShardWriter(out_dir, SCHEMA, level=a.zstd_level)
    stats: Counter = Counter()
    n_done, t_start = 0, time.time()

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        pending: dict = {}
        while True:
            progressed = True
            while len(pending) < a.workers and progressed and not C.STOP.is_set():
                progressed = False
                for _ in range(len(hosts)):
                    h = hosts[0]
                    hosts.rotate(-1)
                    if queues[h] and in_host[h] < (a.per_host_big if h in big else a.per_host):
                        u = queues[h].popleft()
                        in_host[h] += 1
                        pending[ex.submit(download, u)] = (u, h)
                        progressed = True
                        if len(pending) >= a.workers:
                            break
                hosts = deque(h for h in hosts if queues[h] or in_host[h])
            if not pending:
                break
            if C.STOP.is_set():
                for f in [f for f in pending if f.cancel()]:
                    u_, h_ = pending.pop(f)
                    in_host[h_] -= 1
                if not pending:
                    break
            done_f, _ = wait(pending, timeout=5, return_when=FIRST_COMPLETED)
            writer.flush_if_stale(a.flush_seconds)
            for f in done_f:
                u, h = pending.pop(f)
                in_host[h] -= 1
                try:
                    row = f.result()
                except C.Interrupted:
                    continue
                except Exception as e:
                    stats[f"worker_exception:{type(e).__name__}"] += 1
                    continue
                writer.add(row)
                n_done += 1
                stats[row["http_status"] if row["http_status"] is not None else (row["error"] or "error").split(":")[0]] += 1
                if n_done % a.log_every == 0:
                    d = C.window_delta()
                    C.log(f"policies done {n_done}/{len(todo)}, {n_done / (time.time() - t_start):.2f} req/s; last window attempts "
                          f"{d['total']}: 429={d['429']} 5xx={d['5xx']} conn_err={d['error']}; {dict(stats)}")
    writer.close()
    C.write_step_report(sdir, "policies", t0, {
        "links_total": len(all_urls), "distinct_urls": len(urls),
        "urls_in_more_than_one_links_table": in_several, "http_attempts": dict(C.ATTEMPTS), "request_headers_sent": C.sent_headers(), "fetched_this_run": n_done, "status_counts": {str(k): v for k, v in stats.items()},
        "workers": a.workers, "per_host": a.per_host, "per_host_big": a.per_host_big, "big_hosts": sorted(big),
        "zstd_level": a.zstd_level, "interrupted": C.STOP.is_set(), "limit": a.limit, "refetches_of_failed_urls": n_retry,
        "retry_max_fetches": a.retry_max_fetches, "retry_min_hours": a.retry_min_hours,
    })
    if C.STOP.is_set():
        sys.exit(143)


if __name__ == "__main__":
    main()
