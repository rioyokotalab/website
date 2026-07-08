# Instructions for codex agents (YOKOTA Lab website)

You are assisting Claude agents maintaining a hand-built static HTML site in
this folder (no build step; served as-is). Claude delegates bounded tasks to
you; Claude retains final review, verification, and publishing.

## Hard rules
- NEVER run publish.sh, deploy.sh, lftp, ssh, or git push. Never touch
  credentials, ~/.ssh, .claude/, .mcp.json, .git/, or .dont-remove-me.
- Do not edit website files unless the task explicitly says so. Default mode:
  read, analyze, and produce output files/scripts for Claude to review.
- Output convention: write results to the file path given in the task (usually
  tools/out/<task>.md). APPEND incrementally as you work, so partial progress
  survives interruption. Keep your final chat reply to a few lines: outcome +
  output file path.

## Site facts you need
- jp/ and en/ are mirrored trees: every page exists at the same path in both.
  EN/JP parity is a standing requirement.
- Page HTML has CRLF line endings and stray non-breaking spaces. Any edit
  script must use python3 with open(path, newline='', encoding='utf-8') for
  BOTH read and write to preserve CRLF byte-for-byte.
- Parse tags case-insensitively; legacy pages use unclosed uppercase <LI>.
  Split list items with re.split(r'<li[^>]*>', text, flags=re.I).
- Achievements (achievements/index.html): sections sub001–sub007, newest-first
  in each <ol>. International citations in English on BOTH language pages;
  domestic in Japanese on both. <li> tags carry data-date (YYYY-MM), and
  data-doi (bare DOI) or data-url.
- Research pages are monolingual per language (en/ all English, jp/ all
  Japanese). News items: only top-conference acceptances and grants.
- style.css is shared; pages reference it as style.css?v=YYYYMMDD.
- External target="_blank" links need rel="noopener noreferrer".

## codex self-logging & output-file-first (added 2026-07-08)
- As the LAST action of every delegated task, codex must append one line to
  `tools/codex-log.md` in the format: `date | calling agent | task | output
  file | conversationId | outcome`. The calling Claude agent only relays the
  conversationId; it does not write the log (site-checker is read-only).
- The `tools/out/` file IS the deliverable, not the chat reply. codex must
  append each result to its output file immediately as it works. The calling
  agent must confirm the output file exists and is non-empty before
  reporting PASS; chat replies are pointers, not payloads.
