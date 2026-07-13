# Skill: native Codex delegation

Use this skill for a directly started Codex DRIVER and its bounded native
subagents.

## Select an evidence-backed route

Before delegating a website task materially analogous to one of the measured
WBD capability classes, query the versioned policy instead of choosing a model
or effort from memory:

```bash
python3 tools/agent-benchmark/select_route.py --task WBD-003 --objective runtime
```

Objectives are `runtime`, `effective_tokens`, and `reliability`. The selector
defaults to `runtime`; choose `effective_tokens` only when token use is the
priority and `reliability` when outcome risk dominates. It returns the route,
confidence/evidence, required validation, and fallback chain from
`tools/agent-benchmark/routing-policy.json`. Use `--validate` after policy or
summary changes; validation rejects a stale source hash, mismatched evidence,
and non-optimal objective selections. Do not extrapolate the mapping to a
materially different task; collect comparable evidence or use driver judgment
and record the new route.
WBD-005-class work is never accepted from the initial dispatch alone: run the
full listed grader and follow its validation-dependent escalation chain.

## Delegate only when it saves context

Stay solo when a task is small, depends on the root's recent reasoning, changes
security/configuration, is inherently serial, or would take less effort than a
prompt plus review. Delegate when the subtask can be described with repository
paths and an exact deliverable, runs independently, and would otherwise load
substantial source or noisy output into root context.

Default to one subagent. Use at most two concurrently, only for independent
subtasks with separate output files and non-overlapping write scopes. Use the
smallest useful context fork. Prompts cite `AGENTS.md`, relevant `skills/`,
ledger task IDs, source paths, and the exact delta rather than copying payloads.

For a local textual change with explicit acceptance in a large file, give the
worker a task-specific search literal and cap inspection at 40 surrounding
lines. Diagnosis, reference-driven visual work, and broad refactors are exempt.

## Authority boundary

Subagents may read, analyze, test, and write their assigned `tools/out/`
deliverable or explicitly assigned non-overlapping implementation files. They
never edit `tools/state/session.md`, project/owner configuration, credentials,
`.git` internals, or unrelated files. They never publish, deploy, push, make
external account writes, or decide ambiguous conflicts. The root DRIVER owns
user communication, ledger, integration, commits, publishing, and judgment.

## Output contract

For analysis, prefer output-file-first. Append long or interruption-prone work
incrementally. End the deliverable with a final `## Structured result` block
containing these populated fields in order:

- `status`
- `summary`
- `changed_files`
- `commands`
- `verification`
- `evidence` (confirmed facts separate from hypotheses)
- `remaining`

The last delegated action appends exactly one newline-safe line to
`tools/codex-log.md`:
`date | calling agent | task | output file | conversationId | outcome`.

Short instrumented edits may use runner-captured mode when the runner durably
retains raw JSONL, stderr, patch, independent grade, metrics, and final response.
Use schema-free worker output when the independent grader is authoritative.
Never use this mode for lookup batches, long/incremental work, or tasks whose
recovery depends on an output file.

## Root review

The root confirms the deliverable exists, inspects the actual diff/evidence,
spot-checks at least one material claim independently, and runs proportional
integration tests. Never accept a subagent's assertion as verification of its
own work.

Record delegated work with schema v2 when runtime telemetry exists. Include
actual token categories, commands/output, durations, retries, gates, and raw
artifact pointers. Unknown values are null, never zero. Do not claim savings
without matched telemetry.

Delegate only when all answers are yes:

1. Is the subtask independent and bounded?
2. Can on-disk pointers supply nearly all context?
3. Is its write scope absent or disjoint?
4. Is root review cheaper than doing the work locally?
5. Can the root independently verify the material result?
