# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-26.

## Active

### T-25 — purge archived PDF blobs from Git history
Rewrite all branches and eight preserved evaluation tags to remove every
historical `tools/papers/` path, then force-update GitHub with explicit leases,
expire rewritten refs, garbage-collect locally, and verify no reachable PDF
archive object remains. Owner explicitly authorized the destructive rewrite;
existing clones must rebase/reset only with care or preferably reclone.

## Blocked / awaiting user

## Recently completed

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
