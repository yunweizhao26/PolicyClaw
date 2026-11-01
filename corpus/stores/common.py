from __future__ import annotations

import hashlib
import json
import os
import random
import re
import resource
import signal
import sys
import threading
import time
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime, timezone
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import requests
from requests.adapters import HTTPAdapter

HERE = Path(__file__).resolve().parent
DEFAULT_DATA = HERE / "data"
STORES = ("android", "apple")
SETS = STORES + ("shared",)
CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)
SHARD_MAX_ROWS = 10_000
SHARD_MAX_BYTES = 512 * 1024 * 1024
ZSTD_LEVEL = 9
RETRY_STATUS = {429} | set(range(500, 600))


def add_data_dir(ap):
    ap.add_argument("--data-dir", default=str(DEFAULT_DATA), help="root folder for outputs")
    return ap


def store_dir(data_dir, store: str) -> Path:
    if store not in SETS:
        raise SystemExit(f"unknown set {store!r}; expected one of {SETS}")
    p = Path(data_dir) / store
    p.mkdir(parents=True, exist_ok=True)
    return p


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log(msg: str) -> None:
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {msg}", flush=True)


def write_json(path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name("." + path.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    tmp.replace(path)


def usage_snapshot() -> dict:
    s = resource.getrusage(resource.RUSAGE_SELF)
    c = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {
        "cpu_user_s": round(s.ru_utime + c.ru_utime, 2),
        "cpu_sys_s": round(s.ru_stime + c.ru_stime, 2),
        "peak_rss_mb_self": round(s.ru_maxrss / 1024, 1),
        "peak_rss_mb_children": round(c.ru_maxrss / 1024, 1),
    }


def write_step_report(sdir: Path, step: str, started: float, extra: dict) -> None:
    rep = {"step": step, "elapsed_s": round(time.time() - started, 2), **usage_snapshot(), **extra}
    write_json(Path(sdir) / "reports" / f"{step}.json", rep)
    log(f"{step} report: {json.dumps(rep, default=str)[:1500]}")


def list_shards(directory) -> list[Path]:
    d = Path(directory)
    if d.is_file():
        return [d]
    return sorted(d.glob("part-*.parquet")) if d.exists() else []


def read_columns(directory, columns):
    for p in list_shards(directory):
        names = set(pq.ParquetFile(p).schema_arrow.names)
        cols = [c for c in columns if c in names]
        yield p, pq.read_table(p, columns=cols)


def column_values(directory, column):
    for _, t in read_columns(directory, [column]):
        if column in t.column_names:
            yield from t.column(column).to_pylist()


STOP = threading.Event()


class Interrupted(Exception):
    pass


def install_stop_handlers() -> None:
    def handler(signum, frame):
        if not STOP.is_set():
            log(f"signal {signum} received: draining in-flight requests, flushing buffered rows, then exiting")
        STOP.set()
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)


class AdaptiveLimiter:

    def __init__(self, start, floor, ceiling, window=200, cut=0.25, up=0.05, threshold=0.01):
        self.rate = float(min(max(start, floor), ceiling))
        self.floor, self.ceiling, self.window = float(floor), float(ceiling), int(window)
        self.cut, self.up, self.threshold = cut, up, threshold
        self._next = 0.0
        self._lock = threading.Lock()
        self._n = self._n429 = 0
        self.min_rate = self.max_rate = self.rate
        self.windows = self.cut_windows = 0
        self.history: list = []

    def acquire(self) -> None:
        with self._lock:
            now = time.monotonic()
            t = max(now, self._next)
            self._next = t + 1.0 / self.rate
        while True:
            wait_s = t - time.monotonic()
            if wait_s <= 0:
                return
            if STOP.is_set():
                raise Interrupted()
            time.sleep(min(wait_s, 0.5))

    def record(self, status) -> None:
        with self._lock:
            self._n += 1
            self._n429 += status == 429
            if self._n < self.window:
                return
            frac = self._n429 / self._n
            old = self.rate
            if frac > self.threshold:
                self.rate = max(self.floor, self.rate * (1 - self.cut))
                self.cut_windows += 1
            else:
                self.rate = min(self.ceiling, self.rate * (1 + self.up))
            self.windows += 1
            self.min_rate, self.max_rate = min(self.min_rate, self.rate), max(self.max_rate, self.rate)
            if len(self.history) < 2000 and (self.rate != old or self.windows % 20 == 0):
                self.history.append([now_iso(), round(frac, 4), round(old, 2), round(self.rate, 2)])
            self._n = self._n429 = 0

    def summary(self) -> dict:
        return {"final_rate": round(self.rate, 2), "min_rate": round(self.min_rate, 2), "max_rate": round(self.max_rate, 2),
                "windows": self.windows, "windows_with_cut": self.cut_windows, "window_attempts": self.window,
                "floor": self.floor, "ceiling": self.ceiling, "history_tail": self.history[-30:]}


LIMITER: AdaptiveLimiter | None = None


def set_limiter(start, floor, ceiling, window=200, threshold=0.01) -> AdaptiveLimiter:
    global LIMITER
    LIMITER = AdaptiveLimiter(start, floor, ceiling, window, threshold=threshold)
    return LIMITER


def current_rate():
    return round(LIMITER.rate, 2) if LIMITER else None


def _row_bytes(row: dict) -> int:
    n = 64
    for v in row.values():
        if isinstance(v, (str, bytes)):
            n += len(v)
        elif isinstance(v, list):
            n += sum(len(x) for x in v if isinstance(x, (str, bytes)))
    return n


class ShardWriter:

    def __init__(self, directory, schema: pa.Schema, max_rows=SHARD_MAX_ROWS, max_bytes=SHARD_MAX_BYTES,
                 prefix="part", row_group_size=500, level=None):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.schema, self.max_rows, self.max_bytes = schema, max_rows, max_bytes
        self.prefix, self.rgs = prefix, row_group_size
        self.rows: list[dict] = []
        self.bytes = 0
        existing = [int(p.stem.split("-")[1]) for p in self.dir.glob(f"{prefix}-*.parquet")]
        self.index = max(existing) + 1 if existing else 0
        self.written_rows = 0
        self.level = ZSTD_LEVEL if level is None else level
        self.last_flush = time.monotonic()

    def flush_if_stale(self, seconds=600) -> None:
        if self.rows and time.monotonic() - self.last_flush >= seconds:
            self.flush()

    def add(self, row: dict) -> None:
        self.rows.append(row)
        self.bytes += _row_bytes(row)
        if len(self.rows) >= self.max_rows or self.bytes >= self.max_bytes:
            self.flush()

    def flush(self) -> None:
        self.last_flush = time.monotonic()
        if not self.rows:
            return
        table = pa.Table.from_pylist(self.rows, schema=self.schema)
        final = self.dir / f"{self.prefix}-{self.index:05d}.parquet"
        tmp = self.dir / f".{final.name}.tmp"
        pq.write_table(table, tmp, compression="zstd", compression_level=self.level, row_group_size=self.rgs)
        tmp.replace(final)
        self.written_rows += len(self.rows)
        self.index += 1
        self.rows, self.bytes = [], 0

    close = flush


def parquet_column_bytes(directory) -> dict:
    comp, unc, rows = Counter(), Counter(), 0
    for p in list_shards(directory):
        md = pq.ParquetFile(p).metadata
        rows += md.num_rows
        for rg in range(md.num_row_groups):
            g = md.row_group(rg)
            for c in range(g.num_columns):
                col = g.column(c)
                comp[col.path_in_schema.split(".")[0]] += col.total_compressed_size
                unc[col.path_in_schema.split(".")[0]] += col.total_uncompressed_size
    return {"rows": rows, "compressed": dict(comp), "uncompressed": dict(unc)}


_local = threading.local()
ATTEMPTS: Counter = Counter()
_attempt_lock = threading.Lock()
_last_attempts: Counter = Counter()


def window_delta() -> dict:
    global _last_attempts
    with _attempt_lock:
        snap = Counter(ATTEMPTS)
        d = {k: snap[k] - _last_attempts[k] for k in ("total", "429", "5xx", "error")}
        _last_attempts = snap
    return d


def sent_headers() -> dict:
    return dict(get_session().headers)


def sha256_payload(x):
    if x is None:
        return None
    if isinstance(x, list):
        x = "\n".join(x)
    if isinstance(x, str):
        x = x.encode("utf-8")
    return hashlib.sha256(x).hexdigest()


def payload_bytes(x):
    if x is None:
        return None
    if isinstance(x, list):
        return sum(len(i.encode("utf-8")) for i in x) + max(0, len(x) - 1)
    return len(x.encode("utf-8")) if isinstance(x, str) else len(x)


def get_session(pool_size=8) -> requests.Session:
    s = getattr(_local, "session", None)
    if s is None:
        s = requests.Session()
        ad = HTTPAdapter(pool_connections=pool_size, pool_maxsize=pool_size, max_retries=0)
        s.mount("https://", ad)
        s.mount("http://", ad)
        s.headers.update({
            "User-Agent": CHROME_UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        })
        _local.session = s
    return s


def _once(url, timeout, max_bytes, deadline_s, headers):
    t0 = time.monotonic()
    out = {"status": None, "final_url": None, "headers": {}, "content": b"", "content_type": None,
           "error": None, "retryable": False, "history": [], "truncated": False, "dns": False}
    try:
        r = get_session().get(url, timeout=timeout, stream=True, allow_redirects=True, headers=headers)
        try:
            out["status"] = r.status_code
            out["final_url"] = r.url
            out["headers"] = dict(r.headers)
            out["content_type"] = r.headers.get("Content-Type")
            out["history"] = [h.url for h in r.history]
            chunks, n = [], 0
            for chunk in r.raw.stream(65536, decode_content=True):
                chunks.append(chunk)
                n += len(chunk)
                if max_bytes and n > max_bytes:
                    out["truncated"] = True
                    break
                if time.monotonic() - t0 > deadline_s:
                    raise requests.Timeout(f"overall deadline {deadline_s}s exceeded while reading body")
            body = b"".join(chunks)
            out["content"] = body[:max_bytes] if max_bytes else body
        finally:
            r.close()
    except (requests.Timeout, requests.ConnectionError, requests.exceptions.ChunkedEncodingError,
            requests.exceptions.ContentDecodingError) as e:
        out["error"] = f"{type(e).__name__}: {e}"[:500]
        out["retryable"] = not isinstance(e, requests.exceptions.SSLError)
        out["dns"] = any(m in str(e) for m in ("NameResolutionError", "gaierror", "Name or service not known",
                                               "Temporary failure in name resolution", "nodename nor servname"))
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"[:500]
        name = type(e).__name__
        out["retryable"] = name in ("ProtocolError", "ReadTimeoutError", "IncompleteRead", "ReadError")
    return out


def fetch(url, *, timeout=20, max_attempts=4, max_bytes=None, deadline_s=120, headers=None,
          backoff_base=2.0, max_backoff=60.0, conn_attempts=None, retry_dns=True) -> dict:
    t0 = time.monotonic()
    attempts = 0
    while True:
        attempts += 1
        if STOP.is_set():
            raise Interrupted()
        if LIMITER:
            LIMITER.acquire()
        res = _once(url, timeout, max_bytes, deadline_s, headers)
        if LIMITER:
            LIMITER.record(res["status"])
        with _attempt_lock:
            ATTEMPTS["total"] += 1
            st = res["status"]
            if st == 429:
                ATTEMPTS["429"] += 1
            elif st is not None and st >= 500:
                ATTEMPTS["5xx"] += 1
            elif st is None:
                ATTEMPTS["error"] += 1
        if res["status"] in RETRY_STATUS:
            limit = max_attempts
        elif res["retryable"] and not (res["dns"] and not retry_dns):
            limit = conn_attempts or max_attempts
        else:
            limit = 0
        if attempts >= limit:
            break
        delay = min(max_backoff, backoff_base * 2 ** (attempts - 1)) * (0.5 + random.random())
        ra = (res["headers"] or {}).get("Retry-After")
        if ra and str(ra).isdigit():
            delay = max(delay, min(float(ra), max_backoff))
        time.sleep(delay)
    res["attempts"] = attempts
    res["elapsed_ms"] = int((time.monotonic() - t0) * 1000)
    if res["truncated"] and not res["error"]:
        res["error"] = f"body truncated at {max_bytes} bytes"
    return res


def run_window(items, fn, workers, handle, window_factor=4, tick=None):
    it = iter(items)
    ex = ThreadPoolExecutor(max_workers=workers)
    pending = {}
    done_all = False
    try:
        while True:
            while not done_all and not STOP.is_set() and len(pending) < workers * window_factor:
                try:
                    item = next(it)
                except StopIteration:
                    done_all = True
                    break
                pending[ex.submit(fn, item)] = item
            if STOP.is_set():
                for f in [f for f in pending if f.cancel()]:
                    pending.pop(f)
            if not pending:
                break
            done, _ = wait(pending, timeout=5, return_when=FIRST_COMPLETED)
            for f in done:
                item = pending.pop(f)
                try:
                    res = f.result()
                except Interrupted:
                    continue
                except Exception as e:
                    res = e
                handle(item, res)
            if tick:
                tick()
    finally:
        ex.shutdown(wait=True, cancel_futures=True)


AF_RE = re.compile(r"AF_initDataCallback\(([\s\S]*?)\);?\s*</script")
SSD_RE = re.compile(r'<script[^>]*\bid="serialized-server-data"[^>]*>([\s\S]*?)</script>')


def decode_html(content: bytes, content_type: str | None = None) -> str:
    return content.decode("utf-8", errors="replace")


def google_af_args(html: str) -> list[str]:
    return AF_RE.findall(html)


def apple_serialized_data(html: str) -> str | None:
    m = SSD_RE.search(html)
    return m.group(1) if m else None


def raw_json_objects(text: str, key: str) -> list[str]:
    dec = json.JSONDecoder()
    m = re.search(r'"%s"\s*:\s*\[' % re.escape(key), text)
    if not m:
        return []
    i, n, out = m.end(), len(text), []
    while i < n:
        while i < n and text[i] in " \r\n\t,":
            i += 1
        if i >= n or text[i] == "]":
            break
        _, j = dec.raw_decode(text, i)
        out.append(text[i:j])
        i = j
    return out
