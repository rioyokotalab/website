driver: codex
updated: 2026-07-12T22:41+0900
task: T-22 audit website/CV/researchmap/ORCID field mirroring
status: awaiting-user

## Now
- Goal: review and decide the external/profile follow-ups from the completed T-22 field audit.
- Last done: produced the field matrix, 29-line researchmap queue, and nine-work ORCID selection; corrected the EN NII title and the exporter arXiv venue parse. Exporter tests and parity checks pass.
- Next: owner reviews the three T-22 output files and decides whether to perform the manual researchmap/ORCID imports, which postal code is authoritative, and whether the Keio RA role belongs on the website.

## Working set
- Outputs: `tools/out/t22-field-reconciliation.md`, `tools/out/researchmap-import.jsonl`, `tools/out/orcid-works-selection.bib`; full comparison export `tools/out/orcid-works.bib`.
- Committed scope pending: `en/member/yokota.html`, `tools/researchmap-export.py`, ledger/bookkeeping. Verify exporter tests, CRLF preservation, EN/JP parity, markdown budgets, and diff.

## Open questions
- CV postal code 152-8500 conflicts with website 152-8550; no authoritative resolution was found in this pass.
- CV includes a Keio RA role absent from the website; intent is unknown.

## Awaiting user
- T-18 requires owner access to GA Admin; no credentials should be shared.
- T-22 requires owner review of the generated external import selections and two profile-scope decisions; no credentials should be shared.
