import csv
import io
import json
import time
import zipfile

from base import OUT, now, require_compute, sha, write_json
import common as C


def main():
    require_compute()
    folder = OUT / 'tranco'
    folder.mkdir(exist_ok=True)
    if (folder/'manifest.json').exists():
        record = json.loads((folder/'manifest.json').read_text())
        assert sha((folder/record['filename']).read_bytes()) == record['sha256']
        print('Using pinned Tranco list', record['list_id'], flush=True)
        return
    api = 'https://tranco-list.eu/api/lists/date/2026-10-15'
    response_path = folder / 'api-2026-10-15.json'
    if response_path.exists():
        data = json.loads(response_path.read_text())
    else:
        result = C.fetch(api, max_attempts=5, backoff_base=30, max_backoff=120, max_bytes=1_000_000)
        if result['status'] != 200:
            raise RuntimeError(f'Tranco API HTTP {result["status"]}: {result["error"]}')
        data = json.loads(result['content'])
        write_json(response_path, data)
    print('Tranco API', data, flush=True)
    list_id = data.get('list_id') or data.get('id')
    if not list_id:
        raise ValueError('Tranco API did not provide list_id')
    time.sleep(30)
    url = f'https://tranco-list.eu/download/{list_id}/1000000'
    result = C.fetch(url, max_attempts=5, backoff_base=30, max_backoff=120, max_bytes=100_000_000)
    if result['status'] != 200:
        raise RuntimeError(f'Tranco download HTTP {result["status"]}: {result["error"]}')
    body = result['content']
    if body.startswith(b'PK'):
        (folder/f'{list_id}.zip').write_bytes(body)
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            body = archive.read(next(n for n in archive.namelist() if n.endswith('.csv')))
    rows = list(csv.reader(io.StringIO(body.decode('utf-8'))))
    assert len(rows) == 1_000_000 and all(int(r[0]) == i+1 for i,r in enumerate(rows))
    filename = f'tranco-{list_id}-2026-10-15.csv'
    (folder/filename).write_bytes(body)
    write_json(folder/'manifest.json', dict(date='2026-10-15', list_id=list_id, filename=filename,
               sha256=sha(body), rows=len(rows), api_url=api, download_url=url, fetched_at=now()))
    print('Saved', filename, len(rows), flush=True)


if __name__ == '__main__':
    main()
