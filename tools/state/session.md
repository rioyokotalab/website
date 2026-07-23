driver: codex
updated: 2026-07-23T22:45+0900
task: T-205 nightly Codex/Claude benchmark refresh
status: executing

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
- Generic 90-cell GPT and 75-cell Claude freeze plans validate. Selftest,
  capsule audit, focused matrix tests, and a bounded Claude denial-path probe
  pass.
- The first frozen capability cell for each provider passed 100/100. The
  remaining visible singleton blocks are executing sequentially.
- WBD-001 is complete: GPT 18/18 and Claude 15/15 full-score passes. GPT
  median time was nearly flat versus July; Claude improved 7%. Effective
  tokens rose 36% for GPT and about 5.2× for Claude, with unchanged public
  prompt/task hashes.
- The 30-cell provider-specific projection reaches approximately 04:03 JST.
  Optional repeats are deferred; complete singleton denominators remain the
  priority.

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
- Continue the autonomous WBD-002 through WBD-004 provider blocks, reassess
  failures/projection every 15 cells, then release frozen WBD-005 only if the
  complete matrices remain feasible.
