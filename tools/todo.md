# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-87.

## Active

### T-86 — give the header home link an accessible name
Inspect the rendered accessibility tree for the logo/home link on every EN/JP
route; replace decorative empty logo alternatives with concise localized lab
names if the link is unnamed, while keeping its pixels and destination intact,
and add a permanent accessible-name contract.

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

- 2026-07-13 T-85 made long content links and home-news cells safely wrappable, restored missing JP Computers table containment/helper parity, and passed all 52 pages plus EN/JP consent under WCAG text-spacing overrides; fast checks and six affected browser contracts pass (pending commit).
- 2026-07-13 T-84 replaced the legacy -10px heading scroll margin with 24px after reproducing 27px of Japanese-heading clipping beneath the 81px sticky bar; every heading-target link passes at 320/900/901/1200px and all 18 browser tests pass (`919593a`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-83 added a permanent runtime-health contract over all 52 route/viewport loads, all mobile menus, and all gallery families, with zero uncaught exceptions, error-console messages, same-origin request failures, or local HTTP errors (`4efd88d`).
- 2026-07-13 T-82 found current-page specificity masking the forced-color keyboard ring and programmatic Lightbox close focus lacking `:focus-visible`, added two scoped system-highlight overrides, and permanently covers EN/JP nav/link/consent/menu/table/gallery paths; all 16 browser tests pass (`6e5fd56`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-81 suppressed every CSS transition to at most 0.01ms and Lightbox fades/resizing to 0ms only under reduced-motion preference, retained ordinary 600/600/700ms gallery timings, handled live preference changes, and added two permanent browser tests; all 14 browser tests pass (`b37c792`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-80 replaced the final two mirrored `<col width="72">` attributes with one shared class, expanded the legacy-attribute gate to `<col>`, and matched all EN/JP column/row/cell geometry exactly at 320/390/1200px and print (`17ddf92`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-79 removed 67 lines tied exclusively to nine absent legacy classes and one absent wrapper ID, added a repeatable source-reference gate for all 58 remaining classes and 13 IDs, and matched 60 baseline/working computed renders exactly across screen, dark, print, and forced-color states (`4d40725`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-78 verified every public route at 320/1200px plus the root entry without JavaScript, kept content/navigation/images/gallery originals/contact metadata usable, hid the inert mobile hamburger only when JavaScript fails, and added two permanent regression tests; all 12 browser tests pass (`157b872`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-77 added tolerant rendered-layout contracts for 14 EN/JP representative routes at 320/390/900/901/1200px, plus runtime responsive-image density and local keyboard table scrolling checks; all four layout tests pass (`d5b424c`).
- 2026-07-13 T-76 added conventional npm test/test:browser/install commands with reviewed compatibility aliases, enforced the script surface, added EN/JP 900/901px menu and six-family print contracts, and passed all 8 browser plus fast security tests (`175d0b0`).
- 2026-07-13 T-75 wrapped pinned Lightbox with localized modal semantics, named controls/images, inert background, focus entry/trap/return, kept arrow/Escape/close behavior, passed first/next/last tests across six galleries, and added permanent Playwright coverage (`adac83b`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-74 enabled shared CSS for print, added a content-first A4 layer with plain page titles and constrained images/tables, hid navigation/sidebar/footer/fixed/consent/map/gallery chrome, eliminated all 1,920–3,276px overflow across 26 pages, and preserved exact screen geometry (`59586d6`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-73 verified all 26 pages reflow without page-level horizontal overflow at 640/320px effective widths and confirmed EN/JP consent/menu plus map, keyboard-scrolling tables, and fully measurable gallery close controls fit at 200%/400% equivalents (`cca4535`, audit-only).
- 2026-07-13 T-72 measured all 1,920 visible mobile targets at 320/390px; 946 small text links all passed the 24px center-spacing exception, while consent/menu/settings controls measured 48/55.5/35px and the hamburger 42px, so no layout-expanding CSS was warranted (`e76fee4`, audit-only).
- 2026-07-13 T-71 kept seven 39.66MiB gallery originals as zoom targets, added visually inspected 720/1200px display variants (0.92/2.21MiB; 97.7%/94.4% reductions), enforced dimensions/byte budgets/source selection, and verified 1x/2x/3x EN/JP Lightbox behavior (`8189edf`; live publish reserved for user/Claude site-publisher).
- 2026-07-13 T-70 added distinct normal/forced-color current-page navigation, forced-color focus overrides, expanded the collapsed 22px dot-like menu control to a 42px three-bar target, and passed EN/JP 320/390/900/901px operation checks (`8c9748d`; live publish reserved for user/Claude site-publisher).
