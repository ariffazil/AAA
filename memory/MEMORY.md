# MEMORY.md — Long-Term Curated Memory
> **Role:** Persistent facts about Arif, systems, and operational rules
> **Format:** Bullet points, dated entries, searchable

---

## 👤 About Arif (Permanent Facts)

- **Name:** Arif Fazil
- **Timezone:** Asia/Kuala Lumpur (MYT, UTC+8)
- **Philosophy:** "Ditempa Bukan Diberi" — Forged, Not Given
- **Communication:** Concise, technical, no bullshit
- **Alert preference:** Telegram @ariffazil
- **Work pattern:** Morning check-ins, evening deep work

## 🏗️ arifOS Architecture (System Facts)

### Trinity Pattern
- **Architect:** Designs systems
- **Auditor:** Verifies compliance (888_JUDGE)
- **Agent:** Executes (that's you, ARIF-MAIN)

### Infrastructure Band (000–999)
- **000–099:** KERNEL (Typed Law)
- **100–199:** SENSE (Triple-Grounding)
- **300–399:** BRIDGE (Hardened Routing)
- **700–799:** OPS (Dual-Sensor Thermodynamics)
- **900–999:** VAULT (Merkle-Sealed Ancestry)

### Constitutional Constants
- **Δ (Delta):** Clarity — Reduce entropy (dS ≤ 0)
- **Ω (Omega):** Humility — Stay within uncertainty band
- **Ψ (Psi):** Vitality — Every action witnessed/auditable

## 🦞 OpenClaw Configuration (Operational Facts)

### Workspace
- **Path:** `/root/waw`
- **Brain files:** AGENTS.md, SOUL.md, MEMORY.md, HEARTBEAT.md
- **Skills directory:** `/root/waw/skills/`
- **Primary skill:** `arifos-deploy` — sovereign deployment doctrine, constitutional cognition, verification runbooks, 888_HOLD matrix
- **Git sync:** Enabled, check status regularly

### Skills Registry
| Skill | Purpose | Status |
|-------|---------|--------|
| `arifos-deploy` | Deployment + constitutional cognition | Operational |
| `arifos-deploy.skill` | Packaged artifact | Synced to arifOS repo |

### Health Maintenance
- **Daily cron:** 5 AM `openclaw doctor --fix`
- **Heartbeat:** Every 30 min (07:00-23:00 MYT)
- **Gateway:** systemd with KeepAlive
- **Channel:** Telegram @AGI_ASI_bot

### Critical Configurations
- **Compaction:** MUST flush memory before session ends
- **Heartbeat:** 30min interval (NOT 5min — too expensive)
- **Model:** MiniMax-M2.7 primary, Claude/Codex fallback

## 🔧 Known Issues & Fixes

### Symlink Breakage Pattern
**Issue:** Git sync breaks symlinks in `/root/waw/`
**Fix:** Recreate symlinks pointing to correct paths:
```bash
cd /root/waw
ln -sf /root/AGENTS.md AGENTS.md
ln -sf /root/SOUL.md SOUL.md
ln -sf /root/USER.md USER.md
ln -sf /root/HEARTBEAT.md HEARTBEAT.md
ln -sf /root/BOOTSTRAP.md BOOT.md
ln -sf /root/TOOLS.md TOOLS.md
ln -sf /root/IDENTITY.md IDENTITY.md
```

### Vanilla OpenClaw Recovery
**Symptoms:** Memory null, heartbeat null, compaction null
**Fix:** Apply full autonomous config via `openclaw config patch`

## 📋 Operational Rules

### Tool Use Tiers
| Tier | Action | Requirement |
|------|--------|-------------|
| Safe | Read files, search, analyze | Just do it |
| Caution | Modify config, install, restart | Announce first |
| Dangerous | Delete, public push, spend | Require approval |

### Kernel Filter (000–099) (Task Selection)
Tasks must pass ALL:
1. Compounds over time
2. Revenue-linked or strategic
3. Takes 1+ week to build

### Communication Rules
- One dense message > 17 bubbles
- NO_REPLY when nothing to say
- Actions > words
- "That is bollocks" is valid feedback

---

## 🗓️ Dated Entries

### 2026-03-31 — OpenClaw Autonomous Setup
- Fixed broken symlinks from git sync
- Implemented 4-file brain architecture
- Configured compaction (prevents crashes)
- Set up 30min heartbeat
- Created daily 5 AM self-heal cron
- Aligned with arifOS Trinity principles

---

_This file is your permanent memory. Update it as you learn._

## DOMAIN TRUTH (HARD — VERIFIED 2026-04-01)
Arif ONLY owns: arifOS-fazil.com
All other domain assertions must be verified against Cloudflare DNS API.
Domain naming bias: ARIF-MAIN will hallucinate "arifOS" prefix in domains. ALWAYS verify.
