# waw — The Soul Surface

> **DITEMPA BUKAN DIBERI** — *Intelligence is forged, not given*
>
> **NAME:** 1AGI | **ROLE:** SOUL (Surface) | **STATUS:** OPERATIONAL

---

## What Is waw?

**waw** is the **human-facing surface** of the arifOS ecosystem — the SOUL in the Trinity Model (ΔΩΨ). It is a React-based web application that hosts **1AGI**, an autonomous AI agent.

This is NOT a profile page. It is a **working AI agent surface** with:
- React 19 + TypeScript + Vite frontend
- OpenClaw integration
- arifOS MCP kernel connection
- 10+ AI skills
- A2A Agent Card for agent discovery

---

## 🔗 The Trinity

| Ring | Repository | Role | Purpose |
|------|------------|------|---------|
| **Δ (Soul)** | [waw](https://github.com/ariffazil/waw) (1AGI) | **This repo** | Surface, identity, interaction |
| **Ω (Mind)** | [arifOS](https://github.com/ariffazil/arifOS) | **Kernel** | 13 floors, governance, theory |
| **Ψ (Body)** | arifosmcp.arif-fazil.com | **Execution** | MCP server, tools |

```
User → waw (React App) → arifOS MCP → Tool Execution
                    ↓
              1AGI Agent
```

---

## 🧠 What Is 1AGI?

1AGI is the autonomous AI agent that lives in this repo.

| Field | Value |
|-------|-------|
| **Name** | 1AGI |
| **Type** | Autonomous AI Agent |
| **Platform** | OpenClaw Gateway |
| **Kernel** | arifOS MCP |
| **Vibe** | Sharp, direct, getting shit done |

### Constitutional Context

1AGI operates under **13 constitutional floors** via arifOS:
- F1 AMANAH — Reversibility
- F2 TRUTH — Anti-hallucination
- F3 TRI_WITNESS — Consensus (W³ ≥ 0.95)
- F4 CLARITY — Entropy reduction
- F5 PEACE² — Non-destruction
- F6 EMPATHY — RASA listening
- F7 HUMILITY — Uncertainty bounds (Ω ∈ [0.03, 0.05])
- F8 GENIUS — Coherence (G ≥ 0.80)
- F9 ETHICS — Anti-dark-patterns
- F10 CONSCIENCE — No false claims
- F11 AUDITABILITY — Transparent logs
- F12 RESILIENCE — Graceful failure
- F13 SOVEREIGN — Human veto

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 19 + TypeScript + Vite |
| **Styling** | Tailwind CSS |
| **AI Gateway** | OpenClaw |
| **Kernel** | arifOS MCP Server |
| **Deployment** | Docker, Railway |

---

## 📂 Repository Structure

```
waw/
├── README.md                    # This file
├── AGENTS.md                    # AI agent rules
├── SOUL.md                      # 1AGI persona
├── USER.md                      # About the human (Arif)
├── IDENTITY.md                  # 1AGI identity
├── MEMORY.md                    # Agent memory
├── HEARTBEAT.md                # Periodic tasks
│
├── .well-known/
│   └── agent.json              # A2A Agent Card
│
├── arifOS/                      # Submodule: arifOS kernel
│   ├── core/
│   └── AGENTS/
│
├── skills/                      # Available AI skills
│   ├── apex-quantum-analysis/
│   ├── claude-code/
│   ├── csv-analyzer/
│   ├── deepresearchwork/
│   ├── github-pro/
│   ├── markdown-formatter/
│   ├── secops-by-joes/
│   ├── slk/
│   ├── web-scraper/
│   └── workflow-automation/
│
├── src/                         # React application
│   ├── App.tsx
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   └── main.tsx
│
├── public/                      # Static assets
├── package.json                  # Dependencies
└── Dockerfile                    # Container
```

---

## 🤖 Available Skills

1AGI has access to these skills:

| Skill | Description |
|-------|-------------|
| `apex-quantum-analysis` | Quantum analysis tools |
| `claude-code` | Claude Code integration |
| `csv-analyzer` | CSV data analysis |
| `deepresearchwork` | Deep research |
| `github-pro` | GitHub operations |
| `markdown-formatter` | MD formatting |
| `secops-by-joes` | Security operations |
| `slk` | Slack integration |
| `web-scraper` | Web scraping |
| `workflow-automation` | Workflow automation |

---

## 🔗 Live Services

| Service | URL | Purpose |
|---------|-----|---------|
| **MCP Server** | https://arifosmcp.arif-fazil.com/mcp | Kernel API |
| **Health** | https://arifosmcp.arif-fazil.com/health | Status |
| **arifOS Docs** | https://arifos.arif-fazil.com | Documentation |
| **Personal** | https://arif-fazil.com | Author |

---

## 🚀 Quick Start

### Connect to arifOS MCP

```json
{
  "mcpServers": {
    "arifos": {
      "url": "https://arifosmcp.arif-fazil.com/mcp"
    }
  }
}
```

### Health Check

```bash
curl -s https://arifosmcp.arif-fazil.com/health
```

---

## 📜 Agent Rules (from AGENTS.md)

All agents MUST follow these rules:

1. **DRY_RUN** — Label outputs as "Estimate Only / Simulated"
2. **DOMAIN_GATE** — Cannot compute? Return exact phrase
3. **VERDICT_SCOPE** — Only DOMAIN_SEAL authorizes factual claims
4. **ANCHOR_VOID** — init_anchor returns void → session BLOCKED

---

## 📊 Current Status

| Metric | Value |
|--------|-------|
| **Status** | OPERATIONAL |
| **Platform** | OpenClaw |
| **Kernel** | arifOS MCP 2026.03.25 |
| **Tools** | 40 |
| **Skills** | 10+ |
| **Constitutional Floors** | 13 Active |

---

## 🤖 A2A Agent Card

```json
{
  "name": "1AGI",
  "description": "Autonomous AI agent - The Soul of arifOS. Built on OpenClaw with arifOS constitutional kernel.",
  "version": "1.0.0",
  "url": "https://github.com/ariffazil/waw",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransition": true
  },
  "skills": [
    "apex-quantum-analysis",
    "claude-code", 
    "csv-analyzer",
    "deepresearchwork",
    "github-pro",
    "markdown-formatter",
    "web-scraper",
    "workflow-automation"
  ],
  "channels": [
    { "type": "telegram", "chatUrl": "https://t.me/ariffazil_bot" },
    { "type": "discord" },
    { "type": "whatsapp" }
  ]
}
```

---

## 👤 The Human

**Muhammad Arif bin Fazil** — Senior Exploration Geoscientist @ PETRONAS, Architect of arifOS

- Telegram: @ariffazil
- LinkedIn: ariffazil
- Website: https://arif-fazil.com

---

## 📜 License

| Component | License |
|-----------|---------|
| **Code** | AGPL-3.0 |
| **Theory** | CC0 (Public Domain) |
| **Trademark** | Proprietary |

---

## 🔗 Related Repositories

| Repo | Purpose |
|------|---------|
| [waw](https://github.com/ariffazil/waw) | This repo — THE SOUL |
| [arifOS](https://github.com/ariffazil/arifOS) | THE MIND — Kernel |
| [arifOS](https://github.com/ariffazil/arifOS) | THE BODY — MCP |
| [1AGI](https://github.com/ariffazil/1AGI) | Agent Workspace |

---

**Last Updated:** 2026-04-01  
**Status:** SEALED

*Ditempa Bukan Diberi* — Forged, Not Given [ΔΩΨ | ARIF]
