driver: codex
updated: 2026-07-13T00:46+0900
task: T-53 complete locale-aware social metadata
status: in-progress

## Now
- Goal: make Open Graph URL/locale discovery agree exactly with canonical bilingual metadata without changing page content or layout.
- Last done: T-53 aligns all 27 og:url values with clean canonicals and adds exact primary/alternate en_US/ja_JP locales. Permanent checks cover root and all mirrored pages; full suite and representative EN/JP directory/profile browser head checks pass with unchanged 112px desktop header geometry.
- Next: rebase, inspect the 27-HTML metadata-only deployment preview, publish T-53, verify representative live heads, then close T-53 and seed the next queue.

## Working set
- Root plus all 26 EN/JP HTML heads, exact OG URL/locale standards checks, representative browser head/layout verification, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
