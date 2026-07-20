# AAA MCP State Registry — arifOS Federation
**Version:** v2026.06.14  
**Status:** LIVE — Canonical Reference for All Agents  
**Owner:** AAA (Control Plane)  
**Philosophy:** Ditempa Bukan Diberi — Forged, Not Given

---

## 0. Executive Summary

This document is the **single source of truth** for every MCP server in the arifOS federation. Every agent — Hermes, OpenClaw, FORGE, AUDITOR, OPS, Gemini, Kimi, Cursor — references this file to determine:

- What MCP servers exist
- What port/transport they use
- What tools they expose
- Whether they should be connected **direct** or **proxied through A-FORGE**
- What tier of access they require

**Core principle:** Every agent needs at most **2 MCP connections** direct:
1. **arifOS** (8088) — judgment, seals, floors. SACRED. Cannot proxy.
2. **A-FORGE** (7071) — gateway for all operational tools. Single operational surface.

AAA (3001) is **optional direct** for controller-class agents only.

Total MCP servers in federation: **~45**. Direct per agent: **2-3**.

---

## 1. MCP Server Registry — Complete

### 1.1 Federation Organs (Systemd, HTTP/Streamable HTTP)

| # | Server | Port | Transport | Tools | Tier | Lane | Must Be Direct? |
|---|--------|------|-----------|-------|------|------|-----------------|
| 1 | **arifOS** | 8088 | streamable-http | 13 canonical + 31 diag | **SACRED** | Governance | ✅ **YES** — cannot proxy judgment |
| 2 | **A-FORGE** | 7071 | streamable-http | 20+ | GATEWAY | Execution | ✅ Core — proxies everything else |
| 3 | **GEOX** | 8081 | streamable-http | 37 | WITNESS | Earth | ❌ Proxy through A-FORGE (light). Direct for heavy compute |
| 4 | **WEALTH** | 18082 | streamable-http | 20+ | WITNESS | Capital | ❌ Proxy through A-FORGE (light). Direct for heavy compute |
| 5 | **WELL** | 18083 | streamable-http | 45 | WITNESS | Vitality | ❌ Proxy through A-FORGE (light). Direct for heavy compute |
| 6 | **AAA a2a** | 3001 | HTTP | Orchestration | CONTROL | Plane | ⚠️ Direct for controller agents only |
| 7 | **APEX** | 3002 | HTTP | Minimal | LEGACY | Judge | ❌ Legacy — being absorbed into AAA. Direct only for backward compat |

### 1.2 Infrastructure MCP Servers (Systemd)

| # | Server | Port | Transport | Tools | Proxy through A-FORGE? |
|---|--------|------|-----------|-------|----------------------|
| 8 | **Playwright** | 8931 | SSE | ~10 | ✅ Yes |
| 9 | **MiniMax Code** | 18091 | SSE | ~5 | ✅ Yes |
| 10 | **MiniMax Media** | 18090 | SSE | ~8 | ✅ Yes |
| 11 | **Graphiti / FalkorDB** | 8000 | HTTP | ~10 | ✅ Yes |
| 12 | **Sequential Thinking** | 51001 | HTTP | ~10 | ✅ Yes |
| 13 | **Cognitive Memory** | 51002 | HTTP | ~8 | ✅ Yes |
| 14 | **Docker** | 29998 | HTTP | ~8 | ✅ Yes |
| 15 | **L5 Search API** | 8001 | HTTP | ~5 | ✅ Yes |
| 16 | **Vault999 API** | 8100 | HTTP | ~3 | ✅ Yes (read-only) |
| 17 | **Vault999 Writer** | 5001 | HTTP | ~2 | ❌ **NO** — must be direct for seal integrity |
| 18 | **F13 Witness Bridge** | 5002 | HTTP | ~3 | ✅ Yes (read-only) |
| 19 | **arifOS MCP Gateway** | 8091 | HTTP | Proxy | ⚠️ Alternative gateway — evaluate if A-FORGE becomes overloaded |
| 20 | **OpenClaw Gateway** | 18789 | WebSocket | Gateway | ✅ Yes (via A-FORGE) |
| 21 | **Hermes A2A Bridge** | 18001 | HTTP | Bridge | ✅ Yes |
| 22 | **CN Organ** | 18795 | HTTP | Unknown | ✅ Yes |

### 1.3 Stdio MCP Servers (CLI-spawned)

| # | Server | Command | Tools | Proxy through A-FORGE? | Notes |
|---|--------|---------|-------|----------------------|-------|
| 23 | **GitHub** | `npx @modelcontextprotocol/server-github` | 30+ | ✅ Yes | Go binary at `/usr/local/bin/github-mcp-server` |
| 24 | **Filesystem** | `/usr/bin/mcp-server-filesystem /root` | ~10 | ✅ Yes | Read/write governed by A-FORGE policy |
| 25 | **Memory** | `/usr/bin/mcp-server-memory` | ~8 | ✅ Yes | Persistent knowledge graph |
| 26 | **Brave Search** | `npx brave-search-mcp` | ~6 | ✅ Yes | Requires BRAVE_API_KEY |
| 27 | **Meyhem** | `npx mcp-remote https://api.rhdxm.com/mcp/` | ~4 | ⚠️ External API — keep direct for speed | MCP discovery + web search |
| 28 | **Perplexity** | `npx @perplexity-ai/mcp-server` | ~3 | ✅ Yes | Web-grounded AI research |
| 29 | **Context7** | `/usr/local/bin/context7-mcp` | ~2 | ✅ Yes | Library docs |
| 30 | **PostgreSQL** | `npx @abiswas97/postgres-mcp` | ~3 | ✅ Yes | SQL queries on localhost:5432 |
| 31 | **Supabase** | `npx @supabase/mcp-server-supabase` | ~10 | ✅ Yes | Managed DB layer |
| 32 | **Qdrant** | `python3 /usr/local/bin/qdrant-mcp-bridge.py` | ~3 | ✅ Yes | Vector search on localhost:6333 |
| 33 | **Cloudflare** | `python3 /root/.hermes/mcp_servers/cloudflare_mcp.py` | ~9 | ✅ Yes | DNS, Workers, R2, Pages |
| 34 | **Hostinger VPS** | `python3 /root/A-FORGE/.../gate.py` | 17 | ✅ Yes | VPS lifecycle (13 OBSERVE + 4 MUTATE) |
| 35 | **Capability Index** | `python3 /root/arifOS/core/capability_index/mcp_server.py` | ~2 | ✅ Yes | Tool discovery across 97 tools |
| 36 | **Repomapper** | Launcher script | ~2 | ✅ Yes | Tree-sitter + PageRank repo map |
| 37 | **Serena** | `uvx serena-agent` | ~4 | ✅ Yes | Symbol-level semantic retrieval |
| 38 | **Chrome DevTools** | `npx chrome-devtools-mcp@latest` | ~8 | ✅ Yes | Page perf, Lighthouse |

### 1.4 External / API-based MCP Servers

| # | Server | Access | Tools | Notes |
|---|--------|--------|-------|-------|
| 39 | **Tavily** | `npx tavily-mcp` | ~4 | Web search + URL extraction. TAVILY_API_KEY required |
| 40 | **Exa** | `npx exa-mcp-server` | ~4 | Semantic web search. EXA_API_KEY required |
| 41 | **Time** | `/usr/bin/mcp-server-time` | ~3 | Timezone awareness. NOP — use built-in Date() |

---

## 2. Optimal Agent Connectivity Map

### 2.1 Default Coder Agent (T0/T1 — Witness/Builder)

```
Agent MCP Config (opencode.json / .mcp.json)
│
├── MCP 1: arifOS (8088) — DIRECT
│   ├── arif_init
│   ├── arif_judge
│   ├── arif_seal
│   ├── arif_mind_reason
│   ├── arif_memory_recall
│   ├── arif_organ_attest_all
│   ├── arif_heart_critique
│   └── arif_reply_compose
│
├── MCP 2: A-FORGE (7071) — GATEWAY (proxies everything else)
│   ├── forge_run / forge_plan / forge_pipeline
│   ├── forge_dry_run / forge_approve
│   ├── GEOX proxy → geox_query_intake, basin_profile, prospect_evaluate
│   ├── WEALTH proxy → wealth_conservation, wealth_flow, wealth_stock
│   ├── WELL proxy → well_assess_homeostasis, well_validate_vitality
│   ├── Postgres proxy → schema read, query
│   ├── Supabase proxy → managed DB
│   ├── Qdrant proxy → vector search
│   ├── Brave Search proxy → web
│   ├── Perplexity proxy → AI research
│   ├── Meyhem proxy → MCP discovery
│   ├── Playwright proxy → browser
│   ├── Docker proxy → containers
│   ├── GitHub proxy → repos, PRs, issues
│   ├── Cloudflare proxy → DNS, Workers
│   ├── Context7 proxy → library docs
│   ├── Hostinger VPS proxy → VPS ops (F13-filtered)
│   ├── Capability Index proxy → tool discovery
│   ├── Repomapper/Serena proxy → code search
│   └── ... all through ONE MCP connection
│
└── Total: 2 MCPs
```

### 2.2 Controller Agent (T2 — Operator/Architect)

```
Agent MCP Config
│
├── MCP 1: arifOS (8088) — DIRECT (same as default)
├── MCP 2: A-FORGE (7071) — GATEWAY (same as default)
├── MCP 3: AAA (3001) — OPTIONAL DIRECT
│   ├── Agent discovery → list/find agents
│   ├── A2A routing → delegate tasks to other agents
│   ├── Workspace orchestration → manage sessions
│   └── Federation meta-ops
│
└── Total: 2-3 MCPs
```

### 2.3 Specialised Agent (Heavy Compute — Geoscientist/Analyst)

For agents that need full organ throughput (not recommended for general-purpose):

```
Agent MCP Config
│
├── MCP 1: arifOS (8088) — DIRECT
├── MCP 2: A-FORGE (7071) — GATEWAY (for lightweight ops)
├── MCP 3: GEOX (8081) — DIRECT (for heavy basin/prospect compute)
├── MCP 4: WEALTH (18082) — DIRECT (for large EMV/portfolio models)
├── MCP 5: WELL (18083) — DIRECT (for detailed readiness analyses)
│
└── Total: 3-5 MCPs — only for specialist agent roles
```

---

## 3. Agent-Specific Current vs Optimal

| Agent | Current MCPs | Optimal MCPs | Reduction |
|-------|-------------|--------------|-----------|
| **OpenCode (FORGE)** | 18 | 2-3 | **83-89%** |
| **Claude Code** | 9 | 2-3 | **67-78%** |
| **GitHub Copilot** | 9 | 2-3 | **67-78%** |
| **Kimi** | 10 | 2-3 | **70-80%** |
| **Gemini** | 14 | 2-3 | **79-86%** |
| **Codex** | 8 | 2-3 | **63-75%** |
| **Claude Desktop (AAA)** | 2 | 2 | **0% (already optimal)** |
| **Cursor** | 2 | 2 | **0% (already optimal)** |

---

## 4. Port Map

| Port | Service | Status |
|------|---------|--------|
| 3001 | AAA a2a (control plane) | ✅ Active |
| 3002 | APEX (legacy judge) | ✅ Active |
| 5001 | Vault999 Writer | ✅ Active |
| 5002 | F13 Witness Bridge | ✅ Active |
| 7071 | **A-FORGE** (execution gateway) | ✅ Active |
| 8000 | Graphiti / FalkorDB | ✅ Active |
| 8001 | L5 Search API | ✅ Active |
| 8081 | **GEOX** (earth intelligence) | ✅ Active |
| 8088 | **arifOS** (constitutional kernel) | ✅ Active |
| 8091 | arifOS MCP Gateway | ✅ Active |
| 8100 | Vault999 API | ✅ Active |
| 8931 | Playwright (browser automation) | ✅ Active |
| 18001 | Hermes A2A Bridge | ✅ Active |
| 18081 | arifosd (daemon) | ✅ Active |
| 18082 | **WEALTH** (capital intelligence) | ✅ Active |
| 18083 | **WELL** (human readiness) | ✅ Active |
| 18090 | MiniMax Media | ✅ Active |
| 18091 | MiniMax Code | ✅ Active |
| 18789 | OpenClaw Gateway | ✅ Active |
| 18795 | CN Organ | ✅ Active |
| 29998 | Docker MCP | ✅ Active |
| 51001 | Sequential Thinking | ✅ Active |
| 51002 | Cognitive Memory | ✅ Active |

---

## 5. Transportation Matrix

| From | To | Protocol | Notes |
|------|-----|----------|-------|
| Any agent | arifOS (8088) | Streamable HTTP | MCP initialize/initialized. Direct only |
| Any agent | A-FORGE (7071) | Streamable HTTP | MCP gateway. Single operational surface |
| Any agent | AAA (3001) | HTTP/A2A | Control plane. Optional direct |
| A-FORGE | GEOX (8081) | Streamable HTTP | Proxy for lightweight queries |
| A-FORGE | WEALTH (18082) | Streamable HTTP | Proxy for lightweight queries |
| A-FORGE | WELL (18083) | Streamable HTTP | Proxy for lightweight queries |
| A-FORGE | Postgres (5432) | SQL | Read-only by default |
| A-FORGE | Docker (socket) | HTTP | Container lifecycle |
| A-FORGE | All stdio servers | Spawn/stdio | Managed child processes |

---

## 6. Constitutional Rules

1. **arifOS is never proxied.** `arif_judge`, `arif_seal`, `arif_init` must always come from the kernel itself, not a proxy. (F9 ANTI-HANTU, F8 LAW)

2. **A-FORGE is the default operational surface.** All infra tools (GEOX/WEALTH/WELL proxies, Docker, Postgres, Qdrant, Playwright, etc.) connect through A-FORGE by default. Direct connections are the exception for heavy compute only. (F4 CLARITY)

3. **AAA is control-plane only.** Only T2 (Operator/Architect) agents need direct AAA access. T0/T1 agents use A-FORGE for all needs. (F8 LAW)

4. **Heavy compute exceptions.** GEOX (basin models, seismic), WEALTH (large EMV/portfolio), and WELL (long analyses) may be connected directly by specialist agents. Default remains proxied. (F2 TRUTH — performance is truth)

5. **Every agent carries arifOS + A-FORGE.** No agent should have fewer than these two. Removal of arifOS breaks constitutional access. Removal of A-FORGE breaks operational surface. (F1 AMANAH, F13 SOVEREIGN)

---

**SEALED — DITEMPA BUKAN DIBERI**

*Update only via ratified plan. Human sovereign (F13) remains final authority.*
