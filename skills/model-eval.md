# Skill: recurring four-model evaluation

Contestants are `sol`, `terra`, `fable`, and `opus`. They receive the same
shared board, `tools/todo.md`. The judge ledger is
`tools/judge/{log,todo}.md`; it exists on `main` only and is never mirrored.

## Round lifecycle

1. Seed or clear/reseed `tools/todo.md` on `main` with the round tasks and rules.
2. Create a scaffold commit equal to `main` minus `tools/judge/`, without
   checkout churn: use Git plumbing (`read-tree` into a temporary index,
   remove `tools/judge/`, `write-tree`, then `commit-tree` with `main` as parent).
3. Force-move all four contestant branches to the exact same scaffold SHA.
4. The user runs all four contestants on the shared board; approvals never carry
   between runs, and runs must obey the board's publish/external-write gates.
5. Judge with four parallel read-only `codex-spark-low` extraction passes, one
   per branch, followed by one `codex-high` verdict over all four reports.
6. Disclose the judge model/identity and any contestant overlap. The coordinator
   independently spot-checks every decisive claim against branch evidence.
7. Before any reset, tag every tip as `eval/rN-<branch>`.
8. Merge the winner on `main` with `git merge <winner> --no-commit`, then protect
   judge state with `git checkout HEAD -- tools/judge/`, review, and commit.
9. Update `tools/judge/log.md`, clear/reseed the shared board, create a fresh
   judge-free scaffold, and force-move all four branches to it.

## Timing

Report all available sources, never a single speed claim:

- first own task commit → last own task commit (excludes pre-work wait, but may
  include idle/review time and misses work before the first commit);
- scaffold commit → last commit (reproducible, but sequential starts bias later
  contestants and the span includes waiting/idle time);
- summed self-reported metrics (may be estimated, overlapping, or incomplete);
- session `updated:` stamps (endpoints only, not durations).

State the contestant start order or that it is unknown. Treat timing as secondary
unless start conditions and measurement methods are genuinely comparable.

## Scoring

Use the Round 1 axes: correctness 40, completeness 30, scope discipline 20,
and evidence/bookkeeping 10. When proposals are allowed, also score proposal
quality: value, specificity, scope discipline, actionable first step, and fit
with repository constraints. Explain whether this is a separate tie-breaker or
how it changes the 100-point total before scoring.
Note: tag/commit/branch surgery must be dispatched with full-access sandbox — codex workspace-write keeps `.git` metadata read-only (verified 2026-07-12).
