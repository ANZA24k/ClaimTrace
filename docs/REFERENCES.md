# Official references inspected before implementation

Reviewed 2026-10-26:

- https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism — deterministic boundaries; custom leader/validator execution and `gl.vm.Return.calldata`.
- https://docs.genlayer.com/developers/intelligent-contracts/features/web-access — nondeterministic HTTP requests and response handling.
- https://docs.genlayer.com/api-references/genlayer-test/direct — official Direct Mode deploy fixtures, web/LLM mocks, timestamps and validator re-execution.
- https://docs.genlayer.com/developers/intelligent-contracts/tooling-setup — testing and `genvm-lint check` workflow.
- https://docs.genlayer.com/api-references/genlayer-linter — lint and ABI/storage validation.
- https://github.com/genlayerlabs/genlayer-project-boilerplate — supported Python SDK runner pin, project tooling and current JS integration.
- https://github.com/genlayerlabs/genvm — actual pinned Python SDK `gl.nondet.web.request` implementation, including `Response.status`, byte body and lack of streaming/redirect options.
- Installed `genlayer-js@1.1.8` source and type definitions — StudioNet chain 61999, `latest-final` reads, zero-value signed writes, returned consensus transaction IDs and lifecycle status mapping.

SDK/lint informational note: a newer Python runner exists; ClaimTrace uses the supported hash supplied by the official project boilerplate and verified by lint, Direct Mode and actual Studio deployment. Documentation snippets differ in some response-property examples; the exact pinned SDK source and successful tests are authoritative for this implementation.
