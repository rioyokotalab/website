driver: codex
updated: 2026-07-15T07:10+0900
task: T-180 Exhaustive Git recovery audit | idle
status: idle

## Now
- T-180 is complete. All website recovery classifications are consolidated in
  `TODO.md`; harness T-172 owns the authoritative cross-repository table and
  execution order.
- No Git object warrants restoration. The eight damaged website paths are
  exact, and all unreachable objects are pre-incident superseded state.
- Harness T-174, T-173, T-170, and T-175 are the next execution sequence; the
  website has no active implementation task.

## Working set
- `TODO.md`, `tools/state/session.md`, and the harness `TODO.md`; no public-site
  file changed.

## Open questions
- The full local security suite still cannot start its lftp-backed deployment
  policy fixture. Harness T-175 owns the missing reproducible lftp path; no
  network or deployment ran.

## Awaiting user
- None.
