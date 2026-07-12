# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-38.

## Active

### T-33 — externalize repeated executable inline scripts
Move the repeated responsive-menu bootstrap from all 26 pages into a shared
deferred script, inventory remaining inline script types, and tighten
`script-src` as far as possible without disturbing JSON-LD or functionality.

### T-34 — add unobtrusive accessibility landmarks and skip navigation
Add consistent `header`, `nav`, `main`, and `footer` semantics plus a
keyboard-visible skip link across mirrored pages using existing containers and
minimal CSS. Preserve layout, navigation text, and visual identity; test EN/JP
desktop/mobile focus order.

### T-35 — complete image accessibility and loading hints
Resolve the four images without `alt`, classify decorative versus informative
text accurately, and add lazy loading only to below-the-fold images where it is
safe. Preserve gallery behavior and ensure above-the-fold logo/banner images
remain eager.

### T-36 — reduce obsolete presentational markup safely
Inventory deprecated HTML presentation attributes/elements and migrate only
high-confidence repeated patterns into existing CSS without changing computed
layout. Work in small mirrored batches with screenshot/computed-style checks.

### T-37 — add standards and accessibility regression tooling
Add deterministic local checks for document language, unique IDs, landmarks,
image alternatives, link/button semantics, and malformed local references;
document optional browser/validator checks and integrate stable offline rules
into pre-publish without adding deployed dependencies.

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

- 2026-07-13 T-32 found zero consumers of the packed dropdown code, removed all 26 dead loaders and `ddmenu_min.js`, validated a simultaneous report-only policy, then enforced CSP without `'unsafe-eval'`; representative live gallery/navigation/map/consent behavior remained clean (`d305d03`, `a24645c`).
- 2026-07-13 T-31 replaced all 26 JavaScript-only language controls with direct mirrored links, removed the unused loader/asset, made secret scanning deletion-safe, and verified keyboard/no-JavaScript navigation locally and live without visual or wording changes (`ac6c09b`).
- 2026-07-13 T-30 independently verified all three pinned CDN assets and their SHA-384/crossorigin tags on six gallery pages, confirmed the exact Playwright 1.61.1 lock has zero known vulnerabilities, added pre-publish offline and disposable online audit commands, documented trusted sources/quarterly cadence, and proved packages/tests/caches cannot enter deploy staging.
- 2026-07-13 T-26 inventoried all 27 public documents, deployed and browser-tested a narrow report-only CSP, then enforced it with `frame-ancestors 'none'`, restrictive Permissions Policy, and one-day HSTS without subdomains/preload; representative EN/JP home, gallery, research, map, and consent paths remain error-free (`a23a08e`, `3c9ef09`).
- 2026-07-13 T-29 added and published deterministic credential-free security checks for public references, mixed/sensitive URLs, external-link isolation, consent-loader/static pre-consent requests, secret/placeholder patterns, exact deploy staging, HTTPS redirects, headers, and excluded live paths; `publish.sh` now enforces the offline suite, and live mode correctly preserves visibility of T-28's sentinel blocker (`270d494`).
- 2026-07-13 T-27 removed and deployed one expired password-bearing meeting invitation from both news pages without replaying or logging its value; live pages are byte-identical to commit `0c7077b` with zero sensitive query/meeting URLs, while institutional professional contact remains intentionally public.
- 2026-07-13 T-24 removed stale model-evaluation/judge infrastructure, the redundant researchmap implementation report, all 41 tracked paper PDFs (261 MiB), and disposable local browser/npm/Python caches; removed all live references and corrected the preview-hook scope note.
- 2026-07-12 T-23 removed and deployed deletion of 26 unused Dreamweaver `.dwt` templates and all 264 `Instance*` control comments; all 26 live pages and the CV are byte-identical to commit `9636ff7`, with the template URL returning 404.
- 2026-07-12 T-18 owner confirmed GA4 event-data retention is 2 months and Google Signals/advertising features remain disabled; no credentials or account details were stored.
- 2026-07-12 T-21 enabled bounded native Codex delegation with minimal context forks, strict authority boundaries, output-first handoff, root review, and proportional verification; a zero-fork benchmark matched the root baseline and exposed one documentation omission that was fixed.
- 2026-07-12 T-20 replaced account-specific Claude preview hooks with a project-root-aware helper and verified simultaneous clone isolation, stale-PID ownership protection, and default port compatibility.
- 2026-07-12 T-22 audited website/CV/researchmap/ORCID fields, corrected the NII title and exporter parsing, standardized postal code 152-8550, removed the Keio RA role, rebuilt the CV, and completed the owner-reviewed researchmap and ORCID imports; transient outputs were removed.
- 2026-07-12 T-17 added pinned real-Chromium consent regression coverage for EN/JP desktop/mobile, keyboard use, persistence, revocation, and the zero-request-before-consent boundary; browser tooling and artifacts are deploy-excluded.
- 2026-07-12 T-16 hardened `publish.sh`: main/rebase/placeholder/dry-run gates, commit+push before deploy, clean-worktree push, phase-specific failure states, and seven isolated regression scenarios.
- 2026-07-12 T-15 aligned README, Claude/Codex role instructions, context ledger, publish playbook, and durable decision on standing direct-DRIVER authority versus dispatched/MCP worker prohibition.
- 2026-07-12 T-19 restored the README cluster quickstart with exact verified install/auth/clone/config/MCP/hook/check/launch commands; account-portability of the Claude preview hook remains T-20.
