#!/usr/bin/env bash
# lint-memory-phantoms.sh
# Scans /root/.claude/projects/-root/memory/, /root/AAA/eurekas/, /root/AAA/governance/
# for phantom path citations. Phantoms = bare /root/... paths that do not resolve.
# Output: PHANTOM count + per-file enumeration. Read-only; no mutation.
#
# Usage:   bash lint-memory-phantoms.sh                 # scan all 3 dirs
#          bash lint-memory-phantoms.sh <file-or-dir>   # scan one
#          bash lint-memory-phantoms.sh --json          # machine-readable
#          bash lint-memory-phantoms.sh --json <target> # JSON scoped to target
#
# Why:     Federation has been propagating phantom path citations
#          (>=140 across memory/eurekas/governance as of 2026-09-21).
#          This linter surfaces the debt so it can be measured.
#          See /root/.claude/projects/-root/memory/holes-exposed-2026-09-21.md
#
# Reversibility: read-only. rm $0 to revert.

set -u

MEM_DIR="/root/.claude/projects/-root/memory"
EUREKAS_DIR="/root/AAA/eurekas"
GOV_DIR="/root/AAA/governance"

JSON_OUT=0
TARGET=""

for arg in "$@"; do
  case "$arg" in
    --json) JSON_OUT=1 ;;
    --help|-h)
      sed -n '2,18p' "$0"
      exit 0
      ;;
    *) TARGET="$arg" ;;
  esac
done

# Collect target files
if [ -n "$TARGET" ]; then
  if [ -d "$TARGET" ]; then
    FILES=$(find "$TARGET" -maxdepth 1 -type f -name "*.md" 2>/dev/null)
  elif [ -f "$TARGET" ]; then
    FILES="$TARGET"
  else
    echo "ERROR: $TARGET not found" >&2
    exit 2
  fi
else
  FILES=""
  for d in "$MEM_DIR" "$EUREKAS_DIR" "$GOV_DIR"; do
    if [ -d "$d" ]; then
      FOUND=$(find "$d" -maxdepth 1 -type f -name "*.md" 2>/dev/null)
      FILES="${FILES}${FILES:+ }${FOUND}"
    fi
  done
fi

# phantom regex: /root/ + path chars + extension
PHANTOM_RE='/root/[A-Za-z0-9_./-]+\.(py|md|jsonl|json|yaml|sh|log|sha256|txt|db)'

TOTAL=0
PER_FILE_OUT=""
JSON_FILES=""

# Use NUL-delimited iteration
while IFS= read -r f; do
  [ -z "$f" ] && continue
  [ ! -f "$f" ] && continue

  CANDIDATES=$(grep -oE "$PHANTOM_RE" "$f" 2>/dev/null | sort -u)
  FILE_PHANTOMS=""

  while IFS= read -r p; do
    [ -z "$p" ] && continue
    p_clean="${p%[.,;:)]}"
    [ -z "$p_clean" ] && continue
    if [ ! -e "$p_clean" ]; then
      FILE_PHANTOMS="${FILE_PHANTOMS} ${p_clean}"
      TOTAL=$((TOTAL + 1))
    fi
  done <<< "$CANDIDATES"

  if [ -n "$FILE_PHANTOMS" ]; then
    PER_FILE_OUT="${PER_FILE_OUT}
${f}${FILE_PHANTOMS}"
    if [ $JSON_OUT -eq 1 ]; then
      PH_JSON=""
      for p in $FILE_PHANTOMS; do
        PH_JSON="${PH_JSON}\"${p}\","
      done
      PH_JSON="${PH_JSON%,}"
      JSON_FILES="${JSON_FILES}{\"file\":\"${f}\",\"phantoms\":[${PH_JSON}]},"
    fi
  fi
done <<< "$FILES"

if [ $JSON_OUT -eq 1 ]; then
  echo "{\"total_phantoms\":${TOTAL},\"files\":[${JSON_FILES%,}]}"
else
  echo "=== PHANTOM CITATION LINTER ==="
  echo "Memory dir : $MEM_DIR"
  echo "Eurekas dir: $EUREKAS_DIR"
  echo "Gov dir    : $GOV_DIR"
  echo "Files scanned: $(echo "$FILES" | wc -w)"
  echo "TOTAL PHANTOMS: $TOTAL"
  echo "---"
  if [ $TOTAL -eq 0 ]; then
    echo "CLEAN -- no phantom paths detected."
  else
    printf '%s\n' "$PER_FILE_OUT"
  fi
  echo "---"
  echo "Reversibility: read-only. rm $0 to revert."
fi

exit 0