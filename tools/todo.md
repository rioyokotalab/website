# Lab website — task board (ledger)

Protocol + schemas: skills/context-ledger.md. In-flight detail:
tools/state/session.md. Next free id: T-6.

## Active
### T-2 — Fix malformed table row in skills/README.md
Outcome: the row starting `publish-and-verify.md |` gets its missing
leading pipe so it reads `| publish-and-verify.md | ... |`. Confirm no
other row lacks a leading pipe.
Verify: grep -n '^| publish-and-verify' skills/README.md. Size S. Leave
the commit to Claude/user.

### T-3 — Deploy-exclude .agents/ and .codex/
Outcome: deploy.sh exclusion list also excludes repo-root .agents/ and
.codex/ (repo-internal agent config; currently they would mirror
publicly). Do NOT touch .dont-remove-me handling (intentionally
preserved). NEVER run deploy.sh/publish.sh (AGENTS.md hard rule) —
static verification only.
Verify: grep the new exclusion patterns in deploy.sh; then ask the user
to run ./deploy.sh --dry-run and confirm no .agents/.codex lines. Size S.

### T-4 — Document EN/JP parity scope (pages vs assets)
Outcome: skills/en-jp-parity.md states that parity applies to HTML
pages/paths while image assets live only under jp/ (e.g.
jp/research/images20XX/, jp/picture/images/) and are referenced
cross-language; include a repeatable audit command (compare sorted
`find en -type f` vs `find jp -type f`; expected EN-only: none, JP-only:
assets). Add one dated bullet to tools/state/facts.md Site section:
2026-07-12 audit found en=19 vs jp=114 files, 0 broken links across 16
index pages.
Verify: python3 tools/check-md-size.py passes; grep the new wording.
Size M.

### T-5 — DOI spot-check (network) for 2 newest achievements
Outcome: take the 2 newest data-doi values in jp/achievements/index.html;
per skills/web-lookup.md verify each resolves via https://doi.org (HTTP
200/30x); record verdicts + source URLs in tools/out/doi-spotcheck.md
ending with the structured result block (skills/codex-dispatch.md). No
page edits: if one fails, record it under Awaiting user in
tools/state/session.md.
Verify: tools/out/doi-spotcheck.md exists with 2 verdicts. Size M.

## Blocked / awaiting user
(none)

## Recently completed (history lives in git)
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
