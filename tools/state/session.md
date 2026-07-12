driver: codex
updated: 2026-07-13T04:00+0900
task: T-70 strengthen forced-colors compatibility
status: in-progress

## Now
- Goal: preserve visible controls, focus, boundaries, and selected/current states when user-agent forced colors replace the normal palette, without altering normal-mode presentation.
- Last done: T-69 measured all 183 visible main-content text links at only 1.43:1 versus surrounding text, added a thin underline scoped to #main, verified every content link in light/dark modes, left navigation/sidebar/footer/gallery visuals unchanged, and preserved geometry.
- Next: emulate forced-colors active on representative EN/JP desktop/mobile pages, inventory transparent/lost boundaries and state indicators for menus, consent, current links, focus, tables, and back-to-top, then add only targeted system-color overrides.

## Working set
- Representative home/news/computers/contact pages plus consent banner under forced colors; screenshots/computed system colors/focus/current state; any scoped media overrides/cache bump/checker; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
