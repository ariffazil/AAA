#!/usr/bin/env bash
# detect-design-drift.sh — find ALL archived copies of a target file
# Sorted by file size = design age (largest = most design investment)
#
# Usage: detect-design-drift.sh <target-relative-path>
#   e.g.: detect-design-drift.sh makcikgpt-md/index.html
#         detect-design-drift.sh words/writing/index.html
#
# Verified 2026-08-11 — caught the MakcikGPT design drift from 14KB
# live (degraded) to 19KB archive (rich palette with hero canvas).

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <target-relative-path>" >&2
  echo "  e.g.: $0 makcikgpt-md/index.html" >&2
  exit 1
fi

TARGET="$1"

echo "=== Live ==="
find /var/www -name "$(basename "$TARGET")" -path "*$(dirname "$TARGET")*" 2>/dev/null \
  | xargs -I {} sh -c 'echo "$(stat -c%s {})B  $(stat -c%y {} | cut -d. -f1)  {}"' 2>/dev/null \
  | head -5

echo ""
echo "=== Archived copies (sorted by file size, largest = most design investment) ==="
find /root -name "$(basename "$TARGET")" -path "*$(dirname "$TARGET")*" 2>/dev/null \
  | xargs -I {} sh -c 'echo "$(stat -c%s {})B  $(stat -c%y {} | cut -d. -f1)  {}"' 2>/dev/null \
  | sort -nr | head -20

echo ""
echo "=== Git history (all branches) ==="
git -C /root/arif-fazil.com log --all --oneline -- "*$TARGET" 2>/dev/null | head -10

echo ""
echo "=== Decision matrix ==="
echo "If live is SMALLEST but archive has a LARGER version:"
echo "  → ask Arif: 'Found archived design from <date>, <size> bytes — restore?'"
echo ""
echo "If live is LARGEST:"
echo "  → live is canonical, no archaeology needed"
echo ""
echo "If git log shows recent (post-live-deploy) commits touching this path:"
echo "  → check git diff vs live — may indicate sibling agent revert"
