driver: codex
updated: 2026-07-14T15:16+0900
task: T-177 Repair ResearchMap import conflicts | idle
status: idle

## Now
- T-177 is complete: the user confirmed the audited repair imported
  successfully, and the sanctioned public API exposes all eight forced records
  as IDs `54390630`--`54390637`.
- The managed registry now contains 411 visible IDs: 172 papers, four books,
  44 presentations, 60 misc items, one award, 13 media items, 98 committee
  memberships, and 19 projects.
- The live refresh proposed five residual inserts. They were not uploaded; the
  generated residual and every import/error/retry/audit scratch artifact were
  removed, along with ResearchMap bytecode.
- Reviewed overrides now select the correct IDs on both sides of each distinct
  pair. Reusable fail-closed exporter behavior and regression tests remain.

## Working set
- None.

## Open questions
- None.

## Awaiting user
- None.
