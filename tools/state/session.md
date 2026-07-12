driver: codex
updated: 2026-07-13T05:37+0900
task: T-76 standardize browser regression entry points
status: in-progress

## Now
- Goal: make browser validation discoverable through conventional commands and permanently cover responsive-menu and print contracts without bloating the fast structural suite.
- Last done: T-75 added a localized accessibility wrapper to pinned Lightbox with dialog/modal/name, named controls and changing image alternatives, inert background, focus entry/trap/return, and validated first/next/last behavior across all six galleries; four consent plus two new Lightbox Playwright tests pass.
- Next: inspect package scripts and test organization, add npm test/test:browser plus compatibility aliases, write compact EN/JP responsive boundary and print visibility/overflow tests, then run the full browser and fast security suites.

## Working set
- package.json/lock consistency, Playwright config/tests, responsive-menu EN/JP 900/901 and print media contracts, full browser/security verification; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
