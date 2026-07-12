# Lab website — task board (ledger)

Protocol + schemas: skills/context-ledger.md. In-flight detail:
tools/state/session.md. Next free id: T-14.

## Round 2 rules (drivers read first)

- Work ONLY tasks T-10 through T-13 plus optional proposals. NO publish/deploy this round. Explicit approvals (publish, researchmap/ORCID) are NEVER assumed.
- Drivers MAY append proposals under `## Proposed (round 2)`: id `P-<short-slug>`, 2–4 lines each covering goal, scope, first step, and why valuable. The judge triages winners' proposals into real T-ids. Proposal quality is scored.
- Put evidence and deliverables under `tools/out/t1X-*`; follow `skills/context-ledger.md` ledger discipline. Commit bookkeeping files silently with other work.

## Active

### T-10 — update the repo README
Update (or create if missing) root `README.md` to reflect current reality: a
hand-built static EN/JP site with frozen public tree, `skills/` playbooks,
`tools/` ledger+exporters+metrics, agent/codex delegation, and publish workflow.
MUST verify `deploy.sh` exclusion status so README is NOT deployed publicly and
record evidence. Keep it accurate against `CLAUDE.md`/`AGENTS.md` without
duplicating them wholesale. Evidence: `tools/out/t10-readme.md`.

### T-11 — minimize approvals as much as possible (no limits)
Owner directive (2026-07-12): this is a public-information lab website; any
breakage is trivially revertible from a prior git revision, so the benefit of
eliminating approval friction outweighs the risk — there are NO preserved hard
limits this round. Audit every source of approval friction (PreToolUse hooks,
`.claude/settings*.json`, codex sandbox/approval-policy, the
`.claude/config-edit-approved` gate, hand-edit-only blocks) and deliver
`tools/out/t11-permissions.md` proposing the MINIMUM-approval configuration
achievable — aim for zero interactive approvals — with EXACT apply commands per
`skills/config-proposals.md`. You MAY propose removing or loosening the
accidental-edit blocks and hand-edit-only gates; nothing is off-limits. Note
that publish still runs only when the user asks (workflow fact, not a block).

### T-12 — add Google Analytics (GA4) to the website
Add `gtag.js` to EVERY public HTML page (`en/` AND `jp/`) and keep
`Templates/*.dwt` in sync per `skills/html-editing.md`. Use placeholder ID
`G-XXXXXXXXXX`; record blocked-on-user for the real ID; do NOT publish. Verify
EN/JP insertion-count parity per `skills/en-jp-parity.md` and localhost
rendering. Briefly note privacy/consent considerations in `tools/out/t12-ga.md`.

### T-13 — propose a completely new web design
Proposal ONLY: no `en/` or `jp/` page edits. Deliver
`tools/out/t13-redesign/proposal.md` plus an optional self-contained prototype
under `tools/out/t13-redesign/` only (deploy-excluded). Respect the frozen URL
tree: restyle in place, move no pages. Cover `style.css` strategy,
mobile/accessibility, migration plan, and effort estimate.

## Proposed (round 2)

(empty — drivers append here)

## Blocked / awaiting user

(none — T-9 cleared per user instruction 2026-07-12 without an upload decision;
reviewed JSONL retained at `tools/out/researchmap-import.jsonl`)

## Recently completed (history lives in git)

- 2026-07-12 Round-1 4-way eval judged: terra > sol > fable > opus; terra merged (4a15349); tips tagged eval/r1-*; board cleared for round 2.
- 2026-07-12 T-8 confirmed rtx6000-ada is still DOWN+NOT_RESPONDING with 8 configured GPUs; facts.md refreshed, no page edit or job submission; raw Slurm evidence: tools/out/t8-cluster-status.md.
- 2026-07-12 T-7 added the missing 2025-06 CoRR presentation to cv/cv.tex (45 -> 46 presentation items); personal page has no publication section to mirror; no build run; evidence: tools/out/t7-cv-reconciliation.md.
- 2026-07-12 T-6 added `10.1145/3721145.3730422` to the paired ICS 2025 entry after Crossref+DBLP confirmation; scoped EN/JP, local HTTP, and resolver checks pass. ISC candidate left unedited for material title mismatch; evidence: tools/out/t6-doi-attributes.md.
- 2026-07-12 T-3 deploy.sh excludes .agents/ and .codex/; user-side dry-run confirmed 0 matching paths.
- 2026-07-12 T-5 verified the two newest DOI-bearing achievements; both PASS with resolver and Crossref evidence in tools/out/doi-spotcheck.md; no page edits (uncommitted).
- 2026-07-12 T-4 documented HTML-path vs shared-asset EN/JP parity and recorded the 19/114-file, 0-broken-link audit; markdown size check passes (uncommitted).
- 2026-07-12 T-2 fixed the malformed publish-and-verify.md table row in skills/README.md; confirmed no other row lacks a leading pipe (uncommitted).
- 2026-07-12 T-1 applied: CLAUDE.md/AGENTS.md context-ledger versions + pre-commit hook installed by user.
- 2026-07-12 Context-ledger scheme built: skills/context-ledger.md, tools/state/{session,facts,decisions}.md, tools/check-md-size.py, dispatch-contract ledger pointers, README index; CLAUDE.md/AGENTS.md proposals pending (T-1).
- 2026-07-12 Codex network access enabled (sandbox_workspace_write.network_access=true, codex-cli 0.144.1); CLAUDE.md + skills/web-lookup.md updated.
- 2026-07-12 Cat 5 grant-ID extraction -> researchmap research_projects: 10/22 projects populated, 21 papers; fetch_live guard bug fixed; 41 PDFs archived in tools/papers/. Leftover fact (7 unfilled rows) -> tools/state/facts.md.
- RM<->website consolidation Cat 1-4 published (80a0de8); media_coverage exporter (d543652); latency pins (56669c5).
