driver: fable (coordinator)
updated: 2026-07-12T15:17+0900
task: Round 2 4-way eval setup
status: in-progress

## Now
- Goal: establish the judge-only ledger, reseed the shared Round 2 board, and prepare all contestant branches from one judge-free scaffold.
- Last done: Round 1 verdict captured; judge log/checklist, Round 2 tasks, and canonical model-evaluation protocol drafted.
- Next: git surgery worker commits `main`, creates the judge-free scaffold, records its SHA, and resets all four contestant branches.

## Working set
- Files: `tools/judge/{log,todo}.md`; `tools/todo.md`; `skills/{model-eval,README}.md`; `tools/state/session.md`.
- Scratch: `tools/out/r2-drafts.md`.
- Verify: requested line limits, task IDs/rules, judge-only protection lifecycle, and one shared scaffold SHA for all branches.

## Open questions
- None for file drafting; follow-up worker must record the scaffold SHA in `tools/judge/todo.md`.

## Awaiting user
- Run the four contestants after setup and branch reset complete.
