driver: codex
updated: 2026-07-13T03:27+0900
task: T-81 audit reduced-motion behavior
status: in-progress

## Now
- Goal: ensure reduced-motion preference suppresses every nonessential local and gallery transition while preserving immediate, understandable state changes.
- Last done: T-80 replaced the two mirrored obsolete member `<col width="72">` attributes with `.member-table-column`, expanded the standards gate to reject width/alignment on `<col>`, and matched all column/row/cell geometry exactly in eight EN/JP screen/print pairs.
- Next: inventory computed transition/animation/scroll behavior across representative pages, open menu/consent/Lightbox states under normal and reduced preferences, then add only scoped overrides for confirmed residual motion and a browser regression contract.

## Working set
- `style.css`, `js/pagetop.js`, pinned Lightbox runtime states, responsive menu and consent components, Playwright motion tests, cache/ledger bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
