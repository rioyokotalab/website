# Agent web-development regression benchmark

This optional local suite measures Codex capability and token cost on
representative YOKOTA Lab website maintenance tasks. It combines isolated
mutated fixtures, static F2P checks, deterministic browser/visual P2P checks,
and strict changed-file scope. It is not a general frontend leaderboard.

The tracked suite contains task definitions, mutations, grader logic, and the
runner. Compact results and deterministic summaries may be retained while a
routing decision depends on them; the current 173-run comparison supports
`routing-policy.json`. New runs create ignored raw artifacts under
`tools/out/agent-benchmark/` and append compact rows to `results.jsonl`. Raw
artifacts remain disposable once their decision is durable and metric pointers
are removed with them.

Current retained evidence:

- [90-cell matrix summary](gpt56-full-20260713.summary.md)
- [83-repeat adaptive summary](gpt56-repeat-20260714.summary.md)
- [validated dispatch policy](routing-policy.json)

Coverage and deliberate gaps are documented in `coverage.md`. Failure classes
and their stop rules are in `failure-taxonomy.md`.

## Commands

```bash
python3 tools/agent-benchmark/benchmark.py list
python3 tools/agent-benchmark/benchmark.py selftest
python3 tools/agent-benchmark/benchmark.py audit
python3 tools/agent-benchmark/benchmark.py artifacts
python3 tools/agent-benchmark/benchmark.py show RUN_ID
python3 tools/agent-benchmark/benchmark.py run WBD-001 --run-label baseline --run-p2p
python3 tools/agent-benchmark/benchmark.py summarize --run-label baseline
```

Benchmark effort overrides are `low`, `medium`, `high`, `xhigh`, `max`, and
`ultra`, kept in sync with the benchmark metrics schema. `ultra` is absent from
the public model catalog but was promoted after T-146 runtime probes succeeded
on WBD-001 for Luna, Terra, and Sol. The retained
`--probe-undocumented-effort` flag identifies only those three probe runs;
normal subsequent `ultra` cells omit it.

The runner builds a temporary repository with `git archive`, removes benchmark
implementation before the worker starts, commits the mutated fixture, and
grades only the candidate diff. Never run a capsule directly in the root
repository. Publish/deploy scripts and remotes are removed from fixtures.

Use `--handoff-mode runner-lite` for short instrumented trials where the runner
captures the trajectory, patch, grade, metrics, and final message.
`runner-structured` additionally enforces `final.schema.json`; `runner` is its
legacy alias.

Use `--inspection-mode focused` only for an explicit local textual edit in a
large file. Default inspection remains required for diagnosis, refactors, and
reference-driven visual work.

WBD-005 is held out and requires `--include-held-out`. Use it only after a
candidate is frozen. A passing candidate needs every critical assertion, at
least 85/100 per task, no aggregate/P2P/scope regression, and lower measured
worker plus review/repair cost.

`effective_tokens` is input minus cached input plus output. Reasoning output is
retained separately and is not added twice.

## Decision workflow

1. Run selftest and capsule audit before any model call.
2. Probe one visible task and stop on capability failure unless raw evidence
   proves a versioned capsule defect.
3. For a broad process change, use matched tasks/repeats and compare medians and
   ranges rather than isolated minima.
4. Freeze task versions, model/effort, prompt/handoff/inspection modes, grader,
   and runner identities before the visible suite.
5. Run the held-out task only after the visible suite passes.
6. Record spend, failure taxonomy, break-even, regression checks, and review
   before promotion; delete obsolete raw/results records together.
