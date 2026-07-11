# Skills — shared playbooks for Claude agents and codex workers

One canonical copy of every recurring procedure. Claude agents `Read` the
skill files matching the task before acting; codex workers read the same
files when the task or AGENTS.md points to them. Dispatches cite skill paths
(e.g. "apply skills/html-editing.md") instead of restating rules.

Repo-only: `skills/` is excluded from deploy (`deploy.sh -x '^skills/'`).
Skills are normal git-tracked files, NOT hand-edit-only: when a convention
changes, update the matching skill in the same change set.

| Skill | Use when |
| --- | --- |
| html-editing.md | any edit to page HTML, CSS, or templates |
| en-jp-parity.md | any content change, translation, or parity check |
| achievements.md | achievements entries, data-* attributes, citations |
| news-and-members.md | news items, member add/remove, alumni |
| web-lookup.md | any network lookup (Crossref, DBLP, arXiv, J-STAGE, ...) |
| codex-dispatch.md | every codex delegation (contract, output, logging) |
publish-and-verify.md | preview, publish approval, live verify, deploy auth |
| config-proposals.md | hand-edit-only config changes, tools/out lifecycle |
| settings-scope.md | placing Claude Code settings across user/project/local scopes |
| exporters.md | researchmap / ORCID / cv.tex sync and exports |
| figures.md | figure production for research pages |

Default skills per agent (read the ones the task touches):
- site-editor: html-editing, en-jp-parity, achievements, news-and-members, codex-dispatch
- site-checker: en-jp-parity, web-lookup, publish-and-verify, codex-dispatch
- site-author: achievements, news-and-members, en-jp-parity, web-lookup, exporters, figures, codex-dispatch
- site-publisher: publish-and-verify
- site-coordinator / site-rescue: codex-dispatch, config-proposals, plus whatever the task touches
