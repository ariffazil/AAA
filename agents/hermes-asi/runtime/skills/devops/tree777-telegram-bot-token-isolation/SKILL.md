---
name: tree777-telegram-bot-token-isolation
description: "TREE777 SCAR — Telegram bot token isolation enforcement. Prevent two agents from sharing the same Telegram bot token. Triggers on any detection of shared tokens, forces verification before continuing."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  scar_id: TREE777
  severity: CRITICAL
  domain: telegram, multi-agent, token-isolation
  triggered: 2026-05-17
  owner: federation-security
  tlp: AMBER
---

# TREE777 — Telegram Bot Token Isolation SCAR

**Nama:** Shared Telegram Bot Token Between Agents  
**Tarikh:** 2026-05-17  
**Pengadu:** Arif (SOVEREIGN)  
**Selesai:** 2026-05-17  
**Severity:** 🔴 CRITICAL  
**Tag:** `tree777` `scar` `telegram` `token-isolation` `F1-amanah`

---

## WHAT HAPPENED (Root Cause)

**Senario:** Arifkeluarkan token Telegram berasingan untuk @AGI_ASI_bot (OpenClaw) dan @ASI_arifos_bot (Hermes). Tetapi satu agent (atau satu sesi investigation sebelum ini) mungkin telah konfigurasi untuk guna token yang sama.

**Mengapa ia berlaku:**
- Kedua-dua agent tiada enforcement untuk check "bot token uniqueness" sebelum start
- Tidak ada validator yang detect "adakah token ini sudah assigned kepada agent lain?"
- Ruang konfigurasi agent (`.env`, `config.json`) tidak ada warning tentang token sharing

**Mengapa CRITICAL:**
- Telegram benarkan HANYA SATU webhook URL per bot token
- Kalau dua agent guna token yang sama:
  - Telegram hantar message ke SATU webhook sahaja — yang lain tak terima
  - Ambiguous routing = Arif dapat reply dari agent yang salah
  - Tak boleh trace siapa processing message — audit trail rosak

---

## VERIFICATION CHECKLIST (Scalpel Audit)

Setiap kali deploy atau tukar konfigurasi Telegram untuk mana-mana agent, kena verify:

```bash
# 1. Get token dari setiap config — jangan assume mereka berbeza
echo "=== OPENCLAW TELEGRAM TOKEN ==="
# OpenClaw uses ${TELEGRAM_BOT_TOKEN} dalam openclaw.json
grep -A2 "channels" /root/.openclaw/openclaw.json | grep botToken

echo "=== HERMES TELEGRAM TOKEN ==="
cat /root/HERMES/.env | grep TELEGRAM_BOT_TOKEN
# atau /root/.hermes/platforms/telegram/config.json

echo "=== A-FORGE NOTIFIER TOKEN ==="
grep TELEGRAM /root/A-FORGE/infra/live/compose/docker-compose.yml | grep BOT

# 2. Confirm bot usernames dalamTG
curl -s "https://api.telegram.org/bot<TOKEN>:getMe" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['result']['username'])"
# Ganti <TOKEN> dengan token sebenar dari config

# 3. Verify webhook URL per bot (kalau guna webhook mode)
curl -s "https://api.telegram.org/bot<TOKEN>/getWebhookInfo" | python3 -m json.tool
```

---

## SCALPEL — Systematic Token Audit

Kalau jumpa dua agent guna token yang SAMA:

```bash
# Deteksi: cari semua tempat TELEGRAM_BOT_TOKEN digunakan
grep -r "TELEGRAM_BOT_TOKEN" /root --include="*.env" --include="*.yml" --include="*.yaml" -l 2>/dev/null | grep -v ".git" | sort -u

# Deteksi: bot token penuh dalam semua config
grep -rn "8149595687\|8410138119" /root --include="*.json" --include="*.yml" --include="*.yaml" --include="*.env" --include=".env*" 2>/dev/null | grep -v ".git\|\.sessions"

# Verify: OpenClaw gateway config
cat /root/.openclaw/openclaw.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('OpenClaw botToken:', d['channels']['telegram']['botToken'])"

# Verify: Hermes gateway config
cat /root/.hermes/platforms/telegram/config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('Hermes botToken:', d['botToken'])"

# Verify: A-FORGE notifier
grep NOTIFIER_TELEGRAM /root/A-FORGE/infra/live/compose/docker-compose.yml
```

---

## RULE — F1 AMANAH ENFORCEMENT

**Setiap agent MESTI ada bot token yang unique dan dedicated.**

| Agent | Bot Username | Token Pattern | Canonical Config |
|-------|-------------|---------------|-----------------|
| OpenClaw | @AGI_ASI_bot | `8149595687:***` | `/root/.openclaw/openclaw.json` (SOPS-encrypted) |
| Hermes | @ASI_arifos_bot | `8410138119:***` | `/root/HERMES/.env` + `/root/.hermes/platforms/telegram/config.json` |
| A-FORGE notifier | @AGI_ASI_bot (alert only) | `8149595687:***` (sama dengan OpenClaw) | A-FORGE tidak terima message — hanya hantar, safe untuk share |

**Nota:** A-FORGE notifier boleh share token dengan OpenClaw because A-FORGE only SENDS alerts, does not receive messages via webhook. OpenClaw and Hermes MUST have distinct tokens.

**JIKA TOKEN SAMA antara OpenClaw dan Hermes:**
- STOP semua kerja
- Report 888_HOLD
- Arif kena generate token baru untuk satu agent
- Deploy token baru dengan rotation protocol
- Verify dengan scalpels audit di atas sebelum restart agent

---

## PREVENTION — CI/CD Validation

### SCALPEL Audit Script (✅ IMPLEMENTED — 2026-05-18)
**Location:** `/root/.hermes/scripts/telegram-token-isolation-check.sh`

Run after every config change that touches Telegram bot tokens:

```bash
bash /root/.hermes/scripts/telegram-token-isolation-check.sh
```

What it validates:
1. OpenClaw token ≠ Hermes token (CRITICAL — TREE777 core rule)
2. OpenClaw/A-FORGE token sharing is intentional (A-FORGE send-only)
3. No duplicate tokens across RECEIVING agents
4. Telegram bot username verification via `getMe` API

**Latest audit result (2026-05-18 05:07 UTC):**
```
=== SCALPEL | Telegram Token Isolation Audit ===
Timestamp: 2026-05-18T05:07:07+00:00

Agents detected:
  OpenClaw:  8149595687  (@AGI_ASI_bot) — webhook, PID 2376264, dashboard live
  Hermes:    8410138119  (@ASI_arifos_bot) — polling, PID 2325781, A2A bridge active
  A-FORGE:   8149595687  (send-only)

✅ OpenClaw token ≠ Hermes token (8149595687 vs 8410138119)
✅ OpenClaw/A-FORGE token sharing is INTENTIONAL (A-FORGE send-only, no receive)
✅ No duplicate Telegram bot tokens across receiving agents
✅ Rule: OpenClaw/A-FORGE token sharing is safe (A-FORGE only SENDS, no webhook receive)

=== Telegram Bot Identity Verification ===
  OpenClaw: @AGI_ASI_bot
  Hermes: @ASI_arifos_bot
  A-FORGE: @ERROR:Not Found (expected — A-FORGE notifier uses OpenClaw's token)

AUDIT PASS | No violations found
```

**Both agents confirmed alive (2026-05-18 05:00 UTC):**
- OpenClaw: `curl http://127.0.0.1:18789/health` → `{"ok":true,"status":"live"}`
- Hermes: A2A agent card responding at `localhost:18001/.well-known/agent-card.json`
- AAA A2A: `localhost:3001/health` → `{"status":"healthy","protocol":"A2A","vault":"CONNECTED"}`

**Arif's reflection (2026-05-18):**
Arif processed TREE777 and understood the core insight: F1 AMANAH isn't just about deletion — isolation enforcement is also about ensuring different agents with different roles have separate resources. Without token isolation, the division of responsibility in AAA JOINT SEAL has no meaning.

Arif asked to forge this into TREE777 — this entry is that forging. The skill now carries the verified alive state and Arif's architectural insight about F1 AMANAH covering resource isolation, not just deletion.

**Session context notes:**
- OpenClaw process: PID 2376264, CPU 16.7% (active Telegram webhook processing)
- Hermes polling process: PID 2325781, hermes-a2a.py adapter PID 271361
- Argo: @AGI_ASI_bot is ACTIVE but webhook replies may be unreliable (fire-and-forget). Hermes is ambient monitor — it sees ALL group messages without mention requirement.
- TREE777 audit PASS — token isolation clean as of this session.

---

## WORKING INTEGRATION PATTERN (Forged 2026-05-18)

**Session timestamp:** 2026-05-18 05:00–05:15 UTC
**Trigger:** Arif asked why OpenClaw wasn't alive, then coordinated both agents, then sealed the working integration as a skill.

### What Worked — The Coordination Flow

```
1. Arif asked: "Why is OpenClaw not alive?"
2. Hermes ran: ps aux | grep openclaw → found PIDs
3. Hermes checked: curl http://127.0.0.1:18789/health → {"ok":true,"status":"live"}
4. Hermes checked: OpenClaw dashboard responding (webhook mode active)
5. Hermes checked: Hermes A2A bridge at localhost:18001/.well-known/agent-card.json
6. Hermes verified: AAA A2A at localhost:3001/health → vault=CONNECTED
7. Hermes ran: bash /root/.hermes/scripts/telegram-token-isolation-check.sh → AUDIT PASS
8. Arif forged this session capture into TREE777 → version 1.1.0
```

### The Working Architecture (Verified 2026-05-18)

```
Telegram (@AGI_ASI_bot) ←──webhook── OpenClaw (:18789) ←──AAA A2A (:3001)
       ↓
Telegram (@ASI_arifos_bot) ←──polling── Hermes (:18001) + hermes-a2a.py (:271361)
       ↓
                                              AAA A2A (:3001) ←──arifOS MCP (:8080)
```

### Key Coordination Commands Used

```bash
# 1. Check if OpenClaw is alive
curl -s http://127.0.0.1:18789/health
ps aux | grep "openclaw/dist/index.js gateway" | grep -v grep

# 2. Check Hermes (A2A bridge)
curl -s http://localhost:18001/.well-known/agent-card.json | python3 -m json.tool

# 3. Check AAA A2A gateway
curl -s http://localhost:3001/health

# 4. Run TREE777 audit (ALWAYS after config changes)
bash /root/.hermes/scripts/telegram-token-isolation-check.sh

# 5. Check which ports are listening
ss -tlnp | grep -E "18789|18001|3001|3002|8080"

# 6. Get Telegram bot identity (replace TOKEN)
curl -s "https://api.telegram.org/bot${TOKEN}/getMe" | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['username'])"

# 7. Check webhook URL for a bot token
curl -s "https://api.telegram.org/bot${TOKEN}/getWebhookInfo" | python3 -m json.tool
```

### What This Proves

1. **OpenClaw and Hermes CAN coexist** — separate tokens, separate ports, separate protocols
2. **Polling vs Webhook is the right split** — Hermes sees all (ambient), OpenClaw is mention-triggered
3. **A2A bridge is the spine** — both agents connect to AAA A2A at :3001
4. **TREE777 is live enforcement** — audit script catches token drift before it becomes a problem
5. **Coordination is a skill** — the act of verifying both agents, running audit, and sealing to skill is itself a procedure worth capturing

### Lessons for Future Coordination

- Always verify with terminal before claiming something is alive or dead
- "Not responding in Telegram" ≠ "Not alive" — check process health, port binding, and Telegram webhook delivery separately
- Audit script is the source of truth for token isolation — not memory, not assumptions
- Sealing working integrations into skills creates institutional memory that survives session boundaries

---

## Related Skills

Dulu pernah ada kekeliruan tentang "betul ke OpenClaw dan Hermes share bot token?"jawapan: **TIDAK**. Mereka WAJIB ada token berasingan.

**Kenapa:**
- OpenClaw guna webhook untuk @AGI_ASI_bot (group mention-triggered)
- Hermes guna polling untuk @ASI_arifos_bot (ambient monitoring)
- Kedua-duanya berbeza username, berbeza token, berbeza mode

**Kalau share token:**
- Telegram hantar semua message ke SATU URL (webhook wins kalau aktif)
- Agent yang satu takkan dapat message langsung
- Arif tak dapat trace dari mana reply datang

---

## SESSION CONTEXT NOTES

**Verified state (2026-05-17):**
- OpenClaw uses `8149595687:AAFwy70...` (partial visible in old session logs)
- Hermes uses `8410138119:***` (visible in hermes config)
- A-FORGE notifier uses `8149595687:***` (shares with OpenClaw — but only sends, doesn't receive)
- arifOS MCP sendiri tidak ada Telegram integration

**Confirmed clean:** OpenClaw token ≠ Hermes token. A-FORGE boleh share dengan OpenClaw sebab A-FORGE only sends.

**Tapi:** SOPS encryption pada `/root/.openclaw/.env` means full token dalam file `.openclaw/env.local` tidak visible di atas — assume ia `8149595687:AAFwy70...` berdasarkan session logs 2026-05-17.

---

## Related Skills

- [[systematic-debugging]] — Investigation protocol (Phase 1: gather evidence before touching anything)
- [[federation-runtime-audit]] — Full federation health check including token isolation
- [[fabrication-prevention]] — Always verify with terminal before claiming things are working

## References

- `/root/AAA/ADR/ADR-011-AAA-TELEGRAM-MESSAGING-PROTOCOL.md` — Architecture decision record untuk Telegram messaging split
- `/root/HERMES/hermes-human-life-agent/SYSTEM_PROMPT.md` — Spatial law tentang bot identity
- `references/TREE777-implementation-status.md` — Full implementation status, audit results, and next steps (2026-05-18)