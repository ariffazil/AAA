<!-- PROVENANCE
     source-skill: telegram-group-sender-identity
     original-path: /root/AAA/skills/domains/general/workshop/telegram-ops/telegram-group-sender-identity/SKILL.md
     sha256-body: 5949e7e7a17721f3f779eb4a7c1b1e0c3992e9c2c6c11352ee7e7975809b4c0f -->

---
name: telegram-group-sender-identity
description: Fix bot not identifying group senders with empty names.
---

# Telegram Group Sender Identity Resolution

## Trigger

Bot says "User: No name" or generic name in group sessions — can't identify who's prompting.

## How Hermes Group Sender Attribution Works

1. `group_sessions_per_user=True` (default) → each sender gets an isolated session
2. Session key format: `agent:main:telegram:group:{chat_id}:{user_id}`
3. Bot sees `**User: {user_name}**` in system prompt, from `message.from_user.full_name`
4. If Telegram display name is empty → "No name" → identity lost

**Routing is correct. FAIL is display name resolution.**

## Diagnostic Steps

```bash
sqlite3 /root/.hermes/state.db "SELECT session_key FROM gateway_routing WHERE session_key LIKE '%{chat_id}%';"
sqlite3 /root/.hermes/state.db "SELECT id, user_id, display_name, message_count FROM sessions WHERE chat_id = '{chat_id}' AND message_count > 0;"
grep "user=.*chat={chat_id}" /root/.hermes/logs/gateway.log | grep -v "user=ARIF" | head -20
```

## Fix Procedure (3 layers)

### Layer 1: Human fix (permanent)
User sets Telegram first name. Settings → Edit Profile → First Name.

### Layer 2: Database fix (temporary)
Update display_name in sessions.json, state.db sessions, and gateway_routing. See source code locations below for the exact fields.

### Layer 3: Memory fix
Add identity mapping to Hermes memory: `user_id → real name`.

## Pitfalls

- "No name" is the user's actual Telegram name, not a bug.
- Don't inject sender names into message text — session isolation already works.
- Database fix is temporary; new sessions pull fresh name from Telegram.
- gateway_routing.entry_json: update nested `origin.user_name`, not just top-level `display_name`.

## Key Source Code

- `build_session_context_prompt()` at `gateway/session.py:482` — builds `**User:** {name}`
- `is_shared_multi_user_session()` at `gateway/session.py:1049`
- `_source_from_message_for_auth()` at `plugins/platforms/telegram/adapter.py:1002`
- `group_sessions_per_user` config (default True) — per-sender isolation
