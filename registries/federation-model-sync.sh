#!/usr/bin/env bash
# federation-model-sync — SOT-driven OpenCode config alignment
# Usage:
#   federation-model-sync           # check drift only
#   federation-model-sync --render  # regenerate config from SOT
#   federation-model-sync --verify  # validate alignment
#   federation-model-sync --help

set -e

script_dir="$(cd "$(dirname "$0")" && pwd)"
resolver="$script_dir/../AAA/src/resolvers/opencode_render.py"

case "${1:-}" in
  --render|-w)
    python3 "$resolver" --write
    echo "→ Source: /root/AAA/registries/models/AGENT_MODEL_MAP.json"
    echo "→ Target: /root/.config/opencode/opencode.json"
    echo ""
    echo "✅ Config regenerated. Run 'federation-model-sync --verify' to validate."
    ;;
  --verify|-v)
    python3 "$resolver" --verify
    ;;
  --help|-h)
    echo "federation-model-sync — SOT-driven OpenCode config alignment"
    echo ""
    echo "USAGE:"
    echo "  federation-model-sync           check drift only"
    echo "  federation-model-sync --render  regenerate config from SOT"
    echo "  federation-model-sync --verify  validate alignment"
    echo ""
    echo "SOT: /root/AAA/registries/models/AGENT_MODEL_MAP.json"
    echo "     (symlinked as /root/.config/federation-models.json)"
    ;;
  *)
    python3 "$resolver"  # dry-run by default
    ;;
esac
