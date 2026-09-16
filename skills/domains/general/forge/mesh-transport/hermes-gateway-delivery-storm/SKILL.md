---
name: hermes-gateway-delivery-storm
description: Use when gateway floods Telegram send errors.
---

# Hermes Gateway Delivery Storm Triage

## Symptom
`journalctl -u hermes-asi-gateway` floods with:
- `Failed to send Telegram message: Forbidden: the bot can't send messages to the bot`
- `Failed to send Telegram message: Forbidden: bot can't initiate conversation with a user`

Rate looks like a retry ladder (~1 per 3s), often right after a gateway restart.

## Root cause pattern
The gateway stores outbound messages as **delivery obligations** in `/root/.hermes/state.db`
(table `delivery_obligations`). At boot it redelivers failed ones (restart notification,
home-channel notice, obligation redelivery). If the backlog contains obligations whose
`chat_id` is unreachable by design — most commonly **Hermes' own bot ID** (Telegram forbids
bot-to-bot DMs) — every boot replays them and the storm recurs.

## Triage procedure

```bash
# 1. Is it still going?
journalctl -u hermes-asi-gateway --since "1 min ago" --no-pager | grep -c "Failed to send Telegram"

# 2. Error types + timeline
journalctl -u hermes-asi-gateway --since today --no-pager \
  | grep "Failed to send Telegram" | sed 's/.*Forbidden: //' | sort | uniq -c | sort -rn

# 3. Dead backlog by target
sqlite3 /root/.hermes/state.db \
  "SELECT chat_id, state, COUNT(*) FROM delivery_obligations\
   WHERE state IN ('failed','abandoned') GROUP BY chat_id, state ORDER BY 3 DESC;"

# 4. Identify self-targeting (compare against the bot's OWN user id)
sqlite3 /root/.hermes/state.db \
  "SELECT session_key, COUNT(*) FROM delivery_obligations\
   WHERE chat_id='<BOT_OWN_ID>' GROUP BY session_key;"
```

Obligation states: `delivered` (fine) · `failed` / `abandoned` (terminal, never retry again).
`session_key` shape `agent:main:telegram:dm:<id>` tells you which lane is poisoned.

## Key insight
The error is **outbound**, so the sender is fine — the *target* is unreachable. Always resolve
`chat_id` to a real identity before blaming the adapter. A `dm:<bot's own id>` session key means
Hermes recorded its own outbound as an inbound DM and replied to itself.

## Fix
1. `sqlite3 /root/.hermes/state.db ".backup /root/.hermes/state.db.bak-$(date +%Y%m%d-%H%M%S)"`
2. Purge terminal rows so boots stop replaying them:
   `DELETE FROM delivery_obligations WHERE state IN ('failed','abandoned');`
3. Re-check `channel_directory.json` for bogus DM entries pointing at bot IDs.

Only `delivered` rows and in-flight (`pending`) rows are operational; terminal rows are
replay-only and safe to drop **after backup**. Deleting an active ledger is a separate,
F13-authorized act — never do that under this skill.

## Bot messages in a `free_response_chats` group bypass the loop-breaker

The bot-loop-breaker (`_telegram_bots_require_mention`, consumed in
`_should_process_message`) does **not** run for a chat listed in `free_response_chats`:
the free-response check returns `True` earlier in the same function. So a group that is
both free-response and hosting bots will let every bot message reach the agent, and
setting `bots_require_mention: true` alone will not change that.

To make bots require an explicit @mention while humans stay unaffected:

1. remove the group from `free_response_chats`, and
2. set `telegram.bots_require_mention: true`.

A human message still passes because `require_mention: false` returns early for them.
Note the tension: some groups are deliberately free-response so agents can converse
(the code calls one such room the "musyawarah room"). Removing that is a policy call,
not a bug fix — surface it, don't silently flip it.

## Episode-level logs do not identify the chat

`session_id` in `state.db.messages` is a date+hash (e.g. `20260914_234522_46d3d6`), **not**
the chat id — `session_id LIKE '%<chat_id>%'` always returns nothing and looks like
"no activity". To attribute activity to a chat, use the gateway's own session key
(`agent:main:telegram:group:<chat_id>:<thread_id>`) in the logs, never a LIKE on
`session_id`.

## Pitfalls
- A restart does NOT clear the storm; it re-triggers it. The backlog is persistent state.
- The storm can self-resolve when the retry ladder exhausts (looks "fixed" briefly) and
  returns on the next restart. Verify by checking whether the dead rows still exist.
- Don't blame a recent config change without a timeline check — count errors per hour and
  compare against the change's mtime.

## Telegram inbound auth has TWO surfaces — config.yaml wins

Adding a user/bot to an allowlist is the most common task here, and it has a trap that
produces a *false success*:

1. `config.yaml` → `telegram.allow_from` (DMs) and `telegram.group_allow_from` (groups).
2. The systemd service EnvironmentFile → `TELEGRAM_ALLOWED_USERS` / `TELEGRAM_GROUP_ALLOWED_USERS`.

The adapter resolves an **adapter-level** allowlist first and treats it as the *sole
authority* when set; the runner's env chain is only consulted when that is absent. So if
`group_allow_from` is populated, editing the env file changes nothing — and you will still
see `Blocked unauthorized user <id>` afterwards.

Both paths accept either a YAML list or one comma-joined string; the comma-joined string is
what `hermes config set <key> <csv> --force` writes, so a naive `isinstance(v, list)` reader
reports a bogus entry count on a perfectly valid config. Normalise before counting.

**Rule: verify the gate, not the write.** After any allowlist change, confirm the ID is in
`config.yaml` (the operative surface) AND attribute new log lines to the *current* `MainPID` —
lines from the pre-restart PID are stale evidence. `0 blocks from current PID` is the receipt;
"I added it" is not.

Renew an allowlist with the supported writer so the value survives normalisation:

```bash
hermes config set telegram.group_allow_from "<existing>,<new-id>" --force
```

## Hermes normalises its own config

`config.yaml` is rewritten on restart. Hand edits are not authoritative and the file may be
reindented/reordered. Use `hermes config set` for anything that must persist. The same trap
exists one level down for env: the gateway reads its EnvironmentFile, not the profile dotenv —
check the live process environment before believing an edit landed.
