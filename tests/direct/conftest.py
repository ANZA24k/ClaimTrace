import json
import hashlib
import pytest

BODY = 'SYNTHETIC PILOT. Atlas registry record A-10 dated 2026-10-01: ten records published by Atlas lab. Origin: Atlas lab signed register. Publication 2026-10-02 follows registration. All ten records are included.'
URL = 'https://raw.githubusercontent.com/ANZA24k/ClaimTrace/' + 'a'*40 + '/fixtures/atlas.txt'

def source(body=BODY, url=URL):
    raw = body.encode() if isinstance(body, str) else body
    return {'url':url,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}

def assessment(req='SUPPORTED', dim='CONSISTENT', stance='SUPPORTING', quote=BODY[:90]):
    def row(status):
        return {'status':status, 'reason':'The supplied Atlas registry supports this finding.', 'refs':[] if status == 'UNKNOWN' else [{'source':0,'quote':quote}]}
    return {'requirements':[row(req)],'dimensions':[row(dim) for _ in range(4)],'sources':[row(stance)]}

@pytest.fixture
def setup(direct_vm, direct_deploy):
    c = direct_deploy('contracts/claimtrace.py')
    c.lock_claim('Atlas lab published ten records after registration.', '["The registry confirms ten records and their origin."]')
    return c, direct_vm

def prepare(c, vm, value=None, body=BODY):
    c.submit_evidence('1',json.dumps([source(body)]),'Initial committed registry evidence.')
    vm.mock_web('.*raw.*', {'status':200,'body':body})
    vm.mock_llm('.*ClaimTrace.*',json.dumps(value or assessment()))
