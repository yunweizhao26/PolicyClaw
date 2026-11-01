import json
import re

from base import OUT, now, require_compute, sha, write_json
import common as C


def main():
    require_compute()
    folder = OUT/'psl'
    folder.mkdir(exist_ok=True)
    path = folder/'public_suffix_list.dat'
    if (folder/'manifest.json').exists():
        record = json.loads((folder/'manifest.json').read_text())
        assert sha(path.read_bytes()) == record['sha256']
        return
    url = 'https://publicsuffix.org/list/public_suffix_list.dat'
    if path.exists():
        raise RuntimeError('PSL exists without its manifest; inspect before downloading again')
    result = C.fetch(url, timeout=30, max_attempts=4, max_bytes=5_000_000, deadline_s=180)
    if result['status'] != 200:
        raise RuntimeError(f'PSL HTTP {result["status"]}: {result["error"]}')
    body = result['content']
    text = body.decode('utf-8')
    assert '// ===BEGIN ICANN DOMAINS===' in text
    assert '// ===BEGIN PRIVATE DOMAINS===' in text
    assert '// ===END PRIVATE DOMAINS===' in text
    version = re.search(r'^// VERSION:\s*(.+)$', text, re.M)
    path.write_bytes(body)
    write_json(folder/'manifest.json', dict(filename=path.name, source_url=url,
        final_url=result['final_url'], fetched_at=now(), date=now()[:10],
        version=version.group(1) if version else None, sha256=sha(body),
        sections=['ICANN', 'PRIVATE']))


if __name__ == '__main__':
    main()
