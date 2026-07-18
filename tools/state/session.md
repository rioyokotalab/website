driver: claude
updated: 2026-07-18T22:05+0900
task: idle
status: idle

## Now
- T-200 (security proposals) resolved. HSTS max-age raised 1 day → 1 year in
  .htaccess (host-scoped), merged `d8a23ce`; live effect pending owner deploy
  (tools/out/t200-hsts-deploy-handoff.md — needs SFTP password). Org
  default_repository_permission change DECLINED by owner (org-wide 100+ repos;
  T-198 review gate suffices). Recorded in decisions.md + threat model.
- Board clear. Next free ID: T-201.
- Skills applied: config-proposals, publish-and-verify, html-editing (CRLF/LF
  check on .htaccess), context-ledger.

## Working set
- None (closure committed on the T-200 branch).

## Open questions
- None.

## Awaiting user
- Deploy the HSTS .htaccess (owner-run) per the T-200 handoff.
- Optional: T-194 "notify only for failed workflows" checkbox.
