# Group Membership Extraction — 2026-08-05

Procedure for mapping Hermes' `TELEGRAM_ALLOWED_CHATS` to named Telegram groups, used when Arif asks "which groups should Hermes be in?" or "is Hermes missing from any groups?". Differs from a webhook-status probe (which checks whether a token is alive) — this maps which CHATS each bot is in.

## The three live sources (all drift from each other)

| Source | Path | Notes |
|---|---|---|
| **Live systemd drop-in** (truth) | `systemctl show hermes-asi-gateway -p Environment \| tr ' ' '\n' \| grep TELEGRAM_` | Active runtime set; survives config edits that didn't restart |
| **YAML config** (decorative) | `/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml` | May be `[]` even when drop-in lists 12+ chats |
| **Legacy config** (stale) | `/root/.hermes/config.yaml` → `telegram.allowed_chats` + `free_response_chats` | Adapter reads env, not YAML; mismatch is normal |
| **Per-organ cross-check** | `cat /proc/<gateway-PID>/environ \| tr '\0' '\n' \| grep HOME_CHANNELS` | OpenClaw gateway's view; useful for Hermes-vs-OpenClaw diff |

## Extraction procedure

```bash
# 1. Live runtime (truth)
systemctl show hermes-asi-gateway -p Environment | tr ' ' '\n' \
  | grep -E 'TELEGRAM_(HOME|ALLOWED_CHATS|GROUP_ALLOWED_USERS|ALLOWED_USERS)' \
  | sed -E 's/(=.*)/\1/' | head

# 2. YAML (decorative — usually empty for newer configs)
grep -E "home_channel|allowed_chats:|group_allow_from" \
  /usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml

# 3. Cross-gateway diff (Hermes vs OpenClaw)
#    OpenClaw: get PID from pgrep -f openclaw-gateway, then:
cat /proc/<openclaw-PID>/environ | tr '\0' '\n' | grep HOME_CHANNELS
#    Hermes: from step 1
```

## Orphan detection (Hermes-only or OpenClaw-only chats)

A chat in Hermes' `TELEGRAM_ALLOWED_CHATS` but NOT in OpenClaw's `HOME_CHANNELS`:

| Signal | Likely cause |
|---|---|
| `journalctl -u hermes-asi-gateway --since "7 days ago" \| grep "<chat_id>"` empty | (1) Lapsed config or (2) Deliberate single-gateway (private/family) |
| Live traffic in the log | (2) Deliberate — Arif wants Hermes-only, no AGI |
| No traffic + recently added | (3) Drift — added to Hermes but never synced to OpenClaw |

### The "two home channels per gateway" pattern

- `TELEGRAM_HOME_CHANNEL` = where heartbeat/daily briefings go (usually AAA Home)
- `HOME_CHANNELS` = full list of groups the bot responds in (allowlist for inbound)

Absent from `HOME_CHANNELS` = silently blocked at the gate; check this first when a report says "bot isn't responding in group X."

## Unnamed group ID resolution

Most chat IDs in the config are unlabelled. Resolve names via Bot API on a bot that is a member:

```bash
for v in ASI_ARIFOS_BOT_TOKEN AGI_ASI_BOT_TOKEN; do
  for cid in -1003721331017 -1004446358629 -1003890512851; do
    curl -s --max-time 5 "https://api.telegram.org/bot${!v}/getChat?chat_id=$cid" \
      | python3 -c "import json,sys; d=json.load(sys.stdin); r=d.get('result',{}); print(f'$cid → {r.get(\"title\",r.get(\"username\",\"?\"))}')" 2>/dev/null
  done
done
```

`getChat` requires bot membership; a 403 "bot was kicked" is itself evidence the bot is no longer in that group. If both bots are blocked, fall back to memory or ask Arif.

## Worked example (2026-08-05)

- 12 groups in Hermes config, 11 in OpenClaw, 1 Hermes-only orphan `-5443591163`
- 9 of 12 IDs unnamed in config; resolution via `getChat` not yet run (ask Arif before assuming names)
- Resolved procedure: systemd drop-in `TELEGRAM_ALLOWED_CHATS` → parse → diff with OpenClaw `HOME_CHANNELS` → report orphan
