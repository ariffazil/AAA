---
name: telegram-bot-privacy-mode-debug
description: "Diagnose Telegram bot deafness — bot ignores non-mention group msgs despite requireMention:false. Root cause is Telegram server-side privacy mode enforced by Bot API, not OpenClaw config. Fix: BotFather /setprivacy Disable."
tags: [telegram, openclaw, privacy-mode, botfather]
last_updated: 2026-05-01
---

# Telegram Bot Privacy Mode Debug

## Trigger
OpenClaw bot configured with `requireMention: false` but not responding to messages in groups. Bot appears "deaf" to messages that don't @mention it.

## Root Causes (Two Distinct Failure Modes)

### Cause A: BotFather Privacy Mode (Most Common)
Telegram bots have **server-side privacy mode** enforced by Telegram's Bot API Server — messages are blocked at Telegram's servers before they reach OpenClaw. By default, bots only receive:
- Messages @mentioning the bot
- Commands (starting with `/`)
- Replies to the bot's messages

### Cause B: Group Missing from OpenClaw Allowlist
**Group ID not in `groups` block** — the bot IS in the group, IS visible to Telegram (getUpdates confirms), but OpenClaw silently drops messages because `groupPolicy: allowlist` and the group ID isn't in the config.

**Diagnosis for Cause B:**
1. `getUpdates` API confirms bot CAN see the group ✅ (group_id appears in updates)
2. Bot has `can_read_all_group_messages: true` ✅
3. Bot does NOT respond even to @mentions in that specific group
4. Other groups in the config work fine

**Fix for Cause B:**
Add the group ID to `/root/.openclaw/openclaw.json` under `channels.telegram.groups`:
```json
"-1003890512851": {
  "requireMention": false
}
```
Then restart: `systemctl --user restart openclaw-gateway.service`

### Cause A vs Cause B Quick Check
| Check | Cause A (Privacy) | Cause B (Missing Allowlist) |
|-------|-------------------|----------------------------|
| Bot in group? | ✅ yes | ✅ yes |
| `can_read_all_group_messages`? | ❌ no (BotFather) | ✅ yes |
| Responds to @mention? | ❌ no | ❌ no |
| getUpdates shows group? | ❌ no | ✅ yes |

---

## Fix — Must use BotFather (Cause A)

## Diagnosis Checklist
1. Can bot receive DMs? (If yes → privacy mode is likely the only blocker)
2. Does bot respond to @mentions in groups? (If yes → privacy mode is the issue for non-mention messages)
3. Check OpenClaw `requireMention` setting: `grep -n "requireMention" /root/.openclaw/openclaw.json`
4. Check group policy: `grep -n "groupPolicy\|dmPolicy" /root/.openclaw/openclaw.json`

## Fix — Must use BotFather
```
1. Telegram → open @BotFather
2. Send: /setprivacy
3. Select your bot (@YourBotName)
4. Choose: "Disable" ← allows bot to read ALL messages in the group
```

After BotFather disable:
- Bot receives ALL messages in groups it is added to
- OpenClaw's `requireMention: false` then works as intended (no @mention needed to trigger response)
- OpenClaw's `groupPolicy: allowlist` still restricts which groups are accepted

## Verification
Have any group member send "hello" (no @mention, no /command) — bot should respond if:
- `requireMention: false` is set for that group ✅
- Privacy mode is "Disabled" via BotFather ✅
- Bot is in the group ✅
- `groupPolicy: allowlist` is set ✅

## Common Misconceptions
| Misconception | Reality |
|---------------|---------|
| "Set `privacy_mode: 'disabled'` in openclaw.json" | No such config field exists in OpenClaw |
| "Set `requireMention: true`" | That makes it WORSE — requires mentions to respond |
| "Restart OpenClaw will fix it" | Privacy is Telegram-server-enforced, not a config issue |
| "DM me and I'll check logs" | DMs work fine with privacy mode — only group non-mentions are blocked |

## Related
- OpenClaw config: `/root/.openclaw/openclaw.json`
- BotFather: @BotFather on Telegram
