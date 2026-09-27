# Telegram Group Access — Live Verification Recipe

> **When:** Use after any `hermes-id-zen add-group` or `hermes-id-zen add-user`, or whenever someone asks "make sure everyone can access HERMES in this group", or when a family/lane lane is silent and the cause is unknown. NOT for read-only message digest (use `arif-digest-group-chat`).
>
> **Why:** `hermes-id-zen add-*` mutates `config.yaml` + `lanes.yaml` + scaffolds memory files, but none of that proves the bot is *actually* seeing and replying in the group at runtime. This recipe proves the full chain: Telegram-side presence → app-side wiring → gateway polling → member registry alignment. Cheaper than asking Arif "is it working?" from his phone.

## Procedure

### 1. Source the bot token from the env

```bash
source /root/.secrets/kunci-root.env
# Candidate vars: HERMES_TELEGRAM_BOT_TOKEN, ASI_ARIFOS_BOT_TOKEN, ASI_AR...OKEN
# If none exported, grep /root/.secrets/kunci-root.env for `ASI.*TOKEN` and export.
```

### 2. Probe the group via Bot API — five calls in one shell

```python
import os, urllib.request, json
token = os.environ['HERMES_TELEGRAM_BOT_TOKEN']
chat_id = '<target_chat_id>'   # e.g. '-1003768847825' for Kanak-kanak

def get(method, extra=''):
    url = f'https://api.telegram.org/bot{token}/{method}?chat_id={chat_id}{extra}'
    return json.loads(urllib.request.urlopen(url, timeout=10).read())

# Five calls — each tells you a different layer of the stack:
# - getChat               → title, type, active_usernames, permissions, photo, invite_link
# - getChatAdministrators → admins list (user_id, is_bot, status)
# - getChatMemberCount    → total member count
# - getMe                 → bot identity + can_read_all_group_messages flag
# - getUpdates?limit=3    → if EMPTY: gateway is not polling (or webhook-only)
# - getWebhookInfo        → has_custom_certificate, pending_update_count
```

### 3. Cross-reference live state against three sources

| What | Where to check | What "OK" looks like |
|---|---|---|
| Bot Telegram-side | `getMe` result → `can_read_all_group_messages` | `true` (BotFather Group Privacy OFF) |
| Bot in group as admin | `getChatAdministrators` contains the bot user_id | bot present, role = administrator |
| App config wires the chat | `config.yaml` → `telegram.allowed_chats` AND `telegram.extra.channel_prompts[<chat_id>]` | chat_id present in both; for family/peer rooms, also in `free_response_chats` |
| Human/agent members registered | `~/.hermes/lanes/people.yaml` → entries whose `identities[].value` matches each human member's telegram_user_id | every human has a sourced `fact` block with `source: arif (F13 sovereign)` and `scope: shared` for shared rooms |
| Gateway polling, right profile | `hermes gateway status` | status line says running; profile served = the one this session is using (default or `aaa-hermes` etc.) |

### 4. Report to the human in this shape (BM Penang, factual)

```
## Group Info (live dari Bot API)
| Field | Value | (table — title, chat_id, type, members, invite_link)

## Members (live)
| # | Who | Role | Notes | (table — each member with user_id + admin flag)

## Config wiring — semua ✓ (or ✗ with the gap)
- ALLOWED_CHATS ✓/✗
- FREE_RESPONSE_CHATS ✓/✗
- require_mention: false ✓/✗
- Bot Telegram-side: can_read_all_group_messages: TRUE/FALSE
- people.yaml: <human ids> registered F13-admit, tier FAMILY/EXTERNAL/etc.

## Satu gap jujur (only if real)
- gateway multiplex pending, OR a missing people.yaml entry, etc.
```

### 5. Honest answer to "make sure X can access HERMES"

Only say "Y=already wired" after steps 2-3 pass for ALL three layers (Telegram bot presence, app config, people registry). If any layer fails, name the gap plainly — never fabricate "yes everything works" to give a clean answer.

## Pitfalls

- **`systemctl --user is-active hermes-gateway` is not the truth.** It can show `inactive` while a standalone gateway PID runs (look for `gateway run --replace` in `ps -ef`). `hermes gateway status` is the source of truth and exposes the multiplex warning ("standalone: serves only default profile"). When multiple profiles exist (`aaa-hermes`, `hermes_apex`, `hermes_asi`, `hermes_forge`), the standalone gateway leaves them all silent — fix is `hermes gateway migrate --multiplex`. Never declare "gateway OK" from the systemd line alone.

- **Bot API cannot fetch retroactive chat history.** `getUpdates` returns updates since the bot started polling OR nothing if polling is paused. "Digest all messages this group ever sent" requires a userbot client (Telethon/Pyrogram) authenticated as a human account using `api_id` + `api_hash` from `my.telegram.org`. Don't promise "I will read everything" without naming the userbot requirement. Verify the package is actually installed (`python3 -c 'import telethon'`) before claiming capability — it usually isn't in the federation root venv.

- **`can_read_all_group_messages: false` means the bot only sees `/commands` + explicit replies.** Default is `true` for new bots, but if anyone ever re-toggled Group Privacy in BotFather, it sticks silently. Always re-check `getMe` per probe, don't trust past state. If `false`: fix is `@BotFather → /setprivacy → Disable`, a manual BotFather step, NOT a config edit. Don't claim "config wired" when the privacy mode is actually off.

- **`allowed_chats` ≠ `free_response_chats`.** A chat in `allowed_chats` only replies to commands/@mentions; adding it to `free_response_chats` (or chat-level `require_mention: false`) is what makes HERMES respond to ordinary messages. For family/peer rooms, both must be true. The `channel_prompts[<chat_id>]` block in `config.yaml` carries the per-room register/instruction; the chat being absent from it is a separate gap that breaks the room's voice even when the bot is wired.

- **Family-member tier label drifts.** A sibling admitted as `tier: kanak-kanak` because someone said "adik" once was corrected by F13 six days later to `tier: FAMILY, lab support, full agent capability`. The drift cost a four-file sync (person card + registry + manifest + identity table). When a probe reveals a new family member, cross-check the tier against F13's statement, not lexical inference. If the tier line is missing or generic, flag it for confirmation rather than guessing.

- **Vision-call fabrication on family photos.** A vision call returning no result is not license to invent who is in the photo. Name members from `people.yaml` text fields (Arif's own words) — never from facial inference. If no text source exists, ask Arif who is in the photo. The `arif-family-members` skill states this rule; repeat it because the failure mode recurs whenever a probe surfaces a photo.

## One-liner recipe

```bash
source /root/.secrets/kunci-root.env && python3 -c "
import os, urllib.request, json
t = os.environ['HERMES_TELEGRAM_BOT_TOKEN']
c = '-1003768847825'  # <-- swap for target
for m in ['getChat', 'getChatAdministrators', 'getChatMemberCount']:
    print('===', m)
    print(urllib.request.urlopen(f'https://api.telegram.org/bot{t}/{m}?chat_id={c}', timeout=10).read().decode()[:500])
print('=== getMe'); print(urllib.request.urlopen(f'https://api.telegram.org/bot{t}/getMe', timeout=10).read().decode()[:400])
"
```