# SADO Group Rollout — 2026-08-29 Session Reference

First session the rollout doctrine was extracted from. The bot was declared "live test successful" after only outbound delivery returned `ok:true`. Customer (Syed) and Arif then saw the bot fail to auto-reply in the group. This file captures the actual transcript so future rollouts can avoid the same failure.

## Session shape

- Group: SADO supergroup, `chat_id=-1003815535761`, 3 members (Arif, Syed @rico_ricaldo_33, @ASI_arifOS_bot)
- Bot identity: `@ASI_arifOS_bot`, ID `8410138119`, status `administrator` in group
- Bot token: `ASI_ARIFOS_BOT_TOKEN` (not `TELEGRAM_BOT_TOKEN` — the token name is misleading; verify with `getMe`)
- Gateway: `hermes-asi-gateway.service`, journal in `journalctl -u hermes-asi-gateway`
- Lane config: `/root/HERMES/lanes/lanes.yaml` had `arif-sado` and `syed` both keyed to the same chat_id with different user_ids (correct pattern)

## What was actually verified before "live" claim

- `sendMessage` returned `ok:true`, `message_id=13954`, `chat.id=-1003815535761`
- `getChatMember` returned bot as `administrator` with full perms
- `getWebhookInfo` returned `pending_update_count=0`, `last_error=none`, all update types enabled
- `free_response_chats` in `/root/.hermes/config.yaml` included `-1003815535761`

**What was NOT verified:** inbound→agent→reply round-trip from any human member.

## The actual failure

Gateway journal over the next 15 minutes showed:

1. **TTS pipeline timeout storm.** Every reply turn called `iarif_tts_pipeline.sh` which hung 120s and threw `subprocess.TimeoutExpired`. Log lines:
   ```
   subprocess.TimeoutExpired: Command 'bash /root/AAA/engines/iarif_tts_pipeline.sh /tmp/tmp9u33j0ln/input.txt /tmp/hermes_voice/tts_reply_c4d753b21d5e.wav' timed out after 120.0 seconds
   ```
   Five timeouts between 13:38 and 13:51. Every one killed the agent turn before the text reply could be sent.

2. **Hook handler crash.** Recurring line:
   ```
   [hooks] Error in handler for 'agent:end': handle() takes 1 positional argument but 2 were given
   ```
   Same for `agent:start`. Hooks crashed but did not block outbound (separate failure mode from TTS).

3. **Bot pre-filter blocking own messages.** Repeated:
   ```
   [Telegram] Blocked unauthorized user 8410138119 in chat 8410138119
   ```
   The bot's own user ID is not in `TELEGRAM_ALLOWED_USERS`. This is a separate bug — bot echoing its own outbound messages back to itself and the prefilter swallowing them. Not the cause of customer-side silence but a config drift that should be fixed.

4. **No inbound SADO traffic in journal.** Searches for `3815535761`, `SADO`, `ariffazil`, `1042200555` in `journalctl -u hermes-asi-gateway --since "30 min ago"` returned zero matches. Either no human posted in the group, or the messages were processed in a turn that didn't surface chat_id in journal — both worth verifying before next rollout.

## Recovery path

1. Switch the group reply mode to **text-only**. Do not call TTS in the default reply path. Voice via explicit `/voice` slash command only.
2. Investigate why `iarif_tts_pipeline.sh` hangs. Likely causes: GPU rental lag, MiniMax speech-2.8-hd seed step stalling, terminal F0 lock step hanging. Fix root cause before re-enabling voice-by-default.
3. Add bot's own ID `8410138119` to `TELEGRAM_ALLOWED_USERS` to silence the self-echo prefilter spam (cosmetic, not blocking).
4. Verify each leg of the round-trip with two non-Arif humans before declaring live. Syed and one client.
5. Fix hook handlers (`agent:end`, `agent:start` take 2 args, currently takes 1) — wrap in try/except so they don't crash on every turn.

## Honest bridge output that should have happened

Instead of "live test successful", the bridge contract for this session was:

> "Bot identity confirmed (`@ASI_arifOS_bot`, admin in group, webhook healthy, 0 pending). Outbound `sendMessage` works (L1 only). Round-trip belum witness — Syed tolong post satu soalan dalam group, aku monitor webhook pickup. Kalau reply tak sampai dalam 30s, suspect TTS latency amplifier."

That sentence is what would have surfaced the latency amplifier before Arif called it "monetization-grade fail".

## Diagnostic one-liner (copy/paste-ready)

```bash
set -a && source /root/.secrets/kunci-mas.env && set +a && \
echo "=== Bot identity ===" && \
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getMe" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"@{r['username']} id={r['id']}\")" && \
echo "=== Group membership ===" && \
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChatMember?chat_id=-1003815535761&user_id=8410138119" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"status={r['status']}\")" && \
echo "=== Webhook ===" && \
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getWebhookInfo" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"pending={r['pending_update_count']} err={r.get('last_error_message','none')}\")" && \
echo "=== Gateway health (last 5 min) ===" && \
journalctl -u hermes-asi-gateway --since "5 minutes ago" --no-pager 2>&1 | grep -E "TimeoutExpired|Flood control|Blocked unauthorized|agent:end" | wc -l
```

Last line = "0" means clean. Anything >3 = roll back to text-only and notify Arif.
