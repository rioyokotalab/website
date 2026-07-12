# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-68.

## Active

### T-67 — normalize page titles and descriptions
Inventory bilingual title and description metadata for missing, duplicated, or
overlong values; make restrained page-local corrections only where search and
sharing context is ambiguous while preserving current wording wherever sound.

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

- 2026-07-13 T-66 added a deploy-manifest-aware gate for 1,676 local public URLs/fragments including directory indexes, same-origin absolutes, extended media attributes, and CSS assets, with positive/negative fixture tests (pending commit).
- 2026-07-13 T-65 scanned computed persistent text contrast on all 26 pages in light/dark modes, raised only the dark oral-highlight red from 3.12:1 to 6.61:1, removed one near-invisible stray EN hero character, and ended with zero scan failures (`b22cf0b`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-64 traversed 2,131 keyboard stops across all 26 pages at mobile/desktop, consolidated duplicate focus CSS into a palette-matched two-tone ring, and verified representative light/dark/component focus states (`3b01c7b`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-63 verified production HTML/CSS/JS/image responses have validators but no explicit caching or compression, added a repeatable read-only header audit, and avoided unverified Apache directives after the known 500 incident (`9eab2a1`).
- 2026-07-13 T-62 contained only the five narrow-screen page families with clipped legacy tables, made only live overflow regions keyboard-scrollable, preserved exact desktop table geometry, and passed 320/390px containment checks (`9771abb`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-61 gave all 143 Lightbox links unique localized page-local ordinal names, enforced exact order/count, and passed keyboard/pointer gallery checks (`803b27c`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-60 removed 26 empty keywords elements and 53 redundant HTML5 MIME type attributes, retained/parsed JSON-LD, enforced clean heads, and verified resources/scripts/layout (`f57c653`).
- 2026-07-13 T-59 deferred all 64 remaining external script references, permanently enforced defer, and passed consent/menu/pagetop/jQuery-Lightbox/CSP tests with no page errors (`c9b1e03`).
- 2026-07-13 T-58 fixed the EN home heading sequence, replaced one empty heading with a geometry-identical separator, localized all 143 Lightbox link names, removed three empty links, and added permanent heading/interactive-name checks (`282ba34`).
- 2026-07-13 T-57 eliminated all remaining legacy table presentation attributes in two computed-style-gated batches, mapped 91 widths and 8 header cells to classes, rejected an incorrect centering rule before publish, and preserved representative EN/JP layout exactly (`b5db8bb`, `c73d6b1`).
- 2026-07-13 T-56 migrated all 588 raw valign=top attributes across home/profile/News, enforced zero legacy and rendered counts, and preserved representative alignment/cell/row geometry within 1px across families/viewports (`ad217cb`).
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
