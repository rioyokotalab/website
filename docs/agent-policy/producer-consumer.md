# Producer and consumer execution

Producer and consumer DRIVERs are trust-equivalent repository agents. Roles
coordinate queue curation and execution rather than permission. A consumer
normally leaves producer paths and IDs to the producer, but may change or
allocate them when necessary for an in-scope solution after fetching, checking
overlap, recording the reason, and preserving every ledger invariant.

A ready packet grants bounded repository reads, edits, tests, and normal
protected publication, but no owner choice or external mutation. Exhaust every
safe work item before a reversible owner gate; publish the partial record, emit
one value-free report, and create no terminal receipt. Keep active records
within 900 words.

Managed reports and confirmations are optional coordination and review, not an
authorization source or consumer-only gate. When used, validate them with
`tools/consumer_protocol.py`.
Accepted with a new request ID is itself the continuation prompt without
waiting for another task-specific message. Accepted without one acknowledges a
terminal checkpoint and stops without action or another report. Confirmation
never broadens authority.

Use `python3 tools/consumer_validation.py --describe` for proportional checks.
Record-only work runs ledger, whitespace, and role-advisory checks;
implementation adds owning tests; publication, policy, validator, lifecycle,
safety, credential, external-write, or unknown changes require complete
validation. Reuse evidence only while bytes, environment, acceptance scope,
and owning checks remain exact. Role overlap emits an advisory; immutable
packets and ledger validation remain hard gates.
For compatibility, run `python3 tools/producer-ledger.py check-consumer-diff --base origin/main`;
role overlap does not fail it.

Owner authorization has no magic phrase. Unambiguous plain-language approval
of the immediately preceding bounded proposal is sufficient; never require the
owner to paste agent-authored authorization.
