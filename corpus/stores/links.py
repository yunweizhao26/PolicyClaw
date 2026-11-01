#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

SCHEMA = pa.schema([("store", pa.string()), ("app_id", pa.string()), ("policy_url", pa.string()),
                    ("found_at", pa.string()), ("alternates", pa.string())])

APPLE_PRIMARY = ("data[0].data.shelfMapping.privacyHeader.items[i].bodyText.linkedSubstrings[<label>]"
                 " (the entry whose actionMetrics.data[0].fields.location[0].id == 'privacyPolicy').url")
APPLE_FALLBACK = ("data[0].data.shelfMapping.{purchasedLinks,notPurchasedLinks}.items[i]"
                  " (the item whose clickAction.actionMetrics.data[0].fields.location[0].id == 'LinkToPrivacyPolicy')"
                  ".clickAction.url")


def _get(o, *path):
    for p in path:
        try:
            o = o[p]
        except (KeyError, IndexError, TypeError):
            return None
    return o


def _loc_id(action):
    for d in _get(action, "actionMetrics", "data") or []:
        for loc in _get(d, "fields", "location") or []:
            if isinstance(loc, dict) and loc.get("id"):
                return loc["id"]
    return None


def apple_policy_links(raw_json: str) -> list[tuple[str, str]]:
    j = json.loads(raw_json)
    sm = _get(j, "data", 0, "data", "shelfMapping") or {}
    base = "data[0].data.shelfMapping"
    out = []
    for n, item in enumerate(_get(sm, "privacyHeader", "items") or []):
        subs = _get(item, "bodyText", "linkedSubstrings") or {}
        for label, act in subs.items():
            if isinstance(act, dict) and _loc_id(act) == "privacyPolicy" and act.get("url"):
                out.append((act["url"], f"{base}.privacyHeader.items[{n}].bodyText.linkedSubstrings[{label!r}].url"))
    for shelf in ("purchasedLinks", "notPurchasedLinks"):
        for n, item in enumerate(_get(sm, shelf, "items") or []):
            act = item.get("clickAction") if isinstance(item, dict) else None
            if isinstance(act, dict) and _loc_id(act) == "LinkToPrivacyPolicy" and act.get("url"):
                out.append((act["url"], f"{base}.{shelf}.items[{n}].clickAction.url"))
    return out


def android_policy_link(af_args: list[str]):
    from google_play_scraper.constants.element import ElementSpecs
    from google_play_scraper.constants.regex import Regex
    spec = ElementSpecs.Detail["privacyPolicy"]
    dataset = {}
    for arg in af_args:
        key = Regex.KEY.findall(arg)
        if not key or key[0] != f"ds:{spec.ds_num}":
            continue
        val = Regex.VALUE.findall("AF_initDataCallback(" + arg + ");</script")
        if val:
            dataset[key[0]] = json.loads(val[0])
    url = spec.extract_content(dataset)
    return url, f"ds:{spec.ds_num}{spec.data_map}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("store", choices=C.STORES)
    C.add_data_dir(ap)
    a = ap.parse_args()
    t0 = time.time()
    store = a.store
    sdir = C.store_dir(a.data_dir, store)
    page_kind = "details" if store == "android" else "app_page"
    results: dict[str, tuple] = {}
    fetched_ok, stats = set(), Counter()
    for p, t in C.read_columns(sdir / "meta", ["app_id", "kind", "http_status", "data_raw"]):
        for i, k, s, raw in zip(*(t.column(c).to_pylist() for c in ("app_id", "kind", "http_status", "data_raw"))):
            if k != page_kind:
                continue
            if s != 200 or raw is None:
                stats["page_not_200_or_no_data"] += 1
                results.setdefault(i, (None, None, None))
                continue
            fetched_ok.add(i)
            try:
                if store == "android":
                    url, where = android_policy_link(raw)
                    alts = None
                else:
                    found = apple_policy_links(raw)
                    url, where = found[0] if found else (None, None)
                    alts = json.dumps(found[1:]) if len(found) > 1 else None
            except Exception as e:
                stats[f"parse_error:{type(e).__name__}"] += 1
                url, where, alts = None, None, None
            results[i] = (url.strip() if isinstance(url, str) and url.strip() else None, where if url else None, alts)
    rows = [{"store": store, "app_id": i, "policy_url": u, "found_at": w, "alternates": al}
            for i, (u, w, al) in results.items() if u]
    out = sdir / "links" / "part-00000.parquet"
    out.parent.mkdir(exist_ok=True)
    tmp = out.with_name("." + out.name + ".tmp")
    pq.write_table(pa.Table.from_pylist(rows, schema=SCHEMA), tmp, compression="zstd", compression_level=C.ZSTD_LEVEL)
    tmp.replace(out)
    C.write_step_report(sdir, "links", t0, {
        "apps_with_page_data": len(fetched_ok), "apps_seen": len(results), "apps_with_policy_link": len(rows),
        "distinct_policy_urls": len({r["policy_url"] for r in rows}), "stats": dict(stats),
        "method": ("google_play_scraper ElementSpecs.Detail['privacyPolicy'] = ElementSpec(5, [1, 2, 99, 0, 5, 2])"
                   if store == "android" else {"primary": APPLE_PRIMARY, "fallback": APPLE_FALLBACK}),
    })


if __name__ == "__main__":
    main()
