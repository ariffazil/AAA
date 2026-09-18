#!/usr/bin/env bash
# verify-node.sh — resolve the identity of a target BEFORE writing to it.
# Catches the silent misroute: a name you believe maps to node A resolving to node B.
#
# Usage: verify-node.sh <ssh-target> [expected-hostname]
# Exit:   0 match (or no expectation given) | 4 MISMATCH | 5 unreachable

set -uo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $(basename "$0") <ssh-target> [expected-hostname]" >&2
  exit 64
fi

TARGET="$1"
EXPECTED="${2:-}"

OUT="$(ssh -o ConnectTimeout=5 -o BatchMode=yes "$TARGET" 'hostname; tailscale ip -4 2>/dev/null | head -1' 2>/dev/null)"
RC=$?

if [ $RC -ne 0 ] || [ -z "$OUT" ]; then
  echo "VERIFY FAIL: cannot reach '$TARGET' (ssh rc=$RC)" >&2
  echo "Do not assume the node is down — a refused/timed-out dial is an ADDRESS claim, not a health claim." >&2
  exit 5
fi

HOSTNAME_REMOTE="$(printf '%s\n' "$OUT" | sed -n '1p')"
TS_IP="$(printf '%s\n' "$OUT" | sed -n '2p')"

printf 'target=%s resolved_host=%s tailscale_ip=%s\n' "$TARGET" "$HOSTNAME_REMOTE" "$TS_IP"

if [ -z "$EXPECTED" ]; then
  exit 0
fi

if [ "$HOSTNAME_REMOTE" != "$EXPECTED" ]; then
  echo "VERIFY MISMATCH: '$TARGET' resolved to '$HOSTNAME_REMOTE', expected '$EXPECTED'" >&2
  echo "STOP. A write here lands on the wrong machine and every sender-side check will confirm it." >&2
  exit 4
fi

echo "VERIFY OK: '$TARGET' is '$EXPECTED'"
exit 0
