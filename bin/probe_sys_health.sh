#!/bin/bash
# ==============================================================================
# OpenClaw System Probe -> /root/AAA/state/sys_health.json
# F1 Safe: Read-only probes. Atomic write. Prevents Hermes read collisions.
# Tri-Agent: Pure OpenClaw domain. Hermes consumes, never probes.
# ==============================================================================

STATE_DIR="/root/AAA/state"
STATE_FILE="$STATE_DIR/sys_health.json"
TMP_FILE="$STATE_DIR/sys_health.tmp.json"
LOG_FILE="/root/AAA/logs/openclaw_errors.log"

# Source vault secrets for DeepSeek API key
set -a && source /root/.secrets/vault.env && set +a

mkdir -p "$STATE_DIR"

# ------ 1. Timestamp (UTC) ------
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# ------ 2. DeepSeek Liveness (retry: models endpoint → chat ping, 5s timeouts, F1-safe) ------
DS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://api.deepseek.com/v1/models 2>/dev/null)
# Retry with a chat completion ping if models endpoint flakes (transient 401)
if [ "$DS_STATUS" != "200" ]; then
  DS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 -X POST \
    https://api.deepseek.com/v1/chat/completions \
    -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"ping"}],"max_tokens":1}' 2>/dev/null)
fi
[ -z "$DS_STATUS" ] && DS_STATUS=000

# ------ 3. VAULT999 Integrity ------
# Check outcomes.jsonl exists, non-empty, and parseable
if [ -f /root/VAULT999/outcomes.jsonl ] && [ -s /root/VAULT999/outcomes.jsonl ]; then
    # Verify last line is valid JSON
    tail -1 /root/VAULT999/outcomes.jsonl | python3 -c "import json,sys; json.load(sys.stdin)" 2>/dev/null && VAULT_SEAL=true || VAULT_SEAL=false
else
    VAULT_SEAL=false
fi

# ------ 4. Disk Usage (Root Partition) ------
DISK_PCT=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
[ -z "$DISK_PCT" ] && DISK_PCT=0

# ------ 5. Git Dirty Count (all 6 organs) ------
for repo in /root/arifOS /root/A-FORGE /root/AAA /root/GEOX /root/WEALTH /root/WELL; do
    count=$(git -C "$repo" status --porcelain 2>/dev/null | wc -l)
    GIT_DIRTY=$((GIT_DIRTY + count))
done
[ -z "$GIT_DIRTY" ] && GIT_DIRTY=0

# ------ 6. Organ Health (systemd) ------
# Check: arifos, a-forge, aaa, geox, wealth, well
FAILED_ORGANS=$(systemctl list-units --state=failed --no-legend --plain 2>/dev/null | grep -cE 'arifos|a-forge|aaa|geox|wealth|well')
if [ "$FAILED_ORGANS" -eq 0 ]; then
    ORGAN_HEALTH="ALL_GREEN"
else
    ORGAN_HEALTH="SYSTEM_DEGRADED"
fi

# ------ 7. Generate Flat JSON (atomic write via tmp + mv) ------
jq -n \
  --arg ts "$TS" \
  --argjson ds_status "$DS_STATUS" \
  --argjson vault "$VAULT_SEAL" \
  --argjson disk "$DISK_PCT" \
  --argjson git "$GIT_DIRTY" \
  --arg organ "$ORGAN_HEALTH" \
  '{
    timestamp_utc: $ts,
    deepseek_api_status: $ds_status,
    vault_seals_intact: $vault,
    disk_usage_percent: $disk,
    git_dirty_count: $git,
    organ_health: $organ
  }' > "$TMP_FILE" 2>> "$LOG_FILE"

# Atomic move: Hermes will never read a partial file
mv "$TMP_FILE" "$STATE_FILE" 2>> "$LOG_FILE"

echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] sys_health.json written." >> "$LOG_FILE"
