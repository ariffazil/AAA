---
name: hermes-state-db-forensics
description: "Query state.db for Telegram history and token burn — plus the unknown-chat triage ladder (channel_directory → sessions → allowlists → journal Forbidden) for identifying a chat with no history."
version: 1.0.0
tags: [hermes, telegram, sqlite, forensics, tokens, cost, messages, state.db]
---

# Hermes State DB Forensics

Answer "what was said" and "who burns tokens/cost" from the live Hermes gateway store, not from guesses or `session_search` scaffolding. The raw SQLite holds the FULL persisted message archive and per-model token accounting — including chats/messages the agent was not "online" for at delivery time.

## Store locations & tables

Primary store: `/usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db`

- `sessions` — one row per Telegram session per (thread). Schema carries `id`, `source`, `user_id`, `session_key`, `chat_id`, `chat_type` (`dm`/`group`), `thread_id`, `display_name`, `model`, `started_at`, `ended_at`, `message_count`, `input_tokens`, `output_tokens`.
- `messages` — every persisted turn (`role` = `user`/`assistant`/`session_meta`/`tool`), with `content`, `timestamp` (epoch), `token_count`, `reasoning_content`, `platform_message_id`.
- `session_model_usage` — **the real token/cost ledger**: per (session_id, model, billing_provider) with `api_call_count`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `reasoning_tokens`, `estimated_cost_usd`, `actual_cost_usd`, `cost_status`, `cost_source`.
- FTS tables (`messages_fts`, `messages_fts_*`) — full-text over messages; `session_search` wraps these.
- Sibling stores: `sessions/*.db` (bonded request dumps), `cron/executions.db`, `cron/notepad.db`, `verification_evidence.db`.

`sessions.session_key` shape: `agent:main:telegram:dm:<user_id>` (DM) or `agent:main:telegram:group:<chat_id>:<user_id>` (group). Group `chat_id`s are NEGATIVE (e.g. SADO = `-1003815535761`); DMs use the raw numeric user id.

## Verified query patterns (2026-08-13)

**All chats & their message counts (per chat/display/type):**
```sql
SELECT s.chat_id, s.display_name, s.chat_type, COUNT(DISTINCT m.id) AS msgs
FROM messages m JOIN sessions s ON m.session_id=s.id
WHERE m.role='user' GROUP BY s.chat_id, s.display_name, s.chat_type
ORDER BY msgs DESC;
```
This is how you answer "is other users'/agents' chat in the DB?" — yes: every whitelisted DM + every allowlisted group the bot is in accumulates here, humans AND sibling agents (ASI, OpenClaw, FORGE, AGENT MERDEKA all show up as their own rows).

**Message archive for one chat** (set `chat_id`); add `AND m.role='user'` for just human/group traffic:
```sql
SELECT datetime(m.timestamp,'unixepoch','+8 hours') AS t, substr(m.content,1,300)
FROM messages m JOIN sessions s ON m.session_id=s.id
WHERE s.chat_id='-1003815535761' ORDER BY m.timestamp ASC;
```

**Token/cost burn for ONE user** (join usage ledger on user_id):
```sql
SELECT u.model, COUNT(DISTINCT u.session_id) AS sessions, SUM(u.api_call_count) AS calls,
       SUM(u.input_tokens) AS in_tok, SUM(u.output_tokens) AS out_tok,
       SUM(u.cache_read_tokens) AS cache_read, SUM(u.reasoning_tokens) AS reason_tok,
       ROUND(SUM(u.estimated_cost_usd),4) AS est_usd
FROM session_model_usage u JOIN sessions s ON u.session_id=s.id
WHERE s.user_id='1237635275' GROUP BY u.model ORDER BY est_usd DESC;
```

**Cross-user cost/token comparison** (the "who burns" question in one shot):
```sql
SELECT CASE WHEN s.user_id='267378578' THEN 'ARIF'
            WHEN s.user_id='1237635275' THEN 'IZZU'
            WHEN s.chat_id='-1003815535761' THEN 'SADO' ELSE 'other' END AS owner,
       SUM(u.api_call_count) AS calls,
       ROUND(SUM(u.input_tokens)/1000000.0,2) AS in_M,
       ROUND(SUM(u.output_tokens)/1000.0,1) AS out_k,
       ROUND(SUM(u.estimated_cost_usd),3) AS est_usd
FROM session_model_usage u JOIN sessions s ON u.session_id=s.id
GROUP BY owner ORDER BY in_M DESC;
```

## Pitfalls (all hit 2026-08-13)

- **MULTIPLE state.db files exist — query the RIGHT one.** There are 7+ `state.db` files on this VPS. `/root/HERMES/state.db` contains **CLI/agent sessions only** (source = `cli`, `subagent`, `cron`). **Telegram sessions are ONLY in the profile-specific store** (`/usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db`). If you query `/root/HERMES/state.db` for Telegram chat history you will get zero results and wrongly conclude "no data exists." Always verify with `SELECT DISTINCT source FROM sessions` — if you don't see `telegram`, you're in the wrong DB. Sibling agent profiles (`/root/HERMES/profiles/hermes_asi/state.db`, `hermes_forge`, `hermes_apex`) each have their own separate stores.
- **`messages.token_count` is NOT reliable — it reads 0 across the board.** Real token accounting lives ONLY in `session_model_usage`. If you SUM `messages.token_count` for cost you'll conclude "nobody burns anything" — wrong. Always pivot to `session_model_usage` for token/cost queries.
- **`estimated_cost_usd`/`actual_cost_usd` are mostly 0.0 / `cost_status='unknown'`.** Cost attribution is unreliable for most providers (only some rows — e.g. a `deepseek-v4-pro` call — populate a nonzero `$0.22`). Treat **token counts as the signal**, cost as best-effort. Don't claim a precise dollar cost the ledger doesn't actually support.
- **Filter by `user_id` for a person, by `chat_id` for a group.** A user in a group appears under BOTH (their DM rows and the group rows). To isolate one channel use the right column, else you double-count.
- Group `chat_id` is negative — a `WHERE s.chat_id='-1003815535761'` must keep the minus sign; matching by `display_name` is fallible (display names collide / come from session labels).
- Images land inline as `[The user sent an image~ Here's what I can see: ...` + a vision transcript in `content` — grep that prefix to find image-heavy turns; full video/preview attachments are NOT inlined (saved to `cache/`).
- Timestamps are epoch floats IN SECONDS → render with `datetime(x,'unixepoch','+8 hours')` (MYT), no division. **Tell:** if your output shows `1970-01-xx`, you divided seconds by 1000 — `messages.timestamp` AND `sessions.last_activity_at` are both epoch seconds, not millis (hit 2026-08-15). The DB is server-local, not UTC-normalized for display.
- `messages_fts` (via `session_search`) is the curl/search layer; for exact archive/count/aggregate queries go straight to SQLite — searcher and store can disagree on totals.
- **`session_search` itself can hard-fail with an FTS5 shadow-table error** (`fts5: error creating shadow table messages_fts_data: table 'messages_fts_data' already exists`, hit 2026-08-15). Don't debug the tool mid-task — pivot straight to sqlite3; a timestamp-window + role filter replaces full-text search fine for "what just happened" recovery.
- **A "sifar hit" is a host-bounded claim, not a federation claim** (lesson from divergence ticket e-cc9a2dd3, 2026-10-10). Two hosts in the same federation can serve overlapping but non-identical chat sets: the same `/root/.hermes/state.db` path on KVM4 vs KVM8 returned different 9 Oct content because the active gateway moved between them — KVM4 served the Syed DM block, KVM8 served the ARIF/HERMES DM with a quote of it. A single-host probe that returns "sifar" must be reported as `<host>:<path>:<md5> returned 0 rows`, never as "the data does not exist." The RECALL-scar failure class is exactly that conversion: absence in one bounded store presented as absence in reality, then baked into a downstream audit or PDF. Mandatory receipt for any multi-host probe: `host:path:md5:unit_epoch`; if the query spans hosts, every host gets a row in the receipt, even if empty. This is the same class as "Recall ≠ Recall" — a probe-side artefact wearing a fact-shape.
- **`sessions/sessions.json` is a LEGACY MIRROR of the `gateway_routing` table in `~/.hermes/state.db`** (verified 2026-08-15). Maps Telegram session keys (`agent:main:telegram:dm:<user_id>`, sorted by `updated_at`) to the live gateway session id — good for finding WHICH session is active. But that id's messages may live in a DIFFERENT store: gateway-side Telegram sessions sit in the profile store, while the agent's own work sessions for the same chat (tool work, terminal/SSH) land in `/root/.hermes/state.db` under separate ids. When recovering "what happened in the last N hours", don't trust the routing index alone — run `SELECT DISTINCT session_id FROM messages WHERE timestamp > <epoch> ORDER BY session_id DESC` in `/root/.hermes/state.db` and read the non-`cron_*` ids; that found the full work transcript when the routing-index id returned zero rows.

## Your store = your whole federation's memory surface

This DB is not just the operator's diary — it is the mirror of the entire multi-bot federation (all whitelisted humans' DMs + all allowlisted groups + sibling agent chats). That is the architectural point Arif confirmed (user gave agents access). When answering "does X show up / how much does X cost / what did X say", this is the source of truth — and exactly because it holds other people's personal/medical data (e.g. Syed's mother's recovery timeline), treat read access as F13/F6-MARUAH steward duty: never surface a third person's content outside the chat where it belongs.

## Pitfalls: bot-peer chat sessions (hit 2026-08-15)

- **A2A-bridged sibling-agent chats appear as Telegram DMs with BOT user ids as `chat_id`** (e.g. OpenClaw `8149595687`, ASI `8410138119`) but `user_id=267378578` (Arif as injected principal). Authz checks the USER (authorized → inbound processes fine); outbound `sendMessage` targets a bot peer → Telegram hard-rejects **"Forbidden: the bot can't send messages to the bot"** (2,733+ in errors.log). Work in these sessions runs and burns tokens but can NEVER deliver via Telegram — replies must ride the A2A bridge back, or the session is a silent sink.
- Diagnostic one-liner: any `sessions.chat_id` that is ALSO a known sibling-bot user id = bridged chat. Cross-check `grep "can't send messages to the bot" logs/errors.log | wc -l`.
- "Dropping message from unauthorized user in active session: user=<bot_id>" after a failed flush = the bot's own id bouncing on the echo/retry path — authz working correctly, log noise only.
- Don't kill these sessions on sight: they may be an ACTIVE legit turn triggered by the bridge (check `messages` first — if the latest user msg is a relayed principal text, the session is answering, not runaway). Same text fanned to multiple sibling chats (ARIF DM gets it as `/steer`) is normal multi-agent broadcast, not duplication drift.

## Unknown-chat triage ladder (2026-08-15 — "Koho Pharma" incident)

When a chat name surfaces with zero known history ("agent bot tu la" — who is this?), climb this ladder IN ORDER before answering anything:

1. **`channel_directory.json`** (profile root) — the gateway's own roster of every chat it has EVER seen: `platforms.telegram[]` with `id`/`name`/`type` (`dm`/`group`)/`thread_id`, gateway-maintained. Presence = at least one update arrived from that chat; absence = never seen at all. **First probe — cheaper and broader than state.db.** (A bot-peer chat like `8727562763 🔥FORGE🔥`, `8900829116 AGENT MERDEKA` shows here too.)
2. **state.db `sessions` by `chat_id`** — did a session ever start? In directory but zero session rows = inbound dropped by allowlist OR inbound processed but every outbound reply failed.
3. **`config.yaml` allowlists** (`allowed_chats`, `allow_from`, `group_allowed_chats`, `group_allow_from`) — inbound from an unlisted chat is silently dropped, no error logged anywhere.
4. **Journal Forbidden grep** — `journalctl --since <t> | grep "Forbidden:"` (and `logs/errors.log`) classifies the outbound block.

**Two distinct outbound Forbidden signatures — do not conflate:**

| Error string | Meaning | Remedy |
|---|---|---|
| `Forbidden: bot can't initiate conversation with a user` | Target is a HUMAN who never pressed /start on this bot | Human sends /start first; DMs then flow |
| `Forbidden: the bot can't send messages to the bot` | Target chat is itself a BOT — Bot-API bot↔bot DM is impossible, full stop | A2A lane (e.g. `hermes-a2a-listener.service` :18089 JSON-RPC) or a human account as relay |

Both fired within one minute of journal on 2026-08-15 when replying to an unknown "Koho Pharma" DM. Key doctrine: **allowlisting fixes INBOUND only — neither Forbidden is fixable by config; they are Telegram platform law.** So a correct answer to "why is the bot silent to chat X" names which of the four ladder rungs failed, not just "check the config".

## Bare "Continue" recovery (hit 2026-08-15)

When a session opens with a single word — "Continue", "go on", "sambung" — and context is empty (group rotation/restart), reconstruct the referent from the store before replying: (1) skip a failed `session_search`, (2) read `sessions` schema via `pragma_table_info` (columns are `last_activity_at`/`started_at`, NOT `created_at`/`updated_at` — guessing fails), (3) pick the newest session row for that `chat_id` (one group accrues many session rows over days), (4) read its `user`+`assistant` tail — the pending message itself lands in `messages` only asynchronously, so don't loop waiting for it, (5) cross-check the sender's DM sessions by `user_id` in case "Continue" points at DM work, not group banter. Then **match the recovered register**: if the tail is 1-2 line group banter, the correct continuation is one more line of banter, not a status report. Full trail: `references/bare-continue-context-recovery-2026-08-15.md`.

## Support files

- `references/state-db-schema-2026-08-13.md` — verified table schemas (sessions, messages, session_model_usage) and the per-user token/cost SQL, captured from live probe.
- `references/unknown-chat-triage-2026-08-15.md` — Koho Pharma incident: full probe trail (channel_directory hit, zero sessions, zero routing, journal Forbidden ×2), the four-rung ladder, and the two-signature classification table.
- `references/bare-continue-context-recovery-2026-08-15.md` — schema-first ladder for reconstructing what a bare "Continue" refers to when the session context is empty; includes the async-persist gotcha and the register-matching rule.