driver: codex
updated: 2026-07-12T22:55+0900
task: T-22 audit website/CV/researchmap/ORCID field mirroring
status: awaiting-user

## Now
- Goal: push the completed local T-22 decisions and hand off live deployment plus two manual external imports.
- Last done: standardized CV postal code 152-8550, removed the Keio RA role, rebuilt the 22-page CV PDF, and confirmed no supported automatic external writer exists in this repository.
- Next: verify full scope, commit and push the website/CV changes, then leave T-22 awaiting owner/Claude live deployment and the owner's manual researchmap/ORCID uploads. Codex must not run the deploy scripts.

## Working set
- Outputs: `tools/out/t22-field-reconciliation.md`, `tools/out/researchmap-import.jsonl`, `tools/out/orcid-works-selection.bib`; full comparison export `tools/out/orcid-works.bib`.
- Push scope: prior commit `1e96330` plus `cv/cv.tex`, rebuilt `cv/cv.pdf`, and current ledger/report updates. Verify exporter tests, repository-wide RA/address search, CV metadata, markdown budgets, and remote main; live deploy remains external.

## Open questions
- The repository has no researchmap WebAPI write client or configured credential interface; adding one would be separate credential-bearing scope. Do not inspect credentials or automate login.
- ORCID bulk update remains manual BibTeX import; never automate the login UI.

## Awaiting user
- T-18 requires owner access to GA Admin; no credentials should be shared.
- T-22 external files are owner-approved but require the owner to upload them manually; no credentials should be shared.
- T-22 pushed site/CV changes require the owner or Claude site-publisher to deploy them live.
