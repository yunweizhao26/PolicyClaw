import csv
import json
import os
from pathlib import Path
import shutil
import sys
import threading

import pyarrow.parquet as pq

from base import OUT, ROOT, now, require_compute, write_json
from fetch_candidates import candidates
from corpus.collect import verify as V
from policyclaw import llm as L

LOCK = threading.Lock()
SHARED_CACHE = ROOT/'corpus/collect/llm_cache'
ENV = dict(LLM_BACKEND='gemini', LLM_MODEL_NAME='gemini-3.8-flash', GEMINI_THINKING_LEVEL='MEDIUM',
    GOOGLE_CLOUD_PROJECT='project-21073ade-77cc-47de-979', GOOGLE_CLOUD_LOCATION='global',
    GCLOUD_BIN='/scratch/yz5944/opt/google-cloud-sdk/bin/gcloud', LLM_CACHE=str(SHARED_CACHE))
ENV.update(CLOUDSDK_CORE_DISABLE_FILE_LOGGING='true', CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK='true')


def install_audit(usage_name='gemini_usage.jsonl', error_name='gemini_errors.jsonl'):
    def local_path(self, key):
        dest = OUT/'llm_cache'/key[:2]/f'{key}.json'
        source = SHARED_CACHE/key[:2]/f'{key}.json'
        with LOCK:
            if not dest.exists() and source.is_file():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, dest)
        return str(dest)
    L.LLM._path = local_path
    original = L.GeminiLLM._post
    def audited_post(self, *args, **kwargs):
        try:
            result = original(self, *args, **kwargs)
        except Exception as error:
            with LOCK:
                with (OUT/error_name).open('a') as stream:
                    stream.write(json.dumps(dict(at=now(), model=self.model,
                        error=f'{type(error).__name__}: {error}'))+'\n')
            raise
        meta = result.get('usageMetadata', {})
        rec = dict(at=now(), model=self.model, variant=self.variant, usageMetadata=meta,
                   finishReasons=[c.get('finishReason') for c in result.get('candidates', [])])
        with LOCK:
            with (OUT/usage_name).open('a') as stream:
                stream.write(json.dumps(rec)+'\n')
        return result
    L.GeminiLLM._post = audited_post


def main():
    require_compute()
    os.environ.update(ENV)
    install_audit()
    plan_path = Path(sys.argv[1])
    plan = json.loads(plan_path.read_text())
    inputs = []
    previously_verified = set()
    if (OUT/'verify.jsonl').exists():
        for line in (OUT/'verify.jsonl').read_text().splitlines():
            record = json.loads(line)
            if 'error' not in record:
                previously_verified.add(record['id'])
    for arm, end_rank in plan.items():
        for candidate in candidates(arm, end_rank):
            if candidate['rank'] > end_rank: break
            if candidate['candidate_id'] in previously_verified:
                continue
            path = OUT/'fetch'/f'{candidate["candidate_id"]}.parquet'
            row = pq.read_table(path, columns=['http_status', 'visible_chars', 'final_url', 'visible_text']).to_pylist()[0]
            if row['http_status'] is None or not 200 <= row['http_status'] < 300 or row['visible_chars'] < 100:
                continue
            textpath = OUT/'fetch/texts'/f'{candidate["candidate_id"]}.visible.txt'
            if not textpath.exists(): textpath.write_text(row['visible_text'])
            inputs.append(dict(id=candidate['candidate_id'], text_path=str(textpath), url=row['final_url'] or candidate['policy_url'], source=arm))
    folder = OUT/'verify_batches'
    folder.mkdir(exist_ok=True)
    tsv = folder/f'{plan_path.stem}.tsv'
    output = folder/f'{plan_path.stem}.jsonl'
    with tsv.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['id', 'text_path', 'url', 'source'], delimiter='\t')
        writer.writeheader(); writer.writerows(inputs)
    if inputs and not output.exists():
        probe = V.run(inputs[:1], folder, output, 1, True, version='v1')
        if any('error' in r for r in probe):
            raise RuntimeError('Verifier preflight failed; stopping before bulk verification. See '+str(output))
    records = V.run(inputs, folder, output, 8, True, version='v1') if inputs else []
    if any('error' in r for r in records):
        records = V.run(inputs, folder, output, 4, True, version='v1')
    all_records = {}
    for path in sorted(folder.glob('batch-*.jsonl')):
        for line in path.read_text().splitlines():
            record = json.loads(line); all_records[record['id']] = record
    with (OUT/'verify.jsonl').open('w') as stream:
        for record in all_records.values(): stream.write(json.dumps(record, ensure_ascii=False)+'\n')
    write_json(OUT/'verification_config.json', dict(environment=ENV, prompt='v1',
        prompt_path=str(V.PROMPT_PATHS['v1']), shared_cache_read_only=str(SHARED_CACHE),
        new_cache_write_directory=str(OUT/'llm_cache'), language_field='flags.language', english_value='en'))
    if any('error' in r for r in records):
        raise RuntimeError('Unresolved verifier errors; selection cannot skip those ranked candidates')


if __name__ == '__main__':
    main()
