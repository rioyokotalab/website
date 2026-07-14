# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. Immediate execution state:
`tools/state/session.md`. Git preserves older completion detail and command
evidence. Next free id: T-181.

## Recovery priority — do before any other task

- **T-180 — Exhaustively re-audit Git history for additional recovery
  candidates:**
  1. Traverse the complete `website` and `harness` commit graphs, all local
     refs, reflogs, and read-only unreachable-object reports. Begin with the
     verified pre-incident website revision `628b53a` and harness revision
     `5f6382b`; reconcile every restoration and configuration-recovery commit.
  2. Compare pre-incident and current tracked inventories, modes, symlinks,
     renamed control paths, deployment exclusions, and task state. Reconfirm
     the exact eight website paths restored after the deletion and search for
     additional tracked or dangling-object candidates without modifying the
     public site.
  3. Reconstruct website T-11 and T-170–T-179 from Git evidence, including old
     path names before T-178. Cross-reference harness T-172 rather than keeping
     a second divergent harness incident transcript here. T-179's first
     unreachable-object search found surviving ledger variants but not the
     deleted ignored proposal payload; repeat exhaustively without assuming a
     second search will recover it.
  4. Produce a recovery table with source commit/object/path, pre-incident
     purpose, current state, confidence, sensitivity boundary, dependencies,
     validation, and rollback. Distinguish already recovered, intentionally
     retired, confirmed missing, and unresolved state.
  5. Never inspect or restore credentials, private keys, tokens, auth stores,
     shell/client histories, live sessions, `.git` internals, or secret values.
     Perform no restoration or publication during the audit; present one
     reviewed plan first.

## Active

None besides recovery-first T-180.

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
  recreated the missing host directory and passed. Post-incident duplicate
  facts, decisions, session chronology, and the temporary T-179 driver report
  were consolidated into this board. Both ledgers pass structural/budget and
  diff checks; website metrics and standards checks pass; no deploy-included
  file changed. The isolated deployment-policy test stopped before execution
  because recovered normal-PATH `lftp` is absent; no network or deployment ran,
  and T-180 owns that recovery evidence.

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

Older task-by-task completion summaries, driver reports, and the pre-cleanup
T-179 state remain in Git through commit `e9ac8a0` and earlier. Use them as
evidence during T-180, not as current instructions. Harness work is owned by
`~/harness/TODO.md`.
