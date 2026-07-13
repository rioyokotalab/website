driver: codex
updated: 2026-07-14T06:30+0900
task: T-159 Align complete ResearchMap field schemas | in-progress
status: in-progress

## Now
- T-157 is complete. Exhaustive evidence is in
  `tools/out/researchmap-missing-fields-20260714.{json,md}`; the ordered ledger
  now covers T-158--T-165.
- T-158 is complete: five fixtures, the 292-entry ResearchMap/ORCID dry runs,
  and the live comparison pass with current `id` headings.
- T-159 will correct schema mismatches confirmed against the public API (book
  ISBN under identifiers, presentation `location`, and profile field names),
  then expand safe sync ownership for every emitted complete field.
- Checkpoint/push the exporter repair, then implement fixture-first schema
  changes. Campaign window ends around 08:45 JST.

## Working set
- `tools/researchmap-export.py`, `tools/orcid-export.py`
- `tools/test-researchmap-export.py`, `tools/researchmap-state.json`
- `tools/todo.md`, `tools/state/session.md`, `tools/out/`

## Open questions
- None.

## Awaiting user
- None.
