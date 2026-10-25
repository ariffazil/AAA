---
name: hermes-delivery-diagnostics
description: "Use when work is produced but never reaches the human."
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Hermes Delivery Diagnostics

Work exists ≠ work delivered. Three independent layers can swallow output:
producer → destination resolution → platform send. Check them in that order.

## Symptom → layer map

| Symptom | Layer | Where to look |
|---|---|---|
| Agent replies, human sees nothing | destination | `delivery_obligations` rows stuck `abandoned`; `last_error` |
| `Forbidden: the bot can't send messages to the bot` | destination | target chat_id == bot's own user id |
| `Blocked unauthorized user <id> in chat <id>` every 30–60s | inbound gate | self-echo passing the auth gate |
| Cron ran, exit 0, nothing arrived | destination | `deliver: origin` resolving to a stale/wrong chat |

## 1. Verify the destination, never trust the origin

`origin.chat_id` is retrieved content. It must not authorise itself as a recipient.

```bash
sqlite3 /root/.hermes/state.db \
  "select obligation_id, chat_id, state, attempts, last_error from delivery_obligations order by created_at desc limit 10;"
```

An obligation with `state='abandoned'` and `last_error LIKE '%Forbidden%'` is
produced-but-undelivered work. That is the real failure — the log line is only noise.

**Rule:** resolve recipients against a fixed allowlist *before* send; if the resolved
target is not on it, fail closed and send nothing. Do not "fix" this by asking the
caller to pass the right id — that is a promise, not a mechanism.

## 2. Bot-self loop (the loud one, not the blocking one)

Pattern: the bot's own outbound message returns through `getUpdates`; if the auth gate
runs before the own-echo filter it logs
`Blocked unauthorized user <bot_id> in chat <bot_id>`, and callers then try to reply
into that self-chat → `Forbidden: the bot can't send messages to the bot` → retry loop.

Fix shape (`plugins/platforms/telegram/adapter.py`): put `_is_own_message(msg)`
**before** `_is_user_authorized_from_message(msg)` in **every** inbound handler, not
just text. In the 2026-10 audit that was three: `_handle_text_message`,
`_handle_location_message`, `_handle_media_message`.

Also clean state — a code patch does not remove a registration:
- drop the bot's own entry from `channel_directory.json`
- old sessions with `chat_id = <bot_id>` are history, not routes; never let them resolve a new send

## 3. Gateway restart cannot be self-inflicted

Restarting from inside the gateway kills the command before it finishes (SIGTERM
propagates to children). `systemd-run --on-active` is refused for the same reason.

```bash
sudo systemctl restart hermes-asi-gateway   # from a separate shell
```

After restart, prove silence instead of assuming it — grep **after** the start time:

```bash
systemctl show hermes-asi-gateway -p ActiveEnterTimestamp --value
awk '/<restart-time>/ && /can.t send messages to the bot/' /root/.hermes/logs/gateway.log
```

## 4. "0 uploaded" is not success

Scripts that `exit 0` while moving nothing write a green receipt for work that did
not happen. Invisible until someone counts.

```bash
[ "$UPLOADED" -eq 0 ] && [ "$MISSING" -eq 0 ] && fail "0 uploaded and 0 missing — no work done"
```

The `MISSING == 0` guard matters: a genuinely empty queue is not failure, but
"files present, none uploaded" always is.

## Pitfalls

- **`mailread` cannot fetch attachments** — read-only over `list · search · meta ·
  body · labels · check`. A PDF referenced in a mail needs another path; never claim
  to have read it.
- **Sender identity comes from headers**, not the snippet or display name.
- **Two hosts, two configs.** Verify which file the *running container* binds
  (`docker inspect --format '{{json .Mounts}}'`), not the path quoted in chat.
- **`printenv NAME | wc -c`** proves a credential is set without printing it. Never
  `docker inspect ... Config.Env` into a shared chat.
