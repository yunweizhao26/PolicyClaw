import json
import os

import pyarrow.parquet as pq
from lxml import html
from urllib.parse import urldefrag, urljoin

from base import OUT, ROOT, now, sha, write_json
from fetch_candidates import fetch_one, limited_once
from verify_candidates import ENV, SHARED_CACHE, V, install_audit
import common as C


def privacy_links(body, final_url):
    if not body:
        return []
    try:
        page = html.fromstring(body)
    except (ValueError, html.etree.ParserError):
        return []
    result, seen = [], set()
    for anchor in page.xpath('//a[@href]'):
        href = anchor.get('href') or ''
        text = ' '.join(anchor.text_content().split())
        if 'privacy' not in href.lower() and 'privacy' not in text.lower():
            continue
        url = urldefrag(urljoin(final_url, href)).url
        if not url.lower().startswith(('http://', 'https://')) or url in seen:
            continue
        seen.add(url)
        result.append(dict(anchor_text=text, url=url))
    return result


def read_fetch(identity, raw=False):
    path = OUT/'fetch'/f'{identity}.parquet'
    cols = None if raw else [c for c in pq.ParquetFile(path).schema_arrow.names if c != 'body']
    return pq.read_table(path, columns=cols).to_pylist()[0]


class Backend:
    def __init__(self, offline=False):
        self.offline = offline
        self.urls, self.views, self.recorded = {}, {}, set()
        self.manifest = {e['path']:e for e in json.loads((OUT/'snapshots/stored_policies.json').read_text())['files']}
        os.environ.update(ENV)
        self.config = dict(model=ENV['LLM_MODEL_NAME'], variant='thinking=MEDIUM', prompt='v1',
            prompt_sha256=sha(V.PROMPT_PATHS['v1'].read_bytes()), rubric_sha256=sha(V.RUBRIC_PATH.read_bytes()),
            verifier_sha256=sha((ROOT/'corpus/collect/verify.py').read_bytes()))
        for path in sorted((OUT/'fetch').glob('*.parquet')):
            row = pq.read_table(path, columns=['candidate_id', 'policy_url', 'fetched_at']).to_pylist()[0]
            if not (row['fetched_at'] or '').startswith('2026-10-'):
                continue
            old = self.urls.get(row['policy_url'])
            if old is None or (row['fetched_at'], row['candidate_id']) > old:
                self.urls[row['policy_url']] = (row['fetched_at'], row['candidate_id'])
        provenance = json.loads((OUT/'v1/code_provenance.json').read_text())
        v1_compatible = (provenance.get('policyclaw/prompts/verify_policy_page.txt') == self.config['prompt_sha256']
                         and provenance.get('corpus/collect/rubric.md') == self.config['rubric_sha256']
                         and provenance.get('corpus/collect/verify.py') == self.config['verifier_sha256'])
        for path in (OUT/'v1/verify.jsonl', OUT/'verify.jsonl'):
            if not path.exists() or (path.parent.name == 'v1' and not v1_compatible):
                continue
            for line in path.read_text().splitlines():
                row = json.loads(line)
                if 'error' in row or row.get('model') != self.config['model'] or row.get('variant') != self.config['variant']:
                    continue
                if path.parent.name == 'v1':
                    fetched = read_fetch(row['id'])
                    view, _ = V.render_view(fetched['visible_text'], row['url'])
                    key = self.view_key(view)
                else:
                    if row.get('config') != self.config:
                        continue
                    key = row['view_key']
                    self.recorded.add(row['id'])
                self.views[key] = row
        if not offline:
            install_audit('gemini_usage_v2.jsonl', 'gemini_errors_v2.jsonl')
            C._once = limited_once(C._once)
            C.set_limiter(4, 4, 4)
            write_json(OUT/'verification_config.json', dict(environment=ENV, **self.config,
                shared_cache_read_only=str(SHARED_CACHE), new_cache_write_directory=str(OUT/'llm_cache'),
                reuse='Exact rendered v1 prompt, model, and MEDIUM variant; stable URL fetch identities'))

    def view_key(self, view):
        return sha(json.dumps(self.config, sort_keys=True) + '\n' + V.build_prompt(view, 'v1'))

    def fetch(self, url, arm, raw=False):
        existing = self.urls.get(url)
        if existing:
            identity = existing[1]
        else:
            if self.offline:
                raise RuntimeError(f'Audit needs an unfetched URL: {url}')
            identity = 'url-v2-' + sha(url)
            fetch_one(dict(candidate_id=identity, arm=arm, policy_url=url), self.manifest)
            fetched = read_fetch(identity)
            self.urls[url] = (fetched['fetched_at'], identity)
        row = read_fetch(identity, raw=raw)
        assert row['policy_url'] == url
        assert sha(row['visible_text']) == row['visible_sha256']
        assert sha(row['trafilatura_text']) == row['trafilatura_sha256']
        if raw:
            assert sha(row['body'] or b'') == row['body_sha256']
        return dict(row, fetch_id=identity)

    def verify(self, body, arm):
        identity = body['fetch_id']
        url = body.get('final_url') or body['policy_url']
        view, info = V.render_view(body['visible_text'], url)
        key = self.view_key(view)
        old = self.views.get(key)
        if old:
            result = {k:v for k,v in old.items() if k not in ('id', 'source', 'url', 'usage', 'config', 'view_key')}
            result.update(reused_verifier_id=old['id'], usage=dict(calls=0, cached=1, failures=0,
                prompt_tokens=0, completion_tokens=0, thinking_tokens=0, seconds=0))
        else:
            if self.offline:
                raise RuntimeError(f'Audit needs an unverified view: {identity}')
            result = V.verify_view(view, self.config['model'], str(SHARED_CACHE), version='v1', truncated=info['truncated'])
        record = dict(result, id=identity, source=arm, url=url, **info, view_key=key,
                      config=self.config, visible_sha256=body['visible_sha256'])
        if 'error' in record:
            if not self.offline:
                with (OUT/'verifier_failures_v2.jsonl').open('a') as stream:
                    stream.write(json.dumps(dict(at=now(), **record))+'\n')
            raise RuntimeError(f'Verifier unresolved for {identity}: {record["error"]}')
        if identity not in self.recorded and not self.offline:
            with (OUT/'verify.jsonl').open('a') as stream:
                stream.write(json.dumps(record, ensure_ascii=False)+'\n')
            self.recorded.add(identity)
        self.views[key] = record
        return record
