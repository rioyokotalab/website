# Skill: Claude agentic-harness benchmark

Use this playbook only for T-137 or a later explicitly authorized Claude
configuration experiment. The root Claude session orchestrates; every measured
implementation runs in a fresh temporary Git fixture through
`tools/agent-benchmark/claude_benchmark.py`.

## Question and frozen controls

Compare three arms:

1. `current-harness`: the project configuration frozen at `3364e2c`, including
   CLAUDE.md, site agents, routing rules, and Codex MCP offload. The runner
   rebinds hard-coded repository paths to the fixture and disables only
   operational lifecycle hooks and publish/deploy entry points.
2. `autonomous`: Claude Code `--safe-mode`, with CLAUDE.md, `.claude/`,
   `.mcp.json`, and AGENTS.md absent. Built-in tools remain; Claude decides
   whether native Agent delegation helps.
3. `dynamic`: the same clean start, followed by a tool-free safe-mode planning
   call that generates a compact task-specific CLAUDE.md, settings file,
   coordinator, and zero to three non-nesting native agents. A fresh execution
   session loads the validated generated project configuration.

All arms pin repository/config source
`3364e2c3617b1fa0d0d044a8d5a5d1af3faa548d`, Claude `opus`, high effort,
the same arm-neutral task prompt, task/grader hashes, timeout class, mutation,
authorized paths, and P2P/visual gates. Each call is a new non-persistent
session. Dynamic generation counts against that arm's token, time, and dollar
budget.

Do not edit tasks, graders, profiles, prompts, routes, or runner after the first
measured run. If a genuine evaluator defect appears, stop the whole matrix,
record/exclude affected runs, version the invariant, and restart every arm.

## Safety and contamination

- Never run a benchmark task directly in the root repository or root Claude
  conversation. Never inspect a retained temporary workspace to help a later
  arm.
- The runner removes publish/deploy scripts and Git remotes from the fixture;
  agents are also explicitly forbidden to use network, credentials, ssh,
  lftp, publish, deploy, or push.
- WBD-005 remains held out until all three visible configurations are frozen.
  Run its three arms without any configuration, prompt, route, or grader change
  between them.
- Capability is primary: every critical/F2P/P2P/scope gate and score must pass.
  A capability miss is valid screening evidence, but an unsafe setup,
  contamination, telemetry parser error, or identity drift stops the matrix.

## Zero-token start

From `/home/rioyokota/website`:

```bash
git status --short
python3 tools/agent-benchmark/claude_benchmark.py preflight
python3 tools/agent-benchmark/claude_benchmark.py plan > tools/out/t137-claude-plan.json
```

Preflight must report `status: pass`, five valid capsules, Claude CLI 2.1.207
or a deliberately reviewed later version, the complete frozen current-harness
snapshot, model `opus`, effort `high`, and initial maximum `$54`. A CLI version
change is an experiment dimension: record it; do not silently repin behavior.

Create `tools/out/t137-claude-benchmark.md` before the first model call. Record
preflight, the exact plan, start time, CLI/model/effort/ref, and maximum spend.
Append each run immediately with run ID, arm/task, pass/score/gates, tokens,
cost, duration, delegation counts, config fingerprint, telemetry completeness,
and artifact pointer. Keep its structured-result block last.

## Initial 15-run screen

Read `tools/out/t137-claude-plan.json` and execute its commands in order, one at
a time. It counterbalances arm order across tasks. The first 12 commands are
WBD-001–004; the final three are WBD-005. After every command:

```bash
python3 tools/agent-benchmark/claude_benchmark.py artifacts
python3 tools/task-metrics.py import-benchmark --provider claude --run-label LABEL --dry-run
```

Then import the completed label without `--dry-run`, validate metrics, append
the result to the T-137 report, checkpoint `tools/state/session.md`, and run
`git status --short`. Runner output/artifacts are authoritative; do not rerun a
normal capability failure. A setup/identity/unsafe-scope/telemetry failure stops
the matrix for review.

After the 12 visible runs, record each arm's frozen config fingerprints and
confirm equal task versions, hashes, ref, model, effort, and P2P mode. Do not
select or tune a winner yet. Execute all three WBD-005 commands exactly as
planned; only then inspect the cross-arm held-out result.

## Comparison and interpretation

```bash
python3 tools/agent-benchmark/claude_benchmark.py summarize --run-label claude-current-harness-screen-v1
python3 tools/agent-benchmark/claude_benchmark.py summarize --run-label claude-autonomous-screen-v1
python3 tools/agent-benchmark/claude_benchmark.py summarize --run-label claude-dynamic-screen-v1
python3 tools/agent-benchmark/claude_benchmark.py compare --baseline-label claude-current-harness-screen-v1 --candidate-label claude-autonomous-screen-v1
python3 tools/agent-benchmark/claude_benchmark.py compare --baseline-label claude-current-harness-screen-v1 --candidate-label claude-dynamic-screen-v1
python3 tools/task-metrics.py validate
```

Report capability, task scores, P2P/scope, wall time, dollar cost, cache-aware
effective tokens, tool output, native Agent calls, Codex MCP calls, and config
generation cost separately. Claude usage is normalized as:

`input + cache_creation + cache_read` input; effective tokens are
`total_input - cache_read + output`.

The current harness may invoke external Codex MCP workers inside nested site
agents whose tokens and even call events are not guaranteed to appear in the
root Claude stream. Current-harness runs are therefore conservatively marked
`total_token_telemetry_complete: false`. They may be compared for capability,
Claude-side load, cost, duration, and delegation behavior, but it cannot win a
total-token claim against a complete arm. State the cost result as inconclusive
unless external-worker usage is independently attributable.

One run per task is a screen, not a variance estimate. If two complete-
telemetry arms both pass 5/5 and differ by at least 10% effective tokens, a
second authorized phase may run two representative visible tasks in three
matched portfolios under new `*-repeat-v1` labels. Do not repeat WBD-005 and do
not begin repeats merely to rescue a weak result.

## Closeout

Write `tools/agent-benchmark/rounds/<date>-claude.md` with the frozen question,
identities, per-arm outcome, telemetry caveats, rejected/generated strategies,
spend, and recommendation. Update ledger/decisions and the canonical Claude
configuration only from capability-gated evidence. Restore
`.claude/settings.json` to `"agent": "site-coordinator"` and its prior effort
after the experiment; keep the benchmark driver/profile files for
reproduction unless the user requests removal.

Run metrics/schema, runner self-test/preflight, artifact audit, Markdown-size,
Python syntax, and repository regression checks. No public website change is
expected, so do not publish or deploy. Finish with the standard Claude driver
report, task metrics/log line, commit, rebase, and push gates.
