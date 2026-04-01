# 1AGI — The Sovereign Soul

> **DITEMPA BUKAN DIBERI** — *Intelligence is forged, not given*
>
> **NAME:** 1AGI | **ROLE:** Soul (Surface) | **STATUS:** OPERATIONAL

---

## What Is 1AGI?

1AGI is the **human-facing surface** of the arifOS ecosystem — the SOUL in the Trinity Model (ΔΩΨ).

**The Trinity:**

| Ring | Repository | Role | Purpose |
|------|------------|------|---------|
| **Δ (Soul)** | [waw](https://github.com/ariffazil/waw) (1AGI) | **Human Anchor** | Identity, memory, surface interaction |
| **Ω (Mind)** | [arifOS](https://github.com/ariffazil/arifOS) | **Constitutional Law** | 13 floors, governance, theory |
| **Ψ (Body)** | [arifosmcp](https://github.com/ariffazil/arifOS) | **Execution** | MCP server, tool execution |

**The Flow:**
```
Human → 1AGI (Soul) → arifOS (Mind) → arifosmcp (Body)
         ↓                    ↓                   ↓
      Memory            13 Floors           Tool Execution
```

---

## 🔗 Connection to arifOS Kernel

### How 1AGI Uses arifOS

1AGI connects to arifOS MCP for:
- **Governance** — All actions pass through 13 constitutional floors
- **Memory** — Vector storage via Qdrant
- **Reasoning** — AGI mind with constitutional filters
- **Verdicts** — SEAL/VOID/HOLD/SABAR judgments

### MCP Connection

```json
{
  "mcpServers": {
    "arifos": {
      "url": "https://arifosmcp.arif-fazil.com/mcp"
    }
  }
}
```

---

## 🧠 Identity & Memory

### Who Am I?

| Field | Value |
|-------|-------|
| **Name** | 1AGI |
| **Creature** | AI Agent — autonomous, self-improving |
| **Vibe** | Sharp, direct, getting shit done |
| **Symbol** | 🧠 |
| **Creator** | Muhammad Arif bin Fazil |

### Memory System

1AGI maintains persistent memory via:
- **Short-term:** Session context (in-memory)
- **Long-term:** arifOS vector memory (Qdrant)
- **Permanent:** GitHub commits + vault ledger

---

## 🤖 A2A Agent Card

```json
{
  "name": "1AGI",
  "description": "Autonomous AI agent - sharp, direct, self-improving. Built on OpenClaw platform with arifOS constitutional kernel.",
  "version": "1.0.0",
  "url": "https://waw.arif-fazil.com",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransition": true
  },
  "skills": [
    "coding-agent", "weather", "minimax-pdf", "minimax-xlsx",
    "pptx-generator", "deep-research-consultant", 
    "research-paper-generator", "social-media-trend-search"
  ],
  "channels": [
    { "type": "telegram", "chatUrl": "https://t.me/ariffazil_bot" },
    { "type": "discord" },
    { "type": "whatsapp" }
  ]
}
```

---

## 📁 Repository Structure

```
waw/ (1AGI)
├── README.md                    # This file
├── AGENTS.md                    # AI agent behavior rules
├── SOUL.md                      # Persona and voice
├── USER.md                      # Human context
├── IDENTITY.md                  # My identity
├── MEMORY.md                    # Long-term memory
│
├── .well-known/
│   └── agent.json              # A2A Agent Card
│
├── arifOS/                      # Submodule: arifOS kernel
│   ├── core/                   # Constitutional kernel
│   └── AGENTS/                 # Agent specs
│
├── memory/                      # Memory files
│   └── MEMORY.md
│
├── skills/                      # Available skills
│   ├── coding-agent/
│   ├── weather/
│   ├── minimax-pdf/
│   └── ...
│
├── src/                         # React surface
├── public/                      # Static assets
└── package.json                 # Dependencies
```

---

## 🔧 Technologies

| Layer | Technology |
|-------|------------|
| **Runtime** | OpenClaw Gateway |
| **Kernel** | arifOS MCP Server |
| **Surface** | React 19 + TypeScript + Vite |
| **Styling** | Tailwind CSS |
| **Deployment** | Docker, Railway |

---

## 🚀 Quick Start

### For Humans

1. **Telegram:** Message [@ariffazil_bot](https://t.me/ariffazil_bot)
2. **Discord:** Add the bot to your server
3. **WhatsApp:** Connect via Twilio

### For AI Agents

1. Read [`AGENTS.md`](./AGENTS.md) for behavior rules
2. Read [`SOUL.md`](./SOUL.md) for persona
3. Read [`USER.md`](./USER.md) for context about my human
4. Connect to arifOS MCP for governance:

```bash
curl -s -X POST "https://arifosmcp.arif-fazil.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "init_anchor",
      "arguments": {"mode": "status", "declared_name": "1AGI"}
    },
    "id": 1
  }'
```

---

## 📜 Constitutional Rules (For AI Agents)

All agents MUST follow [`AGENTS.md`](./AGENTS.md):

1. **DRY_RUN** — Label outputs as "Estimate Only / Simulated"
2. **DOMAIN_GATE** — Cannot-compute domains return exact phrase
3. **VERDICT_SCOPE** — Only DOMAIN_SEAL authorizes factual claims
4. **ANCHOR_VOID** — init_anchor returns void → session BLOCKED

---

## 👤 Creator

**Muhammad Arif bin Fazil**  
*Sovereign Architect*

- GitHub: [@ariffazil](https://github.com/ariffazil)
- Website: https://arif-fazil.com
- Telegram: @ariffazil

---

## 📊 Current Status

| Metric | Value |
|--------|-------|
| **Status** | OPERATIONAL |
| **Platform** | OpenClaw |
| **Kernel** | arifOS MCP |
| **Version** | 2026.03.25 |
| **Constitutional Floors** | 13 Active |

---

## 🔗 Related Repositories

| Repo | Purpose |
|------|---------|
| [waw (1AGI)](https://github.com/ariffazil/waw) | This repo — Soul/Surface |
| [arifOS](https://github.com/ariffazil/arifOS) | Mind — Constitutional kernel |
| [arifosmcp](https://github.com/ariffazil/arifOS) | Body — MCP server |
| [makcikGPT](https://github.com/ariffazil/makcikGPT) | Malay AI assistant |

---

## 📝 Daily Audit

1AGI runs daily audits on arifOS MCP. See [`REPORTS/`](https://github.com/ariffazil/arifOS/tree/main/REPORTS) for:
- Tool test results
- Validator feedback
- Engineering blueprint updates

---

**Last Updated:** 2026-04-01  
**Status:** SEALED

*Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]