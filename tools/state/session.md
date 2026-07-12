driver: codex
updated: 2026-07-13T00:46+0900
task: T-57 modernize remaining table presentation attributes
status: in-progress

## Now
- Goal: remove remaining table presentation attributes only in homogeneous, computed-style-verified groups while retaining heterogeneous widths and alignment until explicitly mapped.
- Last done: T-57 first batch removes 40 table border, 12 cellpadding, 12 cellspacing, one redundant image border, and migrates 8 gray cells to `.table-heading-cell`; permanent checks reject all four legacy attributes. Full suite passes; EN/JP home/News/member/computers table styles/geometry are exact at desktop/mobile, as are heading-cell colors/weights and the image border.
- Next: rebase, inspect/publish the first T-57 CSS/cache checkpoint, verify live attributes, then map 91 heterogeneous widths and 26 table center alignments to explicit shared classes for the second batch.

## Working set
- First batch: table border/cellpadding/cellspacing/bgcolor across home/News/member/computers plus shared CSS/cache. Second batch: exact width/center mappings. Regression checks and family/viewport geometry throughout.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
