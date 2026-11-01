import ast
from copy import deepcopy
import subprocess

from base import ARMS, OUT, Domains, require_compute, sha
from exclusions import PolicyIE, exclusion_reason, policy_members
from revision_fetch import privacy_links
from revision_select import Selector
from select_candidates import first_duplicate, jaccard, shingles


class FakeBackend:
    def __init__(self, bodies, verified):
        self.bodies, self.verified, self.requests = bodies, verified, []

    def fetch(self, url, arm, raw=False):
        self.requests.append(url)
        return self.bodies[url]

    def verify(self, body, arm):
        record = self.verified.get(body['policy_url'])
        if record == 'error':
            raise RuntimeError('Verifier unresolved')
        return record or dict(id=body['fetch_id'], label='complete_policy', flags=dict(language='en', multiple_orgs=False),
            evidence=[], reason='fixture', view_key='fixture-view')


def body(url, word, status=200, markup=None):
    text = ' '.join(f'{word}{i}' for i in range(40))
    return dict(policy_url=url, final_url=url, http_status=status, visible_text=text, visible_chars=len(text),
        trafilatura_text=text, trafilatura_chars=len(text), visible_sha256=sha(text), trafilatura_sha256=sha(text),
        fetch_id=sha(url), body=markup, fetched_at='2026-10-20T12:00:00+00:00')


def main():
    require_compute()
    paths = list(OUT.glob('revision_*.py')) + [OUT/name for name in ('base.py', 'psl.py', 'exclusions.py',
        'web.py', 'rebuild_app_frames.py', 'archive_revision.py', 'measure.py', 'verify_candidates.py')]
    for path in paths:
        ast.parse(path.read_text(), filename=str(path))
    subprocess.run(['bash', '-n', str(OUT/'run_revision.sbatch')], check=True)
    import trafilatura
    assert trafilatura.__version__ == '2.0.0'
    rules = ['com', 'uk', 'co.uk', '*.ck', '!www.ck', '*.kawasaki.jp', '!city.kawasaki.jp',
             'github.io', 'wixsite.com', 'blogspot.com', '公司.cn']
    d = Domains({'example.com':1, 'sub.example.com':2}, rules=rules)
    for host, expected in [('Sub.Example.COM.', 'example.com'), ('a.b.co.uk','b.co.uk'),
        ('a.b.ck','a.b.ck'), ('x.www.ck','www.ck'), ('a.city.kawasaki.jp','city.kawasaki.jp'),
        ('x.y.kawasaki.jp','x.y.kawasaki.jp'), ('x.user.github.io','user.github.io'),
        ('shop.wixsite.com','shop.wixsite.com'), ('a.b.unknown','b.unknown'),
        ('192.0.2.3','192.0.2.3'), ('https://[2001:db8::1]/','2001:db8::1'),
        ('https://BÜCHER.com/','xn--bcher-kva.com'), ('www.foo.blogspot.com','foo.blogspot.com')]:
        assert d.registered(host) == expected, (host, d.registered(host), expected)
    assert d.registered('https://www.x.公司.cn/') == 'x.xn--55qx5d.cn'
    assert d.registered('https://sub.example.com') == 'example.com'
    markup = b'<a href="/one">Privacy policy</a><a href="/one">repeat Privacy</a><a href="/PRIVACY/two">two</a><a href="../three">Our PRIVACY</a><a href="/four">privacy</a>'
    links = privacy_links(markup, 'https://site.test/final/home')
    assert [r['url'] for r in links] == ['https://site.test/one', 'https://site.test/PRIVACY/two',
                                      'https://site.test/three', 'https://site.test/four']
    assert links[0]['anchor_text'] == 'Privacy policy'
    groups = policy_members(['sanitized_split/train/week1/10.txt','sanitized_split/train/week1/2.txt',
        'sanitized_split/test/digg/1.txt','sanitized_split/test/digg/2.ann','README.md'])
    assert groups['sanitized_split/train/week1'] == ['sanitized_split/train/week1/2.txt','sanitized_split/train/week1/10.txt']
    p = PolicyIE.__new__(PolicyIE)
    one, two = ('a','b','c','d','e'), ('b','c','d','e','f')
    p.policies = [('fixture', {one, two})]
    assert p.maximum({one})['policyie_containment'] == 0.5
    assert p.maximum({one, two})['policyie_containment'] == 1
    assert jaccard({one, two}, {one}) == 0.5
    assert first_duplicate({one, two}, [{one}]) == (0, 0.5)
    assert shingles('ONE, two three four five!') == shingles('one two three four five')
    assert exclusion_reason(['x.test'], {'x.test':{'PolicyIE_test_site'}}) == 'policyie_test_site_domain'
    assert exclusion_reason(['google.com'], {}) is None
    frames, bodies = {a:[] for a in ARMS}, {}
    for arm, count in [('web',1), ('android',3), ('apple',1)]:
        for rank in range(1, count+1):
            key = f'{arm}-{rank}'
            url = f'https://{key}.test/privacy'
            frames[arm].append(dict(arm=arm, rank=rank, frame_rank=rank, candidate_id=key,
                organization_key=key, organization_name=key, policy_url=url, web_domain='site.test'))
            bodies[url] = body(url, key)
    home = 'https://site.test/'
    bodies[home] = body(home, 'home', markup=markup)
    bodies[home]['final_url'] = 'https://site.test/final/home'
    for i, link in enumerate(links):
        bodies[link['url']] = body(link['url'], 'webtext', 404 if i == 0 else 200)
    bodies[links[1]['url']]['final_url'] = 'https://hosted.test/privacy'
    bodies[frames['android'][0]['policy_url']]['final_url'] = 'https://site.test/app-policy'
    bodies[frames['android'][1]['policy_url']]['visible_text'] = bodies[links[1]['url']]['visible_text']
    backend = FakeBackend(bodies, {})
    selector = Selector(backend, d, {}, p)
    assert selector.walk(frames, target=1)
    assert [r['candidate_id'] for r in selector.selected] == ['web-1','android-3','apple-1']
    assert selector.selected[0]['chosen_link_number'] == 2
    assert links[2]['url'] not in backend.requests
    assert selector.rejected[0]['reason'] == 'duplicate_registered_domain'
    assert selector.rejected[0]['shared_domain'] == 'site.test'
    assert selector.rejected[0]['duplicate_final_url'] == 'https://hosted.test/privacy'
    assert selector.rejected[1]['reason'] == 'duplicate_visible_text_jaccard_ge_0.5'
    failed = deepcopy(bodies)
    for link in links[:3]:
        failed[link['url']]['http_status'] = 404
    backend = FakeBackend(failed, {})
    selector = Selector(backend, d, {}, p)
    assert selector.next_organization(frames['web'][0]) is None
    assert len(selector.links) == 3 and links[3]['url'] not in backend.requests
    assert selector.rejected[0]['reason'] == 'no_eligible_link_among_first_three'
    for status, markup_value, expected in [(503, b'failed', 'home_page_not_fetched'),
        (200, b'<a href="/terms">Terms</a>', 'no_privacy_link')]:
        failed[home] = body(home, 'home', status, markup_value)
        selector = Selector(FakeBackend(failed, {}), d, {}, p)
        assert selector.next_organization(frames['web'][0]) is None
        assert selector.rejected[0]['reason'] == expected
    test_candidate = frames['apple'][0]
    test_url = test_candidate['policy_url']
    boundary = deepcopy(bodies)
    boundary[test_url]['visible_text'] = 'a b c d e ' + ' '.join(f'extra{i}' for i in range(40))
    selector = Selector(FakeBackend(boundary, {}), d, {}, p)
    assert selector.next_organization(test_candidate) is None
    assert selector.rejected[0]['reason'] == 'policyie_containment_ge_0.5'
    for label, language, expected in [('partial_policy', 'en', 'verifier_partial_policy'),
                                      ('complete_policy', 'fr', 'not_english')]:
        verification = FakeBackend(bodies, {}).verify(bodies[test_url], 'apple')
        verification['label'] = label
        verification['flags']['language'] = language
        selector = Selector(FakeBackend(bodies, {test_url:verification}), d, {}, p)
        assert selector.next_organization(test_candidate) is None
        assert selector.rejected[0]['reason'] == expected
    boundary[test_url]['visible_chars'] = 99
    selector = Selector(FakeBackend(boundary, {test_url:'error'}), d, {}, p)
    assert selector.next_organization(test_candidate) is None
    assert selector.rejected[0]['reason'] == 'visible_text_under_100_chars'
    backend = FakeBackend(bodies, {links[1]['url']:'error'})
    selector = Selector(backend, d, {}, p)
    try:
        selector.walk(frames, target=1)
    except RuntimeError as error:
        assert str(error) == 'Verifier unresolved' and not selector.selected
    else:
        raise AssertionError('Unresolved verifier was skipped')
    print('PASS: syntax, PSL exact/wildcard/exception/private/default/IP/IDNA, homepage order and first-three limit, '
          'numeric PolicyIE order, exact 0.5 thresholds, cross-arm site/policy duplicates, text duplicates, and failure blocking')


if __name__ == '__main__':
    main()
