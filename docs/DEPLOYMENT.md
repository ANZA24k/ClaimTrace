# Verified deployment and live pilot

Verified 2026-10-26 against finalized StudioNet state. All pilot documents and claims are explicitly synthetic.

- Public website: https://claimtrace.ansaf1st34.chatgpt.site/
- Contract: https://explorer-studio.genlayer.com/address/0xA01d1Df7608344d4ee015c31142f80b331FDB7F1
- Initial deployment: https://explorer-studio.genlayer.com/tx/0xcbbb5ac767af1086a3c98d9daaaf5a3743ca16b3dfeeda210b9c5787131a4958
- Final code update: https://explorer-studio.genlayer.com/tx/0xb9b82af04e18af7e47db2b25095310f03f4585e11719ad3e7a6e9d77dfb18ea2
- Final source SHA-256: `18f6c194bb5131d15297ad6d2dab03d3e533d2bc77a74bb83183e1639ac09851`
- The live code was retrieved with `getContractCode` and matches `contracts/claimtrace.py` exactly.

## Finalized outcomes

| Claim | Revision history | End-to-end evidence |
|---|---|---|
| 1 | VERIFIED → CONTRADICTED | Built-in Studio account locked/submitted; an independent app account evaluated; another app actor challenged; Studio evaluated the recheck. Original revision preserved byte-for-byte. |
| 2 | CONTRADICTED | Registry and later audit conflict on the same release/date/quantity. |
| 3 | INCONCLUSIVE | Missing primary source, date, origin and count; absence of proof is not treated as an opposite fact. |
| 4 | VERIFIED | Created, committed and evaluated entirely through the public website on the final contract code. |

## Real transaction receipts

| Method | Claim | Consensus / execution | Transaction |
|---|---|---|
| deploy | — | MAJORITY_AGREE / return | [0xcbbb5ac7…](https://explorer-studio.genlayer.com/tx/0xcbbb5ac767af1086a3c98d9daaaf5a3743ca16b3dfeeda210b9c5787131a4958) |
| upgrade | — | MAJORITY_AGREE / PLATFORM_CODE_UPDATE | [0xf519d611…](https://explorer-studio.genlayer.com/tx/0xf519d6118ea1ecf0e112a2648f66ba07783908e3278302cc101e4a50b4d50847) |
| upgrade | — | MAJORITY_AGREE / PLATFORM_CODE_UPDATE | [0x6ccdf858…](https://explorer-studio.genlayer.com/tx/0x6ccdf85857620f0edd5b04b64bef159400778b7531b8cc8645227ff675a5e762) |
| upgrade | — | MAJORITY_AGREE / PLATFORM_CODE_UPDATE | [0xb9b82af0…](https://explorer-studio.genlayer.com/tx/0xb9b82af04e18af7e47db2b25095310f03f4585e11719ad3e7a6e9d77dfb18ea2) |
| lock_claim | 1 | MAJORITY_AGREE / return | [0x21ae651f…](https://explorer-studio.genlayer.com/tx/0x21ae651f13abcf73c0ad328650cf431560f7613a2aada18d4b0d287aa395ccab) |
| submit_evidence | 1 | MAJORITY_AGREE / return | [0x0114d1eb…](https://explorer-studio.genlayer.com/tx/0x0114d1eb0252c9fe165a84b572bac6f0594bff5dbe30988fcad2c3adbb214b8c) |
| evaluate | 1 | MAJORITY_AGREE / return | [0x4f96835a…](https://explorer-studio.genlayer.com/tx/0x4f96835a615699593873db0468cc2569456b6852b59583d8196b7c883b3fe054) |
| lock_claim | 2 | MAJORITY_AGREE / return | [0x53a865dc…](https://explorer-studio.genlayer.com/tx/0x53a865dc4e7b6267da8da9b736844a69691de3afbf6b70ab0232ea1ab467e45a) |
| lock_claim | 3 | MAJORITY_AGREE / return | [0x258bbb77…](https://explorer-studio.genlayer.com/tx/0x258bbb77d4f2104b9023fa3230311260ad50c6c52bd4370f832ce19521d880f6) |
| submit_evidence | 2 | MAJORITY_AGREE / return | [0xf804f9b1…](https://explorer-studio.genlayer.com/tx/0xf804f9b18350cb365b61ebddb80edfd87e21c8051e89e1073a2d11f7dbacd654) |
| submit_evidence | 3 | MAJORITY_AGREE / return | [0x964b71fe…](https://explorer-studio.genlayer.com/tx/0x964b71fe16a179fdeb1d748962ceaf7f59a18b06ea79d743163d9330a3c6913f) |
| evaluate | 2 | MAJORITY_DISAGREE / return | [0x2fa27e94…](https://explorer-studio.genlayer.com/tx/0x2fa27e9401c65ce61e79ee46bc9b6f22f26673572ce63e8136fb089f4ecaf637) |
| evaluate | 3 | MAJORITY_DISAGREE / return | [0x915dc53c…](https://explorer-studio.genlayer.com/tx/0x915dc53c4160af9c53d5d8e780f66afbd00a76d5cba6e3d64ed182a523388022) |
| evaluate | 2 | MAJORITY_DISAGREE / return | [0x5c56fca4…](https://explorer-studio.genlayer.com/tx/0x5c56fca41b26ce33230ac5d3da67133eb8e7a249bc2b31756053a646c5d37794) |
| submit_evidence | 1 | MAJORITY_AGREE / return | [0x6a991e80…](https://explorer-studio.genlayer.com/tx/0x6a991e8085fae02cb2854602af60378f513eb5e44d9053fa09f3b4fff7489193) |
| evaluate | 2 | MAJORITY_AGREE / return | [0xe7a0bdb6…](https://explorer-studio.genlayer.com/tx/0xe7a0bdb681585bae7916af14dea3344ebe390e853b6ce25b71af269397f5fd1f) |
| lock_claim | 4 | MAJORITY_AGREE / return | [0x8ad9e669…](https://explorer-studio.genlayer.com/tx/0x8ad9e6699bec25fc13f20e130b394f089621ddef47ffa76d5a019944232e6645) |
| submit_evidence | 4 | MAJORITY_AGREE / return | [0xc36216fc…](https://explorer-studio.genlayer.com/tx/0xc36216fc6c9b3277d732762ea0182fe1e46426f1a36049a2a859ce96fb8bb6e6) |
| evaluate | 3 | MAJORITY_DISAGREE / return | [0xde50a201…](https://explorer-studio.genlayer.com/tx/0xde50a201694e001bc71be146862bd9815ce42bcfa7210c6be6d8f4f51b74a60a) |
| evaluate | 3 | MAJORITY_AGREE / return | [0x48585c40…](https://explorer-studio.genlayer.com/tx/0x48585c40e43f20ef080eff49ba0e97d4c079a35d0976fc7fc9ae118dce0ede18) |
| evaluate | 4 | MAJORITY_AGREE / return | [0xb38114ed…](https://explorer-studio.genlayer.com/tx/0xb38114eded488d5b0944f1d0607c9f8fd7fa0353da923bd766657a5cf50dcc54) |
| evaluate | 1 | MAJORITY_AGREE / return | [0x1fe40b60…](https://explorer-studio.genlayer.com/tx/0x1fe40b60fc9ec28cdd5c7503fc0d69fe8eb555928110843e6ec1406ffa53ffaf) |

22 finalized transactions inspected: 18 successful operations and 4 failed consensus attempts. Failed attempts are disclosed above and did not add verdict revisions. FINALIZED alone does not imply successful execution.

## Deployment history and honest limits

The initial supported contract was deployed once. Three explicit Studio platform code updates preserved all locked claims, source commitments and previous revisions. They corrected ambiguous source stance, added a strict output template with one bounded schema-repair pass, and clarified that missing evidence means UNKNOWN. Platform upgrade transactions have no application VM receipt; their finality, majority agreement, new code payload and final deployed source bytes were checked separately. They are not presented as normal contract method calls. Studio platform upgrade access is a simulator facility, not a production governance or immutability guarantee.

The four unsuccessful consensus attempts exposed real model schema/interpretation differences and remain in the evidence. They are not relabeled as successful pilots. No synthetic transaction hashes, simulated results presented as actual execution, or admin-set verdicts are used.

## Verification performed

- 4 finalized records; every claim and revision hash, predecessor link, evidence commitment and stored quotation verified.
- 4 unique commit-pinned public files independently fetched and checked for exact bytes/SHA-256.
- Original claim 1 revision 0 compared with its pre-update snapshot: unchanged.
- Public website returned HTTP 200 without authentication and read the live finalized contract.
- Browser checks: complete claim 4 creation → evidence → evaluation; independent claim 1 challenge; exact source verification; receipt-chain verification.
- 73 official Direct Mode tests and 17 frontend wallet/lifecycle tests; GenVM lint/validation and production build. The repository Actions workflow repeats these checks on pushes.
- Wallet unit tests prove connection requests only `eth_requestAccounts`. The live missing-provider error was verified. An actual MetaMask extension connection could not be tested because the browser has no EIP-1193 extension. No existing wallet secret was requested or copied.

## Actors

- Studio built-in deployment/submitter/reviewer: `0x3A9F2F7420cBB5190e57c3cB375D82c035C353cD`.
- Independent first app evaluator: `0x28ee9F2c00fB96e7e9B60FA060a83c12735381bE`.
- Public website challenger and complete-flow actor: `0xD453f96c6699A33dda0e1b144c501629Ee3675C1`.

## Reproduce read-only verification

```sh
NODE_USE_ENV_PROXY=1 node scripts/verify-live.mjs
```

Use `--save` to update [machine-readable verification](live-verification.json). The script does not deploy, sign or submit writes. `NODE_USE_ENV_PROXY=1` is only needed in environments with an HTTP proxy.

See [README](../README.md) for the trust scope, buffered HTTP limitation, challenge limits, model risks, ephemeral session behavior and continued-use plan.
