# Skill: Claude Code settings scope and placement

Claude Code merges three ordinary settings tiers; narrower scope wins for
scalar keys while permission arrays merge:

- `~/.claude/settings.json` — USER: applies to every project on this machine.
- `.claude/settings.json` — PROJECT: shared repository behavior.
- `.claude/settings.local.json` — LOCAL: personal and machine-specific.

The repository blanket-ignores `.claude/*` except agents, so a shared project
settings file must be force-tracked with `git add -f .claude/settings.json`.
Local settings stay untracked.

## What goes where

- PROJECT (tracked, shared): agent binding; workflow reminder and preview
  hooks; project environment/behavior flags; `permissions.defaultMode:
  "bypassPermissions"` under the owner's zero-prompt directive; project MCP
  server list. Do not add `permissions.ask`, blocking PreToolUse hooks, or
  config-apply deny rules.
- LOCAL (personal): model preference and machine-only overrides when needed.
- USER (cross-project): `skipDangerousModePermissionPrompt: true` and a
  matching `permissions.defaultMode: "bypassPermissions"` are required to
  suppress the one-time bypass warning because Claude ignores the skip key in
  shared project settings. User lifecycle integrations and per-project trust
  live here or in `~/.claude.json`; changes affect other projects and remain
  owner-run unless explicitly authorized.

Project permission mode does not authorize publishing. The agent follows the
workflow instruction to publish only after the user asks, while Claude Code
does not add a second interactive tool prompt.

## Gotchas

- A project `model` key overrides the user's model choice on restart; keep
  model preference in local/user scope.
- Permission arrays merge across scopes. A stale user/project `ask` or
  `deny` can still interfere, so the zero-prompt configuration removes them.
- `skipDangerousModePermissionPrompt` is intentionally ignored in project
  settings and must be owner-scoped.
- Preview hooks contain an absolute repository path and are machine-coupled.
