driver: codex
updated: 2026-07-14T07:50+0900
task: T-165 Validate, publish, and verify | in-progress
status: in-progress

## Now
- T-157--T-164 are complete. The exhaustive inventory, category fill plans,
  post-fill audit, and import audit are in `tools/out/`. All 309 mirrored
  citations follow the majority format; 30 entries per page have separate
  `[arxiv] [bibtex]` rows; semantics and CRLF are intact.
- The final JSONL has 19 inserts, 299 additive updates, zero deletes, 29 held
  ambiguities, and SHA-256
  `ed567339f86c5a51552cf3e7b8df32459f8d2cdfa1e14a36043ffa050b305228`.
  Managed state remains empty until a successful manual upload is confirmed.
- Independent review found and root fixed both P1 exporter defects plus the
  matcher P2. Managed nested values are excluded, ORCID honors explicit
  metadata guards, and fuzzy titles require contributor/venue context. Both
  audits now recommend SHIP; only 29 deliberate ambiguities and three citation
  conflicts remain held. Offline/security/schema tests and all 38 browser tests
  pass.
- T-165 is running commit, deploy-preview, publication, live-page, and exact
  remote-commit gates. The branch is rebased and current with `origin/main`.
- `git pull --rebase --autostash origin main` reports the branch current. All
  pre-publish offline, schema, import, browser, security, task-metrics, and
  publish-regression gates are green; the next action is commit and deploy
  preview, followed by the repository publish pipeline and live verification.
- A redundant post-rebase ResearchMap API refresh ended with a remote-close;
  per the lookup playbook that provider will not be retried this session. The
  immediately preceding post-fix fresh audit is authoritative because the
  rebase changed no files. Offline hash/shape checks still confirm 318 lines,
  19 inserts, 299 unique updates, zero deletes, and SHA-256 `ed567339…5228`.
- Campaign window ends around 08:45 JST.
- Commit `fcf9d97` is pushed/deployed; both live Achievement pages are exact
  local-byte matches and `origin/main` equals HEAD. The live security gate then
  exposed the preserved server sentinel at HTTP 200. Root added an exact-file
  Apache deny rule and static regression check without reading/changing the
  sentinel; this follow-up must pass preview, publish, and live verification.

## Working set
- `en/achievements/index.html`, `jp/achievements/index.html`
- `tools/researchmap-export.py`, `tools/orcid-export.py`
- `tools/test-researchmap-export.py`, `tools/researchmap-state.json`
- `tools/todo.md`, `tools/state/session.md`, `tools/out/`

## Open questions
- None.

## Awaiting user
- None.
