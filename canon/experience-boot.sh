#!/bin/bash
# experience-boot.sh — Generate experience context block for session init
# Delegates to experience-metabolism.py Phase A
set -euo pipefail

ENGINE="/root/.hermes/scripts/experience-metabolism.py"
OUTPUT="/tmp/experience_boot_context.md"

if [ ! -f "$ENGINE" ]; then
  echo "<!-- experience-metabolism.py not found -->" > "$OUTPUT"
  exit 0
fi

# Run boot-only mode
python3 "$ENGINE" --mode boot --json > /dev/null 2>&1

if [ -f "$OUTPUT" ]; then
  echo "Experience boot context generated: $(wc -c < "$OUTPUT") bytes"
else
  echo "WARNING: boot context not generated" >&2
fi
