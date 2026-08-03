# Website producer queue

Read this after root instructions and before `TODO.md`. Only the sole portfolio
producer may modify this file or `docs/producer/`. Consumers read the first
ready packet in priority/date order, then their own board and matching execution
record. If no packet is ready, remain idle.

Next free ID: Web-220.

## Queue

| Task | State | Priority | Packet |
| --- | --- | ---: | --- |
| Web-213 | gated | 10 | `docs/producer/tasks/Web-213.md` |

## Writer contract

Consumers never modify producer-owned paths or allocate durable IDs. They keep
execution state in `TODO.md`, `docs/tasks/`, and implementation files, and write
completion or blocking evidence under `docs/consumer/receipts/`. Nested in-scope
findings are handled LIFO inside the active task; out-of-scope or authority-gated
findings produce a blocked receipt, not a new goal.

Before publication run `python3 tools/producer-ledger.py validate` and the
role-appropriate diff check against the protected base.
Owner-started nightly runs additionally follow `docs/producer/NIGHTLY.md`.
