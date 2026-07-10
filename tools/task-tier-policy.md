# Codex Task Tier Policy

This table maps `task_type` to the default codex tier the orchestrator should choose before dispatch. It is refreshed from `tools/task-metrics.jsonl`.

## Architecture (2026-07-11)

Five logical codex workers are defined in `tools/codex-workers.json`, the single source of truth: `codex-spark-low` and `codex-spark-medium` use pool `spark`, model `gpt-5.3-codex-spark`, effort `low`/`medium`; `codex-medium` uses pool `standard`, model `gpt-5.6-terra`, effort `medium`; `codex-high` uses pool `standard`, model `gpt-5.6-sol`, effort `high`; `codex-low` is legacy, model `gpt-5.6-terra`, effort `low`, retiring at S13`.

Mandatory dispatch contract: codex mcp-server ignores startup model/effort; every codex call must pass per-call `model=<worker.model>` and `config={"model_reasoning_effort":<worker.effort>}` from the registry, plus `sandbox:"workspace-write"` for writes. Server names are routing labels only.

## Pool preference + status

```text
pool_preference: auto        # auto | prefer-spark | prefer-standard
spark_status: available      # available | unavailable (set unavailable on an explicit capacity/rate-limit error for the run)
```

No reliable numerical quota telemetry exists, so `auto` means task-shape routing plus reactive failover on explicit capacity errors only; proactive "pool nearly exhausted" detection is not possible today.

## Task classes -> default worker

- MECHANICAL-LOW -> `codex-spark-low`: `mechanical-edit`, `verify-parity`, `git-summary`, `deploy-publish` pre-checks, and parse/aggregate portions of `metadata-lookup`; network fetches stay in Claude Bash because codex sandbox has no network. Capacity fallback -> `codex-medium`; never escalate to high just for size.
- ROUTINE-MEDIUM -> substitution boundary: tightly-bounded, limited-context, cheap-retry work -> `codex-spark-medium`; broader, context-heavy, ambiguous, long-running work -> `codex-medium`. Covers heavier edit-script drafting, multi-file sweeps, and `other`.
- COMPLEX-HIGH -> `codex-high`: `content-draft`, `translation`, `exporter-logic`, `diagnosis`, `figure-production`, `config-edit`. Never downgraded to spark even under capacity pressure.

Note: historical medians predate the worker rename; `tier` in metrics now records worker names, while legacy `low`/`medium`/`high` remain in history.

| task_type | default_tier | median_duration_ms | success_rate | n_samples | last_updated |
| --- | --- | --- | --- | --- | --- |
| mechanical-edit | codex-spark-low | 357814.5 | 90% | 10 | 2026-07-11 |
| metadata-lookup | codex-spark-low | 120000 | 60% | 20 | 2026-07-11 |
| verify-parity | codex-spark-low | 57908 | 100% | 9 | 2026-07-11 |
| git-summary | codex-spark-low | 41025.5 | 100% | 14 | 2026-07-11 |
| deploy-publish | codex-spark-low | 29817 | 80% | 5 | 2026-07-11 |
| content-draft | codex-high | - | - | 0 | 2026-07-11 |
| translation | codex-high | - | - | 0 | 2026-07-11 |
| exporter-logic | codex-high | 224063 | 100% | 9 | 2026-07-11 |
| diagnosis | codex-high | 0 | 100% | 1 | 2026-07-11 |
| figure-production | codex-high | - | - | 0 | 2026-07-11 |
| config-edit | codex-high | 34209 | 100% | 15 | 2026-07-11 |
| other | codex-medium | 0 | 100% | 4 | 2026-07-11 |

Note: orchestrator picks the cheapest worker meeting the success bar; failover ladder is spark -> `codex-medium` -> `codex-high` -> Opus -> Fable, one hop per failure, max one cross-pool failover per task.
