---
name: weekly-chat-reflection
description: "Use when Arif runs the weekly users reflection."
version: 1.0.0
tags: [reflection, state.db, telegram, weekly, retrospective, chat-logs, arif]
---

# Weekly Chat Reflection

Produce Arif's weekly retrospective over his own Telegram interactions: what the week meant, where the agent added friction, where it drifted, what shadow-bangang (self-contradiction) it committed, what eureka wisdom surfaced, and what skills/capabilities were gained. This is a recurring ritual, not a one-off — he phrases it "weekly users reflection."

## Live store (read-before-write)

The LIVE Telegram + session store is `/root/.hermes/state.db` (≈1.2 GB, `source=telegram`). `/root/HERMES/state.db` and `/root/runtime/hermes/.hermes/state.db` resolve to the same DB. The profile store `/usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db` (≈35 MB) is a STALE MIRROR whose Telegram data froze mid-2026 — never read current history from it. Verify freshness first: `SELECT MAX(timestamp) FROM messages` — a newest-row age of weeks/months means you are in the wrong DB.

Open read-only: `sqlite3.connect("file:/root/.hermes/state.db?mode=ro", uri=True, timeout=10)`.

## Procedure

1. **Anchor the window.** Compute `wk_start` = epoch of this-week Monday-or-Sunday 00:00 MYT (match what the user means by "this week"), `now` = current epoch. Render all times with `datetime(x,'unixepoch','+8 hours')`.
2. **Confirm the store.** `SELECT MAX(timestamp) FROM messages` + `SELECT DISTINCT source FROM sessions` — expect `telegram` present and freshness within the last day.
3. **Pull the shape** — three aggregates, then the raw dump:
   - message counts per chat (user/assistant/tool + total) in the window
   - token burn per model via `session_model_usage` (this is the real ledger; `messages.token_count` reads 0 everywhere)
   - daily user-message volume per chat
4. **Dump the sovereign's own words** to a file, then read it in paginated chunks (see pitfall). Reading HIS messages is what yields "meaning of interactions" — do not reconstruct from your own replies.
5. **Synthesize into the sections he names**, in his register (BM Penang, `aku`/`hang`, plain human language, no jargon, no tables, no khutbah — standing preferences; see SOUL.md/USER.md).

## Key queries (week window `:wk`..`:now`)

Message counts per chat:
```sql
SELECT s.chat_id, s.display_name, s.chat_type,
       SUM(m.role='user') AS user_msgs, SUM(m.role='assistant') AS asst_msgs,
       SUM(m.role='tool') AS tool_msgs, COUNT(*) AS total
FROM messages m JOIN sessions s ON m.session_id=s.id
WHERE m.timestamp >= :wk AND m.timestamp <= :now
GROUP BY s.chat_id, s.display_name, s.chat_type ORDER BY total DESC;
```

Token burn per model:
```sql
SELECT u.model, SUM(u.api_call_count) AS calls,
       ROUND(SUM(u.input_tokens)/1000.0,1) AS in_k,
       ROUND(SUM(u.output_tokens)/1000.0,1) AS out_k,
       ROUND(SUM(u.cache_read_tokens)/1000.0,1) AS cache_k
FROM session_model_usage u JOIN sessions s ON u.session_id=s.id
WHERE s.last_activity_at >= :wk AND s.last_activity_at <= :now
GROUP BY u.model ORDER BY in_k DESC;
```

Daily volume:
```sql
SELECT date(m.timestamp,'unixepoch','+8 hours') AS d, s.chat_id, s.display_name,
       SUM(m.role='user') AS u
FROM messages m JOIN sessions s ON m.session_id=s.id
WHERE m.timestamp >= :wk AND m.timestamp <= :now AND m.role='user'
GROUP BY d, s.chat_id ORDER BY d, u DESC;
```

Sovereign's own DM words (Arif user_id 267378578) — write to a file, don't inline 400KB:
```sql
SELECT datetime(m.timestamp,'unixepoch','+8 hours') AS t, m.content
FROM messages m JOIN sessions s ON m.session_id=s.id
WHERE s.chat_id='267378578' AND s.chat_type='dm' AND m.role='user'
  AND m.timestamp >= :wk AND m.timestamp <= :now
ORDER BY m.timestamp ASC;
```

## Output structure he expects

Five-to-six sections, human language: (1) the raw shape first (message/token counts, peak days), (2) **insights & meaning** of the interactions, (3) **frictions** — where the agent made him repeat himself, asked what he'd already answered, lectured, or leaked jargon, (4) **drifts** — self-report vs measured reality, provenance-vs-truth collapse, meta-confession loops, (5) **shadow bangang** — the self-contradictions (stated principle vs actual behaviour) that he had to name, (6) **eureka wisdom + new skills/capabilities** gained. End on what is being kept/remembered, not on a question.

## Pitfalls

- **Read the sovereign's dump in paginated chunks.** `read_file` truncates at ~100k chars; a power week is 400KB+. Write the dump to a scratch file, then page with `offset`. If you stop early you will miss the week's decisive turns (e.g. the invariant lesson he delivered at the very end).
- **`messages.token_count` is always 0** — cost/volume comes from `session_model_usage`, never from the messages table.
- **Timestamps are epoch seconds**, not millis; render `+8 hours` for MYT. Output showing `1970-01-xx` means you divided by 1000.
- **Group `chat_id` is negative** (e.g. SADO `-1003815535761`); keep the minus sign. A user in a group also has their own DM rows — filter by `chat_id` for a channel, `user_id` for a person.
- **Reflection ≠ confession dump.** He wants the pattern, not a wall of self-flagellation. Name the friction once, state the rule it violated, move on — do not append a second apology for the same thing (that is itself the meta-confession loop he flags as shadow-bangang).
- **Steward read access.** The DB holds other people's private/medical content (Syed's GERD, Izzu's chats). The reflection is for Arif about his own logs; do not surface a third person's raw content outside its lane.