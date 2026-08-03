# Lab website — task board

This is the consumer-owned execution board. Read `PRODUCER.md` first, then its
first ready packet, this file, `tools/state/session.md`, and only the matching
execution record. If no producer packet is ready, remain idle. Completed
chronology is indexed by `docs/tasks/index.tsv`.
Current and future Website tasks use the `Web-NNN` namespace. Historical
`T-NNN` identifiers remain unchanged in completed records, metrics, and
archives.

## Active and pending queue

| Task | Phase | Record |
| --- | --- | --- |
| Web-213 | pending the next material content/template change or bounded quarterly manual checkpoint | `docs/tasks/Web-213.md` |

Web-213 is local/manual and adds no recurring hosted workflow. It does not
authorize a site deployment by itself; publication remains part of the normal
site task that triggers the sample.

## Completed-task lookup

Use `docs/tasks/index.tsv` for completed work. The exact pre-compaction board
and its immutable Git anchors are preserved at
`docs/history/TODO-full-archive-2026-08-02.md`; do not load them during an
ordinary cold start.
