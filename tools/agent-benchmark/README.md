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

Use `--handoff-mode runner-lite` for short instrumented trials: the runner
captures the trajectory, patch, grade, metrics, and final message while the
worker skips its durable report and log append. `runner-structured` additionally
enforces `final.schema.json`; it is retained for measuring structured-output
overhead rather than used by default. `runner` is its legacy alias.

```bash
python3 tools/agent-benchmark/benchmark.py list
python3 tools/agent-benchmark/benchmark.py selftest
python3 tools/agent-benchmark/benchmark.py run WBD-001 --run-label baseline --run-p2p
python3 tools/agent-benchmark/benchmark.py summarize --run-label baseline
```

WBD-005 is held out and requires `--include-held-out`; use it only after an
optimization candidate is frozen. A passing optimization needs every critical
assertion, at least 85/100 on every matched task, no lower aggregate score, no
P2P or scope regression, and lower measured worker plus review/repair cost.

`effective_tokens` is `input_tokens - cached_input_tokens + output_tokens`.
Reasoning output is retained separately because runner usage reports it as a
subset/detail of output accounting; it is not added twice.
