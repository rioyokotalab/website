driver: codex
updated: 2026-07-13T01:15+0900
task: T-27 remove public secrets and unnecessary personal exposure
status: in-progress

## Now
- Goal: publish and live-verify the completed T-27 exposure cleanup.
- Last done: rebase clean; live dry-run shows exactly two modified files (`en/news/index.html`, `jp/news/index.html`) and zero deletions.
- Next: run the publish transaction, then verify live EN/JP contain zero sensitive query/meeting URLs, match local bytes, and GitHub main matches.

## Working set
- T-27 publish scope: `en/news/index.html`, `jp/news/index.html`, decisions/facts/ledger.
- Audit evidence: current tracked files zero key/token/query shapes; reachable history contains the expired URL in two commits; value was never replayed or written to output/logs.

## Open questions
- Historical Git objects retain the expired URL. Another history rewrite would invalidate hashes again while GitHub still caches prior unreachable commits; it remains outside current scope.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
