# Codex instructions — YOKOTA Lab website

Codex has two roles. A **WORKER** receives a bounded dispatch naming an output
file and scope; its caller owns integration and publication. A **DRIVER** is
started directly by the user and owns orchestration, ledger, verification, and
normal repository completion. If role is ambiguous, act as WORKER.

Codex injects this file into the turn. Do not spend a tool call printing it
again. Load task-specific playbooks and source ranges only when the prompt or
the work requires them.

## Security and authority

- WORKER: never run `publish.sh`, `deploy.sh`, `lftp`, `ssh`, or `git push`.
  Edit website files only when the dispatch explicitly authorizes exact scope;
  otherwise analyze and write the named `tools/out/` deliverable.
- Direct DRIVER: may run the repository publish pipeline and `git push` as the
  normal completion of user-requested repository changes, without a separate
  prompt, but must follow every gate in `skills/publish-and-verify.md`. Never
  force-push. Stop on a failed gate or material scope expansion.
- Never read, print, copy, or modify credentials, `~/.ssh`, or
  `.dont-remove-me`; never edit `.git` internals. Approved scripts may use
  configured authentication without Codex inspecting it. Never automate login
  UIs (researchmap and OpenReview block non-browser clients).
- Project config (`AGENTS.md`, `CLAUDE.md`, `.claude/`, `.mcp.json`) may be
  edited only when the current user task explicitly authorizes that scope.
  Owner-scope config remains proposal-only without exact external-write
  authorization.

## Context ledger

Canonical protocol: `skills/context-ledger.md`.

- DRIVER always reads `tools/todo.md` and `tools/state/session.md` at start. If
  the other driver updated an in-flight task within about one hour, ask before
  takeover. DRIVER owns and checkpoints `session.md` at task start, each
  completed step/failure, before risky or long work, and session end.
- WORKER never edits `session.md`. For a continuation or ledger task, read the
  cited task, prior output, and cited state paths. A self-contained isolated
  dispatch with complete scope (including benchmark capsules) need not read the
  unrelated global board/session. Never rely on chat memory.
- Durable state is ledger + `tools/out/` + commits. Keep prompts as pointers;
  do not copy file payloads into handoffs.

## Driver workflow

1. Reconstruct state from the ledger and set `driver: codex`.
2. Work in small verified steps. Delegate only bounded independent work when
   `skills/codex-delegation.md` predicts net context savings; default one and at
   most two disjoint subagents. Root owns review, decisions, ledger, config,
   commits, publish, and push.
3. Follow the relevant playbooks below. Preserve user changes and use normal
   non-destructive Git commands.
4. At session end update board/session, write
   `tools/out/driver-report-<YYYYMMDD-HHMM>.md`, append one metrics row per task
   attempted, and append the driver `tools/codex-log.md` line. Instrumented work
   uses schema v2 (`tools/task-metrics.schema.json`) and validates with
   `python3 tools/task-metrics.py validate`; unknown telemetry is null, not zero.

## Task playbooks

Read a playbook before work in its domain; do not load unrelated playbooks.

- `skills/html-editing.md` — CRLF-safe HTML, legacy tags, CSS cache versions
- `skills/en-jp-parity.md` — mirrored paths and translation conventions
- `skills/achievements.md` — achievement sections, ordering, data attributes
- `skills/news-and-members.md` — news/member/alumni rules
- `skills/web-lookup.md` — source lookup and verification limits
- `skills/exporters.md` — researchmap/ORCID/CV operations
- `skills/figures.md` — figure recipes
- `skills/codex-dispatch.md` — worker output/log contract
- `skills/codex-delegation.md` — native DRIVER delegation
- `skills/context-ledger.md` — state and handoff protocol
- `skills/publish-and-verify.md` — DRIVER publish/push gates
- `skills/config-proposals.md` — project/owner config scope and output lifecycle

## Site invariants

The site is static HTML served as-is; there is no build step.

- `en/` and `jp/` are mirrored. Apply and verify language parity.
- HTML is CRLF with legacy unclosed uppercase `<LI>`. For both reads and writes,
  scripts use `open(path, newline='', encoding='utf-8')`; parse tags
  case-insensitively (for example `re.split(r'<li[^>]*>', text, flags=re.I)`).
- Achievement rules live in `skills/achievements.md`; do not infer them from a
  nearby entry.
- `style.css` is shared and referenced with a dated cache query. New
  `target="_blank"` links require `rel="noopener noreferrer"`.
- Public trees are `en/`, `jp/`, `images/`, `js/`, `.htaccess`, root HTML,
  robots/sitemap/style, and `cv/cv.pdf`. Tools, skills, config, ledger, README,
  and CV sources are deploy-excluded.

## Network

Network is available with `danger-full-access` and approval policy `never`.
Follow `skills/web-lookup.md`: preferred structured/primary sources, no more
than two lookup items per session, a DNS/HTTP failure is terminal for that
provider in the session, source URL per resolved fact, and independent
verification before factual content is committed or published.

## Worker routing and call contract

Registry: `tools/codex-workers.json`; routing: `tools/task-tier-policy.md`.
Every dispatched call pins both `model=<worker.model>` and
`model_reasoning_effort=<worker.effort>`, uses `sandbox=danger-full-access`,
approval policy `never`, and cwd `/home/rioyokota/website`. Server names are
routing labels only. Use the selected route; report hard failure evidence rather
than silently changing model/effort.

## Worker output and handoff

- Work only in authorized scope. Write the named `tools/out/` deliverable
  incrementally when required; it ends with the `## Structured result` fields
  defined in `skills/codex-dispatch.md`.
- A short instrumented run may explicitly use runner-captured handoff. The
  runner retains raw JSONL, stderr, patch, grade, metrics, and a schema-validated
  final response and owns the log append; the worker does not load the dispatch
  playbook or edit `tools/out/`/`tools/codex-log.md`. Keep output-file-first for
  lookup, long, incremental, or interruption-prone work.
- Otherwise, the last delegated action appends exactly one newline-safe `tools/codex-log.md`
  line: `date | calling agent | task | output file | conversationId | outcome`.
- Never run concurrent writers on overlapping scope. Never revert, overwrite,
  or discard partial work to hide a conflict.
- The caller verifies the actual diff/evidence; a worker does not certify its
  own work. Preserve raw high-stakes command evidence and distinguish confirmed
  facts from hypotheses.
