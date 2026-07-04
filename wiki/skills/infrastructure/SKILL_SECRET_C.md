---
title: "SKILL: Secret Rotation Guide"
type: skill
version: 1.0.0
category: security
risk_band: HIGH
floors: [F1, F11, F13]
evidence_required: true
sources: [/root/.opencode/skills/secret-rotation-guide/SKILL.md]
confidence: high
---

# SKILL: Secret Rotation Guide

> **⚠️ DITEMPA BUKAN DIBERI — Never rotate without Arif's approval.**
> **Source:** `/root/.opencode/skills/secret-rotation-guide/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Planning secret rotation
- Auditing credential inventory
- Detecting exposed or leaked keys
- Managing API key lifecycle
- Keywords: secret rotation, API keys, credentials, exposure

---

## ⚠️ Critical Rules

1. **NEVER rotate a live key without confirming it won't break running services**
2. **NEVER put secrets into VAULT999** — audit ledger, not secret store
3. **Always test after rotation** — verify all services still work
4. **Arif must be at provider dashboards** — agents cannot log into Anthropic/GitHub/etc.

---

## Secret Inventory (2026-05-14)

### 🔴 DEAD — Rotate at Provider Dashboard

| # | Key | Location | Dashboard |
|---|-----|----------|-----------|
| 1 | Anthropic API key | `/root/.claude/credentials/` | console.anthropic.com |
| 2 | GitHub PAT | (sanitized 2026-05-14) | github.com/settings/tokens |
| 3 | Kimi API key | `/root/AAA/.kimi/credentials/` | platform.moonshot.cn |
| 4 | Gemini credentials | `/root/AAA/.gemini/gemini-credentials.json` | aistudio.google.com |
| 5 | Copilot session | `/root/AAA/.copilot/session-store.db` | github.com/settings/copilot |
| 6 | Hermes auth token | `/root/AAA/.hermes/` | hermes agent config |

### 🟡 EXPOSED — On Disk, Needs Rotation

| # | Key | Location |
|---|-----|----------|
| 7 | OpenClaw device auth | `/root/.openclaw/identity/device-auth.json` |
| 8 | OpenClaw Telegram config | `/root/.openclaw/telegram/` |
| 9 | arif-sites OpenCode key | `/root/arif-sites/infra/vps_root/opencode-config/auth.json` |
| 10 | arif-sites Telegram token | `/root/arif-sites/infra/vps_root/telegram-bot/token.env` |
| 11 | Claude Supabase OAuth | `/root/AAA/.claude/` (may not exist) |
| 12 | Jina API key | Location TBD |

### 🟢 LIVE — Do Not Touch

- arifOS governance secret (in env)
- WEALTH Supabase key (in git history — needs rewrite)
- Caddy Cloudflare API token
- Tailscale auth key

---

## Rotation Procedure (Arif Only)

```
1. Log into provider dashboard
2. Generate new key
3. Update key in relevant config file on VPS
4. Restart affected service
5. Verify service health
6. Revoke old key at provider dashboard
7. Mark ledger entry as DONE
```

---

## What NOT To Do

- ❌ Put keys in VAULT999
- ❌ Rotate without testing
- ❌ Delete old credential files until new key verified working
- ❌ Commit keys to git
- ❌ Share keys in chat

---

## Related Pages

- [[skill-secret-hygiene]] — secret hygiene philosophy
- [[skill-vault999-ops]] — VAULT999 safe operations
- [[concept-tools-and-embodiment]] — secrets as hard embodiment
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Secrets mapped. Rotation needs Arif.*
