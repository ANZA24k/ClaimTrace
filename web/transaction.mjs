import {transactionResultNumberToName,transactionsStatusNumberToName} from 'genlayer-js/types';
export function describeTransaction(tx){
  const status=tx.statusName||transactionsStatusNumberToName[String(tx.status)]||String(tx.status);
  const consensus=tx.resultName||transactionResultNumberToName[String(tx.result)]||String(tx.result??'UNKNOWN');
  const receipts=tx.consensus_data?.leader_receipt;
  const receipt=Array.isArray(receipts)?receipts.at(-1):receipts;
  const execution=receipt?.execution_result||receipt?.result?.status||tx.consensusData?.leaderReceipt?.executionResult||null;
  const terminal=['FINALIZED','UNDETERMINED','CANCELED','LEADER_TIMEOUT','VALIDATORS_TIMEOUT'].includes(status);
  const agreed=['AGREE','MAJORITY_AGREE','SUCCESS'].includes(consensus);
  const returned=['return','SUCCESS','FINISHED_WITH_RETURN'].includes(execution);
  return {status,consensus,execution,terminal,success:status==='FINALIZED'&&agreed&&returned};
}
