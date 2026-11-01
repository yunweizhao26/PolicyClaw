import ast
from pathlib import Path
import tempfile

import pyarrow.parquet as pq

from base import OUT, ROOT, ARMS, Domains, require_compute, write_table
from android import decode_details
from apple import is_us_row
from fetch_candidates import extract
from select_candidates import shingles, jaccard, walk
from links import android_policy_link


def main():
    require_compute()
    import trafilatura
    assert trafilatura.__version__ == '2.0.0'
    for path in OUT.glob('*.py'): ast.parse(path.read_text(), filename=str(path))
    domains = Domains({'example.com':1, 'a.example.com':2, 'web.test':3, 'android.test':4, 'apple.test':5})
    assert domains.registered('HTTPS://WWW.A.Example.Com/x') == 'a.example.com'
    assert domains.registered('https://badexample.com') is None
    assert domains.registered('https://x.example.com') == 'example.com'
    assert is_us_row({'request_url':'https://apps.apple.com/us/app/id123'})
    assert not is_us_row({'request_url':'https://apps.apple.com/gb/app/id123'})
    assert not is_us_row({'storefront':'GB','request_url':'https://apps.apple.com/us/app/id123'})
    assert jaccard(shingles('one two three four five six'), shingles('one two three four five seven')) == 1/3
    assert shingles('ONE, two three four five!') == shingles('one two three four five')
    base = dict(policy_url='https://web.test', http_status=200, content_type='text/html',
                body=b'<html><body><p>Kept text</p><script>hidden</script><style>hidden</style><noscript>hidden</noscript></body></html>')
    assert extract(base)['visible_text'] == 'Kept text'
    plain = extract(dict(base, content_type='text/plain; charset=utf-8', body=b'  one two\nthree  '))
    assert plain['visible_text'] == plain['trafilatura_text'] == 'one two\nthree'
    frames, fetched, verified = {}, {}, {}
    for arm in ARMS:
        frames[arm] = []
        for rank in (1, 2):
            identity = f'{arm}-{rank}'
            frames[arm].append(dict(candidate_id=identity, arm=arm, rank=rank,
                organization_key=identity, policy_url=f'https://{arm}.test/{rank}'))
            fetched[identity] = dict(http_status=200, visible_chars=200, visible_text=' '.join(f'{arm}{i}' for i in range(30)),
                final_url=f'https://{arm}.test/{rank}')
            verified[identity] = dict(label='complete_policy', flags=dict(language='en', multiple_orgs=False), evidence=[], reason='test')
    fetched['web-1']['http_status'] = 404
    chosen, rejected, counts, blocked = walk(frames, fetched.get, verified, domains, set(), target=1)
    assert [r['candidate_id'] for r in chosen] == ['web-2', 'android-1', 'apple-1']
    assert rejected[0]['reason'] == 'http_not_2xx' and blocked is None
    chosen, rejected, counts, blocked = walk(frames, lambda i:None if i=='web-2' else fetched[i],
                                             verified, domains, set(), target=1)
    assert not chosen and blocked['arm']=='web'
    fetched['android-1']['final_url']='https://web.test/same-organization'
    chosen, rejected, counts, blocked = walk(frames, fetched.get, verified, domains, set(), target=1)
    assert chosen[1]['candidate_id']=='android-2'
    assert rejected[1]['reason']=='duplicate_final_registered_domain'
    with tempfile.TemporaryDirectory(dir=OUT) as directory:
        path = Path(directory)/'union.parquet'
        write_table(path, [dict(web='a'), dict(android='b')])
        assert pq.read_table(path).column_names == ['web', 'android']
    first = ROOT/'corpus/stores/data_full/android/meta/part-00000.parquet'
    raw = next(pq.ParquetFile(first).iter_batches(batch_size=1, columns=['data_raw'])).to_pylist()[0]['data_raw']
    parsed = decode_details(raw)
    assert parsed['privacyPolicy'] == android_policy_link(raw)[0]
    assert parsed['title'] and parsed['developerId'] and parsed['realInstalls'] is not None
    print('PASS: syntax, longest suffix, exact shingles, HTML/plain extraction, round-robin rejection and blocking, domain duplicates, metadata union, real Android parser parity', flush=True)


if __name__ == '__main__':
    main()
