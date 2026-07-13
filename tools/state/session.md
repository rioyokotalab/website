driver: codex
updated: 2026-07-14T07:18+0900
task: T-164 Generate and audit ResearchMap import | in-progress
status: in-progress

## Now
- T-157 is complete. Exhaustive evidence is in
  `tools/out/researchmap-missing-fields-20260714.{json,md}`; the ordered ledger
  now covers T-158--T-165.
- T-159 is complete: seven fixtures cover corrected ResearchMap schemas,
  balanced legacy/current profile syntax, and non-degrading merge semantics.
  The sanctioned live sync dry-run has 35 candidate inserts, 334 additive or
  corrective updates, zero deletes, and 22 ambiguous records held back.
- T-160--T-162 are complete: 24 mirrored rows now carry every safe value found
  in the local citations plus seven explicit title overrides. The remaining
  nominal gaps are documented as unknown, redundant, structurally
  inapplicable, or one of three conflicting citations held for a later lookup
  allowance.
- T-163 is complete: 309 citations per page now follow the majority format;
  30 arXiv-bearing entries per page have separate `[arxiv] [bibtex]` rows.
  Exact normalized citation semantics stayed unchanged and CRLF is intact.
- T-164 is auditing all 30 inserts and 338 additive/corrective updates; all 23
  ambiguous matches remain excluded and the planner emits zero deletes.
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
