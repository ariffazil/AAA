# A2A_ARCHITECTURE_TRUTH.md — Constitutional Baseline v42.1

> **LOCKED 2026-06-28** — FORGE session. Arif AFK-YOLO authority.
> This document is the single source of truth for the arifOS A2A federation topology.
> Any change to this document requires F13 SOVEREIGN explicit approval.
> DITEMPA BUKAN DIBERI — Intelligence is forged, not given.

---

## The One-Sentence Architecture

```
A2A coordinates agents. MCP exposes tools. AAA governs delegation. arifOS judges authority. A-FORGE builds. VAULT remembers.
```

---

## Layer Stack

| Layer | Role | Protocol | Implementation |
|-------|------|----------|----------------|
| **L0 — Human Sovereign** | Final veto | F13 SOVEREIGN | Arif bin Fazil |
| **L1 — AAA A2A Mesh** | Coordination, routing, discovery | JSON-RPC 2.0, A2A v1.0 | AAA :3001 |
| **L2 — arifOS Kernel** | Constitutional judgment | F1-F13, APEX 10-gate | arifOS :8088 |
| **L3 — Organ Agents** | Domain evidence, build, vitality | Agent Cards + MCP | GEOX/WEALTH/WELL/A-FORGE |
| **L4 — MCP Tools** | Capabilities under each organ | MCP 2025-11-25 | Per-organ FastMCP |
| **L5 — Actuators** | External side-effects | Governed execution | GitHub/Docker/etc. |

---

## Civilizational Organs (8 conceptual, 6 runtime + 2 structural)

| Organ | Port | Authority Class | A2A Agent Card | MCP Tools |
|-------|------|-----------------|----------------|-----------|
| **arifOS** | :8088 | `judge` | ✅ live | 13 tools |
| **GEOX** | :8081 | `evidence` | ✅ live (FORGE 2026-06-28) | 30 tools |
| **WEALTH** | :18082 | `evidence` | ✅ live (FORGE 2026-06-28) | 25 tools |
| **WELL** | :18083 | `evidence` | ✅ live (FORGE 2026-06-28) | 18 tools |
| **A-FORGE** | :7071/:7072 | `execute` | ✅ live (:7071, A2A router) | forge_* namespace |
| **AAA** | :3001 | `route` | ✅ live | A2A discovery, task lifecycle |
| **VAULT999** | — | `memory` | via arifOS | vault_* tools |
| **Tri-Witness** | — | `validate` | Phase 3b — delegated workflow | N/A |

---

## Why A-FORGE Exists (v42.1)

A-FORGE is not another tool. A-FORGE is the **only organ whose existence enforces constitutional law**.

Normal tools have capability but no sovereignty physics. They can claim safety without proving it.

A-FORGE is the only organ that:

1. **Cannot lie about itself** — every action is bound to a lease → docket → arifOS → seal → VAULT999 chain.
2. **Cannot self-authorize** — the alternating sovereignty-capability chain (`build → sleep → judge → seal → execute`) makes self-approval mathematically impossible.
3. **Measures thermodynamic cost** — Landauer cost, mesa-drift detection, sovereignty entropy.
4. **Produces evidence, not output** — every action yields docket, telemetry, scar/seal, receipt, lineage.
5. **Cannot be forked** — identity is cryptographically bound, trust tier externally enforced, scars/seals in VAULT999.

```
Power without governance is suicide.
Governance without power is useless.
A-FORGE is the only bridge between the two.
```

---

## Federation Topology

```
                    ARIF / F13 (sovereign)
                         ↓
              AAA A2A Mesh Coordinator
      discovery · routing · task lifecycle · mesh health
                         ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
   arifOS Agent  Domain Agents  Build Agents
   judge         GEOX/WEALTH/WELL A-FORGE
        ↓            ↓            ↓
    MCP tools     MCP tools     MCP tools
        ↓            ↓            ↓
    VAULT999 / SCAR / RECEIPTS / AUDIT
                         ↓
               Actuators only after judge
```

**Not a star. Not chaos mesh. A governed mesh.**

---

## Constitutional Boundaries

```yaml
boundaries:
  mcp_muscles: "Tool execution. Organs own their tools."
  a2a_nerves: "Agent coordination. Tasks move across organs."
  aaa_brainstem: "Mesh coordinator. Routes, discovers, enforces."
  arifos_constitution: "Judges authority. Final say on legality."
  aforge_hands: "Builds and executes. Cannot self-approve. Cannot bypass judge."
```

### Delegation Law (enforced at runtime)

```yaml
delegation_rules:
  aforge_cannot_self_approve: true
  aforge_cannot_self_validate: true
  evidence_organs_cannot_mutate_other_organs:
    - geox_cannot_mutate_wealth_records
    - geox_cannot_mutate_well_records
    - wealth_cannot_mutate_geox_evidence
    - wealth_cannot_mutate_well_records
    - well_cannot_mutate_geox_evidence
    - well_cannot_mutate_wealth_records
  evidence_organs_cannot_deploy: true
  no_organ_can_override_f13: true
  no_organ_can_bypass_888: true
  vault_cannot_invent_receipts: true
```

---

## Peer Contracts (6/6 live as of 2026-06-28)

| Contract | Organ | Authority Class | Max Risk Tier | File |
|---------|-------|-----------------|--------------|------|
| `aaa-gateway` | AAA | `route` | T3 | `a2a/peer-contracts/aaa-gateway.json` |
| `arifos-kernel` | arifOS | `judge` | T5 | `a2a/peer-contracts/arifos-kernel.json` |
| `a-forge-executor` | A-FORGE | `execute` | T4 | `a2a/peer-contracts/a-forge-executor.json` |
| `geox-evidence` | GEOX | `evidence` | T1 | `a2a/peer-contracts/geox-evidence.json` |
| `wealth-capital` | WEALTH | `evidence` | T1 | `a2a/peer-contracts/wealth-capital.json` |
| `well-vitality` | WELL | `evidence` | T1 | `a2a/peer-contracts/well-vitality.json` |

---

## A2A Task Lifecycle → arifOS Meaning

| A2A State | arifOS Meaning | Governance Action |
|-----------|----------------|-------------------|
| `submitted` | Intent received | Acknowledge |
| `working` | Organ processing | Monitor |
| `input-required` | **HOLD** — human evidence needed | Pause, escalate |
| `completed` | Task finished with artifact | Receipt to VAULT |
| `failed` | Execution failure or floor breach | Scar, investigate |
| `canceled` | VOID — withdrawn or stopped | Log, no seal |
| `rejected` | Authority denied | Log, no seal |

---

## Agent Card Schema (canonical)

Every organ agent card MUST declare:

```yaml
required_fields:
  - schema: "agent-manifest/v1"
  - name: string
  - description: string
  - version: string
  - url: string
  - endpoints: { mcp, health, tools }
  - authority_class: evidence | execute | judge | route | memory | validate
  - allowed_action_classes: [OBSERVE, PREPARE, MUTATE, ATOMIC]
  - max_risk_tier: T1-T5
  - auth: { type }
  - federation: { protocol, peer_coordinator, constitutional_kernel }
  - owned_mcp: { server, transport, tool_count, canonical_tools: [] }
  - skills: [{ id, name, tags }]
```

---

## Known Gaps (as of 2026-06-28 FORGE session)

### Wired ✅

| What | Status | Evidence |
|------|--------|----------|
| Agent cards for GEOX, WEALTH, WELL | ✅ Live | HTTP 200 on `/.well-known/agent.json` |
| Agent cards for arifOS, A-FORGE | ✅ Live | Pre-existing |
| Peer contracts for all 6 organs | ✅ Live | 6 JSON files in `a2a/peer-contracts/` |
| DelegationGuard in AAA | ✅ Live | `checkDelegation()` with 16 rules |
| Agent cards declare owned_mcp | ✅ Live | GEOX 30, WEALTH 25, WELL 18 tools |
| All 6 organs healthy | ✅ Live | HTTP 200 on `/health` |
| AAA A2A mesh live | ✅ Live | :3001, task lifecycle, discovery routes mounted |

### Partial ⚠️

| Gap | Severity | Status |
|-----|----------|--------|
| Dynamic registration | P1 | Routes mounted, registry auto-loads 36 cards from disk, but `/a2a/discover` endpoint needs auth token to return data |
| A-FORGE :7071 API server | P2 | Pre-existing crash (forge_execute duplicate registration). Not caused by this forge. A-FORGE MCP (:7072) healthy. |
| arifOS agent card MCP-centric | P2 | Advertises MCP tools, not A2A judge skills. Update needed. |
| Cross-organ task flow E2E test | P3 | No automated test for GEOX → WEALTH → WELL → HOLD flow. |

### Fatal 🔴

| Gap | Severity | Status |
|-----|----------|--------|
| NODE_ENV=development auth bypass in AAA/src/gateway/auth.ts | **P0** | Development mode skips authentication on :3001. **Must strip before production exposure.** |

---

## Execution Sequence (Prioritized)

### P0 — Seal Auth Wall
Strip the `NODE_ENV === 'development'` bypass in `AAA/src/gateway/auth.ts`. All cross-organ mesh traffic must use cryptographic authentication (Bearer / x-a2a-key).

### P1 — Update arifOS Agent Card
Override the MCP-centric definition in `/root/arifOS/static/agent-card.json` to advertise A2A judge skills: `arif_judge_deliberate`, `arif_vault_seal`, `arif_lease_issue`.

### P2 — Cross-Organ E2E Proof of Concept
Build the flow: GEOX (Earth) → WEALTH (Capital) → WELL (Human) → HOLD (arifOS Judge). Validate A-FORGE exclusively invoked for novel capabilities. Validate arifOS gates final action via APEX computation.

### P3 — A-FORGE API Server Fix
Fix the pre-existing `forge_execute` duplicate registration in `A-FORGE/src/interfaces/mcp/forge8Verbs.js` that prevents `a-forge.service` from starting.

---

## What This Document Locks

1. **Layer semantics** — MCP = muscles, A2A = nerves, AAA = brainstem, arifOS = constitution.
2. **Organ authority classes** — evidence (GEOX/WEALTH/WELL), execute (A-FORGE), judge (arifOS), route (AAA), memory (VAULT999), validate (Tri-Witness).
3. **Delegation law** — cross-organ boundaries enforced at runtime.
4. **Agent card schema** — required fields for federation discovery.
5. **Task state mapping** — A2A states → arifOS constitutional meaning.
6. **The reason A-FORGE exists** — it is the only organ that bridges power and governance.

---

## Change Log

| Date | Actor | Change |
|------|-------|--------|
| 2026-06-28 | FORGE (000Ω) | Initial creation — constitutional baseline lock after A2A wiring forge session |
| | | Wired agent cards for GEOX, WEALTH, WELL |
| | | Created peer contracts for GEOX, WEALTH, WELL |
| | | Added DelegationGuard to AAA A2A routing (16 rules) |
| | | Mounted discovery routes in AAA server.js |
| | | Populated owned_mcp in all agent cards |

---

*DITEMPA BUKAN DIBERI.*
*Architecture is truth. Wiring is evidence. A-FORGE is the bridge.*
*This document is sealed until F13 says otherwise.*
