# Skill: project config changes and tools/out lifecycle

Project configuration such as `AGENTS.md` may be edited directly only when the
current task explicitly authorizes that exact scope. Use the normal edit,
review, and verification workflow. Task authorization to edit project config
does not authorize publishing, credentials access, unrelated owner settings,
or material scope expansion.

Owner-scope files such as `~/.codex/config.toml` remain proposal-only unless the
user explicitly authorizes the exact external write in the current
conversation. Give exact atomic owner-run commands, preserve unrelated keys,
and flag cross-project impact.

`tools/out/` lifecycle: after results are verified and committed or
regenerable, delete only the reviewed task-specific scratch in the same turn;
never blind-wipe the directory. Keep owner-run proposals until application is
confirmed. Ledger and bookkeeping files commit silently with task changes.

Skills are ordinary tracked, deploy-excluded files. When a convention changes,
update its matching skill in the same change set.
