export async function connectAddress(provider) {
  if (!provider?.request) throw new Error('No EIP-1193 wallet found. Open this page in a browser with MetaMask.');
  const accounts = await provider.request({method:'eth_requestAccounts'});
  if (!Array.isArray(accounts) || !/^0x[0-9a-fA-F]{40}$/.test(accounts[0] || '')) throw new Error('Wallet returned no valid public address.');
  return accounts[0];
}
export function validateAddress(value) {
  if (!/^0x[0-9a-fA-F]{40}$/.test(value)) throw new Error('Enter a valid public Studio address. Never enter a private key.');
  return value;
}
