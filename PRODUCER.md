# Website producer queue

Read this after root instructions and before `TODO.md`. The producer normally
curates this file and `docs/producer/` to avoid conflicts. Consumers read the
first ready packet in priority/date order, then their board and record. If no
packet is ready, remain idle unless exceptional in-scope repair requires queue
work.

Next free ID: Web-224.

## Queue

| Task | State | Priority | Packet |
| --- | --- | ---: | --- |
| Web-213 | gated | 10 | `docs/producer/tasks/Web-213.md` |

## Writer contract

Consumers normally leave producer paths and durable-ID allocation to the
producer to avoid conflicts, but may perform either when necessary for an
in-scope solution under the same ledger and publication rules. They exhaust
safe work before reversible owner-choice parking and create receipts only for
durable terminal outcomes. Never delete or rewrite a terminal receipt.

Before publication run `python3 tools/producer-ledger.py validate` and the
role-aware advisory diff check. Immutable packets remain hard protected. The
index and selector are the sole current-disposition authority.
Owner-started nightly runs additionally follow `docs/producer/NIGHTLY.md`.
