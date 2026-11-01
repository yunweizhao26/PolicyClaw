from __future__ import annotations

import argparse, csv, json, statistics, sys, threading, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import sources  # noqa: E402
from rebuild_versions import is_prose, visible_text  # noqa: E402

CDX = "https://web.archive.org/cdx/search/cdx"
RAW = "https://web.archive.org/web/{ts}id_/{url}"
POSITIVE = "complete_policy"
_lock = threading.Lock()
_last = [0.0]


def polite_get(session: requests.Session, url: str, params=None, min_gap: float = 0.5, tries: int = 5):
    for attempt in range(tries):
        with _lock:
            wait = _last[0] + min_gap - time.time()
            if wait > 0:
                time.sleep(wait)
            _last[0] = time.time()
        try:
            r = session.get(url, params=params, timeout=60)
            if r.status_code == 429 or r.status_code >= 500:
                raise requests.HTTPError(str(r.status_code), response=r)
            return r
        except requests.RequestException:
            if attempt == tries - 1:
                raise
            time.sleep(min(60, 5 * 2 ** attempt))


def read_jsonl(path: Path) -> dict:
    return {r["id"]: r for r in (json.loads(l) for l in path.read_text().splitlines() if l.strip())}


def confirmed_pages(d: Path) -> list[dict]:
    rows = list(csv.DictReader((d / "sample.tsv").open(), delimiter="\t"))
    ref = {}
    for path in sorted((d / "labels_adjudicated").glob("*.jsonl")):
        ref.update(read_jsonl(path))
    ver = read_jsonl(d / "verifier_v1_medium.jsonl")
    return [r for r in rows if r["url"] and ref[r["id"]]["label"] == POSITIVE and ver[r["id"]]["label"] == POSITIVE]


def cdx_runs(session, url: str) -> list[list[str]]:
    params = {"url": url, "output": "json", "fl": "timestamp,digest,original", "filter": "statuscode:200",
              "collapse": "digest", "limit": "20000"}
    r = polite_get(session, CDX, params)
    rows = r.json() if r.text.strip() else []
    return rows[1:] if rows else []


def monthly_status(session, url: str) -> Counter:
    params = {"url": url, "output": "json", "fl": "statuscode", "collapse": "timestamp:6", "limit": "5000"}
    r = polite_get(session, CDX, params)
    rows = r.json() if r.text.strip() else []
    return Counter((row[0] or "-")[:1] + "xx" for row in rows[1:])


def spaced(n: int, k: int) -> list[int]:
    if n <= k:
        return list(range(n))
    return sorted({round(i * (n - 1) / (k - 1)) for i in range(k)})


def prose(raw: bytes) -> str:
    return "\n".join(l for l in visible_text(raw).split("\n") if is_prose(l))


def one(page: dict, out: Path, per_url: int, session) -> dict:
    rec = {"id": page["id"], "source": page["source"], "url": page["url"]}
    try:
        runs = cdx_runs(session, page["url"])
        months = monthly_status(session, page["url"])
    except Exception as e:
        return {**rec, "error": f"cdx: {type(e).__name__}: {e}"[:300]}
    rec.update(digest_runs=len(runs), first=runs[0][0] if runs else "", last=runs[-1][0] if runs else "",
               months_by_status=dict(months))
    folder = out / "text" / page["id"]
    folder.mkdir(parents=True, exist_ok=True)
    texts, failed = [], 0
    for i in spaced(len(runs), per_url):
        ts, _, original = runs[i]
        path = folder / f"{ts}.txt"
        if not path.exists():
            try:
                r = polite_get(session, RAW.format(ts=ts, url=original))
                path.write_text(prose(r.content) if r.status_code == 200 else "", encoding="utf-8")
            except Exception:
                failed += 1
                continue
        texts.append((ts, path.read_text(encoding="utf-8")))
    versions, previous = [], None
    for ts, text in texts:
        if text and text != previous:
            versions.append(ts)
            previous = text
    rec.update(downloaded=len(texts), failed=failed, with_prose=sum(1 for _, t in texts if t),
               prose_versions=len(versions), version_starts=versions,
               span_years=round((int(versions[-1][:4]) - int(versions[0][:4])) + (int(versions[-1][4:6]) - int(versions[0][4:6])) / 12, 1) if versions else 0)
    return rec


def population(out: Path):
    stats, urls = {}, {}
    for store in ("gplay", "appstore"):
        folder = sources.STORES[store][0] / "downloads"
        apps = {p.name for p in folder.iterdir() if (p / "clean.txt").is_file()}
        catalog = sources.app_urls(store)
        urls[store] = {catalog.get(a, "") for a in apps} - {""}
        stats[store] = {"apps_with_text": len(apps), "distinct_policy_urls": len(urls[store])}
    stats["urls_in_both_stores"] = len(urls["gplay"] & urls["appstore"])
    (out / "population.json").write_text(json.dumps(stats, indent=2) + "\n")
    print(json.dumps(stats), flush=True)


def summarize(records: list[dict]):
    by = {}
    for r in records:
        by.setdefault(r["source"], []).append(r)
    for src, rs in sorted(by.items()):
        ok = [r for r in rs if "error" not in r]
        archived = [r for r in ok if r["digest_runs"] > 0]
        multi = [r for r in ok if r["prose_versions"] >= 2]
        redirected = [r for r in ok if r["months_by_status"].get("3xx", 0) > r["months_by_status"].get("2xx", 0)]
        vs = [r["prose_versions"] for r in multi]
        print(f"{src}: pages {len(rs)}, errors {len(rs) - len(ok)}, archived {len(archived)}, "
              f"2+ prose versions {len(multi)} ({100 * len(multi) / max(len(ok), 1):.1f}%), "
              f"5+ {sum(1 for r in ok if r['prose_versions'] >= 5)}, "
              f"mostly redirects {len(redirected)}, "
              f"median versions among 2+ {statistics.median(vs) if vs else 0}, "
              f"median digest runs {statistics.median([r['digest_runs'] for r in ok]) if ok else 0}, "
              f"first-capture years {dict(sorted(Counter(r['first'][:4] for r in archived).items()))}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dir", default="confirmation")
    parser.add_argument("--per-url", type=int, default=24)
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()
    d = HERE / args.dir
    out = d / "wayback"
    out.mkdir(exist_ok=True)
    population(out)
    pages = confirmed_pages(d)
    print(f"pages {len(pages)}: {dict(Counter(p['source'] for p in pages))}", flush=True)
    session = requests.Session()
    session.headers["User-Agent"] = "PolicyClaw research crawler (privacy-policy version study)"
    records = []
    with ThreadPoolExecutor(args.threads) as pool, (out / "histories.jsonl").open("w") as handle:
        for i, rec in enumerate(pool.map(lambda p: one(p, out, args.per_url, session), pages), 1):
            records.append(rec)
            handle.write(json.dumps(rec) + "\n")
            handle.flush()
            if i % 25 == 0:
                print(f"{i}/{len(pages)}", flush=True)
    summarize(records)


if __name__ == "__main__":
    main()
