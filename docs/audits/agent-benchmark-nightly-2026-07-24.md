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

Within each current frozen grid, exact-cell, task, baseline, runner, grader,
client, and workflow identities passed validation. The matched-comparison
caveats below identify identities that changed from the prior grid.

| Provider | Previous strict | Current strict | Previous browser-functional | Current browser-functional |
| --- | ---: | ---: | ---: | ---: |
| GPT-5.6 | 85/90 | 86/90 | 89/90 | 90/90 |
| Claude Code | 72/75 | 71/75 | 74/75 | 74/75 |

The matched per-cell median wall-time delta was +38.2 seconds for GPT and
+13.8 seconds for Claude. GPT's median effective-token delta was +5,246.
Claude's was +104,129, but its invocation/accounting changed as described
below.

### Task-level matched results

Each cell shows strict passes, browser-functional passes, and median total time.

| Provider / task | Previous | Current |
| --- | ---: | ---: |
| GPT WBD-001 | 18/18, 18/18, 112.8 s | 18/18, 18/18, 113.8 s |
| GPT WBD-002 | 18/18, 18/18, 129.7 s | 18/18, 18/18, 186.1 s |
| GPT WBD-003 | 18/18, 18/18, 44.6 s | 18/18, 18/18, 70.7 s |
| GPT WBD-004 | 18/18, 18/18, 88.6 s | 18/18, 18/18, 121.3 s |
| GPT WBD-005 | 13/18, 17/18, 206.0 s | 14/18, 18/18, 264.4 s |
| Claude WBD-001 | 15/15, 15/15, 89.1 s | 15/15, 15/15, 82.8 s |
| Claude WBD-002 | 15/15, 15/15, 132.3 s | 15/15, 15/15, 146.7 s |
| Claude WBD-003 | 12/15, 14/15, 62.6 s | 13/15, 15/15, 83.0 s |
| Claude WBD-004 | 15/15, 15/15, 112.5 s | 15/15, 15/15, 135.9 s |
| Claude WBD-005 | 15/15, 15/15, 212.1 s | 13/15, 14/15, 223.1 s |

### Focused workflow iteration

Focused inspection was tested only on the three observed current Claude misses
selected in advance:

| Route | Default | Focused | Interpretation |
| --- | ---: | ---: | --- |
| Opus/xhigh, WBD-003 | 89, browser pass | 100 | recovered |
| Sonnet/xhigh, WBD-003 | 89, browser pass | 89, browser pass | static blind spot persists |
| Sonnet/low, WBD-005 | 63, browser fail | 100, browser pass | functional recovery |

The WBD-005 recovery took 212.5 seconds versus 137.2 seconds for the failed
default cell. Focused inspection is therefore a useful reliability fallback for
cross-cutting changes, not evidence that it should replace every default route.
These cells are not included in either singleton denominator.

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

The matched matrix contains five GPT recoveries and four GPT regressions at the
strict gate, for a net +1 capability pass. Claude has three recoveries and four
regressions, for a net −1 strict pass. This route churn—despite stable task
definitions—shows why a one-point aggregate change should not be interpreted as
a general model capability shift.

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
- Task, prompt, baseline, and scoring semantics are matched. The reviewed GPT
  grader diff was the protected-ledger rename from `tools/todo.md` to
  `TODO.md`; Claude's grader hash is identical.
- Exact historical global tool-schema context was not frozen.
- Focused follow-up cells are reported separately and never added to singleton
  denominators.

## Reproducibility

The exact freezes, machine-readable summaries, matched comparison reports, and
focused experiments are linked from the README benchmark section and colocated
under `tools/agent-benchmark/`. Raw artifacts
for this nightly run remain locally available under
`tools/agent-benchmark/artifacts/`; compact result rows and summaries are
tracked.
