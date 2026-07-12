driver: codex
updated: 2026-07-13T02:28+0900
task: T-64 audit keyboard focus visibility
status: in-progress

## Now
- Goal: ensure every keyboard-reachable control has a visible, unobscured focus indicator using the existing palette and no geometry-changing restyle.
- Last done: T-63 sampled production delivery with compressed GET and HEAD requests, confirmed validators but no explicit caching/compression, added a repeatable read-only audit tool, and declined risky unverified Apache changes.
- Next: render representative EN/JP pages at desktop/mobile, tab through all reachable controls and measure focus outline/box-shadow plus viewport occlusion; inventory confirmed failures before editing CSS.

## Working set
- Representative EN/JP home/news/research/contact/picture/profile pages; computed focus styles and viewport geometry; any shared focus-visible CSS/cache bump/checker; ledger/bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
