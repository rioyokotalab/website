Update the existing Claude Code agent/MCP harness to add quota-aware routing
between GPT-5.3-Codex-Spark and GPT-5.6.

This is an implementation task, not a request for a design proposal. Inspect the
existing harness, make the smallest coherent changes that fit its architecture,
test them, and report the result. Do not assume filenames, directory layout, or
configuration mechanisms. After completing discovery, continue directly into
implementation unless an existing permission or approval boundary prevents it.

======================================================================
OBJECTIVE
======================================================================

Create these logical Codex workers:

1. codex-spark-low
   Preferred model: gpt-5.3-codex-spark
   Preferred reasoning effort: low
   Capacity pool: spark

2. codex-spark-medium
   Preferred model: gpt-5.3-codex-spark
   Preferred reasoning effort: medium
   Capacity pool: spark

3. codex-medium
   Preferred model: gpt-5.6-terra
   Preferred reasoning effort: medium
   Capacity pool: standard

4. codex-high
   Preferred model: gpt-5.6-sol
   Preferred reasoning effort: high
   Capacity pool: standard

The logical worker names should remain stable even when the underlying model
mapping changes later. Store model IDs and reasoning efforts in one authoritative
location rather than scattering them through prompts, scripts, and configuration
files.

Do not use gpt-5.3-codex for the standard workers. It is a deprecated target for
ChatGPT-authenticated Codex.

Do not invent a model named gpt-5.6-codex-spark. The current Spark target remains
gpt-5.3-codex-spark unless the installed Codex client itself reports a newer,
supported Spark replacement.

Use explicit model IDs such as gpt-5.6-terra and gpt-5.6-sol in durable
configuration. Use the moving gpt-5.6 alias only if the installed client accepts
the alias but not the explicit Sol ID, and document that behavior.

======================================================================
NON-NEGOTIABLE SAFETY RULES
======================================================================

Before changing anything:

- Record the current repository root and `git status --short`.
- Identify pre-existing staged, unstaged, and untracked changes.
- Never discard, overwrite, revert, or reformat unrelated user changes.
- Never use `git reset --hard`, destructive checkout commands, or `git clean`.
- Do not create or switch branches unless that is already the harness’s normal
  workflow.
- Preserve all existing sandboxing, permission gates, deployment protections,
  credential protections, and approval policies.
- Do not change authentication methods merely to make a model available.
- Do not expose, copy, rotate, or rewrite API keys, login tokens, or other secrets.
- Do not modify the global default Codex model unless the existing harness
  deliberately owns and manages that setting.
- When configuration is generated, edit the authoritative source and regenerate
  the derived files. Do not patch generated output as the primary fix.
- Do not remove existing agents or MCP definitions unless their behavior is
  demonstrably obsolete and fully replaced.
- Do not run duplicate write-capable agents concurrently against the same
  workspace.

======================================================================
PHASE 1: DISCOVER THE EXISTING ARCHITECTURE
======================================================================

Inspect the harness before deciding how to implement the change. Locate and trace:

- project-level and user-level Claude Code configuration relevant to this harness
- MCP server declarations
- custom agents, subagents, skills, hooks, commands, and router instructions
- Codex wrappers, profiles, aliases, adapters, and invocation helpers
- generated configuration and the source that generates it
- model-selection and reasoning-effort logic
- retry, escalation, fallback, and error-classification logic
- sandbox and approval-policy handling
- any current usage, quota, credit, or model-availability telemetry
- tests for routing, MCP configuration, or agent delegation
- documentation describing the harness architecture

Identify the single source of truth for each of these concerns:

1. logical worker definitions
2. model and reasoning-effort mapping
3. task classification
4. capacity-pool preference
5. retry and fallback behavior
6. delegation prompt construction

Avoid creating a second competing router or configuration system.

Provide a concise discovery summary during execution, then continue without
waiting for confirmation.

======================================================================
PHASE 2: VERIFY LOCAL CODEX CAPABILITIES
======================================================================

Determine the actual installed environment rather than assuming that current
public model names are usable on this account.

1. Check the installed Codex CLI version.

   GPT-5.6 requires Codex CLI 0.144.0 or newer.

2. Determine how this Codex installation is authenticated:

   - ChatGPT account authentication
   - API-key authentication
   - managed workspace authentication
   - another existing provider mechanism

   Preserve the existing authentication method.

3. If Codex CLI is older than 0.144.0:

   - determine how it was installed;
   - update only through the same established installation mechanism when that
     is permitted and safe;
   - do not replace package managers or authentication configuration;
   - if an approval boundary prevents updating it, leave the harness working and
     report the exact blocker.

4. Inspect the actual `codex mcp-server` tool schema with the mechanism supported
   by this installation, such as MCP `tools/list`.

   Confirm whether the `codex` tool accepts:

   - a per-call `model` override
   - a per-call `config` object
   - `model_reasoning_effort` through that config object
   - cwd, sandbox, and approval-policy fields used by the harness

5. Perform minimal, non-destructive availability probes for:

   - gpt-5.3-codex-spark with low effort
   - gpt-5.3-codex-spark with medium effort
   - gpt-5.6-terra with medium effort
   - gpt-5.6-sol with high effort

Use a temporary or harmless working directory, read-only sandboxing, and a very
small prompt. Do not edit project files during these probes.

Confirm model selection through request configuration, structured metadata,
client logs, traces, or other reliable evidence. Do not treat a model’s
self-reported identity as proof of which model ran.

For reasoning effort, distinguish between:

- verified effective through metadata or logs;
- accepted without a validation error but not independently observable;
- rejected or unsupported.

Record the exact error for any rejected model or effort.

6. Spark is a research-preview model and may not be available on this account.
   Failure to access Spark must not break the standard workers.

7. GPT-5.6 may still be rolling out. Use these compatibility rules:

   For codex-medium:
   - first choice: gpt-5.6-terra, medium
   - if Terra is unavailable but Sol is available: gpt-5.6-sol, medium
   - if no GPT-5.6 model is locally available: retain a supported standard model,
     preferring gpt-5.5 and then gpt-5.4, with medium effort
   - clearly report that the GPT-5.6 migration is incomplete rather than silently
     presenting the fallback as GPT-5.6

   For codex-high:
   - first choice: gpt-5.6-sol, high
   - if unavailable: gpt-5.5 high, then gpt-5.4 high
   - clearly report the effective fallback

8. Do not claim that Spark low and Spark medium are distinct unless both settings
   are accepted by the installed client.

   If Spark accepts only one usable effort configuration:

   - expose one truthful Spark worker rather than two misleading tiers;
   - route both low and routine-medium Spark task classes to that worker;
   - update the coordinator instructions accordingly;
   - document why the two requested Spark profiles were collapsed.

======================================================================
PHASE 3: CHOOSE THE LEAST FRAGILE MCP INTEGRATION
======================================================================

Prefer this architecture when the installed MCP schema and existing harness allow
it:

- one Codex MCP server process;
- logical worker definitions in the harness;
- per-call `model` override;
- per-call config override for `model_reasoning_effort`;
- existing per-call cwd, sandbox, and approval settings;
- one central model registry used by the router.

This is preferred over starting four nearly identical long-lived MCP server
processes.

Use separate MCP server entries, Codex profile files, or wrapper processes only
when one of these conditions is true:

- the existing harness intentionally represents every worker as a separately
  named MCP server;
- Claude Code cannot reliably provide per-call model or config overrides;
- the current adapter strips or rejects the nested config object;
- separate processes are required to preserve sandbox or permission boundaries.

When separate entries are necessary:

- follow the existing naming and generation conventions;
- avoid duplicate server names;
- avoid changing global Codex defaults;
- ensure each process receives the intended model and reasoning effort;
- keep authentication and permissions identical unless an existing policy
  requires otherwise;
- ensure startup and shutdown behavior does not leave stale MCP processes.

Do not introduce a second architecture merely because it is easier to add in
isolation.

======================================================================
PHASE 4: CENTRAL MODEL AND POOL DEFINITIONS
======================================================================

Create one authoritative logical mapping equivalent to:

codex-spark-low:
  pool: spark
  model: gpt-5.3-codex-spark
  effort: low

codex-spark-medium:
  pool: spark
  model: gpt-5.3-codex-spark
  effort: medium

codex-medium:
  pool: standard
  model: gpt-5.6-terra
  effort: medium

codex-high:
  pool: standard
  model: gpt-5.6-sol
  effort: high

Adapt this representation to the harness’s existing configuration language and
types. Do not introduce this exact syntax if the harness uses a different native
form.

Treat Spark and standard Codex as the two capacity pools.

Do not assume that Sol, Terra, and Luna have independent quota pools. They are
model choices inside the standard pool unless reliable local telemetry explicitly
shows otherwise.

Do not add GPT-5.6 Luna merely to create another apparent quota pool. Luna may be
useful in a future optimization, but it does not replace the separate Spark pool
objective.

======================================================================
PHASE 5: TASK CLASSIFICATION
======================================================================

Implement or update routing around three task classes.

----------------------------------------------------------------------
A. MECHANICAL-LOW
----------------------------------------------------------------------

Default target: codex-spark-low

Examples:

- repository search and symbol lookup
- file and directory inventory
- occurrence counting and grep-like checks
- exact text replacement
- formatting-only or lint-only fixes
- localized renaming with an explicit mapping
- simple documentation synchronization
- short log summarization
- read-only verification
- repetitive parity checks
- straightforward extraction or transformation
- checking whether specified files contain specified patterns

Requirements:

- the operation is already known;
- little diagnosis or judgment is required;
- the scope is bounded;
- success is directly verifiable.

Fallback:

- if Spark is unavailable or constrained, use codex-medium;
- do not escalate to codex-high merely because the task is repetitive or large.

----------------------------------------------------------------------
B. ROUTINE-MEDIUM
----------------------------------------------------------------------

Both codex-spark-medium and codex-medium are intentionally eligible.

Examples:

- a small or moderate feature with clear requirements
- a localized bug fix
- writing or updating tests
- a contained refactor
- changes across a small group of related files
- routine build-script or configuration changes
- a modest diff review
- a contained diagnostic task
- ordinary website maintenance
- an implementation with explicit acceptance criteria
- work whose result can be checked through tests, builds, diffs, or a specific
  command

Prefer codex-spark-medium when:

- the task is tightly bounded;
- rapid iteration is useful;
- the success criteria are explicit;
- the relevant context is limited;
- a failed attempt is inexpensive to inspect and hand off.

Prefer codex-medium when:

- the task spans a larger part of the repository;
- it requires more context or more tool calls;
- it crosses several files, packages, or subsystems;
- requirements contain ambiguity;
- the task is expected to run autonomously for longer;
- verification requires substantial testing or iteration;
- maintaining a longer chain of context matters;
- an unsuccessful first attempt would be costly.

The shared ROUTINE-MEDIUM class is the substitution boundary. Either medium
worker may perform tasks in this class when its pool is healthy and the task is
within its capability.

----------------------------------------------------------------------
C. COMPLEX-HIGH
----------------------------------------------------------------------

Default target: codex-high

Examples:

- architecture and system design
- subtle root-cause analysis
- concurrency and race conditions
- CUDA, MPI, NCCL, distributed systems, and performance engineering
- security-sensitive changes
- major migrations with uncertain requirements
- numerical or algorithmic correctness
- unfamiliar large codebases
- high-risk deployment or build-system changes
- failures unresolved after a competent medium-tier attempt
- changes where a plausible-looking error could cause significant damage

Do not downgrade these tasks to Spark merely because the standard pool is
constrained.

Do not use codex-high for mechanical work merely because it touches many files.

======================================================================
PHASE 6: QUOTA-AWARE POOL SELECTION
======================================================================

Support a simple logical preference with the harness’s existing configuration
mechanism:

- auto
- prefer-spark
- prefer-standard

Do not force a particular environment-variable or filename convention. Integrate
the setting into the harness’s existing user-configurable mechanism.

Selection priority must be:

1. an explicit per-task worker override, when supplied;
2. safety and capability requirements;
3. known pool availability;
4. configured pool preference;
5. default task-shape routing.

In auto mode, derive pool state only from trustworthy inputs, in this order:

1. reliable existing quota or usage telemetry;
2. an explicit user preference or administrative setting;
3. explicit rate-limit, quota, capacity, or model-unavailable errors observed
   during the current run;
4. unknown.

Do not fabricate remaining percentages.

Do not scrape a graphical usage page, parse unstable human-readable UI text, or
build a large quota-monitoring subsystem unless the harness already has a
supported telemetry integration.

If reliable numerical usage data already exists:

- use it through a small pool-health interface;
- preserve a configurable reserve rather than exhausting either pool;
- use the harness’s existing threshold convention;
- if no convention exists, use a conservative default reserve of 15 percent;
- document exactly which metric and reset window are being evaluated.

If reliable numerical data does not exist:

- retain manual prefer-spark and prefer-standard modes;
- use task shape for the initial automatic choice;
- perform reactive failover on explicit rate-limit or capacity errors;
- clearly document that the harness cannot proactively know that a pool is
  “close” to its limit.

Default automatic behavior when both pools are healthy or unknown:

- MECHANICAL-LOW: prefer Spark.
- tightly bounded ROUTINE-MEDIUM: prefer Spark.
- broader or context-heavy ROUTINE-MEDIUM: prefer standard.
- COMPLEX-HIGH: use standard high.

======================================================================
PHASE 7: FAILOVER AND CIRCUIT-BREAKER BEHAVIOR
======================================================================

Classify failures before changing workers.

A. Capacity failures include explicit evidence of:

- rate limit reached
- quota or usage allowance exhausted
- model at capacity
- model temporarily unavailable
- account not currently entitled to that model

B. Task failures include:

- incorrect reasoning
- incomplete implementation
- lost context
- failure to understand requirements
- uncertain correctness
- inability to diagnose the problem

C. Environment failures include:

- missing executable
- wrong cwd
- unavailable dependency
- malformed local configuration
- transient MCP transport failure
- a command rejected by the existing permission policy

Use these rules:

1. Spark capacity failure on a ROUTINE-MEDIUM task:
   - mark the Spark pool unavailable for the current orchestration run;
   - hand the task to codex-medium once.

2. Standard capacity failure on a ROUTINE-MEDIUM task:
   - if the task is genuinely Spark-suitable, mark the standard pool unavailable
     for the current orchestration run and hand it to codex-spark-medium once;
   - otherwise report the capacity blocker rather than forcing the task onto an
     unsuitable model.

3. Capacity failure on a COMPLEX-HIGH task:
   - do not downgrade it to Spark;
   - report the blocker with preserved diagnostic context.

4. Substantive Spark task failure:
   - escalate once to codex-medium;
   - do not submit the same materially unchanged prompt repeatedly to Spark.

5. Substantive codex-medium failure involving ambiguity, architectural risk, or
   uncertain correctness:
   - escalate once to codex-high.

6. Correctable environment failure:
   - correct the cause and retry the same worker at most once;
   - do not interpret an environment failure as evidence that a stronger model is
     required.

7. After an explicit capacity failure:
   - use an in-memory or run-scoped circuit breaker;
   - do not repeatedly probe the unavailable pool during the same task;
   - do not create an unbounded retry loop.

8. Allow at most one cross-pool failover for a single delegated task unless the
   existing harness already has a stricter bounded retry policy.

======================================================================
PHASE 8: SAFE HANDOFF BETWEEN WORKERS
======================================================================

Never launch both substitute workers as concurrent writers for the same task.

Before handing a failed or interrupted task to another worker:

1. inspect the current working tree;
2. determine whether the first worker changed files;
3. preserve all user-owned pre-existing changes;
4. distinguish completed edits from incomplete edits where possible;
5. prepare a concise handoff package containing:
   - original objective
   - acceptance criteria
   - files inspected
   - files changed
   - current diff summary
   - commands already run
   - test results
   - confirmed evidence
   - hypotheses not yet confirmed
   - exact failure or capacity error
   - remaining work

If the first worker made useful partial changes, ask the replacement worker to
continue from the current state and review those changes.

Do not automatically revert partial work unless:

- it is clearly attributable to the failed worker;
- it is clearly unusable;
- reverting it cannot affect pre-existing user changes;
- the existing harness already has a safe transaction or worktree mechanism.

If the harness supports isolated worktrees or transactional task workspaces,
reuse that mechanism rather than inventing a new one.

======================================================================
PHASE 9: DELEGATION CONTRACT
======================================================================

Every invocation of a Codex worker should receive, in the form already used by
the harness:

- exact task objective
- definition of done
- relevant cwd
- known files or directories
- allowed scope
- read-only versus write permission
- invariants and constraints
- required tests or verification commands
- actions requiring approval
- conditions under which the worker must stop rather than improvise

Require a concise structured result equivalent to:

status:
  success | partial | blocked | failed

summary:
  what was accomplished

changed_files:
  files modified, created, or deleted

commands:
  important commands run

verification:
  tests, builds, checks, and outcomes

evidence:
  confirmed observations separated from hypotheses

remaining:
  unresolved work, uncertainty, or blockers

Do not require this exact serialization if the harness already has a typed result
format. Extend or reuse the existing format.

======================================================================
PHASE 10: IMPLEMENTATION QUALITY
======================================================================

Keep the change small and maintainable.

- Reuse existing types, adapters, routers, and test helpers.
- Centralize model mappings.
- Avoid duplicated task lists for the two medium workers; define the shared
  ROUTINE-MEDIUM class once.
- Keep capability routing separate from pool-health routing.
- Keep error classification separate from task classification.
- Do not encode model IDs directly in many coordinator prompts.
- Preserve backward compatibility with existing agent names where practical.
- When an old name must change, provide an alias or migration path if the harness
  already supports aliases.
- Update nearby documentation that is genuinely part of operating the harness.
- Do not rewrite unrelated documentation or reformat unrelated configuration.

======================================================================
PHASE 11: VERIFICATION
======================================================================

Verify the completed implementation at several levels.

1. Configuration verification

   - all edited configuration parses successfully;
   - generated files match their sources;
   - no duplicate MCP names exist;
   - configuration precedence is understood;
   - existing agents and MCP servers still load.

2. MCP verification

   - the Codex MCP server starts successfully;
   - `tools/list` succeeds;
   - required model and config overrides are present or the chosen alternative
     mechanism is verified;
   - stale server processes are not masking the new configuration.

3. Profile verification

   Perform a minimal read-only smoke test for every distinct effective
   model/effort configuration.

   Verify the selected model from configuration or metadata, not model
   self-report.

4. Router verification

   Test or trace at least these cases:

   - mechanical task selects Spark low;
   - bounded routine task can select Spark medium;
   - broader routine task selects standard medium;
   - difficult task selects standard high;
   - prefer-spark affects an eligible routine task;
   - prefer-standard affects an eligible routine task;
   - simulated Spark rate-limit error fails over once to standard medium;
   - simulated standard rate-limit error fails over once to Spark only when the
     task is Spark-suitable;
   - high-risk task does not downgrade to Spark;
   - an environment error does not incorrectly trigger model escalation;
   - a substantive Spark failure escalates to standard medium;
   - repeated failures cannot create an unbounded retry loop.

   Simulate rate-limit responses through existing mocks, adapters, or test seams.
   Do not intentionally consume the user’s actual quota to test exhaustion.

5. Regression verification

   - run the existing harness tests relevant to the changed components;
   - run configuration validation, linting, and type checking where available;
   - confirm that unrelated agents still resolve and run;
   - inspect the final diff for unintended edits.

6. Reload verification

   Restart or reconnect only the processes required for the new definitions to
   take effect. Do not restart unrelated services.

======================================================================
DEFINITION OF DONE
======================================================================

The work is complete only when:

- the harness has truthful logical Spark-low, Spark-medium, standard-medium, and
  standard-high capabilities, or the report clearly explains why an unsupported
  Spark distinction was collapsed;
- GPT-5.6 Terra is used for standard medium when locally available;
- GPT-5.6 Sol is used for standard high when locally available;
- no standard worker still targets gpt-5.3-codex;
- Spark still targets the actually supported Spark model;
- model mappings are centralized;
- routine-medium tasks can use either Spark or standard capacity;
- capability suitability takes precedence over quota balancing;
- reliable quota data is used only when genuinely available;
- manual pool preference exists when automatic quota visibility is unavailable;
- explicit capacity failures trigger one bounded cross-pool failover;
- partial-work handoff is safe;
- high-risk tasks never silently downgrade to Spark;
- existing permissions and unrelated harness behavior remain intact;
- smoke tests and relevant regression tests pass.

======================================================================
FINAL REPORT
======================================================================

When finished, report:

1. the harness architecture and authoritative configuration points you found;
2. the original Codex CLI version and final version;
3. the authentication mode, without exposing credentials;
4. every file changed;
5. whether one MCP server with per-call overrides or multiple server/profile
   definitions was used, and why;
6. the exact effective model and reasoning effort for every logical worker;
7. which model/effort combinations were verified, merely accepted, rejected, or
   unavailable;
8. whether GPT-5.6 was available on this account;
9. how ROUTINE-MEDIUM task substitution works;
10. how pool health is determined;
11. whether proactive remaining-quota visibility exists;
12. how manual pool preference is configured;
13. the failover and circuit-breaker behavior;
14. tests and smoke checks run, with their outcomes;
15. processes restarted or reconnected;
16. any fallback model still in use and why;
17. remaining limitations or ambiguity;
18. concise relevant diff excerpts;
19. the safest rollback procedure.

Do not dump whole large files. Do not claim success for a model or reasoning effort
that was not actually accepted by the installed environment.
