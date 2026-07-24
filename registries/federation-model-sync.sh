#!/usr/bin/env bash
# federation-model-sync — SOT-driven OpenCode config alignment
# Usage:
#   federation-model-sync           # check drift only
#   federation-model-sync --render  # regenerate config from SOT
#   federation-model-sync --verify  # validate alignment
#   federation-model-sync --help

set -e

script_dir="$(cd "$(dirname "$0")" && pwd)"
resolver="$script_dir/../src/resolvers/opencode_render.py"

case "${1:-}" in
  --render|-w)
    python3 "$resolver" --write --force
    echo "→ Source: /root/AAA/registries/models/AGENT_MODEL_MAP.json"
    echo "→ Target: /root/.config/opencode/opencode.json"
    echo ""
    echo "✅ Config regenerated. Run 'federation-model-sync --verify' to validate."
    ;;
  --verify|-v)
    python3 "$resolver" --verify "${@:2}"
    ;;
  --completeness|-c)
    echo "=== SOT Completeness Check (Path B — canonical roster) ==="
    python3 -c "
import sys
sys.path.insert(0, '$script_dir/../src/resolvers')
from opencode_render import load_sot, validate_sot_completeness, REQUIRED_SOT_AGENTS
sot = load_sot()
errors = validate_sot_completeness(sot)
print(f'Required agents: {len(REQUIRED_SOT_AGENTS)}')
print(f'SOT agents: {len(sot.get(\"agents\", []))} | providers: {len(sot.get(\"providers\", []))} | models: {len(sot.get(\"models\", []))}')
if errors:
    for e in errors: print(f'❌ {e}')
    sys.exit(1)
print('✅ All required agents present with primary_model + status.')
"
    ;;
  --help|-h)
    echo "federation-model-sync — SOT-driven OpenCode config alignment"
    echo ""
    echo "USAGE:"
    echo "  federation-model-sync           check drift only"
    echo "  federation-model-sync --render  regenerate config from SOT"
    echo "  federation-model-sync --verify  validate alignment (add --live for OR catalog check)"
    echo "  federation-model-sync --completeness  SOT agent roster check"
    echo ""
    echo "SOT: /root/AAA/registries/models/AGENT_MODEL_MAP.json"
    echo "     (symlinked as /root/.config/federation-models.json)"
    ;;
  *)
    python3 "$resolver"  # dry-run by default
    ;;
esac
