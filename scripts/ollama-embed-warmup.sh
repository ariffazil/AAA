#!/bin/bash
# Keep nomic-embed-text hot for OpenClaw memory_search (<15s budget)
set -euo pipefail
curl -sf --max-time 60 \
  http://127.0.0.1:11434/api/embeddings \
  -H 'Content-Type: application/json' \
  -d '{"model":"nomic-embed-text","prompt":"keepalive"}' \
  -o /dev/null
