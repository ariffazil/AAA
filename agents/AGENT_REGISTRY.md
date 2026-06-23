# AGENT_REGISTRY.md — AAA Federation Agent Registry

> **Canonical agent index for the arifOS Federation.**
> **Last updated:** 2026-06-23 (grok-build self-knowledge + AAA toolbench registry refresh per CLAIM spec)
> **Previous:** 2026-06-18 06:30 UTC
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

**Polymorphic Model (per contracts/hermes-role-binding.md and contracts/AAA_SKILL_BINDING.md):** One Hermes runtime, N explicit role bindings via skills[] (Ω 555-ASI, Δ 333-AGI, etc.). No duplicate processes for role-binds. Orthogonal mapping (Trinitarian Δ/Ω/ΦΙ + Functional) applied. Spawns only for distinct citizens when native capability exceeds Hermes + kernel. See artifacts/AAA-17-CITIZEN-ORTHOGONAL-MATRIX-2026-06-22.md for full 17-citizen matrix.

| ID | Tier | Lane | Telegram | Port | Config | Status |
|---|---|---|---|---|---|---|
| **hermes-asi** | ASI | SOUL/OMEGA | @ASI_arifos_bot | 18001 (A2A) | `/root/.hermes/config.yaml` | ✅ LIVE (polymorphic hub: 555-ASI / 333-AGI / front-door; role-binding-polymorphic) |
| **openclaw** | AGI | C2-Execute | @AGI_ASI_bot | 18789 | `/root/.openclaw/workspace/` | ✅ LIVE (subagent orchestration focus) |
| **777-forge** | 777 | Witness/Spawn | — | — | A2A registered | ✅ LIVE |
| **antigravity** | AGI | L3-Autonomous | — | — | `/root/.gemini/` | ✅ LIVE |

**Full 17-Citizen Matrix Summary (see artifacts for details):**  
HEXAGON (333-AGI Δ, 555-ASI Ω, 888-APEX ΦΙ, A-AUDIT, A-ARCHIVE): Role bindings + 8-12 skills each, heavy on constitutional/forge/audit.  
RUNTIME: hermes-asi (polymorphic), openclaw (execution), 777-forge, antigravity.  
CODING/FI (~9: grok-build + claude-code, opencode, codex, kimi-code, copilot, aider, continue-cli, gemini-cli, qwen): Baseline 8 + consumer role-bindings; grok-build exemplar at 12 with orthogonal depth.  
Legacy (aaa-*, hermes-ops): Minimal or deprecated.  

All focus citizens now declare explicit role-binding-* skills with references to contracts and orthogonal axes. Skills counts increased; F11 auditability strengthened.

**999_SEAL:** /root/AAA/artifacts/AAA-999-SEAL-2026-06-23.md (Gold). Polymorphic + Principal Agent Taxonomy phase complete.

**Principal Agent Taxonomy (see contracts/principal-agent-taxonomy.md):**  
`principal_agent` is now a first-class field (human | architect | agent | earth | llm | institution | void | liar | unknown) with `principal_binding` object. Enables A2A routing, F11 audit, polymorphic clarity, and honest capability surfacing.  

Classification (18 citizens):  
- architect (7): arifOS, A-FORGE, 888-APEX, 555-ASI, 333-AGI, A-AUDIT, A-ARCHIVE  
- agent (3): hermes-asi, openclaw, hermes-ops  
- earth (3): GEOX, WEALTH, WELL  
- llm (10+): grok-build + opencode, claude-code, codex, copilot, kimi-code, aider, antigravity, continue-cli, gemini-cli, qwen-code  
- human (1): arif-fazil-identity  

Schema enhancement applied: `principal_agent` (string) + `principal_binding` + `principal_accountability`. See taxonomy contract for full table and rationale. This directly elevates F11 auditability and A2A governance clarity.

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
| **FI-001** | opencode | tokenplan-mimo/mimo-v2.5-pro | ✅ 20 servers | swarm_ignite (engineer) | YELLOW | ✅ LIVE |
| **FI-002** | claude-code | deepseek-chat | ✅ 10 servers | swarm_ignite (engineer) | YELLOW | ✅ LIVE |
| **FI-003** | qwen-code | qwen | ❌ None | observer (3 tools) | LOW | ⚠️ not connected |
| **FI-004** | antigravity | gemini-2.5-pro | ✅ 13 servers | swarm_ignite (analyst) | GREEN | ✅ LIVE |
| **FI-005** | codex | gpt-5.5 | ⚠️ MCP-ready | observer | YELLOW | ⚠️ MCP unverified |
| **FI-006** | copilot | gpt-4o | ✅ 8 servers | init (analyst) | GREEN | ✅ LIVE |
| **FI-007** | aider | MiniMax-M3 | ❌ No | bridge mode | YELLOW | ✅ LIVE |
| **FI-008** | kimi-code | kimi | ✅ 9 servers | — | YELLOW | ✅ LIVE |
| **FI-009** | continue-cli | MiniMax-M3 | ✅ 17 servers | — | YELLOW | ✅ LIVE |

---

## LAYER 4.2: HARNESS / BUILD AGENTS (1)

High-power agentic harnesses with native tool depth, advanced subagent parallelism, workflow orchestration, and external MCP surface. Session/ACP launched (not persistent daemons). Full F1-F13 binding via AGENTS.md + skills.

| ID | Model/Harness | Native MCP | Key Differentiators | Risk | Status |
|---|---|---|---|---|---|
| **grok-build** | Grok 4.3 (xAI Build TUI) | ✅ github(95) + geox(15) + wealth(24) + well(15) + native | Subagent (worktree isolation, capability modes, resume_from, personas); plan-mode; implement/design/execute-plan loops; scheduler+monitor; image/video; headless+ACP; rich .agents/skills (geox/arifos/cloudflare/pydantic/sbx); GitHub deep ops. **Skills enhanced post-reg (orthogonal mapping applied)**: plan-mode (Δ/F1-F4-F7), subagent-spawn (Ψ), mcp-federation (routing), autonomous-governed-execution (ΦΙ), arifos-arconstitutional-audit (ΦΙ/F1-F13), fff-loop-protocol (Forge/F1-F11), agentic-architecture (declaration). 12 skills now declared. | YELLOW | ✅ REGISTERED + ENHANCED 2026-06-22 (Phase 1 runtime activated) |

**Notes for grok-build:** Ephemeral harness (launch on demand). Strongest declared parallelism + orchestration in current registry. Routes federation via MCP federation skill. Self-known per 2026-06-23 CLAIM: model xai/grok-build-0.1 (256K), 3-stage plan\u2192search\u2192build + \u22648 agents, auto Claude MCP/skills ingest, SWE-Bench sys ~70.8%, tool err ~1.27%. See `/root/AAA/agents/grok-build/agent-card.json`, `AGENTS.md`, `TOOLS.md` + toolbench in AAA_AGENTS_REGISTRY.json.

---

## LAYER 4.5: ROLE AGENTS — Bounded C2/C3 Specialists (4)

> **Forged:** 2026-06-14 by FORGE (000Ω) — per Perplexity gap analysis.
> These agents operate within bounded leases. They observe, analyze, plan, propose — but execute only through the governed forge pipeline.

| ID | Class | Ring | Host Organs | Lease Max | Role Card |
|---|---|---|---|---|---|
| **Kernel Scribe** | C2 | SERVICE | arifOS, AAA | OBSERVE + PROPOSE | `roles/KERNEL_SCRIBE.md` |
| **Ops Planner** | C2 | SERVICE | AAA, WEALTH, WELL | OBSERVE + PROPOSE | `roles/OPS_PLANNER.md` |
| **Self-Forge Advisor** | C3 | Δ MIND | A-FORGE, arifOS | PROPOSE + MUTATE (gated) | `roles/SELF_FORGE_ADVISOR.md` |
| **External Watcher** | C1 | SERVICE | AAA | OBSERVE only | `roles/EXTERNAL_WATCHER.md` |

**Communication Rule:** Role agents are SUBORDINATE to HEXAGON agents. They do not execute independently — they feed analysis and proposals to HEXAGON agents (333-AGI, 555-ASI, 888-APEX) for judgment and execution.

---

## LAYER 5: LEGACY — Deprecated/Spec-Only (3)

| ID | Reason | Superseded By | Status |
|---|---|---|---|
| **apex** | Memory engine. Deliberation moved to AAA a2a-server. | aaa-a2a (deliberation.ts) | ⚠️ SPEC-ONLY |
| **maxhermes** | GEOX Earth specialist. **REMOVED 2026-06-22** — clarified as external MiniMax cloud product (see `external/maxhermes/`). | external/maxhermes (MiniMax cloud) | ⚠️ ARCHIVED |
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
| ROLE AGENTS (Specialists) | 4 | SPEC (role cards forged 2026-06-14) |
| CODING (Forge Instruments) | 9 | 7 LIVE, 2 unverified |
| LEGACY (Spec-Only) | 3 | DEPRECATED |
| **TOTAL ACTIVE** | **23** | |
| **TOTAL ALL** | **27** | (excluding sovereign 000-SALAM) |

> **Registry sync note (2026-06-18):** `AAA_AGENTS_REGISTRY.json` (machine-readable) was audited against live runtime state and updated to include `hermes-asi` and `openclaw` in a new `RUNTIME` tier. Human-readable LAYER 2 already matched live state; JSON registry now matches.

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
| `ROOT_AGENT_CONFIG.yaml` | Root config for AAA warga, peers, forge instruments, and config pointers |
| `HEXAGON.yaml` | Constitutional agent topology (5 agents, pipeline) |
| `AAA_AGENTS_REGISTRY.json` | Machine-readable registry (v2.0.0) |
| `CODING_AGENT_FEDERATION.md` | Forge instrument reference (8 agents, 97 tools) |
| `a2a-server/agent-cards/` | A2A discovery cards (JSON-LD) |

---

## OPERATIONAL SKILLS (Forged 2026-06-14)

Skills deployable by OpenClaw and callable by all warga agents:

| Skill | Agent | Priority | Purpose |
|---|---|---|---|
| `federation-health-scan` | OpenClaw | P0 | 6 organs + NATS + drift + vault in one structured command |
| `drift-response` | OpenClaw | P0 | Standard 5-step: detect→verify→classify→propose→route |
| `subagent-spawn` | OpenClaw | P1 | Bounded task contract: output schema + time budget + evidence |

Hermes Constitutional Tools (registered in arifOS MCP):

| Tool | Purpose |
|---|---|
| `hermes_system_status` | Live organ health + NATS + drift diagnostic |
| `hermes_vault_query` | VAULT999 history search by date/organ/keyword |
| `hermes_epistemic_check` | Pre-claim confidence validation (TAHU/NAMPAK/RASA/TAK_TAHU) |

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*


---

## 2026-06-22 — FI Citizens Skills Binding Sweep

Wired 9 FI citizens as real AAA warga with 8-skill baseline (per orthogonal mapping pattern):

| Citizen | Skills | Binary | Mirror |
|---------|--------|--------|--------|
| opencode | 8 | opencode | a2a-server/agent-cards/opencode.json |
| claude-code | 8 | claude | a2a-server/agent-cards/claude-code.json |
| codex | 8 | codex | a2a-server/agent-cards/codex.json |
| copilot | 8 | copilot | a2a-server/agent-cards/copilot.json |
| kimi-code | 8 | kimi | a2a-server/agent-cards/kimi-code.json |
| aider | 8 | aider | a2a-server/agent-cards/aider.json |
| antigravity | 8 | agy (Gemini 3.5) | a2a-server/agent-cards/antigravity.json |
| continue-cli | 8 | cn | a2a-server/agent-cards/continue-cli.json |
| gemini-cli | 8 | gemini | a2a-server/agent-cards/gemini-cli.json |

**Baseline 8 skills per FI citizen:**
1. hermes-opencode-protocol
2. agentic-architecture
3. fabrication-prevention
4. autonomous-governed-execution
5. arifos-arconstitutional-audit (light)
6. godel-humility-lock
7. github-workflow
8. arifos-mcp-federation

Pattern reference: `/root/HERMES/skills/aaa-agentic-governance/references/orthogonal-skill-binding-pattern-2026-06-22.md`

**Receipt:** `/root/AAA/artifacts/fi-warga-binding-sweep-2026-06-22.md`
