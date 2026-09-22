#!/usr/bin/env bash
# stamp-legacy-phantoms.sh
# Prepends a PHANTOM-CITING marker to every legacy memory file that cites phantom paths.
# Read-only on the file content itself — only inserts a marker block at top.
# Reversible: re-running with --revert removes the marker.

set -u

MEM_DIR="/root/.claude/projects/-root/memory"
LINTER="/root/AAA/scripts/lint-memory-phantoms.sh"
REGISTRY="/root/AAA/scripts/PHANTOM_REGISTRY_2026-09-21.md"
MODE="${1:-stamp}"  # stamp | revert

if [ "$MODE" != "stamp" ] && [ "$MODE" != "revert" ]; then
  echo "Usage: $0 [stamp|revert]"
  exit 1
fi

# Get current phantom-citing files
PHANTOM_FILES=$($LINTER 2>&1 | grep -E "^\/root/.claude/projects/-root/memory" | awk '{print $1}' | sort -u)

MARKER_START="<!-- PHANTOM-CITING-2026-09-21-START -->"
MARKER_END="<!-- PHANTOM-CITING-2026-09-21-END -->"

MARKER_BLOCK="${MARKER_START}
> ⚠ **PHANTOM-CITING (2026-09-21).** This file references paths that do not exist on the live filesystem. See \`/root/AAA/scripts/PHANTOM_REGISTRY_2026-09-21.md\`. Do NOT cite the phantom paths inside this file as fact. Re-run \`bash /root/AAA/scripts/lint-memory-phantoms.sh <thisfile>\` to see the current list.
${MARKER_END}"

count=0
for f in $PHANTOM_FILES; do
  [ -z "$f" ] && continue
  [ ! -f "$f" ] && continue
  # skip MEMORY.md (handled separately) and skip tonight's already-corrected files
  case "$(basename $f)" in
    MEMORY.md) continue ;;
    holes-exposed-2026-09-21.md) continue ;;
    tier-0-phantom-evidence-2026-09-21.md) continue ;;
  esac

  if [ "$MODE" = "stamp" ]; then
    if grep -q "$MARKER_START" "$f"; then
      continue  # already stamped
    fi
    # prepend marker
    TMP=$(mktemp)
    {
      echo "$MARKER_BLOCK"
      echo
      cat "$f"
    } > "$TMP"
    mv "$TMP" "$f"
    count=$((count + 1))
  else
    # revert: remove the marker block
    if grep -q "$MARKER_START" "$f"; then
      TMP=$(mktemp)
      awk -v start="$MARKER_START" -v end="$MARKER_END" '
        BEGIN { skip = 0 }
        $0 ~ start { skip = 1; next }
        $0 ~ end { skip = 0; next }
        skip == 0 { print }
      ' "$f" > "$TMP"
      # Also remove the leading blank line if it exists
      sed -i '1{/^$/d}' "$TMP" 2>/dev/null
      mv "$TMP" "$f"
      count=$((count + 1))
    fi
  fi
done

echo "$MODE: $count files affected"
echo "Reversibility: $0 revert restores originals"
exit 0