driver: codex
updated: 2026-07-14T05:02+0900
task: T-153 Close the eight-hour campaign | idle
status: idle

## Now
- The user-authorized eight-hour GPT-5.6 routing campaign is complete. No
  benchmark cell remains in flight or pending, and no website publish ran.
- Final evidence is 90 matrix + 83 adaptive = 173 unique runs, 155 capability
  passes, and 154 full-quality passes. Results, artifact directories, and v2
  metric pointers reconcile 173/173/173; all 17 repeat stages report zero
  pending. Summed end-to-end time is 20,645,537 ms and effective tokens are
  4,824,076; monetary cost remains unknown.
- Policy `2026-07-14.3` selects Terra/low for WBD-001; Luna/low runtime and
  Sol/low tokens for WBD-002; Terra/low runtime and Sol/low tokens for WBD-003;
  Luna/low runtime and Sol/low tokens for WBD-004; and Sol/high for WBD-005.
  WBD-001--004 selected routes are 6/6 high-confidence. WBD-005 Sol/high is
  8/9 qualified and requires the full static/browser grader.
- Final policy/hash/evidence/task-coverage/reliability/fallback validation,
  20 selector lookups, deterministic regeneration, artifact/metrics/selftests,
  five mutation/pristine capsules, report assertions, `git diff --check`, and
  the independent follow-up review all pass. Six driver rows for
  T-147--T-149 and T-151--T-153 were appended.
- Resolved incidents remain excluded from evidence: one result-less ENOSPC
  attempt and one uncommitted missing-browser-cache grade. The canonical clone
  is `/tmp/yokota-campaign-local`; final report is
  `tools/out/driver-report-20260714-0508.md`.

## Working set
- `tools/agent-benchmark/gpt56-repeat-20260714.summary.{json,md}`
- `tools/agent-benchmark/routing-policy.json`
- `tools/agent-benchmark/select_route.py`
- `skills/codex-delegation.md`
- `tools/state/{facts,decisions,session}.md`, `tools/todo.md`
- `tools/out/driver-report-20260714-0508.md`

## Open questions
- None.

## Awaiting user
- None.
