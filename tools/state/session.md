driver: codex
updated: 2026-07-24T02:51+0900
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
- WBD-001/002 are full-score for both providers. GPT WBD-001 time was flat;
  Claude improved 7%. WBD-002 slowed for both, including a shared roughly
  26-second browser-grader increase.
- GPT WBD-003 is 18/18; Claude is 13/15 strict full-score: Opus/xhigh and
  Sonnet/xhigh each
  scored 89 because the static grader does not recognize their equivalent
  `rejectButton.focus()` implementation, although all browser tests passed.
  This is a confirmed literal-sensitive grader false negative, not a functional
  regression.
- WBD-004 is complete at GPT 18/18 and Claude 15/15 full-score passes. GPT
  median total time
  increased 88.6 → 121.3 seconds; the increase is split across setup
  (4.0 → 6.5), worker (61.9 → 74.0), and grader (22.7 → 29.9), confirming
  multiple contributors. Claude median total time increased 112.5 → 135.9
  seconds and worker time 63.2 → 88.6; Read-before-Edit retries and direct
  kernel NFS waits were observed.
- A separately labeled two-cell workflow correction is frozen for the two
  WBD-003 misses. It changes only inspection mode from `default` to `focused`
  and will run after both complete singleton matrices.
- GPT WBD-005 and its full 90-cell matrix are complete. WBD-005 improved
  13/18 → 14/18 strict and 17/18 → 18/18 browser-functional: five prior routes
  recovered (including Terra/xhigh's browser failure); four new 91s all pass
  the browser suite and use an equivalent form missed by `js-reduced-zero`.
- Claude's full 75-cell matrix is complete at 71/75 strict and 74/75
  browser-functional. The prior matrix was 72/75 strict and the same 74/75
  functional. Three current strict misses are browser-correct static-grader
  blind spots; Sonnet/low WBD-005 is one genuine functional regression.
- Exact-grid analysis and matched comparison reports validate. Three separately
  labeled focused cells are next: the two WBD-003 syntax misses and the
  Sonnet/low WBD-005 functional failure.

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
- Execute the three frozen focused cells, analyze, obtain reciprocal Claude
  critique, update the README, validate, and publish through protected Git.
