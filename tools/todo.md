# Lab website — task board

Protocol and schemas: `skills/context-ledger.md`. In-flight detail:
`tools/state/session.md`. Next free id: T-145.

## Active

### T-143 — Remove Claude benchmark machinery and retained data

After T-142, remove Claude-only runners, profiles, results, exclusions, round
records, metrics/log rows, and retained artifacts. Preserve only provider-neutral
benchmark assets that still serve Codex, and document any shared-file rewrite
needed to keep schemas and validators coherent.

### T-144 — Remove residual references and prove a zero-trace current tree

After T-143, clean Claude/Anthropic/model-specific wording from skills,
documentation, ledger, logs, schemas, and scripts; run case-insensitive tracked
and ignored-tree scans plus repository regression gates. Historical Git commits
remain intact; no force-push or history rewrite.

## Blocked / awaiting user

None.

## Recently completed

- **T-142 — Remove Claude project and runtime configuration:** removed 20
  tracked runtime/config/registry/dispatch paths (74,489 bytes) plus the
  untracked project-local settings file; replaced root setup, AGENTS, delegation,
  ledger, config, lookup, and publish contracts with Codex-only versions; made
  the retained benchmark route self-contained. Selftest, five-capsule audit,
  Python compile, metrics validation, Markdown budgets, and diff checks pass.
- **T-141 — Decommission inventory and immediate cleanup:** mapped 47 tracked
  keyword-hit files (820,326 bytes) plus `.mcp.json`, classified T-142–T-144
  dependencies, removed 17 completed top-level scratch files (133,343 bytes),
  and compacted todo/facts/decisions from about 16 KB to about 3 KB. Raw
  pointer-backed artifact trees move atomically with their records in T-143.
- **T-109–T-140 — Benchmark program and comparison closeout:** completed and
  superseded by the T-141–T-144 decommission decision. Detailed chronology and
  raw conclusions remain available in Git history through `2a4a097`; transient
  outputs and current-tree comparison records are being removed incrementally.
