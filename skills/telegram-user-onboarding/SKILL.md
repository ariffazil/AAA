---
name: telegram-user-onboarding
description: "Add a new Telegram user + group to the Hermes allowlist. Covers the 3-file config pattern (config.yaml + kunci-mas.env + person register), env-overrides-config gotcha, bot-in-group requirement, user-must-initiate-DM rule, and verification recipe. Use when: 'add X to Telegram', 'allow user Y', 'bot can't see group Z', 'chat not found', 'bot can't initiate conversation'."
version: 1.0.0
triggers:
  - User asks to add a Telegram user to the allowlist
  - User asks to add a group to the allowlist
  - Bot returns "chat not found" or "bot can't initiate"
  - Setting up a new person on Hermes
---

# Telegram User Onboarding

## The 3-File Pattern (ALL THREE must be updated)

### File 1: config.yaml

Path: `/usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml`

```yaml
telegram:
  allow_from:          # DM access
    - 'EXISTING_ID'
    - 'NEW_USER_ID'    # ← add
  allowed_chats:       # Chat access (DMs + groups)
    - '-1003521544074'
    - 'NEW_USER_ID'    # ← DM chat_id
    - 'NEW_GROUP_ID'   # ← group chat_id
  group_allow_from:    # Group message access
    - 'EXISTING_ID'
    - 'NEW_USER_ID'    # ← add
  free_response_chats: # No-mention replies (groups only)
    - '-1003521544074'
    - 'NEW_GROUP_ID'   # ← add for auto-reply in group
```

### File 2: kunci-mas.env (CRITICAL — overrides config)

**Env vars OVERRIDE config.yaml.** If `TELEGRAM_ALLOWED_USERS` exists, adapter reads ONLY that var.

Path: `/root/.secrets/kunci-mas.env`

```bash
# Update ALL THREE:
export TELEGRAM_ALLOWED_USERS="...,NEW_USER_ID"
export TELEGRAM_ALLOWED_CHATS="...,NEW_USER_ID,NEW_GROUP_ID"
export TELEGRAM_GROUP_ALLOWED_USERS="...,NEW_USER_ID"
```

Then regenerate:
```bash
make -f /root/.secrets/Makefile vault-generate
```

### File 3: Person Register + Social Graph

```bash
# /root/AAA/federation/person-register.json — add person entry
# /root/HERMES/lanes/social-graph.yaml — add node + edges
```

## Restart

```bash
hermes gateway restart
# MUST run from external shell — gateway blocks self-restart
```

## Telegram API Gotchas

| Error | Meaning | Fix |
|-------|---------|-----|
| `400: chat not found` | Bot NOT a member of group | Group admin must add bot to group |
| `403: bot can't initiate conversation` | User hasn't messaged bot yet | User sends any message first (anti-spam) |

## Verification

```bash
# Which bot am I using?
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getMe" | jq '.result.username'

# Can bot see the group?
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/getChat?chat_id=GROUP_ID" | jq '.ok'

# Can bot message the user?
curl -s "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/sendMessage" \
  -X POST -H "Content-Type: application/json" \
  -d '{"chat_id":"USER_ID","text":"test"}'
```

## Common Mistakes

1. **Updated config.yaml only** → env vars override → user silently dropped
2. **Bot not in group** → "chat not found" → add bot first
3. **User hasn't messaged bot** → "bot can't initiate" → user sends /start first
4. **Wrong bot token** → different bot in group than config expects → verify with getMe
5. **Forgot vault-generate** → systemd reads flat.env → restart won't pick up changes
