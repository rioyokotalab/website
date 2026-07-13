# Agent web-development regression benchmark

This local benchmark measures capability and token cost on representative
YOKOTA Lab website maintenance tasks. It borrows frozen repository tasks and
F2P/P2P grading from SWE-bench-style evaluation, then adds deterministic local
browser checks. It is not a general frontend leaderboard.

The runner creates a temporary repository from `git archive`, removes the
benchmark implementation before the agent starts, commits the mutated fixture,
and grades only the resulting candidate diff. Raw Codex JSONL, stderr, prompt,
patch, and result live under ignored `tools/out/agent-benchmark/`; compact
per-run rows are appended to `results.jsonl`.

`run` prints a compact decision summary by default; the complete result remains
in its artifact directory. Use `--verbose-result` only when a downstream caller
needs the full inline grader tails rather than following the artifact pointer.

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
