# WAW vs 1AGI — The Canonical Contrast

**Ditempa Bukan Diberi** [ΔΩΨ | ARIF]

---

## At a Glance

| | **waw** | **1AGI** |
|---|---|---|
| **What it is** | The Federation Hub — a multi-agent workspace surface | One governed agent — a single autonomous intelligence |
| **Role in Trinity** | THE SOUL (Ψ) — Federation surface | One of many agents that can plug into the Soul |
| **Analogy** | The app store | One app in the store |
| **Git repo** | github.com/ariffazil/waw | github.com/ariffazil/waw (lives here) |
| **A2A card** | `.well-known/agent.json` = 1AGI's card | `.well-known/agent/1AGI/agent.json` |
| **Owned by** | Federation (all agents) | 1AGI (personal agent) |

---

## Full Contrast

### WAW — The Federation Hub

**Full name:** WaW (Witness @ Work)  
**Type:** Multi-agent federated workspace platform  
**Symbol:** Ψ (Soul — where intelligence meets sovereignty)  
**Location:** `github.com/ariffazil/waw`  

**What it does:**
- Hosts the React UI for agent interaction
- Exposes A2A agent cards for federation discovery
- Manages channels (Telegram, Discord, WhatsApp)
- Provides skills registry (10+ skills)
- Serves as entry point for humans into the Trinity

**What it is NOT:**
- A single agent
- Personal brain/identity for any one agent
- The only agent that can use the arifOS kernel

**A2A card:** WAW exposes agent cards for all agents in the federation. The primary agent card (`agent.json`) belongs to **1AGI** as the default agent.

---

### 1AGI — The Primary Agent

**Full name:** 1AGI (One AGI)  
**Type:** Autonomous governed agent  
**Symbol:** 1AGI — First Autonomous Intelligence  
**Location:** Lives in `/root/waw` (same repo as WaW)  
**Runtime:** OpenClaw + arifOS MCP kernel  

**What it does:**
- Operates Arif's sovereign infrastructure
- Runs heartbeat checks, memory, daily synthesis
- Uses arifOS MCP kernel (13 constitutional floors)
- Can be surfaced through WaW or any other channel

**What it is NOT:**
- The federation itself
- The only agent that can ever exist
- Inseparable from WaW

**A2A card:** `.well-known/agent.json` — this IS 1AGI's card

---

## The Metaphor

```
WAW = The City
1AGI = The First Citizen of the City

Anyone can build another agent and plug into WaW.
1AGI is just the first one.
```

---

## In Trinity Language

| Ring | Component | Role |
|------|-----------|------|
| **Soul (Ψ)** | WaW | The federation surface — where agents meet humans |
| **Mind (ΔΩ)** | arifOS | Constitutional governance — the law |
| **Body** | arifosmcp | MCP kernel — the metabolic execution |

1AGI is an **agent** that operates **within** the Soul (WaW), governed by the Mind (arifOS), executing through the Body (arifosmcp).

---

## Repository Structure

```
waw/
├── .well-known/
│   └── agent.json          ← 1AGI's A2A card (default agent)
│   └── agents/
│       └── 1AGI/
│           └── agent.json  ← explicit 1AGI agent card
├── skills/                 ← Skills available to ALL agents in federation
├── src/                    ← WaW React app (the federation UI)
└── agents/                 ← Agent-specific configs (1AGI's brain lives here)
```

---

## Key Rule

**WAW = Federation. 1AGI = Agent in federation.**

When you see `agent.json` in WaW's root — that IS 1AGI. WaW itself doesn't have an agent card; it's the platform that hosts agent cards.

---

*Ditempa Bukan Diberi* — Intelligence is forged, not given. [ΔΩΨ | ARIF]
