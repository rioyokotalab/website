# Agent matrix summary — claude-nightly-20260723-focused-wbd005

## Integrity and totals

- Exact grid: 1 cells (1 documented + 0 ultra).
- Runner identities: 1 matrix.
- Capability passes: 1/1; mean score: 100.
- Summed end-to-end time: 212,484 ms; worker time: 115,479 ms.
- Effective tokens: 53,700; monetary cost: unknown because no frozen price table was recorded.

## Quality-first Pareto routes

| Task | Route | Score | Total ms | Effective tokens | Tradeoff from faster route |
|---|---|---:|---:|---:|---|
| WBD-005 | claude-sonnet-5/low | 100 | 212,484 | 53,700 | fastest |

## Aggregate by model

| Model | Passes | Full quality | Mean score | Normalized latency | Normalized tokens |
|---|---:|---:|---:|---:|---:|
| claude-sonnet-5 | 1/1 | 1/1 | 100 | 1.0× | 1.0× |

## Aggregate by effort

| Effort | Passes | Full quality | Mean score | Normalized latency | Normalized tokens |
|---|---:|---:|---:|---:|---:|
| low | 1/1 | 1/1 | 100 | 1.0× | 1.0× |

## Capability failures

None.

## Interpretation

- Each matrix cell has one observation. Pareto routes are repeat candidates, not final medians.
- Aggregate latency/token ratios are normalized to each task's best full-quality cell; raw medians across heterogeneous tasks are not used for routing.
