driver: codex
updated: 2026-07-23T21:42+0900
task: T-205 nightly Codex/Claude benchmark refresh
status: ready-for-execution

## Now
- Branch `t205-nightly-agent-benchmark` starts clean from public `main`
  `edd585e991ae4348d82002bb6590fb035256633d`.
- Current clients are Codex CLI 0.145.0 and Claude Code 2.1.207. The previous
  GPT run used Codex 0.144.3; Claude's CLI version is unchanged.
- Benchmark selftest and five-capsule mutation/pristine audit pass. Historical
  summaries cover 90 GPT and 75 Claude singleton cells plus repeats.
- T-203 intentionally removed 89 old Claude raw artifact directories while
  retaining compact rows/summaries, so the raw artifact audit reports those
  historical pointers missing; this is prior archival state, not a new run
  failure.
- Driver sandbox selftest/audit and a real Codex Terra/low WBD-001 probe passed
  100/100 at 55.664 seconds and 13,586 effective tokens. One pair is not
  treated as a trend.
- Independent and reciprocal Claude evidence passed sealed import and receipt
  validation. The reconciled protocol is frozen in
  `tools/state/cowork/t205-nightly-20260723/reconciliation.md`.
- Historical complete singleton runtime is 5.73 hours across both providers.
  The execution rule prioritizes all 165 singleton cells, reevaluates the
  projection every 15 cells, and reserves the final 45 minutes for closeout.

## Working set
- `TODO.md`
- `tools/state/session.md`
- `README.md`
- `tools/agent-benchmark/`
- `tools/state/cowork/t205-nightly-20260723/`
- ignored `tools/agent-benchmark/artifacts/`

## Open questions
- None requiring owner input. Existing task definitions, previous matrices,
  and the explicit eight-hour execution request freeze the initial protocol.

## Awaiting user
- None.

## Next action
- Commit the frozen cowork exchange, advance the session to `executing`, then
  implement and test the generic matrix runner and non-bypass Claude route.
