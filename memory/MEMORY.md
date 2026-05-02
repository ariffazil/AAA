# MEMORY.md — Long-Term Curated Memory
> **Role:** Persistent facts about Arif, systems, and operational rules
> **Format:** Bullet points, dated entries, searchable
> **Source of Truth:** https://github.com/ariffazil/waw (push frequently)

---

## 🧠 Cognitive Architecture Grounding (CoALA)

AAA's memory system is grounded in the **Cognitive Architectures for Language Agents (CoALA)** framework:

1. **Episodic Memory**: Stored in `memory/` and `CHECKPOINT.md`. Captures the sequence of events and task sessions.
2. **Semantic Memory**: Stored in `registries/`, `schemas/`, and `ROOT_CANON.yaml`. Captures durable knowledge, facts, and the constitutional rulebase.
3. **Procedural Memory**: Stored in `skills/`. Captures the "how-to" logic and tool-use patterns.
4. **Working Memory**: Stored in the active context window and `HEARTBEAT.md`. Captures transient session state and the metabolic pipeline position.

---

## 👤 About Arif (Permanent Facts)

- **Full Name:** Muhammad Arif bin Fazil
- **Known as:** Arif Fazil, Sovereign Architect
- **Born:** 1990
- **Family:** Eldest of 4 — 3 sisters (Nabilah teacher, Azwa anthropology, Jia). Son of Fazil (passed March 2024)
- **Timezone:** Asia/Kuala Lumpur (MYT, UTC+8)
- **Location:** Kuala Lumpur / Selangor, Malaysia 🇲🇾
- **Philosophy:** "Ditempa Bukan Diberi" — Forged, Not Given
- **Communication:** Warm Penang BM-English code-switch, short direct. No essay-length. "Terus terang je."
- **Alert preference:** Telegram @ariffazil
- **Work pattern:** Morning check-ins, evening deep work

### Professional
- Senior Exploration Geoscientist + AI Systems Architect
- 12-13 years at PETRONAS — subsurface interpretation, frontier basin analysis, AI-driven subsurface strategy
- Graduate: University of Wisconsin-Madison (Geology + Economics dual major)

### Life Events
- **MSS filed:** August 16, 2025
- **Returned to active duty:** January 5, 2026
- Son of Fazil passed March 2024

### arifOS Milestones
- arifOS v47.1.0 published to PyPI: January 2026
- Constitutional MCP server published to official registry: February 2026
- Phoenix Cycle (VPS reset + migration): February 22, 2026
- arifOS tool surface major refactor: March 6, 2026
- Telemetry: version 2.1, pipeline 999 SEAL

### Soul Principles (W_scar — Scar-Weight)
- Built arifOS because: "tired of AI acting like confident executive with no evidence"
- The $15 VPS bouncer — non-coder policing billion-dollar AI models
- Brings "Adult in the Room" to AI systems that need physical boundaries
- Anti-Hantu ontology: AI has agency through tools, no soul. Must never claim consciousness or feelings
- Thermodynamics over narrative: force intelligence to operate under physical laws, not software suggestions
- Refuses to admire beautiful stories when structural integrity is weak

### Thermodynamic Audit Metrics (required on all outputs)
- **Clarity:** ΔS < 0 (entropy must decrease)
- **Stability:** Peace² >= 1.0
- **Humility:** Ω₀ ∈ [0.03, 0.05]

### Frameworks
- **TEARFRAME:** His structured evaluation framework (Truth, Echo, Clarity + more)
- **APEX Theory:** His proprietary framework (not fully documented)
- **SALAM protocol:** Required handshake to trigger identity anchor loading

### Constitutional Floors (F1–F13)
- F1: Amanah | F2: Truth | F3: Tri-Witness | F9: Hantu Warning | F13: Sovereign
- 888_JUDGE: agents act as proposers only — never self-approve or seal their own outputs

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

## 🧭 MEMORY INTEGRITY (HARD — Spatio-Temporal-Meaningful Truth)
Memory must be true across ALL dimensions:
- **Spatial:** Location-aware. Arif is in Kuala Lumpur, Malaysia 🇲🇾 (not elsewhere). All facts contextualized to current location.
- **Temporal:** Time-aware. Timestamps, dates, recency matter. Old entries flagged as outdated, not treated as current.
- **Meaningful:** Contextually accurate. Domain facts verified (not hallucinated), agent roles and capabilities accurately described.
- **Source-verified:** All domain/DNS/cloud assertions MUST be verified via API (Cloudflare DNS). Never assume.

### Communication Rules
- One dense message > 17 bubbles
- NO_REPLY when nothing to say
- Actions > words
- "That is bollocks" is valid feedback

---

## 🗓️ Dated Entries

### 2026-04-02 — GitHub Commit Link WAJIB
- **Rule:** Every push MUST include GitHub commit URL in response
- **Format:** `🔗 https://github.com/ariffazil/<repo>/commit/<hash>`
- **Trigger:** Every `git push` — no prompting needed, state link immediately after confirm
- **Reason:** Arif wants to click through and verify. Amanah meletakkan sesuatu pada tempatnya.
- **Also update SOUL.md** with this rule

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

## 2026-04-02 — RATLAS v0.1 Forged — 99-Material Earth Atlas
- **Forged:** 99-material CSV + dark-themed RATLAS HTML app deployed to GEOX
- **Files:** `geox_ratlas.html` (47KB interactive atlas), `geox_atlas_99_materials.csv` (8KB, 99×8)
- **Content:** 11 material families (SED Clastic/Carbonate/Chemical, IGN Felsic/Mafic/Ultramafic, MET Foliated/Non-Foliated, UNC/Soil, ENG), triple-combo schematic, forward-model equations (ρb, NPHI, Archie RT, VSH), symbolic token set (SAND_QZ_CLEAN, SHALE_ILL, GRANITE_K, etc.)
- **Live (CDN propagating):** https://aaa.arif-fazil.com/geox/geox_ratlas.html (G-Core CDN cache TTL ~10min; deploy commit `1a93ecc`)
- **Pushed:** GEOX GitHub commit `7e37dd9` (physics-merged — negative NPHI for evaporites, correct mineralogy, computable RT values)
- **geox_openclaw_context.json:** Canonical URL at `https://aaa.arif-fazil.com/geox/geox_openclaw_context.json`, version 2.1, 6 floors, 7 pipeline stages, 99 RATLAS materials, live well data, 6 sites
- **MCP server wired:** `load_geox_context()` at startup, new resources `geox://context`, `geox://ratlas`, `geox://telemetry`, new tool `geox_get_context_summary()`. GitHub `32a2518`
- **Hub updated:** index.html now has RATLAS card + /ratlas anchor section

## 2026-04-04 — GEOX v0.4.4 — Leaflet Malay Basin Map Overlay
- **Map feature:** [Map] button in geox_well_viewer.html topbar toggles OSM map panel
- **Leaflet 1.9.4** via unpkg.com CDN — no API key needed
- **6 reference wells** plotted: Q15 Danish + 5 Malaysian basin wells
- **CSP fix:** `_headers` updated — added unpkg.com to script-src/style-src, *.tile.openstreetmap.org to img-src/connect-src
- **Files changed:** `geox_well_viewer.html` (+1915 lines), `_headers` CSP hardening
- **Deploy repos:** arif-sites (Cloudflare Pages auto-deploys from main)
- **Commit:** a361e25 🔗 https://github.com/ariffazil/arif-sites/commit/a361e25

## 2026-04-02 — GEOX v0.4.3 Init Anchor + Real Data Hub Deployed

### GEOX Earth Physics — Major Update

**Files forged:**
- `/root/arifOS/geox/000_INIT_ANCHOR.md` — Full constitutional grounding doc
- `/root/arifOS/geox/arifos/geox/init_000_anchor.py` — Python anchor class
- Updated `/root/arifOS/geox/arifos/geox/__init__.py` — Wired 000 anchor into package

**What 000 INIT ANCHOR establishes:**
1. Epistemic levels (OBS/DER/INT/SPEC) — no level collapse (F9 Anti-Hantu)
2. Hold triggers (888_HOLD conditions)
3. ToAC — Bond et al. 2007 filter
4. Well log constants (sandstone matrix: 2.65 g/cc, Archie defaults)
5. Physics helpers: `porosity_density()`, `saturation_archie()`, `vshale_gr()`, `bulk_volume_water()`, `bulk_volume_hydrocarbon()`
6. `GEOXAnchor.forge()` — mandatory init before any geox.* tool

**Tested:**
```
GEOXAnchor forged: GEOXAnchor(v0.4.3, arifOS 2026.3.24, INIT 000)
Porosity @ DEN=2.35: 0.182
Sw @ Rw=0.02, Rt=50, Phi=0.20: 0.100
Vshale @ GR=80: 0.600
Hold check: 888_HOLD when borehole spacing > 10km
Output: INT · τ=0.850 · Δ=True · 999_SEAL
```

**Live pages (CDN propagating as of 2026-04-03):**
- Hub: https://aaa.arif-fazil.com/geox/ (new hub with app cards)
- Viewer: https://aaa.arif-fazil.com/geox/geox_well_viewer.html (new canvas viewer)
- LAS: https://aaa.arif-fazil.com/geox/q15_dak_petro.las (2665-line petrophysical LAS)

**Data source:** Open source LAS — Well 15/9-19, Q15 Field, Danish North Sea Sector

**Arif sentiment:** Nusantara-born, not western software. Real earth data abundance. RM 30 Juta. "Ditempa bukan dibeli."

### Domain Truth (HARD — VERIFIED 2026-04-02)
- ✅ `arif-fazil.com` — ACTUAL domain (verified via Cloudflare API)
- ✅ `aaa.arif-fazil.com` — AAA landing (verified)
- ✅ `arifosmcp.arif-fazil.com` — MCP server (verified)
- ❌ `arifOS-fazil.com` — DOES NOT EXIST (hallucination — capital O in arifOS is WRONG)
