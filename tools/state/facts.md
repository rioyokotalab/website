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
- **Global harness discovery (2026-07-14):** isolated Codex and Claude probes
  both loaded the shared `# Global agent working agreements` heading and chose
  `long-running-task-ledger` for durable multi-session work. Six shared skills
  are linked into `~/.codex/skills/`, `$HOME/.agents/skills/`, and
  `~/.claude/skills/`; repository-specific instructions still layer locally.
- **T-167 provider status (2026-07-14):** the fresh `--sync --dry-run` retry
  again ended before retrieval when ResearchMap closed the `published_papers`
  connection. The exporter returned 1 and wrote no import or state changes.
- **Portable global harness (2026-07-14):** `~/harness` preserves the original
  Git history from commit `7f969317c4b597b9adaae629c05cf6723785aff2` and
  contains shared global guidance, six validated personal skills, reviewed
  Codex rules, non-secret config examples, and a fail-closed installer. Live
  Codex, Claude, and user-skill discovery paths are symlinks to it. Its
  requested GitHub repository is configured as `origin`; its exact transport
  may be machine-local.
- **Codex shell-snapshot diagnosis (2026-07-14):** CLI 0.144.3 serialized four
  system Bash-completion functions whose extglob patterns fail its default
  snapshot parser. Restricting `/usr/share/bash-completion/bash_completion` to
  interactive shells preserved other startup behavior and produced a clean
  default ephemeral probe with correct global instruction discovery. The
  separate arg0 warning came from accumulated/racing temp directories.
- **Harness remote status (2026-07-14):** local and remote `main` both resolve
  to `0bd31d1dc4f2ac923e276e81de5b4e3e2b7a1528`, tracking is established, and
  divergence is zero. The successful retry used the externally configured
  `github:rioyokotalab/harness` SSH alias and did not force-push.
