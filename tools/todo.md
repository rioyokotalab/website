# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-169.

## Active

None.

## Blocked / awaiting user

- **T-167 — Resolve held metadata cases:** in a new primary-source lookup batch,
  resolve the three quarantined citation conflicts and manually classify the
  29 ambiguous/cross-type matches without weakening additive safety guards.

## Recently completed

- **T-168 — Relocate benchmark artifacts and clear transient output:** moved
  all 173 referenced raw benchmark runs (1,102 files, 57 MB) byte-for-byte to
  the ignored benchmark-owned `tools/agent-benchmark/artifacts/` archive,
  updated producers and 519 stored path occurrences, passed artifact/capsule/
  metrics/security checks, and left `tools/out/` completely empty.
- **T-166 — Repair and re-import the ResearchMap JSONL:** diagnosed all 86
  bilingual-title validation errors, generated an exact minimal retry, and
  received user confirmation that the retry import succeeded. Recorded 379
  currently visible matched IDs without re-importing the lagging API residual,
  then removed all superseded import/error/retry artifacts and bytecode.
- **T-165 — Validate, publish, and verify:** passed offline/schema/security,
  38/38 browser, deploy-preview, live-byte, and exact-remote-commit gates;
  published both Achievements pages and denied public access to the preserved
  deployment sentinel. The live pages each contain 309 entries and 30 exact
  arXiv/BibTeX rows; final GitHub commit is `65dac52`.
- **T-164 — Generate and audit ResearchMap import:** generated the 318-line
  `tools/out/researchmap-import.jsonl` (19 inserts, 299 additive updates, zero
  deletes), held 29 ambiguous/cross-type matches out, and independently
  rebuilt and schema-checked every operation against the public API. No live
  value is replaced or removed; `user_id` and visible link labels are absent;
  managed-ID state remains unchanged pending a confirmed manual upload.
- **T-163 — Normalize Achievements and add source links:** normalized all 309
  mirrored citations to the majority no-leading-space/terminal-period/plain-
  citation format and added 30 separate `[arxiv] [bibtex]` rows per language
  from existing arXiv attributes. The updater is idempotent, CRLF is intact,
  and exporter citation text remains semantically unchanged.
- **T-162 — Complete domestic and non-reviewed metadata:** audited all 31
  sub005, 48 sub006, and 69 sub007 rows; installed three explicit title guards
  and the locally stated sub007 report volume/number. Every other nominal
  volume/page/location/identifier gap is documented as absent or structurally
  inapplicable rather than guessed.
- **T-161 — Complete international peer-reviewed metadata:** audited all 115
  sub004 rows; added the three locally stated proceeding volume/number values
  and two explicit title guards. Unstated issue/page/identifier gaps remain
  classified, and three citation conflicts are quarantined for a later lookup
  session.
- **T-160 — Complete journal and book metadata:** added 31 citation-evidenced
  journal/series attributes, bilingualized four Japanese author rows, and
  modeled four books with title, contributor range/role, assigned pages,
  publisher, date, identifiers, language, and referee fields. Unavailable and
  inapplicable gaps are explicitly recorded in the local metadata plan.
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
Historical Git commits remain intact; owner-scope settings were not changed.
