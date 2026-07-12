driver: codex
updated: 2026-07-13T03:47+0900
task: T-69 audit non-color link identification
status: in-progress

## Now
- Goal: ensure inline content links are identifiable without relying only on color while preserving navigation, cards, logos, galleries, and the site's restrained visual style.
- Last done: T-68 classified all 38 tables, added 312 native row headers and 8 column headers, marked 8 layout tables presentational, enforced exact per-page semantics, matched accessibility-tree roles, and preserved exact cell/table geometry and computed styling at 390/1200px.
- Next: compute adjacent inline link/text color ratios and current text-decoration across all pages, group failures by structural context, then design the narrowest selector that underlines prose links without affecting navigation or image-only links.

## Working set
- All visible anchors and adjacent text contexts in light/dark modes; computed colors/decorations and structural selectors; any scoped CSS/cache bump/checker; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
