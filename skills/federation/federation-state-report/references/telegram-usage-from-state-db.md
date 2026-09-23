# Telegram Usage from state.db — per-chat and per-user statistics

Use when the sovereign asks "who's been using my bot", "stats for chat X", "how much did the
SADO group cost me", or any per-chat / per-human Telegram usage question that the gateway log
alone cannot answer. The gateway log shows *live* traffic; this file shows *historical* traffic
grounded in the durable ledger.

The gateway log rotates and forgets; `/root/.hermes/state.db` is the long memory. Read-only
throughout — these queries produce a census, not a mutation.

## Schema facts that decide every query

```bash
sqlite3 /root/.hermes/state.db ".tables"
# Authoritative for usage:
#   sessions            — one row per session, carries chat_id, user_id, billing
#   messages            — every turn inside a session, joined via session_id
#   session_model_usage — per-model token + cost ledger (the cost SOT)
#
# Channels/lanes (decorative for stats, real for routing):
#   channel_directory.json — chat_id → {name, type} label map
```

Three schema facts that change how you write the SQL:

1. **`messages` has NO `chat_id` column.** Sessions carry `chat_id`; messages carry `session_id`.
   Querying `WHERE chat_id=...` against `messages` returns nothing. Always join.
2. **`sessions.message_count` is the closed-session counter.** It is written when the session
   ends and only updated when the row reopens. Live, in-flight sessions may show `0` or a stale
   number. For "what's true right now" use `COUNT(messages.id)` joined on `session_id`.
3. **`sessions.actual_cost_usd` is mostly NULL.** The billing bridge does not populate it for
   `billing_provider='custom'` rows (i.e., almost everything that goes through federation
   proxy). The honest cost signal is `session_model_usage.estimated_cost_usd` for the model
   lane, and `sessions.estimated_cost_usd` for the session-level rollup. Treat `actual_cost_usd`
   as metadata, not money.

## Battery — read top-down, head counts first

```bash
DB=/root/.hermes/state.db
LAB=$(jq -r '.platforms.telegram[] | "\(.id)\t\(.name)\t\(.type)"' \
      /root/.hermes/channel_directory.json)

# 0. SIZE — confirm the file is what you think it is
ls -la "$DB"; sqlite3 "$DB" "SELECT COUNT(*) FROM sessions; SELECT COUNT(*) FROM messages;"

# 1. WINDOW — define the time box before everything else
sqlite3 -separator $'\t' "$DB" "
SELECT MIN(started_at), MAX(last_activity_at),
       (MAX(last_activity_at)-MIN(started_at))/86400.0 AS days
FROM sessions WHERE source='telegram';"
# Convert unix timestamps in the same call with datetime(..., 'unixepoch') — never re-format in shell.

# 2. SESSIONS + MSGS + TOKEN ROLLUPS — the headline numbers (single row, no GROUP BY)
sqlite3 -separator $'\t' "$DB" "
SELECT
  COUNT(*),
  COALESCE(SUM(message_count),0),
  COALESCE(SUM(input_tokens),0),
  COALESCE(SUM(output_tokens),0),
  COALESCE(SUM(cache_read_tokens),0),
  COALESCE(SUM(estimated_cost_usd),0),
  COALESCE(SUM(actual_cost_usd),0)
FROM sessions WHERE source='telegram';"

# 3. PER-CHAT — the answer to "who's the heavy user"
sqlite3 -header -column "$DB" "
SELECT s.chat_id,
       COALESCE(s.chat_type,'?') AS ctype,
       COUNT(DISTINCT s.id) AS sess,
       COALESCE(SUM(s.message_count),0) AS msgs,
       COALESCE(SUM(s.input_tokens),0) AS inp,
       COALESCE(SUM(s.output_tokens),0) AS outp,
       COALESCE(SUM(s.cache_read_tokens),0) AS cache_r,
       ROUND(COALESCE(SUM(s.estimated_cost_usd),0),4) AS cost_e,
       COALESCE(MAX(s.last_activity_at),0) AS last_at
FROM sessions s
WHERE s.source='telegram' AND s.chat_id IS NOT NULL
GROUP BY s.chat_id, ctype
ORDER BY sess DESC;"
# Note: NO join on messages here. Joining and SUMming message_count inflates by N sessions
# per chat because each session row contributes its own counter. Pick one source of truth.

# 4. PER-HUMAN — the answer to "which real people are using Hermes"
sqlite3 -header -column "$DB" "
SELECT s.user_id,
       COUNT(DISTINCT s.id) AS sess,
       COUNT(DISTINCT s.chat_id) AS chats_used,
       COALESCE(SUM(s.message_count),0) AS msgs,
       COALESCE(SUM(s.input_tokens),0) AS inp,
       COALESCE(SUM(s.output_tokens),0) AS outp
FROM sessions s
WHERE s.source='telegram'
  AND s.user_id IS NOT NULL
  AND s.user_id NOT LIKE 'system:%'
GROUP BY s.user_id
ORDER BY sess DESC;"
# Excluding `system:%` removes cron-loop noise; excluding the bot's own user_id
# (Hermes = 8410138119 on this host) removes the echo-loop artefact.

# 5. PER-MODEL cost ledger — the real SOT for "how much did inference cost"
sqlite3 -header -column "$DB" "
SELECT billing_provider, model,
       COUNT(*) AS rows,
       SUM(input_tokens) AS inp,
       SUM(output_tokens) AS outp,
       SUM(cache_read_tokens) AS cr,
       ROUND(SUM(actual_cost_usd),4)  AS cost_a,
       ROUND(SUM(estimated_cost_usd),4) AS cost_e
FROM session_model_usage
GROUP BY billing_provider, model
ORDER BY cost_e DESC;"

# 6. ACTIVITY HEAT — hour-of-day and day-of-week
sqlite3 -header -column "$DB" "
SELECT CAST(strftime('%H', started_at, 'unixepoch') AS INTEGER) AS hr,
       COUNT(*) AS sessions
FROM sessions WHERE source='telegram'
GROUP BY hr ORDER BY hr;"

# 7. TOOL FREQUENCY — top tools called from telegram sessions
sqlite3 -header -column "$DB" "
SELECT m.tool_name, COUNT(*) AS calls
FROM messages m JOIN sessions s ON m.session_id=s.id
WHERE s.source='telegram' AND m.role='tool' AND m.tool_name IS NOT NULL
GROUP BY m.tool_name ORDER BY calls DESC LIMIT 25;"

# 8. END-REASON distribution — what terminates sessions
sqlite3 -header -column "$DB" "
SELECT COALESCE(end_reason,'(none)') AS reason, COUNT(*) AS c
FROM sessions WHERE source='telegram' GROUP BY reason ORDER BY c DESC;"
```

## Cross-referencing with gateway.log (live traffic)

The DB is the long memory; the log is the present. They disagree when a session is open.

```bash
LOG=/root/.hermes/logs/gateway.log
# ALWAYS grep -a, the files hold binary bytes.
grep -a -c "inbound message" "$LOG"            # live inbound count, current log only
grep -a -c "Sending response" "$LOG"           # live outbound count, current log only
grep -a -c "Failed to send Telegram message" "$LOG"   # live send-failure rate
# Rotation order: gateway.log (newest) → .1 → .3 (oldest).
# If you must span rotations, grep -a all four and tail the joined stream.
```

Cross-check pattern: pick a chat_id from `sessions` (e.g. the AAA group `-1003753855708`),
then `grep -a "to -1003753855708" gateway.log` and `grep -a "chat=-1003753855708"`. Counts
should be close — `sessions` will be higher (it includes all history; the log rotates).

## Reading the result

- **`SUM(sessions.message_count)` ≠ `COUNT(messages)`.** The first is a column on sessions,
  written at close; the second is a row count in the messages table. They differ for live
  sessions (column stale) and when sessions are closed without their messages being archived.
  When they disagree, **state.db is the truth, the column is a hint**.
- **A non-zero `cache_read_tokens` with zero `cache_write_tokens` is the steady-state shape.**
  It means the system prompt is cached and hits the cache on every turn. A non-zero
  `cache_write_tokens` means a system-prompt change happened in the window.
- **`estimated_cost_usd` is a quote, `actual_cost_usd` is a bill.** Most rows have only the
  quote. Quote the cost as "estimated", never as "spent", unless `actual_cost_usd > 0` on
  every contributing row.
- **Per-user counts undercount in groups.** A group with 50 messages from 5 different humans
  shows up under whichever user_id the gateway tagged — but in many groups the gateway only
  sees the *bot's* user_id and never sees the real sender. `distinct_chats` per user is a
  useful sanity check: a user_id with `distinct_chats > 5` is probably the sovereign himself,
  or the gateway itself.
- **The "?" chat label is a real finding, not a bug.** Either the chat_id is in
  `channel_directory.json` and your label map missed it (the AAA parent
  `-1003753855708` lives there under several topic suffixes — match the parent before the
  topic), or it's a brand-new chat the directory hasn't been told about yet. Either way,
  report it.

## Pitfalls

- **The fan-out join trap.** `JOIN messages m ON m.session_id=s.id` and then
  `SUM(s.message_count)` **doubles** the count. Two choices: (a) drop the join and SUM the
  column directly; (b) keep the join and `COUNT(m.id)`. Never mix SUM(column) with COUNT(*)
  across a JOIN that may multiply rows.
- **`sessions.chat_id` is nullable.** Sessions opened from the CLI or cron have it NULL. Filter
  with `WHERE s.chat_id IS NOT NULL` for any per-chat report; filter with
  `WHERE s.chat_id IS NULL` to enumerate the headless channels (those go to a different report).
- **`chat_type` is denormalised and can disagree with the directory.** A session labelled
  `group` in the DB but `thread` in `channel_directory.json` is a Telegram forum-thread inside
  a supergroup — match by stripping the `:topicId` suffix from the chat_id before lookup.
- **`MAX(last_activity_at)` returns NULL on never-active rows and breaks `SUM`.** Always wrap
  with `COALESCE(MAX(...), 0)` when computing headers in the same query as SUMs. Same trick
  for `MAX(started_at)` when a row was opened but never logged activity.
- **`state.db` is a 1 GB file with WAL.** Reading while writes are in flight shows committed
  data only (`-wal` is the redo log, `-shm` the index). For a one-shot census during heavy
  traffic, prefer `sqlite3 ... ".timeout 5000"` and accept slightly stale numbers; do not
  copy or `VACUUM INTO` the file while the gateway is live.
- **`system:cron` and the bot's own user_id are NOT humans.** Exclude both before claiming a
  user count. The bot's user_id is whatever `getMe` returns; the cron sentinel is the literal
  string `system:cron`.
- **Per-chat `msgs` from `SUM(message_count)` is exact for closed sessions, stale for live
  ones.** If the heaviest chat by `sess` is the one the sovereign is using right now, its
  `msgs` column may be lower than reality. Cross-check with the join-COUNT query and report
  both numbers when they differ.
- **Token totals in the billions are cache, not work.** A 5B `cache_read_tokens` figure with
  25M `output_tokens` is the steady-state cache-hit shape — not a runaway loop. Always show
  the four columns (input / output / cache-read / cache-write) separately. Showing only
  `input_tokens` reads as a runaway and gets a F13 attention call you do not need.
- **`channel_directory.json` is hand-maintained.** A new chat that the bot joined but the
  operator hasn't named will appear as `(-100xxxxxxxxxx)`. Add it before the report, or quote
  the raw chat_id in the report and mark it UNKNOWN.
- **The "1 users" or "0 sessions" symptom on a query that should be rich means the WHERE
  clause excluded the row.** `source='telegram'` is correct for this gateway; `source='tg'`
  or `source='telegram-bot'` will return empty silently. Confirm with `SELECT DISTINCT source
  FROM sessions;` before composing the WHERE.

## What this file does NOT cover

- **Live traffic shape** (inbound/outbound ratio, current log targets) — pair with
  `telegram-ops` C4 (`hermes-telegram-stack-zen`) for stack-aliveness, and with the
  `gateway.log` greps above for live counts.
- **Per-message content extraction** (who said what at 9:23 AM yesterday) — `telegram-ops` C1
  and `telegram-conversation-history-extraction.md`. This file is for *aggregate* stats, not
  message-level recovery.
- **Cost for non-telegram surfaces** — federate the same pattern with `WHERE source='cron'`
  or `source='subagent'`. The shape is identical; the chat_id semantics are not.
