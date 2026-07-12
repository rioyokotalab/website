# Current facts

- **Codex benchmark telemetry (2026-07-13):** codex-cli 0.144.1 `codex exec --json` emits `input_tokens`, `cached_input_tokens`, `output_tokens`, and `reasoning_output_tokens` in the `turn.completed` event. Stdout JSONL and stderr must be stored separately because a successful telemetry probe also emitted a nonfatal shell-snapshot syntax error on stderr.
- **Local screenshot repeatability (2026-07-13):** three fresh Playwright 1.61.1 Chromium captures of the 390x844 English home page, with analytics rejected and animations disabled, were byte-identical (`sha256 cc5abd1e0a1a0e37b4f942d1b3d3c04efd88af82b62305741332766aade85c79`). Exact screenshots are viable only under the pinned local environment; computed geometry remains the cross-environment oracle.
