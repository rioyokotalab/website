driver: claude
updated: 2026-07-18T20:45+0900
task: T-195 Security hardening loop
status: in-progress

## Now
- T-196 merged (`781e317`): repo-content baseline (SECURITY.md, dependabot.yml,
  ci.yml least-privilege + --ignore-scripts, workflow-security check/test).
- T-197 settings APPLIED and verified (rollback:
  tools/out/t197-settings-rollback.md): workflow token read, no token
  PR-approve, SHA-pinning required, Actions restricted to GitHub-owned,
  Dependabot security updates + private vuln reporting on, fork-PR approval
  all-external, wiki/projects disabled. 0 webhooks, 0 deploy keys.
- T-197 doc PR (docs/repository-controls.md + threat-model B9 + settings note)
  pending — landing now.
- T-198 = DECISION for owner: 66 org-inherited write collaborators +
  zero-approval ruleset = anyone can merge to deploy-feeding main. Not
  agent-actionable (org/people/reverses owner choice). Surfaced to owner.

## Working set
- Branch t197-settings-docs: docs/repository-controls.md,
  docs/security-threat-model.md, TODO.md, session.md.

## Open questions
- B9 collaborator/approval decision (T-198) — asked.

## Awaiting user
- T-198 decision; optional T-194 notification checkbox.
