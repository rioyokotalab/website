# Skill: Web lookup (codex has network access)

Codex workers run with `sandbox_mode="danger-full-access"` and
`approval_policy="never"`; outbound network is available directly from the
codex session (configuration reference checked 2026-07-12).
Claude Bash curl is the fallback and one independent-verification route.

- Preferred structured sources first: Crossref `api.crossref.org`, DBLP,
  Semantic Scholar, arXiv, J-STAGE `api.jstage.jst.go.jp`, publisher DOI
  resolvers, researchmap public read API
  `https://api.researchmap.jp/rioyokota/{type}`. Prefer JSON APIs over
  scraping HTML.
- OpenReview and researchmap LOGIN pages block non-browser clients (403):
  never automate a login UI, never enter or read credentials.
- Same-paper confirmation gate: title AND authors AND year must agree before
  recording a DOI/URL; otherwise record BLANK with a reason.
- Record the source URL next to every resolved fact in the output file.
- Session discipline: <=2 lookup items per codex session; append each result
  the instant it resolves and run `tail -1 <output-file>` before continuing.
- A DNS/HTTP failure for a provider is terminal for that provider in the
  session: record it and move on; do not retry-loop.
- Verification gate: factual claims that will be committed, published, or
  reported must be independently cross-checked (a different worker, e.g.
  codex-medium, or Claude curl) against the authoritative source. Never
  surface an unverified claim: verify it or omit it, marking leftovers under
  evidence.hypotheses in the structured result block.
- Never ask the user to confirm publicly-verifiable facts (CLI syntax, API
  behavior, versions); verify from authoritative sources. Escalate only for
  preferences, private values, or judgment decisions.

Cap scope: the <=2-item session cap counts EXTERNAL LOOKUP ITEMS (papers,
DOIs, facts resolved via ad-hoc web queries). Running a repository
exporter/tool that internally calls authorized APIs (e.g.
researchmap-export.py --check-live) is NOT a lookup item; it is governed
by its own task's instructions. (Codified 2026-07-12 after the Sol/Terra
T-9 interpretation split.)
