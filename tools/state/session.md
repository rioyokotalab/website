driver: codex
updated: 2026-07-14T10:30+0900
task: T-166 Repair and re-import ResearchMap JSONL | idle
status: idle

## Now
- T-166 is complete: the user confirmed the corrected retry import succeeded.
- The sanctioned public API matched and recorded 379 IDs: 155 papers, four
  books, 42 presentations, 59 misc items, one award, 13 media items, 91
  committee memberships, and 14 projects.
- The read API still showed 18 inserts and 215 updates from the submitted plan,
  consistent with documented post-import lag. That residual was not uploaded
  and its generated JSONL was removed.
- `tools/out/` was cleared of the original import, error CSV, retry, prior
  reports, and analysis; generated Python bytecode was also removed.
- The repository is ready for a new task. T-167 remains deliberately held.

## Working set
- None.

## Open questions
- None.

## Awaiting user
- None.
