#!/usr/bin/env bash
# ingress_audit.sh — READ-ONLY reconnaissance for a public ingress change.
#
# Never edits config. Never reloads Caddy. Never calls any upstream tool.
#
# Usage:
#   ingress_audit.sh <vhost>        e.g. ingress_audit.sh mcp.arif-fazil.com
#   ingress_audit.sh --port <port>  e.g. ingress_audit.sh --port 3003
set -uo pipefail

VHOSTS_DIR="${VHOSTS_DIR:-/etc/caddy/vhosts}"

section() { printf '\n=== %s ===\n' "$1"; }

is_baseline() { case "$1" in *.bak*|*.pre-*|*.forensic*) return 0 ;; *) return 1 ;; esac; }

show_delta() {
  # read-only comparison; computed in Python so nothing is ever written
  python3 - "$1" "$2" <<'PY'
import sys, difflib
try:
    a = open(sys.argv[1], errors="ignore").read().splitlines(keepends=True)
    b = open(sys.argv[2], errors="ignore").read().splitlines(keepends=True)
except OSError as e:
    print(f"cannot read: {e}"); raise SystemExit
out = list(difflib.unified_diff(a, b, fromfile=sys.argv[1], tofile=sys.argv[2], n=3))
if not out:
    print("(no delta — live file matches baseline)")
else:
    sys.stdout.writelines(out[:120])
PY
}

audit_vhost() {
  local name="$1" live="$VHOSTS_DIR/$1.conf" newest
  section "VHOST $name"
  if [ ! -f "$live" ]; then echo "NOT FOUND: $live"; return 1; fi
  stat -c '%s bytes  mtime=%y  %n' "$live"
  sha256sum "$live"

  newest="$(ls -t "$VHOSTS_DIR/$name.conf".bak* 2>/dev/null | head -1 || true)"
  section "DELTA vs newest baseline"
  if [ -n "$newest" ]; then
    echo "baseline: $(basename "$newest")"
    show_delta "$newest" "$live"
  else
    echo "no baseline found — every block in this vhost is unreviewed."
  fi

  section "ROUTES"
  grep -nE 'reverse_proxy|try_files|respond|redir' "$live" | head -40 || true

  section "AUTH DIRECTIVES"
  if grep -qE '^[[:space:]]*(basic_auth|forward_auth)' "$live"; then
    grep -nE '^[[:space:]]*(basic_auth|forward_auth)' "$live"
  else
    echo "NONE — this vhost trusts the upstream entirely."
  fi

  section "LOG DIRECTIVE"
  if grep -qE '^[[:space:]]*log\b' "$live"; then
    grep -nE '^[[:space:]]*log\b' "$live"
  else
    echo "NONE — caller history for this vhost is UNRECOVERABLE."
    echo '"no log entries" is NOT "nobody called". Report cannot-witness, not clean.'
  fi

  section "UPSTREAM PORTS REFERENCED"
  grep -oE '127\.0\.0\.1:[0-9]+' "$live" | sort -u || true
}

audit_port() {
  local port="${1:-}" pid hits bak_hits live_hits line
  [ -n "$port" ] || { echo "(no port given)"; return 0; }

  section "UPSTREAM :$port"
  line="$(ss -ltnp 2>/dev/null | grep -E ":${port}\b" || true)"
  if [ -z "$line" ]; then echo "NOT LISTENING on :$port"; return 0; fi
  echo "$line"

  pid="$(printf '%s' "$line" | grep -oE 'pid=[0-9]+' | head -1 | cut -d= -f2 || true)"
  if [ -n "$pid" ]; then
    ps -o pid,lstart,etime,cmd -p "$pid" || true
    section "UNIT MAPPING"
    systemctl status "$pid" 2>/dev/null | head -3 || echo "no systemctl mapping for pid $pid"
  fi

  section "PRIOR EXPOSURE — was this port ever in an older vhost?"
  hits="$(grep -l ":$port" "$VHOSTS_DIR"/*.conf* 2>/dev/null || true)"
  if [ -z "$hits" ]; then
    echo "appears in NO vhost, live or backup."
    return 0
  fi
  while IFS= read -r f; do
    if is_baseline "$f"; then echo "  baseline: $f"; else echo "  LIVE    : $f"; fi
  done <<< "$hits"

  bak_hits="$(printf '%s\n' "$hits" | grep -c 'bak\|pre-\|forensic' || true)"
  live_hits="$(printf '%s\n' "$hits" | grep -vc 'bak\|pre-\|forensic' || true)"
  echo "  live vhosts=$live_hits  baseline vhosts=$bak_hits"
  if [ "${bak_hits:-0}" -eq 0 ] 2>/dev/null; then
    echo "  >> FIRST-TIME PUBLIC: no older vhost ever referenced this port."
  fi
}

case "${1:-}" in
  ""|-h|--help)
    sed -n '2,11p' "$0"
    exit 0
    ;;
  --port) audit_port "${2:-}" ;;
  *)
    audit_vhost "$1"
    audit_port "$(grep -oE '127\.0\.0\.1:[0-9]+' "$VHOSTS_DIR/$1.conf" 2>/dev/null | head -1 | cut -d: -f2 || true)"
    ;;
esac

section "REMINDERS"
cat <<'EOF'
- READ-ONLY. No config edits, no Caddy reload, no upstream tool calls.
- `caddy validate` is safe. `caddy reload` is T3 — sovereign only.
- Never invoke a mutation tool to test whether a gate exists. Leave it UNKNOWN.
- Never clear or advance a drift baseline. That is the human's acknowledgement.
EOF
