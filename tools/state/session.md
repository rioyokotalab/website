driver: codex
updated: 2026-07-18T11:42+0900
task: T-188 Make website independent of harness
status: in-progress

## Now
- Website static/security, deployment-policy, and all 38 browser tests pass.
  The incomplete generated Node tree and missing Chromium shell were replaced
  through guarded cleanup plus locked installs; `.last-run.json` records
  `passed`. Harness phase one passes after its website-specific removals. Next
  commit each implementation and validate each commit from an isolated clone.

## Working set
- `TODO.md`
- `tools/state/session.md`
- `.github/workflows/ci.yml`
- `tools/guarded-tree-cleanup.sh`
- `tools/guarded-delete`
- `tools/test-guarded-delete.sh`
- `tools/test-security.sh`
- `.github/workflows/ci.yml`
- website policy, audit, dependency, and validation files named in T-188
- `docs/repository-controls.md`
- `docs/public-repository-safety.md`
- `docs/github-rulesets/main.json`
- `docs/audits/public-history-20260716.json`
- `tools/public-repo-audit.py`
- `tools/test-public-repo-audit.sh`
- `tools/test-github-ruleset.sh`
- `tools/bootstrap-lftp.sh`
- `tools/test-bootstrap-lftp.sh`
- `tools/test-repository-independence.sh`

## Open questions
- None. No dependency requires preservation; historical cross-references are
  provenance only and will remain plainly labeled as such.

## Awaiting user
- None.
