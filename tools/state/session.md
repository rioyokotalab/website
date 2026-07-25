driver: codex
updated: 2026-07-25T16:23+0900
task: T-206 move Zhiyi Huang to Alumni
status: awaiting-user

## Now
- Zhiyi Huang is removed from the current-student table and prepended to
  Alumni on both mirrored member pages.
- The expected current-student count is updated from 25 to 24. Historical
  research and publication records remain unchanged.
- The complete offline suite and two focused browser tests pass; both edited
  HTML files retain CRLF with no bare LF.
- `./deploy.sh --dry-run` stopped before staging comparison because no
  authenticated `web` SSH master exists. No live change was attempted and a
  retry is safe after the owner runs `ssh -fN web`.

## Working set
- `en/member/index.html`
- `jp/member/index.html`
- `TODO.md`
- `tools/state/session.md`
- `tools/out/driver-report-20260725-1623.md`

## Open questions
- None.

## Awaiting user
- Authenticate the configured `web` SSH master when convenient.

## Next action
- Publish the repository change through protected `main`. Then, after
  `ssh -fN web`, rerun and inspect `./deploy.sh --dry-run`, deploy the exact
  member-page delta, and verify both live member pages.
