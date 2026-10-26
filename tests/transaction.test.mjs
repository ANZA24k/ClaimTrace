import test from 'node:test';import assert from 'node:assert/strict';import {describeTransaction} from '../web/transaction.mjs';
const returned={consensus_data:{leader_receipt:[{result:{status:'return'}}]}};
test('accepted is provisional even when execution returned',()=>{const d=describeTransaction({...returned,status:5,result:6});assert.equal(d.status,'ACCEPTED');assert.equal(d.terminal,false);assert.equal(d.success,false);});
test('finalized majority agreement and returned execution succeeds',()=>{assert.equal(describeTransaction({...returned,status:7,result:6}).success,true);});
test('finalized no-majority is never reported as success',()=>{const d=describeTransaction({...returned,status:7,result:5});assert.equal(d.terminal,true);assert.equal(d.success,false);});
test('finalized majority disagreement is never reported as success',()=>{assert.equal(describeTransaction({...returned,status:7,result:7}).success,false);});
test('agreed rollback still fails',()=>{assert.equal(describeTransaction({status:7,result:6,consensus_data:{leader_receipt:[{result:{status:'rollback'}}]}}).success,false);});
test('missing execution evidence never implies success',()=>{assert.equal(describeTransaction({status:7,result:6}).success,false);});
test('undetermined and canceled are terminal failures',()=>{for(const status of [6,8,12,13]){const d=describeTransaction({status,result:5});assert.equal(d.terminal,true);assert.equal(d.success,false);}});
