# Lab website — task board

This is the authoritative cold-start queue. Read it with `AGENTS.md` and
`tools/state/session.md`, then read only the linked record for the first
executable task. Completed chronology is indexed by `docs/tasks/index.tsv`.
Next free ID: T-216.

## Active and pending queue

| Task | Phase | Record |
| --- | --- | --- |
| T-213 | pending the next material content/template change or bounded quarterly manual checkpoint | `docs/tasks/T-213.md` |

T-213 is local/manual and adds no recurring hosted workflow. It does not
authorize a site deployment by itself; publication remains part of the normal
site task that triggers the sample.

## Completed-task lookup

Use `docs/tasks/index.tsv` for completed work. The exact pre-compaction board
and its immutable Git anchors are preserved at
`docs/history/TODO-full-archive-2026-08-02.md`; do not load them during an
ordinary cold start.
