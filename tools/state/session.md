driver: claude
updated: 2026-07-18T20:10+0900
task: T-195 Security attack-surface investigation and hardening loop
status: in-progress

## Now
- Investigation done (evidence-first-research + ledger skills applied).
  Client-side and supply-chain layers are strong: SRI+crossorigin enforced,
  pinned npm lockfile, strict CSP without unsafe-inline, allowlist deploy,
  secret scanning + push protection on, Dependabot alerts ON, fork-PR CI runs
  under read-only job token with no secrets.
- Real gaps are GitHub-side on the now-public repo:
  1. default_workflow_permissions = WRITE (repo-level token default).
  2. can_approve_pull_request_reviews = TRUE.
  3. sha_pinning_required = FALSE (workflow already SHA-pins → free win).
  4. Dependabot security updates DISABLED (alerts on).
  5. fork-PR approval = first_time_contributors (not all outside).
  6. has_wiki / has_projects TRUE but unused.
  7. ci.yml `npm ci` runs lifecycle scripts; top-level perms not minimal.
  8. No SECURITY.md, no dependabot.yml, no workflow-security regression test.
- Queue: T-196 repo-content baseline (files + new test, via PR); T-197
  settings hardening (API, reversible, reported). Threat model:
  `docs/security-threat-model.md`.

## Working set
- docs/security-threat-model.md (new), then T-196 files.

## Open questions
- HSTS max-age=86400 is deliberately short; raising it is a sticky live
  change — proposed, not auto-executed.

## Awaiting user
- None yet.
