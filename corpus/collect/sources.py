from __future__ import annotations

import csv, html, io, json, os, re, urllib.request, zipfile
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

DATA = Path("/scratch/yz5944/nlp+privacy/Contextual-Integrity/ci_policy/data")
PRIVASEER_DIR = DATA / "policy_corpus" / "privaseer"
STORES = {
    "gplay": (DATA / "gplay_corpus", "gplay_catalog.json", "appId", "privacyPolicy"),
    "appstore": (DATA / "appstore_corpus", "appstore_catalog.json", "trackId", "_privacyUrl"),
}
OPP115_ZIP = Path("/scratch/yz5944/nlp+privacy/cache/opp115/OPP-115_v1_0.zip")
OPP115_URL = "https://usableprivacy.org/static/data/OPP-115_v1_0.zip"

STRATA = [("p_lt_0.6", 0.0, 0.6), ("p_0.6_0.9", 0.6, 0.9), ("p_0.9_0.99", 0.9, 0.99), ("p_ge_0.99", 0.99, float("inf"))]
INDEX_COLUMNS = ["policy_id", "url", "domain", "probability"]



def privaseer_files() -> list[Path]:
    return sorted(PRIVASEER_DIR.glob("*.parquet"))


def privaseer_index(threads: int = 8) -> pd.DataFrame:
    def read(path):
        table = pq.read_table(path, columns=INDEX_COLUMNS).to_pandas()
        table.insert(0, "row", np.arange(len(table)))
        table.insert(0, "file", str(path))
        return table
    with ThreadPoolExecutor(threads) as pool:
        index = pd.concat(list(pool.map(read, privaseer_files())), ignore_index=True)
    index["probability"] = pd.to_numeric(index["probability"], errors="coerce")
    index["domain"] = index["domain"].fillna("").str.strip().str.lower()
    return index


def stratum_of(p: float) -> str:
    for name, lo, hi in STRATA:
        if lo <= p < hi:
            return name
    return ""


def stratum_counts(index: pd.DataFrame) -> dict:
    out = {}
    for name, lo, hi in STRATA:
        part = index[(index.probability >= lo) & (index.probability < hi)]
        out[name] = {"rows": int(len(part)), "domains": int(part.domain[part.domain != ""].nunique())}
    out["probability_missing"] = int(index.probability.isna().sum())
    return out


def sample_privaseer(index: pd.DataFrame, per_stratum: int | dict, rng: np.random.Generator,
                     exclude_domains: set = frozenset(), strict: bool = True) -> pd.DataFrame:
    counts = per_stratum if isinstance(per_stratum, dict) else {name: per_stratum for name, _, _ in STRATA}
    used, picks = set(exclude_domains), []
    for name, lo, hi in STRATA:
        want = counts.get(name, 0)
        cand = index[(index.probability >= lo) & (index.probability < hi) & (index.domain != "")]
        domains, got = cand.domain.to_numpy(), 0
        for i in (rng.permutation(len(cand)) if want else []):
            if domains[i] in used:
                continue
            used.add(domains[i])
            picks.append((cand.index[i], name))
            got += 1
            if got == want:
                break
        if got < want and strict:
            raise SystemExit(f"stratum {name}: only {got} distinct domains")
    sample = index.loc[[i for i, _ in picks]].copy()
    sample["stratum"] = [s for _, s in picks]
    return sample


def privaseer_texts(sample: pd.DataFrame, threads: int = 8) -> dict:
    by_file = sample.groupby("file")["row"].apply(lambda rows: sorted(int(r) for r in rows)).to_dict()

    def read(path):
        pf, out, start = pq.ParquetFile(path), {}, 0
        for rg in range(pf.metadata.num_row_groups):
            size = pf.metadata.row_group(rg).num_rows
            wanted = [r for r in by_file[path] if start <= r < start + size]
            if wanted:
                texts = pf.read_row_group(rg, columns=["text"]).column("text").take([r - start for r in wanted])
                out.update({(path, r): t or "" for r, t in zip(wanted, texts.to_pylist())})
            start += size
        return out

    texts = {}
    with ThreadPoolExecutor(threads) as pool:
        for part in pool.map(read, sorted(by_file)):
            texts.update(part)
    return texts



def app_urls(store: str) -> dict:
    folder, catalog, id_field, url_field = STORES[store]
    with open(folder / catalog) as handle:
        entries = json.load(handle)
    return {str(e.get(id_field)): e.get(url_field) or "" for e in entries if e.get(id_field) is not None}


def sample_apps(store: str, n: int, rng: np.random.Generator, urls: dict, exclude_apps: set = frozenset(),
                exclude_urls: set = frozenset()) -> tuple[list[dict], dict]:
    folder = STORES[store][0] / "downloads"
    apps = sorted(os.listdir(folder))
    picks, seen_urls = [], set(exclude_urls)
    stats = {"app_folders": len(apps), "checked": 0, "no_clean_txt": 0, "duplicate_url": 0, "excluded": 0}
    for i in rng.permutation(len(apps)):
        app = apps[i]
        if app in exclude_apps:
            stats["excluded"] += 1
            continue
        stats["checked"] += 1
        path = folder / app / "clean.txt"
        if not path.is_file():
            stats["no_clean_txt"] += 1
            continue
        url = urls.get(app, "")
        if url and url in seen_urls:
            stats["duplicate_url"] += 1
            continue
        seen_urls.add(url)
        picks.append({"app": app, "url": url, "path": str(path)})
        if len(picks) == n:
            break
    if len(picks) < n:
        raise SystemExit(f"{store}: only {len(picks)} pages")
    return picks, stats



class _HTMLText(HTMLParser):
    BLOCK = {"br", "p", "div", "li", "tr", "table", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)


def opp115_text(raw_html: str) -> str:
    parser = _HTMLText()
    parser.feed(raw_html.replace("|||", "<p>"))
    lines = [" ".join(line.split()) for line in html.unescape("".join(parser.parts)).split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def ensure_opp115() -> Path:
    if not OPP115_ZIP.exists():
        OPP115_ZIP.parent.mkdir(parents=True, exist_ok=True)
        tmp = OPP115_ZIP.with_suffix(".part")
        urllib.request.urlretrieve(OPP115_URL, tmp)
        tmp.rename(OPP115_ZIP)
    return OPP115_ZIP


def sample_opp115(n: int, rng: np.random.Generator) -> list[dict]:
    with zipfile.ZipFile(ensure_opp115()) as z:
        names = sorted(m for m in z.namelist()
                       if m.startswith("OPP-115/sanitized_policies/") and m.endswith(".html"))
        doc = z.read("OPP-115/documentation/policies_opp115.csv").decode("utf-8-sig")
        urls = {r["Policy UID"].strip(): r["Policy URL"].strip() for r in csv.DictReader(io.StringIO(doc))}
        out = []
        for i in sorted(rng.choice(len(names), size=n, replace=False)):
            name = names[i]
            uid = Path(name).stem.split("_", 1)[0]
            out.append({"name": Path(name).name, "uid": uid, "url": urls.get(uid, ""),
                        "text": opp115_text(z.read(name).decode("utf-8", errors="replace"))})
    return out
