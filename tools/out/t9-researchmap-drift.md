# T-9 — researchmap drift check (report only)

Started 2026-07-12. The task permits the public API check only; no import or login UI action will be taken.

## Initial API attempt

- Command: `python3 tools/researchmap-export.py --check-live`
- Result: `ERROR: could not fetch live published_papers from researchmap API (URLError: <urlopen error [Errno -3] Temporary failure in name resolution>); aborting without writing /home/rioyokota/website/tools/out/researchmap-import.jsonl (refusing to treat an unreachable API as "everything is new")`
- No JSONL was created or changed, which is the script's safe failure behavior.

## Structured result

- status: in-progress
- summary: Standard-sandbox DNS prevented the public researchmap check; the exporter aborted safely before writing an import file.
- changed_files: tools/out/t9-researchmap-drift.md; tools/state/session.md
- commands: `python3 tools/researchmap-export.py --check-live` (one failed API fetch).
- verification: error confirms no `tools/out/researchmap-import.jsonl` was written.
- evidence:
  - confirmed: DNS failure occurred at the public researchmap API before any drift comparison.
  - hypotheses: none; no drift status can be inferred from an unreachable API.
- remaining: perform one approval-gated retry outside the sandbox, then summarize the resulting JSONL without importing it.

## Live result

- The approval-gated public API run completed and regenerated `tools/out/researchmap-import.jsonl` with 29 JSONL records.
- Proposed inserts by category: `published_papers` 2, `media_coverage` 13, `committee_memberships` 7, `research_projects` 7.
- Proposed updates: 0. Proposed deletes: 0.
- Notable examples: the 2016 performance-model journal paper and 2023 ICPP eigenvalue paper; 13 May–July 2023 media items; 2023 committee entries including IPDPS and PASC; and 2026–2030 / 2026–2029 research projects.
- The live comparison also reported 2 ambiguous existing research projects (the 2022–2026 two-phase-turbulence grant and 2022–2025 hierarchical-low-rank grant); neither was emitted as an import record.
- No import operation or researchmap login UI action was performed.

## Structured result

- status: awaiting-user
- summary: Drift exists: 29 proposed inserts, 0 updates, 0 deletes. The review JSONL is regenerated but deliberately not imported.
- changed_files: tools/out/researchmap-import.jsonl; tools/out/t9-researchmap-drift.md; tools/state/session.md; tools/todo.md (pending blocked-state update)
- commands: `python3 tools/researchmap-export.py --check-live` (standard sandbox DNS failure, followed by one user-approved elevated retry); local JSONL count/category inspection.
- verification: 29 non-empty JSONL lines; all records are `insert` proposals; category counts sum to 29; no update/delete record appears.
- evidence:
  - confirmed: public source collections fetched from https://api.researchmap.jp/rioyokota/{published_papers,books_etc,presentations,misc,awards,media_coverage,committee_memberships,research_projects}.
  - confirmed: the exporter reports 0 award inserts/1 match; 7 committee inserts/91 matches; 7 research-project inserts/13 matches/2 ambiguous.
  - confirmed: no import endpoint or login UI was used.
  - hypotheses: none; the proposed records require user review because importing is explicit-only.
- remaining: user decision required—review and, if desired, manually upload `tools/out/researchmap-import.jsonl` through researchmap Settings > Import. Do not rerun an import automatically.
