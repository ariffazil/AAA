# MEMORY.md — Long-Term Curated Memory
> **Role:** Persistent facts about Arif, systems, and operational rules
> **Format:** Bullet points, dated entries, searchable
> **Source of Truth:** https://github.com/ariffazil/waw (push frequently)

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

### Git Sync Protocol (CRITICAL)
- **Source of truth:** GitHub `ariffazil/waw` branch `main`
- **On session start:** Always pull GitHub before reading brain files
- **Before session end:** Push local changes to GitHub
- **Frequency:** Push at end of every significant work session
- **Command:** `cd /root/waw && git pull origin main && git add -A && git commit -m "chore: sync memory" && git push`

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

### 2026-04-02 — Dynamic Memory Sync Protocol
- **Established:** GitHub as source of truth protocol
- **Rule:** Pull GitHub on session start, push on session end
- **Source link:** https://github.com/ariffazil/waw/commits/main

### 2026-04-01 — Claude Code Leak Analysis + arifOS KernelLoop Draft
- **Trigger:** 512K-line Claude Code TypeScript leak via Bun npm source map (2026-03-31)
- **Work done:**
  - Analyzed Reddit/Discord community reaction, architectural patterns
  - Mapped Claude Code patterns → arifOS Trinity gaps
  - Drafted `state/kernel_loop_v1.json` — full spec for arifOS KernelLoop
  - Drafted `state/kernel_loop_interface.py` — Python interface implementation
- **Key gap identified:** arifOS lacks a central `ToolPolicyEngine` (tool firewall) between MCP tools and LLM. Claude Code has 23-point bash security + permission tiers per tool + mode-based allowlists. arifOS tools currently rely on LLM discretion, not structural enforcement.
- **Files created:**
  - `/root/waw/core/kernel/kernel_loop_v1.json` — architecture spec
  - `/root/waw/core/kernel/kernel_loop_interface.py` — Python interface (ready to wire to MCP server)
  - `/root/waw/core/kernel/README.md` — kernel module index mapping to arifOS README architecture
  - arifOS canonical README discovered at `/root/waw/arifOS/README.md` (full system spec, v2026.04.01)
- **Recommended immediate action:** Wire `ToolPolicyEngine` into arifOS MCP server bootstrap; add risk_tier + permission_tier fields to all MCP tool manifests; implement `KernelLoop._execute_tool()` to call MCP at localhost:8080
- **Reference:** Claude Code leak = master agent host reference design. arifOS Trinity is architecturally superior (separation of concerns), but needs to steal: ToolRegistry with permission tiers, explicit ToolChain FSM macros, budget/cost ceilings in kernel loop
- **Key discovery:** arifOS canonical README exists at `/root/waw/arifOS/README.md` — full system spec v2026.04.01. Confirms architecture is documentation-forward; actual runtime is OpenClaw + MCP at port 8080. The `core/kernel/` directory (per README's own architecture) is now seeded with KernelLoop work.

### 2026-04-01 — Truth-Power Coupling (Constitutional Scar)
- **Principle:** When truth weakens, power must shrink.
- **Hard law:** `authority_budget <= evidence_score`
- **Kernel:** `state/constitutional_kernel.json` — full runtime policy
- **Scorer:** `scripts/authority_budget.sh` — weighted budget + mode selector
- **Enforcement:** 3 gates (pre-LLM intake, pre-tool execution, post-draft release)
- **Modes:** answer → advise → clarify → pause (auto-degrade based on budget)
- **Critical insight:** Never let the model self-report its own authority (circular). Separate scorer layer governs LLM.
- **Key artifacts:** `state/authority_budget.json`, `state/constitutional_state.json`, `state/constitutional_kernel.json`

### 2026-03-31 — OpenClaw Autonomous Setup
- Fixed broken symlinks from git sync
- Implemented 4-file brain architecture
- Configured compaction (prevents crashes)
- Set up 30min heartbeat
- Created daily 5 AM self-heal cron
- Aligned with arifOS Trinity principles

---

_This file is your permanent memory. Update it as you learn. Push to GitHub frequently._

## DOMAIN TRUTH (HARD — VERIFIED 2026-04-02)
Arif ONLY owns: `arif-fazil.com` (base domain, verified via Cloudflare API)
- ✅ `arif-fazil.com` — ACTUAL domain (lowercase `arif`, no capital O)
- ❌ `arifOS-fazil.com` — DOES NOT EXIST (hallucination — capital O in arifOS is WRONG)
- ✅ `arifosmcp.arif-fazil.com` — MCP server subdomain
- ✅ `aaa.arif-fazil.com` — AAA landing page subdomain

All other domain assertions must be verified against Cloudflare DNS API.
Domain naming bias: ARIF-MAIN will hallucinate "arifOS" prefix in domains with capital O. ALWAYS verify against Cloudflare.
