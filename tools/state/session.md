driver: claude
updated: 2026-07-18T17:00+0900
task: T-192 Prepare a sanitized public allowlist mirror
status: awaiting-user

## Now
- T-192 tracked work complete: `tools/build-public-mirror.sh` (single-commit
  allowlist mirror, .htaccess excluded, provenance README, forbidden-path
  checks, value-free audit gate), `tools/test-public-mirror.sh` (7 checks)
  wired into `tools/test-security.sh`, and a mirror section in
  `docs/public-repository-safety.md`. Trial build audit clean (7 public
  large blobs only); full offline suite green; trial cleaned via guarded
  cleanup.
- Next: land the PR and self-merge after CI (standing authorization), then
  owner executes `tools/out/t192-public-mirror-handoff.md` (repo create +
  push are external owner writes). Close T-192 after owner confirmation.

## Working set
- Branch t192-public-mirror: tools/build-public-mirror.sh,
  tools/test-public-mirror.sh, tools/test-security.sh,
  docs/public-repository-safety.md, TODO.md, session.md, report, metrics,
  log.

## Open questions
- None (mirror omits .htaccess by default; owner may opt in via handoff).

## Awaiting user
- Execute the publication steps in tools/out/t192-public-mirror-handoff.md
  and confirm, or adjust the mirror scope first.
