driver: codex
updated: 2026-07-13T04:02+0900
task: T-87 expose one meaningful page-level heading
status: in-progress

## Now
- Goal: ensure every page exposes exactly one useful top-level heading in the accessibility tree while leaving its rendered design unchanged.
- Last done: T-86 confirmed `.htitle > a` was unnamed because its image alt was empty and all textual children were display-none; localized logo alternatives now name all 26 links, with exact standards and route-wide accessibility/runtime tests passing.
- Next: inventory accessible headings; change the hidden institutional `h1` to non-heading metadata, promote each subpage's visually identical banner heading, give EN/JP home pages a visually hidden lab-name `h1`, update selectors, and compare exact screen/print geometry plus heading trees.

## Working set
- 26 header institutional labels and banner headings; EN/JP home main headings; heading accessibility trees; CSS selectors/visual equivalence, standards/tests/cache/ledger bookkeeping.

## Open questions
- T-28 server-layer completion requires admin-compatible Apache/vhost configuration; do not experiment further on production `.htaccess`.
- HSTS must omit `includeSubDomains` and `preload`; confirm HTTP-to-HTTPS and HTTPS coverage before even a short max-age.

## Awaiting user
- T-25 remains pending automatic GitHub server GC; unrelated to T-27 implementation.
