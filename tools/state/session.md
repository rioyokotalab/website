driver: codex
updated: 2026-07-13T00:46+0900
task: T-56 migrate obsolete vertical-alignment attributes
status: in-progress

## Now
- Goal: replace all 588 valign=top cell attributes with a shared class while preserving exact vertical alignment and row geometry across three page families.
- Last done: T-56 migrates all 588 raw valign=top attributes to `.vertical-top` across home/profile/News and permanently enforces zero legacy plus active-DOM counts (36 JP-home instances are inside a historical comment). Full suite passes; representative EN/JP cells retain top alignment and cell/row geometry within 1px across all three families at desktop/mobile.
- Next: rebase, inspect the six-page/CSS/cache deployment preview, publish T-56, verify representative live alignment, then close T-56 and scope T-57 presentation attributes by safe homogeneous groups.

## Working set
- Six EN/JP home/profile/News pages, `.vertical-top` CSS/cache bump, exact standards counts, representative family/viewport geometry, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
