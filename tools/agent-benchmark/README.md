# Agent web-development regression benchmark

This local benchmark measures capability and token cost on representative
YOKOTA Lab website maintenance tasks. It borrows frozen repository tasks and
F2P/P2P grading from SWE-bench-style evaluation, then adds deterministic local
browser checks. It is not a general frontend leaderboard.

Current capability coverage, deliberate gaps, and the threshold for adding a
new capsule are documented in `coverage.md`. Failed-token causes and the stop
rule each category should trigger are in `failure-taxonomy.md`.

The runner creates a temporary repository from `git archive`, removes the
benchmark implementation before the agent starts, commits the mutated fixture,
and grades only the resulting candidate diff. Raw Codex JSONL, stderr, prompt,
patch, and result live under ignored `tools/out/agent-benchmark/`; compact
per-run rows are appended to `results.jsonl`.

## Artifact retention

Keep every run directory referenced by `results.jsonl` or schema-v2 metrics
through at least the next completed benchmark round. The required durable set
is `prompt.txt`, `stdout.jsonl`, `stderr.log`, `candidate.patch`, and
`result.json`; `benchmark.py artifacts` verifies it. Screenshots are optional
diagnostic material: retain decision anchors (the accepted baseline, a
decision-changing failure, and the promoted result) and delete redundant
intermediate copies after their grades and patches are recorded. Per-task and
driver Markdown under `tools/out/` is transient and should be removed once its
decisions are tracked and its reviewer has finished.

Do not delete a referenced run directory merely to reduce disk use. A future
archive/prune operation must first provide a manifest or tombstone mechanism so
metrics pointers remain auditable. Compact completed-round records belong in
`rounds/`; raw trajectories never enter Git.

`run` prints a compact decision summary by default; the complete result remains
in its artifact directory. Use `--verbose-result` only when a downstream caller
needs the full inline grader tails rather than following the artifact pointer.
Failure summaries deduplicate `changed:` findings already represented by
`changed_files` while preserving their count and all diagnostic findings.

Use `--handoff-mode runner-lite` for short instrumented trials: the runner
captures the trajectory, patch, grade, metrics, and final message while the
worker skips its durable report and log append. `runner-structured` additionally
enforces `final.schema.json`; it is retained for measuring structured-output
overhead rather than used by default. `runner` is its legacy alias.

Use `--inspection-mode focused` when target files are large but an explicit
textual edit is local. It tells the worker to search for a task-specific literal, inspect no
more than 40 surrounding lines, and follow the named playbook's preservation
method. The earlier `bounded` wording remains available for reproducing an
experiment that reduced output but allowed a CRLF regression. Each result
records the mode so comparisons do not silently mix inspection strategies.
Use default inspection for reference-driven visual work and diagnosis.

```bash
python3 tools/agent-benchmark/benchmark.py list
python3 tools/agent-benchmark/benchmark.py selftest
python3 tools/agent-benchmark/benchmark.py audit
python3 tools/agent-benchmark/benchmark.py artifacts
python3 tools/agent-benchmark/benchmark.py show RUN_ID
python3 tools/agent-benchmark/benchmark.py run WBD-001 --run-label baseline --run-p2p
python3 tools/agent-benchmark/benchmark.py summarize --run-label baseline
```

WBD-005 is held out and requires `--include-held-out`; use it only after an
optimization candidate is frozen. A passing optimization needs every critical
assertion, at least 85/100 on every matched task, no lower aggregate score, no
P2P or scope regression, and lower measured worker plus review/repair cost.

For a process-wide optimization, use at least two representative tasks and
three baseline/candidate portfolio samples. Compare portfolio medians and full
ranges, not isolated task minima. Promotion requires all capability gates,
candidate median effective tokens at least 5% below baseline, and no unexplained
regression in failures, tool output, or total duration. Non-overlapping ranges
are strong evidence; overlapping ranges make the cost claim inconclusive. After
freezing the candidate, run every visible task and the held-out task once.

`effective_tokens` is `input_tokens - cached_input_tokens + output_tokens`.
Reasoning output is retained separately because runner usage reports it as a
subset/detail of output accounting; it is not added twice.

## Decision workflow

1. Run `benchmark.py selftest`, `benchmark.py audit`, and `benchmark.py
   artifacts` before any model call.
2. Give a new variant one visible-task probe. Stop on capability failure unless
   raw evidence proves a capsule defect; require at least 10% preliminary cost
   improvement before repeats.
3. For a process-wide candidate, collect at most three matched portfolios over
   two representative tasks. Import them into metrics and use strict `compare`.
4. Freeze task versions, routes, prompt/handoff/inspection modes, grader, and
   runner identities. Run every visible task once with P2P.
5. Only after the visible suite passes, run the held-out task once. A rerun
   requires a documented, versioned capsule invariant defect.
6. Record per-label spend, failed-token taxonomy, break-even, raw artifact audit,
   repository regression, and driver review before promotion.

Do not down-route an exposed held-out task or edit a task/grader merely to turn
an ordinary capability failure into a pass.

## Starting the next round

Start only for a concrete model/runtime/process change or a real task that
exposes a documented coverage gap. Read the latest `rounds/` record, then run:

```bash
python3 tools/agent-benchmark/benchmark.py selftest
python3 tools/agent-benchmark/benchmark.py audit
python3 tools/agent-benchmark/benchmark.py artifacts
python3 tools/task-metrics.py validate
```

Pre-register the candidate, matched task versions/routes, token budget, and
stop condition in the ledger before spending model tokens. Give it one visible
probe; continue to matched portfolios only if capability passes and the probe
improves effective tokens by at least 10%.
