driver: codex
updated: 2026-07-13T01:26+0900
task: T-39 make the mobile navigation control accessible
status: in-progress

## Now
- Goal: make mobile navigation keyboard-operable with correct localized semantics and unchanged appearance.
- Last done: T-39 functionality/tests pass. First publish attempt was explicitly aborted at confirmation after the separate Markdown check reported `tools/todo.md` over budget; nothing was committed or deployed. Pruned stale completed summaries per ledger protocol and removed stale active T-35 entry; current task history remains in Git.
- Next: re-run Markdown/security gates, preview/publish the unchanged T-39 implementation, verify live keyboard/ARIA state, then advance to T-40.

## Working set
- All 26 EN/JP pages, responsive menu JS/CSS, cache bump, browser/accessibility tests, ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
