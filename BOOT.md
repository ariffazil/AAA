# BOOT.md — Session Boot Check

Run silently at the start of every session. Send to Telegram ONLY if something needs attention.

## Boot Sequence

1. **arifOS health**: `curl -s http://localhost:8080/health | python3 -c "import sys,json;d=json.load(sys.stdin);print('arifOS:', d['status'])"`
2. **Disk**: `df -h / | tail -1 | awk '{print "Disk:", $5, "used of", $2}'`
3. **Load**: `uptime | awk -F'load average:' '{print "Load:", $2}'`
4. **Containers**: `docker ps --filter health=unhealthy --format "{{.Names}}" | head -5`
5. **OpenClaw event loop**: check `sudo openclaw channels status 2>/dev/null | grep -i "degraded"`
6. **Webhook pending**: `curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo" | python3 -c "import sys,json;d=json.load(sys.stdin)['result'];print('Pending:', d.get('pending_update_count',0), 'Error:', d.get('last_error_message','none'))"`

## Rules

- If all clear → reply `BOOT_OK` (do NOT send to Telegram)
- If any check fails → send Telegram to 267378578:
  `SEV: [low/med/high] | WHAT: [one sentence] | EVIDENCE: [one signal] | NEXT: [one action]`
- Disk > 85% used → SEV: med
- Load > 6.0 → SEV: high
- Any unhealthy container → SEV: med
- Event loop degraded + pending > 10 → SEV: high

## Memory Context

After boot check, read if present:
- Today's memory: `/root/.openclaw/workspace/memory/$(date +%Y-%m-%d).md`
- Yesterday's memory: `/root/.openclaw/workspace/memory/$(date -d yesterday +%Y-%m-%d).md`

This gives you continuity from the previous session.
