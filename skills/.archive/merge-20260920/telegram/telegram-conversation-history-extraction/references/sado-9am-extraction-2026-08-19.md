# Worked Example: SADO Group 9:00–10:00 AM Aug 19 2026

A real extraction session — the parent agent asked: "Read recent messages from SADO Telegram group (chat_id -1003815535761) for the past 24 hours. Specifically get the messages around 9:23–9:27 AM today."

## What the parent claimed (and got wrong)

The task brief stated:
- `Arif user_id: 1042200555`

This is **WRONG**. Per `USER-syed.md` in `aaa-hermes` profile:
> "Telegram: @rico_ricaldo_33 · ID 1042200555"

And `lane-syed.json`:
> `telegram_user_ids: ["1042200555"]`

The brief's "verify Arif from data" instruction was a canary — but the parent skipped it. A future agent receiving a similar task should:

1. NEVER trust the parent caller's user_id naming.
2. Cross-check `USER-<person>.md` and `lane-<person>.json` in the active profile.
3. Cross-check `channel_directory.json` for the canonical user_id → display-name mapping.

## Step-by-step extraction (what worked)

```bash
# Confirm the chat_id exists and gateway is running
jq -r '.platforms.telegram[] | select(.id=="-1003815535761") | .name' /root/.hermes/channel_directory.json
# → "SADO"

# Check gateway health
jq -r '.platforms.telegram.state' /root/.hermes/gateway_state.json
# → "connected" (but with errors — see below)

# Check the last log line timestamp
tail -1 /root/.hermes/logs/gateway.log
# → "2026-08-19 01:41:44,429 ..." (i.e. last write was 8 hours before the requested window)

# Filter for the requested window
grep -E "inbound message.*chat=-1003815535761" /root/.hermes/logs/gateway.log \
  | awk -F'[, ]' '$1" "$2 >= "2026-08-19 09:00" && $1" "$2 <= "2026-08-19 09:59"'
# → (no output)

# Cross-check rotated files
for f in /root/.hermes/logs/gateway.log /root/.hermes/logs/gateway.log.1; do
  count=$(grep -cE "inbound message.*chat=-1003815535761" "$f" 2>/dev/null)
  echo "$f: $count SADO message lines total"
done
# gateway.log: 11 in window 08/18 15:06 → 08/19 01:32
# gateway.log.1: rotated, covers earlier window — no 9am 8/19 hits
```

## What we found (and the gap)

The last SADO group message in `gateway.log` was at **2026-08-19 01:32:57 MYT** (user=ARIF, msg="Isi minyak lepas ambik aku la. We go McD. I need coffee"). After that the gateway stopped writing to the log around 01:41 MYT.

The requested 9:23–9:27 AM window (today) has **zero entries** in any local log file. This is a valid finding — not a failure to search.

## Additional context discovered (notes from the agent.log)

Around the same time the parent agent was asking the live bot to read SADO content, ARIF himself was DMing the bot:

```
2026-08-19 01:35:59  ARIF → bot (DM 267378578): "Aduh. Bot tu auto reply laaa. Aku ada ja dalam group tu. Cuba hang baca apa aku [reply]"
2026-08-19 01:40:18  ARIF → bot (DM 267378578): "U can read from SADO group right"
```

These are **direct messages to the bot**, not messages in the SADO group. The parent agent wanted the agent to extract SADO group history — but the agent had no live API access from the subagent environment.

## Symptoms of the gateway error mode observed

```
2026-08-19 01:36:58  WARNING [Telegram] send_voice fallback: native audio send unavailable
2026-08-19 01:36:59  ERROR [Telegram] Failed to send Telegram message: Forbidden: the bot can't send messages to the bot
2026-08-19 01:37:07  ERROR Failed to deliver response after 2 retries: Forbidden: the bot can't send messages to the bot
2026-08-19 01:40:38  ERROR Failed to send Telegram voice/audio, falling back to base adapter: Message to be replied not found
```

Translation: the gateway is trying to send a reply to its own message_id (or to a message that was deleted). This is the "Forbidden: bot can't send messages to the bot" class — see `hermes-telegram-gateway-ops` for remediation.

## Identity-mapping checklist (canonical recipe)

Before reporting any Telegram user_id in a result, always:

```bash
# Get the display name from channel_directory.json
name=$(jq -r '.platforms.telegram[] | select(.id=="1042200555") | .name' /root/.hermes/channel_directory.json)
echo "1042200555 → $name"  # → "No name"

# Cross-check from USER-syed.md (in active profile)
grep -E "1042200555|rico_ricaldo_33" /root/.hermes/profiles/aaa-hermes/memories/USER-syed.md
# → "| Telegram | @rico_ricaldo_33 · ID 1042200555 |"

# Cross-check from lane-syed.json
jq -r '.triggers.telegram_user_ids' /root/.hermes/profiles/aaa-hermes/memories/lane-syed.json
# → ["1042200555"]
```

So 1042200555 = Syed = "No name" in gateway logs.

## Final output template (what to send the parent)

```
RESULT: HISTORICAL EXTRACTION (SADO group, chat_id=-1003815535761, window 2026-08-19 09:00–10:00 MYT)

NO ENTRIES FOUND in any local log file:
  - /root/.hermes/logs/gateway.log    (last SADO msg: 01:32:57 MYT, ARIF)
  - /root/.hermes/logs/gateway.log.1  (rotated, no 9am hits)
  - /root/.hermes/logs/agent.log      (no 9am SADO turns)

Last SADO group activity (gateway.log):
  2026-08-19 01:32:57 MYT | ARIF (user_id=267378578) | "Isi minyak lepas ambik aku la. We go McD. I need coffee"

PRE-FLIGHT FACT CHECK:
  - Task brief claimed Arif user_id=1042200555. INCORRECT.
  - 1042200555 = Syed (@rico_ricaldo_33).
  - Arif's Telegram user_id = 267378578.

GATEWAY STATUS:
  - gateway_state.json: connected, last updated 2026-08-19 01:40:39 UTC
  - Recent errors: "Forbidden: the bot can't send messages to the bot" + reply-target deleted
  - Inbound log writes stopped around 01:41 MYT — gateway may be wedged
```

## Take-aways for the next session

1. **The "extract recent messages from chat X" task is a real recurring pattern** — not a one-off. Having a dedicated path for it (this skill) saves a lot of grep-and-pray.
2. **Empty window is a valid answer** — never fabricate. "No entries in local logs" is better than an invented quote.
3. **The parent caller's user_id naming is the #1 source of confusion** — always verify. The session discovered this through careful cross-checking, not through trusting the brief.
4. **gateway.log is the source of truth for inbound history** — agent.log has session context but not raw messages; state.db has session history but no chat_id.
