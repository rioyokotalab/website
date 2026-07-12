# Skill: Project config changes and tools/out lifecycle

Project-scope configuration may be edited directly only when the current task
explicitly authorizes that exact scope. This includes `.claude/settings.json`,
`.claude/agents/*.md`, `.mcp.json`, `AGENTS.md`, and `CLAUDE.md`.
Use the normal edit/review/verification workflow; there is no marker-file,
PreToolUse, or human-copy gate. Task authorization to edit config is not
authorization to publish, deploy, push, expose credentials, or change unrelated
owner settings.

Owner-scope files such as `~/.claude/settings.json`, `~/.claude.json`, and
`~/.codex/config.toml` remain proposal-only unless the user explicitly
authorizes the exact external write in the current conversation. Give exact,
atomic owner-run commands, preserve unrelated keys, and flag cross-project
impact.

CLAUDE.md budget: `tools/check-claude-size.py` (git pre-commit) enforces
35000 bytes. Compress or move detail into skills rather than appending.

MCP config: `tools/codex-workers.json` is the worker registry;
`tools/gen-codex-mcp.py` regenerates the `.mcp.json` candidate plus exact
user-scope `claude mcp add-json` commands; `--check` detects drift. Review
the generated candidate, then an explicitly authorized project-config task may
apply it directly. Register all five labels at both user and project scope.

tools/out lifecycle: after results are verified and committed or regenerable,
delete only that task's transient scratch in the same turn; never blind-wipe
`tools/out/`; keep owner-run proposals until application is confirmed. The
bookkeeping trio commits silently alongside other work.

Skills are ordinary git-tracked, deploy-excluded files. When a convention
changes, update its matching skill in the same change set.
