# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-166.

## Active

- **T-160 — Complete journal and book metadata:** resolve every applicable gap
  in sub001--sub003 (42 journals, two book-series items, two books), preserving
  verified identifiers and explicitly distinguishing unavailable/inapplicable
  fields from omissions.
- **T-161 — Complete international peer-reviewed metadata:** process all 115
  sub004 entries in bounded year batches, filling locally evidenced pages,
  locations, identifiers, and other supported fields without guessing.
- **T-162 — Complete domestic and non-reviewed metadata:** process 31 sub005,
  48 sub006, and 69 sub007 entries, preserving bilingual author metadata and
  filling applicable event/location/page/identifier fields.
- **T-163 — Normalize Achievements and add source links:** conform all seven
  sections to the majority no-leading-space/terminal-period/no-inline-anchor
  structure on both pages; add a separate `[arxiv] [bibtex]` row to the 30
  entries with verified arXiv records and keep exporter/CV text clean.
- **T-164 — Generate and audit ResearchMap import:** run the corrected live
  diff after metadata completion, review every insert/update/delete, emit the
  bulk-import JSONL without `user_id`, and retain exact source/audit evidence.
- **T-165 — Validate, publish, and verify:** run EN/JP/CRLF/CV/exporter/schema,
  standards, browser, security, deploy-preview, Git, live-page, and remote-
  commit gates; publish only the reviewed public changes and close the ledger.

## Blocked / awaiting user

None.

## Recently completed

- **T-159 — Align complete ResearchMap field schemas:** corrected Books
  DOI/ISBN identifiers, Presentation location/type, and profile field names;
  added balanced committee/project parsing plus category extraction; and made
  dates, localized values, identifiers, URLs, and language updates additive
  and non-degrading. Seven fixtures pass; the live dry-run has zero deletes and
  holds 22 ambiguous matches out of the import plan.
- **T-158 — Repair Achievements exporter parsing:** installed a shared
  id/legacy-name section parser for ResearchMap and ORCID, added link-row
  stripping and current/legacy-heading fixtures, and restored both 292-entry
  dry runs plus the sanctioned live comparison.
- **T-157 — Inventory ResearchMap and Achievements metadata:** exhaustively
  indexed 309 entries (292 export-eligible), every per-entry missing field and
  citation candidate, 283 live matches/five ambiguous/four unmatched records,
  EN/JP tag parity, sync omissions, and nine ordered work batches in JSON/MD.
- **T-156 — Move benchmark results to README bottom:** moved the complete
  GPT-5.6 benchmark section from near the top of `README.md` to the final
  section, with byte count and normalized section hash unchanged. Verified
  headings, links, policy, Markdown budgets, and security; push-only.
- **T-155 — Housekeeping and fresh-task reset:** fast-forwarded the declared
  workspace by 24 commits, passed repository/ledger/security/benchmark checks,
  restored four exact historical reports needed by log and metric pointers,
  removed about 1.3 GB of reproducible caches, and retained all 173 raw
  benchmark artifacts. Push-only; no website deployment ran.
- **T-154 — Publish benchmark comparison tables in README:** added a prominent
  root-README section with confidence-backed per-task dispatch routes and
  frozen singleton model/effort tables; linked the deterministic evidence and
  policy, corrected the benchmark README retention note, and verified every
  displayed figure against source JSON. Push-only; no website deploy ran.
- **T-153 — Close the eight-hour campaign:** completed the scheduled window
  with 173 reconciled results/artifacts/v2 metrics, deterministic summaries,
  policy/mutation/capsule audits, six driver metrics rows, durable facts and
  decisions, a final report, and tools-only pushes. No website publish ran.
- **T-152 — Install the evidence-backed dispatch policy:** installed and
  validated policy `2026-07-14.3`, a strict selector, task-class validation and
  fallback chains, and a delegation-workflow lookup. All 15 task/objective
  lookups pass; the selector verifies source hash/evidence/task coverage,
  reliability ordering, objective optimality, and route-aware fallbacks.
- **T-151 — Allocate adaptive matched repeats:** completed 83/83 adaptive rows
  in 17 checkpointed stages: 70 full-quality passes and 13 genuine capability
  failures. Final routes are Terra/low for WBD-001; Luna/low runtime and Sol/low
  tokens for WBD-002; Terra/low runtime and Sol/low tokens for WBD-003;
  Luna/low runtime and Sol/low tokens for WBD-004; and Sol/high for every
  WBD-005 objective. WBD-001--004 routes are 6/6 high-confidence; WBD-005
  Sol/high is 8/9 qualified and still requires full validation.
  If evidence is resumed, Sol/high is the only efficient first arm: two clean
  repeats reach 10/11 high-confidence; recompute immediately after a failure.
- **T-149 — Audit and summarize the complete matrix:** added deterministic
  JSON/Markdown analysis with exact cell/identity/artifact/metrics checks. Low
  was the only 15/15 full-quality effort and `ultra` was dominated on every
  task; monetary cost remains unknown, so effective tokens are the cost proxy.
- **T-148 — Complete the `ultra` rows:** completed all 15 ultra cells. Every
  cell passed score 100 with exact scope and P2P, but every ultra route is
  dominated by a documented-effort route.
- **T-147 — Run all documented model/effort/task cells:** completed the frozen
  75-cell grid with automatic switching and task-specific timeouts: 70
  capability passes and five genuine WBD-005 failures.
- **T-146 — Freeze, extend, and preflight the GPT-5.6 round:** froze all
  identities, restored dependencies, audited five capsules, and proved all
  three models accept `ultra`; paused before T-147 at the user's request.
- **T-150 — Expand the GPT-5.6 matrix:** replaced the finalist gate with all
  five WBD tasks across three models and six efforts (90 cells total).
- **T-145 — Plan GPT-5.6 benchmark matrix:** initial gated design; superseded
  by T-150 before paid work began.
- **T-141--T-144 — Remove obsolete comparison machinery and normalize:**
  removed the inactive project integration and retired comparison state,
  retained the reusable regression suite, and compacted current tooling state.

Historical Git commits remain intact; owner-scope settings were not changed.
