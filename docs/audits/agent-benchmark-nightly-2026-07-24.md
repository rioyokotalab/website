# Nightly agent benchmark audit — 2026-07-24

## Scope

This audit compares two exact, frozen singleton matrices against their prior
matched matrices:

- GPT-5.6: 3 models × 6 efforts × 5 tasks = 90 cells.
- Claude Code: 3 models × 5 efforts × 5 tasks = 75 cells.

Every cell starts from public commit
`edd585e991ae4348d82002bb6590fb035256633d`, uses the same task mutation and
held-out grader for its provider comparison, and runs sequentially to avoid
cross-cell contention. The current clients are Codex CLI 0.145.0 and Claude
Code 2.1.207; the prior GPT matrix used Codex CLI 0.144.3, while Claude's
client version is unchanged.

`effective_tokens` is an internal planning proxy
(`input - cached_input + output`), not monetary cost. Its units are not
comparable between providers.

## Results

<!-- T-205: final generated tables are inserted here after both frozen matrices
     pass exact-grid validation. -->

## What changed and why

### Quality

The strict score and browser-functional result are reported separately. The
frozen graders intentionally remain unchanged, but two static assertions reject
semantically equivalent JavaScript forms:

- WBD-003's `reject-first-focus` assertion accepts only a short list of literal
  spellings. Current Claude Opus/xhigh and Sonnet/xhigh both used
  `rejectButton.focus()` and passed all four browser consent tests.
- WBD-005's `js-reduced-zero` assertion assumes one object naming/layout.
  Current candidates can instead select a zero-valued reduced-motion object
  while keeping ordinary 600/600/700 durations inline. Those candidates pass
  all five browser tests.

These rows remain strict misses in the immutable matrix. They are counted as
browser-functional only when every browser check passes; no result is silently
regraded.

GPT's WBD-005 strict result improved from 13/18 to 14/18 and its browser result
from 17/18 to 18/18. Five previously failing routes recovered, including the
prior Terra/xhigh browser failure. Four new 91-point rows are browser-functional
and fail only `js-reduced-zero`.

Claude Sonnet/low produced one genuine WBD-005 regression: it edited
out-of-scope `js/pagetop.js`, set the ordinary-motion durations to zero, and
failed two reduced-motion browser tests. This row is not classified as a grader
blind spot. A separately labeled, one-cell focused-inspection retry tests
whether a tighter workflow recovers the route while preserving the failed
singleton in the broad matrix.

### Runtime

Current wall time is materially noisier and generally slower. This cannot be
attributed to model quality alone:

- WBD-002's browser-grader component rose by roughly 26 seconds for both
  providers, identifying a shared runner/environment contribution.
- The active Claude process was observed in the kernel's `nfs_wait` state while
  stream JSON was being written directly to the NFS-backed artifact directory.
  Worker time therefore includes confirmed storage blocking.
- Setup, worker, and grader medians all increased in at least one matched task
  block. Singletons do not separate transient service latency from these local
  effects.

Future benchmark infrastructure should stage raw worker output on local scratch
and copy it into the durable artifact directory only after the worker exits.
That change was not made during these frozen matrices because it would alter
their runner identity.

### Token proxy and workflow

Claude's current safe invocation uses print mode, `dontAsk`, no session
persistence, a reviewed local tool allowlist, and explicit remote/web/publish
denials. Its fresh/cache-creation term is much larger than the prior reported
proxy, so the token delta is partly an invocation-accounting change rather than
a model-efficiency regression.

One Claude WBD-004 route attempted `Edit` twice after inspecting through shell
commands. Claude's tool policy requires a tool-level `Read` before `Edit`; the
route succeeded after performing that read. This is confirmed avoidable
workflow overhead, not task difficulty.

## Interpretation limits

- Each broad-matrix route is a singleton. Runtime and token medians summarize
  routes, not repeated service-level guarantees.
- Task, prompt, baseline, and scoring semantics are matched. GPT's grader hash
  changed only because the protected ledger filename changed from
  `tools/todo.md` to `TODO.md`; Claude's grader hash is identical.
- Exact historical global tool-schema context was not frozen.
- Focused follow-up cells are reported separately and never added to singleton
  denominators.

## Reproducibility

The exact freezes, machine-readable summaries, matched comparison reports, and
focused experiment are linked from the README benchmark section. Raw artifacts
for this nightly run remain locally available under
`tools/agent-benchmark/artifacts/`; compact result rows and summaries are
tracked.
