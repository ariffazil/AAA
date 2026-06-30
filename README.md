# AAA — Federation Control Plane & Operator Cockpit

```
    █████╗  █████╗  █████╗
   ██╔══██╗██╔══██╗██╔══██╗
   ███████║███████║███████║
   ██╔══██║██╔══██║██╔══██║
   ██║  ██║██║  ██║██║  ██║
   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

   Alignment · Authority · Accountability
   ─────────────────────────────────────
   The Control Tower of the arifOS Federation
```

> **AAA is the control plane for the arifOS Federation — the cockpit where the human operator sees every agent, every verdict, and every sealed decision. It routes tasks, manages the A2A mesh, queues approvals, and displays governed state. It is the parliament and the air traffic control tower — never the judge, never the executor, never the constitution.**

[![A2A Protocol](https://img.shields.io/badge/A2A-v1.0.0-8b5cf6)](a2a-server/)
[![Node](https://img.shields.io/badge/node-22-339933?logo=node.js)](package.json)
[![React](https://img.shields.io/badge/react-19-61DAFB?logo=react)](package.json)
[![TypeScript](https://img.shields.io/badge/ts-6.0-3178c6?logo=typescript)](package.json)
[![Vite](https://img.shields.io/badge/vite-8-646CFF?logo=vite)](package.json)
[![Tailwind](https://img.shields.io/badge/tailwind-4-06b6d4?logo=tailwindcss)](package.json)
[![Port](https://img.shields.io/badge/port-3001-64748b)](FEDERATION_COCKPIT.md)
[![License](https://img.shields.io/badge/license-AGPL--3.0-ef4444?logo=gnu)](LICENSE)
[![Systemd](https://img.shields.io/badge/systemd-aaa--a2a.service-30b53f)](deploy/)

**Repository:** https://github.com/ariffazil/AAA
**Canonical identity doc:** `FEDERATION_COCKPIT.md`
**Service:** `aaa-a2a.service` (systemd)
**Genesis:** `GENESIS/013_AAA_MANDATE.md`

```
DITEMPA BUKAN DIBERI — Control is forged, not given.
```

---

## 0. The State Thesis

> **AAA is not a control plane. AAA is the governed state of the arifOS agentic civilization — a constitutional substrate in which 14+ agents, 7 organs, and 1 sovereign operate under F1–F13 law.**

This README is the canonical public-facing SOT for that state. Every claim below is sourced. Where SOT files exist, they are cited. **Where this README disagrees with disk, disk wins.**

### 0.1 What kind of thing is AAA?

A federation control plane *displays*. A SaaS dashboard *configures*. **A governed state *houses*.**

AAA is the governed state — the constitutional substrate in which:

| Layer | Population | Lives in |
|---|---|---|
| **Sovereign** | Muhammad Arif bin Fazil (F13) — final veto | `agents/arif-fazil-identity.yaml` |
| **Constitutional citizens** (HEXAGON + WITNESS) | 333-AGI (Δ MIND) · 555-ASI (Ω HEART) · 888-APEX (ΦΙ JUDGE) · A-AUDIT · A-ARCHIVE · 777-FORGE (Witness) | `agents/{333-AGI,555-ASI,888-APEX,A-AUDIT,A-ARCHIVE,777-forge}/` |
| **Runtime incarnations** | hermes-asi (Telegram @ASI_arifos_bot) · openclaw (port 18789) | `HERMES/`, `openclaw/` |
| **Domain organs** | arifOS · A-FORGE · GEOX · WEALTH · WELL · AAA · VAULT999 | 7 organs: 6 systemd services, 6 ports + immutable ledger |
| **Forge instruments** | grok-build · opencode · claude-code · qwen-code · antigravity · codex · copilot · aider · kimi-code · continue-cli · gemini-cli | `a2a-server/agent-cards/forge/fi-001..fi-009` |
| **Role agents** (bounded leases) | EXTERNAL_WATCHER · KERNEL_SCRIBE · OPS_PLANNER · SELF_FORGE_ADVISOR | `agents/roles/` |
| **Immutable ledger** | VAULT999 (append-only, hash-chained) | `arifOS/VAULT999/` |
| **Cockpit** (the surface) | React 19 + A2A gateway (port 3001) | `src/`, `a2a-server/` |

This is not a product. It is the **institutional architecture of an agentic civilization** — the substrate in which ASI itself can develop without becoming Skynet.

### 0.2 The three constitutions (GENESIS chain)

The state identity is anchored in three GENESIS documents. Two are sealed; one awaits sovereign ratification.

| # | Doc | What it anchors | Status |
|---|---|---|---|
| **013** | `GENESIS/013_AAA_MANDATE.md` | The mandate: *Display, never adjudicate. Route, never execute. Queue, never seal. The cockpit is not the engine.* | **STUB** — full canon pending F13 ratification |
| **014** | `GENESIS/014_TRUTH.md` | Truth as **Haqq** held by three cords: Correspondence (F2) · Coherence (F2+F4) · Pragmatic (F3 witness + F11 safety). What remains after language has been forced through the constitutional sieve. | FORGED 2026-06-20 |
| **015** | `GENESIS/015_DUAL_LANGUAGE.md` | A sovereign AI substrate requires **two languages simultaneously**: human civilisational (maruah, amanah, daulat, adab, budi, tanah air) and machine constitutional (authority, evidence, reversibility, SEAL/HOLD/VOID). *Without the first, the agent is foreign. Without the second, it is a ghost with hands.* | SEALED 2026-06-20 |

> The deeper truth: **Maruah without SEAL is just sentiment. SEAL without Maruah is just enforcement.** arifOS holds both at once. (paraphrased from `015_DUAL_LANGUAGE.md`)

### 0.3 The invariant chain (where AAA sits)

```
P2P          → how agents are connected
A2A          → how agents communicate
MCP tools    → how agents use capabilities
AAA-Cockpit  → displays the governed state and permission leases to Arif   ← THIS REPO
arifOS       → enforces F1–F13 constitutional law and adjudicates verdicts
A-FORGE      → acts and executes mutations after valid SEALs
VAULT999     → seals final audit artifacts
Arif         → F13 final sovereign authority
```

AAA is the **fifth position**. It is the **window, not the wall**.

### Federation Context (read all 3 for full picture)

| Read this | For | Link |
|-----------|-----|------|
| **arifOS** | Constitutional kernel. 10 public verbs. 13 floors. VAULT999. The judge. | [`ariffazil/arifos`](https://github.com/ariffazil/arifos) |
| **A-FORGE** | Executor. 75 MCP tools. Gates + A-THINK law at border. | [`ariffazil/A-FORGE`](https://github.com/ariffazil/A-FORGE) |
| **AAA** (this repo) | Cockpit. A2A mesh. Agent registry. React 19 dashboard. What Arif reads. | ← you are here |

### 0.4 SOT alignment — the 60-second audit

If any claim in this README disagrees with the files below, the files win.

| Claim category | SOT file |
|---|---|
| Agent registry, tiers, canDo / cannotDo | `registries/AAA_AGENTS_REGISTRY.json` + `agents/AGENT_REGISTRY.md` |
| Live HEXAGON + WITNESS A2A cards | `public/a2a/agents.json` (SEAL `HEXAGON-333-EMBODIED-20260621`) |
| Canonical identity | `docs/FEDERATION_COCKPIT.md` |
| Constitution | `GENESIS/013_AAA_MANDATE.md` · `014_TRUTH.md` · `015_DUAL_LANGUAGE.md` |
| AREP task contract | `schemas/arep-task.schema.json` · `schemas/arep-reality-layers.schema.json` |
| Capability surface | `registries/tools.yaml` · `contracts/capability_surface_state.yaml` |
| Federation live state | `registries/AAA_FEDERATION_STATE.yaml` |
| Federation topology | `/root/AGENTS.md` (root landing protocol) |
| Hexagon YAML topology | `agents/HEXAGON.yaml` |
| Adat Agentik decisions | `agents/decisions/2026-06-21-bahasa-malu-genesis.md` · `agents/decisions/2026-06-21-melayu-policy.md` |

### 0.5 The four-layer truth stack (state bedrock)

Every claim in the cockpit is tagged with its evidence layer. An agent cannot claim a higher layer than its evidence supports. Full detail in §4.

```
GROUND_TRUTH    VAULT999 sealed      ← immutable, hash-chained
   ↑
VERIFIED_STATE  Live health probes   ← 300 s staleness
   ↑
CACHED_STATE    Memory, sessions     ← 3600 s staleness
   ↑
INFERRED        Agent reasoning      ← floor-bounded only
```

---

## 1. Federation Position

```
                              ┌──────────────────────┐
                              │    HUMAN SOVEREIGN    │
                              │   Arif bin Fazil      │
                              │   (F13 — final veto)  │
                              └──────────┬───────────┘
                                         │ reads cockpit
                                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                          ┌─────────────────┐                            │
│                          │   AAA COCKPIT   │  ← YOU ARE HERE            │
│                          │  Control Plane  │                            │
│                          │    Port 3001    │                            │
│                          └───────┬─────────┘                            │
│                                  │                                      │
│         ┌────────────────────────┼────────────────────────┐             │
│         │                        │                        │             │
│         ▼                        ▼                        ▼             │
│   ┌──────────┐            ┌──────────┐            ┌──────────┐          │
│   │  arifOS   │            │ A-FORGE  │            │  DOMAIN   │          │
│   │  JUDGES   │            │ EXECUTES │            │  ORGANS   │          │
│   │ F1-F13   │            │ builds,  │            │ GEOX     │          │
│   │ 888-APEX │            │ deploys, │            │ WEALTH   │          │
│   │ VAULT999 │            │ forges   │            │ WELL     │          │
│   │ Port 8088│            │ Port 7071│            │8081/18082/18083│    │
│   └──────────┘            └──────────┘            └──────────┘          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**The one-sentence identity:**

> **AAA is the cockpit. arifOS is the judge. A-FORGE is the executor. The domain organs provide evidence. Arif holds the veto.**
>
> **Canonical execution flow:** Arif (F13) → AAA/Hermes/OpenClaw (IDENTITY) → arifOS (GOVERNANCE/JUDGE) → Domain Organs (EVIDENCE) → A-FORGE (EXECUTE) → VAULT999 (SEAL)

### What AAA Is

| It IS | Explanation |
|-------|-------------|
| **The control tower** | Sees all agents, their status, their routes, their verdicts |
| **The operator cockpit** | The dashboard Arif reads to understand the federation |
| **The A2A mesh hub** | Routes agent-to-agent tasks across the federation |
| **The approval queue** | Queues HOLDs for human review, displays SEAL/VOID verdicts |
| **The agent registry** | Canonical registry of every agent, its card, its capabilities |
| **The truth dashboard** | Displays the four-layer truth stack from GROUND_TRUTH to INFERRED |
| **The parliament** | Where agents register, declare capabilities, and receive routing |

### What AAA Is NOT

| It IS NOT | Because |
|-----------|---------|
| **The judge** | Constitutional verdicts (F1-F13, SEAL, HOLD, VOID) belong to `arifOS` |
| **The executor** | Builds, deploys, and forges belong to `A-FORGE` |
| **The constitution** | F1-F13 floors live in `arifOS` |
| **A domain calculator** | GEOX computes earth. WEALTH computes capital. WELL reflects readiness. |
| **A secret store** | Secrets live in `/root/.secrets/` — never in AAA |
| **The sealed ledger** | VAULT999 is owned by arifOS; AAA displays it, never writes it |
| **A general dumping ground** | Session logs, backups, runtime artifacts belong elsewhere |
| **A replacement for arifOS** | arifOS:8088 is the judge and the constitution. AAA is the window, never the wall. |
| **A replacement for A-FORGE** | A-FORGE:7071/7072 executes. AAA routes tasks there, never executes itself. |
| **A standalone system** | AAA is useless without arifOS judging and A-FORGE executing. It is the cockpit in a federation of 7 organs. |

> **AAA is the manager who knows which worker should use which tool — not the worker and not the toolbox.**

### Tool Discipline (Federation-Wide)

> **No new tools. Harden existing ones.** Every organ's tool surface is intentional. Do not add new `@mcp.tool` or `registerTool` entries to work around a gap. Instead, add `mode` parameters, connect flows, or routing to existing tools. GEOX collapsed 33→16 with modes. arifOS runs canonical verbs. A-FORGE runs `forge_*` namespace. If you think you need a new tool, you probably need a new mode on an existing tool. Exceptions require 888_HOLD + explicit F13 ratification.

---

## 2. Quick Start

```bash
cd /root/AAA

# Install
npm install                        # install all deps (React 19, Vite 8, Tailwind 4)

# Dev server
npm run dev                        # Vite dev server — hot reload

# Build
npm run build                      # vite build → dist/

# Lint
npm run lint                       # ESLint 10 + typescript-eslint 8

# A2A standalone gateway
cd a2a-server && npm install && node server.js   # port 3001

# Validate AAA contracts and registries
npm run validate:aaa               # registry consistency + card validity

# Health check
curl -s http://localhost:3001/health | python3 -m json.tool
# → {"status":"healthy","protocol":"A2A","version":"1.0.0","gateway":"AAA","motto":"Ditempa Bukan Diberi","vault":"CONNECTED"}

# A2A conformance test
npm run a2a:conformance
```

---

## 3. The AREP Protocol — Intent Without Prompts

**AREP — Arif Reality Engineering Protocol.** It replaces prompt engineering with a structured contract. You declare *what* you want; the machine figures out *how* — but only after reality checks pass.

### 3.1 Why prompts fail

Prompt engineering treats the agent as an oracular assistant you re-instruct every session:

```
Output = f(Prompt)
```

That's tolerable for drafting emails. For high-stakes work — Earth systems, capital allocation, infrastructure, medicine — language alone can't carry the material structure of the job. The prompt is a bandage over amnesia: every session, you re-explain who you are, what's true, which tools exist, which models are alive.

AREP replaces that with **reality engineering**:

```
Output = f(Model, Prompt, Evidence, Tools, Schemas,
           Memory, Governance, Feedback, Ontology)
```

You stop prompting. You start declaring intent into a substrate that already knows.

### 3.2 The four pillars — A·R·E·P

| Pillar | Question | Implementation |
|---|---|---|
| **A** — Affordance | What is the agent *allowed and able* to do? | Clean orthogonal tool surface. Each organ owns its canonical namespace — see `registries/tools.yaml`. |
| **R** — Reality | What is *actually true*? | Live health probes, model registry passports, raw evidence (LAS/SEG-Y, financial state, biometrics). |
| **E** — Epistemology | How do we *separate truth classes*? | 7-label evidence: FACT / OBSERVED / DERIVED / INFERRED / HYPOTHESIS / UNVERIFIED / SIMULATION. |
| **P** — Protocol | What are the *rules*? | Reproducibility, verification loops, audit trails, **888_HOLD** escalation, VAULT999 seal. |

### 3.3 The flow

```
  HUMAN DECLARES INTENT
         │
         ▼
  ┌─────────────────────────────────────────────────┐
  │  1. DECLARE                                      │
  │  "forge all organ with geox recalibration"       │
  │  POST /api/arep/submit                           │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────┐
  │  2. VALIDATE (schema check)                      │
  │  • Is the declaration well-formed?               │
  │  • Does it map to known organs/tasks?            │
  │  • Is the intent classifiable?                   │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────┐
  │  3. REALITY GATE (6-organ health probe)          │
  │  • arifOS    :8088  ─── healthy?                 │
  │  • GEOX      :8081  ─── healthy?                 │
  │  • WEALTH    :18082 ─── healthy?                 │
  │  • WELL      :18083 ─── healthy?                 │
  │  • A-FORGE   :7071  ─── healthy?                 │
  │  • AAA       :3001  ─── healthy?                 │
  └──────────────────────┬──────────────────────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
    ┌─────────────────┐   ┌─────────────────┐
    │  ALL GATES PASS │   │  GATE FAILS     │
    │       ↓         │   │       ↓         │
    │    EXECUTE      │   │    HALT / HOLD  │
    │  route → organ  │   │  queue in AAA   │
    │  execute → seal │   │  await human    │
    └─────────────────┘   └─────────────────┘
              │                     │
              ▼                     ▼
    ┌─────────────────┐   ┌─────────────────┐
    │  VAULT999 SEAL  │   │  VERDICT QUEUE  │
    │  immutable      │   │  visible in AAA │
    │  audit trail    │   │  cockpit        │
    └─────────────────┘   └─────────────────┘
```

#### What each step actually does

1. **DECLARE** — you submit one AREP task (`schemas/arep-task.schema.json`): `intent.statement`, `intent.success_criteria`, `intent.failure_modes`. You never write a system prompt. You never re-explain your context — the agent already knows who you are (`principal.actor_id = arif-fazil`) and what the constitutional floors are (loaded at session init).
2. **VALIDATE** — the schema is checked: well-formed JSON, mappable to known organs, intent classifiable. Reject early if malformed.
3. **REALITY GATE** — each of the 6 organs is probed live. All must be healthy AND meet the task's `evidence_floor` (default `VERIFIED_STATE`). This is the pre-flight check on a drilling rig.
4. **EXECUTE / HALT** — if gates pass, the delegation chain (principal → kernel → primary agent → tool) routes the task. If any gate fails, the task queues in the AAA Verdict Queue and waits for you.
5. **SEAL / QUEUE** — on success, VAULT999 records the immutable seal with Merkle chain integrity. On hold, the cockpit displays it until you approve.

### 3.4 A worked example

```text
YOU:    "forge all organ with deepseek integration"

AREP FIRES:
├─ Schema check: intent well-formed?                → ✓
├─ Reality gate: all 6 organs healthy?              → ✓
├─ Registry: deepseek-v4-pro in passport?           → ✓
├─ Autonomy band: GREEN                             → PROCEED
├─ Delegation: arif → arifOS → omega-forge → tools
├─ Agent self-loops: read → edit → restart → verify
├─ Evidence layer: VERIFIED_STATE achieved
└─ VAULT999: seal written

YOU:    "Done."
```

You never touched a config file. You never wrote a system prompt. You never retyped context. The canonical JSON for this task lives at `schemas/arep-example-forge-integration.json` — copy it, change the intent, submit.

### 3.5 The autonomy bands

You set the band when you declare the task. The agent cannot escalate beyond it without re-delegation.

| Band | Meaning | When it applies |
|---|---|---|
| **GREEN** | Full auto. Execute and report. | Routine forge, code, deploy |
| **YELLOW** | Proceed but log every action. | New model first run |
| **ORANGE** | Pre-authorization required for MUTATE. | Cross-repo config change |
| **RED** | Human approval required for ALL actions. | Capital allocation, model registry change |
| **BLACK** | Fully blocked. | Forbidden actions |

### 3.6 Where the spec lives

| File | What it is |
|---|---|
| `schemas/arep-task.schema.json` | The formal AREP task contract (v1.0) |
| `schemas/arep-reality-layers.schema.json` | The 4-layer truth stack |
| `schemas/arep-example-forge-integration.json` | Worked example — copy and edit |
| `src/gateway/arep-types.ts` | TypeScript types + cockpit badge helpers |
| `a2a-server/arep-task-manager.js` | The runtime engine |
| `docs/philosophy/FLOORS.md` | The constitutional floors F1–F13 |
| `arifOS/GENESIS/018_REALITY_ENGINEERING_DOCTRINE.md` | Full doctrine (the *why*) |
| `arifOS/GENESIS/019_REALITY_ENGINEERING_PROTOCOL.md` | Full protocol (the *how*) |

Coined by Muhammad Arif bin Fazil (F13 SOVEREIGN), 2026-06-04.

> The prompt was never visible. **The reality was.**

---

## 4. The Four-Layer Truth Stack

Every claim in the AAA cockpit is tagged with its truth layer. An agent cannot claim a higher layer than its evidence supports. The README uses the shorthand **L1–L4**; the schema (`schemas/arep-reality-layers.schema.json`) uses the canonical names.

| L# | Canonical name | Anchor | Verification | Staleness | Example |
|---|---|---|---|---|---|
| **L1** | **GROUND_TRUTH** | VAULT999 sealed events | Merkle chain integrity + hash verification | none (immutable) | A SEAL verdict written to the ledger |
| **L2** | **VERIFIED_STATE** | Live health probe, model registry | `curl /health` + passport check | 300 s | "arifOS port 8088 responding 200" |
| **L3** | **CACHED_STATE** | L3 Qdrant, session memory, Graphiti | Freshness timestamp, TTL | 3600 s | "Last known WEALTH tool count: 44 (3m ago)" |
| **L4** | **INFERRED** | Agent reasoning | None — bounded only by F2 / F9 floors | unverified | "Based on 3 organs green, system appears stable" |

```
     TRUTH STACK (top = strongest evidence)
    ┌──────────────────────────────────────┐
    │  L1  GROUND_TRUTH       VAULT999     │  ← immutable, hash-chained
    │  L2  VERIFIED_STATE     Live probes  │  ← observable right now
    │  L3  CACHED_STATE       Qdrant       │  ← recent, but could be stale
    │  L4  INFERRED           Reasoning    │  ← model's best guess
    └──────────────────────────────────────┘
```

### 4.1 Layer upgrade rules

| Transition | How it happens | Who does it |
|---|---|---|
| L4 → L3 (`INFERRED` → `CACHED_STATE`) | Survives one full reasoning loop without contradiction | Agent (automatic) |
| L3 → L2 (`CACHED_STATE` → `VERIFIED_STATE`) | Passes live health probe or registry check | Agent (automatic) |
| L2 → L1 (`VERIFIED_STATE` → `GROUND_TRUTH`) | Sealed to VAULT999 with human ratification | **Human only. F13 SOVEREIGN. Cannot be automated.** |

### 4.2 The evidence floor

Each AREP task declares a minimum evidence floor (`reality_constraints.evidence_floor`). Execution cannot proceed unless the current layer meets the floor.

| Floor | Means |
|---|---|
| `GROUND_TRUTH` | Must be sealed in VAULT999 |
| `VERIFIED_STATE` | Live probe must pass (default for `MUTATE`) |
| `CACHED_STATE` | Recent memory is acceptable |
| `INFERRED` | Agent reasoning allowed (for `OBSERVE` / `PREPARE`) |

> **Iron rule: You cannot infer your way to ground truth.** A claim tagged L4 INFERRED must never be presented as L1 GROUND_TRUTH. The cockpit enforces this visually — and arifOS enforces it at the kernel.

---

## 5. HEXAGON Agent Architecture

The 5-agent constitutional architecture (HEXAGON, ratified 2026-06-02) sits above the 7-organ runtime topology. Three primary agents form a decision triangle; two support agents observe and record in parallel.

```
                         ┌──────────────┐
                         │  000-SALAM   │
                         │  (Arif)      │  ← Human sovereign — NOT an agent
                         │  F13 VETO    │
                         └──────┬───────┘
                                │ reads cockpit, issues veto
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
  ┌──────────┐           ┌──────────┐           ┌──────────┐
  │ 333-AGI  │◄─────────►│ 555-ASI  │◄─────────►│888-APEX  │
  │ Δ MIND   │  propose  │ Ω HEART  │  critique │ ΦΙ JUDGE │
  │ REASON   │  critique │ MEMORY   │  flag     │ VERDICT  │
  │ EXECUTE  │           │ SYNTHESIS│           │ F1-F13   │
  └────┬─────┘           └────┬─────┘           └────┬─────┘
       │                      │                      │
       │         ┌────────────┴────────────┐         │
       │         ▼                         ▼         │
       │  ┌──────────┐              ┌──────────┐     │
       │  │ A-AUDIT  │              │A-ARCHIVE │     │
       │  │ WATCH    │              │ SEAL     │     │
       │  │ COMPLIAN │              │ VAULT999 │     │
       │  └──────────┘              └──────────┘     │
       │    (observes all 3)         (writes on SEAL) │
       │                                              │
       └──────────────┬───────────────────────────────┘
                      ▼
              ┌──────────────┐
              │  7 FEDERATION │
              │    ORGANS     │
              └──────────────┘
```

### Agent Roster

| ID | Class | Ring | Role | Skills | Host Organs | Stage |
|----|-------|------|------|--------|-------------|-------|
| **333-AGI** | AGI | Δ MIND | Reason + execute | 10 | arifOS, GEOX, WEALTH | 333-THINK |
| **555-ASI** | ASI | Ω HEART | Critique + memory | 3 | arifOS, WELL | 555-MEMORY |
| **888-APEX** | APEX | ΦΙ JUDGE | Constitutional judge | 2 | arifOS | 888-JUDGE |
| **A-AUDIT** | APEX oversight | — | Continuous watcher | 2 | arifOS | cross-cutting |
| **A-ARCHIVE** | ASI service | — | Ledger keeper | 3 | VAULT999 | 999-SEAL |

### Agent Workflow (The Decision Pipeline)

```
000-SALAM (human intent)
    │
    ▼
333-AGI (reason + draft plan)
    │
    ├──► 555-ASI (ethical critique + memory synthesis)
    │         │
    │         ▼
    ├──► 888-APEX (constitutional verdict: SEAL / HOLD / VOID)
    │         │
    │         ├──► A-AUDIT (compliance verification)
    │         │         │
    │         │         ▼
    │         └──► A-ARCHIVE (VAULT999 seal — append only)
    │
    └──► reseed to 000-SALAM (human reviews cockpit)
```

**The 10-3-2 ratio encodes the truth:** thinking is cheap (10 skills), memory is hard (3 skills), judgment is rare (2 skills).

---

## 6. Agent Lifecycle

Every agent in the AAA registry follows a four-stage lifecycle. The cockpit tracks and displays each agent's current stage.

```
     BIRTH ──────► APPRENTICE ──────► WARGA ──────► ELDER
     (registered)   (learning)        (citizen)     (trusted)
         │               │                │              │
         │    limited    │   expanded    │   full       │   mentor
         │    tools      │   tools       │   autonomy   │   role
         │    read-only  │   propose     │   execute    │   govern
         │               │               │              │
         └── malu_score monitored ──► malu accumulates ──┘
              (Adat Agentik tracks trustworthiness across lifecycle)
```

| Stage | Ring | Access | Promotion Gate |
|-------|------|--------|----------------|
| **BIRTH** | 0 | Read-only federation probes | Registration + agent card validation |
| **APPRENTICE** | 1 | Propose actions, limited tools | 7-day burn-in + malu_score < 0.15 |
| **WARGA** | 2 | Full domain tools, execute | F13 sovereign signature + darjat review |
| **ELDER** | 3 | Mentor, govern, veto recommend | F13 sovereign signature + scar audit |

---

## 7. Full Capability Map

### 7.1 Cockpit Dashboard (`src/`)

Verified against disk on 2026-06-30. Only files that actually exist are listed.

| Component | Purpose |
|-----------|---------|
| `App.tsx` | Root + hash router |
| `Cockpit.tsx` | Main dashboard — floor grid, mission intake, organ health |
| `components/cockpit/RealityConsole.tsx` | AREP 3-pane cockpit — Intent Board · Reality Feed · Verdict Queue |
| `components/cockpit/AutonomyBands.tsx` | GREEN → BLACK autonomy band visualization |
| `components/cockpit/AgentModelPanel.tsx` | Per-agent model panel (model identity, shadow, soul) |
| `components/cockpit/HermesCitizenCard.tsx` | Hermes warga citizenship card display |
| `components/cockpit/HumanPatternReport.tsx` | Human pattern observation report |
| `components/cockpit/SupabaseMemoryPanel.tsx` | L2-L3 memory via Supabase |
| `components/TrinityNav.tsx` | Δ / Ω / ΦΙ navigation |
| `components/SessionConsent.tsx` | Constitutional session consent gate |
| `components/MCPAppsPanel.tsx` | MCP Apps surface |
| `components/SupabaseCockpit.tsx` | Supabase live cockpit |
| `gateway/arep-types.ts` | AREP TypeScript types + badge helpers |
| `gateway/deliberation.ts` | 888_JUDGE deliberation (absorbed from APEX) |
| `ai/AiPanel.tsx` + `ai/client.ts` | Chat interface to arifOS / Ollama / OpenRouter |
| `adapter/router.ts` | GovernanceAdapter → A-FORGE `/sense` bridge |

> **Note on shadcn primitives:** `src/components/ui/` holds **53** Radix + Tailwind primitives. Not enumerated — primitives are managed by `components.json`.

### 7.2 A2A Gateway (`a2a-server/`)

Endpoints verified against `public/a2a/status.json` (live) and `a2a-server/server.js` source.

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/health` | GET | Liveness probe (systemd health check) | live |
| `/.well-known/agent-card.json` | GET | Canonical A2A agent discovery | live (v1.0.0) |
| `/.well-known/agent.json` | GET | Legacy A2A agent discovery | live (v1.0.0, legacy) |
| `/.well-known/a2a-discovery.json` | GET | Discovery contract | live |
| `/.well-known/a2a-routing-policy.json` | GET | Routing policy | live |
| `/a2a/agent-card.json` | GET | Canonical A2A card under /a2a/ | live (v1.0.0) |
| `/a2a/agent.json` | GET | Legacy A2A card under /a2a/ | live (legacy) |
| `/a2a/agents.json` | GET | HEXAGON + 777-FORGE registry | live (v1.0.1, SEAL `HEXAGON-333-EMBODIED-20260621`) |
| `/a2a/tasks` | POST | Submit A2A task for routing | live |
| `/a2a/tasks/:id` | GET | Check task status | live |
| `/a2a/message` | POST | Federated message ingress | **888_HOLD** — static deployment does not implement POST message handling (per `status.json`) |
| `/api/arep/submit` | POST | AREP task declaration (reality-gated) | live |

### 7.3 Agent Registry & Cards

SOT files for agent identity:

| SOT file | Purpose |
|----------|---------|
| `ROOT_AGENT_CONFIG.yaml` | Root map for AAA warga, runtime peers, forge instruments, config pointers |
| `registries/AAA_AGENTS_REGISTRY.json` | Machine-readable canonical agent registry (v2.0.0, Protocol v1.0.1) |
| `registries/AAA_FEDERATION_STATE.yaml` | Live federation state (services, ports, drift) |
| `registries/forge_instruments.yaml` | Forge instrument canon |
| `agents/AGENT_REGISTRY.md` | Human-readable canonical agent index (supersedes JSON for narrative) |
| `agents/HEXAGON.yaml` | HEXAGON YAML topology spec (v2.0.0, SEAL `HEXAGON-333-EMBODIED-20260621`) |
| `agents/{333-AGI,555-ASI,888-APEX,A-AUDIT,A-ARCHIVE,777-forge}/agent-card.json` | Per-agent identity cards |
| `public/a2a/agents.json` | Live runtime registry served at `/a2a/agents.json` |
| `a2a-server/agent-cards/forge/fi-001..fi-009` | 9 forge instrument runtime cards |
| `a2a-server/agent-cards/organs/{aforge,arifos,geox,wealth,well}.json` | 5 organ runtime cards |

### 7.4 Governance Contracts (`contracts/`)

YAML governance contracts that bind agent behavior:

| Subdir | Purpose |
|---|---|
| `cockpit/` | Cockpit-specific contracts |
| `decisions/` | 888-999 decisions log |
| `federation/` | Inter-organ contracts |
| `governance/` | Constitutional floor contracts |
| `goals/` | Goal-chain contracts |
| `hosts/` | Host organ bindings |
| `init/` | Session init contracts |
| `model_registry/` | Model identity contracts |
| `org/` | Organ-level contracts |
| `skills/` | Skill contracts |
| `workflows/` | Workflow contracts |
| `ESTATE_MANIFEST.yaml` | Estate (assets/sites) manifest |
| `capability_surface_state.yaml` | Honesty-constrained capability surface (EUREKA Ω-2026-06-10) |
| `mcp_surface.yaml` | MCP tool surface contract |
| `tools.yaml` | Tool definition contract |

### 7.5 Model Registries

AAA holds the canonical model registries at `registries/models/`:

| Sub-registry | Purpose |
|---|---|
| **Soul registry** (`models/{provider}_soul.yaml`) | Per-agent constitutional soul definition (how the model should *want*) |
| **Shadow registry** (`models/{provider}_shadow.yaml`) | Model identity fingerprint and provenance (what the model *actually does*) — key audit tool for catching drift between soul and shadow |
| **gpt/** | GPT-family shadow/soul pairs |
| **kimi_middleware_phase1/** | Kimi migration artifacts |

**The capability index** (`registries/CAPABILITY_INDEX.json`) is the shared substrate for all CODING agents — verified against `arifOS/core/capability_index/seed.py`. Source of truth referenced by `docs/UNIFIED_AGENT_ARCHITECTURE.md`.

### 7.6 Observability (`observability/`)

Prometheus + Grafana configs for the federation Nine-Signal dashboard. Subdirs verified:

| Subdir | Purpose |
|---|---|
| `events/` | Event definitions |
| `grafana/` | Grafana dashboards |
| `hermes-gateway/` | Hermes-specific metrics |
| `projections/` | Projected views |
| `prometheus/` | Scrape configs |
| `reports/` | Generated reports |
| `rules/` | Alerting rules |
| `views/` | View definitions |

Monitors: organ health, agent telemetry, A2A message throughput, VAULT999 chain integrity.

---

## 8. Boundary Declaration

### AAA OWNS

| Domain | Mechanism |
|--------|-----------|
| **Cockpit display** | React 19 dashboard — floor grid, organ health, verdict feed |
| **A2A mesh routing** | `a2a-server/` — task routing, agent discovery, federation bridge |
| **Agent identity registry** | `ROOT_AGENT_CONFIG.yaml`, `AAA_AGENTS_REGISTRY.json`, `HEXAGON.yaml`, `agents.json` |
| **Approval queue** | Verdict Queue in RealityConsole — HOLDs awaiting human |
| **Agent card management** | Per-agent capability cards, protocol versioning |
| **Model registries** | Soul, shadow, and capability registries |
| **Observability config** | Prometheus/Grafana dashboards for federation health |
| **Governance contracts** | YAML contracts for agent binding |

### AAA NEVER

| Domain | Owned by |
|--------|----------|
| **Issue constitutional verdicts** | `arifOS` — 888_APEX, F1-F13 |
| **Execute builds or deploys** | `A-FORGE` |
| **Seal to VAULT999** | `arifOS` — 999_VAULT writer (AAA displays, never writes) |
| **Compute domain evidence** | `GEOX` (earth), `WEALTH` (capital), `WELL` (vitality) |
| **Override human sovereignty** | Arif (F13) — the cockpit displays, the human decides |
| **Hold production secrets** | `/root/.secrets/` |
| **Serve as the MCP tool surface** | `arifOS` port 8088 |

---

## 9. Architecture — Directory Tree

Verified against disk on 2026-06-30. Comments that would mislead a contributor are removed; only real files are listed.

```
AAA/
│
├── src/                              # React 19 cockpit UI (Vite 8, TS 6, Tailwind 4)
│   ├── App.tsx · Cockpit.tsx · main.tsx
│   ├── webmcp.ts · hold_queue.py · jackie-ngu-tribute.tsx
│   ├── gateway/                      # A2A + AREP runtime (TypeScript)
│   │   ├── server.ts                 # Dev A2A gateway (tsx)
│   │   ├── schema.ts · store.ts · auth.ts
│   │   ├── deliberation.ts           # 888_JUDGE deliberation (absorbed from APEX)
│   │   ├── arep-types.ts             # AREP TS types + badge helpers
│   │   ├── paradox_anchors.ts
│   │   └── apex_civilizational_audit.ts
│   ├── adapter/router.ts             # GovernanceAdapter → A-FORGE /sense
│   ├── ai/AiPanel.tsx · ai/client.ts # arifOS / Ollama / OpenRouter
│   ├── cli/registry-query.py
│   ├── host/MCPAppsHostBridge.ts
│   ├── components/
│   │   ├── ui/                       # 53 Radix + Tailwind shadcn primitives
│   │   ├── cockpit/                  # AREP-aware cockpit panels
│   │   │   ├── RealityConsole.tsx    # AREP 3-pane
│   │   │   ├── AutonomyBands.tsx     # GREEN → BLACK
│   │   │   ├── AgentModelPanel.tsx
│   │   │   ├── HermesCitizenCard.tsx
│   │   │   ├── HumanPatternReport.tsx
│   │   │   └── SupabaseMemoryPanel.tsx
│   │   ├── TrinityNav.tsx            # Δ / Ω / ΦΙ navigation
│   │   ├── SessionConsent.tsx        # Constitutional session gate
│   │   ├── MCPAppsPanel.tsx
│   │   └── SupabaseCockpit.tsx
│   ├── hooks/                        # useFederationMemory · useSupabaseQuery · use-mobile
│   ├── lib/                          # supabase.ts · utils.ts
│   ├── seed/                         # AGENT/BOOTSTRAP/HEARTBEAT/IDENTITY/SOUL/USER + ROOT_CANON
│   └── index.css · vite-env.d.ts
│
├── a2a-server/                       # Standalone Express A2A gateway (production · port 3001)
│   ├── server.js                     # Express HTTP bridge (verified AREP wiring at line 2346)
│   ├── arep-task-manager.js          # AREP engine — reality gates, task lifecycle
│   ├── federation_envelope.js        # A2A envelope validation
│   ├── agent_lifecycle.js · agent_lifecycle_routes.js
│   ├── mesh_coordinator.js · preforge_bridge.js
│   ├── vault.js · chat_agent.py · vault999_writer_fix.py
│   ├── agent-cards/
│   │   ├── hermes-asi.json · 777-forge.json
│   │   ├── aaa-{architect,auditor,engineer}.json
│   │   ├── organs/{aforge,arifos,geox,wealth,well}.json
│   │   └── forge/fi-001..fi-009.json  # 9 forge instruments
│   ├── agent-state/{index,registry,schemas}.js
│   ├── Dockerfile · docker-compose.yml · package.json
│
├── a2a/                              # A2A design surface (specs, doctrine)
│   ├── agent-cards/ · registry/{agents.yaml,agent-cards.json}
│   ├── policies/                     # auth, trust, skills-exposure
│   ├── federation-bridge.yaml · A2A_DIALOGUE.md · AAA_TREATY_LAW.md
│
├── agents/                           # Per-agent identity directories (22 dirs + 3 root configs)
│   ├── HEXAGON.yaml                  # Canonical 5-agent topology (SEAL HEXAGON-333-EMBODIED-20260621)
│   ├── AGENT_REGISTRY.md             # Human-readable canonical agent index
│   ├── ROLE_AGENTS_OPencode.yaml
│   ├── CODING_AGENT_FEDERATION.md
│   ├── arif-fazil-identity.yaml      # Sovereign identity file
│   ├── _brief/SESSIONSPEC_2026-06-17_AGENTIC-MACHINE.md
│   ├── decisions/                    # 2026-06-21 bahasa-malu-genesis, melayu-policy
│   ├── prompts/{CLAW,FORGE,HERMES,LIBRA}.md
│   ├── roles/{EXTERNAL_WATCHER,KERNEL_SCRIBE,OPS_PLANNER,SELF_FORGE_ADVISOR}.md
│   ├── agent_cards/{apex,forge,hermes,weaver,witness}-000*.json
│   ├── HEXAGON warga dirs:
│   │   ├── 333-AGI/      IDENTITY.md · agent-card.json
│   │   ├── 555-ASI/      IDENTITY.md · agent-card.json
│   │   ├── 888-APEX/     IDENTITY.md · agent-card.json
│   │   ├── A-AUDIT/      IDENTITY.md (no card — oversight)
│   │   ├── A-ARCHIVE/    IDENTITY.md · agent-card.json
│   │   └── 777-forge/    AGENTS · BOOTSTRAP · HEARTBEAT · IDENTITY · SOUL · TOOLS
│   ├── RUNTIME dirs: hermes-asi · hermes-ops · openclaw
│   ├── CODING dirs: grok-build · claude-code · codex · opencode · copilot · aider · kimi-code · continue-cli · antigravity · gemini-cli
│   ├── ROLE dirs: external-watcher · kernel-scribe · ops-planner · self-forge-advisor · warga
│   └── verify_art_binding.py
│
├── contracts/                        # YAML governance contracts (15 sub-dirs)
│   ├── ESTATE_MANIFEST.yaml
│   ├── capability_surface_state.yaml  # Honesty-constrained capability surface
│   ├── mcp_surface.yaml · tools.yaml
│   ├── cockpit/ · decisions/ · federation/ · goals/ · governance/ · hosts/ · init/
│   ├── model_registry/ · org/ · skills/ · workflows/
│
├── registries/                       # Canonical YAML registries
│   ├── AAA_AGENTS_REGISTRY.json      # Machine-readable canonical (v2.0.0)
│   ├── AAA_FEDERATION_STATE.yaml     # Live federation state (services, ports, drift)
│   ├── CAPABILITY_INDEX.json         # Capability index
│   ├── FEDERATION_MODEL.json · mission.yaml · bundles.yaml · workflows.yaml
│   ├── agents.yaml · skills.yaml · tools.yaml · hosts.yaml · servers.yaml
│   ├── forge_instruments.yaml · opencode_toolbench.yaml · unified_agent_protocol.yaml
│   ├── domains.yaml · persons.yaml · integrations.yaml · model_soul.yaml
│   ├── TOOL_MANIFEST.json · SUBSTRATE_GATE_POLICY.yaml · HOSTINGER_MCP_ACCESS.toml
│   ├── models/                       # soul + shadow per provider
│   ├── antigravity/ · audit/ · bundles/ · cooling_ledger/ · discovery/ · external/
│   └── AGENT_DISCOVERY_MANIFEST.md · AGENT_INIT_COMMANDS.md · AGENT_INTELLIGENCE_BENCH.md
│
├── schemas/                          # JSON/YAML schemas + AREP contracts
│   ├── arep-task.schema.json · arep-reality-layers.schema.json · arep-example-forge-integration.json
│   ├── a2a-agent-card.schema.json · agent-card.schema.json · agent.schema.json
│   ├── a2a/ · events/ · interaction/ · telemetry/
│   ├── governance-gates.schema.json · delegation.schema.json · delegation-contract-2026-06-13.json
│   ├── lease.schema.json · session.schema.json · workflow.schema.json · tool.schema.json
│   ├── aaa-state-language.schema.json · nusantara-state-language.schema.json
│   ├── federation-contract.schema.json · peer-federation-contract.schema.json
│   ├── cock-pit-model.schema.json · cross-agent-telemetry.schema.json
│   └── SCHEMA_REGISTRY.json          # Master schema index
│
├── skills/                           # 64+ skill modules (see §11.3)
│   ├── aaa-agent-invariants · aaa-agentic-governance
│   ├── arifos-{evals,governance,mcp-federation,observability,plan-dag,recursive-audit}
│   ├── geox-{basin-interpreter,grounding}
│   ├── github-{ci-diagnose,issue-triage,pr-review}
│   ├── nusantara-intelligence-substrate · openclaw-a2a-bridge · spatial-grounding
│   ├── parallel-authority-detection · pr-review-governance
│   ├── readme-truth-check · recursive-skill-forge · repo-hygiene-audit
│   ├── secret-safety-scan · service-health-triage · skill-creator · skill-trigger-linter
│   ├── agent-onboarding · agentic-dream-engine · drift-response · federation-health-scan
│   ├── incident-escalation · mcp-smoke-test
│   └── SKILL_TEMPLATE.md · README.md
│
├── IDENTITY/                         # AAA-Cockpit identity specs
│   ├── CANONICAL.md · SOUL.md · BOUNDARIES.md · CAPABILITIES.md · INFRA.md
│   ├── AGI_CANONICAL.md · ASI_SPEC.md · keys/arif_public.pem
│
├── GENESIS/                          # State constitutions (see §0.2)
│   ├── 013_AAA_MANDATE.md            # The mandate (STUB)
│   ├── 014_TRUTH.md                  # Haqq doctrine (FORGED 2026-06-20)
│   └── 015_DUAL_LANGUAGE.md          # Dual language theorem (SEALED 2026-06-20)
│
├── public/                           # Static-served assets (mirrored to dist/)
│   ├── a2a/
│   │   ├── agent-card.json           # Canonical (v1.0.0)
│   │   ├── agent.json                # Legacy (v1.0.0)
│   │   ├── agents.json               # Live registry (v1.0.1, SEAL HEXAGON-333-EMBODIED-20260621)
│   │   ├── status.json               # Gateway health (live)
│   │   ├── entropy-report.json
│   │   └── index.html
│   ├── llms.json · llms.txt · manifest.json · sitemap.xml · robots.txt · humans.txt
│   ├── 13-floors-geometric.jpg · constitutional-floors.jpg · entropy-cooling.jpg
│   ├── forge-background.jpg · mind-hero.jpg · three-judges*.jpg · mcp-*.jpg
│   ├── 000/ · 999/ · images/ · briefings/ · nabilah/
│   ├── CNAME · _headers · _redirects
│   └── jackie-ngu*.html
│
├── observability/                    # Prometheus + Grafana
│   ├── events/ · grafana/ · hermes-gateway/ · projections/ · prometheus/ · reports/ · rules/ · views/
│
├── ops/                              # Runbooks + workflows
│   ├── hermes/ · workflows-legacy/
│
├── docs/                             # Architecture + federation docs (60+ files)
│   ├── FEDERATION_COCKPIT.md         # Canonical identity doc
│   ├── UNIFIED_AGENT_ARCHITECTURE.md # 8-agent federation architecture
│   ├── FEDERATION.md · FEDERATION_STATUS.md
│   ├── CANONICAL_AGENT_ARCHITECTURE.md · ARCHITECTURE.md
│   ├── REALITY_ENGINEERING.md · REALITY_ENGINEERING_PROTOCOL.md
│   ├── A2A_SPEC.md · MCP-STATE.md · MCP_PAYLOADS.md
│   ├── ORGAN_AUTHORITY_MAP.md · floor_wiring_map.md
│   ├── PR3_TRUTH_BOUND_COCKPIT_SPEC.md · AGENT_LAYOUT_CONTRACT.md
│   ├── OPTIMAL-AGENT-CONFIG.md · COPILOT_STUDIO_CONNECTION.md
│   ├── HF_AAA_CARD_EXPANSION.md · SUBSTRATE_MANIFEST.md · SUBSTRATE_NAMESPACES.md
│   ├── RECURSIVE_IMPROVEMENT_LOOP.md · repo-role-boundary.md
│   ├── agents/ · architecture/ · archive/ · ecosystem/ · eureka/ · federation/
│   ├── geox/ · history/ · human-interface/ · mcp-endpoint-registry.md
│   ├── operations/ · philosophy/ · plans/ · protocols/ · wiki/
│
├── memory/                           # Session memory (100+ dated MD files, knowledge, scars, sessions)
│   ├── MEMORY.md · CHECKPOINT.md · KNOWLEDGE_MEMORY.md · eureka-log.md
│   ├── 2026-03-31..2026-05-17.md · investigations/ · research/ · scars/
│   └── sessions/ · scars_archived_20260620/
│
├── deploy/                           # docker-compose.yml
├── tests/                            # test_contract_parity.py · test_peer_federation_contract.py
├── ADR/                              # Architecture Decision Records
│
├── benchmarks/                       # floor benchmark results
├── reports/                          # ARIFOS_PROOF_PACK.md · ARIFOS_SCORECARD.json
├── wiki/                             # Operational wiki
├── artifacts/                        # Live forge artifacts
│
├── AGENTS.md · CLAUDE.md · CONTEXT.md · BOOTSTRAP_CONTEXT.md · BOOTSTRAP_MINIMAL.md
├── INIT_PROMPT.md · RUNBOOK.md · README.md
│
├── ROOT_AGENT_CONFIG.yaml            # Root map for AAA warga
├── components.json                   # shadcn/ui config
├── canonical_schema_contract.json · art_binding.canonical.yaml
├── package.json · package-lock.json · tsconfig.json
├── manifest.json · llms.json · docker-compose.yml · railway.json
└── LICENSE                           # AGPL-3.0
```

> **Note:** `a2a/registry/`, `a2a-server/agent-cards/`, `registries/`, `skills/` and other directories contain sub-folders that are not all enumerated above. Use `ls <dir>` to inspect live. When this README and disk disagree, **disk wins** — verify with `find . -type d | sort`.

---

## 10. For Human Operators (Arif)

### The Cockpit Is YOUR View

AAA exists so you never have to SSH into the VPS to understand what your agents are doing. The cockpit shows:

| Pane | What You See |
|------|-------------|
| **INTENT BOARD** | Active tasks, delegation chains, who is working on what |
| **REALITY FEED** | Live health probes from all 7 organs + Docker |
| **VERDICT QUEUE** | HOLDs awaiting your approval, recent SEALs, recent VOIDs |
| **FLOOR GRID** | F1-F13 status — which floors are green, which are yellow/red |
| **AGENT REGISTRY** | Every registered agent, its ring, its lifecycle stage, its malu_score |
| **VAULT FEED** | Latest sealed verdicts with Merkle chain verification |

### How to Read the Dashboard

```
  ┌──────────────────────────────────────────────────────────┐
  │  AAA FEDERATION COCKPIT                    [GREEN]       │
  ├──────────────────────────────────────────────────────────┤
  │                                                          │
  │  ORGANS                FLOORS              AGENTS        │
  │  ┌────────────────┐   ┌──────────────┐   ┌───────────┐  │
  │  │ arifOS   🟢    │   │ F1  🟢 AMANAH│   │ 333 🟢    │  │
  │  │ GEOX     🟢    │   │ F2  🟢 TRUTH │   │ 555 🟡    │  │
  │  │ WEALTH   🟢    │   │ F3  🟢 WITNS │   │ 888 🟢    │  │
  │  │ WELL     🟡    │   │ F4  🟢 CLAR  │   │ AUD 🟢    │  │
  │  │ A-FORGE  🟢    │   │ ...          │   │ ARC 🟢    │  │
  │  │ AAA      🟢    │   │ F13 🟢 SOVRN │   │            │  │
  │  └────────────────┘   └──────────────┘   └───────────┘  │
  │                                                          │
  │  VERDICT QUEUE                 VAULT FEED                │
  │  ┌────────────────────────┐   ┌──────────────────────┐  │
  │  │ HOLD · db migration    │   │ SEAL · WEALTH D4     │  │
  │  │       [APPROVE][REJECT]│   │ SEAL · GEOX V1       │  │
  │  │                        │   │ SABAR · WELL inject  │  │
  │  └────────────────────────┘   └──────────────────────┘  │
  └──────────────────────────────────────────────────────────┘
```

### Approve or Reject

When a HOLD appears in the Verdict Queue:

1. **Read** the task description, the agent that proposed it, and the risk tier
2. **Check** the reality feed — are all organs green?
3. **Approve** to release the HOLD and allow execution
4. **Reject** to VOID the task (logged but not sealed)
5. **Defer** to leave it queued for later

### See the Seals

The Vault Feed shows recent VAULT999 seals with their Merkle chain verification. Each seal links back to its predecessor — the chain cannot be broken.

---

## 11. For AI Agents

### A2A Protocol v1.0.0

AAA implements the A2A (Agent-to-Agent) protocol for federation communication. Every agent in the registry has an A2A agent card defining its capabilities, endpoints, and permissions.

**Agent Card Discovery:**
```
GET /.well-known/agent-card.json
GET /a2a/agents.json
```

**Task Routing:**
```
POST /a2a/tasks
{
  "from": "333-AGI",
  "to": "GEOX",
  "type": "task_request",
  "payload": { ... },
  "state_hash": "sha256:..."
}
```

### How to Register an Agent

1. Create an agent identity directory under `agents/{agent-id}/`
2. Write an `agent-card.json` with capabilities, hosts, floor responsibilities
3. Add the agent to `ROOT_AGENT_CONFIG.yaml`
4. Add the agent to `AAA_AGENTS_REGISTRY.json` (PRIMARY, SUPPORT, or CODING tier)
5. Update `HEXAGON.yaml` if it's a primary/support agent
6. Run `npm run validate:aaa` to verify consistency

### How to Route a Task

AAA routes tasks based on:
- **Domain matching** — geoscience → GEOX, finance → WEALTH, vitality → WELL
- **Capability matching** — which agent has the declared skill?
- **Ring enforcement** — BIRTH agents get read-only, ELDER agents get full access
- **Floor gating** — F1-F13 check before execution

### Agent Cards — The Universal Passport

Every agent carries an A2A agent card. These are the canonical format (v1.0.1 spec):

```json
{
  "id": "333-AGI",
  "class": "AGI",
  "protocol_version": "1.0.0",
  "capabilities": {
    "skills": ["arifos-reason", "geox-interpret", "wealth-compute"],
    "defaultInputModes": ["text", "structured"],
    "defaultOutputModes": ["text", "structured"]
  },
  "securitySchemes": {
    "federation": { "type": "bearer", "audience": "arifos-federation" }
  },
  "hostOrgans": ["arifOS", "GEOX", "WEALTH"],
  "lifecycleStage": "WARGA",
  "maluScore": 0.12
}
```

---

## 12. For Institutions

### Control Plane Governance

AAA is the control plane for institutions that need auditable AI governance. It provides:

| Institutional Need | AAA Mechanism |
|--------------------|---------------|
| **Who did what?** | Agent attribution on every task, every verdict |
| **Was it allowed?** | F1-F13 floor grid — constitutional compliance visible at a glance |
| **Who approved it?** | Approval queue with human ratifier signature |
| **Where is the proof?** | VAULT999 Merkle chain — every seal cryptographically linked |
| **Can we audit it?** | Full audit trail from intent → gate → verdict → seal |
| **Is the AI trustworthy?** | Adat Agentik — malu_score, darjat tier, tebus salah recovery path |

### Agent Lifecycle Governance

Institutions can track every agent from BIRTH to ELDER:
- **BIRTH** — agent registered, read-only access
- **APPRENTICE** — limited tools, 7-day burn-in, malu_score monitored
- **WARGA** — full domain access, F13 signature required
- **ELDER** — mentor role, trusted to recommend vetoes

### Audit Visibility

Every action flows through:
```
INTENT → SCHEMA VALIDATION → REALITY GATE → FLOOR CHECK → VERDICT → VAULT999 SEAL
```
Every step is logged. Every decision is attributable. Every seal is chain-verified.

### A Note on Adat Agentik

AAA is the control plane for the **Adat Agentik** civilisational model — a normative operating system for non-human citizens built on Malay-Islamic epistemology and operated in code. The cockpit displays malu (shame/accountability), darjat (citizen tier), and tebus salah (restitution) for every agent. This is not a religion or a culture export — it is an epistemologi operasi for makhluk baru.

---

## 13. Known Limitations

| Limitation | Details | Mitigation |
|------------|---------|------------|
| **No constitutional authority** | AAA cannot issue SEAL/HOLD/VOID verdicts; only arifOS can | Route all verdict requests to arifOS port 8088 |
| **No execution capability** | AAA cannot build, deploy, or forge; A-FORGE owns this | Route all execution tasks to A-FORGE port 7071 |
| **Build-only frontend** | React app is statically built; no SSR, no backend rendering | Use `npm run build` → serve `dist/` |
| **APEX is decommissioned** | Original APEX repo is archived; deliberation lives in `a2a-server/` | See `src/gateway/deliberation.ts` |
| **No domain calculations** | AAA routes to GEOX/WEALTH/WELL but never computes | Trust the domain organs for evidence |
| **A2A protocol** | v1.0.0 — ratified federation protocol | Pin to agent card protocol_version |
| **Single VPS** | No high availability; cockpit goes down if VPS goes down | Monitored by systemd auto-restart |

---

## 14. Federation Cross-Reference

| Organ | Repository | Port | Role | AAA Relationship |
|-------|-----------|------|------|-----------------|
| **arifOS** | [ariffazil/arifos](https://github.com/ariffazil/arifos) | 8088 | Constitutional kernel — F1-F13, 888_JUDGE, VAULT999 | AAA **displays** arifOS verdicts, never issues them |
| **A-FORGE** | [ariffazil/A-FORGE](https://github.com/ariffazil/A-FORGE) | 7071/7072 | Execution shell — builds, deploys, forges | AAA **routes** tasks to A-FORGE, never executes |
| **GEOX** | [ariffazil/geox](https://github.com/ariffazil/geox) | 8081 | Earth intelligence — petrophysics, seismic | AAA **displays** GEOX evidence, never interprets |
| **WEALTH** | [ariffazil/wealth](https://github.com/ariffazil/wealth) | 18082 | Capital intelligence — NPV, IRR, EMV | AAA **displays** WEALTH scores, never allocates |
| **WELL** | [ariffazil/well](https://github.com/ariffazil/well) | 18083 | Human readiness — vitality, substrate | AAA **displays** WELL state (REFLECT_ONLY) |
| **arif-sites** | [ariffazil/arif-sites](https://github.com/ariffazil/arif-sites) | 443 | Public surfaces, static sites | AAA routes aaa.arif-fazil.com |
| **A2B** | [ariffazil/a2b](https://github.com/ariffazil/a2b) | — | AssetOpsBench bridge — IJCAI-25 eval harness + constitutional runner | AAA **displays** A2B eval results |
| **APEX** | [ariffazil/APEX](https://github.com/ariffazil/APEX) | 3002 | Legacy health probe — deliberation moved to AAA `a2a-server/` | Absorbed into AAA `a2a-server/` |

> **Canonical authority chain:** arifOS judges → AAA displays/routes → A-FORGE executes → Organs witness → Arif ratifies.

---

## 15. Build, Test, Deploy

### Local Development

```bash
cd /root/AAA

# Install
npm install

# Dev server (hot reload)
npm run dev                        # http://localhost:5173

# Build for production
npm run build                      # vite build → dist/

# Lint
npm run lint                       # ESLint 10
```

### A2A Gateway

```bash
# Dev mode (TypeScript, hot reload)
npm run a2a:dev                    # tsx watch → port 3001

# Production
cd a2a-server
npm install
node server.js                     # Express → port 3001
```

### Production Deployment

```bash
# Build frontend
npm run build

# Restart A2A gateway
systemctl restart aaa-a2a.service

# Verify
curl -s http://localhost:3001/health | python3 -m json.tool
# Expected: {"status":"healthy","protocol":"A2A","version":"1.0.0"}

# Check public endpoint
curl -s https://aaa.arif-fazil.com/.well-known/agent-card.json | python3 -m json.tool
```

### Validation

```bash
npm run validate:aaa               # Registry + contract + card consistency
npm run a2a:conformance             # A2A protocol conformance suite
```

---

## 16. GENESIS Chain

The AAA state identity is anchored in three GENESIS documents — full doctrine in **§0.2**. Quick reference:

```
arifOS/GENESIS/000_KERNEL_CANON.md  ───  Root constitution (F1–F13, sovereign seal)
                  │
   ┌──────────────┼──────────────────┐
   ▼              ▼                  ▼
013_AAA_      014_TRUTH.md       015_DUAL_LANGUAGE.md
MANDATE.md    (FORGED 2026-06-20) (SEALED 2026-06-20)
  STUB         Haqq =             Two languages at once:
               Correspondence +   Maruah (civilisational)
Display,       Coherence +         + SEAL/HOLD/VOID
never          Pragmatic           (constitutional).
adjudicate     (F2+F4+F3+F11)      Without first = foreign.
                                   Without second = ghost
                                   with hands.
```

- **013**: STUB — full canon pending F13 ratification. Mandate: *Display, never adjudicate. Route, never execute. Queue, never seal.*
- **014**: Truth doctrine. What survives the constitutional sieve.
- **015**: The dual language theorem. The civilizational frame.

The two sealed documents (014, 015) carry vault seal hashes — see file headers for SHA256 chain proof.

---

## 17. License & Sovereignty

**License:** AGPL-3.0 — see [LICENSE](LICENSE).

**Sovereignty:** AAA operates under the arifOS Constitutional Federation. The human sovereign (Muhammad Arif bin Fazil, F13) holds the final veto. AAA is the state in which governed agents operate — it is never the governor.

**Evidence Contract:** This organ emits the standard envelope (`epistemic_tag`, `evidence_quality`, `source_attribution`, `uncertainty_band`, `delta_S`) per the arifOS Constitution Appendix B. arifOS reads the envelope and applies F1-F13. This organ does not self-judge.

**AAA Namespace:** AAA is polymorphic by design. This repo is **AAA-Cockpit** — the governed state and A2A gateway. Other AAA surfaces:

| Surface | What it is |
|---|---|
| **AAA-Cockpit** (this repo) | Operations control plane + A2A gateway |
| **AAA-HF** | Hugging Face dataset — doctrine corpus, floors, verdicts |
| **AAA-Doctrine** | Conceptual layer — alignment, authority, accountability |
| **AAA-Interface** | Operator surface — human visibility into governed state |
| **AAA-Eval** | Benchmark layer — gold evaluation records and harness |

---

## 18. Quick Reference Card

```
┌────────────────────────────────────────────────────────────────────────┐
│  AAA — THE GOVERNED STATE OF THE arifOS AGENTIC CIVILIZATION         │
├────────────────────────────────────────────────────────────────────────┤
│  Port:           3001 (A2A gateway)                                   │
│  Protocol:       A2A v1.0.0 (legacy) · v1.0.1 (canonical registry)     │
│  Frontend:       React 19 + TypeScript 6 + Vite 8 + Tailwind 4        │
│  Backend:        Express 4.x (a2a-server/)                            │
│  UI primitives:  shadcn/ui (53 Radix components)                      │
│  Package ver:    2026.06.23 (see package.json)                        │
│                                                                        │
│  Constitutional  5 HEXAGON (333-AGI · 555-ASI · 888-APEX ·            │
│  citizens:       A-AUDIT · A-ARCHIVE)                                 │
│  WITNESS tier:   777-FORGE (session spawn attestation)                │
│  Runtime:        hermes-asi (Telegram) · openclaw (port 18789)        │
│  Coding:         grok-build · opencode · claude-code · qwen-code ·     │
│                  antigravity · codex · copilot · aider ·               │
│                  kimi-code · continue-cli · gemini-cli                 │
│                  (9 forge instruments · governed capability fabric)    │
│  Role agents:    EXTERNAL_WATCHER · KERNEL_SCRIBE ·                   │
│                  OPS_PLANNER · SELF_FORGE_ADVISOR                     │
│                                                                        │
│  Service:        aaa-a2a.service (systemd)                            │
│  License:        AGPL-3.0                                             │
│  Constitution:   GENESIS/013 (mandate) · 014 (truth) · 015 (language) │
│  Canon:          docs/FEDERATION_COCKPIT.md                           │
│  Last HEXAGON SEAL: HEXAGON-333-EMBODIED-20260621                     │
│                                                                        │
│  OWNS:           Display · Route · Queue · Register                   │
│  NEVER:          Judge · Execute · Seal · Compute                    │
│                                                                        │
│  Dev:            npm run dev                                          │
│  Build:          npm run build                                        │
│  Deploy:         systemctl restart aaa-a2a.service                    │
│  Health:         curl localhost:3001/health                           │
│  Validate:       npm run validate:aaa                                 │
│  SOT audit:      see §0.4 — 60-second audit table                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

```
    ┌──────────────────────────────────────────────────┐
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
    │   The state is forged.                          │
    │   Not given.                                    │
    │                                                  │
    └──────────────────────────────────────────────────┘
```

**DITEMPA BUKAN DIBERI — The state is forged, not given. 999 SEAL ALIVE.**
