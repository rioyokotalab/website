driver: codex
updated: 2026-07-12T21:06+0900
task: T-12 add Google Analytics (GA4) to the website
status: in-progress

## Now
- Goal: complete T-12 with GA4 `G-DVRGG7FDLX` and privacy-first basic consent, then verify/push/publish.
- Last done: implementation verification passed, pull/rebase was current, and exact T-12 scope was committed as `4c8a20a`.
- Next: run and inspect deletion-bearing `./deploy.sh --dry-run`; if uploads/deletions are expected, run the interactive publish pipeline, push, and verify live pages/assets and consent behavior.

## Working set
- Site: `index.html`, 26 `en/**/*.html` + `jp/**/*.html`, 26 `Templates/*.dwt`, `js/analytics-consent.js`, `style.css`.
- Ledger/evidence: `tools/todo.md`, `tools/state/session.md`, `tools/state/decisions.md`, `tools/out/t12-ga.md`, `tools/out/t12-consent.py`.
- Sources: https://developers.google.com/tag-platform/security/concepts/consent-mode and https://developers.google.com/tag-platform/security/guides/consent.
- Verify: exact target/count/parity checks, JS syntax, browser/network consent behavior, local HTTP, scoped whitespace, dry-run deletion review, live check.

## Open questions
- None; consent text will disclose GA purpose, local choice storage, and a persistent change-settings control.

## Awaiting user
- None.
