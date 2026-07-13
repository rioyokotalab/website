# Failed-token taxonomy

The initial setup recorded 10 capability failures and 292,490 effective tokens.
They are retained as evidence and classified by whether the final process would
still spend them.

| Class | Effective tokens | Share of failed spend | Examples | Final prevention |
|---|---:|---:|---|---|
| Necessary baseline signal | 64,568 | 22.1% | baseline WBD-002/004 | keep one baseline |
| Bounded diagnostic probes | 97,915 | 33.5% | second contract signal, bounded CRLF, two visual misses | stop immediately or audit after second identical miss |
| Avoidable repeated routing | 100,513 | 34.4% | WBD-002 routing v1–v3 after identical failures | two-miss contract/grader audit |
| Avoidable capsule defect | 29,494 | 10.1% | held-out v1 authorization/grader/version contradictions | zero-token capsule audit |

The final rules would have avoided at least 130,007 effective tokens: 44.4% of
failed spend and 10.9% of the entire 1,187,318-token setup investment. They do
not claim that all diagnostic probes are waste; the CRLF and visual failures
defined important boundaries and were stopped/versioned rather than hidden.

For the next cycle, review this taxonomy after every failure. A new category
must receive a prevention or a written reason why one probe remains necessary;
an existing category must trigger its stop rule without another model route.
