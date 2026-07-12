# Skill: codex dispatch contract (canonical copy)

Registry: `tools/codex-workers.json` (worker name -> model/effort/pool).
Routing: `tools/task-tier-policy.md` (task_type -> default worker).
Full policy incl. failover ladder: `.claude/agents/codex-offload-policy.md`.

Per-call contract (MANDATORY — server names are routing labels only):
- Pass `model=<worker.model>` AND
  `config={"model_reasoning_effort":<worker.effort>}` from the registry on
  EVERY call; omitting them silently runs the account default (gpt-5.5).
- Pass `sandbox: "danger-full-access"` and approval policy `never` on every
  call so repository metadata, network, and owner-authorized paths do not cause
  approval pauses or sandbox failures. Use `cwd: "/home/rioyokota/website"`.
- Use exactly the dispatched worker; report hard failures with evidence.
  Never silently reroute or self-escalate — failover and escalation
  decisions belong to the orchestrator.

Output-file-first:
- `tools/out/<task>.md|.py` IS the deliverable; chat replies are pointers.
- Append incrementally; for lookup/edit sessions append each result
  immediately and run `tail -1 <output-file>` before moving on.
- End the file with the mandatory `## Structured result` block
  (status / summary / changed_files / commands / verification / evidence:
  confirmed + hypotheses / remaining), kept as the final content.
- The calling agent confirms the file exists and is non-empty, spot-checks at
  least one claim, and keeps its final message short (~15 lines).

Fan-out:
- Independent bounded subtasks -> multiple codex calls in ONE turn, disjoint
  output files, non-overlapping write scopes. <=2 lookup items or 2-4 other
  items per session. Never spawn Claude subagents in parallel.

Logging (last actions of every delegated task):
- codex appends to `tools/codex-log.md`:
  `date | calling agent | task | output file | conversationId | outcome`.
- New instrumented work appends one schema-v2 line to
  `tools/task-metrics.jsonl`; validate with `python3 tools/task-metrics.py
  validate`. The canonical fields and nullability are in
  `tools/task-metrics.schema.json`. Preserve run/task identity, model/effort,
  capability/P2P/scope gates, actual input/cached/output/reasoning tokens,
  completed/failed command counts, tool-output size, phase durations,
  changed files, retries/escalation, failure provenance, and the raw artifact
  pointer. Unknown values are `null`, never fabricated zero. Legacy v1 lines
  remain accepted for uninstrumented historical work and are never rewritten.
- `tier` = worker name (drivers: driver-claude|driver-codex). Fixed task_type enum: mechanical-edit, content-draft,
  translation, metadata-lookup, verify-parity, git-summary, deploy-publish,
  exporter-logic, diagnosis, figure-production, config-edit, other.

Prompts pass pointers (paths/URLs/skill names), never payloads. Repository
instructions are injected by Codex; do not ask the worker to print them back.
Workers read only the named task-relevant skills and source ranges.

Context ledger (canonical: skills/context-ledger.md):
- Point dispatches at on-disk state — skill paths, tools/state/*, the
tools/todo.md task id, the task's prior tools/out/ file — plus the exact
delta; never restate file contents.
- Workers read the cited ledger paths first and NEVER edit
tools/state/session.md; the driver checkpoints it. A user-started codex
DRIVER session (AGENTS.md "Driving this repo") owns session.md instead.

Probe integrity and log hygiene:
- Copy real command output only — NEVER reconstruct or paraphrase it. Any
  high-stakes evidence (anything that changes a grade, a recorded fact, or
  an edit decision) must be written raw to a tools/out/ file and re-checked
  via a second independent path (different pool, site-checker Bash, or the
  orchestrator's own Read) before anyone acts on it.
- Before appending to tools/codex-log.md or tools/task-metrics.jsonl,
  ensure the file ends with a newline so entries never concatenate.
