import {createClient} from 'genlayer-js';import {studionet} from 'genlayer-js/chains';
const client=createClient({chain:studionet});
console.log(String(await client.readContract({address:'0xA01d1Df7608344d4ee015c31142f80b331FDB7F1',functionName:'get_count',args:[]})));
