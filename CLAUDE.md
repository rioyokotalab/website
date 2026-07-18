@AGENTS.md

# Claude client compatibility

- The imported repository rules are authoritative. References to Codex-only
  mechanics do not transfer automatically; use Claude's native tools while
  preserving the same DRIVER/WORKER, security, ledger, review, and publication
  boundaries.
- A Claude session started directly by the user is a DRIVER. Set
  `driver: claude`, use `--agent claude` when appending driver metrics, and log
  the final session as `claude-driver`. A bounded Claude dispatch is a WORKER
  and never edits the root session ledger, commits, pushes, or deploys.
- Claude child work uses the bounded scope and structured result contract in
  `skills/codex-delegation.md`, but no Codex model-routing claim applies unless
  the actual dispatch surface selected and reported that route.
- All project guidance, tests, and handoff state must resolve inside this
  repository. Do not import or invoke a sibling control repository.
