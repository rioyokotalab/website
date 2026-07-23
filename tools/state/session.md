driver: codex
updated: 2026-07-24T01:24+0900
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
- WBD-002 is complete: GPT 18/18 and Claude 15/15 full-score passes. Median
  total time increased from 129.7 to 186.1 seconds for GPT and from 132.3 to
  146.7 seconds for Claude; both providers shared a roughly 26-second increase
  in browser-grader time, so the current runner/environment is a measured
  contributor independent of worker behavior.
- GPT WBD-003 is complete at 18/18 full-score passes. Claude WBD-003 is in
  progress: Fable is 5/5, Opus is 4/5, and Opus/max recovered its prior July
  singleton failure. Opus/xhigh scored 89 and missed only `reject-first-focus`;
  preserve it as a new singleton regression and run a matched repeat after the
  complete matrices before concluding whether it is stochastic.
- The 75-cell projection reaches approximately 05:02 JST. A continuation
  guard extends the sequential controller through 05:10 so the exact frozen
  singleton denominators remain the priority; optional repeats remain deferred
  except for observed failures.

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
- Complete Claude WBD-003, then run frozen WBD-004 and WBD-005 provider blocks
  sequentially. Preserve every singleton failure, repeat each observed failure
  under the matched workflow if time remains, then analyze complete matrices
  and update the README.
