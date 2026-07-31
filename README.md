<!-- SOT-MANIFEST
federation_release: v2026.07.31
last_verified: 2026-07-31T03:25:00Z
live_commit: 6f9b2ef
truth_rule: /health + agent registry beat any static count in prose
a2a_port: 3001
a2a_status: healthy GREEN (deployment_drift: false)
vault: CONNECTED
seal_chain: append-only (chattr +a) + Merkle anchor every 100 receipts
qqq_version: v1.1.1 (10/10 tests pass)
protocol: A2A v1.0.0
gateway: Express 5.2.1 (a2a-server + a2a-gateway)
godel_lock: ACTIVE federation-wide
agent_lanes: 4 (333-AGI, 555-ASI, 888-APEX, 777-forge)
forge_instruments: 11 (grok-build, opencode, claude-code, qwen-code, antigravity, codex, copilot, aider, kimi-code, continue-cli, gemini-cli)
domain_organs: 6 (arifOS:8088, A-FORGE:7071, GEOX:8081, WEALTH:18082, WELL:18083, AAA:3001)
-->

# 🏛️ AAA — Agentic Intelligence Institution, A2A Control Plane & Federation Cockpit

[![Agentic CI](https://github.com/ariffazil/AAA/actions/workflows/agentic-ci.yml/badge.svg?branch=main)](https://github.com/ariffazil/AAA/actions)
[![Governance Plane](https://github.com/ariffazil/AAA/actions/workflows/aaa-governance.yml/badge.svg?branch=main)](https://github.com/ariffazil/AAA/actions)
[![🖥️ COCKPIT](https://img.shields.io/badge/%F0%9F%96%A5%EF%B8%8F%20INSTITUTION-A2A%20Mesh%20Gateway-0a7b83)](https://aaa.arif-fazil.com)
[![Federation](https://img.shields.io/badge/Federation-v2026.07.31-0a7b83)](https://arifos.arif-fazil.com)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](./LICENSE)

**AAA (Alignment, Authority, Accountability)** is the **Agentic Intelligence Institution** and A2A (Agent-to-Agent) Mesh Gateway of the arifOS Federation. AAA functions as the institutional state, agent registry, task router, and operator cockpit—connecting autonomous agents, forge tools, and human operators under a unified protocol.

---

## 🧬 Conceptual Framework: Agent vs. Skill vs. Tool vs. Organ

To eliminate ambiguity across autonomous agent systems, AAA enforces strict formal definitions for intelligence entities:

```
+-------------------------------------------------------------------------+
|                               AGENTS                                    |
| (Autonomous Citizens with Identity, Authority Ceiling & Intent State)  |
|  Examples: 333-AGI, 555-ASI, 888-APEX, opencode (FI-001)                |
+------------------------------------+------------------------------------+
                                     |
                                 Executes
                                     |
                                     v
+-------------------------------------------------------------------------+
|                                SKILLS                                   |
| (Domain Knowledge Workflows, Heuristics & Epistemic Procedures)         |
|  Examples: FORGE-infra-guardian, AGI-explorer-intelligence              |
+------------------------------------+------------------------------------+
                                     |
                                  Invokes
                                     |
                                     v
+------------------------------------+------------------------------------+
|                                TOOLS                                    |
| (Deterministic Execution Primitives exposed via MCP or Shell)           |
|  Examples: arif_observe, geox_petrophysics, git_commit                  |
+------------------------------------+------------------------------------+
                                     |
                                Hosted On
                                     |
                                     v
+-------------------------------------------------------------------------+
|                                ORGANS                                   |
| (Microservice Hardware/Software Infrastructure Bounds)                  |
|  Examples: arifOS (:8088), A-FORGE (:7071), GEOX (:8081), AAA (:3001)   |
+-------------------------------------------------------------------------+
```

| Entity | Definition | Primary Characteristic | Example |
|:---|:---|:---|:---|
| **Agent** | Autonomous entity with state, identity, & authority boundary | Pursues goals, holds memory, incurs accountability | `333-AGI`, `opencode (FI-001)` |
| **Skill** | Structured procedure or domain reasoning playbook | Declarative instructions (`SKILL.md`), guidance | `AGI-explorer-intelligence` |
| **Tool** | Stateless function or API execution capability | Atomic action, input-output transformation | `geox_petrophysics()`, `arif_think()` |
| **Organ** | Server/system microservice hosting tools & models | Systemd daemon, network port boundary | `GEOX (:8081)`, `WEALTH (:18082)` |

---

## 🌐 Protocol Contrast: A2A Mesh vs. MCP Surface

The arifOS Federation separates inter-agent communication (A2A) from agent-to-tool invocation (MCP):

```
+-------------------------------------------------------------------------+
|                        A2A (Agent-to-Agent Mesh)                        |
| - Protocol: Asynchronous JSON-RPC / Agent Cards / Task Delegation       |
| - Layer: Peer-to-Peer / Multi-Agent Collaboration                      |
| - Hub: AAA Gateway (Port 3001)                                          |
+------------------------------------+------------------------------------+
                                     |
                        Delegates Tasks To Organs
                                     |
                                     v
+-------------------------------------------------------------------------+
|                     MCP (Model Context Protocol)                        |
| - Protocol: Synchronous JSON-RPC 2.0 / FastMCP Transport                |
| - Layer: Agent-to-Tool & System Interoperability                        |
| - Hub: arifOS Governance Kernel (Port 8088)                             |
+-------------------------------------------------------------------------+
```

| Dimension | A2A Mesh Protocol (AAA Gateway) | MCP Surface (arifOS Kernel) |
|:---|:---|:---|
| **Primary Focus** | Inter-agent coordination, task delegation, card registry | Tool exposure, hardware execution, resource reading |
| **Participant** | Agent $\leftrightarrow$ Agent (e.g. `333-AGI` $\to$ `555-ASI`) | Agent $\leftrightarrow$ Tool/Engine (e.g. Agent $\to$ `GEOX`) |
| **State & Lifecycle**| Persistent AREP tasks, long-running agent threads | Synchronous request-response tool invocations |
| **Governance Role**| Task routing, role capability mapping, agent registry | Constitutional floor checking (F1–F13) & `888_HOLD` gates |

---

## 🏛️ Federation Separation of Powers

AAA enforces strict separation of responsibilities across the federation:

| Layer | Organ / Actor | Authority & Capability | Boundary ("Must Never") |
|:---|:---|:---|:---|
| **Sovereign** | **ARIF (F13)** | Absolute Veto, final decision, policy ratification | Be overridden by algorithms |
| **Institution** | **AAA (:3001)** | Agent registration, A2A task routing, Cockpit UI | Self-issue verdicts or execute code |
| **Kernel** | **arifOS (:8088)** | Constitutional adjudication (`SEAL`, `HOLD`, `VOID`) | Execute code mutations directly |
| **Executor** | **A-FORGE (:7071)**| Systems engineering, CI/CD, deployment execution | Self-authorize mutations without SEAL |
| **Witnesses** | **GEOX / WEALTH / WELL** | Earth, capital, & human evidence calculation | Make sovereign decisions |
| **Ledger** | **VAULT999** | Cryptographic append-only proof store | Edit or erase historical receipts |

---

## 🛰️ Live Operator Cockpit & Deployment Topology

AAA provides an enterprise-grade React 19 + Vite 8 cockpit displaying real-time federation health, agent status, and pending `888_HOLD` decisions.

```
Public A2A Gateway: https://aaa.arif-fazil.com
Local Gateway:      http://127.0.0.1:3001
Agent Card Index:   https://aaa.arif-fazil.com/.well-known/agent-card.json
```

### Production Service Operations

```bash
# 1. Inspect AAA Gateway Health & Drift Status
curl -s http://127.0.0.1:3001/health | jq .

# 2. Rebuild & Restart AAA Service (T2 Operation)
cd /root/AAA
npm run build
rsync -a --exclude='.git' --exclude='node_modules' /root/AAA/ /opt/aaa/app/
systemctl restart aaa-a2a

# 3. Validate A2A Conformance Suite
npm run a2a:conformance
```

---

## 🔗 Federation Architecture & Navigation

AAA operates as the Agentic Intelligence Institution, Control Plane, and A2A Mesh Gateway for the **arifOS Federation**. Every organ maintains distinct boundaries and capabilities:

| Organ | Domain Role | Port | Repo | Live MCP | Health Witness | Machine Spec |
|:---|:---|:---:|:---|:---|:---|:---|
| **arifOS** | Constitutional Kernel & Judge | 8088 | [repo](https://github.com/ariffazil/arifos) | [mcp](https://mcp.arif-fazil.com/mcp) | [health](https://arifos.arif-fazil.com/health) | [llms.txt](https://arifos.arif-fazil.com/llms.txt) |
| **A-FORGE** | Governed Execution Engine | 7071 / 7072 | [repo](https://github.com/ariffazil/A-FORGE) | [mcp](https://forge.arif-fazil.com/mcp) | [health](https://forge.arif-fazil.com/health) | [llms.txt](https://forge.arif-fazil.com/llms.txt) |
| **AAA** | Institution, Control Plane & A2A | 3001 | [repo](https://github.com/ariffazil/AAA) | — | [health](https://aaa.arif-fazil.com/health) | [llms.txt](https://aaa.arif-fazil.com/llms.txt) |
| **GEOX** | Earth Intelligence (Subsurface) | 8081 | [repo](https://github.com/ariffazil/GEOX) | [mcp](https://geox.arif-fazil.com/mcp) | [health](https://geox.arif-fazil.com/health) | [llms.txt](https://geox.arif-fazil.com/llms.txt) |
| **WEALTH** | Capital Intelligence (Compute) | 18082 | [repo](https://github.com/ariffazil/WEALTH) | [mcp](https://wealth.arif-fazil.com/mcp) | [health](https://wealth.arif-fazil.com/health) | [llms.txt](https://wealth.arif-fazil.com/llms.txt) |
| **WELL** | Vitality & Readiness Guard | 18083 | [repo](https://github.com/ariffazil/WELL) | [mcp](https://well.arif-fazil.com/mcp) | [health](https://well.arif-fazil.com/health) | [llms.txt](https://well.arif-fazil.com/llms.txt) |
| **HERMES** | Multi-Modal Bridge & Telegram Relay | 8644 | [repo](https://github.com/ariffazil/HERMES) | — | — | — |

**Public Domain:** [arif-fazil.com](https://arif-fazil.com) · **Federation Root:** [arifos.arif-fazil.com](https://arifos.arif-fazil.com)

---

## 📜 Sovereignty & License

- **License:** GNU Affero General Public License v3.0 (**AGPL-3.0**). The institutional control plane must remain open and transparent.
- **Sovereign Authority:** **Muhammad Arif bin Fazil** (F13 SOVEREIGN). AAA is the institutional window for sovereign oversight.

---

*DITEMPA BUKAN DIBERI — The state is forged, not given.*  
*Maruah without SEAL is sentiment. SEAL without Maruah is enforcement. 999 SEAL ALIVE.*

(https://aaa.arif-fazil.com/health) | [llms.txt](https://aaa.arif-fazil.com/llms.txt) |
| **GEOX** | Earth intelligence | [repo](https://github.com/ariffazil/GEOX) | [mcp](https://geox.arif-fazil.com/mcp) | [health](https://geox.arif-fazil.com/health) | [llms.txt](https://geox.arif-fazil.com/llms.txt) |
| **WEALTH** | Capital intelligence | [repo](https://github.com/ariffazil/WEALTH) | [mcp](https://wealth.arif-fazil.com/mcp) | [health](https://wealth.arif-fazil.com/health) | [llms.txt](https://wealth.arif-fazil.com/llms.txt) |
| **WELL** | Vitality guard | [repo](https://github.com/ariffazil/WELL) | [mcp](https://well.arif-fazil.com/mcp) | [health](https://well.arif-fazil.com/health) | [llms.txt](https://well.arif-fazil.com/llms.txt) |
| **HERMES** | Multi-modal bridge | [repo](https://github.com/ariffazil/HERMES) | — | — | — |

**Public:** [arif-fazil.com](https://arif-fazil.com) · **Federation root:** [arifos.arif-fazil.com](https://arifos.arif-fazil.com)
**SOT:** 2026-07-28


    │                                                  │
    │   AAA is the state.                             │
    │   arifOS is the judge.                          │
    │   A-FORGE is the executor.                      │
    │   The organs are the witnesses.                 │
    │   The cockpit is the window.                    │
    │   Arif is the sovereign.                        │
    │                                                  │
    │   The window is not the wall.                   │
    │   The state is not the constitution.            │
    │   The display is not the verdict.               │
    │   The route is not the action.                  │
    │   The queue is not the seal.                    │
    │   The registry is not the law.                  │
    │                                                  │
    │   Maruah without SEAL is sentiment.             │
    │   SEAL without Maruah is enforcement.           │
    │                                                  │
    │   DITEMPA BUKAN DIBERI                         │
    │   The state is forged, not given.               │
    │   999 SEAL ALIVE.                               │
    │                                                  │
    └──────────────────────────────────────────────────┘
```
