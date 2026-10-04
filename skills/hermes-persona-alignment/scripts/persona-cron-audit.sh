#!/usr/bin/env bash
# Verify cron + delivery wiring for a non-operator persona.
# Usage: ./persona-cron-audit.sh <persona-tg-id> [<persona-name>]
# Example: ./persona-cron-audit.sh 1042200555 syed

set -euo pipefail

PERSONA_ID="${1:-}"
PERSONA_NAME="${2:-persona}"

if [ -z "$PERSONA_ID" ]; then
  echo "Usage: $0 <persona-tg-id> [<persona-name>]"
  exit 2
fi

echo "=== $PERSONA_NAME ($PERSONA_ID) cron + delivery audit ==="
echo

# 1. Find cron jobs for this persona
echo "Cron jobs (L2 gateway):"
python3 -c "
import json
d = json.load(open('/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json'))
for j in d.get('jobs', []):
    if '$PERSONA_ID' in str(j.get('deliver', '')):
        print(f\"  - {j['name']} ({j['id']}) expr={j.get('schedule',{}).get('expr')} deliver={j.get('deliver')}\")
"

# 2. Verify deliver field is pinned to persona's chat (not 'origin')
echo
echo "Delivery pinning check (should be telegram:$PERSONA_ID, NOT 'origin' or 'local'):"
python3 -c "
import json
d = json.load(open('/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json'))
for j in d.get('jobs', []):
    if '$PERSONA_ID' in str(j.get('deliver', '')):
        d = j.get('deliver', '')
        if d == 'origin' or d == 'local':
            print(f\"  ⚠️  {j['name']}: deliver={d} (will NOT reach persona)\")
        elif d == 'telegram:$PERSONA_ID':
            print(f\"  ✅ {j['name']}: deliver={d}\")
        else:
            print(f\"  ❓ {j['name']}: deliver={d} (unrecognized)\")
"

# 3. Test hermes send works (verifies envoy PATH + env injection)
echo
echo "hermes send probe (verifies env injection):"
if hermes send -t "telegram:$PERSONA_ID" "[$PERSONA_NAME cron-audit] probe" 2>&1 | grep -qi "not configured\|not found"; then
  echo "  ⚠️  hermes send has env injection issue — fallback: source kunci-mas.env first"
  echo "     set -a && source /root/.secrets/kunci-mas.env && set +a"
else
  echo "  ✅ hermes send succeeded"
fi

# 4. Verify log file (where the persona's responses are appended)
echo
echo "Log file (where to append responses):"
ls -la /root/sado/mak-health/SYMPTOMS.md 2>/dev/null || echo "  (no SYMPTOMS.md yet — persona-specific path needed)"

# 5. Verify persona lane is loaded
echo
echo "Persona lane files:"
for f in "USER-$PERSONA_NAME" "MEMORY-$PERSONA_NAME" "SOUL-$PERSONA_NAME"; do
  if [ -f "/usr/local/lib/hermes-agent/profiles/aaa-hermes/memories/$f.md" ]; then
    echo "  ✅ $f.md"
  else
    echo "  ⚠️  $f.md missing"
  fi
done

echo
echo "=== audit complete ==="
