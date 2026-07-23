# Validation

## Checks

- `benchmark.py selftest`: pass; five tasks and both telemetry parsers validate.
- `benchmark.py audit --ref edd585e...`: pass; every pristine capsule passes
  and every mutation fails its intended assertions.
- `test_matrix.py`: 3/3 pass.
- Frozen analyzers: exact 90-cell GPT, 75-cell Claude, two-cell WBD-003
  focused, and one-cell WBD-005 focused grids pass identity validation.
- Raw artifacts: 90/90 GPT, 75/75 Claude, 2/2 and 1/1 focused `result.json`
  files exist.
- `task-metrics.py validate`: 412 rows, zero errors.
- `cowork-session verify-receipts`: independent/reciprocal receipt chain valid.
- `cowork-session check --phase validating`: pass.
- `tools/test-security.sh`: pass.
- `npx playwright test`: 38/38 pass in 6.0 minutes.
- `git diff --check`: pass.

## Outcome

The broad matrices, matched comparisons, focused workflow experiments, README
tables, and audit satisfy the charter. Strict and browser-functional results
remain separate, focused cells are excluded from singleton denominators, and
the final reciprocal critique's one wording correction is applied.

## Residual risks

- Current routes have one observation each; runtime candidates require repeats
  before becoming service-level routing guarantees.
- Wall time includes observed hard-NFS waits and shared browser-grader variance.
- Claude's safe fresh invocation changes its effective-token accounting
  baseline; provider token units remain non-comparable.
- Literal-sensitive WBD-003/WBD-005 static assertions still reject some
  browser-correct implementations. The frozen rows are preserved without
  regrading.
