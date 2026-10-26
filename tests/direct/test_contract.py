import json
import copy
import hashlib
import sys
import pytest
from conftest import BODY, URL, source, assessment, prepare


def module(c):
    return sys.modules[c.__class__.__module__]

@pytest.mark.parametrize('req,dim,stance,expected',[
    ('SUPPORTED','CONSISTENT','SUPPORTING','VERIFIED'),
    ('CONTRADICTED','CONSISTENT','SUPPORTING','CONTRADICTED'),
    ('SUPPORTED','INCONSISTENT','SUPPORTING','CONTRADICTED'),
    ('SUPPORTED','CONSISTENT','CONTRADICTING','CONTRADICTED'),
    ('SUPPORTED','UNKNOWN','SUPPORTING','PARTIAL'),
    ('UNKNOWN','UNKNOWN','UNKNOWN','INCONCLUSIVE')])
def test_verdicts(setup,req,dim,stance,expected):
    c, vm = setup
    prepare(c,vm,assessment(req,dim,stance))
    c.evaluate('1')
    record = json.loads(c.get_claim('1'))
    assert record['revisions'][0]['result']['verdict'] == expected
    assert vm.run_validator()

@pytest.mark.parametrize('url',[
    'http://localhost/a','https://127.0.0.1/x','https://raw.githubusercontent.com.evil.org/a/b/'+'a'*40+'/x',
    URL+'?x=1', URL+'#x', URL.replace('/fixtures/','/../'), URL.replace('/fixtures/','//'),
    URL.replace('https://','https://user@'), URL.replace('a'*40,'main'),URL.replace('a'*40,'a'*39),
    URL.replace('/fixtures/','/%2e/'),URL.replace('.com/','.com:443/')])
def test_unsafe_urls(setup,url):
    c,vm=setup
    with pytest.raises(ValueError):
        c.submit_evidence('1',json.dumps([source(url=url)]),'Initial evidence trail test.')
    assert json.loads(c.get_claim('1'))['sources'] == []

@pytest.mark.parametrize('mutator',[
    lambda x: x.update(bytes=True), lambda x: x.update(bytes=0),lambda x: x.update(bytes=12001),
    lambda x: x.update(sha256='f'*63),lambda x: x.update(sha256='F'*64),lambda x: x.update(extra='x')])
def test_source_schema(setup,mutator):
    c,vm=setup
    s=source();mutator(s)
    with pytest.raises(ValueError):c.submit_evidence('1',json.dumps([s]),'Initial evidence trail test.')

@pytest.mark.parametrize('raw',['[]','{}','null','[1]','[{}]','[NaN]','[', ' '*8001])
def test_malformed_sources(setup,raw):
    c,vm=setup
    with pytest.raises((ValueError,TypeError)):c.submit_evidence('1',raw,'Initial evidence trail test.')

def test_duplicate_json_keys(setup):
    c,vm=setup
    with pytest.raises(ValueError,match='Duplicate JSON key'):
        c.submit_evidence('1','[{"url":"x","url":"y"}]','Initial evidence trail test.')

def test_duplicates(setup):
    c,vm=setup
    with pytest.raises(ValueError,match='Duplicate'):
        c.submit_evidence('1',json.dumps([source(),source()]),'Initial evidence trail test.')
    s=source(url=URL.replace('atlas','other'))
    with pytest.raises(ValueError,match='Duplicate'):
        c.submit_evidence('1',json.dumps([source(),s]),'Initial evidence trail test.')

def test_owner_and_permissionless_evaluation(setup,direct_bob):
    c,vm=setup
    vm.sender=direct_bob
    with pytest.raises(ValueError,match='Only owner'):c.submit_evidence('1',json.dumps([source()]),'Initial evidence trail test.')
    assert c.get_count()==1

def test_pending_and_replay(setup):
    c,vm=setup
    with pytest.raises(ValueError,match='No pending'):c.evaluate('1')
    prepare(c,vm)
    with pytest.raises(ValueError,match='already pending'):c.submit_evidence('1',json.dumps([source()]),'Initial evidence trail test.')
    c.evaluate('1')
    with pytest.raises(ValueError,match='No pending'):c.evaluate('1')

@pytest.mark.parametrize('body,state',[(b'\xff','INVALID_UTF8'),(b'x'*12001,'OVERSIZED')])
def test_unusable_bytes(setup,body,state):
    c,vm=setup
    s=source(body)
    if len(body)>12000:s['bytes']=12000
    c.submit_evidence('1',json.dumps([s]),'Initial evidence trail test.')
    vm.mock_web('.*raw.*',{'status':200,'body':body})
    c.evaluate('1')
    result=json.loads(c.get_claim('1'))['revisions'][0]['result']
    assert result['verdict']=='INCONCLUSIVE'
    assert result['fingerprints'][0]['state']==state
    assert vm.run_validator()

@pytest.mark.parametrize('status,state',[(404,'HTTP_UNAVAILABLE'),(302,'HTTP_UNAVAILABLE'),(403,'HTTP_UNAVAILABLE')])
def test_http_unavailable(setup,status,state):
    c,vm=setup;prepare(c,vm)
    vm.clear_mocks();vm.mock_web('.*raw.*',{'status':status,'body':''})
    c.evaluate('1')
    assert json.loads(c.get_claim('1'))['revisions'][0]['result']['verdict']=='INCONCLUSIVE'

@pytest.mark.parametrize('status',[429,500,502,503,504])
def test_transient_retry(setup,status):
    c,vm=setup;prepare(c,vm)
    vm.clear_mocks();vm.mock_web('.*raw.*',{'status':status,'body':''})
    with pytest.raises(Exception):c.evaluate('1')
    r=json.loads(c.get_claim('1'));assert r['pending'] and not r['revisions']
    vm.clear_mocks();vm.mock_web('.*raw.*',{'status':200,'body':BODY});vm.mock_llm('.*',json.dumps(assessment()))
    c.evaluate('1');assert len(json.loads(c.get_claim('1'))['revisions'])==1

def test_changed_bytes_and_validator_disagreement(setup):
    c,vm=setup;prepare(c,vm);c.evaluate('1')
    vm.clear_mocks();vm.mock_web('.*raw.*',{'status':200,'body':BODY+'changed'})
    assert not vm.run_validator()

def test_grounding_and_consensus_forgery(setup):
    c,vm=setup;prepare(c,vm);c.evaluate('1')
    result=json.loads(c.get_claim('1'))['revisions'][0]['result']
    forged=copy.deepcopy(result);forged['assessment']['requirements'][0]['refs'][0]['quote']='Fabricated quotation not present'
    assert not vm.run_validator(leader_result=forged)
    forged=copy.deepcopy(result);forged['verdict']='CONTRADICTED'
    assert not vm.run_validator(leader_result=forged)
    assert not vm.run_validator(leader_result={'assessment':{}})
    assert not vm.run_validator(leader_error=ValueError('leader failed'))

def test_validator_semantic_disagreement(setup):
    c,vm=setup;prepare(c,vm);c.evaluate('1')
    vm.clear_mocks();vm.mock_web('.*raw.*',{'status':200,'body':BODY});vm.mock_llm('.*',json.dumps(assessment(req='CONTRADICTED')))
    assert not vm.run_validator()

@pytest.mark.parametrize('mutator',[
    lambda a:a.update(extra=1), lambda a:a.update(requirements=[]),
    lambda a:a['requirements'][0].update(status='VERIFIED'),lambda a:a['requirements'][0].update(refs=[]),
    lambda a:a['requirements'][0]['refs'][0].update(source=True),
    lambda a:a['requirements'][0]['refs'][0].update(source=9),lambda a:a['requirements'][0]['refs'][0].update(quote='not in evidence'),
    lambda a:a['requirements'][0].update(reason=''),lambda a:a.update(sources=[]),
    lambda a:a['dimensions'][0].update(refs=[{'source':0,'quote':'tiny'}])])
def test_malformed_llm(setup,mutator):
    c,vm=setup;a=assessment();mutator(a);prepare(c,vm,a)
    with pytest.raises(Exception):c.evaluate('1')
    assert not json.loads(c.get_claim('1'))['revisions']

def test_challenge_append_and_limit(setup,direct_bob):
    c,vm=setup;prepare(c,vm);c.evaluate('1')
    first=json.loads(c.get_claim('1'))['revisions'][0]
    vm.sender=direct_bob
    for n in (1,2):
        b=BODY+str(n);s=source(b,url=URL.replace('atlas',f'correction{n}'))
        c.submit_evidence('1',json.dumps([s]),'Independent challenge with additional evidence.')
        # No usable evidence is sufficient here to test bounded state transitions.
        vm.clear_mocks();vm.mock_web('.*raw.*',{'status':404,'body':''});c.evaluate('1')
    record=json.loads(c.get_claim('1'))
    assert record['revisions'][0]==first
    assert len(record['sources'])==3 and len(record['revisions'])==3
    assert record['revisions'][1]['previous_hash']==first['revision_hash']
    for rev in record['revisions']:
        h=rev.pop('revision_hash');assert module(c).digest(module(c).canonical(rev))==h
    with pytest.raises(ValueError,match='Two rechecks'):c.submit_evidence('1',json.dumps([source(BODY+'last',url=URL.replace('atlas','last'))]),'Final challenge exceeds the revision cap.')

def test_challenge_expiry(setup):
    c,vm=setup;vm.warp('2026-10-01T00:00:00');prepare(c,vm);c.evaluate('1')
    vm.warp('2026-10-09T00:00:00')
    with pytest.raises(ValueError,match='window closed'):c.submit_evidence('1',json.dumps([source(BODY+'2',url=URL.replace('atlas','later'))]),'Expired challenge with new evidence.')

@pytest.mark.parametrize('claim,requirements', [('tiny','["A sufficient requirement."]'),('x'*1601,'["A sufficient requirement."]'),('A sufficiently long public claim.','[]'),('A sufficiently long public claim.','["short"]'),('A sufficiently long public claim.','["Duplicate requirement.","Duplicate requirement."]')])
def test_lock_limits(setup,claim,requirements):
    c,vm=setup
    with pytest.raises(ValueError):c.lock_claim(claim,requirements)

def test_capacity_and_unknown_read(setup):
    c,vm=setup
    for i in range(7):c.lock_claim('Additional synthetic public claim.', '["A sufficient requirement."]')
    with pytest.raises(ValueError,match='capacity'):c.lock_claim('Additional synthetic public claim.','["A sufficient requirement."]')
    assert c.get_claim('999')=='null'

@pytest.mark.parametrize('allow',[True,False])
def test_ancillary_difference_requires_independent_audit(setup,allow):
    c,vm=setup;prepare(c,vm);c.evaluate('1')
    candidate=json.loads(c.get_claim('1'))['revisions'][0]['result']
    candidate['assessment']['sources'][0]['status']='CONTEXT'
    vm.mock_llm('^Independent evidence audit', json.dumps({'valid':allow}))
    assert vm.run_validator(leader_result=candidate) is allow


def test_audit_malformed_result_rejected(setup):
    c,vm=setup;prepare(c,vm);c.evaluate('1')
    candidate=json.loads(c.get_claim('1'))['revisions'][0]['result']
    candidate['assessment']['sources'][0]['status']='CONTEXT'
    vm.mock_llm('^Independent evidence audit', '{"valid":"true"}')
    assert not vm.run_validator(leader_result=candidate)


def test_one_bounded_schema_repair_preserves_grounding(setup):
    c,vm=setup
    vm.mock_llm('^Schema repair',json.dumps(assessment()))
    invalid=assessment();invalid['requirements']=[]
    prepare(c,vm,invalid)
    c.evaluate('1')
    assert json.loads(c.get_claim('1'))['revisions'][0]['result']['verdict']=='VERIFIED'


def test_repair_cannot_introduce_ungrounded_findings(setup):
    c,vm=setup
    repaired=assessment();repaired['requirements'][0]['refs'][0]['quote']='Invented facts not in the source'
    vm.mock_llm('^Schema repair',json.dumps(repaired))
    invalid=assessment();invalid['requirements']=[]
    prepare(c,vm,invalid)
    with pytest.raises(Exception):c.evaluate('1')
    assert json.loads(c.get_claim('1'))['revisions']==[]
