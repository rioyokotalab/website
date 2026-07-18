#!/bin/sh
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=4.9.2-2ubuntu1.1
VERSION_LINE='Version 4.9.2'
URL=https://archive.ubuntu.com/ubuntu/pool/main/l/lftp/lftp_4.9.2-2ubuntu1.1_amd64.deb
SHA256=60140fcd971e86f0be1cea9d206a4cdf9baead70cb65adcc09403c6294290b72
MEMBER=./usr/bin/lftp
PREFIX=${WEBSITE_LFTP_PREFIX:-$HOME/.local}
archive=
stage=
install_parent=

usage() {
	cat <<'EOF' >&2
Usage: tools/bootstrap-lftp.sh plan|apply|doctor

Plan is read-only. Apply installs the pinned Ubuntu 24.04 x86-64 lftp binary
under ~/.local only when no healthy lftp is already available. Override the
rootless prefix with an absolute WEBSITE_LFTP_PREFIX for isolated validation.
EOF
	exit 2
}

die() {
	echo "bootstrap-lftp: $*" >&2
	exit 2
}

healthy() {
	candidate=$1
	resolved=$(realpath -e -- "$candidate" 2>/dev/null) || return 1
	[ -f "$resolved" ] && [ ! -L "$resolved" ] && [ -x "$resolved" ] ||
		return 1
	"$candidate" --version 2>/dev/null |
		awk -v expected="$VERSION_LINE" '
			index($0, expected) { found=1 }
			END { exit found ? 0 : 1 }
		'
}

resolved_command() {
	command -v lftp 2>/dev/null || true
}

remove_exact_archive() {
	[ -n "$archive" ] || return 0
	[ -e "$archive" ] || [ -L "$archive" ] || return 0
	[ -f "$archive" ] && [ ! -L "$archive" ] || return 1
	[ "$(stat -c '%u' -- "$archive")" = "$(id -u)" ] || return 1
	unlink "$archive"
	archive=
}

cleanup() {
	status=$?
	trap - EXIT HUP INT TERM
	cleanup_failed=0
	remove_exact_archive || cleanup_failed=1
	if [ -n "$stage" ] && [ -d "$stage" ]; then
		"$ROOT/tools/guarded-tree-cleanup.sh" "$install_parent" "$stage" \
			"${TMPDIR:-/tmp}" >/dev/null || cleanup_failed=1
	fi
	if [ "$status" -eq 0 ] && [ "$cleanup_failed" -ne 0 ]; then
		status=1
	fi
	exit "$status"
}

action=${1:-}
[ "$#" -eq 1 ] || usage
case "$action" in plan|apply|doctor) ;; *) usage ;; esac

case "$PREFIX" in /*) ;; *) die "WEBSITE_LFTP_PREFIX must be absolute" ;; esac
case "$(uname -s):$(uname -m)" in Linux:x86_64) ;;
	*) die "pinned bootstrap supports only Linux x86-64" ;;
esac

if [ "$action" = doctor ]; then
	command_path=$(resolved_command)
	[ -n "$command_path" ] && healthy "$command_path" ||
		die "healthy lftp 4.9.2 is unavailable"
	echo "LFTP_DOCTOR status=pass command=$command_path version=$VERSION"
	exit 0
fi

command_path=$(resolved_command)
if [ -n "$command_path" ] && healthy "$command_path"; then
	echo "LFTP_PLAN version=$VERSION action=keep command=$command_path"
	[ "$action" = plan ] || echo 'END lftp changes=none'
	exit 0
fi

install_dir=$PREFIX/opt/website/lftp/$VERSION/ubuntu24.04-x86_64
installed_binary=$install_dir/lftp
stable_link=$PREFIX/bin/lftp

artifact_action=install
if [ -d "$install_dir" ] && [ ! -L "$install_dir" ] && healthy "$installed_binary"; then
	artifact_action=keep
elif [ -e "$install_dir" ] || [ -L "$install_dir" ]; then
	die "existing install path is not the exact healthy artifact: $install_dir"
fi

link_action=create
if [ -L "$stable_link" ] && [ "$(readlink "$stable_link")" = "$installed_binary" ]; then
	link_action=keep
elif [ -e "$stable_link" ] || [ -L "$stable_link" ]; then
	die "existing command path is not owned by this bootstrap: $stable_link"
fi

echo "LFTP_PLAN version=$VERSION action=install prefix=$PREFIX"
echo "FETCH url=$URL sha256=$SHA256"
echo "EXTRACT format=deb member=$MEMBER binary=lftp"
echo "ARTIFACT action=$artifact_action path=$install_dir"
echo "LINK action=$link_action path=$stable_link"
[ "$action" = apply ] || { echo 'END lftp changes=not-applied'; exit 0; }

if [ -r /etc/os-release ]; then
	# The package intentionally relies on the Ubuntu Noble runtime library floor.
	. /etc/os-release
	[ "${ID:-}" = ubuntu ] && [ "${VERSION_ID:-}" = 24.04 ] ||
		die "apply requires Ubuntu 24.04"
else
	die "apply cannot verify Ubuntu 24.04"
fi
for required in curl dpkg-deb tar sha256sum mktemp realpath stat; do
	command -v "$required" >/dev/null 2>&1 || die "apply requires command: $required"
done

mkdir -p "$PREFIX"
[ -d "$PREFIX" ] || die "prefix is not a directory"
PREFIX=$(realpath -e -- "$PREFIX")
install_dir=$PREFIX/opt/website/lftp/$VERSION/ubuntu24.04-x86_64
installed_binary=$install_dir/lftp
stable_link=$PREFIX/bin/lftp

trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

if [ "$artifact_action" = install ]; then
	install_parent=${install_dir%/*}
	mkdir -p "$install_parent"
	archive=$(mktemp "${TMPDIR:-/tmp}/website-lftp.XXXXXX.deb")
	echo "NATIVE curl --proto =https --tlsv1.2 -fL --retry 2 $URL -o TEMP"
	curl --proto '=https' --tlsv1.2 -fL --retry 2 "$URL" -o "$archive"
	printf '%s  %s\n' "$SHA256" "$archive" | sha256sum -c - >/dev/null
	stage=$(mktemp -d "$install_parent/.staging.XXXXXX")
	echo "NATIVE dpkg-deb --fsys-tarfile TEMP | tar -xOf - $MEMBER > STAGING/lftp"
	dpkg-deb --fsys-tarfile "$archive" | tar -xOf - "$MEMBER" >"$stage/lftp"
	[ -f "$stage/lftp" ] && [ ! -L "$stage/lftp" ] ||
		die "package did not contain the expected regular binary"
	chmod 755 "$stage/lftp"
	[ "$(find "$stage" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')" -eq 1 ] ||
		die "package extraction created unexpected paths"
	healthy "$stage/lftp" || die "extracted lftp failed version validation"
	mv -T "$stage" "$install_dir"
	stage=
fi

if [ "$link_action" = create ]; then
	mkdir -p "${stable_link%/*}"
	ln -s "$installed_binary" "$stable_link"
fi
healthy "$installed_binary" || die "installed lftp failed final validation"
[ -L "$stable_link" ] && [ "$(readlink "$stable_link")" = "$installed_binary" ] ||
	die "stable link failed final validation"
remove_exact_archive || die "cannot remove exact temporary archive"
trap - EXIT HUP INT TERM
echo "LFTP_APPLY status=complete command=$stable_link version=$VERSION"
echo "CALLER native='hash -r' reason=refresh-command-path-cache"
