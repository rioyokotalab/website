# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. Immediate execution state:
`tools/state/session.md`. Git preserves older completion detail and command
evidence. Next free id: T-191.

## Active

None.

## Blocked / awaiting user

- **T-190 — Repair the stale local pre-commit hook safely (awaiting owner
  apply):** tracked work is done: canonical `tools/hooks/pre-commit`,
  `tools/hook-doctor.sh` (read-only doctor + owner apply/rollback with
  automatic backup), `tools/test-hook-doctor.sh` (8 checks) wired into
  `tools/test-security.sh`, and README section 4 now installs via the doctor.
  Full offline suite passes; doctor confirms the live hook is stale; no `.git`
  file was edited, the removed checker stays removed, and no bypass was used.
  Owner: follow `tools/out/t190-hook-apply-handoff.md`
  (`tools/hook-doctor.sh apply`, doctor `ok`, one ordinary commit through the
  hook; rollback via `tools/hook-doctor.sh rollback`), then T-190 can close.

## Recently completed

- **T-189 — Add website-owned Claude takeover and live evaluation (complete
  2026-07-18):** repository-owned Claude guidance and client-neutral ledger,
  metrics, publication, and offline coverage passed three bounded sessions,
  primary review, and all tests. Evidence:
  `docs/audits/claude-live-takeover-2026-07-18.md`. No public
  file, deployment, owner setting, credential, or external repository changed.

- **T-188 — Make website independent of harness (complete 2026-07-18):**
  website now owns its manifest/token guarded cleanup, CI path, ruleset
  payload/test, value-free public-history audit tool/evidence/test, and
  checksum-pinned rootless lftp bootstrap. Focused safety checks, the complete
  offline suite, 38 browser tests, and an isolated clean clone with unusable
  `HARNESS_BIN` and a locally bootstrapped lftp passed. PR #3's first CI run
  exposed and fixed a system-path test assumption; exact head `beb44b9` then
  passed required `Offline checks` run `29627893789` and squash-merged as
  `6f1ad83`. Coordinated harness PR #7 passed its own CI and merged as
  `f1b095c`. No public-site file, deployment, live lftp removal, account
  setting, credential, history rewrite, or fleet operation occurred.

- **T-187 — Validate strict `main` ruleset through a pull request (complete
  2026-07-18):** active ruleset `19127356` still exactly matches the reviewed
  five-rule payload with no bypass actor. Deploy-excluded ledger-only PR #1
  passed required `Offline checks`, received non-author `rioyokota2` approval
  on its tested head, and squash-merged through the ruleset as `162bef0`. No
  deployment or public-site file changed.

- **T-186 — Publish recovered ledger commits and add offline CI (complete
  2026-07-17):** pushed the three recovered T-185 commits unchanged, then added
  read-only Ubuntu 24.04 CI for the complete offline static and locked browser
  suites. Hosted run `29566375620` passed at `c90760b`; no public-site file was
  deployed. Strict repository rules remain gated on an eligible non-author
  reviewer and completion of all required direct pushes.

- **T-185 — Assess risks of making the repository public (complete
  2026-07-16):** the current static tree, 379-commit reachable history, public
  staging boundary, client dependencies, live headers/redirects, and excluded
  live paths were reviewed. Both offline and live security suites pass; no
  confirmed credential or direct repository-to-site compromise path was found.
  Public visibility still exposes deleted photos/member content, old config and
  reports, deployment topology, and the local credential-file location. Prefer
  a sanitized public allowlist mirror, or complete an owner privacy/history
  review and enable repository/account protections before exposing this exact
  history. No public file, account, push, or deployment changed.

- **T-184 — Reconcile global PIE and node-onboarding skill work (complete
  2026-07-16):** harness T-189 established the shared ledger-backed PIE skill;
  T-190 then implemented, installed, tested, and published the guarded
  `onboard HOST` workflow at `b5bb171`, with its compact completion ledger at
  `d5b82cd`. The alias remains the entire discovery boundary; credentials stay
  owner-only; both manual restore gates precede separately authorized
  scheduling. No live node, public-site file, deployment,
  credential, SSH configuration, package, or scheduler state changed.

- **T-180 — Exhaustively re-audit Git history for additional recovery
  candidates (complete 2026-07-15):** refs, reflogs, the reachable graph,
  unreachable objects, historical task paths, deployment exclusions, and pre-/
  post-incident trees were reconciled with harness T-172. All eight damaged
  paths match `628b53a` exactly; all 12 unreachable commits are superseded
  pre-incident variants; the ignored T-11 payload is confirmed missing and
  superseded by T-179. Deployment exclusions remain intact. Full evidence is
  preserved in Git history of this entry. No public file, recovery candidate,
  credential/auth state, owner config, package, remote, or deployment changed.

- **T-179 — Recover and consolidate global/local agent configuration
  (complete):** reconstructed the non-secret layered configuration from Git,
  preserved owner settings, and used harness transaction
  `20260714T202625Z-3548153` to restore missing discovery links. Repeated
  plan/doctor, mode, TOML, idempotence, and fresh-client checks passed. Detailed
  recovery chronology was consolidated here; T-175 later restored pinned lftp
  and T-182 passed the complete offline deployment-policy suite. No public
  file, credential, deployment, or unrelated owner setting changed.

## Archived detail

Superseded completion detail and command evidence remain in website Git
history. Cross-repository task references above are immutable provenance, not
execution or ownership dependencies.
