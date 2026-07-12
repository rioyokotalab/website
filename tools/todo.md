# Lab website — task board (ledger)

Protocol + schemas: skills/context-ledger.md. In-flight detail:
tools/state/session.md. Next free id: T-6.

## Active
(none)

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
