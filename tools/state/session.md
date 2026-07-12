driver: codex
updated: 2026-07-13T03:31+0900
task: T-82 audit forced-colors component usability
status: in-progress

## Now
- Goal: verify every modernized interactive state remains distinguishable and operable when user colors override the palette.
- Last done: T-81 found reduced motion left global 150ms link transitions and Lightbox 600/600/700ms fades/resizing active; CSS now caps motion at 0.01ms and the wrapper sets gallery durations to zero only for the preference, restores defaults dynamically, and all 14 browser tests pass.
- Next: render EN/JP mobile/desktop components in forced colors; inspect system-color mapping, focus/current indicators, local overflow, modal controls and consent actions; add a permanent browser contract and only fix demonstrated failures.

## Working set
- EN/JP home/news/picture pages in forced-colors contexts; nav/focus/link/consent/table/Lightbox states; `style.css` only if a confirmed loss exists; Playwright/ledger bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
