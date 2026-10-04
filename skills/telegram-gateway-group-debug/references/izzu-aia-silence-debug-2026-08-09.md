# Izzu AIA Group Silence — Debug Transcript (2026-08-09)

## Symptom

Izzu (Telegram ID 1024343313) posts in AIA group (-1003521544074). Hermes bot ignores completely. Arif (267378578) and Aliff (1237635275) messages are processed normally in the same group.

## Diagnostic path

### Step 1: Lane config — RED HERRING
Found `lane-izzu.json` with wrong group ID (`-1003815535761` = SADO instead of `-1003521544074` = AIA). **This was NOT the cause.** The lane_switch plugin reads from `/root/HERMES/lanes/lanes.yaml` (canonical), NOT from `lane-*.json` files. The `lanes.yaml` had correct triggers for both `izzu` (DM) and `izzu-aia` (group) lanes.

### Step 2: Adapter code analysis
Read `adapter.py:_should_process_message()` and `_is_user_authorized_from_message()`. Both should have passed — AIA is in `free_response_chats`, Izzu is in `allow_from` and `group_allow_from`.

### Step 3: Zero log entries — THE SMOKING GUN
```
grep -c '1024343313' gateway.log → 0
grep -c '1024343313' agent.log → 0
grep -c '1024343313' errors.log → 0
```
Zero mentions of Izzu's ID in ANY log file. The adapter never receives his messages. This rules out all Hermes-side filters.

### Step 4: Env var override — ROOT CAUSE #1
Gateway process env had `TELEGRAM_ALLOWED_USERS` and `TELEGRAM_GROUP_ALLOWED_USERS` that included Arif and Aliff but NOT Izzu or Aliff. The adapter's `_is_user_authorized_from_message` falls through to the runner's `_is_user_authorized` which uses these env vars as sole authority. Config.yaml's `allow_from` was effectively bypassed.

**Fix:** Added Izzu (1024343313) and Aliff (1237635275) to both env vars in `kunci-mas.env`, restarted gateway.

### Step 5: Still zero entries — ROOT CAUSE #2 (suspected)
After env var fix, Izzu's messages still don't appear. This suggests Telegram privacy mode is ON (default), which means non-admin, non-mention messages never reach the bot at all — server-side filter before the adapter.

**Fix:** @BotFather → /setprivacy → Disable → remove and re-add bot to group.

## Key learnings

1. **Lane JSON files are legacy** — always check `lanes.yaml` for the canonical registry
2. **Env vars override config.yaml** — when `TELEGRAM_ALLOWED_USERS` exists, it's the sole auth gate
3. **Zero log entries = upstream problem** — if adapter never sees the message, it's Telegram-level filtering (privacy mode), not a Hermes config issue
4. **Privacy mode is the #1 silent killer** — every new bot starts with it ON; always check first when a specific user is affected but others in the same group work

## Files examined

- `/root/HERMES/lanes/lanes.yaml` — canonical lane registry (correct)
- `/root/HERMES/profiles/aaa-hermes/memories/lane-izzu.json` — legacy file (wrong group ID, but irrelevant)
- `/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/lane_switch/__init__.py` — lane detection logic
- `/usr/local/lib/hermes-agent/plugins/platforms/telegram/adapter.py` — message processing chain
- `/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml` — gateway config
- `kunci-mas.env` — env vars for auth
