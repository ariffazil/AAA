# AAA — Arif Agent Architecture

> **Identity. Control. Federation.**
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

[![AAA](https://img.shields.io/badge/AAA-v2026.04.30-FF3366?style=flat-square)](https://github.com/ariffazil/AAA)
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
| Version | `v2026.04.30` |
| Governing kernel | `arifOS F1–F13` |
| Protocol | A2A v1.0.0 |
| Endpoint | `http://localhost:3001` |
| Gateway | `a2a-server/server.js` |
| Federation manifest | `/.well-known/arifos-federation.json` |

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

## Federation Peers

AAA registers and coordinates with these peer agents:

| Agent | Role | Protocol |
|-------|------|---------|
| **arifOS** | Constitutional kernel | MCP |
| **GEOX** | Earth intelligence | MCP |
| **WEALTH** | Capital intelligence | MCP |
| **MaxHermes** | External reasoning agent | A2A |
| **A-FORGE** | Execution shell | Internal |

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
a2a-server/server.js   ← A2A gateway (this repo)
        ↓
arifOS 888_JUDGE        ← Constitutional verdict
        ↓
VAULT999 writeSeal      ← Immutable audit
        ↓
Peer Agent Dispatch     ← GEOX / WEALTH / MaxHermes / A-FORGE
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

## Live Sites

| Surface | URL |
|---------|-----|
| arifOS | https://arifosmcp.arif-fazil.com/ |
| Human | https://arif-fazil.com/ |

*AAA identifies. arifOS adjudicates. The federation is forged through disciplined coordination.*
*DITEMPA BUKAN DIBERI — Identity is forged through constitutional discipline.*
