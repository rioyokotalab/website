driver: codex
updated: 2026-07-12T23:52+0900
task: T-23 remove legacy Dreamweaver templates
status: in-progress

## Now
- Goal: publish the verified removal of unused Dreamweaver templates and control comments.
- Last done: deletion-bearing live dry-run passed: 26 expected HTML uploads, the pending rebuilt CV PDF from T-22, and removal of the obsolete remote `Templates/` directory; no unrelated upload/deletion.
- Next: run `publish.sh`, confirm its repeated dry-run, then verify 26 live pages contain zero Dreamweaver markers, the live CV matches locally, the remote template path is absent, and GitHub main matches.

## Working set
- Scope: all 26 EN/JP HTML pages (comment-only edits), remove `Templates/`, update `README.md`, `AGENTS.md`, `CLAUDE.md`, `skills/html-editing.md`, ledger/bookkeeping.
- Publish gate: remote dry-run must show only 26 HTML uploads plus deletion of obsolete `Templates/`; stop on any other deletion or unexpected upload.

## Open questions
- No content-level HTML differences. `git diff --check` reports CRLF as trailing whitespace on changed legacy lines; byte comparison verifies exact marker-only transformation.

## Awaiting user
- None.
