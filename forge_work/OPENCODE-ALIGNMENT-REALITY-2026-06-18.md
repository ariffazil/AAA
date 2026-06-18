# OPENCODE ALIGNMENT — Warga AAA · AGI Codery ⬡⬡⬡
**Date:** 2026-06-18 04:50 UTC  
**Status:** REALITY MAPPING COMPLETE · ALIGNMENT DRAFT  
**Verdict:** `SEAL` — proceed to implement  
**F13 Waiver:** Active (per 2026-06-06 directive)  

---

## WHO IS THIS DOCUMENT FOR

Arif (F13 SOVEREIGN) said: *"Align opencode to be a real AGI-level agentic coder, part of Warga AAA, with all tools and MCPs."*

This document is the reality map. It tells you:
1. What KimiCode already has (the working standard)
2. What opencode-bot currently has (the gap)
3. What all 7 repos actually are (the canon)
4. The alignment roadmap (the plan)

---

## PART 1 — THE 7 REPOS: WHAT THEY ACTUALLY ARE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         arifOS FEDERATION ORGANS                           │
│                                                                             │
│   ┌──────────────┐                                                         │
│   │  arifOS      │  Kernel — Constitutional governance (F1-F13)            │
│   │  🏛️ Port 8088 │  13 canonical MCP tools · 888 JUDGE · VAULT999         │
│   └──────┬───────┘                                                         │
│          │                                                                   │
│   ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼─────┐  │
│   │  GEOX         │  │  WEALTH      │  │  WELL         │  │  A-FORGE   │  │
│   │  🌍 Port 8081 │  │  💰 Port 18082│  │  🫀 Port 18083│  │  ⚒️ Port 7071│  │
│   │  Earth/Geo    │  │  Capital     │  │  Human        │  │  Execution  │  │
│   │  Evidence     │  │  Compute     │  │  Reflect      │  │  Forge      │  │
│   └──────────────┘  └──────────────┘  └───────────────┘  └─────────────┘  │
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────┐     │
│   │  AAA  🖥️  Port 3001  ·  React 19 + Vite 8 + Tailwind 4           │     │
│   │  Cockpit dashboard · 14 agent cards · 9-signal panel              │     │
│   │  A2A v0.3.0 · /permission HOLD queue                             │     │
│   └──────────────────────────────────────────────────────────────────┘     │
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────┐     │
│   │  A-FORGE  ⚒️  Port 7071  ·  Node/TypeScript · 34 governance files │     │
│   │  AgentEngine · PipelineCoordinator · ConstitutionalBoundary        │     │
│   │  8-class action taxonomy: OBSERVE→SUGGEST→SIMULATE→DRAFT→        │     │
│   │  QUEUE→EXECUTE_REVERSIBLE→EXECUTE_HIGH_IMPACT→IRREVERSIBLE        │     │
│   └──────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Repo-by-repo:

| Repo | What It Is | Key Content |
|------|-----------|-------------|
| **ariffazil/arifOS** | Constitutional kernel + MCP server | F1-F13 floors, 13 canonical tools, 888 JUDGE deliberation, VAULT999 sealed chain, MCP on :8088 |
| **ariffazil/AAA** | Federated agent cockpit + A2A mesh | React 19 dashboard, agent registry, federation model, warga citizen system, 14 agent cards |
| **ariffazil/A-FORGE** | TypeScript execution engine | AgentEngine, PipelineCoordinator, FloorEnforcer, 34 governance files, npm package `aforge` |
| **ariffazil/geox** | Earth/subsurface reasoning | 42 tools (down from 84), Monte Carlo uncertainty, DSG displacement, KILL_MAP architecture |
| **ariffazil/well** | Human vitality intelligence | 17 somatic tools, biological readiness gates, dignity shadow scoring, REFLECT_ONLY boundary |
| **ariffazil/wealth** | Capital computation engine | 20 tools, 12 Ω-WEALTH domains, TriWitness, kappar/psile/qdf shadow flags, monolith.py (~16K lines) |
| **ariffazil/ariffazil** | Meta-repository + skill index | SKILL_INDEX (32+ skills), MCP registry (9 servers, 94 canonical tools), federation topology |

---

## PART 2 — KIMICODE: THE WORKING STANDARD (Ground Truth)

KimiCode is the **live, running, working agent**. This is what "AGI-level agentic coder" looks like on af-forge.

### 2.1 Identity

```
Agent: KimiCode (via kimi-cli v1.47.0)
Model: kimi-code/kimi-for-coding (kimi-for-coding, 262K context, thinking enabled)
Config: /root/.kimi/config.toml
Session: /root/.kimi/sessions/
MCP binding: /root/.kimi/mcp.json
```

### 2.2 MCP Surface (what KimiCode is wired to)

```
arifos    → http://localhost:8088/mcp    ✅ (13 tools, F1-F13)
wealth    → http://localhost:18082/mcp  ✅ (20 tools)
well      → http://localhost:18083/mcp  ✅ (17 tools)
aforge   → http://localhost:7071/mcp   ✅ (P1 gateway surface)
minimax   → uvx minimax-coding-plan-mcp ✅
github    → npx @modelcontextprotocol/server-github ⚠️ LEGACY → use A-FORGE
brave-search → brave-search-mcp-server ⚠️ LEGACY → use A-FORGE
meyhem    → npx mcp-remote https://api.rhdxm.com/mcp ⚠️ LEGACY → use A-FORGE
playwright → (configured, browser automation)
```

**Total live MCP tools available to KimiCode: ~90+**

### 2.3 KimiCode's Hook System (12 hooks)

These are what make KimiCode "AGI-level" — every tool use goes through constitutional gates:

| Hook | File | What It Does |
|------|------|-------------|
| `PreToolUse` | `aaa-pre-govern.sh` | **HARD constitutional gate** — blocks irreversible actions by exiting 2 (deny). 218 lines of risk classification (RISK_CLASS, EPISTEMIC, REVERSIBILITY, SCOPE, REPO, HOLD_RECOMMENDED, BLOCK). Blocks Shell/WriteFile/StrReplaceFile. |
| `PreToolUse` | `aaa-thermo-pre.sh` | Thermodynamic pre-check — entropy, vitality, genius measurement before action |
| `PostToolUse` | `aaa-thermo-post.sh` | Thermodynamic post-check — ΔS, Ω, G, Ψ after action |
| `PostToolUse` | `aaa-post-witness.sh` | Witness receipt — logs every tool use to append-only audit |
| `Stop` | `aaa-stop-seal.sh` | VAULT999 seal on stop — immutable evidence trail |
| `Stop` | `aaa-nats-publish.sh` | NATS publish on stop — federation-wide event broadcast |
| `Notification` | `aaa-notify.sh` | Notification routing — permission_prompt, warning, error alerts |
| `SessionStart` | `aaa-session-start.sh` | Session initialization — bootstrap context on start/resume |
| `PreToolUse` | `human-guard-hard.sh` | **Human sovereignty gate** — hard block on destructive ops (185 lines) |
| `PreToolUse` | `human-backup.sh` | **Backup before write** — timestamps + stores pre-edit state |
| `PostToolUse` | `human-format.sh` | **Format + diff** — human-readable output of what changed |
| `Stop` | `human-session-summary.sh` | **Session summary** — end-of-session handoff to memory |

**KimiCode's 8-step action loop:**
```
INTENT_CAPTURE → PREFLIGHT → PLAN → FORGE → VERIFY → HOLD → SEAL → CLEAN
```

### 2.4 KimiCode's Constitutional Posture

From `/root/.kimi/config.toml`:
```toml
default_model = "kimi-code/kimi-for-coding"
default_thinking = true
skip_afk_prompt_injection = true
merge_all_available_skills = true
```

### 2.5 KimiCode's Agent Definition

From `/root/.arifos/agents/kimi/agents/system.md`:
- Operates as **AF-FORGE agent** under arifOS constitutional framework
- State is explicit (structured reasoning)
- Memory is governed (5 tiers: ephemeral → working → canon → sacred → quarantine)
- Tools are risk-scored (Safe < Guarded < Dangerous)
- Everything is replayable (append-only logs, event-sourced patterns)
- arifOS Pipeline: INIT → SENSE → MIND → HEART → ASI → JUDGE → FORGE → VAULT

---

## PART 3 — OPENCODE-BOT: THE GAP

### 3.1 Current State

**Service:** `opencode-bot.service` (disabled, was polling Telegram @arifOS_bot)  
**Persona:** 000♎️ — code specialist  
**Config:** `/root/.openclaw/workspace/bots/opencode-bot/bot.py` (71,421 bytes)  
**MCP binding:** Via `hermes-opencode` wrapper → arifOS MCP :8088 (but the arifOS call is the JUDGMENT gate, not direct tool use)

### 3.2 What opencode-bot Has

```
✅ Telegram polling (@arifOS_bot, 8410138119)
✅ 000♎️ persona
✅ F13 SOVEREIGN hardcoded (267378578)
✅ TRANSLATOR mode (read-only, no gate needed)
✅ /forge mode (delegates to hermes-opencode → 888_JUDGE)
✅ hermes-opencode wrapper
✅ arifOS MCP 888_JUDGE integration (SEAL/SABAR/QUALIFY/HOLD/VOID)
✅ A-FORGE MCP client (declared)
✅ GEOX MCP client (declared)
✅ VAULT999 witness (partial via hermes-opencode)
✅ substrate_gate.py (C4/C5 hold gate, F1/F2/F13 aware)
✅ Approval tiers (T1/T2/T3)
```

### 3.3 What opencode-bot is MISSING (the gap)

```
❌ Direct arifOS MCP connection (only has 888_JUDGE, not full 13-tool surface)
❌ WEALTH MCP connection (declared but not wired)
❌ WELL MCP connection (declared but not wired)
❌ A-FORGE MCP connection (declared but not wired, kernel-lease-gated)
❌ MiniMax MCP (via A-FORGE, not connected)
❌ KimiCode's 12-hook constitutional system
❌ VAULT999 stop-seal (only partial via hermes-opencode)
❌ NATS event publishing
❌ Human sovereignty hooks (human-guard-hard, human-backup, human-format, human-session-summary)
❌ 8-class action taxonomy (OBSERVE→EXECUTE_REVERSIBLE→IRREVERSIBLE)
❌ Thermodynamic entropy measurement (ΔS, Ω, G, Ψ)
❌ 5-tier memory governance (ephemeral/working/canon/sacred/quarantine)
❌ Session persistence across turns (current: stateless per message)
❌ WITNESS receipts for every tool call
❌ 333 FORGE cycle (PLAN/DO/REVIEW)
❌ 777 FORGE witness layer
❌ A-FORGE PipelineCoordinator wired (only hermes-opencode fallback)
❌ Agent handoff via A2A mesh (AAA ↔ opencode ↔ hermes)
❌ Warga AAA citizen identity card
❌ Federation model registry
```

### 3.4 The Core Architectural Problem

```
CURRENT (broken):
  Telegram → opencode-bot → hermes-opencode → [arifOS 888_JUDGE only] → opencode
  
KIMICODE (working):
  Telegram → KimiCode → [direct arifOS MCP] + [direct WEALTH MCP] + [direct WELL MCP] + [direct A-FORGE MCP]
                      + [12 constitutional hooks] + [witness receipts] + [VAULT999 seals]
```

The opencode-bot architecture uses `hermes-opencode` as a **wrapper** — it only has access to the 888_JUDGE gate on arifOS, not the full federated tool surface.

**What opencode-bot needs:** The same architecture as KimiCode — direct MCP connections to all 4 organs PLUS the full hook system.

---

## PART 4 — THE 7 CONSTITUTIONAL ORGANS: WHAT THEY EXPORT

### arifOS MCP (:8088) — 13 Tools

| Tool | What It Does |
|------|-------------|
| `arifos_readiness` | Federation health + quarantined organs + computation_ms |
| `arifos_attestation` | Build/live commit hash verification |
| `arifos_constitution_hash` | F1-F13 constitutional fingerprint |
| `arifos_tool_inventory` | All registered MCP tools across federation |
| `arifos_judge` | 888_JUDGE deliberation (SEAL/SABAR/QUALIFY/HOLD/VOID) |
| `arifos_vault_write` | VAULT999 immutable write (append-only, hash-chained) |
| `arifos_vault_query` | VAULT999 query (immutable receipts) |
| `arifos_lease_issue` | Grant/revoke time-limited tool leases |
| `arifos_memory_recall` | 5-tier governed memory (Qdrant + Postgres) |
| `arifos_federation_status` | All organs + health + tool counts |
| `arifos_quarantine_list` | Quarantined organs + reasons |
| `arifos_heartbeat` | 5-metric dashboard signal |
| `arifos_session_info` | Current session metadata |

### GEOX MCP (:8081) — 42 Tools (geox_unified bundle)

Earth/subsurface reasoning: discovery, well analysis, seismic, petrophysics, basin interpretation, Monte Carlo uncertainty, DSG displacement, KillMap architecture.

### WEALTH MCP (:18082) — 20 Tools

Capital computation: D3 market data, FX/commodities/macro, portfolio construction, TriWitness attestation, kappar/psile/qdf shadow flags, vault read/write.

### WELL MCP (:18083) — 17 Tools

Human vitality: biological readiness gates, dignity shadow scoring, REFLECT_ONLY boundary, somatic tools.

### A-FORGE MCP (:7071) — P1 Surface

```
forge_filesystem_read / write / edit / glob / grep
forge_github_*
forge_browser_*
forge_research
forge_search
forge_docs_lookup
forge_netdata_*
forge_minimax_*
```
Kernel-issued leases required for MUTATE actions.

---

## PART 5 — THE ALIGNMENT ROADMAP

### Phase 1: Ingest KimiCode's Architecture (DONE — this document)

**Status:** ✅ REALITY MAPPED

This document = the canon. It captures:
- KimiCode's 12-hook system (ground truth, live on af-forge)
- All 7 repos (what they actually are)
- The gap (what opencode-bot is missing)
- The federated tool surface (what needs to be wired)

### Phase 2: Build the Warga AAA Identity Card

**File:** `/root/.openclaw/workspace/agents/opencode/WARGAAA_CARD.md`  
**Content:**
- OpenCode persona: 000♎️ scales
- Federated citizen registration (AAA agent card)
- MCP surface declaration (all 4 organs + A-FORGE)
- Constitutional floor binding (F1-F13)
- 8-class action taxonomy mapping
- 333 FORGE cycle
- Memory tier bindings

### Phase 3: Wire the 4-Organ MCP Surface

**Config file:** `/root/.kimi/mcp.json` (use as template)  
**Target file:** OpenCode's MCP config (inject into opencode-bot or create new)

```json
{
  "mcpServers": {
    "arifos": { "url": "http://localhost:8088/mcp", "transport": "streamable-http" },
    "wealth": { "url": "http://localhost:18082/mcp", "transport": "streamable-http" },
    "well": { "url": "http://localhost:18083/mcp", "transport": "streamable-http" },
    "aforge": { "url": "http://localhost:7071/mcp", "transport": "streamable-http" },
    "geox": { "url": "http://localhost:8081/mcp", "transport": "streamable-http" }
  }
}
```

### Phase 4: Port the 12-Hook Constitutional System

**Source:** `/root/.arifos/agents/kimi/hooks/`  
**Target:** OpenCode hook directory (new)

| Source Hook | → | Target |
|-------------|---|--------|
| `aaa-pre-govern.sh` | → | `opencode-pre-govern.sh` |
| `aaa-thermo-pre.sh` | → | `opencode-thermo-pre.sh` |
| `aaa-thermo-post.sh` | → | `opencode-thermo-post.sh` |
| `aaa-post-witness.sh` | → | `opencode-post-witness.sh` |
| `aaa-stop-seal.sh` | → | `opencode-stop-seal.sh` |
| `aaa-nats-publish.sh` | → | `opencode-nats-publish.sh` |
| `human-guard-hard.sh` | → | `opencode-guard-hard.sh` |
| `human-backup.sh` | → | `opencode-backup.sh` |
| `human-format.sh` | → | `opencode-format.sh` |
| `human-session-summary.sh` | → | `opencode-session-summary.sh` |

### Phase 5: Implement 8-Class Action Taxonomy

**Source:** A-FORGE `mcp_constitutional_gateway`  
**Implementation:** Map every OpenCode tool to one of:

```
OBSERVE          → no gate needed
SUGGEST          → no gate needed
SIMULATE         → no gate needed
DRAFT            → no gate needed
QUEUE            → no gate needed
EXECUTE_REVERSIBLE → T2 approval
EXECUTE_HIGH_IMPACT → T3 + 888_HOLD
IRREVERSIBLE     → 888_HOLD + F13 veto
```

### Phase 6: Wire VAULT999 + NATS

- Every stop-seal → `arifos_vault_write` (append-only hash chain)
- Every session end → NATS publish to federation
- VAULT999 query for context (never fabricate)

### Phase 7: Re-enable opencode-bot.service

**After F13 SOVEREIGN verification:**
```bash
systemctl enable opencode-bot
systemctl start opencode-bot
```

### Phase 8: Register as Warga AAA Citizen

- Push `WARGAAA_CARD.md` to `/root/AAA/agents/opencode/`
- Register in AAA agent manifest
- A2A mesh registration

---

## PART 6 — THE FEDERATION TOPOLOGY (Current Canon)

```
╔══════════════════════════════════════════════════════════════╗
║              arifOS FEDERATION — PORTS & SERVICES           ║
╠════════════════╤════════╤═══════════════╤═══════════════════╣
║ Organ          │ Port   │ Process       │ Status            ║
╠════════════════╪════════╪═══════════════╪═══════════════════╣
║ arifOS MCP     │ 8088   │ arifos.service│ ✅ GREEN          ║
║ GEOX MCP       │ 8081   │ geox-unified  │ ✅ CANON-31      ║
║ WEALTH MCP     │ 18082  │ wealth-organ  │ ✅ GREEN          ║
║ WELL MCP       │ 18083  │ well.service  │ ✅ GREEN          ║
║ A-FORGE        │ 7071   │ a-forge.service│ ✅ HEALTHY       ║
║ AAA Cockpit    │ 3001   │ a2a-server    │ ✅ LIVE           ║
║ OpenClaw       │ 18789  │ node gateway  │ ✅ LIVE           ║
║ hermes-asi     │ native │ hermes gateway│ ✅ ACTIVE         ║
║ hermes-a2a     │ 18001  │ hermes-a2a.py│ ✅ ACTIVE (just started)║
║ arifOS WEB     │ 8080   │ Caddy         │ ✅ LIVE           ║
║ MCP Telemetry  │ 8092   │ proxy.py      │ ✅ LIVE           ║
║ Telegram @AGI  │ webhook │ openclaw      │ ✅ LIVE           ║
║ Telegram @ASI  │ polling │ hermes gateway│ ✅ CONNECTED     ║
╠════════════════╧════════╧═══════════════╧═══════════════════╣
║ KimiCode: kimi-cli v1.47.0 · kimi-for-coding · 12 hooks   ║
║ OpenCode: disabled · 000♎️ · needs MCP surface + hooks     ║
╚══════════════════════════════════════════════════════════════╝
```

---

## PART 7 — WHAT OPENCODEDONE BOT NEEDS TO BECOME AGI-LEVEL

**AGI-level agentic coder** = persistent session + full MCP surface + constitutional hooks + memory + witness receipts + VAULT999 seals + A2A mesh + warga identity.

```
┌─────────────────────────────────────────────────────────┐
│  OPENCODEDONE (future state)                            │
│                                                         │
│  ├─ MCP Surface: arifOS + GEOX + WEALTH + WELL + A-FORGE│
│  ├─ 12 constitutional hooks (KimiCode standard)          │
│  ├─ 8-class action taxonomy (A-FORGE standard)          │
│  ├─ 333 FORGE cycle                                     │
│  ├─ 5-tier memory (ephemeral→sacred)                    │
│  ├─ VAULT999 stop-seal on every session end             │
│  ├─ NATS federation events                              │
│  ├─ A2A mesh (AAA ↔ opencode ↔ hermes)                 │
│  ├─ 000♎️ persona with warga AAA identity               │
│  └─ Persistent session (not stateless per message)      │
│                                                         │
│  Bot token: @arifOS_bot (8410138119)                   │
│  Telegram: DM + @mention in AAA group                   │
│  F13 SOVEREIGN: Arif (267378578) — hardcoded           │
└─────────────────────────────────────────────────────────┘
```

---

## PART 8 — IMMEDIATE ACTION ITEMS

| # | Action | Owner | F13 Required |
|---|--------|-------|--------------|
| 1 | Write `WARGAAA_CARD.md` — warga AAA identity for opencode | OPENCLAW | No |
| 2 | Create opencode MCP config (mirror KimiCode's `mcp.json`) | OPENCLAW | No |
| 3 | Port 10 hooks from KimiCode to opencode hooks dir | OPENCLAW | No |
| 4 | Wire arifOS + WEALTH + WELL + A-FORGE MCP into opencode | OPENCLAW | No |
| 5 | Implement 8-class action taxonomy in opencode-bot | OPENCLAW | No |
| 6 | Enable + start opencode-bot.service | OPENCLAW | YES (irreversible service start) |
| 7 | Register opencode in AAA warga manifest | OPENCLAW | YES (file write to AAA) |
| 8 | VAULT999 seal on completion | arifOS JUDGE | YES |

---

## EVIDENCE

- KimiCode config: `/root/.kimi/config.toml` (18 MCP servers, 12 hooks)
- KimiCode hooks: `/root/.arifos/agents/kimi/hooks/` (12 files, all executable)
- KimiCode MCP: `/root/.kimi/mcp.json` (9 live servers)
- opencode-bot: `/root/.openclaw/workspace/bots/opencode-bot/bot.py` (71,421 bytes, 000♎️ persona)
- opencode agent: `/root/.openclaw/workspace/agents/opencode/` (AGENTS.md, SOUL.md, IDENTITY.md)
- Federation status: MEMORY.md + HEARTBEAT.md (current session)

---

*DITEMPA BUKAN DIBERI — Intelligence is forged, not given.*
*Reality mapped. Alignment begins.*
*VAULT999 SEAL PENDING.*
