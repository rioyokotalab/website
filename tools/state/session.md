driver: codex
updated: 2026-07-17T17:15+0900
task: T-186 Publish recovered ledger commits and add offline CI
status: in-progress

## Now
- The three existing T-185 recovery commits were reviewed, passed the complete
  offline suite, and were pushed unchanged at `fdaa18d` with no deployment.
  A separate read-only GitHub Actions workflow now runs ledger/static policy
  checks plus the locked Playwright browser suite on Ubuntu 24.04. Validate,
  commit, push, and require its hosted check to pass. The complete local static
  suite passes; the restarted machine's pre-existing `node_modules` is missing
  `playwright/lib/common`, so local browser execution is not acceptance evidence
  and the generated dependency tree was not destructively replaced. Hosted run
  `29565322001` failed before browser setup because the generic runner lacked
  the guarded-delete harness required by deploy-policy tests. The correction
  fetches and verifies exact public harness commit `6bcadab` in runner temp and
  passes its binary explicitly. Hosted run `29565463735` then reached the same
  step but failed because the runner also lacks `lftp`, which the local
  `file:///` mirror regression exercises. Install exact Ubuntu 24.04 package
  `4.9.2-2ubuntu1.1` without running any live-site check, then rerun the hosted
  gate.

## Working set
- `TODO.md`
- `tools/state/session.md`
- `.github/workflows/ci.yml` after the existing commits are published

## Open questions
- None.

## Awaiting user
- None.
