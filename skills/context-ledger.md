# Skill: context ledger — cross-session working memory

Goal: NO task may depend on chat context to survive. A fresh session —
Claude (CLAUDE.md) or codex (AGENTS.md) — reconstructs all in-flight work
from these files alone. Restarts and claude<->codex handoffs are the
normal case, not the exception.

## File map and routing

| File | Holds | Budget (bytes) |
| --- | --- | --- |
| tools/todo.md | task board: Active / Blocked-awaiting-user / Recently completed; stable ids T-<n> | 8000 |
| tools/state/session.md | THE handoff file: current task, last/next step, working set, open questions, pending asks; overwrite in place — it means "now" | 4000 |
| tools/state/facts.md | current facts: site quirks, cluster numbers, exporter/service behavior, environment | 10000 |
| tools/state/decisions.md | durable decisions + one-line rationale, dated, newest first | 10000 |
| tools/codex-log.md | dispatch/driver session log (existing format) | — |
| tools/out/ | transient deliverables/scratch (gitignored) | — |

Routing rule: procedures -> skills/*; tasks -> todo.md; "now" ->
session.md; facts -> facts.md; choices+why -> decisions.md. Never grow
one file with another's content. Over budget -> prune oldest or least
relevant lines (git keeps history; never create archive copies). Budgets
enforced by tools/check-md-size.py in the pre-commit hook (hook is
untracked — reinstall after a fresh clone).

## Session start (both drivers)
1. Read tools/todo.md + tools/state/session.md (always; they are tiny).
2. If session.md holds an in-flight task: continue from its `Next:` after
   verifying `Files:` against git status. One driver at a time: if the
   OTHER driver updated session.md within ~1 hour, ask the user before
   taking over.
3. Read facts.md / decisions.md sections only as the task needs them.

## Checkpoint triggers (update session.md in place)
- Task start: task id, goal, plan sketch, working set.
- After each completed step, significant discovery, or failure.
- Before anything long or risky (publish, deploy, mass edit, big
  dispatch).
- At every turn end where state changed; at session end. Task finished ->
  set `task: idle`, move one completion line to todo.md.
- On user decisions: durable choice -> decisions.md; pending request ->
  session.md "Awaiting user". Standing direct-DRIVER publish/push authority is
  durable in decisions.md and the role playbook. Exceptional task-specific
  permission outside standing scope (config apply, credentials, destructive or
  material scope expansion) is conversation-scoped: record the ASK, never a
  carried approval.

## session.md schema (keep these headings exactly)
    driver: claude | codex
    updated: <ISO local time>
    task: T-<n> <title> | idle
    status: in-progress | blocked | awaiting-user | idle
    ## Now            (goal / last done / next)
    ## Working set    (files, tools/out paths, verify commands)
    ## Open questions
    ## Awaiting user

## todo.md schema
`### T-<n> — <title>` under Active or Blocked / awaiting user; body:
outcome definition + pointers (ledger paths, tools/out deliverable).
Header line records the next free id. Completions: one line each under
Recently completed, newest first, commit hash when known; prune past
budget.

## Commit rule
Ledger files (tools/todo.md, tools/state/**) commit silently alongside
whatever else is being committed, exactly like the bookkeeping trio;
NEVER a dedicated commit, never prompt the user. Uncommitted ledger still
survives restarts (disk persistence); commits are for history, not
persistence.

## Dispatch interface (drivers -> codex workers)
- Prompts point at canonical on-disk state: skill paths, tools/state/*,
  the todo.md task id, the task's prior tools/out/ file — plus the exact
  task delta. Never restate file contents in prompts.
- Workers read the cited paths before starting, append progress to their
  own tools/out/<task> deliverable, and NEVER edit session.md — the
  driver checkpoints. (A codex DRIVER is not a worker: it owns
  session.md.)

## Driver symmetry and handoff
- Claude driver: CLAUDE.md. codex driver: AGENTS.md "Driving this repo".
  Handoff = checkpoint session.md + stop; the next driver (either brand)
  resumes at Session start step 2. Nothing else needs to transfer.
- Codex drivers may use native subagents under `skills/codex-delegation.md`;
  the root DRIVER alone owns `session.md`, checkpoints before delegation, and
  verifies every result. Subagent handoffs live under `tools/out/`, not chat.
- Driver bookkeeping in tools/task-metrics.jsonl uses agent claude|codex
  and tier driver-claude|driver-codex; workers keep tier = worker name.

## Driver session report (reviewer telemetry)
Every driver session (claude or codex) ends by writing
tools/out/driver-report-<YYYYMMDD-HHMM>.md (transient; the reviewer
deletes it after grading) containing:
- model + reasoning effort actually used; session start/end times.
- Per task attempted: id, outcome (done | blocked | awaiting-user |
  failed), files touched, verification commands run and their results.
- Escalations: every sandbox/approval escalation requested (and whether
  the user approved), every network fetch (URLs), every rule the session
  could not follow and why.
- Self-noted gaps: anything a reviewer should double-check.
Metrics: one line PER task attempted, tier driver-codex, plus an optional
"model" key (allowed only on driver-* lines). codex-log line format for
drivers: `date | <brand>-driver (<model>) | tasks | report path | n/a |
outcome` (brand = claude or codex; claude drivers use agent "claude",
tier "driver-claude"). The Claude review pass grades the report against git diff (not
against session.md claims), records the verdict as a metrics line
(task_type "other", note "driver-review: ..."), then deletes the report
scratch.
