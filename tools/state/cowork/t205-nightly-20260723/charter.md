# Charter

## Task

For eight hours beginning 2026-07-23 evening JST, rerun the README's
YOKOTA-Lab website-maintenance benchmark for both Codex and Claude, compare
matched current results with the retained July 2026 results, identify evidence
for changes in quality, runtime, and effective tokens, iteratively test
workflow improvements, and update the benchmark table and analysis from the
final validated evidence.

## Boundaries

- Target: `/home/rioyokota/projects/website`, task T-205, branch
  `t205-nightly-agent-benchmark`.
- Codex is driver and the only target writer; Claude Code is co-pilot.
- The five task mutations, F2P/P2P graders, critical assertions, and score
  thresholds remain unchanged. Never improve a score by weakening a task,
  grader, held-out gate, scope check, or failure classification.
- Use the same six model names and provider-supported effort levels shown in
  the existing README. Preserve provider-specific token caveats.
- Raw benchmark work occurs only in runner-created disposable capsules.
  Neither agent may deploy, publish the website, change hosting settings,
  inspect credentials or `.dont-remove-me`, automate login, or modify
  `/home/rioyokota/harness`.
- Ordinary task Git/PR publication is authorized after validation. No website
  deployment is in scope.
- Stop launching new cells by the reserved closeout boundary; preserve partial
  evidence rather than publishing an incomplete or incomparable table.

## Baseline and sandboxes

- Immutable target baseline:
  `edd585e991ae4348d82002bb6590fb035256633d`.
- Driver sandbox: `/home/rioyokota/.cache/t205-cowork/driver`.
- Co-pilot sandbox: `/home/rioyokota/.cache/t205-cowork/copilot`.
- Both are independent local clones checked out detached at the same baseline.
- The co-pilot stages are direct children of its sandbox. External seals and
  protected digest manifests live outside the target, exchange, and both
  sandboxes under `/home/rioyokota/.cache/t205-cowork-seals/`.
- Current clients: `codex-cli 0.145.0` and Claude Code `2.1.207`. The resolved
  co-pilot command uses Claude print mode, `dontAsk`, and a reviewed read/Bash
  tool list; it never uses `--dangerously-skip-permissions`.
- The staged exchange cannot enforce an OS boundary around Claude. Blinded
  staging, explicit authority, protected digests, a recoverable Git preimage,
  and receipt validation are the controls; this residual is recorded rather
  than described as equivalent to Codex confinement.

## Acceptance

1. Cowork independent and reciprocal evidence imports have valid external
   seals and receipts; reconciliation freezes one driver-executed protocol.
2. Benchmark selftest and capsule audit pass before calls. A low-effort visible
   capability probe passes for one model from each provider before broad runs.
3. Current and historical comparisons use identical task/grader identities,
   explicit client/model/effort/prompt/handoff/inspection identities, complete
   cell grids, and provider-internal token comparisons.
4. Improvements are selected from matched visible-task evidence, preserve all
   critical/P2P/scope gates, and reach the held-out task only after freezing.
5. Every published table denominator is backed by a complete validated matrix;
   failures and reruns remain visible rather than being overwritten.
6. `results.jsonl`, metrics, summaries, README, cowork receipts, and ledger
   validate; `git diff --check`, focused benchmark tests, the offline suite,
   browser suite where relevant, protected CI, and final diff review pass.
7. The protected PR merges without force-push. No deployment occurs. Raw
   artifacts and sandboxes are either retained with exact pointers or cleaned
   only through the applicable guarded workflow.
