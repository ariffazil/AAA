#!/usr/bin/env bash
# attest-transfer.sh — RECEIVER-side attestation for a cross-node artifact transfer.
# Run this ON THE RECEIVING NODE. Its output is the evidence; the sender's copy is not.
#
# Usage: attest-transfer.sh <path>
# Prints: host=... path=... sha256=... bytes=... lines=... mtime=...
# Exit:   0 attested | 2 path not found | 3 not a regular file

set -uo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $(basename "$0") <path>" >&2
  exit 64
fi

TARGET="$1"

if [ ! -e "$TARGET" ]; then
  # Distinguish 'absent' from 'wrong tree' — the cheapest falsifier of a claimed write.
  DIR="$(dirname "$TARGET")"
  echo "ATTEST FAIL: path not found on this node" >&2
  echo "host=$(hostname)" >&2
  echo "looked_for=$TARGET" >&2
  if [ -d "$DIR" ]; then
    echo "dest_dir=$DIR mtime=$(stat -c '%y' "$DIR")" >&2
    echo "dest_dir_contents:" >&2
    ls -la "$DIR" >&2
  else
    echo "dest_dir=$DIR DOES NOT EXIST on this node either" >&2
  fi
  exit 2
fi

if [ ! -f "$TARGET" ]; then
  echo "ATTEST FAIL: not a regular file: $TARGET" >&2
  exit 3
fi

HOST="$(hostname)"
ABS="$(readlink -f "$TARGET")"
SHA="$(sha256sum "$TARGET" | awk '{print $1}')"
BYTES="$(stat -c '%s' "$TARGET")"
MTIME="$(stat -c '%y' "$TARGET")"

# Line count: cheap extra field for text artifacts; blank for binary.
LINES=""
case "$TARGET" in
  *.txt|*.md|*.json|*.jsonl|*.yaml|*.yml|*.py|*.sh|*.log)
    LINES="$(wc -l < "$TARGET" | tr -d ' ')"
    ;;
esac

printf 'host=%s path=%s sha256=%s bytes=%s lines=%s mtime=%s\n' \
  "$HOST" "$ABS" "$SHA" "$BYTES" "$LINES" "$MTIME"

exit 0
