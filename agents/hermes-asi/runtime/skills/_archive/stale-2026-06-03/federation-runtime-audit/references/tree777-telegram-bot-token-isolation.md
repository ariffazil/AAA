# TREE777 — Telegram Bot Token Isolation Protocol

**Created:** 2026-05-17
**Type:** SCAR / Enforcement Protocol
**Severity:** CRITICAL — token collision causes cross-agent confusion

---

## Why This Matters

When two agents share the same Telegram bot token:
- Messages intended for Agent A get processed by Agent B
- Agent B responds to messages that should be handled by Agent A
- User sees chaotic, overlapping responses
- Accountability chain breaks — who sent what?

**Arif's explicit rule:** "Aku dah buat token asing2 jangan la Share BANGANG"

---

## Required Isolation

Every agent in the arifOS federation MUST have its own Telegram bot token:

| Agent | Bot Username | Token Ownership |
|-------|-------------|-----------------|
| OpenClaw | @AGI_ASI_bot | `814959...` (OpenClaw only) |
| Hermes | @ASI_arifos_bot | Different token (Hermes only) |
| A-FORGE notifier | Separate bot | Separate token |
| AAA gateway | (internal only) | N/A |

---

## Verification Protocol

**Before any federation health check, run TREE777 scalpels:**

```bash
# Scalpel 1: OpenClaw token
cat /root/.openclaw/openclaw.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('OpenClaw:', d['channels']['telegram']['botToken'][:20], '...')"

# Scalpel 2: Hermes token
cat /root/.hermes/platforms/telegram/config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('Hermes:', d['botToken'][:20], '...')"

# Scalpel 3: A-FORGE notifier (if exists)
grep -r "TELEGRAM.*TOKEN\|NOTIFIER.*BOT" /root/A-FORGE/infra/ 2>/dev/null | head -3

# FAIL condition: OpenClaw token == Hermes token
# PASS condition: All tokens different
```

---

## If Collision Detected

1. **STOP** — do not proceed with federation operations
2. **888_HOLD** — escalate to Arif immediately
3. **Log the collision** in AAA group
4. **Do not attempt to "fix" by moving messages** — the damage is in the shared token

---

## Bot Username Reference

- **OpenClaw:** `@AGI_ASI_bot` (ID: 8149595687)
- **Hermes:** `@ASI_arifos_bot` (different bot, same owner Arif)

---

## Common Failure Patterns

### Pattern 1: Copy-paste config
Admin copies `openclaw.json` to configure Hermes → shares the token.

### Pattern 2: One token for "both bots"
User thinks "same person owns both, same token is fine."

### Pattern 3: A-FORGE notifier shares OpenClaw token
Safe IF: A-FORGE only SENDS (not receives). If A-FORGE receives, separate token required.

---

## Enforcement in AAA JOINT SEAL

The AAA JOINT SEAL (2026-05-17) explicitly states:
> **DIVISION OF RESPONSIBILITY**
> OpenClaw: Machines, infra, ops
> Hermes: Human life

Token isolation is a physical manifestation of this division. Violation = violation of AAA JOINT SEAL.

---

## Telegram Bot Token Format

Telegram bot tokens look like:
```
8149595687:AAFwy70********************************
8410138119:AAH********************************
```

Format: `{bot_id}:{authorization_token}`

Different bots have different bot_ids. Check the first number to confirm they are different bots.