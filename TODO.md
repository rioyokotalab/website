# Lab website — task board

This is the authoritative resume point for the YOKOTA Lab website repository.
Protocol and schemas: `skills/context-ledger.md`; immediate execution state:
`tools/state/session.md`; durable choices: `tools/state/decisions.md`. Git
retains superseded chronology and command-level evidence — keep only current
state, active tasks, blockers, and compact historical pointers here. Next
free ID: T-195.

## Current state

- The repository, including its full history, is public (T-192, 2026-07-18)
  at the owner's explicit instruction; every tracked file is public the
  moment it is pushed. Secret scanning and push protection are enabled with
  zero alerts.
- `main` is protected by active ruleset `19127356`: pull request plus the
  required `Offline checks` CI run, linear history, conversation resolution,
  no bypass actors, zero required approvals. A driver may self-merge its own
  PR after the required check passes and may repair local pre-commit hook
  drift via `tools/hook-doctor.sh` (standing authorizations in decisions.md).
- The live pre-commit hook matches the tracked canonical
  `tools/hooks/pre-commit`; `tools/hook-doctor.sh` verifies, applies, and
  rolls back (T-190).
- The site is static mirrored EN/JP HTML with no build step. Deployment is
  positive-allowlist staging behind gated `publish.sh`/`deploy.sh`; tools,
  skills, ledger, config, README, and CV sources never deploy.
- The complete offline suite (`tools/test-security.sh`) and the locked
  browser tests run green in required CI; the repository is operationally
  independent of any sibling repository (T-188).

## Next resume checkpoint

The board is empty. One optional owner step remains from T-194: the
account-level "Only notify for failed workflows" checkbox
(`tools/out/t194-actions-notifications-handoff.md`). Claim T-195 for new
work, read the matching playbook in `skills/`, and checkpoint
`tools/state/session.md` at task start.

## Active tasks

None.

## Completed-task index

Git history is the durable evidence store: full chronology lives in this
file's history, at `tools/todo.md` before the `628b53a` root rename. The
anchored versions below hold command-level detail for each era.

| Task | Completed outcome / durable pointer |
|---|---|
| pre-T-1 | 2026-07-08–11: ResearchMap metadata fields 1–5 applied to both mirrored achievements pages and the researchmap/ORCID exporters; JP mobile-nav fix; codex-offload configuration and SPARK worker migration; size-guard pre-commit. Free-form chronology at `986ed09:tools/todo.md`. |
| T-1–T-23 | 2026-07-12: context-ledger scheme adopted; README rewrite; deploy exclusions; DOI/CV reconciliation; permission audit; two design-evaluation rounds closed without adoption; bounded native Codex delegation; Dreamweaver template cleanup. `28f8685:tools/todo.md`. |
| T-24–T-53 | 2026-07-12–13: security and metadata hardening — archived-PDF history purge, expired-credential removal, CSP/HSTS/Permissions-Policy enforcement, SRI audit, positive-allowlist deploy staging, offline security suite wired into `publish.sh`, landmarks, crawler files, social metadata. `d44f862:tools/todo.md`, `8aa8582:tools/todo.md`. |
| T-54–T-108 | 2026-07-13: page-quality campaign — titles/descriptions, image dimensions/lazy-loading/decoding, shared-CSS migration off legacy markup, print layer, no-JS, reduced-motion and forced-colors support, accessible Lightbox, dead-CSS source-reference gates, locked Playwright suite. `b37c792:tools/todo.md`, `17b5eb8:tools/todo.md`. |
| T-109–T-141 | 2026-07-13: agent-benchmark era — capability suite frozen, harness calibrated, routing/handoff optimization iterations, artifact and handoff integrity gates, metrics schema and compaction. `d888cbc:tools/todo.md`. |
| T-142–T-166, T-168 | 2026-07-13–14: GPT-5.6 benchmark matrix campaign, evidence-backed dispatch policy, WBD005 qualification, obsolete comparison machinery removed. `d928540:tools/todo.md`. |
| T-167, T-177 | 2026-07-14: ResearchMap reconciliation completed, including fail-closed sync inserts (see decisions.md). `041a453:TODO.md`. |
| T-170–T-176, T-178 | 2026-07-14: portable agent harness established and moved out of the website, including the pinned lftp restore. `041a453:TODO.md`. |
| T-179–T-183 | 2026-07-14–16: post-incident recovery — layered agent configuration reconstructed (T-179); exhaustive Git recovery re-audit found no additional candidate (T-180); npm validation logs removed (T-181); deployment staging and mirror deletion guarded (T-182); recovered repositories pushed with next-task handoff (T-183). `041a453:TODO.md`, `64c4b18:TODO.md`. |
| T-184 | Global PIE and node-onboarding skill work reconciled; alias-only discovery boundary, credentials owner-only. |
| T-185 | Public-visibility risk assessment: no credential path found; history exposure caveats recorded and later accepted at T-192. |
| T-186 | Recovered ledger commits pushed; read-only offline CI added (run `29566375620` at `c90760b`). |
| T-187 | Strict `main` ruleset validated end-to-end through PR #1 (`162bef0`). |
| T-188 | Website made operationally independent of the harness; PR #3 merged as `6f1ad83`. |
| T-189 | Website-owned Claude takeover and live evaluation passed; `docs/audits/claude-live-takeover-2026-07-18.md`. |
| T-190 | Canonical pre-commit hook and doctor landed (PR #7 `e6faf3b`); owner-applied hook verified byte-identical; standing authorization recorded. |
| T-191 | Live ruleset `19127356` verified to match `docs/github-rulesets/main.json`; presumed divergence did not exist; read-only. |
| T-192 | Sanitized-mirror route built then reversed by the owner (PR #10 closed unmerged); repository made public with ruleset intact; secret scanning enabled, zero alerts (PR #11, `676c209`). |
| T-193 | Task board restyled to the harness layout: current state, resume checkpoint, and this grouped completed-task index reconstructed from full board history. |
| T-194 | "CI workflow run" email noise fixed repo-side: redundant post-merge push run removed from `ci.yml` (strict up-to-date + squash makes it byte-identical to the tested PR head); account "Only notify for failed workflows" step handed to the owner. Owner also ruled `~/harness` read-only for website sessions (`063f021`). |
