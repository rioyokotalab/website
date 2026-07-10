# Codex Task Tier Policy

This table maps `task_type` to the default codex tier the orchestrator should choose before dispatch. It is refreshed from `tools/task-metrics.jsonl`.

| task_type | default_tier | median_duration_ms | success_rate | n_samples | last_updated |
| --- | --- | --- | --- | --- | --- |
| mechanical-edit | low | 420460 | 88% | 8 | 2026-07-10 |
| metadata-lookup | low | 180000.0 | 60% | 15 | 2026-07-10 |
| verify-parity | low | 119678 | 100% | 7 | 2026-07-10 |
| git-summary | low | 26173.0 | 100% | 4 | 2026-07-10 |
| deploy-publish | low | 37923 | 100% | 3 | 2026-07-10 |
| content-draft | high | - | - | 0 | - |
| translation | high | - | - | 0 | - |
| exporter-logic | high | 285507 | 100% | 3 | 2026-07-10 |
| diagnosis | high | - | 100% | 1 | 2026-07-10 |
| figure-production | high | - | - | 0 | - |
| config-edit | high | 900000 | 100% | 3 | 2026-07-10 |
| other | medium | - | 100% | 2 | 2026-07-10 |

Note: orchestrator prefers the LOWEST tier meeting the success bar while minimizing completion time; escalate low->medium->high on failure.
