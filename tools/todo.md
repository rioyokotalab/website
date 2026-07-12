# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-103.

## Active

### T-102 — enforce names for every rendered data table
Audit all routes in both languages through the browser accessibility tree;
ensure every non-presentational table has a nonempty contextual name while
layout tables remain excluded, and make the invariant permanent.

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

- 2026-07-13 T-101 associated both active-student data tables with their existing localized `sub002` headings, retained six rendered faculty/secretary/alumni tables as presentational, and passed exact static, five layout/name browser, fast, and staging checks (pending commit).
- 2026-07-13 T-100 added localized native visually-hidden captions to both Hinadori hardware tables, preserved their four column headers/specifications and 1×1 clipped caption geometry, and passed exact static, five layout/name browser, fast, and staging checks (pending commit).
- 2026-07-13 T-99 associated 22 yearly archive tables with their existing localized year headings, named two nested seminar-details tables, and passed exact static, five layout/name browser, fast, and staging checks (pending commit).
- 2026-07-13 T-98 added localized native visually-hidden captions to the two home-news tables, preserved 1×1 clipped geometry and all 48 rendered row headers, and passed exact static, five layout/name browser, fast, and staging checks (pending commit).
- 2026-07-13 T-97 proved the mirrored empty `#gallery` hooks had no runtime/navigation consumers, removed both hooks and five dead selector families while preserving live frame rules, synchronized root/route cache versions, and passed CSS-source, six layout/no-JS, fast, and staging checks (pending commit).
- 2026-07-13 T-96 classified seven empty semantic containers, retained three spacing paragraphs and two CSS-referenced gallery hooks, removed only two zero-purpose Japanese profile articles, and passed exact static, five layout/runtime, fast, and staging checks (pending commit).
- 2026-07-13 T-95 removed 20 empty legacy `tbody` artifacts from the EN/JP news archives while retaining all three nonempty explicit sections and every row, and passed source/rendered-DOM, five layout/browser, fast, and staging checks (pending commit).
- 2026-07-13 T-94 added valid ISO/native time semantics to 96 English and 100 Japanese single-day archive dates, preserved four legacy styled separators and all four visible multi-day ranges, and passed exact static, five layout/browser, fast, and staging checks (pending commit).
- 2026-07-13 T-93 added valid ISO/native time semantics to all 32 rendered English and 14 rendered Japanese home-news dates, deliberately excluded 18 commented Japanese historical rows, and passed exact static, five browser/layout, fast, and staging checks (pending commit).
- 2026-07-13 T-92 identified the two mirrored CV downloads as `application/pdf`, retained their explicit labels/new-tab behavior, and passed exact static, two route-wide browser, fast, and staging checks (pending commit).
- 2026-07-13 T-91 wrapped the unchanged EN/JP postal, telephone, and email text in native address semantics, kept maps outside, neutralized default italics, and passed exact static, five browser/layout, fast, and staging checks (pending commit).
- 2026-07-13 T-90 added exact destination-language metadata to all 26 visible EN↔JP switches, enforces mirrored href/text/hreflang triples statically, and passed two route-wide browser contracts plus fast and staging checks (pending commit).
- 2026-07-13 T-89 traversed every focusable element on all 26 routes at 390/1200px in both directions, found the floated header logo left its link with a 0×0 focus box, gave that anchor containing geometry without moving the layout, and passed the 50.8-second exhaustive keyboard contract plus six layout/forced-color contracts (pending commit).
- 2026-07-13 T-88 inventoried all 207 image elements and their link/caption context, removed one Japanese machine-generated placeholder from an English decorative event image, and now enforces the exact localized image-role set across all 26 routes; fast checks and two route-wide browser contracts pass (pending commit).
- 2026-07-13 T-87 replaced 26 CSS-hidden institutional headings with metadata, added one localized native off-screen `h1` per page without changing the visible H2→H3 structure, and passed exact static gates plus seven route/layout/no-JS browser contracts (pending commit).
- 2026-07-13 T-86 confirmed all 26 header logo/home links were unnamed in the accessibility tree, added concise localized logo alternatives without visual changes, enforced parity, and passed route-wide name/runtime plus fast checks (pending commit).
