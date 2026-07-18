driver: claude
updated: 2026-07-18T22:35+0900
task: T-199 Add Claude to the agent benchmark
status: awaiting-user

## Now
- Claude support added to tools/agent-benchmark/benchmark.py: parse_claude_jsonl
  + run_claude + dispatch_worker(model) routing any claude* model. selftest
  (with a new claude-parser case) + audit pass. Harness code landing via PR;
  frozen results.jsonl left unchanged (pilot row reverted).
- PILOT PASSED: WBD-001 / claude-fable-5 / low → score 100/100,
  critical_pass, changed exactly en+jp/index.html; worker 18.9s, total 63.5s
  (grader 34s), effective_tokens 23,121, cost $0.61 (116k cached input).
- Full-matrix decision pending owner: 5 tasks × {fable-5, opus-4-8,
  sonnet-5} × 5 efforts = 75 singletons (+ adaptive repeats). Est. ~$200–350
  and ~4–5 h sequential (Opus dominates cost). Reported; awaiting go.
- Skills applied: plan-interview-execute, research-engineering-validation,
  context-ledger.

## Working set
- tools/agent-benchmark/benchmark.py (Claude dispatch).

## Open questions
- Run full matrix autonomously, or scope it down (fewer efforts/models)?

## Awaiting user
- Go / scope for the 75-cell matrix.
