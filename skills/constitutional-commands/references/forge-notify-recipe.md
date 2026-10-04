# FORGE Notification Routing — Working Recipe (2026-08-08)

## The Fix

`/root/A-FORGE/duties/forge-notify.sh` was posting to Arif's DM. He wanted AAA group. Two bugs:

1. `CHAT_ID` was `267378578` (user ID) → should be `-1003753855708` (group ID with `-100` supergroup prefix)
2. `parse_mode` was declared in function signature but NOT passed to curl → Markdown didn't render

## Verified Diff

```bash
# Before
CHAT_ID="267378578"
# ...
RESPONSE=$(curl -sf -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  -d text="${MESSAGE}" \
  --max-time 10 2>/dev/null || echo '{"ok":false}')

# After
CHAT_ID="-1003753855708"
# ...
RESPONSE=$(curl -sf -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  -d text="${MESSAGE}" \
  -d parse_mode="${PARSE_MODE}" \
  --max-time 10 2>/dev/null || echo '{"ok":false}')
```

## Live Test (executed)

```bash
bash /root/A-FORGE/duties/forge-notify.sh "🧪 *FORGE → AAA Group* — test post from @arifOS_bot. Chat = -1003753855708. Markdown should render.
Issues: 0 | Warnings: 0"
```

Output: `[NOTIFY] Sent to AAA group (-1003753855708)` — exit 0. Formatting intact in Telegram.

## Duty Scripts That Use forge-notify.sh

| Script | Schedule | Triggers notify? |
|---|---|---|
| `forge-constitutional-sync.sh` | 07:00 UTC / 15:00 MYT | Always (compliance brief) |
| `forge-vitality-pulse.sh` | 15:00 UTC / 23:00 MYT | Always (vitality brief) |
| `forge-drift-scanner.sh` | 02:00 UTC / 10:00 MYT | Only on DRIFT_FOUND (silent when clean) |

All three will now auto-post to AAA group. No more copy-paste from DM.

## Why -100 Prefix

Telegram supergroup IDs use `-100` prefix for negative identifiers. Without it:
- Just `1003753855708` (positive) → may go to wrong destination or silently fail
- `-1003753855708` (negative) → correct supergroup

The `-100` prefix is a Telegram API convention for "this is a supergroup, not a user or basic group."

## Token Source

```
TOKEN_FILE="/root/.secrets/tokens/telegram-opencode-bot"
```

This is the FORGE bot (`@arifOS_bot`) token. NOT the OpenClaw GUTS token (`telegram-agi-asi-bot`). The same FORGE bot account posts into the AAA group — destination is the chat_id, identity is the token.
