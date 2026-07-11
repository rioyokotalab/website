# Skill: Config changes and tools/out lifecycle

Hand-edit-only files (NEVER edited in place by agents or codex):
`.claude/agents/*.md`, `.mcp.json`, `AGENTS.md`, `CLAUDE.md`.
- Write full proposed copies under `tools/out/` and give the user an EXACT
  copy-paste apply command (cp/mv or a reviewed apply.sh). Preserve agent
  frontmatter verbatim unless the change IS the frontmatter (then flag it).
- `.claude/config-edit-approved` and PreToolUse hooks are accidental-edit
  blocks, never authorization.

CLAUDE.md budget: `tools/check-claude-size.py` (git pre-commit) enforces
35000 bytes; check proposals with `--file <path>`. Compress or move detail
into skills/ rather than appending.

MCP config: `tools/codex-workers.json` is the worker registry;
`tools/gen-codex-mcp.py` regenerates the `.mcp.json` proposal plus exact
user-scope `claude mcp add-json` commands; `tools/gen-codex-mcp.py --check`
detects drift. `.mcp.json` is repo-only and deploy-excluded. Register all
five labels at BOTH user scope (~/.claude.json) and project .mcp.json.

tools/out lifecycle: after results are verified and committed/regenerable,
delete only that task's transient scratch in the same turn; never blind-wipe
`tools/out/`; keep pending deliverables until upload/apply confirmation.
The bookkeeping trio (`tools/task-metrics.jsonl`, `tools/task-tier-policy.md`,
`tools/codex-log.md`) commits silently alongside other changes — never
prompt the user to commit it separately.

Skills upkeep: when a convention changes, update the matching skills/*.md in
the same change set; skills are git-tracked, deploy-excluded, and NOT
hand-edit-only.

Settings placement (user/project/local scopes, tracking caveat): see
`skills/settings-scope.md`.
