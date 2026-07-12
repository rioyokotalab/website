driver: codex
updated: 2026-07-13T03:46+0900
task: T-85 audit user text-spacing resilience
status: in-progress

## Now
- Goal: ensure users can expand text spacing without clipped content, overlap, page-level horizontal scrolling, or unusable controls.
- Last done: T-84 reproduced EN headings landing 2.5px and JP headings 27px under sticky navigation; `scroll-margin-top` is now 24px, all heading-target links land below the bar at four boundaries, and all 18 browser tests pass.
- Next: inject line-height 1.5, paragraph spacing 2em, letter spacing 0.12em and word spacing 0.16em across all 26 pages at 320/1200px; measure overflow, element text clipping/overlap, mobile menus, consent and galleries; fix only demonstrated hard constraints and retain the audit.

## Working set
- all public text-bearing elements and component controls under user spacing overrides at mobile/desktop; page/element geometry; Playwright and any narrowly implicated CSS; ledger/test bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
