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
cd "$HOME"
git clone https://github.com/rioyokotalab/website.git
cd "$HOME/website"
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

The repository benchmark was run on two agent stacks against the identical
capsules, mutated fixtures, and F2P / browser P2P graders: **GPT-5.6** (three
models × six efforts, 90 singletons + 83 adaptive repeats = 173 runs) and
**Claude Code** (three models × five efforts, 75 singletons + 14 WBD-003
repeats = 89 runs). This is a YOKOTA Lab website-maintenance benchmark, not a
general leaderboard. `effective_tokens` = input − cached input + output is a
planning proxy, not monetary cost, and is **not comparable across providers**
(Claude Code's large cached system prompt inflates its input term); compare
within a provider. GPT denominators are out of 30 cells/model (six efforts),
Claude out of 25 (five efforts). Both stacks reached full quality on nearly
every cell — GPT 154/173 full-quality overall, Claude 72/75 singletons with the
three misses (all WBD-003 at higher effort) not reproducing (14/14 repeats).

### Per-model comparison (full-quality singleton medians)

| Model | Full-quality cells | Median total time | Median effective tokens |
| --- | ---: | ---: | ---: |
| `gpt-5.6-luna` | 29/30 | 110.1 s | 24,322 |
| `gpt-5.6-terra` | 26/30 | 101.1 s | 22,692 |
| `gpt-5.6-sol` | 29/30 | 118.7 s | 19,823 |
| `claude-fable-5` | 25/25 | 51.4 s | 25,405 |
| `claude-opus-4-8` | 24/25 | 86.3 s | 28,892 |
| `claude-sonnet-5` | 23/25 | 41.1 s | 29,404 |

Within Claude, Fable 5 was the only model to pass every singleton and was the
most token-efficient; Sonnet 5 was fastest overall; Opus 4.8 slowest. Wall-clock
medians ran lower for the Claude stack, but token counts are not cross-comparable
per the caveat above.

### Per-effort comparison (full-quality singleton medians, all models)

| Effort | GPT cells | GPT time | GPT tokens | Claude cells | Claude time | Claude tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| low | 15/15 | 69.4 s | 12,141 | 15/15 | 46.2 s | 22,771 |
| medium | 13/15 | 77.2 s | 18,867 | 14/15 | 47.0 s | 23,701 |
| high | 14/15 | 102.0 s | 23,545 | 15/15 | 71.3 s | 27,480 |
| xhigh | 13/15 | 127.6 s | 22,199 | 15/15 | 68.8 s | 33,591 |
| max | 14/15 | 134.3 s | 25,992 | 13/15 | 142.2 s | 45,277 |
| ultra | 15/15 | 131.8 s | 32,103 | — | — | — |

**Low effort was best on both stacks** — fastest, cheapest, and (for Claude) the
only effort with no misses; higher effort added time and tokens with no quality
gain and all of the variance. GPT's `ultra` cells all passed but were dominated
by another effort on every task (Claude has no `ultra`).

### Recommended dispatch routes (GPT-5.6)

Reliability confidence gates route selection before runtime or token use. The
runtime objective is the default; every implementation still requires the linked
policy's independent validation. For Claude, all model × effort routes are
reliable, so routing is by runtime/tokens — default to low effort; per-task
routes are in the Claude summary.

| Measured task class | Runtime / reliability route (expected time) | Effective-token route (expected tokens) | Evidence |
| --- | --- | --- | --- |
| WBD-001 — bilingual legacy-HTML semantics | `gpt-5.6-terra` / low (57.0 s) | `gpt-5.6-terra` / low (11,444) | 6/6, high-confidence |
| WBD-002 — mirrored secure accessible links | `gpt-5.6-luna` / low (94.0 s) | `gpt-5.6-sol` / low (14,867) | both 6/6, high-confidence |
| WBD-003 — security/privacy JavaScript | `gpt-5.6-terra` / low (35.6 s) | `gpt-5.6-sol` / low (12,355) | both 6/6, high-confidence |
| WBD-004 — responsive CSS visual contracts | `gpt-5.6-luna` / low (59.0 s) | `gpt-5.6-sol` / low (21,394) | both 6/6, high-confidence |
| WBD-005 — cross-cutting shared assets | `gpt-5.6-sol` / high (249.1 s) | `gpt-5.6-sol` / high (45,053) | 8/9, qualified; full grader mandatory |

Full methods, intervals, failures, and exact values:
[GPT full matrix](tools/agent-benchmark/gpt56-full-20260713.summary.md),
[GPT adaptive repeats](tools/agent-benchmark/gpt56-repeat-20260714.summary.md),
[GPT routing policy](tools/agent-benchmark/routing-policy.json), and
[Claude summary](tools/agent-benchmark/claude-full-20260718.summary.md). Query
the GPT policy with, for example:

```sh
python3 tools/agent-benchmark/select_route.py --task WBD-003 --objective runtime
```
