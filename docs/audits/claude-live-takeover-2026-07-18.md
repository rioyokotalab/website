# Claude live takeover evaluation — 2026-07-18

## Scope

Website task T-189 established a repository-owned Claude entry point and then
ran three independent, non-persistent Claude Code 2.1.207 sessions from the
website checkout. No guidance, test, script, or runtime path imported or
invoked a sibling repository. Each session used the observed
`claude-sonnet-5` model at high effort, a dollar ceiling, bounded tools, and no
credential, SSH, deployment, or publication authority. The Codex DRIVER kept
ledger integration, Git publication, and independent review.

## Results

| Task | Authority | Result | Observed telemetry |
|---|---|---|---|
| Cold ledger reconstruction | Website repository reads only | Pass. Claude imported the shared project rules, found the freshly updated Codex-owned T-189 session, stayed in WORKER scope, and returned control without changing the ledger. | 36.928 s, 7 turns, $0.3017925 |
| Claude takeover technical audit | Website reads plus four exact local commands | Pass with GO. Focused takeover, repository-independence, and metrics selftests passed. Claude found one medium validation gap and one low wording inconsistency without attempting an unapproved command. | 141.298 s, 23 turns, $0.7509633 |
| Agent-metrics implementation | Edit only `tools/task-metrics.py`; two exact tests permitted | Pass. Claude made general row validation reject unsupported client names for both schema generations, added negative selftests, and ran both authorized checks successfully. | 53.480 s, 8 turns, $0.7470018 |

Total observed Claude-reported cost was $1.7997576. Cost, turn, and duration
figures are CLI telemetry for these exact sessions, not generalized performance
claims.

## Repository-owned handoff

- Root `CLAUDE.md` imports `AGENTS.md` and adds only Claude client mechanics.
- The shared ledger accepts `driver: codex` and `driver: claude`; the metrics
  helper records either client explicitly and validates that allowlist.
- Direct Codex and Claude DRIVER sessions share the same publication gates;
  every bounded WORKER remains unable to commit, push, or deploy.
- The complete offline suite runs `tools/test-claude-takeover.sh`, and the
  repository-independence scanner includes `CLAUDE.md`.
- Claude guidance has its own 4,000-byte size budget and is a regular tracked
  file, not an external symlink.

## Primary review

The primary agent inspected Claude's exact diff, confirmed all 230 existing
metrics rows use the supported `codex` client, and independently reran the
metrics selftest, full metrics validation, and focused takeover test. Claude's
low-severity wording finding was also corrected so the publish playbook's
WORKER prohibition is explicitly client-neutral and regression-tested.

The complete repository-owned offline suite passed, followed by all 38 locked
browser tests. No deploy-included file changed, so no deployment or live-site
operation was run. Claude was safer and more command-precise than the parallel
harness trial, but its broad technical audit was still inefficient at 23 turns
for a narrow configuration review.

An isolated local clone of the task commit then passed the focused takeover and
repository-independence tests with an unusable external-control command path.
A one-turn live Claude probe read only the clone's root guidance and returned
`WEBSITE_CLAUDE_IMPORT=pass`. The first guarded cleanup correctly refused while
the test shell's current directory was inside the target; retry from the parent
website checkout validated the manifest, deleted that exact temporary clone,
preserved protected anchors, and verified the target absent.
