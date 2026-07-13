# Current facts

- **GPT-5.6 campaign freeze:** run label `gpt56-full-20260713`, baseline
  `c4b0720`, full prompt, default inspection, runner-lite, P2P, task-specific
  timeouts, and deterministic task-blocked order. Deadline is
  2026-07-14T05:08+0900.
- **WBD-001 ultra preflight:** Luna, Terra, and Sol each passed at 100/100 with
  exact scope. Ultra is runtime-verified and present in the local benchmark and
  v2 metrics schemas.
- **WBD-003 documented block (single observations):** all 15 arms passed the
  capability gate; 14 scored 100. Sol/xhigh scored 89 after failing only
  `denied-default`. Terra/low was fastest (25,045 ms total); Sol/low used the
  fewest effective tokens (8,298). These are provisional until ultra and
  matched-repeat evidence are available.
- **WBD-001 complete matrix (single observations):** all 18 model/effort arms
  passed at 100. Terra/medium was fastest (39,270 ms total, 10,671 effective
  tokens); Luna/low used the fewest tokens (43,941 ms, 8,117 tokens). Those two
  are the only initial score/runtime/token Pareto routes and need matched
  repeats before selection.
