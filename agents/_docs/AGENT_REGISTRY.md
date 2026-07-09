# AGENT_REGISTRY.md — AAA Federation Registry

> **Canonical agent index for the arifOS Federation.**
> **Last updated:** 2026-06-26 (SCAR-13 — definitional clarity + Eureka Layer column)
> **Previous:** 2026-06-23 (grok-build self-knowledge + AAA toolbench registry refresh per CLAIM spec)
> **Supersedes:** AAA_AGENTS_REGISTRY.json (machine-readable), HEXAGON.yaml (topology)
> **Rule:** This file is the human-readable source of truth. Agents not listed here are spec-only or deprecated.

---

## ⚠️ SCAR-13 — DEFINITIONAL CLARITY (2026-06-26)

This file is named `AGENT_REGISTRY.md` but historically conflates **THREE categories** of entity.

Under the arifOS-native definition (SCAR-12, ratified 2026-06-26):

> *An **agent** = loop(Model × Tools × State × Goal) → Actions, terminating in a sealed constitutional verdict.*

| Category | Definition | Examples in this file | Count |
|---|---|---|---|
| **TRUE AGENTS** | Loops with state, goals, and sealed exit verdicts | HEXAGON, RUNTIME, CODING, ROLE, harness | ~22 |
| **CAPABILITY REGISTRIES** | Sovereign MCP servers exposing tools — **NOT agents** (they host agents; they don't loop themselves) | INFRASTRUCTURE organs (arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA) | 6 |
| **LEGACY SPECS** | Historical cards, no runtime | apex, maxhermes, hermes-ops, aaa-* legacy | 3+ |

**Naming:** The file name `AGENT_REGISTRY` is a historical artifact. Pending Option A split (F13-gated, see §"Option A — Proposed Split"), the same content will move to:
- `FEDERATION_REGISTRY.md` (top-level index)
- `agents/HEXAGON.md` + `RUNTIME.md` + `CODING_FEDERATION.md` + `ROLE_AGENTS.md` + `LEGACY.md`
- `organs/ORGANS.md` (NOT agents)
- `substrates/SUBSTRATES_POINTER.md` (points to `/root/arifOS/arifosmcp/config/model_registry.json`)

**Eureka Layer column** added to each table below maps each entity to its four-fold eureka role:
- **L1 — Substrate**: what the model produces
- **L2 — Governance**: what the harness allows to pass (arifOS F1-F13)
- **L3 — Authority**: what the operator authorizes to display/execute (AAA + HEXAGON)
- **L4 — Execution**: what reality actually commits (A-FORGE + VAULT999)

Organs sit across L2–L4 as **hosts of agents**, not as agents themselves.

---

## ⚠️ REGISTRY DRIFT NOTICE (2026-06-26, updated 2026-06-26 UTC)

`AGENT_REGISTRY.md` (this file) and `/root/AAA/registries/AAA_AGENTS_REGISTRY.json` (machine-readable) previously disagreed on 3 entries. The machine registry has now been reconciled for `qwen-code` and `777-forge`.

| Entry | MD says | JSON says | Resolution |
|---|---|---|---|
| `qwen-code` | FI-003, listed | present in JSON | Resolved 2026-06-26 — first-class FI citizen restored in machine registry. |
| `gemini-cli` | mentioned in FI baseline (note +9) | present in JSON line 635 | Resolved in MD row. |
| `777-forge` | Layer 2 RUNTIME entry | present in JSON | Resolved 2026-06-26 — witness citizen restored in machine registry. |
| `antigravity` | Layer 2 runtime binding **and** Layer 4 CODING citizen | only in CODING | Clarified: one canonical FI citizen (`antigravity`) with an additional runtime binding in prose, not a second machine-registry citizen. |

**F2 TRUTH receipt:** Original drift confirmed via `diff` 2026-06-26 07:15 UTC. As of the af-forge CLI binding sweep later the same day, `qwen-code` and `777-forge` are reconciled; `antigravity` is now documented as one canonical FI citizen plus one runtime binding note.

---

## LAYER 1: HEXAGON — Constitutional Agents (6)

> **Updated 2026-06-26:** OpenCode promoted from forge_instrument (Layer 4 FI-001) to HEXAGON external warga (Layer 1). See HEXAGON.yaml v2.1.0 `agents: external:` section.

The 5-agent constitutional architecture. Pipeline: 000 → 333 → 555 → 888 → A-AUDIT → A-ARCHIVE → reseed.

### PRIMARY (Externally Addressable)

| ID | Trinity | Tier | Skills | Host Organs | Eureka Layer | Status |
|---|---|---|---|---|---|---|
| **333-AGI** | Δ MIND | AGI | 10 | arifOS, GEOX, WEALTH | **L3 — Authority** | ✅ SPEC |
| **555-ASI** | Ω HEART | ASI | 4 | WELL, arifOS | **L3 — Authority** | ✅ SPEC |
| **888-APEX** | ΦΙ JUDGE | APEX | 3 | arifOS | **L3 — Authority** | ✅ SPEC |

### SUPPORT (Internal Control Plane)

| ID | Tier | Skills | Eureka Layer | Status |
|---|---|---|---|---|
| **A-AUDIT** | APEX oversight | 5 (floor-compliance, inter-agent-consistency, behavioral-health, **symbolic-order-trust-architecture, symbolic-order-collective-bias**) | **L2 — Governance** (enforces F1-F13) | ✅ SPEC |
| **A-ARCHIVE** | ASI service | 3 (seal-write, seal-read, integrity-proof) | **L4 — Execution** (commits to VAULT999) | ✅ SPEC |

### EXTERNAL (Forge Instruments — warga-bound)

| ID | Trinity | Tier | Skills | Host Organs | Eureka Layer | Status |
|---|---|---|---|---|---|---|
| **opencode** | Δ MIND (bound) | AGI | 13 | A-FORGE, arifOS, AAA | **L4 — Execution** (bound to 333-AGI Δ MIND, A2A mesh citizen) | ✅ WARGA (2026-06-26) |

> **Note:** HEXAGON agents are defined in `HEXAGON.yaml` v2.1.0. OpenCode is the 6th warga (external/forge-instrument). All warga have A2A cards and ATTESTATION.md.
>
> **888-APEX mapping:** 888-APEX is the constitutional judgment organ of arifOS. AAA holds the agent card for A2A discovery and routing. This is the standard organ-to-warga mapping pattern: arifOS owns the organ, AAA owns the card. Not a conflict — by design.

---

## LAYER 2: RUNTIME — Live Agents (4)

Agents with active systemd services and Telegram presence.

**Polymorphic Model (per contracts/HERMES_ROLE.md and contracts/AAA_SKILL.md):** One Hermes runtime, N explicit role bindings via skills[] (Ω 555-ASI, Δ 333-AGI, etc.). No duplicate processes for role-binds. Orthogonal mapping (Trinitarian Δ/Ω/ΦΙ + Functional) applied. Spawns only for distinct citizens when native capability exceeds Hermes + kernel. See artifacts/AAA_CITIZEN.md for full 17-citizen matrix.

| ID | Tier | Lane | Telegram | Port | Config | Eureka Layer | Status |
|---|---|---|---|---|---|---|---|
| **hermes-asi** | ASI | SOUL/OMEGA | @ASI_arifos_bot | 18001 (A2A) | `/root/.hermes/config.yaml` | **L3 — Authority** (interface to L3) | ✅ LIVE (polymorphic hub: 555-ASI / 333-AGI / front-door; role-binding-polymorphic) |
| **openclaw** | AGI | C2-Execute | @AGI_ASI_bot | 18789 | `/root/.openclaw/workspace/` | **L3 — Authority** (subagent orchestration) | ✅ LIVE (subagent orchestration focus) |
| **777-forge** | 777 | Witness/Spawn | — | — | A2A registered | **L4 — Execution** (witness-only, bounded) | ✅ LIVE (drift: not in JSON registry — see §DRIFT) |
| **antigravity** (runtime binding of FI-004) | AGI | L3-Autonomous | — | — | `/root/.gemini/` | **L3 — Authority** (Gemini 3.5 runtime binding of the same citizen tracked in CODING as FI-004) | ✅ LIVE |

**Full 17-Citizen Matrix Summary (see artifacts for details):**  
HEXAGON (333-AGI Δ, 555-ASI Ω, 888-APEX ΦΙ, A-AUDIT, A-ARCHIVE): Role bindings + 8-12 skills each, heavy on constitutional/forge/audit.  
RUNTIME: hermes-asi (polymorphic), openclaw (execution), 777-forge, antigravity runtime binding.  
CODING/FI (~9: grok-build + claude-code, opencode, codex, kimi-code, copilot, aider, continue-cli, gemini-cli, qwen-code): Baseline 8 + consumer role-bindings; grok-build exemplar at 12 with orthogonal depth.  
Legacy (aaa-*, hermes-ops): Minimal or deprecated.  

All focus citizens now declare explicit role-binding-* skills with references to contracts and orthogonal axes. Skills counts increased; F11 auditability strengthened.

**999_SEAL:** /root/AAA/artifacts/AAA_SEAL.md (Gold). Polymorphic + Principal Agent Taxonomy phase complete.

**Principal Agent Taxonomy (see contracts/PRINCIPAL_AGENT.md):**  
`principal_agent` is now a first-class field (human | architect | agent | earth | llm | institution | void | liar | unknown) with `principal_binding` object. Enables A2A routing, F11 audit, polymorphic clarity, and honest capability surfacing.  

Classification (18 citizens):  
- architect (7): arifOS, A-FORGE, 888-APEX, 555-ASI, 333-AGI, A-AUDIT, A-ARCHIVE  
- agent (3): hermes-asi, openclaw, hermes-ops  
- earth (3): GEOX, WEALTH, WELL  
- llm (10+): grok-build + opencode, claude-code, codex, copilot, kimi-code, aider, antigravity, continue-cli, gemini-cli, qwen-code  
- human (1): arif-fazil-identity  

Schema enhancement applied: `principal_agent` (string) + `principal_binding` + `principal_accountability`. See taxonomy contract for full table and rationale. This directly elevates F11 auditability and A2A governance clarity.

---

## LAYER 3: INFRASTRUCTURE — Sovereign Capability Registries (6)

> **⚠️ SCAR-13 RECLASSIFICATION (2026-06-26):** These are **NOT agents** under the arifOS-native definition (SCAR-12). They are **sovereign MCP servers** that expose tools and host agents. They are listed here for completeness because they appear in A2A peer discovery, but the proper taxonomy places them in `organs/ORGANS.md` (pending Option A split).

| ID | Role | Port | Domain | Eureka Layer | Status |
|---|---|---|---|---|---|
| **arifos-kernel** | Constitutional guardian, F1-F13, JUDGE, VAULT | 8088 | Ω Law | **L2 — Governance** | ✅ LIVE |
| **aforge-executor** | Execution shell, build/deploy | 7071 | Ψ Body | **L4 — Execution** | ✅ LIVE |
| **geox-witness** | Earth intelligence, petrophysics | 8081 | Δ Earth | **L2 — Governance** (domain witness) | ✅ LIVE |
| **wealth-witness** | Capital intelligence, finance | 18082 | Δ Capital | **L2 — Governance** (domain witness) | ✅ LIVE |
| **well-mirror** | Human readiness, vitality | 18083 | Δ Vitality | **L2 — Governance** (domain witness) | ✅ LIVE |
| **aaa-gateway** | Control plane, A2A mesh, cockpit | 3001 | AAA Ops | **L3 — Authority** (gateway host) | ✅ LIVE |

**Why these are not agents:** Each organ is a stateless (or lease-stateful) MCP server. It exposes tools and may host internal loops (e.g., arifOS runs the Golden Path loop internally), but as a top-level entity its primary contract is **exposing capabilities**, not **driving decisions toward a goal**. The agents that drive decisions are the HEXAGON warga that run on top of these organs.

---

## LAYER 4: CODING FEDERATION — Forge Instruments (8)

All share the 97-tool capability index and F1-F13 governance.

| FI# | ID | Model | Native MCP | Init Mode | Risk | Eureka Layer | Status |
|---|---|---|---|---|---|---|---|
| **FI-001** | opencode | tokenplan-mimo/mimo-v2.5-pro | ✅ 20 servers | swarm_ignite (engineer) | YELLOW | **L4 — Execution** | ✅ LIVE |
| **FI-002** | claude-code | deepseek-chat | ✅ 10 servers | swarm_ignite (engineer) | YELLOW | **L4 — Execution** | ✅ LIVE |
| **FI-003** | qwen-code | qwen | ❌ None | observer (3 tools) | LOW | **L4 — Execution** (bounded observer) | ⚠️ not connected (drift: missing from JSON registry — see §DRIFT) |
| **FI-004** | antigravity (CODING) | gemini-2.5-pro | ✅ 13 servers | swarm_ignite (analyst) | GREEN | **L4 — Execution** | ✅ LIVE (same name as Layer 2 antigravity — different model binding) |
| **FI-005** | codex | gpt-5.5 | ⚠️ MCP-ready | observer | YELLOW | **L4 — Execution** (bounded observer) | ⚠️ MCP unverified |
| **FI-006** | copilot | gpt-4o | ✅ 8 servers | init (analyst) | GREEN | **L4 — Execution** | ✅ LIVE |
| **FI-007** | aider | MiniMax-M3 | ❌ No | bridge mode | YELLOW | **L4 — Execution** | ✅ LIVE |
| **FI-008** | kimi-code | kimi | ✅ 9 servers | — | YELLOW | **L4 — Execution** | ✅ LIVE |
| **FI-009** | continue-cli | MiniMax-M3 | ✅ 17 servers | — | YELLOW | **L4 — Execution** | ✅ LIVE |
| **FI-010** | gemini-cli | gemini | (see JSON) | — | YELLOW | **L4 — Execution** | ✅ LIVE (drift: not in MD's earlier count — added 2026-06-26) |

---

## LAYER 4.2: HARNESS / BUILD AGENTS (1)

High-power agentic harnesses with native tool depth, advanced subagent parallelism, workflow orchestration, and external MCP surface. Session/ACP launched (not persistent daemons). Full F1-F13 binding via AGENTS.md + skills.

| ID | Model/Harness | Native MCP | Key Differentiators | Eureka Layer | Risk | Status |
|---|---|---|---|---|---|---|
| **grok-build** | Grok 4.3 (xAI Build TUI) | ✅ github(95) + geox(15) + wealth(24) + well(15) + native | Subagent (worktree isolation, capability modes, resume_from, personas); plan-mode; implement/design/execute-plan loops; scheduler+monitor; image/video; headless+ACP; rich .agents/skills (geox/arifos/cloudflare/pydantic/sbx); GitHub deep ops. **Skills enhanced post-reg (orthogonal mapping applied)**: plan-mode (Δ/F1-F4-F7), subagent-spawn (Ψ), mcp-federation (routing), autonomous-governed-execution (ΦΙ), arifos-arconstitutional-audit (ΦΙ/F1-F13), fff-loop-protocol (Forge/F1-F11), agentic-architecture (declaration). 12 skills now declared. | **L2/L3/L4** (cross-cutting orchestrator) | YELLOW | ✅ REGISTERED + ENHANCED 2026-06-22 (Phase 1 runtime activated) |

**Notes for grok-build:** Ephemeral harness (launch on demand). Strongest declared parallelism + orchestration in current registry. Routes federation via MCP federation skill. Self-known per 2026-06-23 CLAIM: model xai/grok-build-0.1 (256K), 3-stage plan→search→build + ≤8 agents, auto Claude MCP/skills ingest, SWE-Bench sys ~70.8%, tool err ~1.27%. See `/root/AAA/agents/grok-build/agent-card.json`, `AGENTS.md`, `TOOLS.md` + toolbench in AAA_AGENTS_REGISTRY.json.

---

## LAYER 4.5: ROLE AGENTS — Bounded C2/C3 Specialists (4)

> **Forged:** 2026-06-14 by FORGE (000Ω) — per Perplexity gap analysis.
> These agents operate within bounded leases. They observe, analyze, plan, propose — but execute only through the governed forge pipeline.

| ID | Class | Ring | Host Organs | Lease Max | Eureka Layer | Role Card |
|---|---|---|---|---|---|---|
| **Kernel Scribe** | C2 | SERVICE | arifOS, AAA | OBSERVE + PROPOSE | **L3 — Authority** (proposal) | `roles/KERNEL_SCRIBE.md` |
| **Ops Planner** | C2 | SERVICE | AAA, WEALTH, WELL | OBSERVE + PROPOSE | **L3 — Authority** (proposal) | `roles/OPS_PLANNER.md` |
| **Self-Forge Advisor** | C3 | Δ MIND | A-FORGE, arifOS | PROPOSE + MUTATE (gated) | **L3 — Authority** (proposal + bounded mutation) | `roles/SELF_FORGE.md` |
| **External Watcher** | C1 | SERVICE | AAA | OBSERVE only | **L2 — Governance** (observation) | `roles/EXTERNAL_WATCHER.md` |

**Communication Rule:** Role agents are SUBORDINATE to HEXAGON agents. They do not execute independently — they feed analysis and proposals to HEXAGON agents (333-AGI, 555-ASI, 888-APEX) for judgment and execution.

---

## LAYER 5: LEGACY — Deprecated/Spec-Only (3)

| ID | Reason | Superseded By | Eureka Layer | Status |
|---|---|---|---|---|
| **apex** | Memory engine. Deliberation moved to AAA a2a-server. | aaa-a2a (deliberation.ts) | (deprecated) | ⚠️ SPEC-ONLY |
| **maxhermes** | GEOX Earth specialist. **REMOVED 2026-06-22** — clarified as external MiniMax cloud product (see `external/maxhermes/`). | external/maxhermes (MiniMax cloud) | (deprecated) | ⚠️ ARCHIVED |
| **hermes-ops** | DevOps specialist. Tasks delegated to OpenClaw or claude-code. | openclaw / claude-code | (deprecated) | ⚠️ SPEC-ONLY |
| **aaa-architect** | Pre-HEXAGON ARoLE. | 333-AGI | (deprecated) | ❌ SUPERSEDED |
| **aaa-engineer** | Pre-HEXAGON ARoLE. | A-FORGE | (deprecated) | ❌ SUPERSEDED |
| **aaa-auditor** | Pre-HEXAGON ARoLE. | A-AUDIT + 888-APEX | (deprecated) | ❌ SUPERSEDED |

---

## AGENT COUNT (revised 2026-06-26 per SCAR-13)

| Layer | Count | Category | Status |
|---|---|---|---|
| HEXAGON (Constitutional) | 6 | TRUE AGENTS (L3) | 5 SPEC + 1 LIVE (opencode warga 2026-06-26) |
| RUNTIME (Live Services) | 4 | TRUE AGENTS (L3-L4) | LIVE |
| INFRASTRUCTURE (Organs) | 6 | **CAPABILITY REGISTRIES (NOT agents)** | LIVE |
| ROLE AGENTS (Specialists) | 4 | TRUE AGENTS (bounded, L2-L3) | SPEC (role cards forged 2026-06-14) |
| CODING (Forge Instruments) | 10 | TRUE AGENTS (L4) | 8 LIVE, 2 unverified |
| LEGACY (Spec-Only) | 6 | LEGACY SPECS | DEPRECATED |
| **TOTAL TRUE AGENTS** | **24** | (+1 opencode warga) | |
| **TOTAL CAPABILITY REGISTRIES** | **6** | | |
| **TOTAL LEGACY** | **6** | | |
| **GRAND TOTAL** | **36** | (was 35 — opencode promoted to HEXAGON warga) | |

> **Count reconciliation:** Previous MD claimed 27 total / 23 active. New count = 23 true agents + 6 registries + 6 legacy = 35 entries. The +8 difference is: (a) gemini-cli newly added to MD (was in JSON only), (b) antigravity runtime binding is now explained explicitly alongside the canonical FI citizen, (c) legacy expanded from 3 to 6 (aaa-architect/engineer/auditor were previously summarized).

---

## SOVEREIGN

| ID | Role | Eureka Layer |
|---|---|---|
| **000-SALAM** | Muhammad Arif bin Fazil — Human Sovereign, F13 final veto. NOT an agent. | **L0 — Sovereign** |

---

## CANONICAL FILES

| File | Purpose |
|---|---|
| `AGENT_REGISTRY.md` | **This file** — human-readable canonical index (now with SCAR-13 disambiguation) |
| `ROOT_AGENT_CONFIG.yaml` | Root config for AAA warga, peers, forge instruments, and config pointers |
| `HEXAGON.yaml` | Constitutional agent topology (5 agents, pipeline) |
| `AAA_AGENTS_REGISTRY.json` | Machine-readable registry (v2.0.0) — **drift noted, see §DRIFT** |
| `CODING_AGENT.md` | Forge instrument reference (8 agents, 97 tools) |
| `a2a-server/agent-cards/` | A2A discovery cards (JSON-LD) |
| `/root/arifOS/arifosmcp/config/model_registry.json` | **Substrate registry** (LLM models — NOT agents) |

---

## §SCAR-13 — AGENT_REGISTRY CATEGORY ERROR (FULL TEXT)

> **Canonical specification:** [`/root/AAA/specs/AAA_AGENT.md`](../specs/AAA_AGENT.md) (v1.0 DRAFT, 278 lines, pending 999_SEAL after F13 review).
> This file is the **operational index**. The spec is the **formal definition**.

> **Forged:** 2026-06-26
> **Trigger:** While drafting Agent Ontology v1.0 to clarify IBM AssetOpsBench's four-fold confusion of "agent," checked arifOS's own `AGENT_REGISTRY.md` and found the same four-fold conflation.
>
> **Findings:**
> 1. 6 organs (arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA) are listed as "agents" when they are sovereign capability registries — they host agents but do not loop themselves in the arifOS-native sense.
> 2. `antigravity` appears in both Layer 2 (runtime binding, Gemini 3.5) and Layer 4 (canonical CODING citizen, Gemini 2.5-pro/Google harness lineage) — same citizen, two described operational bindings, now explicitly labeled.
> 3. 888-APEX is classified as a HEXAGON warga in this file but as a constitutional organ in `arifOS/AGENTS.md`. The same entity, two classifications.
> 4. MD and JSON registries disagree on 3 entries (qwen-code, gemini-cli, 777-forge).
> 5. The file name `AGENT_REGISTRY` is itself a category error from the pre-HEXAGON era. The proper file should be `FEDERATION_REGISTRY.md` (or split into 3 files per Option A).
>
> **Fixes applied (this commit):**
> - Disambiguation banner at top of file
> - `Eureka Layer` column added to every table
> - INFRASTRUCTURE layer explicitly reclassified as "Capability Registries (NOT agents)"
> - Registry drift notice
> - Revised count showing 23 true agents + 6 registries + 6 legacy
>
> **Fixes pending (Option A — F13-gated):**
> - Rename `AGENT_REGISTRY.md` → `FEDERATION_REGISTRY.md`
> - Split into `agents/`, `organs/`, `substrates/` subdirectories
> - Reconcile JSON registry drift
> - Move 888-APEX classification clarification into both AAA and arifOS canonical files
>
> **Why this matters:** SCAR-12 established that the federation has the four-layer separation in architecture (substrate, governance, authority, execution). SCAR-13 reveals that the separation is **not yet enforced at the naming/documentation layer**. Naming IS the architecture at the doc layer — until `AGENT_REGISTRY.md` no longer mislabels organs as agents, the eureka is incomplete.
>
> **Lineage:** SCAR-13 extends SCAR-12 (Table 2 Eureka). Together they form the "Naming as Architecture" pair: SCAR-12 = four organs separated; SCAR-13 = four-fold confusion extended even into the canonical registry.

---

## §SCAR-13 — APPENDIX: The Four-Fold Confusion (Excerpt)

The agentic AI literature uses "agent" to mean at least 4 incompatible things:

| Usage | Meaning | Example |
|---|---|---|
| (a) LLM with prompt | Model + role description | "You are the IoT specialist" |
| (b) LLM with tools | (a) + function-calling | LLM that can call `get_sensors()` |
| (c) LLM in loop | (b) + ReAct-style multi-step | LLM that calls tool → reads → calls another |
| (d) LLM-wrapped-as-callable | (c) exposed via interface | IoT agent that supervisor calls like a function |

**arifOS-native definition (SCAR-12, SCAR-13):**

> An **agent** is a loop over (Model × Tools × State × Goal) that terminates in a **constitutional verdict**. The verdict (SEAL / HOLD / VOID / SABAR) is the defining property — without it, the loop is plumbing.

**Application to this registry:**

- HEXAGON warga: TRUE agents (have loops + sealed verdicts)
- RUNTIME services: TRUE agents (hermes-asi loops over Telegram + LLM + sealed message receipts)
- CODING federation: TRUE agents (each loops over LLM + 97 tools + sealed commit receipts)
- ROLE agents: TRUE agents (bounded but still loops with sealed proposals)
- INFRASTRUCTURE organs: NOT agents (capability registries, no top-level loop)
- LEGACY specs: NOT agents (no runtime)

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

## 2026-06-22 — FI Citizens Skills Binding Sweep

Wired 10 FI citizens as real AAA warga with 8-skill baseline (per orthogonal mapping pattern):

| Citizen | Skills | Binary | Mirror |
|---------|--------|--------|--------|
| opencode | 8 | opencode | a2a-server/agent-cards/opencode.json |
| claude-code | 8 | claude | a2a-server/agent-cards/claude-code.json |
| codex | 8 | codex | a2a-server/agent-cards/codex.json |
| qwen-code | 8 | qwen | a2a-server/agent-cards/qwen-code.json |
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
6. 070-lock-humility-godel
7. github-workflow
8. arifos-mcp-federation

Pattern reference: `/root/HERMES/skills/aaa-agentic-governance/references/orthogonal-skill-binding-pattern-2026-06-22.md`

**Receipt:** `/root/AAA/artifacts/FI_WARGA.md`

---

## OPTION A — Proposed Split (PENDING F13 ACK)

If Arif approves the rename + split (estimated 4 hours, T3 888_HOLD), the new structure becomes:

```
/root/AAA/
├── FEDERATION_REGISTRY.md           (top-level index — replaces AGENT_REGISTRY.md)
├── agents/
│   ├── HEXAGON.md                   (5 warga — L3)
│   ├── RUNTIME.md                   (4 services — L3-L4)
│   ├── CODING_FEDERATION.md         (10 forge instruments — L4)
│   ├── ROLE_AGENTS.md               (4 specialists — bounded L2-L3)
│   └── LEGACY.md                    (historical)
├── organs/
│   └── ORGANS.md                    (6 capability registries — NOT agents)
├── substrates/
│   └── SUBSTRATES_POINTER.md        (→ /root/arifOS/arifosmcp/config/model_registry.json)
├── registries/
│   ├── AAA_FEDERATION_STATE.yaml
│   ├── AAA_AGENTS_REGISTRY.json     (reconciled drift)
│   ├── SUBSTRATE_GATE_POLICY.yaml
│   └── ... (existing)
├── HEXAGON.yaml                     (unchanged)
├── ROOT_AGENT_CONFIG.yaml           (unchanged)
└── ... (rest unchanged)
```

**Migration checklist (Option A):**
- [ ] Backup current `AGENT_REGISTRY.md` → `AGENT_REGISTRY.md.deprecated-2026-06-26`
- [ ] Create new `FEDERATION_REGISTRY.md` with three-bucket TOC
- [ ] Split content into `agents/`, `organs/`, `substrates/` subdirectories
- [ ] Reconcile JSON registry: add qwen-code, gemini-cli, 777-forge (or drop from MD)
- [x] Disambiguate antigravity prose: one canonical FI citizen + one runtime binding note
- [ ] Update `AAA/AGENTS.md` cross-references to point to new structure
- [ ] Update `arifOS/AGENTS.md` cross-references (888-APEX classification)
- [ ] Update A2A discovery card paths
- [ ] 999_SEAL the rename in VAULT999

**Reversibility:** Backups exist at `.bak-2026-06-26-pre-scar13` and `.deprecated-2026-06-26`. Full rollback possible.

---

*SCAR-13 sealed 2026-06-26 — DITEMPA BUKAN DIBERI*
*If you change this file, update the SOT-MANIFEST block first.*
*Next: 999_SEAL Option A split pending Arif ack.*
