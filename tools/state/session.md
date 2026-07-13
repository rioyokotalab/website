driver: codex
updated: 2026-07-13T17:39+0900
task: T-142 Remove Claude project and runtime configuration
status: in-progress

## Now
- T-141 complete: current-tree inventory found 47 tracked keyword-hit files
  (820,326 bytes) plus `.mcp.json`; exact T-142--T-144 groups recorded. The
  delegated classifier stalled after discovery and was interrupted; root
  reproduced and completed the classification.
- Immediate cleanup removed 17 completed top-level benchmark reports/plans
  (133,343 bytes). Todo/facts/decisions were compacted from roughly 16 KB to
  roughly 3 KB. Pointer-backed raw artifact trees remain until T-143.
- Next: delete active project/runtime integration and obsolete MCP/dispatch
  machinery, then rewrite the Codex-facing config/driver instructions so the
  intermediate tree remains operable.

## Working set
- `tools/out/t141-claude-removal-inventory.md`
- `tools/out/t141-benchmark-cleanup-inventory.md`
- `.claude/`, `CLAUDE.md`, `.mcp.json`
- `AGENTS.md`, `.gitignore`, root/shared configuration playbooks
- MCP/worker-registry generation and dispatch files named in the inventory
- Verify: current-tree path/reference scan, Git diff/status, Markdown budgets,
  Codex delegation/config documentation consistency.

## Open questions
- None blocking. Owner-scope settings and `.git` internals remain excluded;
  Git history remains intact.

## Awaiting user
- None.
