# T-6 — recent achievement DOI attributes

Started 2026-07-12 by the codex driver.

## Inventory

- Parsed both achievements files with case-insensitive `<li>` handling and CRLF-preserving reads.
- Each file has 49 entries dated 2024-01 or later without `data-doi`; the qualifying sequences match exactly between EN and JP.
- Distribution: `sub004` 33 (22 already have `data-url`), `sub005` 5 (3 `data-url`), `sub006` 1 (1 `data-url`), `sub007` 10 (4 `data-url`). No qualifying entry appears in `sub001`–`sub003`.
- The first two lookup items are the likely publisher-proceedings records rather than workshop/preprint or domestic-event entries:
  1. Chen Zhuang et al., “Scaling Large-scale GNN Training to Thousands of Processors on CPU-based Supercomputers,” ICS 2025.
  2. Thomas Spendlhofer et al., “On the Interplay Between Precision, Rank, Admissibility, and Iterative Refinement for Hierarchical Low-Rank Matrix Solvers,” ISC High Performance 2025.

## Structured result

- status: in-progress
- summary: Inventory complete; two bounded DOI candidates selected for Crossref plus independent publisher confirmation.
- changed_files: tools/out/t6-doi-attributes.md
- commands: CRLF-safe Python inventory/comparison; targeted `rg` citation inspection.
- verification: EN/JP qualifying sequence equality confirmed (49 each).
- evidence:
  - confirmed: The two selected citations occur in `sub004` with matching EN/JP markup and no existing `data-doi`.
  - hypotheses: Both selected peer-reviewed conference proceedings may have publisher-assigned DOIs; no DOI is recorded until Crossref and an independent source agree on title, authors, and year.
- remaining: resolve up to two selected lookup items, make only verified paired attribute edits, then run scoped parity and HTTP/resolver checks.

## Lookup item 1 — Crossref attempt

- Citation: Chen Zhuang et al., “Scaling Large-scale GNN Training to Thousands of Processors on CPU-based Supercomputers,” ICS 2025.
- Source URL: https://api.crossref.org/works?query.title=Scaling%20Large-scale%20GNN%20Training%20to%20Thousands%20of%20Processors%20on%20CPU-based%20Supercomputers
- Result: Crossref was unavailable in this session: `curl: (6) Could not resolve host: api.crossref.org`.
- Per `skills/web-lookup.md`, Crossref will not be retried in this session. No DOI has been inferred or added.

## Structured result

- status: in-progress
- summary: Inventory complete; the first Crossref lookup was blocked by DNS before any metadata was received.
- changed_files: tools/out/t6-doi-attributes.md
- commands: CRLF-safe Python inventory/comparison; targeted `rg` citation inspection; one Crossref `curl` request.
- verification: EN/JP qualifying sequence equality confirmed (49 each); Crossref failure captured verbatim.
- evidence:
  - confirmed: The selected ICS citation occurs in matching `sub004` entries without `data-doi`.
  - hypotheses: Its DOI remains unconfirmed. A different structured provider or publisher record may be checked without retrying Crossref.
- remaining: attempt the selected items through a non-Crossref source; make only a paired edit if independent metadata confirmation is available.

## Lookup item 1 — Crossref result

- Citation: Chen Zhuang et al., “Scaling Large-scale GNN Training to Thousands of Processors on CPU-based Supercomputers,” ICS 2025.
- Structured source: https://api.crossref.org/works?query.title=Scaling%20Large-scale%20GNN%20Training%20to%20Thousands%20of%20Processors%20on%20CPU-based%20Supercomputers&rows=5
- Crossref top result: DOI `10.1145/3721145.3730422`; title exactly matches; all 11 site authors match in order; publisher ACM; container *Proceedings of the 39th ACM International Conference on Supercomputing*; published-print 2025-06-08; pages 57–72.
- Independent publisher-page attempt: https://dl.acm.org/doi/10.1145/3721145.3730422 returned HTTP 403 in this session, so it cannot yet serve as the independent confirmation.
- Resolver candidate: https://doi.org/10.1145/3721145.3730422

## Structured result

- status: in-progress
- summary: Crossref resolves lookup item 1 to `10.1145/3721145.3730422`, but a separate metadata source is still required before an edit.
- changed_files: tools/out/t6-doi-attributes.md
- commands: CRLF-safe Python inventory/comparison; targeted `rg` citation inspection; Crossref `curl` (sandbox DNS failure, then user-approved elevated retry); ACM publisher-page browser request.
- verification: EN/JP qualifying sequence equality confirmed (49 each); Crossref title/authors/year agree with the site citation; ACM source was unavailable (403).
- evidence:
  - confirmed: Crossref's exact title, 11-author sequence, and 2025 publication metadata identify the ICS entry as DOI `10.1145/3721145.3730422`.
  - hypotheses: The DOI is not yet independently verified because ACM denied the metadata request; no page edit has been made.
- remaining: obtain an independent non-ACM metadata confirmation for item 1 or leave it unedited; then evaluate one more bounded lookup item.

## Lookup item 1 — DBLP attempt

- Structured source URL: https://dblp.org/search/publ/api?q=Scaling%20Large-scale%20GNN%20Training%20to%20Thousands%20of%20Processors%20on%20CPU-based%20Supercomputers&format=json&h=5
- Initial sandbox result: `curl: (6) Could not resolve host: dblp.org`.
- This is the first DBLP attempt; an approval-gated retry is being used only to distinguish the sandbox DNS restriction from provider unavailability. No ordinary DBLP retry will follow.

## Structured result

- status: in-progress
- summary: Item 1 has a Crossref DOI candidate; both independent-source routes are currently blocked in the standard sandbox (ACM 403; DBLP DNS).
- changed_files: tools/out/t6-doi-attributes.md
- commands: CRLF-safe Python inventory/comparison; targeted `rg` citation inspection; Crossref `curl` (sandbox DNS failure, then user-approved elevated retry); ACM publisher-page browser request; initial DBLP `curl`.
- verification: EN/JP qualifying sequence equality confirmed (49 each); Crossref title/authors/year agree with the site citation.
- evidence:
  - confirmed: Crossref identifies `10.1145/3721145.3730422` for the first citation.
  - hypotheses: Independent confirmation is pending and no page edit has been made.
- remaining: complete the single approval-gated DBLP retry for item 1, then either verify or leave it untouched before considering item 2.

## Lookup item 1 — DBLP result

- Independent structured source: https://dblp.org/rec/conf/ics/ZhuangZWCHLYDEM25
- DBLP record `conf/ics/ZhuangZWCHLYDEM25` confirms the exact title; all 11 authors in the site order; venue ICS; year 2025; pages 57–72; and DOI `10.1145/3721145.3730422`.
- The DBLP result independently agrees with Crossref on title, author list, year, pages, and DOI. The paired site entries are therefore eligible for an attribute-only edit.

## Structured result

- status: in-progress
- summary: Lookup item 1 is independently confirmed as DOI `10.1145/3721145.3730422`; the paired HTML edit is ready.
- changed_files: tools/out/t6-doi-attributes.md
- commands: CRLF-safe Python inventory/comparison; targeted `rg` citation inspection; Crossref `curl` (sandbox DNS failure, then user-approved elevated retry); ACM publisher-page browser request; DBLP `curl` (sandbox DNS failure, then user-approved elevated retry).
- verification: EN/JP qualifying sequence equality confirmed (49 each); Crossref and DBLP agree on the title, 11 authors, year 2025, pages 57–72, and DOI.
- evidence:
  - confirmed: `10.1145/3721145.3730422` is a same-paper match for the selected ICS 2025 citation.
  - hypotheses: The second selected candidate has not been queried yet.
- remaining: add the verified attribute to matching EN/JP entries with a CRLF-safe script; run scoped checks; optionally use the remaining lookup slot for the ISC 2025 candidate.

## Edit and verification — lookup item 1

- Applied with `tools/out/apply-t6-doi.py`, which opens each page with `newline=''`, requires exactly one author/date match, rejects a pre-existing DOI, and changes only the opening `<li>` tag.
- Changed each matching `sub004` tag to include `data-doi="10.1145/3721145.3730422"`; no visible citation text changed.
- Scoped parity: one matching DOI-bearing `<li>` in EN and one in JP; both files retain CRLF-only line endings (`bare_lf=0`).
- Local check: `curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/jp/achievements/index.html` returned `200`.
- Resolver check: `https://doi.org/10.1145/3721145.3730422` returned `302` to `https://dl.acm.org/doi/10.1145/3721145.3730422`.
- Diff review: exactly one attribute-only line modification in each achievements page. `git diff --check` reports the conventional CRLF carriage return as trailing whitespace on those changed CRLF lines; the CRLF-preservation check above is clean.

## Structured result

- status: in-progress
- summary: Added and verified one paired DOI attribute: the ICS 2025 entry now carries `10.1145/3721145.3730422` in both language pages.
- changed_files: en/achievements/index.html; jp/achievements/index.html; tools/out/t6-doi-attributes.md; tools/out/apply-t6-doi.py; tools/state/session.md
- commands: CRLF-safe Python inventory/comparison and edit script; targeted `rg`; Crossref and DBLP public API requests; local HTTP request; DOI resolver header check; `git diff` inspection.
- verification: EN/JP target count 1/1; no bare LF introduced; local JP achievement page HTTP 200; DOI resolver HTTP 302 to the ACM record; diff limited to the two data-doi additions.
- evidence:
  - confirmed: Crossref and DBLP independently agree that the matched citation's DOI is `10.1145/3721145.3730422`.
  - hypotheses: The remaining ISC 2025 candidate may have a DOI but has not been queried.
- remaining: use the second and final session lookup item for the ISC 2025 candidate, or close after this bounded verified addition.

## Lookup item 2 — Crossref result

- Site citation: Thomas Spendlhofer, Qianxiang Ma, Yasuhiro Matsumoto, Rio Yokota, “On the Interplay Between Precision, Rank, Admissibility, and Iterative Refinement for Hierarchical Low-Rank Matrix Solvers,” ISC High Performance, June 2025.
- Structured source: https://api.crossref.org/works?query.title=On%20the%20Interplay%20Between%20Precision%2C%20Rank%2C%20Admissibility%2C%20and%20Iterative%20Refinement%20for%20Hierarchical%20Low-Rank%20Matrix%20Solvers&rows=5
- Crossref top result: DOI `10.23919/isc.2025.11017731`; same four authors and 2025 ISC High Performance record, pages 1–12; however, its title is “On the Interplay Between Precision, Rank and Admissibility for Iterative Hierarchical Low-Rank Matrix Solvers.”
- The title differs materially from the site citation (not merely punctuation), so the same-paper gate is not met. No DOI will be added unless an independent record resolves the discrepancy.

## Structured result

- status: in-progress
- summary: One DOI is added and verified. The second candidate's Crossref record matches authors/year/venue but not the displayed title, so it is currently ineligible for a data-doi edit.
- changed_files: en/achievements/index.html; jp/achievements/index.html; tools/out/t6-doi-attributes.md; tools/out/apply-t6-doi.py; tools/state/session.md
- commands: CRLF-safe Python inventory/comparison and edit script; targeted `rg`; Crossref and DBLP public API requests; local HTTP request; DOI resolver header check; `git diff` inspection.
- verification: First DOI: EN/JP target count 1/1, local JP HTTP 200, resolver HTTP 302. Second DOI candidate: Crossref reports a material title mismatch.
- evidence:
  - confirmed: `10.1145/3721145.3730422` is independently verified and added to the paired ICS entry.
  - hypotheses: `10.23919/isc.2025.11017731` may refer to a revised or differently titled version, but it cannot be attached without an exact title match.
- remaining: use DBLP (the independent source) to confirm or rule out the ISC title discrepancy; then close T-6 with only safe edits.

## Lookup item 2 — DBLP result and decision

- Independent structured source query: https://dblp.org/search/publ/api?q=On%20the%20Interplay%20Between%20Precision%20Rank%20Admissibility%20Iterative%20Refinement%20Hierarchical%20Low-Rank%20Matrix%20Solvers&format=json&h=5
- DBLP returned zero records for the site-title query. It does not independently resolve the title difference or establish a same-paper match.
- Decision: leave `10.23919/isc.2025.11017731` off the site. The task permits attribute-only edits, so correcting the citation title is out of scope; attaching the DOI despite the mismatch would violate the title/authors/year confirmation gate.

## Structured result

- status: completed
- summary: Added one independently verified DOI attribute to the paired ICS 2025 achievement entry. Left the ISC 2025 candidate unchanged because Crossref's title differs materially and DBLP could not confirm it.
- changed_files: en/achievements/index.html; jp/achievements/index.html; tools/out/t6-doi-attributes.md; tools/out/apply-t6-doi.py; tools/state/session.md
- commands: CRLF-safe Python inventory/comparison and edit script; targeted `rg`; Crossref and DBLP public API requests; local HTTP request; DOI resolver header check; `git diff` inspection.
- verification: EN/JP qualifying sequence was 49/49 before the edit; added DOI target count is 1/1; no bare LF introduced; local JP achievements page is HTTP 200; DOI resolver returns HTTP 302 to the ACM record; page diff contains only the paired attributes.
- evidence:
  - confirmed: Crossref and DBLP agree that Chen Zhuang et al., ICS 2025, is DOI `10.1145/3721145.3730422` (same title, 11 authors, year, and pages).
  - confirmed: The resolver URL is https://doi.org/10.1145/3721145.3730422 and redirects to the ACM record.
  - confirmed: Crossref's ISC record is DOI `10.23919/isc.2025.11017731`, but its title is materially different; DBLP found no record for the site's title query.
  - hypotheses: The ISC mismatch may reflect a revised title, but no claim or edit relies on that possibility.
- remaining: none for T-6; any future title reconciliation should be a separately scoped content correction before adding the ISC DOI.
