# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-180.

## Active

None.

## Blocked / awaiting user

None.

## Recently completed

- **T-179 — Recover untracked global/local agent configuration:** reconstructed
  T-11 and T-170–T-173 from Git history; restored Codex never/full-access and
  exact website trust while preserving the current model; transactionally
  recreated 17 missing harness/global discovery links; retained surviving
  Claude owner state and the repository hook; and passed host-side idempotence,
  doctor, TOML, transaction-mode, and fresh Codex discovery/default checks.

- **T-178 — Align repository housekeeping paths:** moved the website task board
  to root `TODO.md`; moved harness client sources to `.codex/` and `.claude/`;
  updated every current reference and the fail-closed legacy-link migration;
  and passed website, isolated-installer, live-link, and clean-clone checks.

- **T-177 — Repair and close the ResearchMap import:** corrected six reported
  conflicts and two silent similarity merges with a minimal 16-operation
  repair, received confirmation that it imported successfully, recorded all
  eight new IDs and 411 visible managed IDs, deleted the unuploaded five-row
  live residual, and removed every transient ResearchMap artifact and cache.

- **T-167 — Resolve held metadata cases:** corrected three citation conflicts,
  classified all 29 held matches, reconciled one safely detected live candidate
  drift, and independently audited a 251-operation additive ResearchMap plan
  with 25 inserts, 226 updates, zero deletes, and zero unresolved ambiguities.
  All offline/browser/live gates passed; mirrored Achievements pages were
  published at `fd2f2d8`, and the resulting import was completed under T-177.

- **T-176 — Prepare a restart-safe handoff:** audited the board, session,
  reports, metrics, website worktree, and synchronized harness repository;
  confirmed there is no active task, preserved the T-167 dirty working set,
  and made the explicit restart boundary “wait for user; do not start T-169.”

- **T-175 — Push the integrated harness:** after the user externally changed
  `origin` to the configured SSH alias and requested a retry, confirmed the
  remote was empty, passed all local and clean-clone gates, pushed local
  `0bd31d1` to new remote `main` without force, established tracking, and
  verified exact commit equality with zero divergence. T-169 was not started.

- **T-174 — Diagnose Codex CLI shell-snapshot warnings safely:** traced the
  arg0 warning to accumulated/racing temp directories, removed 329 empty dirs,
  quarantined four inactive scaffolding dirs, preserved three active locks,
  isolated the snapshot failure to four extglob-dependent system-completion
  functions, made Bash completion interactive-only, passed a clean default
  ephemeral discovery probe, and documented the workaround at harness commit
  `0bd31d1`. T-169 was not started.

- **T-173 — Integrate Codex and Claude in a portable harness:** preserved Git
  history while moving the repository to `~/harness`, split Codex/Claude/shared
  surfaces, installed common guidance and six skills for both clients, excluded
  sensitive/runtime Claude state, added the requested GitHub `origin` without
  pushing, passed live and clean-clone discovery checks, and committed
  `805db48` locally.

- **T-172 — Version the portable global Codex harness:** created the original
  allowlisted repository (moved to `~/harness` by T-173), made global guidance,
  six personal skills, and reviewed rules canonical there, installed
  fail-closed discovery symlinks, verified a fresh Codex project and
  clean-clone restore, and committed `7f96931` without sensitive/runtime files.
- **T-171 — Add automatic global-configuration promotion policy:** added and
  fresh-project-verified a global rule that automatically promotes only stable,
  evidence-backed, non-sensitive cross-project guidance and personal skills;
  keeps repositories self-contained; and batches approval for `config.toml`,
  profiles, hooks, MCP, plugins, authentication, packages, and external state.
- **T-170 — Separate project and global Codex configuration:** installed and
  diagnostically verified `~/.codex/AGENTS.md` plus six reusable personal
  skills for ledgers, delegation, evidence, research engineering,
  presentations, and research-program management. Kept all website formats,
  deployment, ResearchMap, ledger adapters, and WBD routing evidence local;
  left the existing mode-0600 `~/.codex/config.toml` unread and untouched.
- **T-168 — Relocate benchmark artifacts and clear transient output:** moved
  173 referenced raw runs (1,102 files, 57 MB) to the ignored benchmark-owned
  archive, migrated every producer/result/metric pointer, passed all checks,
  and left `tools/out/` empty.
- **T-166 — Repair and re-import the ResearchMap JSONL:** repaired all 86
  bilingual-title validation errors, received confirmation that the retry
  import succeeded, recorded 379 visible matched IDs, and removed transient
  import artifacts.
- **T-165 — Validate, publish, and verify:** passed offline, browser,
  deployment, live-byte, and remote-commit gates; published both Achievements
  pages at commit `65dac52`.
- **T-157–T-164 — ResearchMap metadata campaign:** inventoried 309 entries,
  filled evidence-backed metadata, normalized mirrored Achievements formatting,
  added 30 arXiv/BibTeX rows per language, aligned exporter schemas, and
  generated an independently audited additive import.
- **T-146–T-156 — GPT-5.6 benchmark campaign and housekeeping:** reconciled
  173 runs, installed routing policy `2026-07-14.3`, published comparison
  tables at the bottom of the README, and preserved all referenced evidence.

Older completion history remains in Git and `tools/codex-log.md`.
