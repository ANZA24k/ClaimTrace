import {transactionResultNumberToName,transactionsStatusNumberToName} from 'genlayer-js/types';
export function describeTransaction(tx){
  const status=tx.statusName||transactionsStatusNumberToName[String(tx.status)]||String(tx.status);
  const consensus=tx.resultName||transactionResultNumberToName[String(tx.result)]||String(tx.result??'UNKNOWN');
  const receipts=tx.consensus_data?.leader_receipt;
  const completed=(Array.isArray(receipts)?receipts:receipts?[receipts]:[]).filter(r=>r?.result?.payload!=='idle');
  const receipt=completed[0];
  const runtime=receipt?.execution_result||null;
  const execution=receipt?.result?.status||runtime||tx.consensusData?.leaderReceipt?.executionResult||null;
  const terminal=['FINALIZED','UNDETERMINED','CANCELED','LEADER_TIMEOUT','VALIDATORS_TIMEOUT'].includes(status);
  const agreed=['AGREE','MAJORITY_AGREE','SUCCESS'].includes(consensus);
  const returned=completed.length>0&&completed.every(r=>['return','FINISHED_WITH_RETURN'].includes(r?.result?.status||r?.execution_result)&&(!r?.execution_result||['SUCCESS','FINISHED_WITH_RETURN'].includes(r.execution_result)));
  return {status,consensus,execution,terminal,success:status==='FINALIZED'&&agreed&&returned};
}
