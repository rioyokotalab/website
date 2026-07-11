# Lab website — active task list

Cross-session source of truth. Keep minimal; completed-task history lives in git.

## Active / pending
- CLAUDE.md compaction phase 1 (SAFE PASS, in progress): DELETE stale/historical C1-C6 + pure-deletion MOVEs B1-B4 -> tools/out/CLAUDE.md proposal with apply command.
- CLAUDE.md compaction phase 2 (agent-boundary): first ADD domain knowledge to .claude/agents/*.md (ResearchMap/ORCID/CV/figures/Drive/SSH-deploy/Hinadori), then delete from CLAUDE.md (B6-B12).
- CLAUDE.md compaction phase 3 (in-place polish A1-A9), then resolve D-list decisions.
- Resolve CV-sync contradiction (D6): CLAUDE.md says both "only when explicitly asked" and "update cv/cv.tex in the same edit"; pick one. Full detail in tools/out/claude-compaction-suggestions.md.

## Operational reminders
- Every codex call passes `model=<worker.model>` + `config={"model_reasoning_effort":...}`; write-capable calls pass `sandbox:"workspace-write"`. codex has no network and cannot `rm`.
- `git pull --rebase` before every push; publish only after explicit user OK.
- After every task: append one line to tools/task-metrics.jsonl and refresh tools/task-tier-policy.md.
- Delete transient tools/out/ scratch as soon as its task is verified/committed.
