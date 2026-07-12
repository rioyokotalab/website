driver: codex
updated: 2026-07-13T00:46+0900
task: T-57 modernize remaining table presentation attributes
status: in-progress

## Now
- Goal: remove remaining table presentation attributes only in homogeneous, computed-style-verified groups while retaining heterogeneous widths and alignment until explicitly mapped.
- Last done: T-57 second batch maps all 91 table/cell widths to explicit percentage classes and removes 26 inert align=center attributes (an attempted centering class was rejected by geometry tests before publish). Zero legacy table presentation attributes remain. Full suite passes; representative EN/JP table/cell width, margin, x-position, and height are exact across home/News/member/computers at desktop/mobile.
- Next: rebase, inspect and publish the CSS/cache second T-57 checkpoint, verify representative live table layout, then close T-57 and start T-58 structural accessibility audit.

## Working set
- First batch: table border/cellpadding/cellspacing/bgcolor across home/News/member/computers plus shared CSS/cache. Second batch: exact width/center mappings. Regression checks and family/viewport geometry throughout.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
