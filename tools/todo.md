# Lab website — task board (ledger)

Protocol + schemas: skills/context-ledger.md. In-flight detail:
tools/state/session.md. Next free id: T-10.

## Active
### T-6 — Add missing data-doi attributes to recent achievements
Outcome: in jp/achievements/index.html, find <li> entries with
data-date >= 2024-01 that lack data-doi (skills/achievements.md for
section semantics). Resolve up to 4 DOIs via Crossref/DBLP per
skills/web-lookup.md (record source URLs; independently confirm metadata
matches the citation text). Add data-doi to the SAME entries in BOTH
en/ and jp/ pages — attribute-only, no visible text changes. Page HTML
is CRLF with legacy uppercase tags: edit via python per
skills/html-editing.md, never sed/Edit on raw lines.
Verify: en/jp grep counts for the touched entries identical; curl -s -o
/dev/null -w '%{http_code}' localhost:8000/jp/achievements/index.html
returns 200; each added DOI resolves 30x at doi.org. If NO qualifying
entries exist, record a clean verdict and close. Size M-L. Leave commits
to Claude/user.

### T-7 — Reconcile cv.tex with recent achievements
Outcome: compare achievements entries dated 2025-01 or newer against
cv/cv.tex (sync is bidirectional with achievements/index.html and the CV
sections of jp/member/yokota.html — see CLAUDE.md content conventions +
skills/exporters.md). Add any missing entries to cv.tex following its
existing entry format exactly, and mirror the same additions to the
jp/member/yokota.html CV section if it lists them. Do NOT run
./cv/build-cv.sh (explicit-only).
Verify: list each added entry with its source achievements line; grep
counts before/after; no build attempted. If already in sync, record the
clean verdict with evidence. Size M-L.

### T-8 — Computers-page status of the 8-GPU RTX 6000 Ada node
Outcome: using READ-ONLY cluster queries only (sinfo, scontrol show
node) — NEVER submit jobs (no yrun/ybatch/srun) — determine whether the
8-GPU RTX 6000 Ada node (CPU shown as "-" in the computers pages) is
back up. If still down: update the dated note in tools/state/facts.md
and close. If up: scontrol does not reveal the CPU model — do NOT guess
and do NOT edit the pages; park this task as Blocked / awaiting user
with the exact probe request for site-checker/user. Never guess
hardware facts (CLAUDE.md).
Verify: raw sinfo/scontrol output quoted in the driver report. Size M.

### T-9 — researchmap drift check (report only, NO import)
Outcome: run python3 tools/researchmap-export.py --check-live
(skills/exporters.md). Mirroring is EXPLICIT-ONLY: never import, never
touch the researchmap login UI. Summarize the drift (counts of
adds/updates by category, notable examples) in the driver report and
park the decision as Blocked / awaiting user if any drift exists;
otherwise record clean and close.
Verify: tools/out/researchmap-import.jsonl regenerated; drift counts
quoted. Size M.

## Blocked / awaiting user
(none)

## Recently completed (history lives in git)
- 2026-07-12 T-3 deploy.sh excludes .agents/ and .codex/; user-side dry-run confirmed 0 matching paths.
- 2026-07-12 T-5 verified the two newest DOI-bearing achievements; both PASS with resolver and Crossref evidence in tools/out/doi-spotcheck.md; no page edits (uncommitted).
- 2026-07-12 T-4 documented HTML-path vs shared-asset EN/JP parity and recorded the 19/114-file, 0-broken-link audit; markdown size check passes (uncommitted).
- 2026-07-12 T-2 fixed the malformed publish-and-verify.md table row in skills/README.md; confirmed no other row lacks a leading pipe (uncommitted).
- 2026-07-12 T-1 applied: CLAUDE.md/AGENTS.md context-ledger versions + pre-commit hook installed by user.
- 2026-07-12 Context-ledger scheme built: skills/context-ledger.md,
tools/state/{session,facts,decisions}.md, tools/check-md-size.py,
dispatch-contract ledger pointers, README index; CLAUDE.md/AGENTS.md
proposals pending (T-1).
- 2026-07-12 Codex network access enabled
  (sandbox_workspace_write.network_access=true, codex-cli 0.144.1);
  CLAUDE.md + skills/web-lookup.md updated.
- 2026-07-12 Cat 5 grant-ID extraction -> researchmap research_projects:
  10/22 projects populated, 21 papers; fetch_live guard bug fixed; 41
  PDFs archived in tools/papers/. Leftover fact (7 unfilled rows) ->
  tools/state/facts.md.
- RM<->website consolidation Cat 1-4 published (80a0de8); media_coverage
  exporter (d543652); latency pins (56669c5).
