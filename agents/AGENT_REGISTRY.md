# AGENT_REGISTRY.md — AAA Federation Agent Registry

> **Canonical agent index for the arifOS Federation.**
> **Last updated:** 2026-06-13 15:45 UTC
> **Supersedes:** AAA_AGENTS_REGISTRY.json (machine-readable), HEXAGON.yaml (topology)
> **Rule:** This file is the human-readable source of truth. Agents not listed here are spec-only or deprecated.

---

## LAYER 1: HEXAGON — Constitutional Agents (5)

The 5-agent constitutional architecture. Pipeline: 000 → 333 → 555 → 888 → A-AUDIT → A-ARCHIVE → reseed.

### PRIMARY (Externally Addressable)

| ID | Trinity | Tier | Skills | Host Organs | Status |
|---|---|---|---|---|---|
| **333-AGI** | Δ MIND | AGI | 10 | arifOS, GEOX, WEALTH | ✅ SPEC |
| **555-ASI** | Ω HEART | ASI | 4 | WELL, arifOS | ✅ SPEC |
| **888-APEX** | ΦΙ JUDGE | APEX | 3 | arifOS | ✅ SPEC |

### SUPPORT (Internal Control Plane)

| ID | Tier | Skills | Status |
|---|---|---|---|
| **A-AUDIT** | APEX oversight | 3 (floor-compliance, inter-agent-consistency, behavioral-health) | ✅ SPEC |
| **A-ARCHIVE** | ASI service | 3 (seal-write, seal-read, integrity-proof) | ✅ SPEC |

> **Note:** HEXAGON agents are defined in `HEXAGON.yaml`. Their IDENTITY/SOUL/AGENTS files are pending forge. They currently exist as A2A agent cards only.

---

## LAYER 2: RUNTIME — Live Agents (4)

Agents with active systemd services and Telegram presence.

| ID | Tier | Lane | Telegram | Port | Config | Status |
|---|---|---|---|---|---|---|
| **hermes-asi** | ASI | SOUL/OMEGA | @ASI_arifos_bot | 18001 (A2A) | `/root/.hermes/config.yaml` | ✅ LIVE |
| **openclaw** | AGI | C2-Execute | @AGI_ASI_bot | 18789 | `/root/.openclaw/workspace/` | ✅ LIVE |
| **777-forge** | 777 | Witness/Spawn | — | — | A2A registered | ✅ LIVE |
| **antigravity** | AGI | L3-Autonomous | — | — | `/root/.gemini/` | ✅ LIVE |

---

## LAYER 3: INFRASTRUCTURE — Organs as A2A Peers (6)

| ID | Role | Port | Domain | Status |
|---|---|---|---|---|
| **arifos-kernel** | Constitutional guardian, F1-F13, JUDGE, VAULT | 8088 | Ω Law | ✅ LIVE |
| **aforge-executor** | Execution shell, build/deploy | 7071 | Ψ Body | ✅ LIVE |
| **geox-witness** | Earth intelligence, petrophysics | 8081 | Δ Earth | ✅ LIVE |
| **wealth-witness** | Capital intelligence, finance | 18082 | Δ Capital | ✅ LIVE |
| **well-mirror** | Human readiness, vitality | 18083 | Δ Vitality | ✅ LIVE |
| **aaa-gateway** | Control plane, A2A mesh, cockpit | 3001 | AAA Ops | ✅ LIVE |

---

## LAYER 4: CODING FEDERATION — Forge Instruments (8)

All share the 97-tool capability index and F1-F13 governance.

| FI# | ID | Model | Native MCP | Init Mode | Risk | Status |
|---|---|---|---|---|---|---|
| **FI-001** | opencode | deepseek-chat | ✅ 18 servers | swarm_ignite (engineer) | YELLOW | ✅ LIVE |
| **FI-002** | claude-code | deepseek-chat | ✅ 10 servers | swarm_ignite (engineer) | YELLOW | ✅ LIVE |
| **FI-003** | qwen-code | qwen | ❌ None | observer (3 tools) | LOW | ⚠️ not connected |
| **FI-004** | antigravity | gemini-2.5-pro | ✅ 13 servers | swarm_ignite (analyst) | GREEN | ✅ LIVE |
| **FI-005** | codex | gpt-5.5 | ⚠️ MCP-ready | observer | YELLOW | ⚠️ MCP unverified |
| **FI-006** | copilot | gpt-4o | ✅ 8 servers | init (analyst) | GREEN | ✅ LIVE |
| **FI-007** | aider | MiniMax-M3 | ❌ No | bridge mode | YELLOW | ✅ LIVE |
| **FI-008** | kimi-code | kimi | ✅ 9 servers | — | YELLOW | ✅ LIVE |
| **FI-009** | continue-cli | MiniMax-M3 | ✅ 17 servers | — | YELLOW | ✅ LIVE |

---

## LAYER 5: LEGACY — Deprecated/Spec-Only (3)

| ID | Reason | Superseded By | Status |
|---|---|---|---|
| **apex** | Memory engine. Deliberation moved to AAA a2a-server. | aaa-a2a (deliberation.ts) | ⚠️ SPEC-ONLY |
| **maxhermes** | GEOX Earth specialist. Hermes handles Earth tasks directly. | hermes-asi | ⚠️ SPEC-ONLY |
| **hermes-ops** | DevOps specialist. Tasks delegated to OpenClaw or claude-code. | openclaw / claude-code | ⚠️ SPEC-ONLY |
| **aaa-architect** | Pre-HEXAGON ARoLE. | 333-AGI | ❌ SUPERSEDED |
| **aaa-engineer** | Pre-HEXAGON ARoLE. | A-FORGE | ❌ SUPERSEDED |
| **aaa-auditor** | Pre-HEXAGON ARoLE. | A-AUDIT + 888-APEX | ❌ SUPERSEDED |

---

## AGENT COUNT

| Layer | Count | Status |
|---|---|---|
| HEXAGON (Constitutional) | 5 | SPEC (cards only) |
| RUNTIME (Live Services) | 4 | LIVE |
| INFRASTRUCTURE (Organs) | 6 | LIVE |
| CODING (Forge Instruments) | 9 | 7 LIVE, 2 unverified |
| LEGACY (Spec-Only) | 3 | DEPRECATED |
| **TOTAL ACTIVE** | **19** | |
| **TOTAL ALL** | **27** | (excluding sovereign 000-SALAM) |

---

## SOVEREIGN

| ID | Role |
|---|---|
| **000-SALAM** | Muhammad Arif bin Fazil — Human Sovereign, F13 final veto. NOT an agent. |

---

## CANONICAL FILES

| File | Purpose |
|---|---|
| `AGENT_REGISTRY.md` | **This file** — human-readable canonical index |
| `HEXAGON.yaml` | Constitutional agent topology (5 agents, pipeline) |
| `AAA_AGENTS_REGISTRY.json` | Machine-readable registry (v2.0.0) |
| `CODING_AGENT_FEDERATION.md` | Forge instrument reference (8 agents, 97 tools) |
| `a2a-server/agent-cards/` | A2A discovery cards (JSON-LD) |

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
