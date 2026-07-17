driver: codex
updated: 2026-07-17T17:04+0900
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
  and the generated dependency tree was not destructively replaced.

## Working set
- `TODO.md`
- `tools/state/session.md`
- `.github/workflows/ci.yml` after the existing commits are published

## Open questions
- None.

## Awaiting user
- None.
