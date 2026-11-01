from copy import deepcopy

from base import ARMS, Domains, require_compute
from select_candidates import first_duplicate, jaccard, shingles, walk


def main():
    require_compute()
    a={('a','b','c','d','e'),('b','c','d','e','f')}
    b={('a','b','c','d','e')}
    assert jaccard(a,b)==0.5 and first_duplicate(a,[b])==(0,0.5)
    assert first_duplicate(a,[{('x','x','x','x','x')}]) is None
    domains=Domains({f'{a}.test':i+1 for i,a in enumerate(ARMS)})
    frames={}; bodies={}; verified={}
    for arm in ARMS:
        frames[arm]=[]
        for rank in range(1,4):
            key=f'{arm}-{rank}'
            frames[arm].append(dict(arm=arm,rank=rank,candidate_id=key,organization_key=key,
                                   policy_url=f'https://{arm}.test/{rank}'))
            bodies[key]=dict(http_status=200,visible_chars=200,
                visible_text=' '.join(f'{arm}{i}' for i in range(40)),final_url=f'https://{arm}.test/{rank}')
            verified[key]=dict(label='complete_policy',flags={'language':'en','multiple_orgs':False},
                               evidence=[],reason='test')
    verified['web-1']['flags']['language']='fr'
    bodies['web-2']['visible_chars']=99
    chosen,rejected,counts,blocked=walk(frames,bodies.get,verified,domains,set(),target=1)
    assert chosen[0]['candidate_id']=='web-3'
    assert [r['reason'] for r in rejected]==['not_english','visible_text_under_100_chars']
    broken=deepcopy(verified); broken['web-3']={'error':'temporary API failure'}
    chosen,rejected,counts,blocked=walk(frames,bodies.get,broken,domains,set(),target=1)
    assert not chosen and blocked['reason']=='verifier_unresolved'
    bodies['android-1']['visible_text']=bodies['web-3']['visible_text']
    chosen,rejected,counts,blocked=walk(frames,bodies.get,verified,domains,set(),target=1)
    assert chosen[1]['candidate_id']=='android-2'
    assert rejected[-1]['reason']=='duplicate_visible_text_jaccard_ge_0.5'
    assert rejected[-1]['jaccard']==1.0
    print('PASS: exact 0.5 boundary, non-English and 99-character rejection, verifier-error turn blocking, cross-arm text duplicates')


if __name__=='__main__':
    main()
