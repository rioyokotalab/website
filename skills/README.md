# Skills — repository playbooks

Keep one canonical copy of each recurring procedure. Codex and Claude read only
the playbooks matching the task; dispatches cite paths instead of restating
rules.

Skills are tracked and deploy-excluded. Update the matching skill whenever a
convention changes.

These files remain repository-local and self-contained. Personal defaults and
cross-project workflows live outside the repository in `~/.codex/AGENTS.md`
and user skills; this project must not depend on that private layer. The local
ledger, delegation, lookup, and configuration playbooks deliberately retain
website-specific paths, limits, benchmark routing, and authority gates even
when a more general personal skill exists.

| Skill | Use when |
| --- | --- |
| `html-editing.md` | page HTML, CSS, or template edits |
| `en-jp-parity.md` | bilingual content or parity checks |
| `achievements.md` | achievement entries and citations |
| `news-and-members.md` | news, members, and alumni |
| `web-lookup.md` | external factual lookup |
| `codex-delegation.md` | native subagent dispatch and handoff |
| `context-ledger.md` | session checkpoints and durable state |
| `publish-and-verify.md` | preview, push, publish, and live verification |
| `config-proposals.md` | project config, owner proposals, output lifecycle |
| `exporters.md` | researchmap, ORCID, and CV operations |
| `figures.md` | research-page figure production |

For normal site edits, start with `html-editing.md` and `en-jp-parity.md`, then
load only the content-specific procedures needed by the task.
