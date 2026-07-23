# Reconciliation

## Evidence accepted

- Both agents confirmed the immutable baseline
  `edd585e991ae4348d82002bb6590fb035256633d`, the unchanged five-task
  corpus, and the current client identities: Codex CLI 0.145.0 and Claude Code
  2.1.207.
- The driver independently passed `benchmark.py selftest` and `audit`, and a
  real Codex `gpt-5.6-terra`/`low` WBD-001 capability probe passed every gate
  at 100/100. Its 55.664-second total runtime is not trend evidence by itself.
- Both agents confirmed that the existing matrix runner hard-codes the July
  GPT freeze and checks the wrong artifact root. Broad execution is blocked
  until a generic freeze-driven runner and a path-catching test exist.
- Both agents confirmed that the historical Claude invocation hard-codes
  `--dangerously-skip-permissions`. The current run must use `dontAsk` with a
  reviewed capsule-local tool set, and this methodology change must be
  disclosed.
- Historical complete singleton runtime is the planning estimate: 2.996 hours
  for 90 GPT cells and 2.734 hours for 75 Claude cells. The combined 5.73-hour
  measurement supports attempting both matrices within the eight-hour window,
  while retaining the 45-minute closeout reserve.
- The co-pilot's independently sealed evidence and reciprocal critique were
  semantically reviewed and imported. Both receipts pass the skill's receipt
  validation, and protected live-file digests remained unchanged.

## Disagreements and uncertainty

- The apparent 10.430-second Codex probe improvement is accepted only as
  capability evidence. It is rejected as evidence of a speed trend until
  matched repeats or a complete matched group exist.
- Run IDs remain the existing deterministic
  `(run_label, task, model, effort)` form. Each distinct prompt, handoff, and
  inspection combination receives a unique run label, and validation rejects
  one label spanning multiple mode combinations. This avoids a mid-series ID
  schema change without losing identity.
- The co-pilot could inspect Git and source but its own `dontAsk` boundary
  denied Python execution, even with correct selftest syntax. The driver is
  therefore the execution authority for selftest/audit; the record does not
  claim independent co-pilot execution.
- A non-bypass Claude subprocess is still an empirical gate. It must edit and
  validate WBD-001 normally, and a denied-tool fixture must produce a bounded,
  explicit failure rather than a hang before the broad Claude matrix begins.
- Runtime and tokens remain noisy. Comparisons use complete matched groups,
  provider-internal token units, dispersion, and targeted repeats. Client,
  service, host/NFS, and Claude permission-policy changes are covariates, not
  automatically causal explanations.

## Frozen plan

1. Implement a provider-neutral `--freeze` matrix route, canonical artifact
   lookup, dry-run validation, unique-label/mode validation, and deterministic
   matrix comparison. Preserve old result-row and run-ID compatibility.
2. Replace Claude's bypass invocation with print-mode stream JSON,
   `--permission-mode dontAsk`, no session persistence, and the reviewed
   capsule-local tools `Read`, `Edit`, `Write`, and `Bash`. The capsule has no
   remotes or publish authority; the behavioral workspace boundary remains an
   explicitly recorded residual rather than an OS sandbox claim.
3. Freeze two new labels with baseline/task/grader/client/runner/mode hashes:
   `gpt56-nightly-20260723-full` and
   `claude-nightly-20260723-full`. Both use `full`, `runner-lite`, `default`,
   P2P enabled, WBD-001 through WBD-004 first, and WBD-005 last.
4. Run driver selftest/audit and provider capability probes. Stop only the
   affected provider on identity, authentication, telemetry, timeout, or
   non-bypass-policy failure; preserve exact public diagnostics.
5. Execute the complete singleton grids from the immutable baseline:
   GPT = 3 models × 6 efforts × 5 tasks = 90 cells; Claude = 3 models ×
   5 efforts × 5 tasks = 75 cells. Alternate provider blocks so partial
   progress is balanced, while preserving provider-internal order.
6. At each 15-cell checkpoint, project completion from measured wall time.
   Stop new optional repeats first if the projection enters the closeout
   reserve. The complete singleton matrices take precedence over workflow
   experiments; no partial matrix may replace a complete README denominator.
7. Compare current and July matrices by provider, model, effort, and task.
   Repeat only failures or material visible-task shifts that can finish before
   the reserve. Accept a workflow change only with matched non-inferior quality
   and repeatable time/token benefit; freeze it before any held-out use.
8. Stop launching calls no later than 45 minutes before the eight-hour
   boundary. Generate summaries, update README only from complete matrices,
   validate repository/results/receipts, publish through protected Git, and do
   not deploy the website.

## Acceptance gates

- Generic runner tests catch an invalid freeze, artifact-root mismatch,
  duplicate run ID, and one run label spanning multiple workflow modes.
- `benchmark.py selftest` and `audit` pass, and both WBD-001 capability probes
  complete with raw artifacts and valid telemetry.
- Every published matrix has its full expected grid and a unique immutable row
  per cell; task, grader, prompt, baseline, client, runner, and workflow
  identities match its freeze.
- Claude's command contains no dangerous bypass, the normal probe succeeds,
  and the denial-path probe terminates clearly within its bound.
- Comparisons do not mix provider token units, suppress failures, weaken
  graders, or describe singleton noise as causation.
- Focused tests, `git diff --check`, the repository offline suite, relevant
  browser checks, cowork receipt validation, final diff review, and protected
  CI pass before merge. No deployment occurs.
