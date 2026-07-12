# Skill: native Codex delegation

Use this skill only for a directly started Codex DRIVER. Claude-dispatched MCP
workers continue to follow `skills/codex-dispatch.md` and do not gain DRIVER
authority.

## Delegate only when it saves context

Stay solo when a task is small, depends on the root's recent reasoning, changes
security/configuration, is inherently serial, or would take less effort than a
prompt plus review. Delegate a bounded subtask when it can be described with
repository paths and an exact deliverable, runs independently, and would
otherwise load substantial source or noisy command output into the root
context.

Default to one subagent. Use at most two concurrently, and only for independent
subtasks with separate output files and non-overlapping write scopes. Use the
smallest useful context fork (`none` for fully on-disk tasks; a short recent
fork only when necessary). Prompts cite `AGENTS.md`, relevant `skills/`, ledger
task IDs, source paths, and the exact delta rather than copying file contents.

## Authority boundary

Subagents may read, analyze, test, and write their assigned `tools/out/`
deliverable or explicitly assigned non-overlapping implementation files. They
never edit `tools/state/session.md`, project or owner configuration, credentials,
`.git` internals, or unrelated files. They never publish, deploy, push, make
external account writes, or decide ambiguous conflicts. The root DRIVER owns
all user communication, ledger checkpoints, integration, commits, publishing,
and final judgment.

## Handoff and review

For analysis, prefer output-file-first: the deliverable ends with a populated
`## Structured result` block as defined in `skills/codex-dispatch.md`. For a
code edit, require changed-file and verification summaries. The root confirms
the deliverable exists, inspects the actual diff or evidence, spot-checks at
least one material claim independently, runs proportional integration tests,
and rejects or corrects incomplete work. Never accept a subagent's assertion as
verification of its own work.

Record delegated work with schema v2 (`tools/task-metrics.schema.json`) when the
runtime reports it. Include worker and root-review cost: actual token categories,
prompt/instruction bytes, completed/failed commands and output size, setup/
worker/grader/review durations, retries, score/gates, and failure phase. Raw
trajectories stay under `tools/out/`; the metrics line stores only their pointer.
Do not claim token savings without matched measured telemetry. When telemetry is
unavailable, use `null` and record only observable proxies; never silently treat
unknown tokens or review time as zero.

## Decision checklist

Delegate only if every answer is yes:

1. Is the subtask independent and bounded?
2. Can on-disk pointers supply nearly all context?
3. Is its write scope absent or disjoint?
4. Is root review cheaper than doing the whole subtask in root context?
5. Can the root independently verify the material result?
