# Skill: web lookup

Codex runs with outbound network access. Prefer structured primary sources:
Crossref, DBLP, Semantic Scholar, arXiv, J-STAGE, publisher DOI resolvers, and
the public researchmap API. Prefer JSON APIs over scraped HTML.

- Never automate login pages or enter/read credentials.
- Confirm title, authors, and year before recording a DOI or publication URL.
- Record the source URL next to every resolved fact.
- Limit each session to two external lookup items. Repository exporters that
  call already authorized APIs follow their own task instructions and do not
  consume this cap.
- A DNS/HTTP failure is terminal for that provider in the session; do not
  retry-loop.
- Independently cross-check factual claims that will be committed, published,
  or reported, using another authoritative source or a separate bounded Codex
  review. Verify or omit; unresolved material belongs under hypotheses.
- Ask the user only for private values, preferences, or judgment decisions;
  verify publicly discoverable facts directly.
