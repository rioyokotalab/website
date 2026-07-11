# Skill: Web lookup (codex has network access)

Codex workers run with `sandbox_workspace_write.network_access=true`
(verified codex-cli 0.144.1): fetch sources DIRECTLY from the codex session.
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
