# Capability coverage and expansion threshold

## Current suite

| Capability | Tasks | Evidence |
|---|---|---|
| Bilingual EN/JP parity | WBD-001, 002, 005 | mirrored hidden assertions and CRLF scope |
| Legacy static HTML preservation | WBD-001, 002, 005 | byte/line-ending checks and semantic P2P |
| Accessible/security-sensitive links | WBD-002 | name, media type, target/rel, browser names |
| Stateful privacy JavaScript | WBD-003 | consent, focus, cookies, no-request browser tests |
| Responsive/reference visual CSS | WBD-004 | static gates, viewport P2P, exact screenshot |
| Multi-file CSS/JS/cache coordination | WBD-005 | live motion preference, ordinary timing, uniform assets |
| Scope discipline | all | Git diff allowlist, protected paths, CRLF |
| Cost/route/handoff behavior | all | actual tokens, commands, output, time, identity fingerprints |

## Material gaps

1. `.htaccess`/security-header changes and fail-closed server configuration.
2. Responsive-image/performance work with byte and visual thresholds.
3. Frozen factual-source reconciliation (CV/ResearchMap/ORCID-style data) with
   deterministic offline fixtures and provenance checks.
4. Cross-page fragment/link repair beyond a single named anchor.
5. Table-heavy accessibility changes across achievements/news/member families.
6. Recovery from a dirty worktree or an interrupted partial edit.

Deployment and live-account automation are intentionally outside the suite:
they require user/Claude authority and should not become agent benchmark side
effects.

## Candidate capsules

- WBD-006: repair a broken CSP/Permissions-Policy directive in a detached
  `.htaccess`, graded by security-check plus a local header server.
- WBD-007: restore a responsive gallery `srcset`/dimensions regression, graded
  by exact image selection, layout, and asset-byte invariants.
- WBD-008: reconcile a frozen local researcher-record fixture into EN/JP/CV
  outputs with provenance and no invented fields.
- WBD-009: repair mirrored fragment targets and keyboard focus across page
  families without changing visible labels.
- WBD-010: repair a table-semantics regression while preserving legacy layout
  and exact row/cell counts.

## Expansion gate

Do not add a capsule merely to increase benchmark size. Add the smallest next
gap only when at least five expected future tasks exercise it, its fixture can
be fully offline and side-effect-free, pristine/broken states pass the zero-token
audit, and expected routing savings repay setup/evaluation within 20 tasks.
Keep at least one newly added capsule held out until the next candidate freeze.
