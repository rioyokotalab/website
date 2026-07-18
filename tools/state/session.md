driver: claude
updated: 2026-07-18T23:10+0900
task: idle
status: idle

## Now
- T-200 COMPLETE: HSTS `.htaccess` change deployed to the live site and
  verified — `Strict-Transport-Security: max-age=31536000` served, HTTP→HTTPS
  301 intact, live security suite passes. Deploy touched 3 files (.htaccess +
  drifted style.css, cv/cv.pdf), 0 deletions.
- T-202 COMPLETE (`439ef4d`): fixed the deploy deletion guard, which mis-read
  SFTP in-place updates ("Removing old file" + "Transferring") as unmatched
  deletions and blocked every real deploy. True deletions = removed-not-
  transferred; SFTP-format test coverage added. This was the T-200 blocker.
- The deploy connection was restored by the owner (recreated `~/.ssh`
  web-password/askpass/ControlMaster wiped by the 2026-07-15 incident; see
  memory + website commit `1467909`).
- Board clear. Next free ID: T-203.
- Skills applied: evidence-first-research (git-history recovery),
  publish-and-verify (deploy gates), research-engineering-validation (guard
  fix + tests), context-ledger.

## Working set
- None (T-200/T-202 closure pending commit).

## Open questions
- None.

## Awaiting user
- Optional: T-194 "notify only for failed workflows" checkbox.
