# YOKOTA Laboratory website

Source for <https://www.rio.scrc.iir.isct.ac.jp>. The site is hand-built static
HTML: there is no framework, compilation step, or generated public tree. Files
in the deployed set are served at their corresponding URLs.

The public URL tree is intentionally stable. Edit pages in place rather than
moving them. The `en/` and `jp/` trees mirror one another so the language switch
can replace one prefix with the other.

## Quickstart

GitHub write access and web-server credentials are provisioned separately by
the owner. Never copy credentials into repository configuration.

### 1. Install Node.js and agent clients

```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install 24.16.0
nvm alias default 24.16.0
npm install --global @openai/codex@0.144.1 @anthropic-ai/claude-code@2.1.207
codex login --device-auth
```

### 2. Clone and configure the clients

```sh
mkdir -p "$HOME/projects"
git clone https://github.com/rioyokotalab/website.git "$HOME/projects/website"
cd "$HOME/projects/website"
mkdir -p "$HOME/.codex"
printf '%s\n' 'approval_policy = "never"' 'sandbox_mode = "danger-full-access"' 'model_reasoning_effort = "medium"' '' "[projects.\"$PWD\"]" 'trust_level = "trusted"' > "$HOME/.codex/config.toml"
chmod 600 "$HOME/.codex/config.toml"
```

Owner-scope configuration affects other projects. Preserve unrelated keys when
updating an existing file; see `skills/config-proposals.md`.
Claude reads the tracked root `CLAUDE.md`, which imports the same repository
rules as Codex. Authenticate Claude interactively through its supported client
flow; never put authentication material in project files.

### 3. Verify or install the deployment client

The offline deployment-policy suite requires lftp 4.9.2. A healthy system
command is accepted; otherwise the repository can install its checksum-pinned
Ubuntu 24.04 x86-64 package without root access:

```sh
tools/bootstrap-lftp.sh doctor || tools/bootstrap-lftp.sh plan
tools/bootstrap-lftp.sh apply
hash -r
tools/bootstrap-lftp.sh doctor
```

`plan` is read-only. `apply` downloads only the pinned HTTPS package, verifies
its SHA-256 digest, extracts only `./usr/bin/lftp`, and installs under
`~/.local`. It does not require another repository.

### 4. Install repository pre-commit checks

The canonical hook is tracked at `tools/hooks/pre-commit`. Install or verify
the live copy with the doctor:

```sh
tools/hook-doctor.sh          # read-only status
tools/hook-doctor.sh apply    # back up any existing hook, install canonical
tools/hook-doctor.sh rollback # restore the pre-apply backup if needed
```

### 5. Verify and start

```sh
codex --version
codex login status
codex doctor --summary
claude --version
claude doctor
python3 tools/check-md-size.py
git status --short
codex  # or: claude
```

## Preview and tests

There is no build step. Preview from the repository root:

```sh
python3 -m http.server 8000
```

Open <http://localhost:8000/jp/index.html> and the corresponding English page.

Install the locked browser-test dependencies and run the bilingual consent
regression suite with:

```sh
npm ci
npm run test:consent:install
npm run test:consent
```

Run deterministic credential-free pre-publish checks with:

```sh
tools/test-security.sh
```

Add read-only checks of live headers and deploy-excluded paths with:

```sh
tools/test-security.sh --live
```

The offline suite checks EN/JP structure, language metadata, unique IDs,
navigation landmarks, localized skip links, image alternatives, fragments,
stylesheet versions, script safety, the deploy allowlist, and supply-chain
pins. The browser suite remains the deeper runtime check.

### Supply-chain maintenance

The gallery assets use reviewed HTTPS cdnjs URLs, exact versions, SHA-384
integrity, and `crossorigin="anonymous"`. Recompute remote hashes and run npm's
advisory audit in disposable directories with:

```sh
npm run test:supply-chain:online
```

Run the online check quarterly and before dependency changes. Update one
dependency at a time, regenerate only the lockfile, update all six gallery
pages together, and rerun browser, offline, and online checks.

## Repository map

| Path | Purpose |
| --- | --- |
| `en/`, `jp/` | Mirrored English and Japanese public pages |
| `style.css`, `js/`, `images/` | Shared public presentation and assets |
| `cv/` | Public PDF plus deploy-excluded source/build files |
| `skills/` | Canonical editing, lookup, ledger, and publish playbooks |
| `tools/` | Checks, exporters, ledger, metrics, and transient output |
| `docs/` | Repository-owned ruleset, audit evidence, and controls |
| `AGENTS.md`, `CLAUDE.md` | Shared role, security, workflow, and repository invariants |
| `publish.sh`, `deploy.sh` | Gated publish pipeline and SFTP mirror |

The playbook index is `skills/README.md`. Read the playbook for the area being
changed; this README is orientation, not the procedure itself.

The repository is operationally self-contained: its CI, guarded cleanup,
ruleset restore payload, public-history audit, and rootless lftp bootstrap do
not fetch or invoke a separate control repository. Historical task references
are provenance only.

## Working on the site

At driver start, read `TODO.md` and `tools/state/session.md`, then only
the facts, decisions, and task playbooks required for the work. Checkpoint
in-flight state according to `skills/context-ledger.md`.

For a normal page change:

1. Read `skills/html-editing.md`, `skills/en-jp-parity.md`, and any relevant
   content playbook.
2. Edit both language trees where applicable and preserve legacy HTML/CRLF
   conventions.
3. Run scoped parity, link, and regression checks.
4. Preview both languages.
5. A directly user-started DRIVER completes the gated commit/push/publish
   workflow; bounded workers return evidence and never publish or push.

Native subagent delegation follows the bounded contract in
`skills/codex-delegation.md` and the active client's repository entry point.
Use it only for independent bounded work where an on-disk handoff saves root
context. The root DRIVER owns the ledger, review, integration, configuration,
commits, and external writes.

Project configuration changes require explicit task scope. Owner-scope changes
remain proposal-only without exact authorization.

## Exporters and derived records

`tools/` includes researchmap and ORCID exporters plus their checks. Follow
`skills/exporters.md`. External account writes, CV PDF builds, and operations
that need private values require the explicit authorization described there;
credentials and login UIs are never automated.

The context ledger separates state by purpose:

- `TODO.md`: task board;
- `tools/state/session.md`: current handoff;
- `tools/state/facts.md`: verified current facts;
- `tools/state/decisions.md`: durable choices and rationale.

## Publishing and deployment

A directly user-started Codex or Claude DRIVER has standing authority to push
or publish completed owner-requested repository changes after every gate in
`skills/publish-and-verify.md` passes. Workers never publish or push. Blocked
work, unrelated changes, credentials, force operations, unexpected deploy
changes, and material scope expansion remain fail-closed.

`deploy.sh` builds a fresh positive-allowlist staging tree and mirrors it to the
SFTP web root with deletion. Only `.htaccess`, `index.html`, `style.css`,
`en/`, `jp/`, `images/`, `js/`, and `cv/cv.pdf` can enter staging;
`.dont-remove-me` is the sole preserved remote exception.

## Invariants

- Preserve every public path and EN/JP counterpart.
- Update shared navigation/header/footer markup across both trees with a
  CRLF-safe scripted replacement.
- Preserve `.dont-remove-me`; never expose credentials or `.git`.
- Add `rel="noopener noreferrer"` to new `target="_blank"` links.
- Publish or push only after role, scope, verification, rebase, and applicable
  dry-run gates pass.

## Benchmark results (July 2026)

The 2026-07-23/24 refresh reran two exact, sequential singleton matrices against
the same public baseline and task capsules: **GPT-5.6** (3 models × 6 efforts ×
5 tasks = 90 cells) and **Claude Code** (3 × 5 × 5 = 75 cells). This is a
website-maintenance benchmark, not a general leaderboard. Strict frozen-grader
passes were 86/90 for GPT (previously 85/90) and 71/75 for Claude (previously
72/75). Browser-functional results were 90/90 for GPT (previously 89/90) and
74/75 for Claude (unchanged).

Four GPT and three Claude strict misses passed every browser test but used
semantically valid JavaScript forms rejected by literal-sensitive static
assertions. Claude Sonnet/low's WBD-005 miss was different: it changed an
out-of-scope file and failed two browser tests. A separately labeled focused
retry recovered that route to 100; focused inspection also recovered one of two
Claude WBD-003 static misses. These retries do not alter the singleton totals.

`effective_tokens = input - cached_input + output` is a planning proxy, not
monetary cost, and is **not comparable across providers**. Claude's current
fresh, no-session-persistence invocation also changed its accounting baseline.

### Per-model matched change

Times and tokens are medians over strict full-quality singleton cells.

| Model | Strict cells, previous → current | Median total time | Median effective tokens |
| --- | ---: | ---: | ---: |
| `gpt-5.6-luna` | 29/30 → 27/30 | 110.1 → 121.1 s | 24,322 → 26,819 |
| `gpt-5.6-sol` | 29/30 → 29/30 | 118.7 → 146.5 s | 19,823 → 32,487 |
| `gpt-5.6-terra` | 26/30 → 30/30 | 101.1 → 160.4 s | 22,692 → 25,685 |
| `claude-fable-5` | 25/25 → 25/25 | 112.8 → 126.1 s | 25,405 → 129,411 |
| `claude-opus-4-8` | 24/25 → 23/25 | 144.4 → 144.9 s | 28,892 → 129,309 |
| `claude-sonnet-5` | 23/25 → 23/25 | 98.8 → 122.9 s | 29,404 → 156,992 |

### Per-effort current result

| Effort | GPT strict cells | GPT time | GPT tokens | Claude strict cells | Claude time | Claude tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| low | 14/15 | 99.3 s | 23,792 | 14/15 | 97.9 s | 125,312 |
| medium | 15/15 | 103.1 s | 27,319 | 15/15 | 117.1 s | 129,411 |
| high | 15/15 | 130.7 s | 28,534 | 14/15 | 101.7 s | 130,536 |
| xhigh | 14/15 | 131.8 s | 34,718 | 13/15 | 169.4 s | 137,350 |
| max | 13/15 | 171.0 s | 32,487 | 15/15 | 201.2 s | 153,197 |
| ultra | 15/15 | 210.8 s | 33,863 | — | — | — |

Higher effort did not monotonically improve quality, time, or token use.
GPT/medium and Claude/medium passed every strict cell at materially lower
median time than max; GPT/ultra also passed every cell but was slower and more
token-heavy than medium. Because every current route has only one observation,
the following quality-first routes are repeat candidates, not service-level
guarantees.

### Current runtime candidates

| Measured task class | GPT-5.6 | Claude Code |
| --- | --- | --- |
| WBD-001 — bilingual legacy-HTML semantics | `terra` / low (44.7 s) | `fable-5` / low (49.2 s) |
| WBD-002 — mirrored secure accessible links | `terra` / low (131.5 s) | `opus-4-8` / low (112.9 s) |
| WBD-003 — security/privacy JavaScript | `luna` / low (32.0 s) | `sonnet-5` / low (45.5 s) |
| WBD-004 — responsive CSS visual contracts | `sol` / medium (70.1 s) | `sonnet-5` / low (54.1 s) |
| WBD-005 — cross-cutting shared assets | `sol` / low (160.8 s) | `sonnet-5` / medium (153.1 s) |

Current wall time includes confirmed NFS blocking and shared browser-grader
slowdown, so it must not be attributed entirely to the model clients. Full
methods, matched deltas, failures, and interpretation:
[nightly audit](docs/audits/agent-benchmark-nightly-2026-07-24.md),
[GPT summary](tools/agent-benchmark/gpt56-nightly-20260723.summary.md),
[GPT comparison](tools/agent-benchmark/gpt56-nightly-20260723.comparison.json),
[Claude summary](tools/agent-benchmark/claude-nightly-20260723.summary.md), and
[Claude comparison](tools/agent-benchmark/claude-nightly-20260723.comparison.json).
Focused results:
[WBD-003](tools/agent-benchmark/claude-nightly-20260723-focused-wbd003.summary.md)
and
[WBD-005](tools/agent-benchmark/claude-nightly-20260723-focused-wbd005.summary.md).
