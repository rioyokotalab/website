# Lab website — active task list

Cross-session source of truth. Keep minimal; completed-task history lives in git.

## Active / pending

## Operational reminders
- Every codex call passes `model=<worker.model>` + `config={"model_reasoning_effort":...}`; write-capable calls pass `sandbox:"workspace-write"`. codex has no network and cannot `rm`.
- `git pull --rebase` before every push; publish only after explicit user OK.
- After every task: append one line to tools/task-metrics.jsonl and refresh tools/task-tier-policy.md.
- Delete transient tools/out/ scratch as soon as its task is verified/committed.
