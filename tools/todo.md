# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-81.

## Active

### T-80 — replace obsolete member-table column sizing
Replace the final mirrored `<col width>` presentational attributes with a
shared semantic class, preserving the exact EN/JP biography-table geometry at
mobile/desktop and keeping print and narrow local-scroll behavior unchanged.

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

- 2026-07-13 T-79 removed 67 lines tied exclusively to nine absent legacy classes and one absent wrapper ID, added a repeatable source-reference gate for all 58 remaining classes and 13 IDs, and matched 60 baseline/working computed renders exactly across screen, dark, print, and forced-color states (pending commit).
- 2026-07-13 T-78 verified every public route at 320/1200px plus the root entry without JavaScript, kept content/navigation/images/gallery originals/contact metadata usable, hid the inert mobile hamburger only when JavaScript fails, and added two permanent regression tests; all 12 browser tests pass (`157b872`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-77 added tolerant rendered-layout contracts for 14 EN/JP representative routes at 320/390/900/901/1200px, plus runtime responsive-image density and local keyboard table scrolling checks; all four layout tests pass (`d5b424c`).
- 2026-07-13 T-76 added conventional npm test/test:browser/install commands with reviewed compatibility aliases, enforced the script surface, added EN/JP 900/901px menu and six-family print contracts, and passed all 8 browser plus fast security tests (`175d0b0`).
- 2026-07-13 T-75 wrapped pinned Lightbox with localized modal semantics, named controls/images, inert background, focus entry/trap/return, kept arrow/Escape/close behavior, passed first/next/last tests across six galleries, and added permanent Playwright coverage (`adac83b`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-74 enabled shared CSS for print, added a content-first A4 layer with plain page titles and constrained images/tables, hid navigation/sidebar/footer/fixed/consent/map/gallery chrome, eliminated all 1,920–3,276px overflow across 26 pages, and preserved exact screen geometry (`59586d6`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-73 verified all 26 pages reflow without page-level horizontal overflow at 640/320px effective widths and confirmed EN/JP consent/menu plus map, keyboard-scrolling tables, and fully measurable gallery close controls fit at 200%/400% equivalents (`cca4535`, audit-only).
- 2026-07-13 T-72 measured all 1,920 visible mobile targets at 320/390px; 946 small text links all passed the 24px center-spacing exception, while consent/menu/settings controls measured 48/55.5/35px and the hamburger 42px, so no layout-expanding CSS was warranted (`e76fee4`, audit-only).
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
