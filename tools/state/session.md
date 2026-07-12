driver: codex
updated: 2026-07-12T21:12+0900
task: idle
status: idle

## Now
- Goal: clean handoff with a current, forward-looking task board.
- Last done: T-12 is live/pushed at `5199bbd`; stale Round-2/T-9/completion notes were removed, T-15 through T-18 were seeded, and all finished `tools/out/` scratch was audited and deleted.
- Next: start T-15 unless the owner chooses another active task.

## Working set
- Task board: `tools/todo.md` (T-15 through T-18).
- Current facts/choices: `tools/state/facts.md`, `tools/state/decisions.md`.
- Scratch policy: `tools/out/` is empty; new task outputs are created only while needed and deleted after verification/application.
- Verify this cleanup with `python3 tools/check-md-size.py`, `git diff --check`, empty-directory check, and full staged diff review.

## Open questions
- Priority among T-15, T-16, and T-17; default is board order.

## Awaiting user
- T-18 requires owner access to GA Admin; no credentials should be shared.
