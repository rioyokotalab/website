# YOKOTA Laboratory website

Source for <https://www.rio.scrc.iir.isct.ac.jp>. This is a hand-built static
HTML site with no build step. The `jp/` and `en/` trees mirror one another, and
the folder structure is the live URL structure.

## Quick start

Do this once. Afterward, start Claude Code in the repository and describe what
you want in plain language.

1. Ask the lab administrator for the SFTP server password.

2. Install the prerequisites for your computer.

   **A. Personal macOS MacBook**

   Install Homebrew, load it into this shell, and install Git, lftp, GitHub CLI,
   and Node.js:

   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   if [ -x /opt/homebrew/bin/brew ]; then eval "$(/opt/homebrew/bin/brew shellenv)"; else eval "$(/usr/local/bin/brew shellenv)"; fi
   brew install git lftp gh node python
   ```

   **B. Hinadori login node (Linux)**

   Git, Python 3, and lftp are generally already installed. The following
   installs GitHub CLI and Node.js only if they are missing, entirely under
   your home directory and without `sudo`:

   ```sh
   mkdir -p "$HOME/.local/bin"
   case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.profile"; export PATH="$HOME/.local/bin:$PATH" ;; esac
   if ! command -v gh >/dev/null 2>&1; then
     GH_VERSION=$(curl -fsSL https://api.github.com/repos/cli/cli/releases/latest | python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"].removeprefix("v"))')
     case "$(uname -m)" in x86_64) GH_ARCH=amd64 ;; aarch64|arm64) GH_ARCH=arm64 ;; *) echo "Unsupported architecture: $(uname -m)"; exit 1 ;; esac
     curl -fsSL "https://github.com/cli/cli/releases/download/v${GH_VERSION}/gh_${GH_VERSION}_linux_${GH_ARCH}.tar.gz" -o "/tmp/gh_${GH_VERSION}.tar.gz"
     tar -xzf "/tmp/gh_${GH_VERSION}.tar.gz" -C /tmp
     install -m 755 "/tmp/gh_${GH_VERSION}_linux_${GH_ARCH}/bin/gh" "$HOME/.local/bin/gh"
   fi
   if ! command -v node >/dev/null 2>&1; then
     curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
     export NVM_DIR="$HOME/.nvm"
     [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
     nvm install --lts
   fi
   ```

3. Install Claude Code and Codex CLI. Codex CLI 0.144.0 or newer is required
   for the MCP workers.

   ```sh
   curl -fsSL https://claude.ai/install.sh | bash
   npm install -g @openai/codex
   claude --version
   codex --version
   ```

   Confirm that the last command reports version 0.144.0 or newer.

4. Authenticate GitHub, Claude Code, and Codex. Complete the browser or terminal
   prompts opened by each command.

   ```sh
   gh auth login --git-protocol https --web
   gh auth setup-git
   claude auth login
   codex login
   ```

5. Clone the repository over HTTPS and enter it.

   ```sh
   git clone https://github.com/rioyokotalab/website.git
   cd website
   ```

6. Configure the password-only SFTP connection. This adds the `web` host only
   when it is absent, prompts without echoing the password, and keeps all
   credential files readable only by you.

   ```sh
   mkdir -p "$HOME/.ssh"
   chmod 700 "$HOME/.ssh"
   touch "$HOME/.ssh/config"
   chmod 600 "$HOME/.ssh/config"
   if ! grep -Eq '^[[:space:]]*Host[[:space:]]+web([[:space:]]|$)' "$HOME/.ssh/config"; then
     cat >> "$HOME/.ssh/config" <<'EOF'
   Host web
   	HostName web-o3.noc.titech.ac.jp
   	User gsic0017
   	ControlMaster auto
   	ControlPath ~/.ssh/cm-%r@%h-%p
   	ControlPersist yes
   EOF
   fi
   bash -c 'umask 077; read -rsp "web server password: " p; printf "%s\n" "$p" > "$HOME/.ssh/web-password"; echo'
   cat > "$HOME/.ssh/web-askpass" <<'EOF'
   #!/bin/sh
   cat "$HOME/.ssh/web-password"
   EOF
   chmod 700 "$HOME/.ssh/web-askpass"
   ```

7. Register the five Codex MCP worker labels at Claude Code user scope. These
   commands are generated from `tools/codex-workers.json` by
   `tools/gen-codex-mcp.py`:

   ```sh
   claude mcp add-json --scope user codex-spark-low '{"type":"stdio","command":"codex","args":["-c","sandbox_mode=\"workspace-write\"","-c","approval_policy=\"never\"","mcp-server"]}'
   claude mcp add-json --scope user codex-spark-medium '{"type":"stdio","command":"codex","args":["-c","sandbox_mode=\"workspace-write\"","-c","approval_policy=\"never\"","mcp-server"]}'
   claude mcp add-json --scope user codex-medium '{"type":"stdio","command":"codex","args":["-c","sandbox_mode=\"workspace-write\"","-c","approval_policy=\"never\"","mcp-server"]}'
   claude mcp add-json --scope user codex-high '{"type":"stdio","command":"codex","args":["-c","sandbox_mode=\"workspace-write\"","-c","approval_policy=\"never\"","mcp-server"]}'
   claude mcp add-json --scope user codex-low '{"type":"stdio","command":"codex","args":["-c","sandbox_mode=\"workspace-write\"","-c","approval_policy=\"never\"","mcp-server"]}'
   ```

   The repository’s committed `.mcp.json` supplies the required project-scope
   definitions automatically. Accept Claude Code’s one-time project trust
   prompt when it appears; both scopes are required for the project agents.

8. Create the local Claude Code hooks that start the preview server when a
   session opens and stop it when the session ends. This file is gitignored.

   ```sh
   mkdir -p .claude
   cat > .claude/settings.local.json <<'EOF'
   {
     "hooks": {
       "SessionStart": [{ "hooks": [{ "type": "command", "timeout": 10,
         "command": "f=$PWD/.claude/http-server.pid; if ! { [ -f \"$f\" ] && kill -0 \"$(cat \"$f\")\" 2>/dev/null; }; then { nohup python3 -m http.server 8000 >/dev/null 2>&1 & echo $! > \"$f\"; }; fi" }] }],
       "SessionEnd": [{ "hooks": [{ "type": "command", "timeout": 10,
         "command": "f=$PWD/.claude/http-server.pid; if [ -f \"$f\" ]; then p=$(cat \"$f\"); if [ -n \"$p\" ] && ps -p \"$p\" -o command= 2>/dev/null | grep -q http.server; then kill \"$p\" 2>/dev/null; fi; rm -f \"$f\"; fi" }] }]
     }
   }
   EOF
   ```

9. Start Claude Code from the repository folder. Everything after this is
   conversational.

   ```sh
   claude
   ```

## How it works: updating the website

Tell Claude Code what to change in plain language. Claude follows the site’s
rules, updates the matching Japanese and English pages, and lets you inspect
the result at <http://localhost:8000/jp/index.html> and the `/en/` counterpart.
Nothing goes live until you say **OK**. Claude then publishes the approved
change, commits and pushes it to GitHub, and verifies the live site.

Deployment mirrors the repository’s deployed set to `www/` over SFTP with
`mirror -R --delete`: new and changed files are uploaded, and files removed
locally are removed remotely. Excluded repo-only paths are neither uploaded nor
deleted remotely. The exclusions include `.git`, `.claude`, `tools`, deployment
scripts, `CLAUDE.md`, `README.md`, `AGENTS.md`, `.mcp.json`, `.gitignore`, and
the CV sources (`cv/cv.tex`, `cv/cv.cls`, and `cv/build-cv.sh`); the built
`cv/cv.pdf` is deployed.

## Rules that keep the site healthy

- Every page must exist at the same path in both `jp/` and `en/`; the language
  toggle swaps `/jp/` and `/en/` in the URL.
- Preview both languages and give explicit approval before publishing.
- Never upload `.git` or repository-only tooling to the public server.
- Keep `.dont-remove-me`; it is a hosting marker file.
- Let Claude Code handle editing, preview startup, publishing, pushing, and live
  verification so the repository and server stay synchronized.
