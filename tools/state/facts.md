# Current facts (ledger; routing: skills/context-ledger.md)

Update in place when reality changes; date entries. No procedures here
(-> skills/), no tasks (-> tools/todo.md).

## Site / pages
- 2026-07-12 parity audit found en=19 vs jp=114 files and 0 broken local
  links across 16 core index pages; HTML page paths mirror, while JP-only
  files are shared image assets.
- 2026-07-12 Computers page: 81 GPUs. 2-GPU RTX 6000 Ada node CPU = AMD
  EPYC 9654 (user-supplied); 8-GPU RTX 6000 Ada node CPU remains unknown
  ("-" in table) and Slurm node rtx6000-ada remains DOWN+NOT_RESPONDING
  with 8 configured GPUs/500000 MB (read-only sinfo+scontrol query).
  Refresh CPU facts only via site-checker probes; never guess.
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
- 2026-07-12 T-11 applied and verified: project Claude uses
  `bypassPermissions`, all six site agents use bypass mode, and all five Codex
  MCP servers use `approval_policy="never"` plus
  `sandbox_mode="danger-full-access"`; owner Claude/Codex defaults match.
  Start a fresh session to load these defaults. Product-managed sandboxing may
  still override local configuration.
- Git pre-commit hook (.git/hooks/pre-commit) is UNTRACKED: after a fresh
  clone, reinstall it (tools/out proposal apply.sh did this once; content
  calls check-claude-size.py + check-md-size.py).
- Preview: localhost:8000; deploy is SFTP-only to www/ via publish.sh ->
  deploy.sh (deletion-bearing; --dry-run first).
- tools/ and skills/ are deploy-excluded; tools/out/ is gitignored
  scratch; tools/state/ is git-tracked.
- 2026-07-12 pm: codex worker-sandbox outbound DNS/network went DOWN across
  spark and standard pools (doi.org 000, empty bodies); Claude Bash
  (site-checker) fallback worked; interactive driver sessions recover via
  user-approved escalations. Separately: http:// arXiv API URLs 301 with an
  empty body — always use https. Recheck network before relying on codex
  lookups.
