# Codex Offload Policy

Shared standing policy for YOKOTA Lab website agents with codex MCP access. `tools/codex-workers.json` is the worker registry; `tools/task-tier-policy.md` is the task-routing policy. Dispatch mechanics are condensed in `skills/codex-dispatch.md`; this file is the full policy. Repo-root `skills/` holds the shared domain playbooks (index: `skills/README.md`).

## Default posture

- **OFFLOAD FIRST and MAXIMIZE offload.** Site-coordinator and every codex-enabled agent should offload bounded repository reading, parsing, counting, drafting, translation, analysis, lookup, citation/exporter reasoning, figure/script generation, and CRLF-safe edit-script drafting before consuming Claude context.
- Offload by default when work spans more than 2 files, about 100 lines, multiple pages, substantial HTML, or non-trivial drafting or reasoning. This applies to retries: narrow or fan out the work instead of repeating it in Claude context.
- Codex workers use `sandbox_mode="danger-full-access"` with `approval_policy="never"`; web/metadata lookups run inside codex following `skills/web-lookup.md`, with Claude Bash curl as fallback and independent verification.
- Pass file/URL pointers and skill paths, not copied payloads. Claude reads the resulting `tools/out/` file plus minimal spot checks and keeps its response short.
- Continuously identify work that can move from Claude to codex. Project config may be edited directly only when the current task explicitly scopes it; owner-scope config remains proposal-only unless the user authorizes the exact write.

## Codex-enabled agents

- site-checker, site-editor, site-author, site-coordinator, and site-rescue may use their granted codex MCP routing labels. site-coordinator may dispatch codex directly.
- site-publisher has no codex worker.
- MCP server names grant and route tools only; they do not select the model or reasoning effort.

## Logical workers (single source of truth)

Definitions come only from `tools/codex-workers.json`:

| Worker | Pool | Model | Effort | Status |
| --- | --- | --- | --- | --- |
| `codex-spark-low` | spark | `gpt-5.3-codex-spark` | low | active |
| `codex-spark-medium` | spark | `gpt-5.3-codex-spark` | medium | active |
| `codex-medium` | standard | `gpt-5.6-terra` | medium | active |
| `codex-high` | standard | `gpt-5.6-sol` | high | active |
| `codex-low` | standard | `gpt-5.6-terra` | low | legacy |

There are two capacity pools: **spark** and **standard**. `codex-low` is a legacy worker, not the default for a current task class. Update the registry first when worker definitions change.

## MANDATORY per-call dispatch contract

> **CRITICAL:** Verified 2026-07-11: codex mcp-server startup model/effort pins are a safety net only. Every codex call MUST explicitly pass the chosen registry entry's `model=<worker.model>` and `config={"model_reasoning_effort":<worker.effort>}`.

- A call to `mcp__codex-<name>__codex` without both per-call values silently uses the account-default model (`gpt-5.5`). Never rely on the server name to set a model. Server names are routing labels used for tool-granting only.
- Every call MUST pass `sandbox: "danger-full-access"` and approval policy
  `never`; per-call values override startup config. This avoids interactive
  approvals and workspace-sandbox failures, including git metadata writes.
- `cwd` should be `/home/rioyokota/website`.
- Before dispatch, resolve the logical worker in `tools/codex-workers.json`; do not copy a stale model/effort mapping from prose.

## Task classes and worker selection

The orchestrator chooses the logical worker before dispatch and records its name as `tier`. A worker must use exactly the dispatched model/effort contract; it must report failure rather than silently changing worker.

| Task type enum | Class | Default worker |
| --- | --- | --- |
| `mechanical-edit` | MECHANICAL-LOW | `codex-spark-low` |
| `metadata-lookup` (network-capable; sources and gates in `skills/web-lookup.md`) | MECHANICAL-LOW | `codex-spark-low` |
| `verify-parity` | MECHANICAL-LOW | `codex-spark-low` |
| `git-summary` | MECHANICAL-LOW | `codex-spark-low` |
| `deploy-publish` (pre-checks only; codex never publishes) | MECHANICAL-LOW | `codex-spark-low` |
| `other` | ROUTINE-MEDIUM | shape-dependent |
| `content-draft` | COMPLEX-HIGH | `codex-high` |
| `translation` | COMPLEX-HIGH | `codex-high` |
| `exporter-logic` | COMPLEX-HIGH | `codex-high` |
| `diagnosis` | COMPLEX-HIGH | `codex-high` |
| `figure-production` | COMPLEX-HIGH | `codex-high` |
| `config-edit` | COMPLEX-HIGH | `codex-high` |

- **MECHANICAL-LOW -> `codex-spark-low`:** deterministic, bounded mechanical work, including direct authorized network fetches. Size alone does not justify high.
- **ROUTINE-MEDIUM -> substitution boundary:** use `codex-spark-medium` for tightly bounded, limited-context, cheap-to-retry tasks; use `codex-medium` for broader, context-heavy, ambiguous, or long-running tasks. This class includes heavier edit-script drafting, multi-file sweeps, and `other`. Per observed 2026-07-11 results, the orchestrator MAY route bounded, well-specified `translation`/`content-draft` batches to `codex-medium`; keep scopes small — the recorded failures were oversized scopes, cutoffs, and one unauthorized-apply overreach.
- **COMPLEX-HIGH -> `codex-high`:** judgment-heavy classes default to `gpt-5.6-sol` at high effort to maximize offload. Never downgrade these tasks to spark because of capacity pressure.

The fixed task-type enum is: `mechanical-edit`, `content-draft`, `translation`, `metadata-lookup`, `verify-parity`, `git-summary`, `deploy-publish`, `exporter-logic`, `diagnosis`, `figure-production`, `config-edit`, `other`.

## Quota-aware pool selection

`tools/task-tier-policy.md` owns these run controls:

```text
pool_preference: auto        # auto | prefer-spark | prefer-standard
spark_status: available      # available | unavailable
```

- `auto` means task-shape routing followed by reactive failover only on an **explicit** capacity, rate-limit, or entitlement error.
- prefer-spark selects codex-spark-medium for an eligible, spark-suitable ROUTINE-MEDIUM task when the spark pool is available; prefer-standard selects codex-medium for an eligible ROUTINE-MEDIUM task when the standard pool is available. If the preferred pool is unavailable or unsuitable, fall back to the safety/capability and availability rules.
- There is no reliable numerical quota telemetry, so do not infer exhaustion or proactively reroute from latency or generic failures. If reliable telemetry becomes available, add a 15% reserve before routing against reported capacity.

## Failover and circuit breaker

Classify every failure **before** rerouting as `capacity`, `task`, or `environment`.

### Capacity failure

- On an explicit spark capacity/rate-limit/entitlement error, fail over once to `codex-medium`.
- On an explicit `codex-medium` capacity error, fail over once to `codex-spark-medium` only when the task is spark-suitable.
- COMPLEX-HIGH is never downgraded. If `codex-high` cannot run for capacity reasons, report a blocker for orchestrator action.
- Permit at most **one cross-pool failover per task**.
- Run-scoped circuit breaker: after a pool returns an explicit capacity error, mark it unavailable for the run (`spark_status: unavailable` for spark) and do not probe it again during that run.

### Task failure

- Escalation ladder: `spark-*` -> `codex-medium` -> `codex-high` -> Opus -> Fable, exactly one hop per failure.
- Revise or narrow the task using the failure evidence at every hop. Never submit a materially unchanged failed prompt to spark again.
- A task failure is not evidence that the whole pool is unavailable.

### Environment failure

- Examples: missing binary, wrong `cwd`, missing `sandbox: "danger-full-access"`, bad path, or MCP transport failure.
- Fix the environmental cause and retry the **same worker once**. Do not treat an environment failure as model weakness or advance the task-failure ladder.

A failed same-worker environment retry is terminal: record the error and report a blocker. After the final available escalation-ladder endpoint fails, report a blocker; do not restart the ladder. These limits are per task for the run and may not be reset by reclassifying or redispatching the same failure.

## Safe handoff between workers

- Never run two write-capable workers concurrently on one task. Fan-out is allowed only for independent bounded subtasks with separate output files and non-overlapping write scopes.
- Before rerouting, inspect `git status`, preserve all user-owned and pre-existing changes, and identify any partial worker output.
- Never auto-revert or overwrite a failed worker's partial edits. Claude decides how to reconcile them.
- The task's `tools/out/` file is the handoff package. Append failure evidence, work completed, changed files, commands, and remaining work before the next worker starts.

## Fan-out

- When work decomposes into independent bounded subtasks, issue multiple appropriate codex calls in one turn rather than serial calls or extra Claude subagents.
- Prefer small parallel codex sessions: no more than 2 lookup items or about 2-4 other independent items per session. Each session gets pointers, its own `tools/out/` deliverable, the mandatory per-call contract, and a final self-log entry.
- Never fan out overlapping write scopes. The calling Claude agent aggregates output files and performs only minimal spot checks.

## Delegation form

Every prompt must include:

- calling agent and conversationId when available;
- task type enum, class, and chosen logical worker;
- concrete task, referenced paths/URLs, and acceptance criteria;
- the relevant `skills/*.md` paths the worker must read;
- output path under `tools/out/`;
- required sandbox mode; and
- reminder that the worker definition must be passed per call and the structured result block is mandatory.

Do not paste whole files, large snippets, or generated payloads into prompts; codex reads `AGENTS.md`, the named skills, and referenced repository files.

## Output-file-first

- The `tools/out/` file is the deliverable. Append resolved results immediately so partial progress survives cutoff; do not batch all findings at the end.
- For lookup/edit sessions, append each result as resolved and run `tail -1 <output-file>` before continuing. Keep lookup batches to no more than 2 items.
- Proposed scripts go to `tools/out/<task>.py`; Claude reviews and decides whether to execute them.
- Codex chat replies contain only the outcome and output path.

## Structured result block (mandatory)

Every codex `tools/out/` deliverable MUST end with this block, populated for that task:

```markdown
## Structured result

- status: success | partial | blocked | failed
- summary: ...
- changed_files: ...
- commands: ...
- verification: ...
- evidence:
  - confirmed: ...
  - hypotheses: ...
- remaining: ...
```

If more findings are appended later, move or repeat the updated block so it remains the final content.

## Apply-command duty

- For any proposed change to `.claude/agents/*.md`, `.mcp.json`, `AGENTS.md`, or `CLAUDE.md`, place the proposal under `tools/out/` and give the user an exact copy-paste `mv`/apply command. Never edit these hand-edit-only files directly.

## Logging and metrics

- As the **last action** of every delegated codex task, append to `tools/codex-log.md`:

```text
date | calling agent | task | output file | conversationId | outcome
```

- The calling agent relays the conversationId. site-checker is read-only, so the codex worker writes the log; site-editor/site-author may fill a missing line only if the worker could not.
- The orchestrator appends one `tools/task-metrics.jsonl` record per task and periodically refreshes `tools/task-tier-policy.md`:

```json
{"date":"...","task_type":"...","agent":"...","tier":"...","duration_ms":0,"success":true,"note":"..."}
```

## Claude verification

- The calling Claude agent confirms the output exists and is non-empty, reads it, and independently spot-checks at least one claim with minimal evidence before reporting success.
- Codex does not independently certify its own work. Claude reviews, decides, executes proposed scripts, verifies, and reports.
- The calling agent's final message stays near 15 lines and gives the outcome, changed/inspected paths, verification, and output pointers without pasting payloads.

## Facts, preferences, and verification gate

- **Facts vs preferences:** Never ask the user to confirm publicly-verifiable facts, including tool install/login commands, CLI/flag syntax, public API behavior, and library/version information. Verify them from authoritative sources instead. Codex workers have network access and fetch official documentation and authorized sources directly per `skills/web-lookup.md`; a network-capable Bash subagent (`site-checker` or `site-author`) remains available for independent checks. Escalate to the user only for personal preferences, private or credentialed values, or judgment decisions.
- **Independent verification gate:** Any worker output that will be committed, published, or presented to the user as fact must be independently verified before it is applied or reported. User-facing, committed, or factual results from `codex-spark-low` must be cross-checked by `codex-medium`. Factual external claims must also be verified against their authoritative source by an independent checker (another network-capable codex worker, or `site-checker`/`site-author` curl). Routine internal bookkeeping, including metrics, todo, and log appends, is exempt to avoid waste.
- Never surface an unverified external claim: verify it or omit it. When a codex worker emits content it could not verify, it must identify that content clearly under the structured result block's `evidence.hypotheses`; the orchestrator must verify it before use rather than asking the user.

## Division of labor and hard boundaries

- Codex generates, analyzes, parses, looks up, drafts content/translations/citations, reasons about exporter logic, produces figures or proposed scripts, and records evidence.
- Claude reviews, decides, executes scripts, reconciles partial edits, verifies, publishes, and reports.
- Codex never edits website pages directly unless a task explicitly authorizes that exact scope. Project config edits likewise require exact current-task scope; owner-scope config stays proposal-only unless explicitly authorized.
- Codex never publishes and never runs `publish.sh`, `deploy.sh`, `lftp`, `ssh`, or `git push`.
- Codex never touches credentials, `~/.ssh`, or `.dont-remove-me`; normal git metadata and explicitly scoped project config are allowed.

## Codex approval prompts (no per-prompt "don't ask again")

Codex shell-command approval requests ("MCP server codex-<tier> requests your input … Allow Codex to run …") are codex elicitations, NOT Claude Code's allow/deny system, so they offer only Accept/Decline with no persistence. Silence them via codex config, not by clicking:

- Global default: `~/.codex/config.toml` with `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`.
- Per call: dispatchers MUST pass approval policy `never` with `sandbox: "danger-full-access"`. Per-call values override config.toml; model/effort still come from per-call `model`/`config`.
