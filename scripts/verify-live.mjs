import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {describeTransaction} from '../web/transaction.mjs';
const config=JSON.parse(readFileSync('web/deployment.json'));
const client=createClient({chain:studionet});
const sha=v=>createHash('sha256').update(v).digest('hex');
const canon=v=>JSON.stringify(v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,JSON.parse(canon(v[k]))])):Array.isArray(v)?v.map(x=>JSON.parse(canon(x))):v).replace(/[\u007f-\uffff]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));
const deployed=await client.getContractCode(config.contract);
assert.equal(deployed,readFileSync('contracts/claimtrace.py','utf8'),'Deployed source differs from repository');
const count=Number(await client.readContract({address:config.contract,functionName:'get_count',args:[],transactionHashVariant:'latest-final'}));
const records=await Promise.all(Array.from({length:count},(_,i)=>String(i+1)).map(async id=>JSON.parse(await client.readContract({address:config.contract,functionName:'get_claim',args:[id],transactionHashVariant:'latest-final'}))));
const sourceCache=new Map();
for(const record of records){
 assert.equal(sha(canon(record.locked)),record.claim_hash,'Claim hash mismatch');let previous=record.claim_hash;
 for(const revision of record.revisions){
  const {revision_hash,...payload}=revision;
  assert.equal(revision.previous_hash,previous);assert.equal(sha(canon(payload)),revision_hash);assert.equal(sha(canon(revision.sources)),revision.evidence_hash);previous=revision_hash;
  for(const s of revision.sources){if(sourceCache.has(s.url))continue;const res=await fetch(s.url,{redirect:'error',signal:AbortSignal.timeout(25000)});assert.equal(res.status,200);const b=new Uint8Array(await res.arrayBuffer());assert.equal(b.length,s.bytes);assert.equal(sha(b),s.sha256);sourceCache.set(s.url,new TextDecoder('utf-8',{fatal:true}).decode(b));}
  for(const rows of Object.values(revision.result.assessment))for(const row of rows)for(const ref of row.refs){assert.ok(sourceCache.get(revision.sources[ref.source].url).includes(ref.quote),'Ungrounded on-chain quotation');}
 }
}
const transactions=[];const entries=[{hash:config.deployment_transaction,method:'deploy',expect_success:true},...(config.upgrades||[]),...config.pilot];
for(let start=0;start<entries.length;start+=4){
 transactions.push(...await Promise.all(entries.slice(start,start+4).map(async entry=>{const tx=await client.getTransaction({hash:entry.hash});const detail=describeTransaction(tx);assert.equal(detail.status,'FINALIZED','Transaction not finalized: '+entry.hash);if(entry.method==='upgrade'){assert.equal(typeof tx.data?.new_code,'string','Missing platform upgrade code');const upgraded=tx.data.new_code.startsWith('#')?tx.data.new_code:Buffer.from(tx.data.new_code,'base64').toString('utf8');detail.code_sha256=sha(upgraded);if(entry.hash===config.upgrades.at(-1).hash)assert.equal(upgraded,deployed,'Final upgrade bytes differ');detail.execution='PLATFORM_CODE_UPDATE';detail.success=['AGREE','MAJORITY_AGREE'].includes(detail.consensus);}if(entry.expect_success)assert.equal(detail.success,true,'Expected transaction did not execute successfully: '+entry.hash);return {...entry,...detail,from:tx.from_address,to:tx.to_address,created_at:tx.created_at,rounds:tx.consensus_history?.consensus_results?.length||0};})));
}
for(const [id,expected] of Object.entries(config.expected_verdicts||{})){const r=records.find(x=>x.id===id);assert.equal(r?.revisions.at(-1)?.result.verdict,expected);assert.equal(r.pending,false);}
const result={verified_at:new Date().toISOString(),network:'studionet',contract:config.contract,source_sha256:sha(deployed),count,source_count:sourceCache.size,transactions,records};
if(process.argv.includes('--save')){writeFileSync('docs/live-verification.json',JSON.stringify(result,null,2)+'\n');}
console.log(JSON.stringify({verified_at:result.verified_at,source_matches:true,source_sha256:result.source_sha256,claims:records.map(r=>({id:r.id,verdicts:r.revisions.map(v=>v.result.verdict),pending:r.pending})),verified_sources:sourceCache.size,finalized_transactions:transactions.length},null,2));
