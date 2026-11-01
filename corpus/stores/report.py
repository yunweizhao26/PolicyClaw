#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

STEPS = ["sitemaps", "sample", "meta", "links"]
SHARED_STEPS = ["policies", "text"]


def load_json(p):
    p = Path(p)
    return json.loads(p.read_text()) if p.exists() else None


def parse_time_log(p):
    p = Path(p)
    if not p.exists():
        return None
    txt = p.read_text()

    def num(pat):
        m = re.search(pat + r":\s*([\d:.]+)", txt)
        return m.group(1) if m else None

    wall = num(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\)")
    secs = None
    if wall:
        parts = [float(x) for x in wall.split(":")]
        secs = sum(v * 60 ** i for i, v in enumerate(reversed(parts)))
    rss = num(r"Maximum resident set size \(kbytes\)")
    return {"wall_s": secs, "user_cpu_s": float(num(r"User time \(seconds\)") or 0),
            "sys_cpu_s": float(num(r"System time \(seconds\)") or 0),
            "peak_rss_gb": round(int(rss) / 1024 / 1024, 2) if rss else None}


def compressed_size(table: pa.Table) -> int:
    buf = io.BytesIO()
    pq.write_table(table, buf, compression="zstd", compression_level=C.ZSTD_LEVEL)
    return buf.tell()


def storage_per_kind(meta_dir, store, per_kind=500):
    got: dict[str, dict] = {}
    for p in C.list_shards(meta_dir):
        pf = pq.ParquetFile(p)
        for batch in pf.iter_batches(batch_size=100, columns=["kind", "page_html", "data_raw"]):
            t = pa.Table.from_batches([batch])
            for k in set(t.column("kind").to_pylist()):
                g = got.setdefault(k, {"rows": 0, "html": [], "raw": []})
                if g["rows"] >= per_kind:
                    continue
                sub = t.filter(pa.compute.equal(t.column("kind"), k))
                g["rows"] += sub.num_rows
                g["html"].append(sub.select(["page_html"]))
                g["raw"].append(sub.select(["data_raw"]))
    out = {}
    for k, g in got.items():
        n = g["rows"]
        ent = {"sampled_rows": n}
        for col, key in (("html", "page_html"), ("raw", "data_raw")):
            tb = pa.concat_tables(g[col])
            nonnull = n - tb.column(0).null_count
            ent[key] = {"rows_with_value": nonnull,
                        "compressed_bytes_per_row": round(compressed_size(tb) / n, 1) if n else None,
                        "raw_bytes_per_row": round(tb.nbytes / n, 1) if n else None}
        out[k] = ent
    return out


def dup_stats(sha, size):
    seen, saved, n, in_dup = {}, 0, 0, 0
    cnt = Counter(h for h in sha if h)
    for h, b in zip(sha, size):
        if not h:
            continue
        n += 1
        if h in seen:
            saved += b or 0
        else:
            seen[h] = b
    in_dup = sum(c for c in cnt.values() if c > 1)
    total = sum(b or 0 for h, b in zip(sha, size) if h)
    return {"rows_with_payload": n, "distinct_payloads": len(cnt), "rows_in_identical_groups": in_dup,
            "share_rows_in_identical_groups": round(in_dup / n, 4) if n else None,
            "payload_bytes_total": total, "bytes_saved_by_storing_distinct_once": saved,
            "share_bytes_saved": round(saved / total, 4) if total else None}


def recompress_experiment(directory, host_col=None):
    shards = C.list_shards(directory)
    if not shards:
        return None
    p = shards[0]
    t = pq.read_table(p)
    out = {"shard": p.name, "rows": t.num_rows, "on_disk_bytes": p.stat().st_size, "uncompressed_bytes": t.nbytes}

    def size(tb, level):
        buf = io.BytesIO()
        pq.write_table(tb, buf, compression="zstd", compression_level=level, row_group_size=500)
        return buf.tell()

    for lv in (3, 9, 19):
        out[f"zstd{lv}"] = size(t, lv)
    if host_col and host_col in t.column_names:
        import pyarrow.compute as pc
        hosts = [host(u or "") for u in t.column(host_col).to_pylist()]
        order = sorted(range(len(hosts)), key=hosts.__getitem__)
        ts = t.take(pa.array(order))
        for lv in (9, 19):
            out[f"zstd{lv}_sorted_by_{host_col}_host"] = size(ts, lv)
    return out


def host(u):
    try:
        return (urlsplit(u).hostname or "").lower()
    except ValueError:
        return ""


def build(store, data_dir, population_override, per_kind):
    sdir = Path(data_dir) / store
    R: dict = {"store": store, "data_dir": str(data_dir)}
    sm = load_json(sdir / "reports/sitemaps.json") or {}
    pop = sm.get("ids_found")
    partial = bool(sm.get("max_sitemaps"))
    if partial and sm.get("sub_sitemaps_processed_total") and sm.get("sub_sitemaps_listed_in_index"):
        est = pop / sm["sub_sitemaps_processed_total"] * sm["sub_sitemaps_listed_in_index"]
    else:
        est = pop
    if population_override:
        est = population_override
    R["sitemaps"] = {"ids_found": pop, "sub_sitemaps_listed": sm.get("sub_sitemaps_listed_in_index"),
                     "sub_sitemaps_processed": sm.get("sub_sitemaps_processed_total"), "partial_run": partial,
                     "population_used_for_extrapolation": round(est) if est else None,
                     "population_note": "scaled from a partial sitemap run" if partial else "full sitemap run"}

    cols = ["app_id", "kind", "http_status", "error", "attempts", "elapsed_ms", "data_raw_sha256", "data_raw_bytes"]
    latest: dict[tuple, tuple] = {}
    for _, t in C.read_columns(sdir / "meta", cols + ["storefront"]):
        sfs = t.column("storefront").to_pylist() if "storefront" in t.column_names else ["US"] * t.num_rows
        for r, sf in zip(zip(*(t.column(c).to_pylist() for c in cols)), sfs):
            latest[(r[0], r[1], sf or "US")] = r[2:]
    apps = {k[0] for k in latest}
    dup_by_kind = {}
    for kind in sorted({k[1] for k in latest}):
        vals = [v for (a_, k_, _sf), v in latest.items() if k_ == kind]
        dup_by_kind[kind] = dup_stats([v[4] for v in vals], [v[5] for v in vals])
    by_kind: dict[str, Counter] = {}
    fail_types: Counter = Counter()
    for (a, k, _sf), (s, e, att, ms, _h, _b) in latest.items():
        by_kind.setdefault(k, Counter())[str(s) if s is not None else "no response"] += 1
        if e:
            fail_types[e.split(":")[0]] += 1
    mrep = load_json(sdir / "reports/meta.json") or {}
    if store == "apple":
        lk = [v for (a_, k_, sf_), v in latest.items() if k_ == "lookup" and sf_ == "US" and v[0] == 200]
        R["lookup_coverage"] = {"ids_with_lookup_response": len(lk),
                                "ids_missing_from_us_lookup": sum(1 for v in lk if v[4] is None),
                                "share_missing_from_us_lookup": round(sum(1 for v in lk if v[4] is None) / len(lk), 4) if lk else None}
    else:
        det = [v for (a_, k_, sf_), v in latest.items() if k_ == "details" and sf_ == "US"]
        R["lookup_coverage"] = {"details_responses": len(det), "details_200": sum(1 for v in det if v[0] == 200),
                                "datasafety_fetched_only_when_details_200": True}
    R["meta"] = {
        "apps": len(apps), "responses_by_kind_and_status": {k: dict(v) for k, v in by_kind.items()},
        "share_of_apps_by_kind_and_status": {k: {s: round(n / len(apps), 4) for s, n in v.items()} for k, v in by_kind.items()},
        "identical_payloads_by_kind": dup_by_kind,
        "failure_types": dict(fail_types), "requests_per_second": mrep.get("requests_per_second"),
        "workers": mrep.get("workers"),
        "mean_attempts": round(sum(v[2] for v in latest.values() if v[2]) / max(1, len(latest)), 3),
    }
    page_kind = "details" if store == "android" else "app_page"
    ok_apps = {a for (a, k, _sf), v in latest.items() if k == page_kind and v[0] == 200}

    links = {}
    lp = sdir / "links"
    if lp.exists():
        for _, t in C.read_columns(lp, ["app_id", "policy_url"]):
            links.update(zip(t.column("app_id").to_pylist(), t.column("policy_url").to_pylist()))
    url_apps: Counter = Counter(links.values())
    R["links"] = {
        "apps_in_meta": len(apps), "apps_with_page_200": len(ok_apps), "apps_with_policy_link": len(links),
        "share_of_all_apps": round(len(links) / len(apps), 4) if apps else None,
        "share_of_apps_with_page_200": round(len(links) / len(ok_apps), 4) if ok_apps else None,
        "distinct_policy_urls": len(url_apps),
        "distinct_policy_urls_per_app_with_link": round(len(url_apps) / len(links), 4) if links else None,
        "max_apps_sharing_one_url": max(url_apps.values()) if url_apps else 0,
    }

    shared = Path(data_dir) / "shared"
    pdir, tdir = shared / "policies", shared / "text"
    mine = set(links.values())
    pol: dict[str, tuple] = {}
    for _, t in C.read_columns(pdir, ["policy_url", "http_status", "content_type", "error", "body_bytes", "elapsed_ms", "attempts"]):
        for r in zip(*(t.column(c).to_pylist() for c in t.column_names)):
            if r[0] in mine:
                pol[r[0]] = r[1:]
    stat = Counter(str(v[0]) if v[0] is not None else "no response" for v in pol.values())
    ctype = Counter(((v[1] or "none").split(";")[0].strip().lower()) for v in pol.values())
    perr = Counter(v[2].split(":")[0] for v in pol.values() if v[2])
    txt: dict[str, tuple] = {}
    for _, t in C.read_columns(tdir, ["policy_url", "text_chars", "skipped_reason"]):
        for r in zip(*(t.column(c).to_pylist() for c in t.column_names)):
            if r[0] in mine:
                txt[r[0]] = r[1:]
    extracted = [v[0] for v in txt.values() if v[0] is not None]
    short = [c for c in extracted if c < 100]
    hosts = Counter()
    for a, u in links.items():
        hosts[host(u)] += 1
    mrep_p = load_json(shared / "reports/policies.json") or {}
    R["policies"] = {
        "urls_downloaded": len(pol), "status_distribution": dict(stat), "failure_types": dict(perr),
        "content_types": dict(ctype.most_common(15)),
        "texts_extracted": len(extracted), "skipped_or_non_html": len(txt) - len(extracted),
        "extracted_under_100_chars": len(short),
        "share_under_100_chars_of_extracted": round(len(short) / len(extracted), 4) if extracted else None,
        "share_under_100_chars_of_downloaded": round(len(short) / len(pol), 4) if pol else None,
        "note_js_candidates": "extracted text under 100 characters marks candidates for JavaScript rendering",
        "top_hosts_by_app_count": hosts.most_common(20),
    }

    meta_cb = C.parquet_column_bytes(sdir / "meta")
    pol_cb = C.parquet_column_bytes(pdir)
    txt_cb = C.parquet_column_bytes(tdir)
    n_apps = max(1, len(apps))
    per_kind_sizes = storage_per_kind(sdir / "meta", store, per_kind) if meta_cb["rows"] else {}
    R["storage"] = {
        "meta_total_compressed_bytes": sum(meta_cb["compressed"].values()),
        "meta_compressed_bytes_by_column": meta_cb["compressed"],
        "meta_compressed_bytes_per_app_by_column": {c: round(v / n_apps, 1) for c, v in meta_cb["compressed"].items()},
        "meta_per_kind_sample": per_kind_sizes,
        "policy_body_compressed_bytes_per_policy": round(pol_cb["compressed"].get("body", 0) / max(1, pol_cb["rows"]), 1),
        "policy_table_compressed_bytes_per_policy": round(sum(pol_cb["compressed"].values()) / max(1, pol_cb["rows"]), 1),
        "text_compressed_bytes_per_policy": round(txt_cb["compressed"].get("text", 0) / max(1, txt_cb["rows"]), 1),
    }

    res = {}
    for s in STEPS + SHARED_STEPS:
        sdir_s = shared if s in SHARED_STEPS else sdir
        tl = parse_time_log(sdir_s / "logs" / f"{s}.time")
        rep = load_json(sdir_s / "reports" / f"{s}.json") or {}
        res[s] = {"time_v": tl, "in_process": {k: rep.get(k) for k in ("elapsed_s", "cpu_user_s", "cpu_sys_s", "peak_rss_mb_self", "peak_rss_mb_children")} if rep else None}
    R["resources"] = res

    R["compression_note"] = "recompression test on shared policies and on one meta shard: see pilot_report of the shared set and storage.meta_recompression"
    if meta_cb["rows"]:
        R["storage"]["meta_recompression"] = recompress_experiment(sdir / "meta")

    ex: dict = {"assumptions": [
        "Per-app and per-policy costs measured on this sample hold for the full population (uniform random sample).",
        "Throughput scales only with the same worker counts; a higher request rate would shorten the time but may trigger rate limits.",
        "Distinct policy URLs per app are held at the sample ratio; real dedupe across a larger population is probably better, so policy counts and bytes are upper bounds.",
        "File counts assume shards of 10,000 rows or 512 MB of raw bytes, whichever comes first.",
        "The sitemap step is already full-population; its time is the measured one.",
    ]}
    N = est
    if N and apps:
        m_el = (mrep.get("elapsed_s") or 0) / n_apps
        ex["population_apps"] = round(N)
        ex["meta_time_hours"] = round(m_el * N / 3600, 1)
        comp_app = R["storage"]["meta_compressed_bytes_per_app_by_column"]
        with_html = sum(comp_app.values())
        no_html = with_html - comp_app.get("page_html", 0)
        ex["meta_parquet_tb_with_page_html"] = round(with_html * N / 1e12, 3)
        ex["meta_parquet_tb_without_page_html"] = round(no_html * N / 1e12, 3)
        unc = meta_cb["uncompressed"]
        raw_no_html = (sum(unc.values()) - unc.get("page_html", 0)) / n_apps
        rows_per_app = meta_cb["rows"] / n_apps
        ex["meta_files_without_page_html"] = max(math.ceil(rows_per_app * N / C.SHARD_MAX_ROWS), math.ceil(raw_no_html * N / C.SHARD_MAX_BYTES))
        unc_all = sum(unc.values()) / n_apps
        ex["meta_files_with_page_html"] = max(math.ceil(rows_per_app * N / C.SHARD_MAX_ROWS), math.ceil(unc_all * N / C.SHARD_MAX_BYTES))
        if links and pol:
            urls_total = N * len(url_apps) / n_apps
            p_el = (mrep_p.get("elapsed_s") or 0) / max(1, mrep_p.get("fetched_this_run") or len(pol))
            ex["distinct_policy_urls"] = round(urls_total)
            ex["policies_time_hours"] = round(p_el * urls_total / 3600, 1)
            body_b = pol_cb["compressed"].get("body", 0) / max(1, pol_cb["rows"])
            ex["policies_parquet_tb"] = round(body_b * urls_total / 1e12, 3)
            ex["text_parquet_tb"] = round(R["storage"]["text_compressed_bytes_per_policy"] * urls_total / 1e12, 3)
            unc_p = sum(pol_cb["uncompressed"].values()) / max(1, pol_cb["rows"])
            ex["policies_files"] = max(math.ceil(urls_total / C.SHARD_MAX_ROWS), math.ceil(unc_p * urls_total / C.SHARD_MAX_BYTES))
            ex["text_files"] = math.ceil(urls_total / C.SHARD_MAX_ROWS)
        ex["note"] = "The sitemap step's ids.parquet and work shards add a few hundred files and are excluded here."
    R["extrapolation"] = ex
    return R


def build_shared(data_dir):
    shared = Path(data_dir) / "shared"
    R = {"store": "shared", "data_dir": str(data_dir)}
    sets = {}
    for st in C.STORES:
        lp = Path(data_dir) / st / "links"
        sets[st] = set(C.column_values(lp, "policy_url")) if lp.exists() else set()
    both = sets["android"] & sets["apple"]
    cols = ["policy_url", "http_status", "body_sha256", "body_bytes"]
    rows = {}
    for _, t in C.read_columns(shared / "policies", cols):
        for r in zip(*(t.column(c).to_pylist() for c in t.column_names)):
            rows[r[0]] = r[1:]
    R["policies"] = {
        "distinct_urls_downloaded": len(rows),
        "urls_android": len(sets["android"]), "urls_apple": len(sets["apple"]),
        "urls_linked_from_both_stores": len(both), "fetches_saved_by_cross_store_dedupe": len(both),
        "status_distribution": dict(Counter(str(v[0]) if v[0] is not None else "no response" for v in rows.values())),
        "identical_bodies": dup_stats([v[1] for v in rows.values()], [v[2] for v in rows.values()]),
    }
    R["recompression"] = {
        "policies_shard": recompress_experiment(shared / "policies", host_col="final_url"),
        "text_shard": recompress_experiment(shared / "text"),
    }
    return R


def markdown_shared(R):
    p = R["policies"]
    L = ["# Pilot report: shared policies and text", "", f"Data folder: `{R['data_dir']}`", "",
         f"- distinct URLs downloaded: {p['distinct_urls_downloaded']} (android {p['urls_android']}, apple {p['urls_apple']}, linked from both: {p['urls_linked_from_both_stores']}, so {p['fetches_saved_by_cross_store_dedupe']} fetches saved)",
         f"- status: {p['status_distribution']}",
         f"- identical bodies: {p['identical_bodies']}", "", "## Recompression test (first shard of each table)"]
    for k, v in R["recompression"].items():
        L.append(f"- {k}: {v}")
    return "\n".join(L) + "\n"


def markdown(R):
    s, m, l, p, st, ex = R["sitemaps"], R["meta"], R["links"], R["policies"], R["storage"], R["extrapolation"]
    L = [f"# Pilot report: {R['store']}", "", f"Data folder: `{R['data_dir']}`", "",
         "## Population", f"- ids found in sitemaps: {s['ids_found']} ({s['population_note']}; used for extrapolation: {s['population_used_for_extrapolation']})",
         f"- sub-sitemaps listed/processed: {s['sub_sitemaps_listed']}/{s['sub_sitemaps_processed']}", "",
         "## Store metadata", f"- apps: {m['apps']}; requests per second: {m['requests_per_second']} with {m['workers']} workers; mean attempts {m['mean_attempts']}"]
    for k, v in m["share_of_apps_by_kind_and_status"].items():
        L.append(f"- {k}: " + ", ".join(f"{a}: {b:.1%}" for a, b in v.items()))
    L += [f"- lookup/coverage: {R['lookup_coverage']}", f"- identical payloads (data_raw) by kind: {m['identical_payloads_by_kind']}",
          f"- failure types: {m['failure_types'] or 'none'}", "",
          "## Policy links", f"- apps with a policy link: {l['apps_with_policy_link']} of {l['apps_in_meta']} ({l['share_of_all_apps']}); of apps with a 200 page: {l['share_of_apps_with_page_200']}",
          f"- distinct policy URLs: {l['distinct_policy_urls']} ({l['distinct_policy_urls_per_app_with_link']} per app with a link; most-shared URL used by {l['max_apps_sharing_one_url']} apps)", "",
          "## Policy downloads", f"- URLs downloaded: {p['urls_downloaded']}; status: {p['status_distribution']}",
          f"- failures: {p['failure_types'] or 'none'}", f"- content types: {p['content_types']}",
          f"- texts extracted: {p['texts_extracted']}; skipped (non-HTML or no body): {p['skipped_or_non_html']}; under 100 characters: {p['extracted_under_100_chars']} ({p['share_under_100_chars_of_extracted']} of extracted), candidates for JavaScript rendering",
          "- top hosts by app count: " + ", ".join(f"{h} ({n})" for h, n in p["top_hosts_by_app_count"][:20]), "",
          "## Storage (compressed Parquet; per-kind figures recompressed at zstd 3, the crawl level)"]
    for k, e in st["meta_per_kind_sample"].items():
        L.append(f"- {k} (first {e['sampled_rows']} rows): page_html {e['page_html']['compressed_bytes_per_row']} B/response, data_raw {e['data_raw']['compressed_bytes_per_row']} B/response")
    L += [f"- meta shard recompression (bytes): {st.get('meta_recompression')}"]
    L += [f"- meta per app by column: {st['meta_compressed_bytes_per_app_by_column']}",
          f"- policy body {st['policy_body_compressed_bytes_per_policy']} B/policy; policy table {st['policy_table_compressed_bytes_per_policy']} B/policy; text {st['text_compressed_bytes_per_policy']} B/policy", "",
          "## Resources per step"]
    for step, v in R["resources"].items():
        tv, ip = v["time_v"], v["in_process"]
        L.append(f"- {step}: " + (f"/usr/bin/time wall {tv['wall_s']} s, user {tv['user_cpu_s']} s, sys {tv['sys_cpu_s']} s, peak RSS {tv['peak_rss_gb']} GB" if tv else "no time log")
                 + (f"; in-process elapsed {ip['elapsed_s']} s, cpu {ip['cpu_user_s']}+{ip['cpu_sys_s']} s" if ip else ""))
    L += ["", "## Extrapolation to the full population"] + [f"- {k}: {v}" for k, v in ex.items() if k not in ("assumptions", "note")]
    L += [f"- {ex.get('note', '')}", "", "Assumptions:"] + [f"- {a}" for a in ex["assumptions"]]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("stores", nargs="*", default=list(C.SETS))
    ap.add_argument("--population", type=int, default=None, help="override the population used for extrapolation")
    ap.add_argument("--per-kind", type=int, default=500, help="rows per kind used to measure compressed bytes per column")
    C.add_data_dir(ap)
    a = ap.parse_args()
    for store in a.stores:
        sdir = C.store_dir(a.data_dir, store)
        if store == "shared":
            R = build_shared(a.data_dir)
            md = markdown_shared(R)
        else:
            R = build(store, a.data_dir, a.population, a.per_kind)
            md = markdown(R)
        C.write_json(sdir / "reports" / "pilot_report.json", R)
        (sdir / "reports" / "pilot_report.md").write_text(md, encoding="utf-8")
        C.log(f"{store}: wrote {sdir / 'reports' / 'pilot_report.md'}")


if __name__ == "__main__":
    main()
