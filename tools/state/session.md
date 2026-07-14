driver: codex
updated: 2026-07-14T15:00+0900
task: T-177 Repair ResearchMap import conflicts
status: awaiting-user

## Now
- Reconciliation is complete. ResearchMap similarity-merged eight reviewed
  distinct inserts into existing works: six later exact-ID updates were
  reported as HTTP 409, and two merges were silent. The audited repair is
  `tools/out/researchmap-import-retry-2.jsonl`: eight exact-ID corrective
  updates followed by eight forced distinct inserts, zero deletes, SHA-256
  `424050fa4ab0fad28c614c50cba4ac2f29406475294034c51c13226cb16403c1`.
- Upload only this 16-line retry. Never re-upload the original 251-line file;
  the other 245 rows were not reported as failed and may already have applied.
- Exporter sync inserts now fail closed: ordinary unmatched records use
  `merge`, while only explicit reviewed-distinct overrides use `force`.

## Working set
- `tools/out/errors_researchmap-import-8.csv`
- `tools/out/researchmap-import.jsonl`
- `tools/out/researchmap-import-audit-20260714.md`
- `tools/out/researchmap-import-retry-2.jsonl`
- `tools/out/researchmap-import-retry-2-audit.md`
- `tools/out/researchmap-import-8-silent-merge-plan.json`
- `tools/researchmap-retry-errors.py`

## Open questions
- Whether the 16-line repair imports without further provider-side errors.

## Awaiting user
- Manually upload only `tools/out/researchmap-import-retry-2.jsonl`, then report
  success or provide the new ResearchMap error CSV. Never automate the login.
