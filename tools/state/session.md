driver: codex
updated: 2026-07-13T03:59+0900
task: T-86 give the header home link an accessible name
status: in-progress

## Now
- Goal: ensure the prominent header logo/home link has a concise localized accessible name on every route without visual changes.
- Last done: T-85 found expanded long URLs clipped by content clear-fixes, added wrapping to main links/home-news cells, and uncovered missing JP Computers containment/helper parity; all 52 spaced route states and EN/JP consent pass, as do fast and six affected browser contracts.
- Next: query accessible names for `.htitle > a` across all routes, confirm the empty logo alt plus CSS-hidden descendants leave it unnamed, add localized EN/JP alternatives only where required, enforce exact parity, and retain a browser test.

## Working set
- the 26 `.htitle > a` logo links and their EN/JP logo images; accessibility tree/name computation; mirrored HTML, standards and Playwright bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
