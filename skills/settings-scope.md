# Skill: Claude Code settings scope and placement

Three settings tiers, all read and MERGED at startup (narrower scope
overrides wider on key conflicts):

- `~/.claude/settings.json` — USER: applies to every project on this machine.
- `.claude/settings.json` — PROJECT: shared repo behavior.
- `.claude/settings.local.json` — LOCAL: machine/personal, `.gitignore`d.

Repo caveat: `.gitignore` blanket-ignores `.claude/*` (only
`!.claude/agents/` is un-ignored), so BOTH settings files are untracked by
default — only `.claude/agents/*.md` ship on clone. To make PROJECT settings
survive a fresh clone, force-track them: `git add -f .claude/settings.json`.
LOCAL settings must stay untracked.

## What goes where

- PROJECT (tracked, shared): agent binding (`agent: site-coordinator`);
  `permissions.deny` for secrets (.env/.secrets/credentials) and the
  apply-proposals guard; `permissions.ask` for Bash `*publish*`/`*deploy*`;
  ALL workflow hooks (PostToolUse metrics/tier reminder, publish→CLAUDE.md
  doc-sync reminder, PreToolUse config-edit guard, SessionStart/End
  localhost:8000 preview server); project env flags (DISABLE_BACKGROUND_TASKS,
  DISABLE_1M_CONTEXT) and behavior policy (includeGitInstructions,
  autoMemoryEnabled).
- LOCAL (personal): accumulated `permissions.allow` approvals;
  `permissions.defaultMode`; `enabledMcpjsonServers` (per-machine MCP trust);
  personal model preference.
- USER-scope candidates: cross-project prefs like `effortLevel` (and model).

## Gotchas

- Model pin: a `"model"` key in PROJECT `settings.json` overrides your own
  `/model` default on every restart. Keep model preference in LOCAL scope or
  omit it — never in the tracked project file.
- Hooks are shell-command reminders (nudges), not model logic. Workflow-
  enforcing hooks belong in the TRACKED project file so they survive re-clone.
- SessionStart/End preview hooks embed the absolute repo path; harmless while
  the repo lives at one path, but they are machine-coupled.
