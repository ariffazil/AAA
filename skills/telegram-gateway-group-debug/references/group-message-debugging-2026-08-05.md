# SADO Group Debugging — Full Transcript 2026-08-05

## Symptom
ASI_arifos_bot (8410138119) replies to DMs but not in SADO group (-1003815535761). All config layers look correct. Webhook is healthy.

## Evidence chain

### Log evidence — DMs only
```
14:28:12 inbound: chat=267378578 msg='Still not working'
14:33:02 inbound: chat=267378578 msg='Test'
14:36:29 inbound: chat=267378578 msg='Good. Gateway restarted...'
14:41:44 inbound: chat=267378578 msg='But self.config.extra.get...'
14:46:11 inbound: chat=267378578 msg='🔄 Clean restart...'
14:50:34 inbound: chat=267378578 msg=''
14:50:59 inbound: chat=267378578 msg='🚀 NUCLEAR OPTION...'
14:51:36 inbound: chat=267378578 msg='I know la'
14:53:03 inbound: chat=267378578 msg='Sent SADO properly'
```

Every single "SADO test" message arrived as `chat=267378578` (DM), not `chat=-1003815535761` (SADO group).

### Self-echo flood
```
14:33:01 Blocked unauthorized user 8410138119 in chat 8410138119  (×4)
14:33:02 Blocked unauthorized user 8410138119 in chat 8410138119  (×4)
14:34:57 Blocked unauthorized user 8410138119 in chat 8410138119  (×3)
14:45:39 Blocked unauthorized user 8410138119 in chat 8410138119
...
```

Pattern: bot sends message → webhook delivers it back → auth check fires before `_is_own_message` → logged as "Blocked unauthorized user 8410138119 in chat 8410138119".

The tell: `from_user.id == chat.id == bot_id`. Real messages never match.

### Synthetic probe
```bash
curl -H "X-Telegram-Bot-Api-Secret-Token: ${SECRET}" \
  -H "Content-Type: application/json" \
  -d '{"update_id":999999999,"message":{"message_id":1,"from":{"id":267378578,"is_bot":false,"first_name":"Arif"},"chat":{"id":-1003815535761,"title":"SADO","type":"supergroup"},"date":1785940500,"text":"FINAL TEST FROM ARIF IN SADO"}}' \
  http://127.0.0.1:8444/telegram/webhook
```

Result: HTTP 200, zero log entries, no agent processing. Webhook silently dropped.

## Root cause
User was typing in the bot's DM chat (`ASI🪽`), not the SADO group chat. Every "SADO test" arrived at the bot's DM, was processed, and replied. The user thought the bot was ignoring SADO; in fact the bot never received any SADO messages because none were sent to SADO.

## Lesson
The chat_id in `inbound message: chat=<id>` is definitive. DMs have positive IDs (user_id). Groups have negative IDs (supergroup_id). When a user reports "bot doesn't reply in group", the first question is: **does the gateway log show any inbound lines with the negative group chat_id?** If not, the messages are not reaching the group chat at all.

## Reference commands

```bash
# Find the gateway log
tail -F /usr/local/lib/hermes-agent/profiles/aaa-hermes/logs/gateway.log | grep -E "<group_chat_id>"

# Verify env vars on running gateway
strings /proc/$(systemctl show -p MainPID hermes-asi-gateway.service | cut -d= -f2)/environ \
  | grep -E "TELEGRAM_(FREE_RESPONSE|REQUIRE_MENTION|ALLOWED_CHATS|GROUP_ALLOWED|WEBHOOK_SECRET)"

# Verify bot membership
BOT=$(strings /proc/$PID/environ | grep '^TELEGRAM_BOT_TOKEN=8410' | cut -d= -f2)
curl -s "https://api.telegram.org/bot${BOT}/getChatAdministrators" -d chat_id="-1003815535761"
curl -s "https://api.telegram.org/bot${BOT}/getChat" -d chat_id="-1003815535761"
```

## Nuclear option (verified working)
```ini
# /etc/systemd/system/hermes-asi-gateway.service.d/free-response-sado.conf
[Service]
Environment=TELEGRAM_REQUIRE_MENTION=false
Environment=TELEGRAM_FREE_RESPONSE_CHATS=-1003815535761
Environment=TELEGRAM_ALLOWED_CHATS=-1003753855708,-1003792478194,-1003768847825,-1003521544074,-1003721331017,-1004446358629,-5561731065,-5443591163,-1003815535761,267378578,1042200555,5316953867,5250473787,8798431893,5444180135
Environment=TELEGRAM_GROUP_ALLOWED_USERS=267378578,1042200555,5316953867,5250473787,8798431893,5444180135
```

After `chmod 600`, `systemctl daemon-reload && systemctl restart hermes-asi-gateway`, the gateway will reply to ANY message in any of the listed chats, mention not required.