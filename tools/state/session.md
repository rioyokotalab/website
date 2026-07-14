driver: codex
updated: 2026-07-14T10:17+0900
task: T-166 Repair and re-import ResearchMap JSONL | awaiting-user
status: awaiting-user

## Now
- ResearchMap rejected 86/318 lines because its bulk importer requires both
  JA and EN title slots: 5 inserts and 81 updates. The other 232 source lines
  were not listed in the error CSV and may already have applied.
- `tools/out/researchmap-import-retry-1.jsonl` contains exactly the 86 failed
  lines with only the missing title language added. Its SHA-256 is
  `2174570dda5226462439437f31fcbc5880f349dd0f789af06febec733421632a`.
- The exporter and retry generator now enforce the bilingual-title constraint;
  offline fixtures and an operation-by-operation retry audit pass.
- Managed-ID state must remain unchanged until the user confirms a successful
  retry. ResearchMap login/import remains manual.
- Obsolete `tools/out/` artifacts were removed at the user's request. The
  original import, error CSV, retry, analysis, and current driver report remain
  until the retry result is known.

## Working set
- `tools/out/errors_researchmap-import-6.csv`
- `tools/out/researchmap-import.jsonl`
- `tools/out/researchmap-import-retry-1.jsonl`
- `tools/out/researchmap-import-error-analysis-20260714.md`

## Open questions
- None.

## Awaiting user
- Upload only `tools/out/researchmap-import-retry-1.jsonl` and report whether
  ResearchMap accepts it. If it returns another error CSV, preserve and upload
  that CSV; do not re-upload the original 318-line file.
