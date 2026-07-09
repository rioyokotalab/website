# Codex Offload Policy

Shared standing policy for YOKOTA Lab website agents with codex MCP access.

## Codex-Enabled Agents

- site-checker, site-editor, site-author, site-coordinator, and site-rescue all have codex-low, codex-medium, and codex-high available.
- site-publisher -> NO codex tier.
- site-coordinator offloads directly to the tier chosen per the Tier Selection rule for bounded reading, parsing, drafting, translation, analysis, and edit-script drafting, not only by instructing subagents to offload.

## Tier Selection

- The ORCHESTRATOR chooses the codex tier (low|medium|high) per task from task type plus the policy table `tools/task-tier-policy.md`, and states it in the dispatch. The subagent uses EXACTLY that tier and does NOT override it; on hard failure it reports back and the orchestrator escalates low->medium->high, then Opus->Fable for persistent Claude-side bugs.
- Goal: minimize task completion time by using the cheapest/fastest effort that still succeeds for each task type, learned empirically from `tools/task-metrics.jsonl`.
- SEED DEFAULTS until data: mechanical-edit=low, metadata-lookup=low, verify-parity=low, git-summary=low, deploy-publish=low, content-draft=high, translation=high, exporter-logic=high, diagnosis=high, figure-production=high, config-edit=high, other=medium.
- TASK-TYPE ENUM: mechanical-edit, content-draft, translation, metadata-lookup, verify-parity, git-summary, deploy-publish, exporter-logic, diagnosis, figure-production, config-edit, other.
- METRICS DUTY: after each task the orchestrator appends one line to `tools/task-metrics.jsonl`:

```json
{"date","task_type","agent","tier","duration_ms","success","note"}
```

- The orchestrator periodically refreshes `tools/task-tier-policy.md` from `tools/task-metrics.jsonl`.

## Default Posture

- OFFLOAD FIRST.
- If a task involves reading more than 2 files, reading more than about 100 lines, site-wide or multi-page analysis, parsing substantial HTML, counting/parsing, generating substantial content, non-trivial drafting, translating, citation parsing, exporter reasoning, figure/script drafting, or drafting a CRLF-preserving edit script, delegate to the orchestrator-selected codex tier.
- This applies to retries too. If a first attempt is incomplete, narrow or fan out codex work; do not consume Claude context by doing the same bulk reading, parsing, drafting, or lookup work manually.
- Do not spend expensive Claude agent context doing bulk reading, counting, parsing, drafting, or first-pass reasoning when codex can read the repository itself. This applies to the site-coordinator directly as well as to codex-enabled subagents.
- The Claude agent reads the `tools/out/` deliverable plus minimal spot-check evidence, then keeps its reply short.

## Fan-Out Rule

- When a task decomposes into independent bounded subtasks, issue multiple `mcp__codex-<tier>__codex` calls in a SINGLE turn rather than doing them serially or spawning more Claude subagents.
- Prefer many parallel codex sessions over many Claude subagents. Fan out many parallel codex-low sessions for simple lookup/parse/aggregate work when the orchestrator-selected tier for that task type is low. Claude subagent capacity is scarce weekly-limited capacity; codex capacity is cheap and encouraged.
- Keep each codex session small enough to finish before cutoff. For lookup work, cap each session at <=2 items. For other bounded work, aim for <=2-4 independent items per session.
- Each codex session must receive pointers, not payloads; write its own `tools/out/` deliverable; append incrementally; and self-log one line to `tools/codex-log.md` as its last action.
- The calling Claude agent aggregates the `tools/out/` files plus minimal spot-checks and does not paste codex payloads into chat.

## Continuous Offload Improvement

- Continuously and frequently improve the configuration to offload as much work as possible from Claude to codex. On an ongoing basis, the coordinator should look for Claude-side work (reading, parsing, counting, drafting, translating, analysis, script-generation) that codex could do instead, and propose config updates (to `.claude/agents/*.md`, `AGENTS.md`, `CLAUDE.md`, `codex-offload-policy.md`) that push that work down to codex -- always delivered as `tools/out/` proposals with an exact copy-paste apply command.

## Delegation Form

- Pass pointers, not payloads.
- A codex prompt must include:
  - calling agent name;
  - task type from the Tier Selection enum;
  - orchestrator-selected codex tier;
  - concrete task;
  - file paths or URL pointers to inspect;
  - acceptance criteria;
  - output path under `tools/out/<task>.md` or `tools/out/<task>.py`;
  - conversationId from the caller when available.
- Never paste whole file contents, large snippets, or generated payloads into the codex prompt. codex reads `AGENTS.md` and the referenced files itself.

## Output-File-First

- The `tools/out/` file is the deliverable.
- codex must append each result to the output file immediately as it works; do not batch all findings until the end.
- Lookup/edit codex sessions must append each resolved result to their `tools/out/` file the instant it is resolved and run `tail -1 <output-file>` to confirm the write landed BEFORE moving on. Batching or end-of-run writes get lost on cutoff.
- Keep lookup batches to <=2 items.
- For scripts, codex writes the complete proposed script to `tools/out/<task>.py`; Claude reviews and runs it only if appropriate.
- codex final chat replies must be short: outcome plus output path.

## Apply-Command Duty

- When proposing changes to any hand-edit-only config file (.claude/agents/*.md, .mcp.json, AGENTS.md, CLAUDE.md), the agent MUST give the user an EXACT copy-paste shell command (mv/apply) to move the tools/out/ proposals into place. This apply-command duty is itself documented in the config files for high visibility.

## Logging

- As the LAST action of every delegated codex task, codex appends one line to `tools/codex-log.md`:

```text
date | calling agent | task | output file | conversationId | outcome
```

- The calling Claude agent relays the conversationId to codex.
- site-checker is read-only, so it does not write the log itself; codex writes the line.
- site-editor and site-author may write a log line themselves only when their delegated codex run did not or could not do it, and should say so in their report.

## Claude Verification

- After codex returns, the calling Claude agent reads only:
  - the codex output file;
  - minimal spot-check evidence, such as one or two grep/read/curl confirmations.
- The calling agent must confirm the output file exists and is non-empty.
- The calling agent must independently spot-check at least one codex claim before reporting PASS or success.
- codex never verifies its own work; site-checker or the calling Claude agent performs independent verification.

## Division Of Labor

- codex generates, analyzes, parses, drafts translations, drafts citations, reasons about exporter logic, and drafts edit scripts.
- Claude reviews, decides, executes edit scripts, verifies, and reports to the user.
- codex never edits website pages directly.
- codex never publishes.
- codex never touches credentials, `.ssh`, `.git`, `.claude`, `.mcp.json`, or `.dont-remove-me`.
- codex never runs `publish.sh`, `deploy.sh`, `lftp`, `ssh`, or `git push`.

## Calling-Agent Final Output

- The calling Claude agent's final message is capped at about 15 lines.
- It reports outcome, changed or inspected paths, verification result, and pointers to `tools/out/` files.
- It does not paste codex payloads into chat.
