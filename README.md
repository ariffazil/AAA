# AAA — Arif Agent Architecture

> **Identity. Control. Federation.**
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

[![AAA](https://img.shields.io/badge/AAA-v1.0.0-FF3366?style=flat-square)](https://github.com/ariffazil/AAA)
[![arifOS](https://img.shields.io/badge/arifOS-F1%E2%80%93F13_Governed-FF6B00?style=flat-square)](https://github.com/ariffazil/arifOS)
[![A2A](https://img.shields.io/badge/A2A-v1.0.0-00D4FF?style=flat-square)](https://github.com/ariffazil/AAA)
[![License](https://img.shields.io/badge/License-AGPL_V3-4EAF0C?style=flat-square)](./LICENSE)

---

## What AAA Is

AAA is the **sovereign identity layer, control plane, and A2A federation gateway** for the arifOS constitutional kernel. It exposes governed delegation and coordination surfaces to external agents via the A2A v1.0.0 protocol, while arifOS provides the constitutional Floors F1–F13 that constrain all operations.

AAA does not adjudicate. It **identifies, authenticates, and routes**. The constitutional verdict belongs to arifOS.

---

## Position in the arifOS Trinity

```
External Agent (A2A v1.0.0)
    ↓ POST /tasks
AAA Gateway (a2a-server/)
    ├── 888_JUDGE gate (hold skills require constitutional verdict)
    ├── F9 Anti-Hallucination check
    ├── VAULT999 audit
    └── arifOS Constitutional Floors F1–F13
         ↓
    Peer Agent (arifOS / GEOX / WEALTH / A-FORGE)
    
YOU ARE HERE ──────────────────────────────── ↑
```

AAA sits at the **federation boundary** — it is the front door and the gatekeeper.

---

## Current Source of Truth

| Field | Value |
|-------|-------|
| Canonical repository | `https://github.com/ariffazil/AAA` |
| Package version | `1.0.0` |
| Governing kernel | `arifOS F1–F13` |
| Protocol | A2A v1.0.0 |
| Endpoint | `http://localhost:3001` |
| Gateway | `a2a-server/server.js` |
| Federation manifest | `/.well-known/arifos-federation.json` |
| Primary agent | **OPENCLAW** (AGI-level gateway) |
| Agent tier framework | 000–999 governed loop + L0–L5 autonomy ladder |
| Governance files | AGENTS.md, SOUL.md, LOOP.md, AUTONOMY.md, HEARTBEAT.md, CHECKPOINT.md, DECISIONS.md, TASKS.md |

---

## A2A v1.0.0 Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/.well-known/agent-card.json` | A2A v1.0.0 agent card |
| `GET` | `/.well-known/arifos-federation.json` | Federation peer manifest |
| `GET` | `/health` | Health + vault status |
| `POST` | `/tasks` | Create task (888_JUDGE gate) |
| `GET` | `/tasks/:taskId` | Get task by ID |
| `GET` | `/tasks/:taskId/stream` | SSE task stream |
| `POST` | `/tasks/:taskId/cancel` | Cancel task |
| `GET` | `/tasks/:taskId/subscribe` | SSE task subscription |

---

## Agent Tier Architecture

**Two intelligence tiers govern the federation:**

| Tier | Agents | Definition |
|------|--------|------------|
| **AGI** | OPENCLAW, maxhermes, opencode, hermes-ops | Bounded, self-monitoring operator — governed tool use + 000-999 loop |
| **ASI** | hermes-asi, hermes | Advanced Specialist Intelligence — generalist reasoning, deep memory, routing |

### Agent Registry

| Agent | Tier | Role |
|-------|------|------|
| **OPENCLAW** | AGI | Primary gateway + orchestrator (this agent) |
| **hermes-asi** | ASI | Generalist reasoning + routing + coordination |
| **hermes** | ASI | Memory engine + deep recall |
| **maxhermes** | AGI | GEOX Earth Intelligence specialist |
| **opencode** | AGI | Coding specialist |
| **hermes-ops** | AGI | Execution specialist (DevOps + workflows) |

---

## Federation Peers

AAA registers and coordinates with these peer agents:

| Agent | Role | Protocol | Tier |
|-------|------|---------|------|
| **arifOS** | Constitutional kernel | MCP | Constitutional |
| **GEOX** | Earth intelligence | MCP | AGI |
| **WEALTH** | Capital intelligence | MCP | AGI |
| **OPENCLAW** | Gateway + orchestrator | A2A | AGI |
| **hermes-asi** | Generalist reasoning | A2A | ASI |
| **hermes** | Memory engine | A2A | ASI |
| **MaxHermes** | GEOX specialist | A2A | AGI |
| **A-FORGE** | Execution shell | Internal | AGI |

---

## Constitutional Posture

AAA operates under arifOS constitutional Floors F1–F13:

- **No silent self-approval** — every skill route requires constitutional check
- **No irreversible action without human acknowledgment**
- **No bypass of VAULT999 audit trail**
- **888_JUDGE gate** enforced before `agent-dispatch` and `agent-handoff`

---

## Architecture

```
External Agent (A2A v1.0.0)
    ↓ POST /tasks
OPENCLAW Gateway (AAA / a2a-server/)
    ├── 888_JUDGE gate (hold skills require constitutional verdict)
    ├── F9 Anti-Hallucination check
    ├── VAULT999 audit
    └── arifOS Constitutional Floors F1–F13
         ↓
    Peer Agent Dispatch (hermes-asi / hermes / maxhermes / opencode / hermes-ops)
         ↓
    GEOX / WEALTH / A-FORGE
```

---

## Sibling Organ READMEs

| Organ | One-liner |
|-------|----------|
| [`arifOS`](https://github.com/ariffazil/arifOS) | Constitutional kernel — F1–F13 floors, 13 tools, VAULT999 |
| [`A-FORGE`](https://github.com/ariffazil/A-FORGE) | Execution shell, orchestration, and operator observability |
| [`GEOX`](https://github.com/ariffazil/geox) | Governed earth intelligence — seismic, petrophysics, basin analysis |
| [`WEALTH`](https://github.com/ariffazil/wealth) | Capital intelligence — NPV, IRR, EMV, crisis triage |
| [`WELL`](https://github.com/ariffazil/well) | Biological substrate governance — human readiness mirroring |

---

## The Trinity (ΔΩΨ) & Live Surfaces

AAA sits at the federation boundary, fulfilling the **BODY (Ψ)** role alongside A-FORGE, while arifOS serves as the **MIND (Ω)** and the human sovereign as the **SOUL (Δ)**.

| Surface | Role | URL |
|---------|------|-----|
| **Human** | SOUL (Δ) | `https://arif-fazil.com/` |
| **arifOS** | MIND (Ω) | `https://arifos.arif-fazil.com/` |
| **AAA / A-FORGE** | BODY (Ψ) | `https://aaa.arif-fazil.com/` |
| **MCP Canonical** | BODY (Ψ) | `https://mcp.arif-fazil.com/` |
| **GEOX** | Earth | `https://geox.arif-fazil.com/` |

> **Note:** `arifosmcp.arif-fazil.com` is a legacy 301 redirect to the canonical `mcp.arif-fazil.com` endpoint.

*AAA identifies. arifOS adjudicates. The federation is forged through disciplined coordination.*
*DITEMPA BUKAN DIBERI — Identity is forged through constitutional discipline.*
