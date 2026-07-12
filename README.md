# YOKOTA Laboratory website

Source for <https://www.rio.scrc.iir.isct.ac.jp>. The site is hand-built static
HTML: there is no framework, package install, compilation, or generated public
tree. Files in the deployed set are served at the corresponding URL.

The public URL tree is intentionally frozen. Improvements should restyle or
edit pages in place, not move them. The `en/` and `jp/` HTML trees mirror one
another so the language switch can replace one prefix with the other.

## Repository map

| Path | Purpose |
| --- | --- |
| `en/`, `jp/` | Mirrored English and Japanese public pages. |
| `Templates/` | Dreamweaver-era page templates; keep site-wide markup in sync with them. |
| `style.css`, `js/`, `images/` | Shared public presentation and assets. Some English pages reuse assets under `jp/`. |
| `cv/` | Public `cv.pdf` plus repo-only TeX sources and build script. |
| `skills/` | Canonical playbooks for editing, parity, content, lookup, exporting, and publishing. |
| `tools/` | Cross-session ledger, exporters, checks, worker registry, metrics, and transient `out/` deliverables. |
| `CLAUDE.md`, `AGENTS.md` | Role-specific operating rules for Claude and Codex. |
| `publish.sh`, `deploy.sh` | Approval-gated publish pipeline and SFTP mirror implementation. |

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
5. Publish only after the user explicitly approves the reviewed change in the
   current conversation.

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
`tools/codex-log.md`. Hand-edit-only agent/config changes are prepared as full
proposals under `tools/out/`; see `skills/config-proposals.md` for the review
and apply contract.

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

Publishing is approval-gated. The complete edit, preview, approval, publish,
live-verification, and Git synchronization procedure is
`skills/publish-and-verify.md`. Codex does not run the publishing commands;
publishing is performed by the user or Claude's site-publisher after explicit
approval.

`deploy.sh` mirrors the deploy-included repository tree to the SFTP web root
with deletion. Its exclusions protect repository-only material from both
upload and remote deletion. They include `.git/`, `.agents/`, `.claude/`,
`.codex/`, `tools/`, `skills/`, the deployment scripts, agent/config docs,
and the CV sources. `README.md` is explicitly excluded by
`-x '^README\.md$'`, so this file is not part of the public website.

## Invariants

- Preserve every public path and EN/JP counterpart.
- Keep shared markup in `Templates/*.dwt` synchronized with pages.
- Preserve `.dont-remove-me` and never expose credentials or `.git`.
- Add `rel="noopener noreferrer"` to new `target="_blank"` links.
- Do not publish or push merely because an edit is complete; follow the
  approval and ownership rules in the role instructions and publish playbook.
