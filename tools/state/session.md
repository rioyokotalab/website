driver: codex
updated: 2026-07-14T06:49+0900
task: T-160 Complete journal and book metadata | in-progress
status: in-progress

## Now
- T-157 is complete. Exhaustive evidence is in
  `tools/out/researchmap-missing-fields-20260714.{json,md}`; the ordered ledger
  now covers T-158--T-165.
- T-159 is complete: seven fixtures cover corrected ResearchMap schemas,
  balanced legacy/current profile syntax, and non-degrading merge semantics.
  The sanctioned live sync dry-run has 35 candidate inserts, 334 additive or
  corrective updates, zero deletes, and 22 ambiguous records held back.
- T-160 is using the exhaustive inventory to add only citation-evidenced
  metadata for sub001--sub003 and to classify structurally inapplicable gaps.
- Campaign window ends around 08:45 JST.

## Working set
- `en/achievements/index.html`, `jp/achievements/index.html`
- `tools/researchmap-export.py`, `tools/orcid-export.py`
- `tools/test-researchmap-export.py`, `tools/researchmap-state.json`
- `tools/todo.md`, `tools/state/session.md`, `tools/out/`

## Open questions
- None.

## Awaiting user
- None.
