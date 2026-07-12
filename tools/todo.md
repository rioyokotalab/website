# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-49.

## Active

### T-48 — remove remaining inline presentation styles
Migrate repeated inline style blocks and `style` attributes to narrowly scoped
shared classes, preserve representative computed styles, then remove
`'unsafe-inline'` from the CSP style policy after report-only and browser gates.

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

- 2026-07-13 T-47 paired all 155 lazy content images with asynchronous decoding, permanently enforced the relationship, and passed browser decode/load checks across news, portraits, research, galleries, and computer imagery (`579a41d`).
- 2026-07-13 T-46 added verified intrinsic 450x65 EN and 436x65 JP dimensions to all 26 header logos, enforced them, and preserved desktop/mobile geometry within 0.0625px (`d0a7d99`).
- 2026-07-13 T-45 added localized accessible map titles, moved embed presentation into shared CSS, permanently enforced the contract, and preserved exact desktop/mobile dimensions (`d8c111a`).
- 2026-07-13 T-44 marked exact current destinations for assistive technology in desktop/mobile navigation, permanently enforced linked/mobile-only/unlinked states, and preserved header geometry (`227fef0`).
- 2026-07-13 T-43 added exact self-canonical and reciprocal EN/JA/x-default metadata to all 26 pages, permanently enforced mirrored mappings, and passed representative no-layout-change browser checks (`966b87b`).
- 2026-07-13 T-42 modernized root metadata, removed an invalid empty meta element, and added a styled bilingual no-script fallback; browser checks preserved EN/JP/non-English routing and verified the fallback (`3c97aae`).
- 2026-07-13 T-41 gave every back-to-top control a stable target and localized accessible name, honored reduced-motion preferences in CSS/JS, and added permanent regression coverage; normal and reduced-motion browser behavior passed in EN/JP (`0569865`).
- 2026-07-13 T-40 folded responsive navigation into one scoped modern script, removed 26 obsolete loaders and the 2015 global/polyfill asset, and corrected desktop button visibility caught by regression; EN/JP keyboard/pointer and desktop/mobile behavior passed (`7e7e940`).
- 2026-07-13 T-39 replaced all 26 decorative hamburger divs with localized real buttons, synchronized `aria-expanded`, preserved geometry within 1px, and permanently enforced the accessible control contract (`4c6748f`).
- 2026-07-13 T-36 migrated all 145 uniform `<p align="center">` instances to a shared semantic class; computed centering and representative wrapper geometry remained identical, while heterogeneous table layout attributes were intentionally retained (`75a215c`).
- 2026-07-13 T-37 added zero-dependency standards/accessibility enforcement for mirrored paths, languages, unique IDs, landmarks/navigation/skip links, image semantics/loading, fragments, stylesheet versions, and safe script/link semantics; it now runs automatically before every publish.
- 2026-07-13 T-38 replaced duplicated desktop/mobile `topnav` IDs with a shared class across all 26 pages and aligned two duplicated EN event anchors with JP; every ID is unique, fragments are distinct, and menu geometry stayed within 1px (`9a44e31`).
- 2026-07-13 T-35 completed image alternatives with localized professor portrait text and decorative alternatives for redundantly captioned gallery images; all content images remain lazy while logos/heroes remain eager (`d44f862`).
- 2026-07-13 T-34 added semantic header/main/footer landmarks, distinct navigation labels, and localized keyboard-visible skip links to all 26 pages; desktop/mobile geometry stayed within 1px of baseline and live returning-visitor focus reaches main without altering privacy-banner focus (`d94effd`).
- 2026-07-13 T-33 externalized all 26 repeated responsive-menu bootstraps and the root language redirect, verified EN/JP redirect/mobile/consent behavior 7/7, passed a live report-only gate, then enforced `script-src` without `'unsafe-inline'`; only inert JSON-LD remains inline (`557d795`, `f682185`).
- 2026-07-13 T-32 found zero consumers of the packed dropdown code, removed all 26 dead loaders and `ddmenu_min.js`, validated a simultaneous report-only policy, then enforced CSP without `'unsafe-eval'`; representative live gallery/navigation/map/consent behavior remained clean (`d305d03`, `a24645c`).
- 2026-07-13 T-31 replaced all 26 JavaScript-only language controls with direct mirrored links, removed the unused loader/asset, made secret scanning deletion-safe, and verified keyboard/no-JavaScript navigation locally and live without visual or wording changes (`ac6c09b`).
- 2026-07-13 T-30 independently verified all three pinned CDN assets and their SHA-384/crossorigin tags on six gallery pages, confirmed the exact Playwright 1.61.1 lock has zero known vulnerabilities, added pre-publish offline and disposable online audit commands, documented trusted sources/quarterly cadence, and proved packages/tests/caches cannot enter deploy staging.
