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
