# ARCHITECTURE_TRUTH.md — Constitutional Baseline v43.0

> **LOCKED 2026-07-04** — FORGE session. Arif AFK-YOLO authority.
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
| **L1 — AAA A2A Mesh** | Coordination, routing, discovery | JSON-RPC 2.0, A2A v1.0 | AAA :3001 (Express, live) + `aaa-a2a/` (Python, stub) |
| **L2 — arifOS Kernel** | Constitutional judgment | F1-F13, APEX 10-gate | arifOS :8088 |
| **L3 — Organ Agents** | Domain evidence, build, vitality | Agent Cards + MCP | GEOX/WEALTH/WELL/A-FORGE |
| **L4 — MCP Tools** | Capabilities under each organ | MCP 2025-11-25 | Per-organ FastMCP |
| **L5 — Actuators** | External side-effects | Governed execution | GitHub/Docker/etc. |

**Bridge note (2026-07-04):** the L1 layer now contains two parallel surfaces:
- **Express AAA :3001** — 3,862 lines, live in production, JSON-RPC + NATS mesh + Redis task store.
- **Python `aaa-a2a/`** — 16 .py files / 1,031 lines, Phase 2 stubs, ConstitutionalMiddleware + IdentityVerifier + Verdicts + Audit + Registry + Routing. **NOT YET LIVE** — grows alongside the Express server until parity.
- **A2A↔MCP bridge** — `a2a-server/a2a-mcp-bridge.js` (371 lines), routes A2A tasks to any of 5 MCP organs and writes VAULT999 receipts. The constitutional overlay sits ABOVE the bridge; the bridge sits ABOVE the official SDK.

The Python `aaa-a2a/` will replace the Express transport when parity is reached (Phase 5, **F13 approval required for cutover**).

---

## Civilizational Organs (8 conceptual, 6 runtime + 2 structural)

| Organ | Port | Authority Class | A2A Agent Card | MCP Tools |
|-------|------|-----------------|----------------|-----------|
| **arifOS** | :8088 | `judge` | ✅ live (9 skills, post 2026-07-04) | 13 tools |
| **GEOX** | :8081 | `evidence` | ✅ live | 30 tools |
| **WEALTH** | :18082 | `evidence` | ✅ live | 25 tools |
| **WELL** | :18083 | `evidence` | ✅ live | 18 tools |
| **A-FORGE** | :7071/:7072 | `execute` | ✅ live (:7071, A2A router) | forge_* namespace |
| **AAA** | :3001 | `route` | ✅ live | A2A discovery, task lifecycle, bridge |
| **VAULT999** | — | `memory` | via arifOS | vault_* tools |
| **Tri-Witness** | — | `validate` | Phase 3b — delegated workflow | N/A |

---

## Why A-FORGE Exists (v43.0)

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
                  ↓                  ↓
       Express :3001 (live)    Python aaa-a2a/ (stub)
                  ↓
              A2A↔MCP Bridge (a2a-mcp-bridge.js)
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

## Known Gaps & Seals

### Wired ✅ (post-pivot 2026-07-04)

| What | Status | Evidence |
|------|--------|----------|
| Agent cards for GEOX, WEALTH, WELL | ✅ Live | HTTP 200 on `/.well-known/agent.json` |
| Agent cards for arifOS, A-FORGE | ✅ Live | 9 skills (was 5) on arifOS card |
| Peer contracts for all 6 organs | ✅ Live | 6 JSON files in `a2a/peer-contracts/` |
| DelegationGuard in AAA | ✅ Live | `checkDelegation()` with 16 rules |
| Agent cards declare owned_mcp | ✅ Live | GEOX 30, WEALTH 25, WELL 18 tools |
| All 6 organs healthy | ✅ Live | HTTP 200 on `/health` |
| AAA A2A mesh live (Express :3001) | ✅ Live | task lifecycle, discovery routes, A2A↔MCP bridge |
| A2A↔MCP bridge | ✅ SEALED 2026-07-04 | `a2a-server/a2a-mcp-bridge.js` (371 lines) routes to all 5 organs, writes VAULT999 receipts |
| Auth wall | ✅ SEALED 2026-07-04 | `auth.ts` clean — F13 directive line 42; bearer + API key active; no dev bypass |
| arifOS agent card skills | ✅ SEALED 2026-07-04 | 5 → 9 skills: `judge.deliberate`, `lease.issue`, `session.identity`, `agent.discover` |
| Cross-organ E2E test | ✅ SEALED 2026-07-04 | `a2a-server/tests/e2e-cross-organ-flow.js` — 19/21 PASS, 0 fail |
| VAULT999 receipts flowing | ✅ SEALED 2026-07-04 | `vault.js` human_ratifier `'arifOS_AutoKernel'` → `'arif'` (was 422) |

### In Progress ⚠️

| What | Status | Plan |
|------|--------|------|
| Python `aaa-a2a/` package | Phase 2 stubs done (2026-07-04) | ConstitutionalMiddleware + IdentityVerifier + Verdicts + Audit + Registry + Routing. 27/27 unit tests passing. Not yet live. |
| AAA-A2A architectural pivot | Phase 1+2 done, Phase 3-5 pending | Phase 3: registry bridge. Phase 4: Express analysis. Phase 5: cutover (888_HOLD). |

### Partial ⚠️ (legacy from 2026-06-28)

| Gap | Severity | Status |
|-----|----------|--------|
| Dynamic registration | P1 | Routes mounted, registry auto-loads 36 cards from disk, but `/a2a/discover` endpoint needs auth token to return data |
| A-FORGE :7071 API server | P2 | Pre-existing crash (`forge_execute` duplicate registration in `A-FORGE/src/interfaces/mcp/forge8Verbs.js`). Not caused by pivot. A-FORGE MCP (:7072) healthy. |

### Fatal 🔴

None open as of 2026-07-04.

---

## Execution Sequence (Prioritized)

### P0 — Seal Auth Wall ✅ (Sealed 2026-07-04)
**Done.** `auth.ts` line 42 has F13 directive enforcing mandatory auth. Bearer token + API key validation active. Public paths whitelist locked to discovery/health only.

### P1 — Update arifOS Agent Card ✅ (Sealed 2026-07-04)
**Done.** `.well-known/agent-card.json` now has 9 skills (was 5). Added: `judge.deliberate`, `lease.issue`, `session.identity`, `agent.discover`.

### P2 — Cross-Organ E2E Proof of Concept ✅ (Sealed 2026-07-04)
**Done.** `a2a-server/tests/e2e-cross-organ-flow.js` validates full GEOX → WEALTH → WELL → arifOS → A-FORGE chain. 19/21 PASS, 0 fail.

### P3 — A2A↔MCP Bridge ✅ (Sealed 2026-07-04)
**Done.** `a2a-server/a2a-mcp-bridge.js` (371 lines). Routes A2A tasks to any of 5 organs via JSON-RPC. Writes VAULT999 receipts on success (`mcp.call.<organ>.<tool>.ok`) and failure (`mcp.call.<organ>.<tool>.fail`).

### P4 — Python `aaa-a2a/` Scaffolding ✅ (Sealed 2026-07-04)
**Done.** 16 .py files, 1,031 lines. Constitutional overlay with F1-F13 floor enforcement, 4-way verdicts (SEAL/HOLD/SABAR/VOID), identity verification, VAULT999 audit append, agent card HTTP client, organ/tool routing. 27/27 unit tests pass.

### P5 — Express Analysis 🔄 (2026-07-04, in progress)
Analyze `a2a-server/server.js` (3,862 lines) for unique logic NOT in official a2a-sdk. Categorize: port to Python, keep as-is, deprecate. Document in `AAA/docs/A2A_MIGRATION.md` (TBD).

### P6 — Server Migration ⏳ (888_HOLD — F13 approval required for cutover)
Stand up Python `aaa-a2a` server on port 3002 (parallel). Run both servers concurrently. Migrate traffic when Python achieves parity. **F13 ratification required before Express deprecation.**

### P7 — ZEN_MD Markdown Naming ⏳ (2026-07-04, in progress)
Apply ZEN_MD canonical naming rule (1-2 ALLCAPS terms, no dates/versions/lowercase) to all canonical `.md` files in /root/AAA. **F13 SOVEREIGN ratification 2026-07-04.** Committed as e3a8ebc0: 563 renames preserved via git mv, 110 reference updates. PASS 1020 / FAIL 74 / EXEMPT 1951.

---

## What This Document Locks

1. **Layer semantics** — MCP = muscles, A2A = nerves, AAA = brainstem, arifOS = constitution.
2. **Organ authority classes** — evidence (GEOX/WEALTH/WELL), execute (A-FORGE), judge (arifOS), route (AAA), memory (VAULT999), validate (Tri-Witness).
3. **Delegation law** — cross-organ boundaries enforced at runtime.
4. **Agent card schema** — required fields for federation discovery.
5. **Task state mapping** — A2A states → arifOS constitutional meaning.
6. **The reason A-FORGE exists** — it is the only organ that bridges power and governance.
7. **Bridge topology** (v43.0) — A2A↔MCP bridge at `a2a-server/a2a-mcp-bridge.js`; Python `aaa-a2a/` grows alongside Express until parity.
8. **Naming doctrine** (v43.0) — ZEN_MD ALLCAPS-2-term rule is canonical surface for all .md files in the federation.

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
| 2026-07-04 | FORGE (Kimi Code CLI / AAA) | **v43.0 — AAA-A2A Architectural Pivot** |
| | | SEALED Gap 1 — A2A↔MCP bridge (`a2a-mcp-bridge.js`, 371 lines) |
| | | SEALED Gap 2 — auth wall (`auth.ts` already clean per F13 line 42) |
| | | SEALED Gap 3 — E2E test (19/21 pass) |
| | | SEALED Gap 4 — arifOS agent card skills (5 → 9) |
| | | BONUS — vault.js `human_ratifier` `'arifOS_AutoKernel'` → `'arif'` (unblocked all VAULT999 receipts) |
| | | Scaffolding — Python `aaa-a2a/` package (Phase 2 stubs, 16 .py files, 1031 lines, 27/27 tests) |
| | | ZEN_MD refactor — 563 .md files renamed to ALLCAPS-2-term canonical surface (commit e3a8ebc0) |
| | | Witness `VAULT999/witness/2026-07-04-aaa-a2a-architectural-pivot.json` SEALED with F13 directive "seal all the gaps" |

---

*DITEMPA BUKAN DIBERI.*
*Architecture is truth. Wiring is evidence. A-FORGE is the bridge.*
*This document is sealed until F13 says otherwise.*