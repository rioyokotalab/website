driver: codex
updated: 2026-07-15T05:30+0900
task: T-179 Recover untracked global/local agent configuration | idle
status: idle

## Now
- T-179 is complete. T-11 was reconstructed at commit `194fc04`; its later
  README preserves the exact Codex bootstrap and hook recipes. T-170–T-173's
  superseding portable/global layer is canonical in `~/harness`.
- Merged never/full-access and exact website trust into the mode-600 Codex
  config while preserving Sol/high and the existing home trust. Surviving
  Claude user/project state was inspected only through selected non-secret
  keys and left unchanged.
- Harness transaction `20260714T202625Z-3548153` created 17 missing links and
  retained eight Claude links. The repeated host plan is all-keep, doctor has
  zero failures, both manifest files are mode 600, and Codex/agent discovery
  each has seven linked skills.
- A fresh host-level, tool-free Codex process returned `GLOBAL_OK SKILL_OK` and
  reported Sol/high, approval never, and danger-full-access. The current app
  process retains its startup mounts/policy until restarted.
- The untracked pre-commit hook survived. Its Claude-size branch is obsolete
  after T-142 but inert for the current Codex-only tracked tree; repository
  policy forbids the agent from editing `.git`, so it was preserved.

## Working set
- Website ledger/report/metrics changes for T-179 only.
- Owner/global recovery paths are complete and independently validated.

## Open questions
- Product-managed policy may still override local never/full-access in some
  surfaces; the direct host CLI cold-start probe honored the recovered values.

## Awaiting user
- None.
