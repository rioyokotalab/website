# Codex Task Tier Policy

Maps `task_type` to the default codex worker the orchestrator chooses before dispatch. Refreshed from `tools/task-metrics.jsonl`. Dispatch mechanics: `skills/codex-dispatch.md`; full policy: `.claude/agents/codex-offload-policy.md`.

## Architecture (2026-07-11)

Five logical workers in `tools/codex-workers.json`, the single source of truth: `codex-spark-low` and `codex-spark-medium` (pool spark, model `gpt-5.3-codex-spark`, effort low/medium); `codex-medium` (standard, `gpt-5.6-terra`, medium); `codex-high` (standard, `gpt-5.6-sol`, high); `codex-low` (legacy, `gpt-5.6-terra`, low).

Mandatory dispatch contract: startup pins in .mcp.json are a safety net only; every codex call passes per-call `model=<worker.model>`, `config={"model_reasoning_effort":<worker.effort>}`, `sandbox:"danger-full-access"`, and approval policy `never`. Server names are routing labels only.

Network: generated MCP servers use `sandbox_mode="danger-full-access"`; web/metadata lookups run inside codex per `skills/web-lookup.md`, with Claude Bash curl as fallback and independent verification.

## Pool preference + status

```text
pool_preference: auto        # auto | prefer-spark | prefer-standard
spark_status: available      # available | unavailable (set unavailable on an explicit capacity/rate-limit error for the run)
```

No reliable numerical quota telemetry exists, so `auto` means task-shape routing plus reactive failover on explicit capacity errors only; proactive "pool nearly exhausted" detection is not possible today.

prefer-spark selects codex-spark-medium for an eligible, spark-suitable ROUTINE-MEDIUM task when the spark pool is available; prefer-standard selects codex-medium for an eligible ROUTINE-MEDIUM task when the standard pool is available. If the preferred pool is unavailable or unsuitable, fall back to the safety/capability and availability rules.

## Task classes -> default worker

- MECHANICAL-LOW -> `codex-spark-low`: `mechanical-edit`, `verify-parity`, `git-summary`, `deploy-publish` pre-checks, and `metadata-lookup` including direct network fetches per `skills/web-lookup.md`. Capacity fallback -> `codex-medium`; never escalate to high just for size.
- ROUTINE-MEDIUM -> substitution boundary: tightly-bounded, limited-context, cheap-retry work -> `codex-spark-medium`; broader, context-heavy, ambiguous, long-running work -> `codex-medium`. Covers heavier edit-script drafting, multi-file sweeps, and `other`. Per observed 2026-07-11 results, bounded well-specified `translation`/`content-draft` batches MAY be routed to `codex-medium`; keep scopes small — recorded failures were oversized scopes, cutoffs, and one unauthorized-apply overreach.
- COMPLEX-HIGH -> `codex-high`: house-style-critical `content-draft`, `translation` where nuance dominates, `exporter-logic`, `diagnosis`, `figure-production`, `config-edit`. Never downgraded to spark even under capacity pressure.

Note: historical medians predate the worker rename; `tier` in metrics records worker names, while legacy `low`/`medium`/`high` values remain in history. metadata-lookup success was depressed by pre-network-access sandbox DNS blocks; expect improvement now that codex fetches directly.

| task_type | default_tier | median_duration_ms | success_rate | n_samples | last_updated |
| --- | --- | --- | --- | --- | --- |
| mechanical-edit | codex-spark-low | 46427.5 | 94.44 | 18 | 2026-07-11 |
| metadata-lookup | codex-spark-low | 120000 | 63.64 | 22 | 2026-07-11 |
| verify-parity | codex-spark-low | 42500 | 95.00 | 20 | 2026-07-11 |
| git-summary | codex-spark-low | 37621 | 100.0 | 20 | 2026-07-11 |
| deploy-publish | codex-spark-low | 39895.5 | 92.86 | 14 | 2026-07-11 |
| content-draft | codex-high (codex-medium allowed when bounded) | 493734 | 75.00 | 8 | 2026-07-11 |
| translation | codex-high (codex-medium allowed when bounded) | 381715 | 100.0 | 2 | 2026-07-11 |
| exporter-logic | codex-high | 224063 | 100.0 | 11 | 2026-07-11 |
| diagnosis | codex-high | 165000 | 100.0 | 4 | 2026-07-11 |
| figure-production | codex-high | - | - | 0 | 2026-07-11 |
| config-edit | codex-high | 126741 | 100.00 | 33 | 2026-07-11 |
| other | shape-dependent (ROUTINE-MEDIUM) | 0 | 100.00 | 11 | 2026-07-11 |
| grant-extraction | codex-spark-low | 1206682 | 100.0 | 2 | 2026-07-12 |
| file-archive | codex-spark-low | 314702 | 100.0 | 1 | 2026-07-12 |
| file-archive-audit | codex-spark-low | 2197996 | 100.0 | 1 | 2026-07-12 |
| doi-verify | codex-spark-low | 10375 | 100.0 | 2 | 2026-07-12 |
| grant-project-match | codex-spark-low | 574470 | 100.0 | 2 | 2026-07-12 |
| tooling-fix | codex-spark-low | 22236 | 100.0 | 1 | 2026-07-12 |
| context-check | codex-spark-low | 12953 | 100.0 | 1 | 2026-07-12 |

Failover ladder: spark -> `codex-medium` -> `codex-high` -> Opus -> Fable, one hop per failure, max one cross-pool failover per task. A failed same-worker environment retry is terminal: record the error and report a blocker. After the final available escalation-ladder endpoint fails, report a blocker; do not restart the ladder. These limits are per task for the run and may not be reset by reclassifying or redispatching the same failure.

## Latency guardrails

- Cap a codex call at two lookup items, 2–4 drafting/edit-spec items, or one bounded file transformation. Split larger work into independent output files.
- At five minutes for a bounded medium/high call, return incremental partial results and re-dispatch the remainder; do not combine lookup, reconciliation, drafting, and edit-script generation in one call.
- Route mechanical edits, metric/todo maintenance, simple parse/count/aggregate work, and routine parity checks to `codex-spark-low`; use `codex-spark-medium` only for bounded moderate reasoning.
- Network lookups run inside codex (`skills/web-lookup.md`): <=2 sources per session; a DNS/HTTP failure is terminal for that provider in the session; record the source URL per resolved fact.
- Require DOI/unique-key targeting and EN/JP dry-run counts before multi-page writes. Allow one local and one live verification per committed batch unless new state or a mismatch appears.
- Record scope_items, network_needed, and retry_reason in each metric note (or future structured fields).
- gpt-5.3-codex-spark cannot accept image inputs; PDF fetches that require the web/browser tool (DNS-blocked hosts like anlp.jp, ipsj.ixsq.nii.ac.jp) must go to codex-medium (gpt-5.6-terra) or another vision-capable worker.
