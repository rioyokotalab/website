driver: codex
updated: 2026-07-12T11:11+0900
task: T-9 researchmap drift check (report only, NO import)
status: awaiting-user

## Now
- Goal: report the explicit public researchmap drift check without importing or interacting with the login UI.
- Last done: public API check regenerated a 29-record proposed-insert JSONL (2 papers, 13 media, 7 committees, 7 projects), with 0 updates/deletes and 2 ambiguous projects; driver report, metrics, and codex log are written.
- Next: wait for the user's explicit decision whether to manually upload the reviewed JSONL; do not import it automatically.

## Working set
- Files: tools/out/researchmap-import.jsonl; tools/out/t9-researchmap-drift.md; tools/todo.md; tools/state/session.md
- Scratch: tools/out/t9-researchmap-drift.md; tools/out/driver-report-20260712-1109.md
- Verify: 29 JSONL inserts, no updates/deletes; no import or login UI action.

## Open questions
- Whether to manually upload the reviewed 29-record JSONL through researchmap Settings > Import.

## Awaiting user
- Review `tools/out/researchmap-import.jsonl` and decide whether to manually upload it. This is explicit-only; no approval is carried forward.
