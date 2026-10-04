# state.db — Telegram group history archive (verified 2026-08-13)

Hermes archives every message that reaches the bot — group and DM — in the
session DB. The Telegram Bot API has no `getHistory`, but the server-side
archive does. So "can you read the SADO group history?" = **yes, since the
bot joined the group**. Only pre-join messages are absent (Telegram never
delivered them).

## The false-negative this reference prevents

Saying "aku tak boleh scroll balik sejarah group" without probing state.db.
The Bot-API limitation does NOT apply to the local archive. Probe first.

## Location

```
/usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db
```

Tables: `sessions`, `messages` (+ FTS index `messages_fts` for keyword search).

## Key schema

`sessions`: `id`, `session_key`, `chat_id`, `chat_type` (dm/group),
`display_name`, `started_at` (REAL epoch), `message_count`.
- session_key pattern for groups:
  `agent:main:telegram:group:<chat_id>:<user_id>` with display_name = group title

`messages`: `session_id`, `role` ('user'/'assistant'/'tool'), `content`
(full text), `timestamp` (REAL epoch), `observed` (1 = unmentioned group
message captured by the observe pipeline), `platform_message_id`.
- Group user rows carry a `[NAME|user_id]` prefix in content.
- Images arrive as `[The user sent an image~ ...]` transcript text, not raw media.

## Recipe

```bash
DB=/usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db

# 1. Which chats are archived (per-chat session counts)
sqlite3 "$DB" "SELECT session_key, display_name, chat_type, COUNT(*)
  FROM sessions GROUP BY chat_type ORDER BY COUNT(*) DESC LIMIT 15;"

# 2. Archive span + total message count for one chat
sqlite3 "$DB" "SELECT datetime(min(m.timestamp),'unixepoch','+8 hours'),
    datetime(max(m.timestamp),'unixepoch','+8 hours'), COUNT(*)
  FROM messages m JOIN sessions s ON m.session_id=s.id
  WHERE s.chat_id='-1003815535761';"

# 3. Latest human messages in a group (newest first)
sqlite3 "$DB" "SELECT datetime(m.timestamp,'unixepoch','+8 hours'),
    substr(m.content,1,100)
  FROM messages m JOIN sessions s ON m.session_id=s.id
  WHERE s.chat_id='-1003815535761' AND m.role='user'
  ORDER BY m.timestamp DESC LIMIT 20;"

# 4. Keyword search across the chat (FTS)
sqlite3 "$DB" "SELECT m.id, substr(m.content,1,120) FROM messages_fts f
  JOIN messages m ON m.id=f.rowid
  WHERE messages_fts MATCH 'abang sado' LIMIT 10;"
```

Timestamps are UTC epoch — add `'+8 hours'` for MYT.

## Verified evidence (2026-08-13)

- SADO group `-1003815535761`: 2,985 messages archived, span
  2026-08-05 23:16 → 2026-08-13 21:57 MYT.
- Sessions table grouped view: DM Arif 201 sessions, SADO group 97 sessions.
- Total messages in DB at probe time: 58,886.

## Boundary statement to give the human

- ✅ Full recall of everything the bot received since it joined the group.
- ❌ Messages from before the bot joined — Telegram never delivered them;
  no server-side copy exists here.
- Real-time monitoring of new messages: only the gateway-bound session sees
  them live; this archive query works from any session.
