# Current facts (ledger; routing: skills/context-ledger.md)

Update in place when reality changes; date entries. No procedures here
(-> skills/), no tasks (-> tools/todo.md).

## Site / pages
- 2026-07-05 Computers page: 81 GPUs. 2-GPU RTX 6000 Ada node CPU = AMD
  EPYC 9654 (user-supplied); 8-GPU RTX 6000 Ada node CPU unknown ("-" in
  table; node down). Refresh only via site-checker probes; never guess.
- Every external target="_blank" link carries rel="noopener noreferrer".
- Page HTML is Dreamweaver-era (floats, table layouts, CRLF, legacy
  uppercase unclosed <LI>); style.css targets existing selectors — keep
  class/id names stable.
- Frozen public tree: en/ and jp/ mirror every path 1:1; js/chglang.js
  swaps the prefix, so missing counterparts 404.

## Exporters / external services
- researchmap: 7 research projects (rows 2,3,5,6,7,13,19) have no grant
  numbers — user chose to leave unfilled (2026-07-12). Login UI blocks
  non-browser clients (403); public read API works. OpenReview likewise
  blocks non-browser clients.
- 41 publication PDFs archived in tools/papers/ as
  {FirstAuthorLastName}{Year}.pdf (grant-ID extraction source set).

## Tooling / environment
- codex-cli 0.144.1: outbound network in workspace-write sandbox via
  -c sandbox_workspace_write.network_access=true (verified).
- codex sandbox: workspace-write keeps .git/ read-only by design (commits fail with index.lock "Read-only file system"); a FRESH session with sandbox danger-full-access CAN write .git. Sandbox mode is fixed at session start — per-call overrides on codex-reply are silently ignored.
- Git pre-commit hook (.git/hooks/pre-commit) is UNTRACKED: after a fresh
  clone, reinstall it (tools/out proposal apply.sh did this once; content
  calls check-claude-size.py + check-md-size.py).
- Preview: localhost:8000; deploy is SFTP-only to www/ via publish.sh ->
  deploy.sh (deletion-bearing; --dry-run first).
- tools/ and skills/ are deploy-excluded; tools/out/ is gitignored
  scratch; tools/state/ is git-tracked.
