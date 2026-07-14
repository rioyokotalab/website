driver: codex
updated: 2026-07-14T14:34+0900
task: T-167 Resolve held metadata cases | idle
status: idle

## Now
- T-169 has moved to `/home/rioyokota/harness/TODO.md` and is no longer owned
  by this repository's board.
- T-167 resumed at the user's request from the verified offline checkpoint.
  The offline gates pass: 16 exporter fixtures, the full security suite,
  metadata idempotence, 309-entry/30-source-row normalization, and CRLF
  preservation.
- The fresh live attempt retrieved data and then stopped safely on candidate
  drift for the 2014 WCCM entry: expected no candidate, found
  `published_papers:39797632`. The exact ResearchMap record and the university
  researcher profile both identify that proceedings work, so its reviewed
  override changed from `distinct` to an exact `match`; the later journal
  article remains separate. Re-run offline checks, then rebuild the live plan.
- The rebuilt plan and independent fresh-API audit pass: 251 operations (25
  inserts, 226 additive updates), zero deletes, zero unresolved ambiguities,
  and all 29 reviewed classifications applied. Managed-ID state is unchanged.
  The full security suite, 38 browser tests, metrics schema, metadata checks,
  normalization checks, and CRLF checks pass. Check remote state and deployment
  preview next; stop on any conflict, destructive preview, or auth failure.
- T-167 is complete and published at `fd2f2d8`. The GitHub remote matches that
  commit, both live Achievements pages match local bytes exactly, and the live
  security gate passes. The reviewed import JSONL is retained for optional
  manual ResearchMap upload; no account write or managed-ID update occurred.

## Working set
- `/home/rioyokota/harness/TODO.md` at local commit `e76993d` (one commit ahead
  of its remote; no harness push was requested)
- `tools/out/researchmap-import.jsonl`
- `tools/out/researchmap-import-audit-20260714.md`
- `tools/out/researchmap-held-decisions-20260714.md`
- `tools/out/driver-report-20260714-1433.md`

## Open questions
- Five classified holds need human canonical-ID choices only if duplicate
  records should later be consolidated; their current operation-free state is
  safe.

## Awaiting user
- Optional: review and manually upload
  `tools/out/researchmap-import.jsonl` in ResearchMap. Its audited SHA-256 is
  `a76493bcd32f5233d40c66d5d6a846a795c953a05f617e8c52b469ffc8f37f16`.
