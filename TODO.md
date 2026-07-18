# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. Immediate execution state:
`tools/state/session.md`. Git preserves older completion detail and command
evidence. Next free id: T-191.

## Recovery priority — do before any other task

- **T-180 — Exhaustively re-audit Git history for additional recovery
  candidates (complete 2026-07-15):** the full local refs, reflogs, reachable
  graph, read-only unreachable objects, historical task paths, deployment
  exclusions, pre-incident reports, metrics/logs, and pre-/post-incident trees
  were reconciled with harness T-172. No public file, recovery candidate,
  credential/auth state, owner config, package, remote, or deployment changed.

  - `628b53a` and current each contain 275 paths with identical mode counts
    (257 regular and 18 executable; no symlink/submodule). All eight damaged
    paths—`README.md`, `cv/build-cv.sh`, `cv/cv.cls`, `cv/cv.pdf`, `cv/cv.tex`,
    `package.json`, `publish.sh`, and `style.css`—match `628b53a` exactly by
    object ID, working-file hash, and mode. The only later website changes are
    the six recovery-ledger files.
  - All 12 unreachable commits predate the incident and are superseded July 12
    evaluation variants or the July 14 ResearchMap autostash. Named trees map
    216 of 218 unreachable blobs. Safe header-only checks identify the other
    two as in-progress T-29 and T-30 `session.md` checkpoints. None should be
    restored or published.
  - The ignored T-11 permission payload has no current path, reachable object,
    or unreachable tree name. Commits `b73c2c5`, `f92abf3`, `31b5b5b`, and
    `194fc04` preserve its intent and applied outcome, but the payload is
    confirmed missing from local evidence and is superseded by T-179. The
    surviving ignored T-170 configuration reports/proposals and T-167–T-178
    driver reports predate the incident, are deploy-excluded, and remain valid
    historical evidence; preserve them.
  - T-170–T-179, the `tools/todo.md` to root `TODO.md` rename at `628b53a`, the
    harness dot-directory move at `94119a2`, and both post-incident website
    commits reconcile without a missing tracked path. Harness T-172 contains
    the authoritative recovery table, sensitivity boundaries, validation and
    rollback routes, and reviewed execution order.
  - Deployment exclusions still keep tools, skills, ledgers, config, README,
    and CV sources out of the public tree. Metrics validation and standards
    checks use the repository Python entry points. Harness T-175 originally
    restored the local lftp prerequisite; T-188 now owns its checksum-pinned
    rootless bootstrap and complete offline validation locally.

## Active

- **T-190 — Repair the stale local pre-commit hook safely (ready for Claude):**
  T-189's first commit failed because `.git/hooks/pre-commit` still calls the
  removed `tools/check-claude-size.py` before the valid
  `tools/check-md-size.py`; the README already documents the current hook.
  A Claude DRIVER should claim T-190, read `skills/config-proposals.md`, and
  implement the smallest website-owned, deploy-excluded canonical hook/doctor
  plus focused offline coverage and an exact owner apply/rollback handoff.
  Do not restore the removed checker, depend on a sibling repository, use
  `--no-verify` as the final fix, deploy, or change public-site files. Agent
  edits to the live `.git` hook remain forbidden without a new explicit owner
  override, so mark `awaiting-user` after tracked work. Complete only after the
  owner-applied hook matches the canonical form, the size gate passes, and an
  ordinary test commit reaches it without bypass.

## Blocked / awaiting user

None.

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
