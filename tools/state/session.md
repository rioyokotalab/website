driver: codex
updated: 2026-07-13T04:40+0900
task: T-101 name active-student data tables
status: in-progress

## Now
- Goal: expose localized contextual names for the two student data tables while leaving layout-only member tables semantically presentational.
- Last done: T-100 added native localized visually-hidden captions to both Hinadori hardware tables, preserved four headers/specifications and clipped geometry, and passed exact static, five layout/name browser, fast, and staging checks.
- Next: distinguish active student tables from commented postdoc and role=presentation faculty/secretary/alumni tables, associate only the data tables with `sub002`, and verify accessible table inventory/geometry.

## Working set
- EN/JP member tables, `sub002` headings, data versus presentation roles, accessible inventory and geometry.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
