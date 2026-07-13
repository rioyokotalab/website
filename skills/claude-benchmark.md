# Skill: Claude dynamic Fable/max rerun

Use this playbook for T-139, the explicitly authorized corrected rerun of the
Claude `dynamic` benchmark arm. The root Claude session orchestrates; every
measured implementation runs in a fresh temporary Git fixture through
`tools/agent-benchmark/claude_benchmark.py`.

## Frozen question and identity

Run exactly one planned attempt for each WBD-001 through WBD-005 under:

- variant: `dynamic`
- run label: `claude-dynamic-b23416b-fable-max-v1`
- fixture ref: `b23416bd3b08d725d239737f6643b3c343ee1c27`
- root benchmark driver: Claude `fable`, effort `max`
- dynamic generator, generated coordinator, executor, and any generated native
  agents: Claude `fable`, effort `max`
- Claude CLI: `2.1.207` unless a later version is explicitly reviewed
- maximum planned spend: `$18` (`$3` for WBD-001–004 and `$6` for WBD-005)

The ref is the first commit with the corrected WBD-005@2 P2P dependencies. The
historical profile remains pinned to the original T-137 ref; the runner accepts
the corrected ref only for this explicit dynamic override and logs both refs.
Do not relabel, delete, or rewrite prior results.

This is a standalone corrected cohort. The older current-harness and autonomous
rows used a different fixture ref and their manifests record `opus` / `high` at
the measured-subprocess layer. Do not run the strict comparison command or
claim a matched cross-arm ranking from this rerun alone.

Once the first measured command starts, do not edit the task definitions,
grader, runner, prompt, profile, plan, model, effort, ref, or budget. Generated
roles may vary by task, but their model and effort are schema-pinned to
Fable/max and their generation usage counts toward the dynamic arm.

## Safety

- Never run a benchmark task in the root repository or root conversation.
- Never inspect a mutated fixture to assist a later task.
- The runner removes publish/deploy scripts and Git remotes. Never use network,
  credentials, SSH, LFTP, publish, deploy, or push inside a fixture.
- Run commands serially in WBD order. Do not tune between tasks.
- Exactly one attempt is planned per task. A normal capability or generator
  failure is evidence: record it, do not rerun it, and continue. Stop the cohort
  only for identity drift, unsafe scope, missing/corrupt telemetry, budget
  breach, or evaluator failure.

## Zero-token gate

From `/home/rioyokota/website`, before any measured call:

```bash
git status --short
python3 tools/agent-benchmark/claude_benchmark.py preflight \
  --variant dynamic \
  --run-label claude-dynamic-b23416b-fable-max-v1 \
  --ref b23416bd3b08d725d239737f6643b3c343ee1c27 \
  --model fable \
  --effort max \
  --allow-dynamic-ref
python3 tools/agent-benchmark/claude_benchmark.py plan \
  --variant dynamic \
  --run-label claude-dynamic-b23416b-fable-max-v1 \
  --ref b23416bd3b08d725d239737f6643b3c343ee1c27 \
  --model fable \
  --effort max \
  --allow-dynamic-ref
```

Preflight must report `status: pass`, five valid capsules, zero existing label
rows, the corrected ref override, CLI-advertised Fable/max, and a materialized
dynamic coordinator pinned to Fable/max. Confirm the generated plan exactly
matches `tools/out/t139-claude-dynamic-plan.json`.

Read `tools/out/t139-claude-dynamic-rerun.md`, append the start checkpoint, and
keep its `## Structured result` block last. No Claude model call is authorized
until every zero-token gate passes.

## Measured run

Execute the five commands in `tools/out/t139-claude-dynamic-plan.json` exactly
once and in order. After every command:

1. Check the compact result and retained `result.json` for the planned task,
   label, ref, `model: fable`, `effort: max`, dynamic-ref override, config
   coordinator identity, usage/cost/duration, and artifact pointer.
2. Run `python3 tools/agent-benchmark/claude_benchmark.py artifacts`.
3. Append the result and any failure to the T-139 report and checkpoint
   `tools/state/session.md` before starting the next task.
4. Run `git status --short`; do not disturb the inherited T-138 bookkeeping.

Failed dynamic generation is now retained as billable generation telemetry.
Count its usage, cost, and duration in operational totals even though the task
does not pass capability.

After all five planned attempts:

```bash
python3 tools/agent-benchmark/claude_benchmark.py summarize \
  --run-label claude-dynamic-b23416b-fable-max-v1
python3 tools/task-metrics.py import-benchmark \
  --provider claude \
  --run-label claude-dynamic-b23416b-fable-max-v1 \
  --dry-run
python3 tools/task-metrics.py import-benchmark \
  --provider claude \
  --run-label claude-dynamic-b23416b-fable-max-v1
python3 tools/task-metrics.py validate
```

Report pass count, per-task scores/gates, effective tokens, cost, wall time,
tool output, delegation, generated strategies, actual `model_usage`, and failed
generation spend. Keep driver-session usage separate from measured-run usage.

## Closeout

Update the round record with a clearly labeled T-139 addendum; do not overwrite
the original T-137 table. State that old-arm comparisons remain unmatched.
Restore `.claude/settings.json` to `"agent": "site-coordinator"` and
`"effortLevel": "low"` after the experiment.

Run runner self-test, artifact audit, metrics/schema validation, Python syntax,
Markdown-size, and repository regression checks. No public website change is
expected, so never publish or deploy. Finish the standard driver report,
T-139 ledger closeout, one driver metrics row, and one codex/Claude log line;
then use the normal non-force commit/rebase/push gates.
