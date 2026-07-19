# 🗺️ FEDERATION MAP — arifOS Civilization Stack

> **DITEMPA BUKAN DIBERI — Forged, Not Given.**
> **Canonical reference for all 8 repos. If any README disagrees, this file wins.**
> **Last ratified: 2026-07-19 | F13 SOVEREIGN**

---

## 1. THE STACK — 5 Layers, 9 Repos

```
┌─────────────────────────────────────────────────┐
│ L0: CANON — ariffazil/ariffazil                  │
│   APEX THEORY, identity, writings, civilization  │
├─────────────────────────────────────────────────┤
│ L1: ROOT — arifOS + AAA                          │
│   arifOS: constitutional kernel, F1-F13, 000→999 │
│   AAA:    state foundation, A2A, cockpit, seals  │
├─────────────────────────────────────────────────┤
│ L2: EXECUTIVE — A-FORGE                          │
│   Agentic forge, MCP orchestration, deployment   │
├─────────────────────────────────────────────────┤
│ L3: DOMAIN ORGANS — GEOX, WEALTH, WELL, HERMES   │
│   Specialized intelligence, evidence-only        │
├─────────────────────────────────────────────────┤
│ L4: PUBLIC SURFACE — arif-sites                  │
│   arif-fazil.com, docs, operator surfaces        │
└─────────────────────────────────────────────────┘
```

## 2. ROLE TAXONOMY

| Role | Repos | What they do | Can mutate? | Can adjudicate? |
|------|-------|-------------|-------------|-----------------|
| **CANON** | ariffazil/ariffazil | Identity, APEX THEORY, writings | Yes (own docs) | No (human only) |
| **ROOT** | arifOS, AAA | Govern, judge, seal, display state | No | arifOS: YES / AAA: No |
| **EXECUTIVE** | A-FORGE | Execute, build, deploy, orchestrate | **Yes (after SEAL)** | No |
| **DOMAIN** | GEOX, WEALTH, WELL, HERMES | Compute evidence, specialize, bridge | No | No |
| **PUBLIC** | arif-sites | Public websites, docs, discovery | Yes (content only) | No |

## 3. INTER-REPO DEPENDENCIES

```
ariffazil/ariffazil
  └─ references all repos (documentation, not code dependency)

arifOS
  ├─ AAA          ← A2A gateway, state queries
  ├─ A-FORGE      ← execution dispatch (forge_judge_proxy)
  ├─ GEOX         ← earth evidence routing
  ├─ WEALTH       ← capital evidence routing
  └─ WELL         ← vitality evidence routing

AAA
  ├─ arifOS       ← kernel API, verdicts, VAULT999
  └─ A-FORGE      ← execution state, job status

A-FORGE
  ├─ arifOS       ← SEAL verdicts, leases, governance
  ├─ AAA          ← A2A state, cockpit triggers
  ├─ GEOX         ← geoscience tools (via MCP)
  ├─ WEALTH       ← capital tools (via MCP)
  └─ WELL         ← vitality tools (via MCP)

GEOX / WEALTH / WELL / HERMES
  └─ arifOS       ← evidence routing, governance gates

arif-sites
  ├─ arifOS       ← health, discovery, llms.txt
  ├─ AAA          ← cockpit embedding
  └─ all organs   ← public surface for each
```

## 4. MCP SURFACES

| Repo | Port | Public Endpoint | Tools |
|------|------|----------------|-------|
| arifOS | 8088 | `arifos.arif-fazil.com/mcp` | 8 public: arif_init, arif_observe, arif_think, arif_route, arif_memory, arif_judge, arif_forge, arif_seal |
| A-FORGE | 7072 | `mcp.arif-fazil.com/mcp` | 80+ forge_* tools |
| GEOX | 8081 | `geox.arif-fazil.com/mcp` | 15 geox_* tools |
| WEALTH | 18082 | `wealth.arif-fazil.com/mcp` | 20+ capital_* tools |
| WELL | 18083 | `well.arif-fazil.com/mcp` | 10+ well_* tools |
| HERMES | 8644 | N/A (Telegram bridge) | Operator edge only |
| AAA | 3001 | N/A (A2A, not MCP) | Cockpit + A2A gateway |
| arif-sites | N/A | `arif-fazil.com` | Static sites, llms.txt discovery |

## 5. GOVERNANCE FLOW

```
human intent
    ↓
arifOS (000 arif_init)        ← session bootstrap
    ↓
domain organ (111 observe)    ← GEOX/WEALTH/WELL evidence
    ↓
arifOS (333 arif_think)       ← structured reasoning
    ↓
arifOS (888 arif_judge)       ← constitutional verdict
    ↓
A-FORGE (777 arif_forge)      ← governed execution
    ↓
arifOS (999 arif_seal)        ← VAULT999 immutable record
    ↓
AAA (state display)           ← cockpit reflects truth
```

## 6. FILE CONVENTIONS

Every repo MUST have:
- `README.md` — human-facing, SOT manifest, role declaration
- `FEDERATION.md` — machine-readable role + dependency declaration (see §7)
- `AGENTS.md` — AI agent instructions for that repo
- `LICENSE` — AGPL-3.0 (all federation repos)

Every repo SHOULD have:
- `.github/workflows/` — CI aligned with federation standards
- `docs/` — architecture decisions, contracts, receipts
- `Makefile` or equivalent — `make health`, `make test`, `make prove`

## 7. FEDERATION.md SPEC

Every repo's `FEDERATION.md` must declare:

```yaml
# Required fields
role: CANON | ROOT | EXECUTIVE | DOMAIN
organ: ariffazil | arifos | aaa | aforge | geox | wealth | well
layer: L0 | L1 | L2 | L3

# Required
depends_on:
  - repo: ariffazil/<name>
    reason: <why>

# If MCP server
mcp:
  port: <port>
  endpoint: <url>
  tools_count: <N>

# Required
governance:
  judge: arifOS  # always
  seal: VAULT999  # always
  floors: F1-F13  # always

# Optional
agentic_surface: true | false  # only A-FORGE
citizenship: warga-aaa  # all federation repos
```

---

*Ratified by F13 SOVEREIGN. Amended only via 888_HOLD + F13 ack.*
*DITEMPA BUKAN DIBERI — The federation is forged, not given.*
