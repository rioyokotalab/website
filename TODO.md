# Lab website — task board

This is the authoritative resume point for the YOKOTA Lab website repository.
Protocol and schemas: `skills/context-ledger.md`; immediate execution state:
`tools/state/session.md`; durable choices: `tools/state/decisions.md`. Git
retains superseded chronology and command-level evidence — keep only current
state, active tasks, blockers, and compact historical pointers here. Next
free ID: T-206.

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
- The live pre-commit hook matches canonical `tools/hooks/pre-commit`;
  `tools/hook-doctor.sh` verifies/applies/rolls back (T-190).
- The site is static mirrored EN/JP HTML with no build step. Deployment is
  positive-allowlist staging behind gated `publish.sh`/`deploy.sh`; tools,
  skills, ledger, config, README, and CV sources never deploy.
- The offline suite (`tools/test-security.sh`) and locked browser tests run
  green in required CI, which triggers on pull requests only (T-194). The
  repository is operationally independent of any sibling repo (T-188).
- Website-started sessions treat `~/harness` as strictly read-only (owner
  rule in `AGENTS.md`, `063f021`); its shared skills are read and applied by
  default per the promoted global guidance (harness `66abee5`).

## Next resume checkpoint

No active task. The next free ID is T-206.

## Active tasks

None.

## Completed-task index

Git history is the durable evidence store: full chronology lives in this
file's history, at `tools/todo.md` before the `628b53a` root rename. The
anchored versions below hold command-level detail for each era.

| Task | Completed outcome / durable pointer |
|---|---|
| pre-T-1–T-23 | Initial ResearchMap/site fixes and the context-ledger, deployment exclusions, bounded delegation, and repository workflow. `986ed09:tools/todo.md`, `28f8685:tools/todo.md`. |
| T-24–T-108 | Security, deploy allowlisting, metadata, accessibility, responsive/print behavior, and locked browser coverage. `d44f862:tools/todo.md`, `17b5eb8:tools/todo.md`. |
| T-109–T-178 | Agent benchmark/handoff work, ResearchMap reconciliation, and extraction of the portable harness. `d888cbc:tools/todo.md`, `d928540:tools/todo.md`, `041a453:TODO.md`. |
| T-179–T-189 | Recovery, guarded deployment cleanup, protected CI, harness independence, and website-owned Claude takeover. `64c4b18:TODO.md`, `docs/audits/claude-live-takeover-2026-07-18.md`. |
| T-190 | Canonical pre-commit hook and doctor landed (PR #7 `e6faf3b`); owner-applied hook verified byte-identical; standing authorization recorded. |
| T-191 | Live ruleset `19127356` verified to match `docs/github-rulesets/main.json`; presumed divergence did not exist; read-only. |
| T-192 | Sanitized-mirror route built then reversed by owner; repository made public with ruleset intact; secret scanning enabled, zero alerts (`676c209`). |
| T-193 | Task board restyled to the harness layout: current state, resume checkpoint, and this grouped completed-task index reconstructed from full board history. |
| T-194 | "CI workflow run" email noise fixed (`69172ae`): CI is PR-only (post-merge push run was redundant); owner enabled the account "notify only on failure" setting. Owner also ruled `~/harness` read-only for website sessions (`063f021`). |
| T-195–T-198 | Attack-surface hardening loop (`docs/security-threat-model.md`). T-196 repo-content baseline (`781e317`: SECURITY.md, dependabot.yml, least-privilege CI token, `workflow-security-check.py` + test). T-197 settings applied (reversible via `tools/out/t197-settings-rollback.md`: read-only token, SHA-pinned + GitHub-owned actions, Dependabot security updates, private vuln reporting, fork-PR approval all-external, wiki/projects off). T-198 = B9: `main` requires 1 review with a Repository-admin bypass (owner self-merges; 66 org write collaborators need approval) — ruleset `19127356`, `3574f40`. Verified `actions/checkout` v7.0.0 bump `c52c101`. |
| T-199 | Repeated the README benchmark with Claude (harness support `58f5e7b`): 75 singletons × {fable-5, opus-4-8, sonnet-5} × 5 efforts + 14 repeats. 72/75 full-quality; the 3 higher-effort WBD-003 misses were variance (14/14 repeats pass). Low effort best; Fable 25/25. `tools/agent-benchmark/claude-full-20260718.summary.md` + README section. |
| T-200 | Security proposals: HSTS `max-age` raised 1 day → 1 year, **deployed and verified live** (max-age=31536000, HTTP→HTTPS intact). Org `default_repository_permission` change **declined** (org-wide 100+ repos; T-198 gate suffices). |
| T-201 | Merged the GPT-5.6 and Claude README benchmark tables into one section (unified 6-model table + side-by-side per-effort comparison; token caveat kept). |
| T-202 | Fixed the deploy deletion guard (`439ef4d`): it mis-read SFTP in-place updates as unmatched deletions, blocking every real deploy since T-182. True deletion = removed-not-transferred; SFTP-format test added. Unblocked T-200. |
| T-203 | Housekeeping: pruned 8 stale remote-tracking refs, deleted the superseded `t187-ruleset-closeout` branch, and guarded-deleted 92 disposable Claude benchmark artifact dirs (~37 MB; 173 GPT artifacts + tracked evidence intact). |
| T-204 | Relocated the Local checkout to `~/projects/website` by fresh clone; preserved all ignored state and the remote-backed branch, kept Playwright runtime state local for NFS performance, passed offline and 38 browser checks, and guarded-deleted the old checkout. |
| T-205 | Reran exact current GPT-5.6 (90 cells) and Claude Code (75 cells) matrices through receipt-backed cowork. GPT moved 85→86 strict and 89→90 browser-functional; Claude moved 72→71 strict and held 74 browser-functional. Focused inspection recovered two selected routes. README tables, matched comparisons, and `docs/audits/agent-benchmark-nightly-2026-07-24.md` updated; security and 38 browser tests pass. |
