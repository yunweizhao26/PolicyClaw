import csv
from datetime import datetime, timezone
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import sys
import time
from urllib.parse import urlsplit

import pyarrow as pa
import pyarrow.parquet as pq
import idna

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
PYTHON = '/scratch/yz5944/miniconda3/envs/llm/bin/python'
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'corpus/stores'))
ARMS = ('web', 'android', 'apple')


def require_compute():
    if not os.environ.get('SLURM_JOB_ID'):
        raise RuntimeError('Every workload must run on a compute node through Slurm')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha(value):
    if isinstance(value, str):
        value = value.encode('utf-8')
    return hashlib.sha256(value).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str)+'\n')
    tmp.replace(path)


def write_table(path, rows, schema=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(rows, pa.Table):
        table = rows
    elif schema is not None:
        table = pa.Table.from_pylist(rows, schema=schema)
    else:
        keys = list(dict.fromkeys(k for row in rows for k in row))
        table = pa.Table.from_pydict({k: [row.get(k) for row in rows] for k in keys})
    tmp = path.with_suffix(path.suffix + '.tmp')
    pq.write_table(table, tmp, compression='zstd')
    tmp.replace(path)


def hostname(value):
    if not isinstance(value, str) or not value.strip():
        return ''
    try:
        value = value.strip()
        try:
            return str(ipaddress.ip_address(value.strip('[]')))
        except ValueError:
            pass
        host = urlsplit(value if '://' in value else 'https://' + value).hostname or ''
        host = host.rstrip('.')
        try:
            return str(ipaddress.ip_address(host))
        except ValueError:
            return idna.encode(host, uts46=True).decode('ascii').lower()
    except (ValueError, TypeError):
        return ''


class Domains:
    def __init__(self, ranks=None, rules=None):
        if ranks is None:
            manifest = json.loads((OUT / 'tranco/manifest.json').read_text())
            with (OUT / 'tranco' / manifest['filename']).open(newline='') as stream:
                ranks = {hostname(domain): int(rank) for rank, domain in csv.reader(stream)}
        self.ranks = ranks
        if rules is None:
            manifest = json.loads((OUT/'psl/manifest.json').read_text())
            body = (OUT/'psl'/manifest['filename']).read_bytes()
            assert sha(body) == manifest['sha256'], 'Pinned PSL changed'
            rules = body.decode('utf-8').splitlines()
        self.exact, self.wildcards, self.exceptions = set(), set(), set()
        for line in rules:
            rule = line.split('//', 1)[0].strip()
            if not rule:
                continue
            if rule.startswith('!'):
                self.exceptions.add(hostname(rule[1:]))
            elif rule.startswith('*.'):
                self.wildcards.add(hostname(rule[2:]))
            else:
                self.exact.add(hostname(rule))

    def registered(self, url):
        host = hostname(url)
        if not host:
            return None
        try:
            return str(ipaddress.ip_address(host))
        except ValueError:
            pass
        labels = host.split('.')
        matched, exception = 1, 0
        for i in range(len(labels)):
            suffix = '.'.join(labels[i:])
            width = len(labels) - i
            if suffix in self.exceptions:
                exception = max(exception, width)
            if suffix in self.exact:
                matched = max(matched, width)
            if i > 0 and suffix in self.wildcards:
                matched = max(matched, width + 1)
        public_width = exception - 1 if exception else matched
        return '.'.join(labels[-(public_width + 1):])


def snapshot(name, directories):
    path = OUT / 'snapshots' / f'{name}.json'
    if path.exists():
        return json.loads(path.read_text())
    files, skipped = [], []
    for directory in directories:
        directory = Path(directory)
        paths = [directory] if directory.is_file() else sorted(directory.glob('*.parquet'))
        for p in paths:
            try:
                st = p.stat()
                if 'data_full' in p.parts and time.time() - st.st_mtime < 120:
                    skipped.append(dict(path=str(p), reason='modified_in_last_120_seconds'))
                    continue
                pf = pq.ParquetFile(p)
                files.append(dict(path=str(p), size=st.st_size, mtime_ns=st.st_mtime_ns,
                                  rows=pf.metadata.num_rows, columns=pf.schema_arrow.names))
            except Exception as e:
                skipped.append(dict(path=str(p), reason=f'open_failed:{type(e).__name__}:{e}'))
    value = dict(name=name, captured_at=now(), files=files, skipped=skipped)
    write_json(path, value)
    return value


def unchanged(entry):
    st = Path(entry['path']).stat()
    if st.st_size != entry['size'] or st.st_mtime_ns != entry['mtime_ns']:
        raise RuntimeError('source_changed_since_snapshot')
    if 'data_full' in Path(entry['path']).parts and time.time() - st.st_mtime < 120:
        raise RuntimeError('modified_in_last_120_seconds')


def load_exclusions():
    return {r['registered_domain'] for r in pq.read_table(OUT/'exclusions.parquet').to_pylist()
            if r['registered_domain']}
