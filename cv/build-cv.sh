#!/usr/bin/env bash
# build-cv.sh — compile cv.tex -> cv.pdf using tectonic.
#
# Purpose: cv.tex (and cv.cls) live at the repo root; this script rebuilds
# cv.pdf from them. Run it on demand whenever cv.tex or cv.cls changes,
# then let publish.sh deploy the resulting cv.pdf along with the rest of
# the site. Not run automatically by publish.sh.
#
# Requires tectonic (installed to ~/.local/bin/tectonic; no sudo needed).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

TECTONIC="${TECTONIC:-tectonic}"
if ! command -v "$TECTONIC" >/dev/null 2>&1; then
    if [ -x "$HOME/.local/bin/tectonic" ]; then
        TECTONIC="$HOME/.local/bin/tectonic"
    else
        echo "error: tectonic not found on PATH or at ~/.local/bin/tectonic" >&2
        exit 1
    fi
fi

"$TECTONIC" cv.tex

if [ -f "$SCRIPT_DIR/cv.pdf" ]; then
    echo "Success: cv.pdf written to $SCRIPT_DIR/cv.pdf"
else
    echo "error: expected $SCRIPT_DIR/cv.pdf but it was not produced" >&2
    exit 1
fi
