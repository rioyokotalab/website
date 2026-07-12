driver: codex
updated: 2026-07-13T04:30+0900
task: T-96 remove empty semantic article artifacts
status: in-progress

## Now
- Goal: remove semantically misleading empty containers only when they have no visual or runtime purpose.
- Last done: T-95 removed 20 empty EN/JP news `tbody` artifacts, retained all three nonempty explicit sections and every row, and passed source/rendered-DOM, five layout/browser, fast, and staging checks.
- Next: classify empty articles/sections/paragraphs by computed geometry and selector/runtime references; remove only zero-geometry unreferenced articles and preserve spacing paragraphs/gallery hooks.

## Working set
- Empty semantic containers, computed geometry, selector/runtime references, standards/layout tests.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
