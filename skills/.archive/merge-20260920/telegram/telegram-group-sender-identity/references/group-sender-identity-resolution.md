# Group Sender Identity Resolution — Diagnostic Transcript

> Session: 2026-08-30, AAA group thread 52537
> Problem: Bot can't identify who's prompting in SADO group

## Context

Arif asked to "map all active users with direct DM access." Initial analysis misidentified users:
- "No name" (1042200555) → assumed unknown. **Actually = Abang Sado Syed (Udin)**, Arif's partner.
- "Mohd" (1237635275) → assumed generic. **Actually = Izzu**, Arif's scar buddy.
- SADO group assumed to have multiple members. **Actually = just Arif + Syed** (others removed for privacy).

Arif's correction: *"Omg that's fail!!"* — the bot talked to his partner for weeks without knowing who he was.

## Root Cause Analysis

### How Hermes routes group messages

1. Telegram sends `message.from.id` and `message.from.first_name` with every group message
2. Hermes adapter extracts these in `_source_from_message_for_auth()` (adapter.py:1002)
3. `user_id` and `user_name` are stored in `SessionSource`
4. Gateway creates session key: `agent:main:telegram:group:{chat_id}:{user_id}`
5. `group_sessions_per_user=True` (default) → isolated session per sender
6. `build_session_context_prompt()` (session.py:482) injects `**User: {user_name}` into system prompt

### Why it failed

Syed's Telegram first_name = "" (empty). Telegram displays this as "No name." The gateway correctly routes his messages to a separate session, but the bot sees:

```
**User:** No name
```

No identity context. No mapping to "Abang Sado Syed." The bot treated him as an anonymous stranger in his own partner's system.

### Why the session data was confusing

Gateway routing table showed TWO sessions for SADO group:
- `agent:main:telegram:group:-1003815535761:1042200555` → Syed
- `agent:main:telegram:group:-1003815535761:267378578` → Arif

But state.db sessions table showed most SADO sessions with `user_id=267378578` (Arif) because the session snapshots were taken at different times and some sessions were created before per-user isolation was fully active.

## Evidence Collected

### Gateway routing (state.db)
```
agent:main:telegram:group:-1003815535761:1042200555 → session 20260816_151136_aaa01509 (199 msgs)
agent:main:telegram:group:-1003815535761:267378578 → multiple sessions
```

### Gateway log sender attribution
```
174 messages: user=ARIF (Arif)
  11 messages: user=Mohd (Izzu in AIA)
   6 messages: user=unknown
   5 messages: user=No name (Syed)
```

### Key code paths
- `build_session_context_prompt()` at `gateway/session.py:482` — builds system prompt context
- `is_shared_multi_user_session()` at `gateway/session.py:1049` — determines shared vs isolated
- `_source_from_message_for_auth()` at `plugins/platforms/telegram/adapter.py:1002` — extracts sender
- `group_sessions_per_user` config (default True) — per-sender isolation toggle

## Fix Applied

### Database layer (temporary)
1. Updated `sessions.json`: 2 Syed entries → display_name = "Abang Sado Syed (Udin)"
2. Updated `state.db sessions`: 4 sessions → display_name updated, origin_json updated
3. Updated `state.db gateway_routing`: 7 entries → display_name + origin.user_name + origin.chat_name updated

### Memory layer (persistent)
Added user identity map to Hermes memory:
```
Syed = Telegram 1042200555 = "Abang Sado Syed" / "Udin"
Izzu = Telegram 1237635275 = "Mohd" display name
```

### Human layer (permanent fix needed)
**Action required:** Ask Syed to set his Telegram first name to "Udin" or "Syed." This is the only permanent fix — database changes get overwritten when Telegram sends fresh user info.

## Related: AIA Group

Same pattern applies to Izzu (Mohd, 1237635275) in AIA group. His Telegram name is "Mohd" — generic but not empty. Bot sees "User: Mohd" with no context about scar buddy relationship or AIA group purpose.

**Fix:** Izzu could set a more distinctive Telegram name, or Arif can add more context to the memory identity map.
