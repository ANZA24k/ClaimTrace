import test from 'node:test';import assert from 'node:assert/strict';import {connectAddress,validateAddress} from '../web/wallet.mjs';
test('connection requests only public accounts, never signs or sends',async()=>{const calls=[];const address='0x'+'a'.repeat(40);assert.equal(await connectAddress({request:async args=>{calls.push(args);return [address]}}),address);assert.deepEqual(calls,[{method:'eth_requestAccounts'}]);});
test('no provider returns useful error',async()=>{await assert.rejects(connectAddress(null),/MetaMask/);});
test('user rejection propagates without retries',async()=>{let calls=0;await assert.rejects(connectAddress({request:async()=>{calls++;throw new Error('Rejected by user')}}),/Rejected/);assert.equal(calls,1);});
test('malformed wallet reply is rejected',async()=>{await assert.rejects(connectAddress({request:async()=>['secret']}),/valid public/);});
test('address input rejects secrets and malformed values',()=>{for(const a of ['','0x'+'f'.repeat(64),'seed phrase','0x1234'])assert.throws(()=>validateAddress(a));assert.equal(validateAddress('0x'+'b'.repeat(40)),'0x'+'b'.repeat(40));});
