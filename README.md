# YOKOTA Laboratory website

Source for <https://www.rio.scrc.iir.isct.ac.jp>. The site is hand-built static
HTML: there is no framework, package install, compilation, or generated public
tree. Files in the deployed set are served at the corresponding URL.

The public URL tree is intentionally frozen. Improvements should restyle or
edit pages in place, not move them. The `en/` and `jp/` HTML trees mirror one
another so the language switch can replace one prefix with the other.

## Quickstart: new lab-cluster account

These commands reproduce the verified CLI versions and repository settings
without copying credentials or account-private model defaults. GitHub write
access and web-server credentials are provisioned separately by the owner.
The install commands follow the current [Codex CLI](https://developers.openai.com/codex/cli/),
[Codex configuration](https://developers.openai.com/codex/config-basic), and
[Claude Code setup](https://docs.anthropic.com/en/docs/claude-code/setup)
documentation.

### 1. Install Node.js and Codex CLI

```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install 24.16.0
nvm alias default 24.16.0
npm install --global @openai/codex@0.144.1
```

### 2. Install Claude Code

```sh
curl -fsSL https://claude.ai/install.sh | bash
touch "$HOME/.bashrc"
grep -qxF 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc" || printf '%s\n' 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
export PATH="$HOME/.local/bin:$PATH"
claude install 2.1.207
```

### 3. Authenticate both CLIs

```sh
codex login --device-auth
claude auth login
```

### 4. Clone the repository

```sh
cd "$HOME"
git clone https://github.com/rioyokotalab/website.git
cd "$HOME/website"
```

### 5. Configure the direct Codex DRIVER

```sh
mkdir -p "$HOME/.codex"
printf '%s\n' 'approval_policy = "never"' 'sandbox_mode = "danger-full-access"' 'model_reasoning_effort = "medium"' '' "[projects.\"$PWD\"]" 'trust_level = "trusted"' > "$HOME/.codex/config.toml"
chmod 600 "$HOME/.codex/config.toml"
```

### 6. Register Claude's Codex workers for this account

```sh
python3 tools/gen-codex-mcp.py
sed -n '/^claude mcp add-json/p' tools/out/spark-apply-commands.sh | sh
rm -f tools/out/.mcp.json tools/out/spark-apply-commands.sh
python3 tools/gen-codex-mcp.py --check
```

### 7. Install the repository pre-commit checks

```sh
mkdir -p .git/hooks
printf '%s\n' '#!/bin/sh' 'if git diff --cached --name-only | grep -Fx "CLAUDE.md" >/dev/null; then' '    python3 tools/check-claude-size.py || exit 1' 'fi' '' 'python3 tools/check-md-size.py || exit 1' '' 'exit 0' > .git/hooks/pre-commit
chmod 755 .git/hooks/pre-commit
```

### 8. Verify the setup

```sh
claude --version
codex --version
claude auth status
codex login status
codex doctor --summary
claude mcp list
python3 tools/gen-codex-mcp.py --check
python3 tools/check-claude-size.py
python3 tools/check-md-size.py
git status --short
```

### 9. Start a driver

Claude DRIVER:

```sh
cd "$HOME/website"
claude
```

Codex DRIVER:

```sh
cd "$HOME/website"
codex
```

Local preview:

```sh
cd "$HOME/website"
python3 -m http.server 8000
```

### Browser consent regression tests

The site still has no build step. These commands install repo-only test
dependencies and a local Chromium build, then verify the bilingual privacy
banner and its pre-consent network boundary in a real browser:

```sh
npm ci
npm run test:consent:install
npm run test:consent
```

## Repository map

| Path | Purpose |
| --- | --- |
| `en/`, `jp/` | Mirrored English and Japanese public pages. |
| `style.css`, `js/`, `images/` | Shared public presentation and assets. Some English pages reuse assets under `jp/`. |
| `cv/` | Public `cv.pdf` plus repo-only TeX sources and build script. |
| `skills/` | Canonical playbooks for editing, parity, content, lookup, exporting, and publishing. |
| `tools/` | Cross-session ledger, exporters, checks, worker registry, metrics, and transient `out/` deliverables. |
| `CLAUDE.md`, `AGENTS.md` | Role-specific operating rules for Claude and Codex. |
| `publish.sh`, `deploy.sh` | Role-gated publish pipeline and SFTP mirror implementation. |

The authoritative playbook index is [`skills/README.md`](skills/README.md).
Read the skill for the area being changed before editing; the root README is
an orientation guide, not a replacement for those procedures.

## Working on the site

At the start of a driver session, read:

- `tools/todo.md` for active and blocked tasks;
- `tools/state/session.md` for the current handoff and next step;
- the relevant portions of `tools/state/facts.md` and
  `tools/state/decisions.md` when the task needs them.

Checkpoint in-flight work in `tools/state/session.md` according to
`skills/context-ledger.md`. Durable context belongs in the ledger or a task
deliverable, not only in chat.

For a normal page change:

1. Read `skills/html-editing.md`, `skills/en-jp-parity.md`, and any
   content-specific playbook.
2. Edit both language trees where applicable, preserve legacy HTML/CRLF
   conventions, and update the matching templates for site-wide markup.
3. Run the scoped parity and link checks described by the playbooks.
4. Preview locally and inspect both languages.
5. A directly user-started DRIVER publishes and pushes the completed change
   after every preflight gate passes; dispatched/MCP workers return evidence to
   their orchestrator and never publish or push.

There is no build step. A simple local preview from the repository root is:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000/jp/index.html> and the corresponding `/en/`
page.

## Agents and Codex delegation

Claude can coordinate the specialized site agents and dispatch bounded work to
the Codex worker registry in `tools/codex-workers.json`. Codex can also be
started directly as the repository driver. Both roles share the same ledger
and playbooks, so a handoff is reconstructed from disk rather than conversation
history.

Recurring worker routing and task metrics live in
`tools/task-tier-policy.md`, `tools/task-metrics.jsonl`, and
`tools/codex-log.md`. Project configuration changes require explicit task scope; owner-scope
configuration remains proposal-only unless the user authorizes the exact write.
See `skills/config-proposals.md` for the review contract.

A directly started Codex DRIVER may use native Codex subagents under
`skills/codex-delegation.md`. Delegation is reserved for bounded independent
work where minimal-context handoff saves more root context than it costs; the
root DRIVER retains ledger ownership, review, verification, and all publish or
push authority. Claude's `.claude/agents/` definitions remain Claude-specific.

## Exporters and derived records

`tools/` includes exporters for researchmap and ORCID plus checks for their
state. The detailed workflow is in `skills/exporters.md`. External account
updates, researchmap/ORCID operations, and CV PDF builds require the explicit
authorization described there; credentials and login UIs are never automated.

The context ledger separates current work by purpose:

- `tools/todo.md`: task board;
- `tools/state/session.md`: single in-flight handoff;
- `tools/state/facts.md`: verified current facts;
- `tools/state/decisions.md`: durable choices and rationale.

## Publishing and deployment boundary

Publishing is role- and preflight-gated. A directly user-started Claude or
Codex DRIVER has standing authority to publish and push completed
owner-requested repository changes without a separate permission prompt.
Dispatched/MCP Codex workers never publish or push; Claude may route an eligible
publish through its `site-publisher`. Blocked work, unrelated dirty files,
credentials, force operations, unexpected deploy changes, and material scope
expansion remain fail-closed. The complete procedure is
`skills/publish-and-verify.md`.

`deploy.sh` mirrors the deploy-included repository tree to the SFTP web root
with deletion. Its exclusions protect repository-only material from both
upload and remote deletion. They include `.git/`, `.agents/`, `.claude/`,
`.codex/`, local browser-test tooling and artifacts, `tools/`, `skills/`, the
deployment scripts, agent/config docs, and the CV sources. `README.md` is explicitly excluded by
`-x '^README\.md$'`, so this file is not part of the public website.

## Invariants

- Preserve every public path and EN/JP counterpart.
- Update shared navigation, header, and footer markup directly across all EN/JP
  pages with a CRLF-safe scripted replacement.
- Preserve `.dont-remove-me` and never expose credentials or `.git`.
- Add `rel="noopener noreferrer"` to new `target="_blank"` links.
- Publish/push only from an eligible direct DRIVER after the role, scope,
  verification, rebase, and deploy-dry-run gates in the publish playbook pass.
