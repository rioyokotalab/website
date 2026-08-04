# Producer and consumer execution

A ready packet grants bounded repository reads, edits, tests, and normal
protected publication, but no owner choice or external mutation. Exhaust every
safe work item before a reversible owner gate; publish the partial record, emit
one value-free report, and create no terminal receipt. Keep active records
within 900 words.

Validate managed reports and confirmations with `tools/consumer_protocol.py`.
Accepted with a new request ID is itself the continuation prompt without
waiting for another task-specific message. Accepted without one acknowledges a
terminal checkpoint and stops without action or another report. Confirmation
never broadens authority.

Use `python3 tools/consumer_validation.py --describe` for proportional checks.
Record-only work runs ledger, whitespace, and consumer-boundary checks;
implementation adds owning tests; publication, policy, validator, lifecycle,
safety, credential, external-write, or unknown changes require complete
validation. Reuse evidence only while bytes, environment, acceptance scope,
and owning checks remain exact. Before publication run
`python3 tools/producer-ledger.py check-consumer-diff --base origin/main`.
