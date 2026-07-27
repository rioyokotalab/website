# Lab website — task board

This is the authoritative resume point for the YOKOTA Lab website repository.
Protocol and schemas: `skills/context-ledger.md`; immediate execution state:
`tools/state/session.md`; durable choices: `tools/state/decisions.md`. Git
retains superseded chronology and command-level evidence — keep only current
state, active tasks, blockers, and compact historical pointers here. Next
free ID: T-210.

## Current state

- The repository and full history are public by owner instruction (T-192);
  every pushed tracked file is public. Secret scanning and push protection
  are enabled with zero alerts.
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

No active task. T-209 is locally complete and PR #35 passed its implementation
`Offline checks`; merge only after the closeout-only commit receives the same
required check.

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
| T-195–T-198 | Attack-surface hardening (`docs/security-threat-model.md`): repository controls `781e317`; reversible settings in `tools/out/t197-settings-rollback.md`; ruleset `19127356` requires one review with Repository-admin bypass (`3574f40`). |
| T-199 | Claude benchmark: 72/75 strict; all 14 repeats passed. Evidence: `tools/agent-benchmark/claude-full-20260718.summary.md`. |
| T-200 | Security proposals: HSTS `max-age` raised 1 day → 1 year, **deployed and verified live** (max-age=31536000, HTTP→HTTPS intact). Org `default_repository_permission` change **declined** (org-wide 100+ repos; T-198 gate suffices). |
| T-201 | Merged the GPT-5.6 and Claude README benchmark tables into one section (unified 6-model table + side-by-side per-effort comparison; token caveat kept). |
| T-202 | Fixed the deploy deletion guard (`439ef4d`): it mis-read SFTP in-place updates as unmatched deletions, blocking every real deploy since T-182. True deletion = removed-not-transferred; SFTP-format test added. Unblocked T-200. |
| T-203 | Pruned 8 stale refs, one superseded branch, and 92 guarded disposable Claude artifact dirs; tracked evidence remained intact. |
| T-204 | Relocated Local to `~/projects/website`, preserving ignored/runtime state; offline and 38 browser checks passed before guarded old-checkout deletion. |
| T-205 | Reran GPT-5.6/Claude matrices and updated matched README results; evidence in `docs/audits/agent-benchmark-nightly-2026-07-24.md`. |
| T-206 | Moved Zhiyi Huang from the 24-person current-student table to Alumni on both mirrored member pages (`837cf9a`), preserved historical records, deployed the 166-file allowlisted snapshot with zero deletions, verified both live pages byte-identical, and passed the live security suite. |
| T-207 | Verified no-op hardening audit: live Actions are read-only/no-approve; Dependabot security updates, grouped monthly npm/Actions updates, secret scanning and push protection are enabled; ruleset `19127356` preserves one review, admin bypass, strict Offline checks, linear history, and resolved conversations. npm audit has zero findings; task-metrics, size, standards, security, supply-chain, workflow, and offline suites pass. The 8,316-byte ledger gate was resolved below the 8,000-byte budget; a closeout-order gate was resolved by restoring numeric index order. No website or deployment target changed. |
| T-208 | Removed only merged hardening/benchmark/ruleset task refs and the clean merged T-207 worktree; verified clean/current repository state and zero housekeeping residue. No site content or deployment changed. |
| T-209 | Updated exact `@playwright/test` and its supply-chain guard to 1.62.0 via PR #35. Online supply-chain, zero-vulnerability audit, offline security, 38 browser tests on local storage, and protected CI passed; unchanged 1.61.1 reproduced the candidate's NFS timeouts. No site content or deployment changed. |
