---
name: FORGE-telegram-audit
id: forge-telegram-audit
version: 1.1.0
risk_tier: low
description: 'Automated TREE777 security checks for Telegram bot tokens, webhook isolation,
  bot permission scope, and A2A bridge security. v1.1.0: organ paths from registry,
  ports from live probes. USE WHEN: "telegram audit", "bot security", "webhook check",
  "token isolation", "TREE777 check", "telegram permissions".'
owner: A-FORGE
floor_scope:
- F1
- F2
- F4
- F11
- F12
- F13
autonomy_tier: T0
capability_tier: fed-long-context
ecology_state: WARM
---
# Telegram Security Audit (TREE777) — Probe-Based v1.1.0

**Automated Telegram bot security checks — token isolation, webhook exposure, permission scope.**

## Preflight: Discover Paths and Ports

**DO NOT hardcode.** Read from organ registry and live config:

```bash
# Discover organ source paths
python3 -c "
import yaml
with open('/root/AAA/federation/organs.yaml') as f:
    reg = yaml.safe_load(f)
for o in reg.get('organs', []):
    if o['id'] in ('aaa','arifos','aforge','hermes'):
        print(f'{o[\"id\"]}: src={o.get(\"source_path\",\"?\")} port={o.get(\"port\",\"?\")}')
"

# Read bot config paths from live services
# OpenClaw config: check systemd unit for --config flag
systemctl cat openclaw 2>/dev/null | grep -oP '/[^\s]+\.json' | head -3
# Hermes config
systemctl cat hermes 2>/dev/null | grep -i config | head -3
```

## TREE777 Protocol Checks

### T1 — Token Isolation
```bash
# Bot tokens should be isolated in their service configs
# NEVER in git-tracked files

# Scan for leaked tokens — use registry-derived paths
AAA_PATH=$(python3 -c "import yaml;r=yaml.safe_load(open('/root/AAA/federation/organs.yaml'));print([o['source_path'] for o in r['organs'] if o['id']=='aaa'][0])")
ARIFOS_PATH=$(python3 -c "import yaml;r=yaml.safe_load(open('/root/AAA/federation/organs.yaml'));print([o['source_path'] for o in r['organs'] if o['id']=='arifos'][0])")

# Scan git-tracked paths for tokens (should return 0)
grep -r "tg\|telegram\|bot" "$AAA_PATH" 2>/dev/null | grep -i token | wc -l
grep -r "tg\|telegram" "$ARIFOS_PATH" 2>/dev/null | grep -i token | wc -l
```

### T2 — Webhook Exposure
```bash
# Webhook should NOT be publicly exposed without auth
# Probe Telegram API for webhook info
BOT_TOKEN=$(cat /root/.openclaw/tg_token 2>/dev/null || echo "")
if [ -n "$BOT_TOKEN" ]; then
  curl -s "https://api.telegram.org/bot$BOT_TOKEN/getWebhookInfo" | jq '{url: .result.url, has_custom_certificate: .result.has_custom_certificate}'
fi

# Check webhook port from systemd unit, not hardcoded
WEBHOOK_PORT=$(systemctl cat openclaw 2>/dev/null | grep -oP 'port[= ]\K[0-9]+' | head -1 || echo "8787")
echo "Webhook port: $WEBHOOK_PORT"
ss -tlnp | grep "$WEBHOOK_PORT"
```

### T3 — Bot Permissions
```bash
BOT_TOKEN=$(cat /root/.openclaw/tg_token 2>/dev/null || echo "")
if [ -n "$BOT_TOKEN" ]; then
  curl -s "https://api.telegram.org/bot$BOT_TOKEN/getMe" | jq '{username: .result.username, can_join_groups: .result.can_join_groups, can_read_all_group_messages: .result.can_read_all_group_messages, supports_inline_queries: .result.supports_inline_queries}'
fi
```

### T4 — A2A Bridge Security
```bash
# Discover A2A port from organ registry
A2A_PORT=$(python3 -c "import yaml;r=yaml.safe_load(open('/root/AAA/federation/organs.yaml'));print([o.get('a2a_port',o.get('port')) for o in r.get('organs',[]) if o['id']=='aaa'][0])")
echo "A2A port (from registry): $A2A_PORT"

ss -tlnp | grep "$A2A_PORT"
curl -s -o /dev/null -w "%{http_code}" "http://localhost:$A2A_PORT/.well-known/agent-card.json"
```

### T5 — Bot Separation
```bash
# @AGI_ASI_bot (OPENCLAW) vs @ASI_arifos_bot (Hermes)
# Separate processes, separate tokens, separate contexts
ps aux | grep -E "hermes|openclaw|telegram" | grep -v grep
```

### T6 — Log Exposure
```bash
# Check logs don't contain plaintext tokens
# Log paths from systemd journal or service config
for logdir in /var/log /root/.openclaw/logs; do
  [ -d "$logdir" ] && echo "Checking $logdir..." && grep -rc "bot[0-9]" "$logdir" 2>/dev/null | grep -v ":0$" | head -5
done
```

### T7 — Rate Limiting
```bash
# Check for 429 errors — probe journalctl, not hardcoded log paths
journalctl -u openclaw --since "24h ago" --no-pager 2>/dev/null | grep -c "429\|Too Many Requests"
journalctl -u hermes --since "24h ago" --no-pager 2>/dev/null | grep -c "429\|Too Many Requests"
```

## TREE777 Report

```
TREE777 TELEGRAM SECURITY AUDIT
═══════════════════════════════════════
Time: YYYY-MM-DD HH:MM UTC

✅/❌ T1 Token Isolation — git-tracked paths clean
✅/❌ T2 Webhook Exposure — local-only with auth
✅/❌ T3 Bot Permissions — least privilege
✅/❌ T4 A2A Bridge — localhost only
✅/❌ T5 Bot Separation — separate PIDs + tokens
✅/❌ T6 Log Exposure — no plaintext tokens
✅/❌ T7 Rate Limits — no 429 errors

OVERALL: ✅ PASS | ⚠️ WARNINGS | ❌ FAIL
═══════════════════════════════════════
```

## De-hardcoding Log (v1.1.0)
- Organ paths (AAA, arifOS) read from `/root/AAA/federation/organs.yaml`
- A2A port (18001) discovered from organ registry
- Webhook port (8787) probed from systemd unit config
- Log scanning uses journalctl (live) instead of hardcoded log paths
- Bot config paths discovered via systemctl cat + grep
- Telegram API URLs and token file paths kept (external API + standard locations)
