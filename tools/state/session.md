driver: codex
updated: 2026-07-12T20:26+0900
task: idle
status: idle

## Now
- Goal: cold restart ready.
- Last done: verified owner-applied T-11 configuration, exact 20-file project overlay, Claude bypass at project/user scope, six bypass agents, five Codex never/full-access MCP servers, five trusted owner project records, owner Codex never/full-access defaults, mode-600 owner files, generator drift, JSON/TOML syntax, and size/diff checks; committed project/ledger changes locally.
- Next: end this pre-T-11 session and start a fresh Claude/Codex session; the new session reads this ledger and confirms a clean worktree before ordinary work.

## Working set
- Applied project config: `.claude/settings.json`, `.claude/agents/*.md`, `.mcp.json`, AGENTS.md, CLAUDE.md, aligned skills/registry/generator/tier policy/README.
- Applied owner config (selected keys verified only): `~/.claude/settings.json`, `~/.claude.json`, `~/.codex/config.toml`.
- Evidence: tools/out/driver-report-20260712-2024.md; archived proposal tools/out/r2-deliverables/sol/t11-permissions.md.
- Verify on cold start: `git status --short`; `python3 tools/gen-codex-mcp.py --check`; `codex --version`.

## Open questions
- None for T-11.

## Awaiting user
- T-12: real GA4 `G-...` measurement ID and privacy/consent decision; never publish `G-XXXXXXXXXX`.
