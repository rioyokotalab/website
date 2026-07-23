# Driver execution

## Steps and results

1. Re-fetched public `origin/main`; the frozen baseline remained
   `edd585e991ae4348d82002bb6590fb035256633d`.
2. Generalized `run_matrix.py` around an explicit freeze, corrected artifact
   lookup to `tools/agent-benchmark/artifacts/`, retained historical run-ID
   compatibility, and added unique-label/workflow validation plus focused
   tests.
3. Replaced Claude's dangerous bypass with print-mode stream JSON,
   `dontAsk`, no session persistence, the reviewed
   `Read`/`Edit`/`Write`/`Bash` allowlist, and explicit denials for dynamic
   tool discovery, web tools, remote shells/transfers, downloads, GitHub CLI,
   and Git push.
4. Driver selftest and all five pristine/mutated capsule audits passed. The
   focused matrix test passed three cases, and both 90-cell/75-cell freeze dry
   runs produced exact complete plans.
5. A deliberately disallowed Bash call under the Claude subprocess policy
   attempted the tool, returned a structured permission denial and result,
   exited zero, and did not time out. This proves the wrapper observes a
   bounded denial rather than hanging.
6. Codex capability cell
   `gpt56-nightly-20260723-full-low-luna-wbd001` passed 100/100 in
   86,191 ms with 15,556 effective tokens.
7. Claude capability cell
   `claude-nightly-20260723-full-low-fable-5-wbd001` passed 100/100 in
   49,236 ms with 123,383 effective tokens under the non-bypass policy.
8. The remaining visible singleton blocks are running sequentially with
   provider alternation and immutable per-cell checkpoints.
9. WBD-001 completed as an exact matched block: GPT 18/18 and Claude 15/15
   capability/full-score passes. GPT median time was effectively flat
   (112.8 → 113.8 seconds) while median effective tokens rose
   22,049 → 29,988. Claude median time improved 89.1 → 82.8 seconds while
   effective tokens rose 25,071 → 129,736.
10. At 30 total cells, provider-specific matched median runtime scales were
    1.24× for GPT and 0.88× for Claude. Applying each only to its provider
    projected singleton completion near 04:03 JST; optional repeats remain
    deferred, and the sequential protocol remains intact.
11. WBD-002 completed without a capability or score miss: GPT 18/18 and
    Claude 15/15. Task-wide median total time moved 129.7 → 186.1 seconds for
    GPT and 132.3 → 146.7 seconds for Claude. The browser-grader component rose
    by approximately 26 seconds for both providers, isolating a shared current
    runner/environment contribution rather than attributing the whole delta to
    either worker.
12. GPT WBD-003 completed 18/18 at 100. Claude Fable completed 5/5 at 100.
    Claude Opus/max recovered its July singleton miss and scored 100, while
    Opus/xhigh newly scored 89 after failing only `reject-first-focus`; its
    scope and changed file were otherwise correct. The singleton is retained
    and a matched repeat is required before classifying the regression.
13. Artifact review showed that Opus/xhigh implemented
    `rejectButton.focus()`, and all four browser consent tests passed. The
    static assertion recognizes only three equivalent literal spellings and
    does not recognize this local-variable form. The 89 is therefore a
    confirmed static-grader false negative, not a user-visible functional
    regression. Do not change or regrade the frozen singleton; test whether
    `inspection-mode=focused` reduces this syntax variance in a separately
    labeled workflow cell if closeout time permits.
14. Sonnet/xhigh independently produced the same semantically correct
    `rejectButton.focus()` form, passed all four browser consent tests, and
    received the same 89 because of the literal-only static assertion. Two
    independent routes now demonstrate that this is a systematic measurement
    blind spot for a valid implementation form rather than an isolated product
    failure.
15. GPT WBD-004 completed 18/18 at 100. Median total time increased
    88.6 → 121.3 seconds versus July, with measured increases in setup
    (4.0 → 6.5), worker (61.9 → 74.0), and grader (22.7 → 29.9). The first
    cell's setup alone rose to 28.7 seconds while later cells were lower, and
    live NFS reads also varied; storage/setup and browser-grader variance are
    confirmed covariates alongside worker service time.
16. Higher effort did not improve WBD-004 quality. For example, Terra/medium
    scored 100 in 76.6 seconds and 19,637 effective tokens, while Terra/xhigh
    scored the same 100 in 145.4 seconds and 54,838 tokens. Sol/medium was the
    fastest current GPT observation at 70.1 seconds; singletons remain
    insufficient for a stable service guarantee.
17. Claude Fable/low WBD-004 passed 100 but rose 112.8 → 218.6 seconds and
    19,483 → 102,144 effective tokens. Its trajectory contains nine tool calls
    versus six previously and two rejected `Edit` calls: shell inspection did
    not satisfy Claude's enforced requirement to `Read` the target before
    editing. The eventual edit passed after a `Read`. This is a confirmed
    safe-invocation workflow cost and motivates a separately labeled
    Read-before-Edit experiment after the frozen matrices.
18. Multiple Local probes blocked on the repository's hard NFS mount. More
    decisively, the active Claude Opus/max process was observed in kernel
    `nfs_wait` while its stream JSON was written directly to the NFS-backed
    artifact path. It later completed 100 in 236.5 seconds, of which 194.6 was
    counted as worker time. Current worker duration therefore includes proven
    storage blocking and cannot be interpreted as pure model/service latency.
    Future runner work should stage raw artifacts locally and copy them only
    after process completion; do not change the frozen runner mid-matrix.
19. Claude WBD-004 completed 15/15 at 100, making the combined task block
    33/33. Median total time rose 112.5 → 135.9 seconds and worker time
    63.2 → 88.6; grader time was nearly flat (30.2 → 31.2). Sonnet/low was
    fastest at 54.1 seconds, while Sonnet/xhigh took 338.6 seconds at the same
    score. Effective tokens rose 31,323 → 137,350 under the new fresh-input,
    no-session-persistence invocation and remain provider-internal only.

## Deviations

- `--allowedTools` is additive to existing Claude permission settings rather
  than an exclusive boundary. The driver discovered this empirically when a
  Bash denial probe using only `Read` still executed Bash. No benchmark cell
  had started on Claude at that point. The final policy therefore combines
  the reviewed allowlist with explicit high-risk `--disallowedTools` rules and
  the capsule's removed remotes/publish authority. This remains a behavioral,
  not OS-enforced, workspace boundary as the charter already records.
- The current grader SHA differs from the July GPT matrix only because the
  protected ledger filename changed from `tools/todo.md` to `TODO.md`; scoring
  code and task-definition hashes are unchanged. The current grader exactly
  matches the July Claude matrix. This administrative identity drift will be
  disclosed in the final comparison.
- The first 15-cell projection pessimistically applied GPT's WBD-001 slowdown
  to both providers and projected 04:49. After the full matched Claude block,
  separate provider scaling moved the estimate to 04:03. No concurrency was
  introduced because it would contaminate wall-time comparison.
