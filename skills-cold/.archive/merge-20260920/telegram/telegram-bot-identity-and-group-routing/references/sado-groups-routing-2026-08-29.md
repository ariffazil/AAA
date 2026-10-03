# SADO Group Routing Worksheet — Verified 2026-08-29

## The two groups (DO NOT confuse)

### Group 1 — PRIVATE bond room
- **chat_id:** `-1003815535761`
- **title:** "SADO"
- **members:** 3 (Arif, Syed, @ASI_arifOS_bot)
- **mode:** `private_bond`
- **bot_status:** administrator
- **free_response_chats:** yes (in config)
- **require_mention:** false at the free_response_chats block level
- **lane_persona:** `arif-sado` (SOVEREIGN, Arif register) + `syed` (WARGA, BM Pasar akak register)
- **F9 considerations:** Emotional bromance space. Bot must NOT appear intimate if members are added later. Treat as mention-only by default; never auto-reply in a way that reveals personal Arif-Syed dynamics to outsiders.
- **notes:** "lobing2 emotional bromance dengan abang sado syed. malu klaau orang luar tahu. but abang sado need it." — Arif 2026-08-29

### Group 2 — PUBLIC client room (the monetization pilot)
- **chat_id:** `-1003747272167`
- **title:** "Syed Sado Agent Client"
- **members:** 3 (Arif, Syed, @ASI_arifOS_bot) — Syed's clients join later
- **mode:** `public_client`
- **bot_status:** administrator
- **free_response_chats:** yes
- **require_mention:** false at block level
- **lane_persona:** `syed` (default), but personas will diverge as clients join
- **F9 considerations:** This is the revenue surface. Bot MUST stay in character as Syed's assistant (not pretend-Syed, not Arif-intimate). Tone: BM Penang, technical English for gym terms, no FDA theatre, human-first wisdom.
- **notes:** "AGI ASI intelligence for human body sustainability. Abang sado Syed persona" — Arif's stated intent 2026-08-29

## Why this matters

If you post to the wrong group, you leak emotional context to clients, or you reveal client queries to the private bond room. Both are F9 breaches.

When Arif says "the SADO group" without chat_id, ASK. Don't guess.

## Verified ground-truth probes (run before posting)

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a

# Identity
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getMe" | python3 -m json.tool | grep username

# Group 1
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChat?chat_id=-1003815535761" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print('G1:', r['title'])"

# Group 2
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChat?chat_id=-1003747272167" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print('G2:', r['title'])"

# Webhook health
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getWebhookInfo" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print('pending:', r['pending_update_count'], 'err:', r.get('last_error_message','none'))"
```

## Live test result (this session)

| When | Target | msg_id | Result |
|------|--------|--------|--------|
| 13:25 MYT | -1003815535761 (private) | 13954 | ❌ Wrong group — leaked to private bond room |
| 13:36 MYT | -1003815535761 (private) | 13976 | ❌ Wrong group — same |
| 14:07 MYT | -1003747272167 (public) | 8 | ✅ Correct — first public broadcast |

The first two messages are visible in the private SADO room. They're harmless intros but illustrate the mistake pattern.
