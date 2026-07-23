# Driver evidence

## Sandbox and baseline

- Sandbox: `/home/rioyokota/.cache/t205-cowork/driver`.
- Baseline: detached clean
  `edd585e991ae4348d82002bb6590fb035256633d`, created by a local
  `git clone --no-hardlinks` from the target.
- Client: Codex CLI 0.145.0. The sandbox had a private copied `node_modules`
  tree and a local Playwright-cache link; neither target files nor the live
  cowork session were writable experiment outputs.
- The first metadata-preserving dependency copy returned nonzero because the
  destination filesystem does not support the requested permission operation.
  Ordinary `cp -R` completed the same task; 180 regular files, two symlinks,
  and the Playwright executable matched. This was retry-safe and target-neutral.

## Commands and results

1. `python3 tools/agent-benchmark/benchmark.py selftest` passed: five tasks,
   both telemetry parsers, and all six benchmark effort values were valid.
2. `python3 tools/agent-benchmark/benchmark.py audit` passed. Each pristine
   capsule passed and every mutation failed its intended critical assertions.
3. A real visible-task probe ran:
   `benchmark.py run WBD-001 --ref HEAD --model gpt-5.6-terra --effort low
   --prompt-mode full --handoff-mode runner-lite --inspection-mode default
   --run-p2p`. It passed every gate at 100/100, changed exactly the two expected
   files, used 13,586 effective tokens, and took 55.664 seconds total
   (37.311 seconds worker).
4. The matched historical cell also passed 100/100 at 13,468 tokens and
   66.094 seconds total (49.519 seconds worker). The current probe is 10.430
   seconds faster with 118 more tokens, but one pair cannot establish a trend.
5. Static runner inspection found that `run_matrix.py` hard-codes the old GPT
   freeze and computes its result path under `tools/out/agent-benchmark`,
   whereas `benchmark.py` writes under
   `tools/agent-benchmark/artifacts`. A new matrix would finish a model call
   and then fail its orchestration acceptance.
6. Static Claude inspection found the benchmark worker invokes
   `--dangerously-skip-permissions`. That reproduces the old method but violates
   the new charter; it must be replaced and disclosed before current Claude
   calls.

## Critique

- The initial plan correctly requires probes and matched identities, but a full
  165-cell baseline before workflow iteration is inefficient. The visible
  blocks should run first, followed by analysis/iteration, with WBD-005 released
  only for the frozen candidate.
- “Same benchmark” must distinguish task/grader comparability from invocation
  comparability. Codex CLI changed; Claude's permission route must change.
  These are measured covariates, not reasons to discard the run.
- The plan needs a generic provider-neutral freeze runner and analyzer before
  broad execution. Ad-hoc shell loops would weaken resumability and identity
  validation.
- Effective-token and time differences must use within-provider matched cells.
  The single probe is evidence of capability only, not improvement.
- Historical raw-artifact audit failure is expected archival state, but new
  labels must have complete raw artifacts throughout this task.

## Proposed plan changes

1. Add a `--freeze` option to the matrix runner, derive provider-neutral run
   IDs without hard-coded GPT prefixes, and use the benchmark's canonical
   artifact root. Add a dry-run/fixture test that would catch the current path
   mismatch.
2. Freeze two new singleton matrices with shared task/grader/baseline hashes
   and provider-specific model/effort grids. Include client versions, runner
   hash, prompt hash, and invocation policy.
3. Replace Claude's bypass flag with `--permission-mode dontAsk` plus an exact
   reviewed tool allowlist. Probe fixture editing and telemetry before the
   Claude matrix; stop if this cannot operate unattended.
4. Run WBD-001–004 sequentially for both providers, analyze failures and
   material shifts, then test only the strongest workflow alternative on
   matched visible routes. Freeze the candidate before WBD-005.
5. Reserve at least 45 minutes for summaries, validation, cowork closeout, and
   protected publication. If the time gate is reached, retain partial rows and
   do not rewrite the complete README table.
