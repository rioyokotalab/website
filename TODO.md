# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. Immediate execution state:
`tools/state/session.md`. Git preserves older completion detail and command
evidence. Next free id: T-186.

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
    checks use the repository Python entry points. Harness T-175 restored the
    local checksum-pinned lftp prerequisite; T-182 then passed the complete
    offline security suite without a network or live deployment.

## Active

None.

## Blocked / awaiting user

None.

## Recently completed

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

Superseded task detail remains in Git; harness work is owned by
`~/harness/TODO.md`.

## Issues appended during the T-180 sweep

- **T-181 — Remove validation-command npm logs (complete 2026-07-15):** an
  incorrect assumption that repository validation was exposed as npm scripts
  failed before any test and created two diagnostic logs under `~/.npm/_logs`.
  The files were never read; each exact canonical path was independently
  checked for owner and post-incident timestamp, unlinked non-recursively, and
  verified absent. The actual ledger checks are
  `python3 tools/task-metrics.py validate`, `python3 tools/check-md-size.py`,
  and `python3 tools/standards-check.py`.
- **T-182 — Guard deployment staging and mirror deletion (complete
  2026-07-15):** the T-175 review found raw recursive temporary-tree cleanup in
  `deploy.sh` and three test/preview scripts, plus unbounded remote recursive
  deletion in the lftp mirror. Added one shared canonical cleanup helper that
  delegates to the harness's immutable manifest/token workflow, protects the
  account home, verifies absence, and preserves operation/signal status. All
  four owners now use it; no raw recursive cleanup remains in website shell
  scripts. The lftp wrapper hashes and revalidates every staged file, requires
  two identical validated dry-runs, protects `.dont-remove-me`, caps file
  deletions at 250, refuses unsafe paths and all recursive directory deletion,
  then applies autonomously without an approval prompt. Exact local file-
  backend deletion, sentinel preservation, recursive-directory refusal, home-
  target refusal, warning/error ShellCheck, Bash/Python syntax, diff checks,
  preview/publish regressions, and the complete offline security suite pass.
  No SSH, credential, live-server, public-file, push, or deployment operation
  ran. The one validation-created bytecode file was unlinked exactly.
- **T-183 — Push recovered repositories and prepare the next-task handoff
  (complete 2026-07-15):** reconciled both clean branches with `origin/main`,
  reserved harness T-182 ahead of the owner-gated T-181 proposal, validated the
  ledgers and local harness doctor, and pushed without force or deployment.
  Final acceptance requires each current local `HEAD` to equal its remote
  `origin/main`; exact revisions are reported in the session handoff.
