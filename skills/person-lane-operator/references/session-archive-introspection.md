# Session Archive Introspection — what is archived, who burns tokens

> Forged 2026-08-13. When the sovereign asks "what do you have archived about
> X?", "are other users' messages in the database?", or "does Y burn a lot of
> tokens?" — QUERY THE DB, never assert from memory. Evidence-first (F2).

## The archive shape (Hermes profile)

One SQLite DB holds ALL chats the bot has seen (DMs + groups), at:
`/usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db` (profile-relative).

Key tables:
- `sessions` — one row per conversation: `id, source, user_id, chat_id, chat_type
  ('dm'|'group'), display_name, thread_id, origin_json`
- `messages` — one row per message: `id, session_id, role ('user'|'assistant'|'tool'),
  content, timestamp, platform_message_id, token_count, api_content`

Everything the bot observes in any allowed chat is passively archived here —
not an active "I read it" act, a complete log. Per-human distilled memory lives
separately in lane files (`/root/HERMES/lanes/`); state.db is the raw record.

## Cookbook (verified queries)

```bash
DB=/usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db

# 1. Full archive map: every chat the bot has seen + message counts
sqlite3 -separator '|' $DB "SELECT chat_id, display_name, chat_type,
  COUNT(m.id) FROM sessions s LEFT JOIN messages m ON m.session_id=s.id
  WHERE s.source='telegram' GROUP BY s.chat_id ORDER BY COUNT(m.id) DESC;"

# 2. Dump one chat's human-visible traffic (readable, pipes stripped)
sqlite3 -separator '|' $DB "SELECT m.timestamp, m.role,
  substr(replace(replace(m.content,char(10),' '),'|',' '),1,180)
  FROM messages m JOIN sessions s ON s.id=m.session_id
  WHERE s.chat_id='<CHAT_ID>' AND m.role IN ('user','assistant')
  AND m.content IS NOT NULL ORDER BY m.timestamp ASC LIMIT 400;"

# 3. Per-human attribution INSIDE a group — sender tags live in content,
#    formatted '[DisplayName user_id] message...'
sqlite3 $DB "SELECT substr(m.content,1,160) FROM messages m JOIN sessions s
  ON s.id=m.session_id WHERE s.chat_id='<CHAT_ID>' AND m.role='user'
  AND m.content LIKE '%<USER_ID>%';"

# 4. Token-burn proxy per chat (message count x avg content length)
sqlite3 -separator '|' $DB "SELECT s.chat_id, s.display_name, COUNT(m.id),
  AVG(length(m.content)) FROM sessions s JOIN messages m ON m.session_id=s.id
  WHERE m.role='user' AND s.source='telegram'
  GROUP BY s.chat_id ORDER BY COUNT(m.id) DESC;"
```

## Pitfalls (forged from live probes)

1. **`token_count` may be empty/unpopulated** — `SUM(token_count)` returned
   nothing in this install. Measure first (`SELECT SUM(token_count)...`); if
   empty, fall back to the length proxy: message count x avg chars. Never
   quote a token figure you didn't derive.
2. **Groups have no sender column** — who-said-what inside a group is only
   recoverable via the `[Name user_id]` prefix tags in `content`. A person with
   no tagged messages in a chat has zero direct footprint there (they may still
   appear indirectly via replies/quotes).
3. **One DB, all chats** — a sovereign "I gave my agent access to others"
   question deserves the honest scope answer: every allowed chat is archived in
   the same file, no per-user silo at the raw layer (isolation happens at lane
   injection time, not storage time).
4. **Cost ≠ the named person** — when asked "does X burn tokens?", attribute by
   the proxy table. Common real pattern: the quiet third party costs ~nothing;
   the burn lives in the operator's own DMs and the agent's deep-research turns
   (many tool-result rows per one human question). Say who actually pays.
5. **Relationship dynamics: count before judging.** Before labeling a dynamic
   (e.g. "parasitic"), pull both parties' message ratios from the archive. In
   the 2026-08-13 SADO case the raw ratio (~90/10 energy split) reframed the
   verdict from "parasite" to "asymmetric devotion — different registers, not
   extraction". Evidence rewrites the narrative; let it.

## Sovereign-question framing

- Answer scope questions with real numbers (chats, message counts, sessions).
- State the privacy implication plainly when access was extended to others:
  all their messages in allowed chats are stored; that is by sovereign design
  but worth naming (F11 auditability, F6 maruah).
- Distinguish raw archive (state.db) from distilled lane memory (lanes dir) —
  they answer different questions.
