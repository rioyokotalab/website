driver: codex
updated: 2026-07-14T04:24+0900
task: T-153 Close the eight-hour campaign
status: in-progress

## Now
- User authorized an adaptive eight-hour GPT-5.6 campaign ending
  2026-07-14T05:08+0900. New benchmark execution is complete; retain the
  remaining window for independent review, policy verification, durable
  closeout, commit, and push. Do not publish the website.
- Frozen matrix `gpt56-full-20260713` is complete: 90/90 unique cells across
  Luna/Terra/Sol, six efforts, and five WBD tasks; 85 capability passes and 84
  full-quality passes. All 173 matrix+repeat artifacts/result/metric pointers
  reconcile.
- Adaptive set `gpt56-repeat-20260714` is complete: 83/83 planned rows in 17
  stages, 70 full-quality passes, 13 genuine capability failures, 9,858,353 ms
  summed end-to-end time, and 2,259,278 effective tokens. Deterministic analysis
  and all stage dry-runs pass; plan SHA-256 is
  `266d2d782a422f43e76056b6d69eea0b3d57623fb8fbfce12fe85ce2632f0137`.
- Policy `2026-07-14.3` selects Terra/low for WBD-001; Luna/low runtime and
  Sol/low tokens for WBD-002; Terra/low runtime and Sol/low tokens for WBD-003;
  Luna/low runtime and Sol/low tokens for WBD-004; and Sol/high for WBD-005.
  WBD-001--004 selected routes are 6/6 high-confidence. WBD-005 Sol/high is
  8/9 qualified (Wilson lower 0.565; expected 249,071 ms and 45,053 effective
  tokens per success) and requires the full grader because one failure was
  observed.
- Policy validation, source-summary SHA verification, and all 15 objective
  lookups pass. Metrics validate at 180 rows (173 v2 benchmark + seven legacy
  driver); artifacts audit at 173 directories and 46,540,517 bytes.
- Independent worker review confirms 154/173 combined full-quality passes,
  exact frozen identities/counts, all objective routes, and no remaining policy
  mismatch; report: `tools/out/benchmark-final-audit-20260714.md`.
- Selector validation now cross-checks all five task IDs, 12 policy routes,
  reliability ordering, and objective choices against the pinned summary;
  negative tests reject stale hashes, altered evidence, deleted tasks,
  duplicate routes, weaker reliability choices, and external summary symlinks.
  All 15 lookups return a fallback chain that excludes the selected route.
- Follow-up independent mutation review passes with no blocker: canonical
  validation passes; 72/72 evidence mutations, 15/15 alternate selections,
  and 16/16 grouped coverage/reliability/path/fallback checks behave correctly.
- Timeout audit: zero of 173 workers timed out. Task defaults were 300/300/600/
  600/900 seconds; the maximum worker duration was 325,613 ms, so task-specific
  relaxation protected broad work without slowing the short-task failure gate.
- Resolved incidents: `/home` ENOSPC moved canonical work to
  `/tmp/yokota-campaign-local`; one result-less partial attempt was removed.
  One invalid missing-browser-cache result was transactionally removed and
  identically rerun after restoring Chromium. Neither is benchmark evidence.

## Working set
- `tools/agent-benchmark/gpt56-repeat-20260714.summary.{json,md}`
- `tools/agent-benchmark/routing-policy.json`
- `tools/agent-benchmark/select_route.py`
- `tools/todo.md`, `tools/state/session.md`
- Pending: independent audit, final driver report/metrics/log, final audit,
  tools-only commit and `github:rioyokotalab/website` push.

## Open questions
- None.

## Awaiting user
- None.
