# Codex Offload Policy

Shared standing policy for YOKOTA Lab website agents with codex MCP access.

## Default Posture

- OFFLOAD FIRST.
- If a task involves reading more than 2 files, reading more than about 100 lines, site-wide or multi-page analysis, parsing substantial HTML, generating substantial content, translating, citation parsing, exporter reasoning, figure/script drafting, or drafting a CRLF-preserving edit script, delegate to the agent's own codex tier.
- Do not spend the expensive Claude agent context doing bulk reading, counting, parsing, drafting, or first-pass reasoning when codex can read the repository itself.

## Delegation Form

- Pass pointers, not payloads.
- A codex prompt must include:
  - calling agent name;
  - concrete task;
  - file paths or URL pointers to inspect;
  - acceptance criteria;
  - output path under `tools/out/<task>.md` or `tools/out/<task>.py`;
  - conversationId from the caller when available.
- Never paste whole file contents, large snippets, or generated payloads into the codex prompt. codex reads `AGENTS.md` and the referenced files itself.

## Output-File-First

- The `tools/out/` file is the deliverable.
- codex must append each result to the output file immediately as it works; do not batch all findings until the end.
- For scripts, codex writes the complete proposed script to `tools/out/<task>.py`; Claude reviews and runs it only if appropriate.
- codex final chat replies must be short: outcome plus output path.

## Logging

- As the LAST action of every delegated codex task, codex appends one line to `tools/codex-log.md`:

```text
date | calling agent | task | output file | conversationId | outcome
```

- The calling Claude agent relays the conversationId to codex.
- site-checker is read-only, so it does not write the log itself; codex writes the line.
- site-editor and site-author may write a log line themselves only when their delegated codex run did not or could not do it, and should say so in their report.

## Claude Verification

- After codex returns, the calling Claude agent reads only:
  - the codex output file;
  - minimal spot-check evidence, such as one or two grep/read/curl confirmations.
- The calling agent must confirm the output file exists and is non-empty.
- The calling agent must independently spot-check at least one codex claim before reporting PASS or success.
- codex never verifies its own work; site-checker or the calling Claude agent performs independent verification.

## Division Of Labor

- codex generates, analyzes, parses, drafts translations, drafts citations, reasons about exporter logic, and drafts edit scripts.
- Claude reviews, decides, executes edit scripts, verifies, and reports to the user.
- codex never edits website pages directly.
- codex never publishes.
- codex never touches credentials, `.ssh`, `.git`, `.claude`, `.mcp.json`, or `.dont-remove-me`.
- codex never runs `publish.sh`, `deploy.sh`, `lftp`, `ssh`, or `git push`.

## Calling-Agent Final Output

- The calling Claude agent's final message is capped at about 15 lines.
- It reports outcome, changed or inspected paths, verification result, and pointers to `tools/out/` files.
- It does not paste codex payloads into chat.
