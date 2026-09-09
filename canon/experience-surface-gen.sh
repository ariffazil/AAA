#!/bin/bash
# experience-surface-gen.sh — Regenerate experience surface via metabolism engine
# Delegates to experience-metabolism.py for all computation
# Output: experience_surface.md + /tmp/experience_boot_context.md
set -euo pipefail

ENGINE="/root/.hermes/scripts/experience-metabolism.py"

if [ ! -f "$ENGINE" ]; then
  echo "ERROR: experience-metabolism.py not found at $ENGINE" >&2
  exit 1
fi

# Run full pipeline (boot context + surface + measurement)
python3 "$ENGINE" --mode full --json > /dev/null 2>&1

echo "Experience metabolism pipeline executed: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
