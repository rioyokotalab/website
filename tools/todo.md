# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-44.

## Active

### T-40 — simplify the legacy menu JavaScript
Replace the 2015 classList compatibility implementation and global helper
surface with small modern DOM code scoped to the responsive menu. Preserve the
current 800px behavior and remove dead smartphone/screen helpers after browser
coverage proves equivalence.

### T-41 — improve back-to-top semantics and reduced-motion behavior
Give the arrow-only back-to-top link localized accessible text, use a stable
top target instead of an empty fragment, and respect `prefers-reduced-motion`
for transitions/scrolling without changing the visible circular control.

### T-42 — modernize root redirect metadata and fallback
Bring root `index.html` metadata in line with bilingual pages, add a no-script
fallback with direct EN/JP choices, and retain locale-aware redirect behavior
without a blank dead end. Preserve existing default-to-Japanese policy.

### T-43 — add canonical and alternate-language metadata
Add self-canonical plus reciprocal `hreflang="en"`, `hreflang="ja"`, and
`x-default` links to mirrored pages with exact URL/path verification. Ensure no
visible content or layout changes and extend standards enforcement.

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
