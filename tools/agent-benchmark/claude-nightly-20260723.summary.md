# Agent matrix summary — claude-nightly-20260723-full

## Integrity and totals

- Exact grid: 75 cells (75 documented + 0 ultra).
- Runner identities: 75 matrix.
- Capability passes: 71/75; mean score: 99.09.
- Summed end-to-end time: 11,200,736 ms; worker time: 7,329,113 ms.
- Effective tokens: 9,848,624; monetary cost: unknown because no frozen price table was recorded.

## Quality-first Pareto routes

| Task | Route | Score | Total ms | Effective tokens | Tradeoff from faster route |
|---|---|---:|---:|---:|---|
| WBD-001 | claude-fable-5/low | 100 | 49,236 | 123,383 | fastest |
| WBD-001 | claude-opus-4-8/low | 100 | 77,805 | 122,340 | +28.569 s, -1043 tokens (36.51 tokens/s) |
| WBD-002 | claude-opus-4-8/low | 100 | 112,907 | 121,574 | fastest |
| WBD-003 | claude-sonnet-5/low | 100 | 45,536 | 43,320 | fastest |
| WBD-003 | claude-opus-4-8/medium | 100 | 75,363 | 38,639 | +29.827 s, -4681 tokens (156.94 tokens/s) |
| WBD-003 | claude-opus-4-8/low | 100 | 82,981 | 37,388 | +7.618 s, -1251 tokens (164.22 tokens/s) |
| WBD-004 | claude-sonnet-5/low | 100 | 54,129 | 153,494 | fastest |
| WBD-004 | claude-opus-4-8/high | 100 | 106,001 | 136,233 | +51.872 s, -17261 tokens (332.76 tokens/s) |
| WBD-004 | claude-opus-4-8/low | 100 | 115,384 | 133,662 | +9.383 s, -2571 tokens (274.01 tokens/s) |
| WBD-004 | claude-fable-5/medium | 100 | 120,459 | 129,411 | +5.075 s, -4251 tokens (837.64 tokens/s) |
| WBD-004 | claude-fable-5/low | 100 | 218,620 | 102,144 | +98.161 s, -27267 tokens (277.78 tokens/s) |
| WBD-005 | claude-sonnet-5/medium | 100 | 153,050 | 158,736 | fastest |
| WBD-005 | claude-fable-5/medium | 100 | 172,919 | 129,844 | +19.869 s, -28892 tokens (1454.12 tokens/s) |

## Aggregate by model

| Model | Passes | Full quality | Mean score | Normalized latency | Normalized tokens |
|---|---:|---:|---:|---:|---:|
| claude-fable-5 | 25/25 | 25/25 | 100 | 1.78× | 1.11× |
| claude-opus-4-8 | 23/25 | 23/25 | 99.2 | 1.84× | 1.08× |
| claude-sonnet-5 | 23/25 | 23/25 | 98.08 | 1.45× | 1.37× |

## Aggregate by effort

| Effort | Passes | Full quality | Mean score | Normalized latency | Normalized tokens |
|---|---:|---:|---:|---:|---:|
| high | 14/15 | 14/15 | 99.4 | 1.49× | 1.31× |
| low | 14/15 | 14/15 | 97.53 | 1.13× | 1.09× |
| max | 15/15 | 15/15 | 100 | 2.65× | 1.38× |
| medium | 15/15 | 15/15 | 100 | 1.3× | 1.17× |
| xhigh | 13/15 | 13/15 | 98.53 | 1.83× | 1.25× |

## Capability failures

- WBD-003 claude-opus-4-8/xhigh: score 89; failed:reject-first-focus.
- WBD-003 claude-sonnet-5/xhigh: score 89; failed:reject-first-focus.
- WBD-005 claude-opus-4-8/high: score 91; failed:js-reduced-zero.
- WBD-005 claude-sonnet-5/low: score 63; failed:js-reduced-zero, p2p-failed:npx playwright test tests/reduced-motion.spec.js tests/lightbox-accessibility.spec.js tests/runtime-health.spec.js.

## Interpretation

- Each matrix cell has one observation. Pareto routes are repeat candidates, not final medians.
- Aggregate latency/token ratios are normalized to each task's best full-quality cell; raw medians across heterogeneous tasks are not used for routing.
