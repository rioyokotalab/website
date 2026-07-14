# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. Immediate execution state:
`tools/state/session.md`. Git preserves older completion detail and command
evidence. Next free id: T-183.

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

None. Current recovery/tool/fleet work is owned by `~/harness/TODO.md`.

## Blocked / awaiting user

None.

## Recently completed

- **T-179 — Recover and consolidate global/local agent configuration:** after
  the home-deletion incident, reconstructed T-11 and T-170–T-173 from Git
  history and chose the current layered design rather than retired project
  machinery. Restored Codex `never`/`danger-full-access` plus exact home and
  website trust while preserving Sol/high; harness transaction
  `20260714T202625Z-3548153` recreated 17 missing command/guidance/rule/skill
  links and retained eight surviving Claude links. Repeated plan/doctor,
  mode-0600 transaction, TOML, idempotence, and fresh host Codex checks passed
  (`GLOBAL_OK SKILL_OK`). Surviving Claude settings and the untracked website
  pre-commit hook were left unchanged; agents do not edit `.git`. Product-
  managed policy may still override local defaults on some surfaces, but the
  verified fresh host CLI honored them. The app's synthetic read-only
  `.agents` mount blocked one sandboxed probe; the bounded real-host recovery
  recreated the missing host directory and passed. Duplicate recovery detail
  and the temporary T-179 report were consolidated into this board. Ledger,
  metrics, standards, and diff checks pass; no deploy-included file changed.
  The first isolated deployment-policy test stopped before
  execution because normal-PATH lftp was absent. Harness T-175 later restored
  it through a checksum-pinned local transaction, and website T-182 passed the
  complete offline deployment-policy suite without a network or live deploy.

- **T-170–T-176 and T-178 — Establish and move the portable agent harness:**
  separated
  cross-project agreements from website rules; added conservative promotion;
  versioned the non-secret allowlisted harness; integrated Codex and Claude;
  diagnosed shell-snapshot/arg0 warnings; pushed the harness after the owner
  configured its SSH remote; transferred harness task ownership; and moved the
  website board plus harness client sources to their current root/dot paths.
  The canonical implementation and current recovery state now live in
  `~/harness`; this board retains only the website-facing outcome. Key durable
  commits include `194fc04`, `7f96931`, `805db48`, `0bd31d1`, and `628b53a`.

- **T-177 and T-167 — Complete the ResearchMap reconciliation:** reviewed 29
  held classifications, published the mirrored citation corrections, audited
  an additive 251-operation plan, repaired six conflicts and two silent merges,
  received successful-import confirmation, recorded all eight forced IDs and
  411 visible managed IDs, and removed the unuploaded residual and transient
  import artifacts. Exact operation and hash evidence remains in Git and
  `tools/researchmap-state.json`.

- **T-168 and T-146–T-166 — Close the benchmark/metadata campaign:** relocated
  173 referenced benchmark runs to the ignored benchmark archive, reconciled
  all result/metric pointers, installed routing policy `2026-07-14.3`,
  completed the ResearchMap metadata/export sequence, and published the
  validated Achievements pages. Detailed evidence remains in the benchmark
  data, state files, metrics, and Git.

## Archived detail

Superseded task detail remains in Git through `e9ac8a0`; harness work is owned
by `~/harness/TODO.md`.

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
