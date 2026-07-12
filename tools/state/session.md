driver: codex
updated: 2026-07-12T21:32+0900
task: idle
status: idle

## Now
- Goal: idle after restoring the README cluster quickstart.
- Last done: T-19 added and validated exact commands for pinned Claude/Codex setup, authentication, clone, direct Codex config/trust, generated Claude MCP registration, pre-commit checks, health checks, and driver/preview launch.
- Next: start T-15 unless the owner chooses another active task; T-20 tracks the discovered account-specific Claude preview hook.

## Working set
- T-19 files: `README.md`, `tools/todo.md`, `tools/state/session.md`.
- Sources: official Codex CLI/config docs, official Claude Code setup/auth/settings docs, NVM v0.40.4 docs, and current local CLI help/settings.
- Verification passed: 12 shell blocks parse with `bash -n`; Codex TOML command parses and writes mode 600; MCP generator drift, markdown budgets, diff check, unique task IDs, secret-pattern diff scan, and empty `tools/out/` pass.

## Open questions
- The committed Claude preview hook is account-specific; tracked as T-20 because changing `.claude/settings.json` needs explicit project-config scope.

## Awaiting user
- T-18 requires owner access to GA Admin; no credentials should be shared.
