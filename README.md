<!-- SOT-MANIFEST
federation_release: v2026.08.09
last_verified: 2026-08-14T04:50:00Z
live_commit: a091b432 (housekeeping(aaa): SOT drift fix, entropy cleanup, registry sync)
truth_rule: /health + agent registry beat any static count in prose
a2a_port: 3001
a2a_status: healthy GREEN (deployment_drift: false)
vault: CONNECTED
seal_chain: append-only (chattr +a) + Merkle anchor every 100 receipts
qqq_version: v1.1.1 (10/10 tests pass)
protocol: A2A v1.0.0
gateway: Express 5.2.1 (a2a-server + a2a-gateway)
godel_lock: ACTIVE federation-wide
agent_lanes: 4 (333-AGI, 555-ASI, 888-APEX, 777-FORGE)
forge_instruments: 11 (opencode, grok-build, claude-code, kimi-code, codex, copilot, aider, qwen-code, antigravity, continue-cli, gemini-cli)
domain_organs: 6 (arifOS:8088, A-FORGE:7071, GEOX:8081, WEALTH:18082, WELL:18083, AAA:3001)
-->

# 🏛️ AAA — Agentic Intelligence Institution & A2A Control Plane

[![Agentic CI](https://github.com/ariffazil/AAA/actions/workflows/agentic-ci.yml/badge.svg?branch=main)](https://github.com/ariffazil/AAA/actions)
[![Governance Plane](https://github.com/ariffazil/AAA/actions/workflows/aaa-governance.yml/badge.svg?branch=main)](https://github.com/ariffazil/AAA/actions)
[![🖥️ COCKPIT](https://img.shields.io/badge/%F0%9F%96%A5%EF%B8%8F%20INSTITUTION-A2A%20Mesh%20Gateway-0a7b83)](https://aaa.arif-fazil.com)
[![Federation](https://img.shields.io/badge/Federation-v2026.08.09-0a7b83)](https://arifos.arif-fazil.com)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](./LICENSE)

> **AAA is the institution. It routes and displays. It never judges.**
> **DITEMPA BUKAN DIBERI — The state is forged, not given.**

**AAA (Alignment, Authority, Accountability)** is the institutional control plane of the arifOS Federation. It operates the A2A (Agent-to-Agent) Mesh Gateway, the agent identity registry, the task router, and the operator cockpit — connecting **11 forge instruments**, **6 domain organs**, and the sovereign human operator under a unified protocol.

---


## Institutional density (2026-08-09)

Hermes / federation are evolving as **anti-chaos infrastructure**, not agent thrash.

| Doc | Role |
|-----|------|
| `governance/HOLY8_FOUR_LAYER_LANGUAGE.md` | Observation / Interpretation / Constraint / Action |
| `governance/HERMES_DNA.md` | ECHO·SCAR·ATLAS·MAP topology + Dark Mirror |
| `governance/DOUBLE_HELIX_ECHO_SCAR.md` | Dual continuity strands |
| `governance/INSTITUTIONAL_COMPRESSION.md` | Ambiguity reduction + freeze |
| `governance/AGENTIC_INSTITUTION_PARADOXES.md` | MAP·ATLAS·ECHO doctrine |

Telemetry (observe-only freeze): `map-atlas-echo` · Kabarkan → PG · cron 6h.

## 🧬 Agent · Skill · Tool · Organ — The Entity Ontology

```
+-------------------------------------------------------------------------+
|                               AGENTS                                    |
| (Autonomous Citizens with Identity, Authority & Intent State)           |
|  333-AGI · 555-ASI · 888-APEX · opencode (FI-001)                       |
+------------------------------------+------------------------------------+
                                     | Executes
                                     v
+-------------------------------------------------------------------------+
|                                SKILLS                                   |
| (Domain Knowledge Workflows & Epistemic Procedures)                     |
|  AGI-explorer-intelligence · FORGE-infra-guardian                       |
+------------------------------------+------------------------------------+
                                     | Invokes
                                     v
+-------------------------------------------------------------------------+
|                                TOOLS                                    |
| (Deterministic Execution Primitives via MCP or Shell)                   |
|  arif_observe · geox_petrophysics · forge_git                           |
+------------------------------------+------------------------------------+
                                     | Hosted On
                                     v
+-------------------------------------------------------------------------+
|                                ORGANS                                   |
| (Microservice Infrastructure Bounds — systemd daemons)                  |
|  arifOS (:8088) · A-FORGE (:7071) · GEOX (:8081) · AAA (:3001)         |
+-------------------------------------------------------------------------+
```

---

## 🌐 A2A Mesh vs. MCP Surface

| Dimension | A2A (AAA Gateway :3001) | MCP (arifOS Kernel :8088) |
|:---|:---|:---|
| **Focus** | Agent ↔ Agent coordination | Agent ↔ Tool invocation |
| **Protocol** | Async JSON-RPC · Agent Cards · Task Delegation | Sync JSON-RPC 2.0 · FastMCP |
| **State** | Persistent AREP tasks, long-running threads | Synchronous request-response |
| **Governance** | Task routing, role mapping, agent registry | F1–F13 floor checking, 888_HOLD gates |

---

## 🛰️ Operator Cockpit

AAA provides a React 19 + Vite 8 cockpit displaying real-time federation health, agent status, and pending `888_HOLD` decisions.

```
Public Gateway:  https://aaa.arif-fazil.com
Local Gateway:   http://127.0.0.1:3001
Agent Card:      https://aaa.arif-fazil.com/.well-known/agent-card.json
```

```bash
curl -s http://127.0.0.1:3001/health | jq .     # Health & drift
cd /root/AAA && npm run build                     # Rebuild
npm run a2a:conformance                           # Validate A2A suite
```

---

## 🏛️ Federation Navigation

| Organ | Role | Port | Repo | MCP | Health | LLMs |
|:---|:---|:---:|:---|:---|:---|:---|
| **⚖️ arifOS** | Constitutional Kernel — judges, seals | 8088 | [repo](https://github.com/ariffazil/arifos) | [mcp](https://mcp.arif-fazil.com/mcp) | [health](https://arifos.arif-fazil.com/health) | [llms.txt](https://arifos.arif-fazil.com/llms.txt) |
| **⚒️ A-FORGE** | Execution Engine — builds, deploys | 7071/72 | [repo](https://github.com/ariffazil/A-FORGE) | [mcp](https://forge.arif-fazil.com/mcp) | [health](https://forge.arif-fazil.com/health) | [llms.txt](https://forge.arif-fazil.com/llms.txt) |
| **🏛️ AAA** | Control Plane — A2A gateway, cockpit | 3001 | [repo](https://github.com/ariffazil/AAA) | — | [health](https://aaa.arif-fazil.com/health) | [llms.txt](https://aaa.arif-fazil.com/llms.txt) |
| **🌍 GEOX** | Earth Intelligence — seismic, wells | 8081 | [repo](https://github.com/ariffazil/GEOX) | [mcp](https://geox.arif-fazil.com/mcp) | [health](https://geox.arif-fazil.com/health) | [llms.txt](https://geox.arif-fazil.com/llms.txt) |
| **💰 WEALTH** | Capital Intelligence — NPV, risk | 18082 | [repo](https://github.com/ariffazil/WEALTH) | [mcp](https://wealth.arif-fazil.com/mcp) | [health](https://wealth.arif-fazil.com/health) | [llms.txt](https://wealth.arif-fazil.com/llms.txt) |
| **🫀 WELL** | Vitality Guard — human readiness | 18083 | [repo](https://github.com/ariffazil/WELL) | [mcp](https://well.arif-fazil.com/mcp) | [health](https://well.arif-fazil.com/health) | [llms.txt](https://well.arif-fazil.com/llms.txt) |
| **🔮 HERMES** | Multi-Modal Bridge — Telegram relay | 8644 | [repo](https://github.com/ariffazil/HERMES) | — | — | — |
| **🌐 arif-fazil.com** | Public Web Surface — one domain | 443 | [repo](https://github.com/ariffazil/arif-fazil.com) | — | [verify](https://arif-fazil.com/999/verify) | — |
| **💀 VAULT999** | Immutable Seal — append-only receipt chain | fs | [repo](https://github.com/ariffazil/arifOS/VAULT999) | — | [verify](https://arifos.arif-fazil.com/health) | — |

---

## 📡 Federation Registries

AAA operates the A2A (Agent-to-Agent) mesh — discovery metadata is exposed at the standard agent card endpoints.

| Registry | Manifest |
|----------|----------|
| **A2A v1.0** | `GET https://aaa.arif-fazil.com/.well-known/agent.json` — base agent card |
| **A2A v2.x** | `GET https://aaa.arif-fazil.com/.well-known/agent-card.json` — extended card (authenticated) |
| **Federation Discovery** | `GET https://arifos.arif-fazil.com/.well-known/federation/agents.json` — all 11 forge instruments |

Federation surface: [aaa.arif-fazil.com](https://aaa.arif-fazil.com) · Health: `GET https://aaa.arif-fazil.com/health`

---

## � Sovereignty & License

- **License:** GNU Affero General Public License v3.0 (**AGPL-3.0**)
- **Sovereign:** **Muhammad Arif bin Fazil** (F13 SOVEREIGN). AAA is the institutional window for sovereign oversight.

> *DITEMPA BUKAN DIBERI — Forged, Not Given.*  
> *Maruah without SEAL is sentiment. SEAL without Maruah is enforcement. 999 SEAL ALIVE.*

---

## 🛡️ CI Governance (F13 verdict 2026-08-10)

This repo follows the federation's CI governance pattern (replicated from `ariffazil/arifOS` PR #683). The pattern ensures Dependabot PRs receive a real, reproducible unprivileged verdict — no more all-red check rolls from structurally-incompatible gates.

**Per-repo adapter** (see `.github/workflows/` for the actual files):

- `.github/dependabot.yml` — `uv` (Python) / `cargo` (Rust) / `npm` (TypeScript) ecosystem; cooldown 3d; open-PRs 5; constitutional packages un-grouped (no `ignore:` — visibility preserved)
- `.github/workflows/dependabot-ci.yml` — unprivileged gate; runs ONLY on Dependabot PRs; SHA-bound probes
- `.github/workflows/{ci-uv-lock-invariant|cargo-lock-invariant|npm-lock-invariant}.yml` — universal `{uv lock --check && uv sync --frozen | cargo check --locked && cargo build --locked | npm ci}` invariant on every PR + push to main
- `.github/workflows/auto-merge-dependabot.yml` — constitutional package denylist (per-language); F13 review the only merge path
- Privileged workflows gated with `if: github.actor != 'dependabot[bot]' && github.actor != 'app/dependabot'` — so they SKIP for Dependabot PRs where their inputs cannot be satisfied

**Constitutional packages** (denied auto-merge, require F13 review):

| Language | Denylist |
|---|---|
| Python | `protobuf`, `cryptography`, `fastmcp-slim`, `fastmcp`, `caio`, `sentence-transformers`, `pynacl`, `blake3` |
| Rust    | `serde`, `tokio`, `hyper`, `axum`, `reqwest`, `rustls`, `async-trait`, `clap`, `tracing` |
| TypeScript | `zod`, `@modelcontextprotocol/sdk`, `fastmcp`, `mcp-sdk`, `tsx`, `vitest`, `@types/node`, `typescript`, `ts-node` |
| Static site | `vite`, `react`, `react-dom`, `react-router`, `@tanstack/react-query`, `tailwindcss` |

**Reference:** [`/root/AGENTS.md`](/root/AGENTS.md) — canonical federation doctrine. `AAA/docs/ORGAN.md` — topology.

DITEMPA BUKAN DIBERI — governance is forged, not given.
