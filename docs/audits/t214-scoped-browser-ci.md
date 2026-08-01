# T-214 — Scope locked browser CI to relevant changes

## Outcome

Website PR #38 changed only `TODO.md`, passed the complete local offline suite,
and then waited 5m26s for the required hosted job. The hosted browser install
and run dominated that latency even though no deploy-included site byte,
browser test, dependency, workflow, or tool changed.

The required `Offline checks` job remains present for every pull request. It
still checks out complete history without persisted credentials, installs the
pinned transport dependency, and runs the full ledger, standards, security,
supply-chain, and static-site policy suite. A NUL-delimited, fail-closed path
classifier now skips only the locked browser dependency install and browser
run when every changed path is in the explicit ledger/documentation-only set.
All other changes—including workflows, tools, package files, tests, and public
site paths—run the locked browser gate.

Rename detection is disabled for classification so a move from a public path
into a documentation path exposes both the removed and added path and therefore
runs browser tests. Empty, malformed, absolute, parent-traversing, control-byte,
or non-UTF-8 input also runs browser tests. The classifier prints only the
boolean scope and path count; it never evaluates a path as shell text.

## Acceptance

- Documentation/ledger-only fixtures skip browser work.
- Public site, workflow, tool/test, malformed, and empty fixtures require it.
- Both browser steps are bound to the classifier output.
- The real workflow retains least privilege, pinned actions, no persisted
  credentials, and ignored npm lifecycle scripts.
- The complete offline suite passes before protected publication.
- No site content, deployment, hosting setting, required approval, or
  non-owner pull-request isolation changes.
