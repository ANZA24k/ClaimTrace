# ClaimTrace

**Lock a public claim. Trace every committed source. Preserve the verdict and its challenges.**

ClaimTrace addresses evidence cherry-picking and moving goalposts in public claims: release announcements, research summaries, transparency reports and other statements whose support is spread across multiple documents. A reviewer should be able to reproduce which exact evidence was assessed, see contradictory sources, and distinguish the original assessment from a later challenge.

GenLayer is central: each leader and validator independently retrieves all committed sources and interprets whether the combined trail supports the locked requirements. The comparator requires identical source fingerprints, per-requirement outcomes and canonical verdicts. Matching detail classifications are accepted directly; differing ancillary classifications require an additional independent semantic audit of every proposed finding against the retrieved bytes. The contract—not the frontend or LLM—derives the canonical verdict. There is no off-chain verdict API or admin verdict override.

## Live deployment

See [deployment evidence](docs/DEPLOYMENT.md) for the verified contract, transaction hashes, actors, pilot results and website. [Pilot inputs](docs/pilot-inputs.json) contain exact commit-pinned source commitments. All pilot facts are synthetic; none certify an actual organization.

## Try it

1. Open the website linked in the deployment evidence. No wallet is needed to read finalized records.
2. Select a claim. Inspect its locked requirements, source URLs/SHA-256/byte lengths, findings, exact quotations, contradictions and history. Independently verify source bytes or the receipt chain, and export audit JSON.
3. To create a claim, choose **Lock a claim**, enter a precise statement and 1–6 requirements. An isolated test-only StudioNet account is generated in browser memory. Review the exact contract, account, arguments and zero-value write before confirming. Keep the tab open: reloading discards that account, so finish initial evidence submission first.
4. Submit 1–6 public commit-pinned GitHub raw files. The browser retrieves the bytes and prepares the SHA-256/byte-length commitments for review. Only the locking account may submit initial evidence.
5. Choose **Evaluate pending evidence**. Any actor can evaluate. The app signs with its isolated test account, genuinely submits to the deployed contract, records the returned transaction hash, polls status, distinguishes provisional acceptance from finalization and reloads finalized state. Rejected/reverted/undetermined execution is not a successful verdict. Pending hashes can be checked again after reloading without silently resubmitting.
6. After a verdict, any actor can append new counter-evidence within seven days of the first evaluation. Two rechecks maximum; six sources cumulative. No source or old verdict can be deleted. Submit and evaluate are separate transactions, so exact evidence is committed before interpretation.

MetaMask/EIP-1193 **Connect wallet** requests only `eth_requestAccounts`. It never signs, switches chains, sends transactions or requests token approvals. The connected wallet is not the isolated Studio signing account. Studio’s built-in account signs the primary pilot through Studio itself; its private key is never copied into ClaimTrace. You can also call the same five public methods directly in [GenLayer Studio](https://studio.genlayer.com).

## Verdict rules

| Verdict | Deterministic rule |
|---|---|
| CONTRADICTED | Any requirement is contradicted, a trail dimension is materially inconsistent, or a source materially contradicts the claim. Contradictions take precedence over favorable support. |
| VERIFIED | All requirements are supported, all four dimensions are consistent and all committed sources passed exact retrieval checks. |
| PARTIAL | At least one requirement is supported but VERIFIED conditions are not met, with no material contradiction. |
| INCONCLUSIVE | No requirement has sufficient usable support, with no material contradiction. |

The four trail dimensions are consistency, chronology, provenance and completeness. Missing evidence means UNKNOWN, not a fabricated contradiction. A documented correction may explain a discrepancy only if the evidence supports its chronology and authority.

## Deterministic safeguards

- Sequential on-chain claim IDs; owner-bound initial submission; immutable claim, owner, creation timestamp and requirements; per-account eight-claim and global 128-claim pilot limits.
- Fixed HTTPS raw.githubusercontent.com host, full lowercase 40-hex commit, safe path components; no userinfo, port, query, fragment, escapes, IP addresses or arbitrary domains.
- Strict source schemas, duplicate JSON-key rejection, no duplicate URLs or SHA-256 content, 12,000-byte maximum per document and six cumulative documents.
- Every response is checked for status, actual byte length and SHA-256 before strict UTF-8 decoding. Changed/oversized/unavailable/invalid-encoding evidence is explicitly fingerprinted and cannot support VERIFIED. Transient 429/5xx/network failures abort execution, retaining pending evidence for retry; failed evaluations do not consume a revision.
- Each source gets an assessment; each requirement and all four dimensions must be present. Decisive findings require exact 8–400-character quotes anchored to a supplied source. Invalid indices, invented quotes, incomplete coverage and unexpected fields fail validation. Each node has one bounded schema-repair pass; the repaired answer must pass the same checks or execution aborts. Missing proof is explicitly UNKNOWN, never automatically contradictory.
- The prompt frames claim, requirements and all retrieved content as untrusted data. No embedded instructions, external browsing or unsupported model memory is authorized. Deterministic grounding and independent re-execution provide defense in depth; prompt injection and model reasoning are not mathematically eliminated.
- Hash-linked append-only revisions bind the original claim, evidence set, submitter, evaluator, timestamps, all findings and previous revision. Permissionless evaluation has no authority to edit evidence or verdicts.

## Methods

| Method | Access | Purpose |
|---|---|---|
| `lock_claim(claim, requirements_json)` | Any account within pilot capacity | Create immutable claim; returns string ID. |
| `submit_evidence(claim_id, sources_json, reason)` | Owner initially; anyone for bounded challenges | Append new evidence and set pending evaluation. |
| `evaluate(claim_id)` | Permissionless | Independent retrieval/assessment and append a consensus revision. |
| `get_claim(claim_id)` | Public view | Complete JSON record, or `null`. |
| `get_count()` | Public view | Number of locked claims. |

Source schema: `[{"url":"https://raw.githubusercontent.com/OWNER/REPO/FULL_40_HEX_COMMIT/file.txt","sha256":"64_lowercase_hex","bytes":123}]`.

## Run and verify

Python 3.12+, Node 22+. Dependencies are pinned in `requirements.txt` and `package-lock.json`.

```sh
pip install -r requirements.txt
genvm-lint check contracts/claimtrace.py
mkdir -p ~/.cache/gltest-direct
cp ~/.cache/genvm-linter/genvm-universal-*.tar.xz ~/.cache/gltest-direct/
pytest -q
npm ci
npm test
npm run build
npm run dev
```

The SDK bundle copy reuses the linter’s verified release download because the published Direct Mode loader expects the older `genvm-universal` asset filename. This is an SDK cache compatibility step, not a mock replacement. CI runs the official GenLayer Direct Mode fixtures and linter. Web and LLM calls in unit tests are mocked; the live pilot is separate evidence of actual GenVM execution.

Read [architecture and security boundaries](docs/ARCHITECTURE.md) and [official API references used](docs/REFERENCES.md). The Python runner is pinned to the current official project boilerplate’s supported SDK hash and was validated in the deployed Studio instance.

## Honest limits and continued use

This is a working StudioNet development project, not production adjudication. Studio simulates stake, fees and consensus; test GEN has no monetary value. A commitment authenticates bytes, not truth or authorship. Only supplied sources are compared; undisclosed evidence can change the conclusion. Users should supply authoritative primary documents when claims concern real-world facts. A GitHub repository can publish an attributed document without proving the attributed author actually wrote it.

The SDK buffers web responses and exposes no streaming transfer cap or redirect-control option to contracts. ClaimTrace uses a Range header and rejects oversize/mismatched final bytes before parsing; it cannot guarantee a malicious server will not send a larger response or that the platform will not follow a redirect before returning it. The browser verifier does stream-bound reads and rejects redirects. Only a fixed trusted source host is allowed by the contract.

Model errors, prompt injection and correlated validator bias remain possible. Classification consensus requires agreement on structured statuses, not identical prose, and does not establish universal truth. An invalid or unavailable original source remains in the cumulative trail and continues to prevent VERIFIED, even after later valid evidence is appended. Permanent HTTP unavailability records INCONCLUSIVE/partial findings and may consume an evaluation; transport failures are retryable. Challenges are first-come and can consume the two available slots; there is no token bond or anti-Sybil identity claim. A challenger can add irrelevant bytes, but cannot remove earlier counter-evidence or overwrite history. Capacity and response limits bound cost; the 128-claim pilot capacity can be exhausted by multiple accounts.

The website’s isolated test account is intentionally ephemeral. It is not a production wallet, must never be funded with real assets, and is lost on reload. For ongoing identity, use the methods in Studio with a retained built-in account. A production release needs persistent user-controlled signing, authenticated source provenance, rate/bond policy, resource-bound HTTP support, external security review and testnet validation. A credible next step is organization-owned public evidence registries with scheduled, linked snapshot commitments and user-signed challenges; the current contract already preserves the audit trail those workflows require.
