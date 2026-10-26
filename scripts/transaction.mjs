import {createClient} from 'genlayer-js';import {studionet} from 'genlayer-js/chains';import {readFileSync,writeFileSync,existsSync} from 'node:fs';
const [method,argsJson,actor='0x3A9F2F7420cBB5190e57c3cB375D82c035C353cD']=process.argv.slice(2);
const config=JSON.parse(readFileSync('web/deployment.json'));
const client=createClient({chain:studionet,account:actor});
const args=JSON.parse(argsJson||'[]');
if(method==='status'){
const tx=await client.getTransaction({hash:args[0]});writeFileSync(`/tmp/claimtrace-${args[0]}.json`,JSON.stringify(tx,(_,v)=>typeof v==='bigint'?v.toString():v,2));console.log(JSON.stringify({hash:args[0],status:tx.statusName||tx.status,data:tx.data,consensus_data:tx.consensus_data},(_,v)=>typeof v==='bigint'?v.toString():v));
}else if(method==='read'){
console.log(JSON.stringify(await client.readContract({address:config.contract,functionName:args[0],args:args.slice(1),transactionHashVariant:'latest-final'}),(_,v)=>typeof v==='bigint'?v.toString():v));
}else{throw new Error('Use the website session or Studio built-in account for reviewed signing. A copied public address cannot authorize a write.');}
