# Current facts (ledger; routing: skills/context-ledger.md)

Update in place when reality changes; date entries. No procedures here
(-> skills/), no tasks (-> tools/todo.md).

## Site / pages
- 2026-07-12 GA4 `G-DVRGG7FDLX` is live via privacy-first basic consent:
  `js/analytics-consent.js` blocks all Google tag requests until acceptance,
  persists/reopens bilingual choices locally, and keeps advertising consent
  denied; commit `5199bbd`.
- 2026-07-12 owner confirmed GA4 event-data retention is 2 months and Google
  Signals/advertising features remain disabled.
- 2026-07-12 parity audit found en=19 vs jp=114 files and 0 broken local
  links across 16 core index pages; HTML page paths mirror, while JP-only
  files are shared image assets.
- 2026-07-12 Computers page: 81 GPUs. 2-GPU RTX 6000 Ada node CPU = AMD
  EPYC 9654 (user-supplied); 8-GPU RTX 6000 Ada node CPU remains unknown
  ("-" in table) and Slurm node rtx6000-ada remains DOWN+NOT_RESPONDING
  with 8 configured GPUs/500000 MB (read-only sinfo+scontrol query).
  Refresh CPU facts only via site-checker probes; never guess.
- Every external target="_blank" link carries rel="noopener noreferrer".
- Page HTML retains legacy floats, table layouts, CRLF, and uppercase unclosed
  `<LI>`, but the unused Dreamweaver templates/control comments were removed
  and deployed in T-23 (`9636ff7`); style.css targets existing selectors — keep
  class/id names stable.
- Frozen public tree: en/ and jp/ mirror every path 1:1; js/chglang.js
  swaps the prefix, so missing counterparts 404.

## Exporters / external services
- researchmap: 7 research projects (rows 2,3,5,6,7,13,19) have no grant
  numbers — user chose to leave unfilled (2026-07-12). Login UI blocks
  non-browser clients (403); public read API works. OpenReview likewise
  blocks non-browser clients.

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
- Use HTTPS for the arXiv API; HTTP redirects may yield an empty body.
