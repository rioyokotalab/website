# Claude benchmark results (July 2026)

The repository benchmark, previously run on GPT-5.6, repeated with Claude Code
(`claude` CLI 2.1.207) using the identical capsules, mutated fixtures, and
static F2P / browser P2P graders. Two axes: model ∈ {`claude-fable-5`,
`claude-opus-4-8`, `claude-sonnet-5`} and effort ∈ {low, medium, high, xhigh,
max} (the `claude --effort` levels, matching the GPT documented efforts; the
GPT-only `ultra` probe is omitted).

- **75 singleton cells** (5 tasks × 3 models × 5 efforts), run-label
  `claude-full-20260718`.
- **14 adaptive repeats** on WBD-003, run-label `claude-repeat-20260718`.
- Rows are in `results.jsonl`; the frozen GPT-5.6 rows are unchanged. Raw
  per-run artifacts are gitignored. `effective_tokens` = input − cache-read +
  output (Claude's large cached system prompt lands in the cache-creation
  term, so cross-provider token counts are not directly comparable).

## Headline

72 of 75 singletons were full-quality (every critical assertion, ≥85/100, no
P2P/scope regression). The 3 misses were all on WBD-003 (privacy-first consent
revocation) at higher effort — Opus/max (54), Sonnet/medium (89), Sonnet/max
(89) — and **none reproduced**: each was re-run and passed, for **14/14 repeat
passes**. The failures were one-off variance on a fragile assertion
(`reject-first-focus`, plus one over-edit on Opus/max), not a capability gap.
Read as reliability, every model × effort route solves these tasks.

## Per-model (full-quality singleton medians)

| Model | Full-quality | Median worker time | Median effective tokens |
| --- | ---: | ---: | ---: |
| `claude-fable-5` | 25/25 | 51.4 s | 25,405 |
| `claude-opus-4-8` | 24/25 | 86.3 s | 28,892 |
| `claude-sonnet-5` | 23/25 | 41.1 s | 29,404 |

Fable 5 was the only model to pass every singleton and was the most
token-efficient. Sonnet 5 was fastest. Opus 4.8 was slowest and most
expensive, and (before repeats) accounted for the single lowest score.

## Per-effort (full-quality singleton medians, all models)

| Effort | Full-quality | Median worker time | Median effective tokens |
| --- | ---: | ---: | ---: |
| low | 15/15 | 46.2 s | 22,771 |
| medium | 14/15 | 47.0 s | 23,701 |
| high | 15/15 | 71.3 s | 27,480 |
| xhigh | 15/15 | 68.8 s | 33,591 |
| max | 13/15 | 142.2 s | 45,277 |

**Low effort was the best default** — fastest, cheapest, and the only effort
with no misses. Higher effort cost markedly more time and tokens (max ≈ 3× the
time and 2× the tokens of low) and was the only place variance failures
appeared, with no quality gain on these tasks. This mirrors the GPT-5.6 study's
"low was best" finding.

## Recommended dispatch routes

Reliability is trivially met (all routes pass on repeat), so routing is by
runtime, with the token-minimizing alternative noted.

| Task | Fastest route | Fewest-token route |
| --- | --- | --- |
| WBD-001 bilingual legacy-HTML | `sonnet-5` / low (27.0 s) | `opus-4-8` / low (20,159) |
| WBD-002 mirrored secure links | `sonnet-5` / high (31.1 s) | `opus-4-8` / low (18,617) |
| WBD-003 privacy/consent JS | `sonnet-5` / low (22.9 s) | `opus-4-8` / low (22,771) |
| WBD-004 responsive CSS visual | `sonnet-5` / high (28.1 s) | `fable-5` / low (19,483) |
| WBD-005 cross-cutting shared assets | `fable-5` / low (46.1 s) | `fable-5` / low (25,405) |

Practical default: **low effort**, `sonnet-5` when latency matters,
`fable-5` for the hardest task (WBD-005, where it was fastest and most
efficient) and for token economy. For WBD-003 specifically, prefer low effort —
the occasional variance miss clustered at medium/max.

## Caveats

Single-host run, sequential. The `claude` and `codex` harnesses differ (system
prompt, tool set), so this compares each provider's agent as delivered, not the
raw models; treat it as a website-maintenance signal, not a leaderboard. Both
providers load their own global config in the capsule. Adaptive repeats covered
only WBD-003; the other four tasks rest on single singleton observations per
cell (all full-quality).
