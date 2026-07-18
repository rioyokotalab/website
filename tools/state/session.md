driver: codex
updated: 2026-07-18T11:54+0900
task: T-188 Make website independent of harness
status: in-progress

## Now
- Local and isolated-clone website validation passed, including all 38 browser
  tests. PR #3 CI then failed because the lftp plan test used `/usr/bin` to
  simulate absence, but CI had just installed `/usr/bin/lftp`; its expected
  `action=install` grep therefore failed. The test now uses a minimal fake PATH
  containing only `dirname` and `uname`. Rerun locally, commit, push, and require
  a new green `Offline checks` run before merge.

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
