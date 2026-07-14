driver: codex
updated: 2026-07-14T10:41+0900
task: T-168 Relocate benchmark artifacts and clear transient output | idle
status: idle

## Now
- T-168 is complete. The 173 raw benchmark directories were required by 173
  metric pointers and the benchmark artifact audit, so they were moved to
  ignored `tools/agent-benchmark/artifacts/` rather than deleted.
- The move preserved all 1,102 files before the required path normalization;
  producers, documentation, compact results, raw results, and metrics now use
  the benchmark-owned path. Artifact, capsule, metrics, and security checks
  pass. `tools/out/` is empty.

## Working set
- None.

## Open questions
- None.

## Awaiting user
- None.
