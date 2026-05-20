# TREE777 — Agent Identity Matrix

**Purpose:** Central registry of all federation agents and their Telegram bot token ownership.  
**Why:** Prevent silent message routing failures when agents share tokens.  

---

## AGENT-TOKEN REGISTRY

| Agent | Bot Username | Token (last 6) | Status | Last Verified |
|-------|-------------|---------------|--------|---------------|
| OpenClaw | @AGI_ASI_bot | `...` | ✅ ACTIVE | 2026-05-19 |
| Hermes | @ASI_arifos_bot | `...` | ✅ ACTIVE | 2026-05-19 |
| A-FORGE Notifier | @AFORGE_NOTIFY_bot | `...` | ✅ ACTIVE | 2026-05-19 |
| Abang Sado Bot | @AbangSadoBot | — | 🔜 PENDING | — |

---

## VERIFICATION COMMAND

```bash
# Check all Telegram tokens in federation
grep -r "TELEGRAM_BOT_TOKEN\|botToken\|BOT_TOKEN" /root \
  --include="*.env" --include="*.yml" --include="*.yaml" --include="*.json" \
  -h 2>/dev/null | grep -v ".git\|.sessions\|node_modules" | sort -u

# Verify bot ownership
curl -s "https://api.telegram.org/bot<TOKEN>/getMe" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['result']['username'])"
```

---

## RULE (F1 AMANAH)

**Every agent MUST have a unique, dedicated Telegram bot token.**  
Shared token = Telegram sends all messages to ONE webhook = silent routing failure.  
No error is thrown. Messages just disappear.

---

## ADDING A NEW AGENT

1. Create new bot via @BotFather
2. Register in this matrix with token last 6 chars + verification date
3. Add to agent's config — NEVER reuse existing token
4. Run verification command after deployment

---

*Last updated: 2026-05-19*
*DITEMPA BUKAN DIBERI*