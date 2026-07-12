driver: codex
updated: 2026-07-12T23:55+0900
task: T-29 add continuous security regression checks
status: in-progress

## Now
- Goal: make security invariants deterministic and pre-publish enforced.
- Last done: T-29 offline harness passes, deploy policy and seven publish scenarios pass, and live mode validates HTTPS redirect/headers/status while correctly flagging only the known public `.dont-remove-me` T-28 blocker. One missing `rel` was repaired in JP news.
- Next: rebase, inspect the deletion-bearing dry-run, publish/push the completed T-29 scope, then verify the changed live news page and remote commit.

## Working set
- Prepared scope: `tools/security-check.py`, `tools/test-security.sh`, publish/test integration, README/playbook, one JP news link hardening, ledger/bookkeeping.
- Verification passed: offline security/deploy suites, seven publish cases, Markdown budgets. Live audit has exactly one expected T-28 finding for `/.dont-remove-me`.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
