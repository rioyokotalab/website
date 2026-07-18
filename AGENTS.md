# Agent instructions — YOKOTA Lab website

Codex and Claude share two roles. A **WORKER** receives a bounded dispatch
naming an output file and scope; its caller owns integration and publication.
A **DRIVER** is started directly by the user and owns orchestration, ledger,
verification, and normal repository completion. If role is ambiguous, act as
WORKER.

Codex reads this file directly; Claude imports it through root `CLAUDE.md`.
Do not spend a tool call printing it again. Load task-specific playbooks and
source ranges only when required.

## Security and authority

- WORKER: never run `publish.sh`, `deploy.sh`, `lftp`, `ssh`, or `git push`.
  Edit website files only when the dispatch explicitly authorizes exact scope;
  otherwise analyze and write the named `tools/out/` deliverable.
- Direct DRIVER: may run the repository publish pipeline and `git push` as the
  normal completion of user-requested repository changes, but must follow every
  gate in `skills/publish-and-verify.md`. Never force-push. Stop on a failed
  gate or material scope expansion.
- Never read, print, copy, or modify credentials, `~/.ssh`, or
  `.dont-remove-me`; never edit `.git` internals. Approved scripts may use
  configured authentication without Codex inspecting it. Never automate login
  UIs.
- Project config (`AGENTS.md`) may be edited only when the current user task
  explicitly authorizes that scope. Owner-scope config remains proposal-only
  without exact external-write authorization.

## Context ledger

Canonical protocol: `skills/context-ledger.md`.

- DRIVER always reads `TODO.md` and `tools/state/session.md` at start. If
  another driver updated an in-flight task within about one hour, ask before
  takeover. DRIVER owns and checkpoints `session.md` at task start, each
  completed step/failure, before risky or long work, and session end.
- WORKER never edits `session.md`. For a continuation or ledger task, read the
  cited task, prior output, and cited state paths. A self-contained isolated
  dispatch with complete scope need not read the unrelated global board.
- Durable state is ledger + `tools/out/` + commits. Keep prompts as pointers;
  do not copy file payloads into handoffs.

## Driver workflow

1. Reconstruct state from the ledger and set `driver:` to the active client,
   `codex` or `claude`.
2. Work in small verified steps. Delegate only bounded independent work when
   the client-native delegation route predicts net context savings; default
   one and at most two disjoint subagents. Codex routing is documented in
   `skills/codex-delegation.md`; Claude uses the equivalent authority and
   handoff contract in `CLAUDE.md`. Root owns review, decisions, ledger,
   config, commits, publishing, and push.
3. Follow the relevant playbooks below. Preserve user changes and use normal
   non-destructive Git commands.
4. At session end update board/session, write
   `tools/out/driver-report-<YYYYMMDD-HHMM>.md`, append one metrics row per task
   attempted, and append the driver `tools/codex-log.md` line. Instrumented
   work uses schema v2 (`tools/task-metrics.schema.json`) and validates with
   `python3 tools/task-metrics.py validate`; unknown telemetry is null, not
   zero.

## Task playbooks

Read a playbook before work in its domain; do not load unrelated playbooks.

- `skills/html-editing.md` — CRLF-safe HTML, legacy tags, CSS cache versions
- `skills/en-jp-parity.md` — mirrored paths and translation conventions
- `skills/achievements.md` — achievement sections, ordering, data attributes
- `skills/news-and-members.md` — news/member/alumni rules
- `skills/web-lookup.md` — source lookup and verification limits
- `skills/exporters.md` — researchmap/ORCID/CV operations
- `skills/figures.md` — figure recipes
- `skills/codex-delegation.md` — native delegation and worker handoff contract
- `skills/context-ledger.md` — state and handoff protocol
- `skills/publish-and-verify.md` — DRIVER publish/push gates
- `skills/config-proposals.md` — project/owner config scope and output lifecycle

## Site invariants

The site is static HTML served as-is; there is no build step.

- `en/` and `jp/` are mirrored. Apply and verify language parity.
- HTML is CRLF with legacy unclosed uppercase `<LI>`. For both reads and writes,
  scripts use `open(path, newline='', encoding='utf-8')`; parse tags
  case-insensitively.
- Achievement rules live in `skills/achievements.md`; do not infer them from a
  nearby entry.
- `style.css` is shared and referenced with a dated cache query. New
  `target="_blank"` links require `rel="noopener noreferrer"`.
- Public trees are `en/`, `jp/`, `images/`, `js/`, `.htaccess`, root HTML,
  robots/sitemap/style, and `cv/cv.pdf`. Tools, skills, config, ledger, README,
  and CV sources are deploy-excluded.

## Network

Network is available with `danger-full-access` and approval policy `never`.
Follow `skills/web-lookup.md`: prefer structured primary sources, use no more
than two lookup items per session, treat a DNS/HTTP failure as terminal for that
provider in the session, record a source URL per resolved fact, and verify
independently before factual content is committed or published.

## Worker output and handoff

- For an explicit local text edit in a large file, locate the most
  task-specific literal with `rg` and inspect no more than 40 surrounding
  lines. Reference-driven visual work and diagnosis require broader inspection.
- Work only in authorized scope. Write the named `tools/out/` deliverable
  incrementally when required; it ends with the `## Structured result` fields
  defined in `skills/codex-delegation.md`.
- A short instrumented run may explicitly use runner-captured handoff. Prefer
  schema-free output when independent grader/runner artifacts are authoritative.
- Otherwise, the last delegated action appends exactly one newline-safe
  `tools/codex-log.md` line:
  `date | calling agent | task | output file | conversationId | outcome`.
- Never run concurrent writers on overlapping scope. Never revert, overwrite,
  or discard partial work to hide a conflict.
- The caller verifies the actual diff/evidence; a worker does not certify its
  own work. Preserve raw high-stakes command evidence and distinguish confirmed
  facts from hypotheses.
