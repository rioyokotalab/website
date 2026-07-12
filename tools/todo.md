# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-59.

## Active

### T-56 — migrate obsolete vertical-alignment attributes
Replace all 588 `valign="top"` table-cell attributes with a shared class in
bounded page-family batches, retaining exact computed alignment and row sizes.

### T-57 — modernize remaining table presentation attributes
Inventory and migrate legacy table border, alignment, spacing, width, and
background attributes only where shared classes can preserve computed layout
exactly; split heterogeneous cases rather than normalizing content tables.

### T-58 — audit heading hierarchy and accessible names
Check all 26 pages for skipped/empty headings and unlabeled interactive
controls after the semantic migrations, fix only unambiguous structural issues,
and add page-level regression coverage without changing visible wording.

## Blocked / awaiting user

### T-28 — minimize deploy and web-server exposure
Positive-allowlist staging is deployed and verified: only 149 manifest files
can upload, rogue/stale remote paths delete, staging symlinks fail closed, and
the sentinel alone is preserved. The first server-layer `.htaccess` denial
attempt caused global HTTP 500 and was immediately rolled back in `0371605`.
Existing server config already denies directory listings and `.htaccess`, but
`.dont-remove-me` remains HTTP 200. Completing dotfile/source denial requires a
compatible Apache/vhost rule supplied by the server administrator; do not retry
unknown `.htaccess` directives on production.

### T-25 — purge archived PDF blobs from Git history
Rewritten main and all eight local evaluation tags contain zero `tools/papers/`
objects; GitHub main was lease-force-updated and fresh clones contain zero paper
paths. Local backup refs, reflogs, objects, and rollback bundle were removed.
GitHub still accepts a direct fetch of obsolete tip `78fe51a`, meaning its
unreferenced server cache has not yet garbage-collected the non-sensitive blobs.
GitHub documents that Support will not manually purge non-sensitive data; no
further repository action can force server-side GC. Existing clones should be
recloned or carefully reset to rewritten main.

## Recently completed

- 2026-07-13 T-55 migrated all 152 News nowrap attributes to a shared class, enforced zero legacy usage/exact EN/JP counts, and preserved representative cell/row geometry within 1px at desktop/mobile (`b59384a`).
- 2026-07-13 T-54 unified responsive JS/CSS at a non-overlapping mobile ≤900px/desktop ≥901px boundary, fixed the inert 801–900px hamburger, cache-busted assets, and passed EN/JP boundary/live checks (`4676d13`).
- 2026-07-13 T-53 aligned all 27 Open Graph URLs to clean canonicals, added reciprocal en_US/ja_JP locale metadata, enforced exact head values, and preserved representative layout (`1a8cd47`).
- 2026-07-13 T-52 added minimal robots and a generated 27-URL bilingual sitemap with three alternates per URL, integrated both into positive deployment/security checks, excluded repo-only paths, and verified every live destination (`d3ad764`).
- 2026-07-13 T-51 replaced 100 heading anchors and 200 News event anchors with semantic/same-position IDs, collision-safely preserved all historical aliases, eliminated legacy `name` markup, and matched representative fragment positions exactly at desktop/mobile (`8aa8582`, `02d5a3f`, `91a70fc`).
- 2026-07-13 T-50 added exactly one high fetch priority to each page's hero banner, enforced the classification, and preserved EN/JP home/subpage geometry within 1px at desktop/mobile (`c413ba6`).
- 2026-07-13 T-49 resolved 104 incomplete image-dimension occurrences from 60 verified local assets, preserved percentage/fixed presentation via shared classes, enforced valid dimensions, matched loaded geometry within 1px, and proved pre-load space reservation (`7850281`).
- 2026-07-13 T-48 migrated five style blocks, eleven style attributes, and runtime style mutations into shared classes; exact computed parity passed, a strict policy produced zero report-only violations across consent/menu/scroll/gallery/map tests, and CSP now enforces without style `unsafe-inline` (`4fa5652`, `c8bccd3`, `4650272`).
- 2026-07-13 T-47 paired all 155 lazy content images with asynchronous decoding, permanently enforced the relationship, and passed browser decode/load checks across news, portraits, research, galleries, and computer imagery (`579a41d`).
- 2026-07-13 T-46 added verified intrinsic 450x65 EN and 436x65 JP dimensions to all 26 header logos, enforced them, and preserved desktop/mobile geometry within 0.0625px (`d0a7d99`).
