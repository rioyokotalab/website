driver: codex
updated: 2026-07-23T20:52+0900
task: T-205 nightly Codex/Claude benchmark refresh
status: planning

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
- The matrix runner's hard-coded freeze/artifact path and Claude's prior bypass
  invocation require correction before broad calls. Driver evidence is frozen;
  run the sealed blinded Claude evidence window next.

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
