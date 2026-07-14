driver: codex
updated: 2026-07-14T14:32+0900
task: T-167 Resolve held metadata cases
status: in-progress

## Now
- T-169 has moved to `/home/rioyokota/harness/TODO.md` and is no longer owned
  by this repository's board.
- T-167 resumed at the user's request from the verified offline checkpoint.
  The offline gates pass: 16 exporter fixtures, the full security suite,
  metadata idempotence, 309-entry/30-source-row normalization, and CRLF
  preservation.
- The fresh live attempt retrieved data and then stopped safely on candidate
  drift for the 2014 WCCM entry: expected no candidate, found
  `published_papers:39797632`. The exact ResearchMap record and the university
  researcher profile both identify that proceedings work, so its reviewed
  override changed from `distinct` to an exact `match`; the later journal
  article remains separate. Re-run offline checks, then rebuild the live plan.
- The rebuilt plan and independent fresh-API audit pass: 251 operations (25
  inserts, 226 additive updates), zero deletes, zero unresolved ambiguities,
  and all 29 reviewed classifications applied. Managed-ID state is unchanged.
  The full security suite, 38 browser tests, metrics schema, metadata checks,
  normalization checks, and CRLF checks pass. Check remote state and deployment
  preview next; stop on any conflict, destructive preview, or auth failure.

## Working set
- `/home/rioyokota/harness/TODO.md` and `/home/rioyokota/harness/README.md`
- `/home/rioyokota/.bashrc` interactive-only system-completion guard; rollback
  copy in the private T-174 quarantine
- `~/.codex/AGENTS.md`, `~/.codex/rules/default.rules`,
  `~/.codex/skills/<personal>`, `$HOME/.agents/skills/<personal>`,
  `~/.claude/CLAUDE.md`, and `~/.claude/skills/<personal>` symlinks
- T-167 uncommitted files listed by Git plus
  `tools/researchmap-match-overrides.json`.
- `tools/out/researchmap-held-decisions-20260714.md`

## Open questions
- Five T-167 holds need human canonical-ID choices only if duplicate records
  should later be consolidated; their current operation-free state is safe.

## Awaiting user
- None.
