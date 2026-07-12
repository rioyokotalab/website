# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-76.

## Active

### T-73 — verify high-zoom reflow
Exercise representative EN/JP pages at browser-equivalent 200% and 400% zoom,
including open menus, consent, tables, maps, and galleries; fix only content
loss, overlap, or two-dimensional page scrolling while retaining normal layout.

### T-74 — modernize print presentation
Audit print previews for navigation clutter, fixed controls, consent UI, clipped
tables, and hidden destinations; add a small print-only layer that prioritizes
page content and useful link context without affecting screen presentation.

### T-75 — audit gallery dialog accessibility
Verify Lightbox focus entry, labeling, next/previous/close controls, keyboard
operation, focus containment, escape behavior, and focus return in EN/JP; add
local compatibility fixes only where the pinned library leaves a real gap.

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

- 2026-07-13 T-72 measured all 1,920 visible mobile targets at 320/390px; 946 small text links all passed the 24px center-spacing exception, while consent/menu/settings controls measured 48/55.5/35px and the hamburger 42px, so no layout-expanding CSS was warranted (audit-only).
- 2026-07-13 T-71 kept seven 39.66MiB gallery originals as zoom targets, added visually inspected 720/1200px display variants (0.92/2.21MiB; 97.7%/94.4% reductions), enforced dimensions/byte budgets/source selection, and verified 1x/2x/3x EN/JP Lightbox behavior (`8189edf`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-70 added distinct normal/forced-color current-page navigation, forced-color focus overrides, expanded the collapsed 22px dot-like menu control to a 42px three-bar target, and passed EN/JP 320/390/900/901px operation checks (`8c9748d`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-69 found all 183 visible main-content text links relied on a 1.43:1 color difference, added a thin content-only underline in light/dark modes, kept all site chrome unchanged, and preserved exact geometry (`d7e1d21`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-68 added 312 scoped row headers and 8 scoped column headers to genuine data tables, removed table semantics from 8 layout tables, enforced exact classification, matched accessibility-tree roles, and preserved exact computed geometry/styles (`5dccd09`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-67 corrected four route-mismatched titles, made all 26 bilingual titles/descriptions unique and page-local, mirrored them into Open Graph metadata, enforced structure/length/uniqueness, and preserved exact mobile/desktop geometry (`e79ab88`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-66 added a deploy-manifest-aware gate for 1,676 local public URLs/fragments including directory indexes, same-origin absolutes, extended media attributes, and CSS assets, with positive/negative fixture tests (`e0b6c66`).
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
