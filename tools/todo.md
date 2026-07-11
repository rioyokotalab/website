# Lab website — active task list

Cross-session source of truth. Keep minimal; completed-task history lives in git.

## Active / pending
- researchmap sync (#2, design b) IMPLEMENTED in tools/researchmap-export.py (`--sync` = inserts + field-diff updates + registry-bounded deletes; `managed_ids` registry added to tools/researchmap-state.json; offline fixture tests pass). PENDING: (1) Claude-side live `python3 tools/researchmap-export.py --sync --dry-run` + human review of the N inserts / M updates / K deletes summary before any upload; (2) a CLAUDE.md researchmap-section doc-update proposal describing the new `--sync`/update/delete grammar + `managed_ids` registry.

## Operational reminders
- Every codex call passes `model=<worker.model>` + `config={"model_reasoning_effort":...}`; write-capable calls pass `sandbox:"workspace-write"`. codex has no network and cannot `rm`.
- `git pull --rebase` before every push; publish only after explicit user OK.
- After every task: append one line to tools/task-metrics.jsonl and refresh tools/task-tier-policy.md.
- Delete transient tools/out/ scratch as soon as its task is verified/committed.
