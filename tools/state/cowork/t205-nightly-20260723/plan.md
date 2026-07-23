# Initial plan

## Confirmed facts and assumptions

- Confirmed: the target is clean public `main` at `edd585e`; historical compact
  evidence contains 90 GPT singleton cells, 83 GPT repeats, 75 Claude singleton
  cells, and 14 Claude repeats.
- Confirmed: prior GPT cells used Codex CLI 0.144.3; current Codex is 0.145.0.
  Prior and current Claude use CLI 2.1.207.
- Confirmed: selftest and the pristine/mutated audit pass for all five task
  versions. Existing task definitions support Codex and Claude dispatch.
- Confirmed: `run_matrix.py` is tied to the old GPT freeze and currently looks
  for results under `tools/out/agent-benchmark` while `benchmark.py` writes to
  `tools/agent-benchmark/artifacts`; it cannot safely orchestrate a new matrix
  unchanged.
- Confirmed: prior Claude execution used
  `--dangerously-skip-permissions`. The new protocol must replace that with a
  reviewed non-prompting mode/tool allowlist or an environment-native boundary;
  comparable methodology differences must be disclosed.
- Confirmed: T-203 removed historical Claude raw directories intentionally,
  while retaining result rows and summaries. Historical comparison therefore
  relies on tracked compact evidence.
- Assumption to test: the same public model names remain accepted by current
  clients. A bounded visible low-effort probe will falsify this before broad
  spend.
- Assumption to test: performance changes primarily reflect Codex client/model
  service variance, host/NFS effects, and safer Claude invocation rather than
  changed task semantics. Identity hashes and matched repeats will separate
  those explanations.

## Steps

1. Create independent same-baseline sandboxes, validate their identities, and
   run a blinded driver evidence pass covering runner integrity, one safe
   visible dry/probe path, matrix completeness, time estimates, and security.
2. Stage the same charter/plan for Claude with an external seal and protected
   live digests. Run Claude natively with a bounded evidence prompt, import only
   after semantic inspection and receipt validation, then repeat with both
   evidence files exposed for reciprocal critique.
3. Reconcile disagreements and freeze: model/effort grids, run labels,
   baseline/task/grader hashes, runner/prompt/handoff/inspection identities,
   order, capability probes, historical comparator, visible/held-out split,
   iteration budget, and hard closeout reserve.
4. As driver, implement only the minimum benchmark infrastructure required for
   generic freeze-driven resumable Codex and Claude matrices, correct artifact
   path validation, deterministic analysis, and a non-bypass Claude worker
   invocation. Add focused tests before any broad call.
5. Run selftest/audit and one low-effort WBD-001 capability probe per provider.
   Stop a provider on model/effort/auth/telemetry/infrastructure failure; do not
   reinterpret absence as a score.
6. Run the complete singleton baselines sequentially from the immutable target
   commit: GPT has 3 models × 6 efforts × 5 tasks = 90 cells; Claude has
   3 models × 5 efforts × 5 tasks = 75 cells. Run visible task blocks first and
   hold WBD-005 until the protocol candidate is frozen.
7. Compare current vs historical matrices by model, effort, and task using
   full-quality counts, score failures, medians, dispersion, effective tokens,
   CLI identities, and failure taxonomy. Never infer a general trend from one
   singleton; schedule matched repeats for failures or material shifts.
8. Iterate only on workflow variables that do not change task/grader
   semantics—prompt/handoff/inspection discipline, route selection, and
   non-bypass Claude tool policy. Test on visible tasks with matched routes;
   accept a change only if quality is non-inferior and runtime/tokens improve
   reproducibly. Freeze before held-out WBD-005.
9. Complete held-out cells/repeats, write provider summaries and a cross-run
   comparison explaining supported causes and uncertainties, then update the
   README table with exact denominators and current CLI context.
10. Validate results/metrics schemas, benchmark identities, receipt chain,
    focused tests, offline/browser regression, final diff, Git cleanliness,
    and no deployment. Publish through protected PR/CI, merge, and leave the
    ledger idle with raw evidence pointers and cleanup state.

## Evidence questions

1. Can the current runner produce and locate one complete artifact for each
   provider, and can every row be tied to the same task/grader/baseline hashes?
2. Are all six public model names and documented effort levels still accepted?
3. Which current-vs-prior changes exceed singleton variance, and do matched
   repeats reproduce them?
4. Do failures cluster by task assertion, model, effort, provider, invocation
   policy, or NFS/host timing?
5. Can Claude run unattended without the dangerous bypass flag while retaining
   required fixture-local tools and zero external writes?
6. Does compact/focused workflow reduce time or tokens without scope, P2P,
   critical-assertion, or held-out regression?
7. Is the eight-hour budget sufficient for complete comparable matrices plus
   repeats and protected closeout; what is the deterministic truncation order
   if it is not?

## Risks and recovery

- Cost/time: 165 singleton calls plus repeats may approach the eight-hour
  window. Run sequentially for comparable wall time, checkpoint each row, stop
  new calls with at least 45 minutes reserved for analysis/validation, and
  never publish a partial grid as complete.
- Client/model drift: a name or effort may be rejected. Stop that provider,
  retain exact non-secret error evidence, inspect current help, and revise only
  with a recorded identity change; never silently substitute.
- Unsafe Claude automation: the previous bypass flag conflicts with the
  current security posture. Use `dontAsk` plus reviewed tools and capsule
  authority; if unattended editing cannot work safely, stop rather than weaken
  safeguards.
- Statistical overclaim: singletons are noisy. Use medians only for complete
  groups, matched repeats for failures/material shifts, and label causal
  explanations as evidence-backed or uncertain.
- Benchmark gaming: changes to tasks, graders, thresholds, held-out visibility,
  or failure filtering are forbidden. Hash identities and review the final
  diff.
- Partial artifacts/results: run IDs are immutable and resumable. Record exact
  changed state and retry only when no result row exists; never overwrite or
  duplicate a run ID.
- Sandboxes/raw artifacts consume space. Retain them during the run. Any
  multi-path/tree cleanup requires guarded deletion and post-delete checks.
- Publication: re-fetch/rebase, run protected checks, and stop on ambiguity.
  No force-push or website deployment.
