driver: codex
updated: 2026-07-24T02:09+0900
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
- Independent and reciprocal Claude evidence passed sealed import and receipt
  validation. The reconciled protocol is frozen in
  `tools/state/cowork/t205-nightly-20260723/reconciliation.md`.
- Generic 90-cell GPT and 75-cell Claude freeze plans validate. Selftest,
  capsule audit, focused matrix tests, and a bounded Claude denial-path probe
  pass.
- WBD-001 is complete: GPT 18/18 and Claude 15/15 full-score passes. GPT
  median time was nearly flat versus July; Claude improved 7%. Effective
  tokens rose 36% for GPT and about 5.2× for Claude, with unchanged public
  prompt/task hashes.
- WBD-002 is complete: GPT 18/18 and Claude 15/15 full-score passes. Median
  total time increased from 129.7 to 186.1 seconds for GPT and from 132.3 to
  146.7 seconds for Claude; both providers shared a roughly 26-second increase
  in browser-grader time, so the current runner/environment is a measured
  contributor independent of worker behavior.
- GPT WBD-003 is 18/18; Claude is 13/15 strict full-score: Opus/xhigh and
  Sonnet/xhigh each
  scored 89 because the static grader does not recognize their equivalent
  `rejectButton.focus()` implementation, although all browser tests passed.
  This is a confirmed literal-sensitive grader false negative, not a functional
  regression.
- GPT WBD-004 is complete at 18/18 full-score passes. The median total time
  increased 88.6 → 121.3 seconds; the increase is split across setup
  (4.0 → 6.5), worker (61.9 → 74.0), and grader (22.7 → 29.9), confirming
  multiple contributors. Claude WBD-004 is now executing.
- A separately labeled two-cell workflow correction is frozen for the two
  WBD-003 misses. It changes only inspection mode from `default` to `focused`
  and will run after both complete singleton matrices.
- The updated projection extends beyond the exact eight-hour boundary because
  WBD-004 and WBD-005 are the historically slowest blocks. A continuation
  guard extends the sequential controller through 05:10 so the exact frozen
  singleton denominators remain the priority and lets any started block finish;
  optional repeats remain deferred except for the two observed failures.

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
- Complete Claude WBD-004, then run frozen WBD-005 provider blocks
  sequentially. Execute the frozen two-cell focused workflow only after both
  complete grids, then analyze, obtain reciprocal Claude critique, update the
  README, validate, and publish through protected Git.
