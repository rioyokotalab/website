# Agent matrix summary — claude-nightly-20260723-focused-wbd003

## Integrity and totals

- Exact grid: 2 cells (2 documented + 0 ultra).
- Runner identities: 2 matrix.
- Capability passes: 1/2; mean score: 94.5.
- Summed end-to-end time: 276,868 ms; worker time: 252,183 ms.
- Effective tokens: 107,631; monetary cost: unknown because no frozen price table was recorded.

## Quality-first Pareto routes

| Task | Route | Score | Total ms | Effective tokens | Tradeoff from faster route |
|---|---|---:|---:|---:|---|
| WBD-003 | claude-opus-4-8/xhigh | 100 | 162,690 | 50,111 | fastest |

## Aggregate by model

| Model | Passes | Full quality | Mean score | Normalized latency | Normalized tokens |
|---|---:|---:|---:|---:|---:|
| claude-opus-4-8 | 1/1 | 1/1 | 100 | 1.0× | 1.0× |
| claude-sonnet-5 | 0/1 | 0/1 | 89 | 0.0× | 0.0× |

## Aggregate by effort

| Effort | Passes | Full quality | Mean score | Normalized latency | Normalized tokens |
|---|---:|---:|---:|---:|---:|
| xhigh | 1/2 | 1/2 | 94.5 | 1.0× | 1.0× |

## Capability failures

- WBD-003 claude-sonnet-5/xhigh: score 89; failed:reject-first-focus.

## Interpretation

- Each matrix cell has one observation. Pareto routes are repeat candidates, not final medians.
- Aggregate latency/token ratios are normalized to each task's best full-quality cell; raw medians across heterogeneous tasks are not used for routing.
