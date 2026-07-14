# Current facts

- **GPT-5.6 campaign identity:** matrix label `gpt56-full-20260713`, repeat
  label `gpt56-repeat-20260714`, frozen baseline `c4b0720`, full prompt,
  default inspection, runner-lite, P2P, automatic model/effort switching, and
  task-specific timeouts. The final repeat plan SHA-256 is
  `266d2d782a422f43e76056b6d69eea0b3d57623fb8fbfce12fe85ce2632f0137`.
- **Complete evidence:** 90/90 matrix cells and 83/83 adaptive rows are
  complete. Combined evidence is 173 unique runs, 155 capability passes, and
  154 full-quality passes. All 173 result rows, artifact directories, and v2
  metric pointers reconcile; repeat stages have zero pending cells.
- **Runtime/tokens:** the campaign accumulated 20,645,537 ms end-to-end and
  4,824,076 effective tokens. Monetary cost is unknown because no price table
  or billed-cost field was frozen. No worker timed out; worker maxima for
  WBD-001--005 were 164, 206, 105, 108, and 326 seconds.
- **Final route evidence:** WBD-001 Terra/low is 6/6 high-confidence. WBD-002
  Luna/low and Sol/low, WBD-003 Terra/low and Sol/low, and WBD-004 Luna/low and
  Sol/low are each 6/6 high-confidence. WBD-005 Sol/high is 8/9 qualified with
  Wilson-95 lower bound 0.565 and expected 249,071 ms / 45,053 effective tokens
  per full-quality success.
- **Objective routes:** runtime/reliability select Terra/low for WBD-001,
  Luna/low for WBD-002, Terra/low for WBD-003, Luna/low for WBD-004, and
  Sol/high for WBD-005. Effective-token routing changes WBD-002--004 to
  Sol/low; WBD-001 and WBD-005 are unchanged.
- **Policy:** `tools/agent-benchmark/routing-policy.json` version
  `2026-07-14.3` is pinned to deterministic summary SHA-256
  `0ecc265620f3c77ab7f2ce410722d3a49213b71a1a0b2628a307a192e835c170`.
  Its selector validates exact task coverage, all 12 retained evidence routes,
  objective ordering, colocated source identity, and route-aware fallbacks.
- **Cautions:** low effort was the only 15/15 full-quality singleton effort;
  `ultra` was dominated on every task. WBD-005 had 18 non-full-quality cells,
  including 13 `js-reduced-zero` and five `css-zero-motion` assertion failures
  (with overlap), so its full static/browser grader remains mandatory. Evidence
  generalizes only to materially analogous capability classes.
- **T-167 completion (2026-07-14):** a fresh live rebuild and independent audit
  validate 251 operations (25 inserts, 226 additive updates), zero deletes,
  zero unresolved ambiguities, and 29 reviewed classifications. Five explicit
  holds remain operation-free. The JSONL SHA-256 is
  `a76493bcd32f5233d40c66d5d6a846a795c953a05f617e8c52b469ffc8f37f16`;
  managed-ID state is unchanged. Website commit `fd2f2d8` and both deployed
  Achievements pages were independently verified.
- **ResearchMap T-177 completion (2026-07-14):** the user confirmed the
  16-operation repair imported successfully after six reported conflicts and
  two silent similarity merges were corrected. The public API now exposes all
  eight forced records as IDs `54390630`--`54390637`; the managed registry
  records 411 visible IDs (172 papers, four books, 44 presentations, 60 misc,
  one award, 13 media items, 98 committee memberships, and 19 projects). A
  five-insert post-import residual was treated as lag/unresolved absence and
  deleted without upload, together with all transient ResearchMap artifacts.
