# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-31.

## Active

### T-26 — harden HTTP response headers and CSP
Inventory every inline script/style, external origin, iframe, form, and browser
feature used by the 26 public pages; design and deploy a Content-Security-Policy
that preserves the site and privacy-first consent flow. Add modern
`Permissions-Policy`, CSP `frame-ancestors`, and a cautious HSTS rollout only
after confirming HTTPS coverage; do not enable `includeSubDomains` or preload
without separately verifying every subdomain. Test headers and browser behavior
locally and live before tightening from report-only to enforcement.

### T-28 — minimize deploy and web-server exposure
Convert the current broad mirror into a verified deploy allowlist or equivalent
fail-closed exclusion scheme so only public HTML/assets, `cv/cv.pdf`, and
required server files can reach `www/`. Disable directory listing and access to
dotfiles, source/config/backup/temp/map files at the server layer; add isolated
regression fixtures proving unexpected root files cannot be uploaded and remote
public files cannot be accidentally deleted.

### T-29 — add continuous security regression checks
Create a credential-free security test command covering HTTPS redirects,
required response headers, forbidden/mixed-content URLs, external-link rel
attributes, local path traversal/broken references, deploy-excluded leakage,
known placeholder IDs, secret-pattern scanning with reviewed allowlists, and
privacy-first zero-request-before-consent behavior. Make it deterministic and
run it from the pre-publish pipeline without introducing network writes.

### T-30 — audit third-party and test-tool supply chain
Verify every CDN resource is HTTPS, version-pinned, and protected by correct SRI
and `crossorigin`; evaluate whether self-hosting the small Lightbox/jQuery
dependency set reduces risk. Add repeatable npm lockfile/audit checks for
Playwright tooling, document update cadence and trusted sources, and ensure no
test dependency or cache can enter the deployed tree.

## Blocked / awaiting user

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

- 2026-07-13 T-27 removed one expired password-bearing meeting invitation from both news pages without replaying or logging its value; current tracked key/token/query scans, CV metadata, and 107-image GPS/metadata scans are clean, while institutional professional contact remains intentionally public.
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
