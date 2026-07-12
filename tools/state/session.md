driver: codex
updated: 2026-07-13T04:42+0900
task: T-102 enforce names for every rendered data table
status: in-progress

## Now
- Goal: verify and permanently enforce that every rendered data table across all 26 routes has a useful accessible name.
- Last done: T-101 associated both student data tables with localized `sub002` headings, retained six faculty/secretary/alumni tables as presentational, and passed exact static, five layout/name browser, fast, and staging checks.
- Next: enumerate every browser-exposed table/name by route, confirm expected home/hardware/student/year/seminar inventory, reject empty/duplicate names within a route, and preserve presentation-table exclusion.

## Working set
- All routes' browser-exposed tables, accessible names, presentation-table exclusion, permanent regression coverage.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
