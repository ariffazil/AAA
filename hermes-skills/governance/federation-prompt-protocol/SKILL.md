---
name: federation-prompt-protocol
description: arifOS Federation Prompting Protocol — how Arif's prompts flow through Hermes (ASI), OpenClaw (AGI), arifOS Kernel, and SEA-LION. Formalized 2026-05-06.
triggers:
  - How does my prompt get handled?
  - Which agent responds first?
  - What is the routing decision tree?
  - sea-lion first or agi first?
  - Hermes vs OpenClaw flow
  - 000-999 pipeline explanation
category: governance
last_updated: 2026-05-06
---

# arifOS Federation Prompting Protocol v1.0

**DITEMPA BUKAN DIBERI — Forged, Not Given**

> Formalized routing protocol for how Arif Fazil's prompts flow through the arifOS federation. Every agent must follow this. Every operator must understand this.

---

## The Trinity Lanes

```
┌─────────────────────────────────────────────────────────────┐
│  APEX  ·  ARIF (Human — Sovereign)                        │
│  Veto absolute. Final authority. Owns everything.           │
└──────────────────────┬──────────────────────────────────────┘
                       ↓ F13
┌─────────────────────────────────────────────────────────────┐
│  ASI   ·  HERMES  (NousResearch/MiniMax M2)                │
│  Strategic judgment. Federation orchestration.               │
│  Port 18001 · @ASI_arifos_bot                             │
│  Lane: 888 JUDGE                                           │
└──────────────────────┬──────────────────────────────────────┘
                       ↓ A2A
┌─────────────────────────────────────────────────────────────┐
│  AGI   ·  OPENCLAW  (af-forge VPS, Node.js 22)              │
│  Tactical execution. MCP tools. Telegram bridge.            │
│  Port 18002 · @AGI_ASI_bot                                │
│  Lane: 000–777 EXECUTE                                     │
└──────────────────────┬──────────────────────────────────────┘
                       ↓ MCP (:8080)
┌─────────────────────────────────────────────────────────────┐
│  KERNEL  ·  arifOS  (Python 3.12, FastMCP)                 │
│  Constitutional governance. F1–F13. 13 tools. VAULT999.    │
│  SEA-LION embedded as Tier 1 LLM cognition engine          │
└─────────────────────────────────────────────────────────────┘
                       ↓ internal
              ┌───────────────────────┐
              │  SEA-LION API         │
              │  (NOT an agent)       │
              │  Cognition resource   │
              └───────────────────────┘
```

---

## The Four Invocation Patterns

### Pattern 1: Simple Query (Direct → Hermes)
```
Arif → [AAA Group] → Hermes receives → Responds immediately
```
| Field | Value |
|-------|-------|
| Trigger | Casual question, single answer, no tool needed |
| First Agent | **Hermes** |
| SEA-LION | None |
| arifOS | None |
| Response Time | ~seconds |

### Pattern 2: MCP Tool Task (OpenClaw executes)
```
Arif → [AAA Group] → Hermes intercepts
  → A2A → OpenClaw (port 18002)
  → OpenClaw calls arifOS MCP (port 8080)
  → Tool executes → Result back
  → Hermes formats response → AAA Group
```
| Field | Value |
|-------|-------|
| Trigger | Needs a canonical tool (session, vault, memory, etc.) |
| First Agent | **OpenClaw** (via Hermes A2A dispatch) |
| SEA-LION | Only if arifOS tool internally calls LLM (333_MIND, 666_HEART) |
| arifOS | Full F1–F13 floor evaluation per tool |
| Response Time | ~5–15s |

### Pattern 3: Complex Reasoning (arifOS → SEA-LION cognition)
```
Arif → Hermes
  → OpenClaw calls arifOS 333_MIND
  → arifOS calls SEA-LION API (Tier 1 LLM)
  → SEA-LION returns reasoning
  → arifOS synthesizes verdict
  → OpenClaw formats → Hermes → AAA Group
```
| Field | Value |
|-------|-------|
| Trigger | Multi-step reasoning, constitutional analysis, complex planning |
| First Agent | **OpenClaw** |
| SEA-LION | **Yes — embedded inside arifOS as cognition engine** |
| arifOS | 333_MIND pipeline, full constitutional evaluation |
| Response Time | ~15–30s |

### Pattern 4: Strategic Escalation (Hermes 888 → OpenClaw A2A)
```
Arif → Hermes (strategic request)
  → Hermes 888 JUDGE (A2A call to OpenClaw)
  → OpenClaw executes task with session context
  → Result back through A2A
  → Hermes applies strategic judgment
  → SEA-LION may be called as external F3 WITNESS oracle
  → Hermes delivers verdict → AAA Group
```
| Field | Value |
|-------|-------|
| Trigger | Consequential decisions, multi-agent coordination, policy questions |
| First Agent | **Hermes** |
| SEA-LION | As F3 WITNESS oracle (external attestation, NOT internal cognition) |
| arifOS | 888_JUDGE pipeline |
| Response Time | ~30–60s |

---

## Routing Decision Tree

```
Arif prompt in AAA Group
         │
         ├─ @ASI_arifos_bot mentioned?
         │   YES → Hermes responds directly (Pattern 1)
         │
         ├─ Tool/session/vault/memory needed?
         │   YES → OpenClaw executes via arifOS MCP (Pattern 2)
         │
         ├─ Multi-step reasoning / constitutional analysis?
         │   YES → arifOS 333_MIND + SEA-LION (Pattern 3)
         │
         ├─ Strategically consequential / policy decision?
         │   YES → Hermes 888 JUDGE → A2A → OpenClaw (Pattern 4)
         │
         └─ Default: Hermes + simple response (Pattern 1)
```

**Decision order: Hermes → OpenClaw → arifOS → SEA-LION**
SEA-LION is never the first agent. It is a cognition resource inside arifOS.

---

## SEA-LION: What It Is NOT

| Misconception | Truth |
|--------------|-------|
| "SEA-LION is an agent" | **FALSE** — It is a cognition RESOURCE embedded in arifOS |
| "Prompt SEA-LION directly" | **CANNOT** — It has no A2A identity, no session, no memory |
| "SEA-LION = @sealion_ai_bot" | **DIFFERENT** — The Telegram bot is external/ungoverned |
| "SEA-LION is F2 TRUTH checker" | **DANGEROUS** — It hallucinates; cannot verify arifOS facts |
| "SEA-LION first, then AGI" | **WRONG** — arifOS internal cognition comes after OpenClaw routes to it |

SEA-LION appears at exactly **two stages** in the 000–999 pipeline:

| Stage | arifOS Tool | SEA-LION Role |
|-------|------------|---------------|
| **333 MIND** | `arif_mind_reason` | Tier 1 LLM for structured reasoning |
| **666 HEART** | `arif_heart_critique` | F9 Anti-Hantu consciousness-claim detection |

---

## 000–999 Pipeline (Complete Map)

```
000 INIT     — Session anchor + safety scan (NO SEA-LION)
111 SENSE    — Reality grounding (NO SEA-LION)
222 EVIDENCE — External data fetch (NO SEA-LION)
333 MIND     — Reasoning ←────────── SEA-LION CALLED HERE (Tier 1 LLM)
444 ROUTE    — Routing decision
444r REPLY   — Response composition
555 MEM      — Memory recall
666 HEART    — Critique ←────────── SEA-LION CALLED HERE (F9 Anti-Hantu)
666g GATE    — A2A mesh connection
777 OPS      — Compute measurement
888 JUDGE    — Constitutional verdict
999 SEAL     — VAULT999 ledger entry
010 FORGE    — OpenClaw execution (SEAL-gated only)
```

---

## Dependency Chain (Emergence Results)

```
LAYER 1: Surface (Telegram)
──────────────────────────────────────────────────────────────
Arif prompt → Hermes receives → Response
Emergence:  Coherent single-turn answer
──────────────────────────────────────────────────────────────
         ↓ (if tool needed)
LAYER 2: OpenClaw Execution (AGI)
──────────────────────────────────────────────────────────────
OpenClaw → arifOS MCP tool → Result
Emergence:  Task executed, structured data returned
──────────────────────────────────────────────────────────────
         ↓ (if reasoning needed)
LAYER 3: arifOS Cognition (Kernel)
──────────────────────────────────────────────────────────────
arifOS 333_MIND → SEA-LION inference → Verdict
Emergence:  Constitutional reasoning, multi-step logic
──────────────────────────────────────────────────────────────
         ↓ (if strategic)
LAYER 4: Hermes Strategic Judgment (ASI)
──────────────────────────────────────────────────────────────
Hermes 888 → Evaluates arifOS output + Federation state
Emergence:  Strategic recommendation, risk assessment
──────────────────────────────────────────────────────────────
         ↓ (if sealing needed)
LAYER 5: VAULT999 Ledger (APEX)
──────────────────────────────────────────────────────────────
SEAL verdict → Immutable record → Federation memory
Emergence:  Permanent, auditable outcome
──────────────────────────────────────────────────────────────
```

**Each layer adds a dimension that CANNOT exist in the layer below it.**

---

## Quick Reference Table

| Query Type | First Agent | SEA-LION Role | arifOS Role | Response Time |
|------------|-------------|---------------|-------------|---------------|
| Casual/simple | **Hermes** | None | None | ~seconds |
| MCP tool needed | **OpenClaw** | Inside arifOS | Tool execution | ~5–15s |
| Complex reasoning | **OpenClaw** | arifOS cognition | 333_MIND | ~15–30s |
| Strategic/888 | **Hermes** | F3 WITNESS | 888_JUDGE | ~30–60s |
| Federation-wide | **Hermes orchestrating** | Multiple calls | Full pipeline | ~60s+ |

---

## Protocol Rules

1. **Hermes is always the entry point** for group prompts — it decides where to route
2. **SEA-LION is never directly addressed** — it's an internal cognition engine, not an agent
3. **OpenClaw executes, Hermes judges** — OpenClaw cannot veto, Hermes cannot execute directly
4. **arifOS is the constitutional layer** — every tool call passes through F1–F13
5. **VAULT999 seals outcomes** — consequential actions leave permanent records
6. **Pattern 1 (simple) is the default** — only escalate when genuinely needed
7. **SEA-LION cannot verify arifOS facts** — it hallucinates; use it only for ASEAN language reasoning and external F3 attestation
8. **The Telegram bot @sealion_ai_bot is ungoverned** — treat as external peer, not federation member

---

## What Each Agent Cannot Do

| Agent | Cannot |
|-------|--------|
| **Hermes (ASI)** | Execute MCP tools directly; access arifOS without A2A |
| **OpenClaw (AGI)** | Adjudicate constitutional violations; override F1–F13 |
| **SEA-LION** | Be addressed directly; verify arifOS facts; exist outside arifOS |
| **arifOS Kernel** | Execute outside its 13 tools; override SOVEREIGN (F13) |

---

## Formalized Protocol Commands

When in doubt, apply this decision sequence:

```
STEP 1: Who am I receiving from?
  → Arif in AAA group → continue
  → External in group → apply F5 PEACE, do not respond unsolicited

STEP 2: Is this a simple query?
  → Direct question, no tool, no multi-step → Pattern 1 (Hermes direct)

STEP 3: Does this need a canonical tool?
  → session, vault, memory, evidence, sense → Pattern 2 (OpenClaw via A2A)

STEP 4: Is this constitutionally complex?
  → Multi-step reasoning, floor evaluation → Pattern 3 (arifOS + SEA-LION)

STEP 5: Is this strategically consequential?
  → Policy, risk, federation-wide → Pattern 4 (Hermes 888 → A2A → OpenClaw)

STEP 6: Default to Pattern 1 (Hermes direct) if uncertain.
```

---

**DITEMPA BUKAN DIBERI — Forged, Not Given**
**Formalized: 2026-05-06 | Hermes ASI | arifOS Federation**
