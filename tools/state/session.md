driver: codex
updated: 2026-07-13T11:38+0900
task: T-137 Compare Claude agentic-harness strategies
status: awaiting-user

## Now
- Goal: prepare a reproducible Claude comparison of current-harness,
  autonomous safe-mode, and dynamically generated task-specific configuration.
- Last done: implemented the three profiles, isolated runner, dynamic config
  generator, provider-aware telemetry/schema, temporary benchmark driver, and
  exact runbook. Zero-model preflight passes all five capsules and materializes
  current/autonomous/dynamic configs at 62,497/0/1,689 synthetic bytes.
- Next: user exits Codex and starts `claude`; `claude-benchmark-driver` resumes
  here, reruns preflight/plan, and executes the counterbalanced 15-run screen.

## Working set
- `CLAUDE.md`; `.claude/settings.json`; `.claude/agents/`
- `.claude/benchmark-profiles/`
- `skills/claude-benchmark.md`; `tools/agent-benchmark/claude_benchmark.py`
- `tools/agent-benchmark/tasks.json`; `tools/agent-benchmark/task_ops.py`
- `tools/task-metrics.py`; `tools/task-metrics.schema.json`

## Open questions
- None. The initial plan has 15 runs and a hard aggregate ceiling of $54;
  current-harness total-token claims remain conservative/inconclusive because
  nested Codex MCP usage is not guaranteed in Claude's telemetry.

## Awaiting user
- Exit Codex and start Claude. The user explicitly authorized this driver
  handoff and the project configuration experiment; no repeated takeover prompt
  is needed.
