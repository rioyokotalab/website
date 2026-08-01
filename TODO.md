# Lab website — task board

This is the authoritative resume point for the YOKOTA Lab website repository.
Protocol and schemas: `skills/context-ledger.md`; immediate execution state:
`tools/state/session.md`; durable choices: `tools/state/decisions.md`. Git
retains superseded chronology and command-level evidence — keep only current
state, active tasks, blockers, and compact historical pointers here. Next
free ID: T-215.

## Current state

- The repository and full history are public by owner instruction (T-192);
  every pushed tracked file is public. Secret scanning and push protection
  are enabled with zero alerts.
- `main` is protected by active ruleset `19127356`: pull request plus the
  required `Offline checks` CI run, strict current checks, linear history, and
  conversation resolution. Zero required approvals and the owner/admin bypass
  are the owner's later accepted policy; do not treat T-198's older one-review
  choice as a live drift or change it during hardening.
- The live pre-commit hook matches canonical `tools/hooks/pre-commit`;
  `tools/hook-doctor.sh` verifies/applies/rolls back through Git's common
  directory in both primary and linked worktrees (T-190, T-210).
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

T-212's worker-scoped portfolio review is published through PR #38 at
`3573e75`; no local worker handoff remains. T-214's scoped-browser change and
protected proof are published through PRs #39–#40 at `e22c8dc`: workflow-
changing CI passed in 5m02s, while documentation-only required gates passed in
23s and 25s with locked-browser setup/run skipped. Neither task deployed the
site or changed `tools/state/session.md`.

T-211 (2026-07-31 claude overnight audit) verified the full
offline suite, metrics, and hook state green on `9e1cd10` with no actionable
issue absent owner input.
No hosting-policy reconciliation is pending; required approvals remain zero.

## Active tasks

| Task | Phase | Durable pointer |
|---|---|---|
| T-213 | queued change-triggered accessibility and source-integrity sampling; local/manual, no added Actions | this board |

### T-213 acceptance

At the next material content/template change and at a bounded quarterly manual
checkpoint, sample representative EN/JP pages with keyboard and one assistive
technology, verify external factual links against primary sources, and record
only actionable regressions. Automated checks remain necessary but do not
claim full accessibility conformance. Do not add a recurring hosted workflow;
reuse the local offline/browser gates and publish only with a normal site task.
Use W3C's current [WCAG-EM 2.0](https://www.w3.org/TR/wcag-em-2/) sampling
method and [sustaining accessibility](https://www.w3.org/WAI/planning-and-managing/sustain/)
guidance rather than inventing a site-specific conformance claim.

## Completed-task lookup

Git history is the durable chronology; this board intentionally does not
duplicate it. Exact prior boards are available at these immutable anchors:

- pre-T-1–T-108: `986ed09:tools/todo.md`, `d44f862:tools/todo.md`, and
  `17b5eb8:tools/todo.md`;
- T-109–T-178: `d888cbc:tools/todo.md`, `d928540:tools/todo.md`, and
  `041a453:TODO.md`;
- T-179–T-189: `64c4b18:TODO.md` plus
  `docs/audits/claude-live-takeover-2026-07-18.md`;
- T-190–T-211: `736e14a:TODO.md`, with repository audit artifacts under
  `docs/audits/` and benchmark evidence under `tools/agent-benchmark/`.

Current operational invariants from those tasks are retained above. Consult
an anchored board only when a new task depends on that historical detail.

T-212 removed one stale 56.8 MB public staging root through a guarded manifest,
found no local historical branch or extra worktree, and passed the complete
offline security suite after compacting this ledger below its 8,000-byte gate.
T-214 scopes the locked browser install/run to changes outside the explicit
ledger/documentation-only set while keeping the required `Offline checks` job,
full local policy suite, untrusted-PR isolation, and fail-closed path handling;
evidence is in `docs/audits/t214-scoped-browser-ci.md`.
