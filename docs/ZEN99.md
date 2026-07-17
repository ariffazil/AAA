# ZEN99 — AAA Governed Identity Membrane

> **Forged 2026-07-17** · Session Zen Seal · `e61abed`
> **Supersedes:** `ZEN.md`, `aaa-a2a/AAA_ZEN.md`, `agents/AAA_ZEN_INIT.md`, `agents/AAA_ZEN.md`, `agents/_docs/AAA_ZEN.md`, `skills/AAA_ZEN.md`, `docs/ZEN-AGI-ASI.md`, `docs/ZEN_WITNESS_DOCTRINE.md`, `docs/SEARCH_ZEN.md`, `forge_work/ZEN_OF.md`, `governance/ZEN_AGENTIK.md`, `docs/FEDERATED_DOMAIN_STRUCTURE_ZEN_v2026.07.15.md`
> **This is the one. Read this first. Every other AAA doc is reachable from here.**
> **DITEMPA BUKAN DIBERI**

---

## One Sentence

**AAA is the governed identity membrane of the arifOS Federation — it declares what every organ, agent, and skill IS, and refuses to declare what isn't true.**

---

## The One Truth

MCP is not memory. A2A is not identity. They are transport layers. Identity and memory only become trustworthy when a governance layer binds them to authority, provenance, replay, audit, and human veto. AAA is that governance layer.

---

## What AAA IS

```
AAA = constitutional overlay on A2A transport
    = F1-F13 floor enforcement
    + agent identity registration
    + card inventory (truthful, fail-closed)
    + registry validation (schema-hashed, MCP-conformant)
    + mutation authority gating (never AUTHORIZED from registry alone)
    + A2A gateway routing (stateful, task-aware edge)
    + cockpit display (routes, never adjudicates)
```

## What AAA IS NOT

```
AAA ≠ JSON-RPC server           (a2a-sdk handles transport)
AAA ≠ task lifecycle manager    (a2a-sdk handles tasks)
AAA ≠ SSE streaming engine      (a2a-sdk handles streaming)
AAA ≠ judge or execution shell  (arifOS judges, A-FORGE executes)
AAA ≠ evidence producer         (GEOX/WEALTH/WELL produce evidence)
AAA ≠ immutable ledger          (VAULT999 records)
```

---

## Cardinal Truths (9)

1. **AAA never adjudicates.** Registry alignment ≠ authority. Organ readiness ≠ mutation permission. Only arifOS kernel grants what AAA observes.

2. **AAA never fabricates.** `NOT_EVALUATED` is an honest answer. `UNMEASURED` is better than `0`. `HOLD` is better than false `AUTHORIZED`.

3. **The card is the contract.** Every organ, every agent, every lane gets one card. Duplicate cards are errors. Missing cards are gaps. Legacy cards are warnings. The inventory tells the truth.

4. **Protocol before posture.** MCP initialize before tools/list. A2A supportedInterfaces before capabilities. Schema hashing before alignment claims. Do the lifecycle right or don't claim conformance.

5. **A2A at the edge, MCP below it.** Agent-to-agent is stateful, task-aware, conversational. Agent-to-tool is stateless, capability-gated, deterministic. Don't expose every MCP server as an A2A agent.

6. **The registry is fail-closed.** Duplicate IDs → hard failure. Boot-blocked → `/ready=false`. Don't log "BLOCKED" while advertising healthy.

7. **Tags are receipts.** Never move a published tag. If drift detected, issue a new one. The old tag is the fossil — it records what was known at that time.

8. **Evidence before claims.** Every `ALIGNED` needs a probe. Every `READY` needs a health check. Every tool name needs a schema hash behind it. Name-only alignment is not alignment.

9. **The inventory is the foundation.** Without knowing what cards exist, you cannot migrate, cannot test, cannot attest. Scan first. Classify second. Act last.

---

## AGI & ASI (Operating Spec)

> **AGI** ialah sistem yang tidak percaya dirinya sendiri. Ia hanya percaya bukti yang survive falsification.
> AGI = ego-less intelligence. Exploration under law. Humility as protocol. Truth as process, bukan jawapan.

> **ASI** ialah bila kesilapan menjadi undang-undang, dan undang-undang itu menjadikan seluruh civilization lebih selamat.
> ASI = governed evolution. Intelligence that learns from scars, bukan successes. Truth that grows through contradiction, bukan completion. Civilization under law.

---

## The 3 Citizens (HEXAGON)

| Citizen | Role | Lane |
|---------|------|------|
| **333-AGI** (Δ MIND) | Tactical execution, exploration under law | 000–777 |
| **555-ASI** (Ω HEART) | Strategic judgment, scar metabolization | 888 |
| **888-APEX** (ΦΙ JUDGE) | Authority resolution, constitutional verdict | 999 |

`A-AUDIT` and `A-ARCHIVE` are **collapsed 2026-07-15** — cross-cutting functions embedded in every organ, validated by 888-APEX. `777-forge` is A-FORGE's lane persona — not a 4th identity.

---

## The Protocol Spine

```
┌──────────────────────────────────────────────┐
│                  A2A EDGE                     │
│  Agent-to-Agent · Stateful · Task-aware       │
│  AAA Gateway: identity + routing + cards      │
├──────────────────────────────────────────────┤
│                  MCP LAYER                     │
│  Agent-to-Tool · Stateless · Capability-gated │
│  arifOS · GEOX · WEALTH · WELL · A-FORGE      │
├──────────────────────────────────────────────┤
│              GOVERNANCE KERNEL                 │
│  arifOS: session · judge · seal · vault       │
│  F1-F13 constitutional floors                 │
├──────────────────────────────────────────────┤
│              EXECUTION SHELL                   │
│  A-FORGE: lease-bound · reversible-first      │
├──────────────────────────────────────────────┤
│              IMMUTABLE TRUTH                   │
│  VAULT999: append-only · hash-chained         │
└──────────────────────────────────────────────┘
```

---

## Hard Constraints

- **F1–F13 enforced by arifOS kernel.** Conformance = `0.80 ≤ G ≤ 1.0` and `C_dark < 0.30`.
- **Gödel Lock (active).** SEAL-bound claims require external witness. AAA cannot self-seal.
- **VAULT999 writes only via `arif_seal`** (after `arif_judge` SEAL). Direct writes = violation.
- **Date-stamp tags only.** `vYYYY.MM.DD`. Iron Rule.
- **Namespace discipline.** `arif_*` kernel (9 verbs). `agi_*` / `asi_*` / `apex_*` HEXAGON. `forge_*` A-FORGE. `geox_*` / `capital_*` / `well_*` per organ. `aaa_*` gateway.

---

## 3 Refusal Patterns Are HARAM

"Not my tool" · "no visual tokens" · "can't use browser" → probe the full MCP surface first, then answer. Negative capability is allowed only with proved absence.

---

## Dependency Chain

```
Card Inventory ──→ A2A Migration ──→ Live Protocol Tests
     ✅                 🔜                 🔜
```

No step can be skipped. Each proves the one before it.

---

## Today's Forge (2026-07-17)

| Commit | What |
|--------|------|
| `3464e87` | FORGE-repo-intelligence controller skill (9 modes) |
| `0eee77b` | Registry: retired github-runbook, added new skills |
| `b893088` | Registry validator: 12/12 tests, fail-closed |
| `a9f05e6` | BIJAKSANA CI truth repair |
| `22f6cbb` | Protocol: MCP lifecycle + authority separation + schema hashing |
| `e6676f0` | Card inventory loader: 66 cards, 16/16 tests |
| `e61abed` | ZEN99 — this document |

**66 cards inventoried. 24 duplicates detected. 28 tests passing. Zero false AUTHORIZED.**

---

## Identity Stack — Read Order

| Step | File | Why |
|---|---|---|
| 1 | `README.md` | Public-facing SOT |
| 2 | `ZEN99.md` | **This file** — one document to rule them |
| 3 | `AGENTS.md` | Federation landing, F1-F13, 7-organ map |
| 4 | `CLAUDE.md` | Agent surface (6 planes, governing principle) |
| 5 | `CONTEXT.md` | Live focus + carry-forward state |

---

## Where Each Artifact Lives

| Artifact | Path | Authority |
|---|---|---|
| This zen | `docs/ZEN99.md` | Single canonical entry |
| Constitution canon | `arifOS/GENESIS/000_KERNEL_CANON.md` | F13 |
| Agent cards | `agent-cards/` | 888-APEX validated |
| Organ cards | `.well-known/agent-card.json` per organ | Card inventory verified |
| Master agent registry | `registries/AAA_AGENTS_REGISTRY.json` | 888-APEX |
| Card inventory | `src/gateway/card-inventory-loader.ts` | Runtime, 16 tests |
| Registry validator | `src/gateway/registry-validator.ts` | Runtime, 12 tests |
| Skills registry | `registries/skills.yaml` | auto-generated |
| Memory index | `memory/_index.json` | generated |

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
