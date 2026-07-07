# ResearchMap metadata attributes — persistent project todo

Goal: enrich every Achievements `<li>` with the metadata ResearchMap needs, stored
as invisible `data-*` attributes on the `<li>` (rendered page unchanged). Done
one FIELD at a time, each field rolled across sections sub001..sub007, so each
step is small and independently verifiable. This file is the source of truth for
progress across sessions — read it first, update + commit it after each step.

Rules live in CLAUDE.md: the `data-date` convention + no-year-only derivation
rule (Content conventions), and the failure-driven workflow rules (Delegation to
subagents). Section entry counts (en, 2026-07-08): sub001=42, sub002=2, sub003=2,
sub004=115, sub005=32, sub006=45, sub007=79. EN and JP citations are identical for
international entries, so each attribute is written to BOTH language files.

## Legend
- [x] done & live   - [~] in progress   - [ ] not started

## Per-field workflow (repeat for every field)
1. Derive values — site-author, SMALL batches (<=3-4 entries), authorize hosts
   (Crossref/DBLP/Semantic Scholar/J-STAGE/DOI resolvers), append each result to
   a tools/out/ file IMMEDIATELY (survives mid-run cutoff).
2. Write attribute to BOTH en+jp — site-editor, give unique title substring +
   value per entry, CRLF-safe python3 script; stop if any substring is non-unique.
3. Verify — site-checker: localhost 200 + EN/JP parity (counts & values).
4. User previews at http://localhost:8000/jp/achievements/index.html, approves.
5. Publish — site-publisher runs publish.sh; expect the publickey push to fail,
   then site-editor recovers the push via the /tmp/ssh-* socket. Verify live.
6. Update tools/researchmap-export.py (and orcid-export.py) to PREFER the new
   attribute over heuristic parsing when present.
7. Tick the boxes below, commit+push this file.

## Field order & progress

### Field 1 — data-date (publication_date; REQUIRED)
- [x] sub001 journal (42) — live 2026-07-08, commit 517df17 (4 Jan placeholders: TSIPN, TMLR, 2x JSCES)
- [ ] sub002 book series (2)
- [ ] sub003 books (2)
- [x] sub004 intl peer-reviewed (115) — conferences: first day of conference
- [ ] sub005 domestic peer-reviewed (32)
- [ ] sub006 intl non-reviewed (45)
- [ ] sub007 domestic non-reviewed (79)
- [ ] exporter prefers data-date over heuristic date parsing

### Field 2 — data-doi
- [ ] sub001  - [ ] sub002  - [ ] sub003  - [ ] sub004  - [ ] sub005  - [ ] sub006  - [ ] sub007
- [ ] exporter emits doi from data-doi

### Field 3 — data-volume / data-number / data-pages (journals & proceedings)
- [ ] sub001  - [ ] sub004  - [ ] sub005 (others N/A)
- [ ] exporter emits volume/number/starting_page/ending_page

### Field 4 — data-authors (normalized; later ja/en split)
- [ ] sub001  - [ ] sub002  - [ ] sub003  - [ ] sub004  - [ ] sub005  - [ ] sub006  - [ ] sub007
- [ ] exporter emits authors from data-authors

### Field 5 — books/presentations extras
- [ ] data-isbn / data-publisher for sub002, sub003
- [ ] data-event / data-location (+ data-invited) for sub006, sub007
- [ ] exporter emits these

## Notes
- Values that cannot be confirmed follow the no-year-only style rule per field
  (dates -> `-01` placeholder). Prefer fixing the source citation over guessing.
- Keep this file and CLAUDE.md in sync when the plan changes.
