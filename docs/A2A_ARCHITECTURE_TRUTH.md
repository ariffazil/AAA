# A2A Architecture Truth — Gap Analysis

> **Status:** AUDIT REPORT — not a SEAL.  
> **Date:** 2026-06-28  
> **Auditor:** FORGE (000Ω)  
> **Sovereign:** Muhammad Arif bin Fazil (F13)  
> **DITEMPA BUKAN DIBERI**

---

## 1. Executive Summary

The corrected doctrine is **architecturally aligned** with the current codebase:

```text
ARIF / F13
    ↓
AAA A2A Mesh (coordination, discovery, task routing)
    ↓
Organ Agents (arifOS, GEOX, WEALTH, WELL, A-FORGE, VAULT)
    ↓
MCP Tool Servers (under each organ)
```

However, the **implementation is ahead of the organs**. AAA has a live A2A gateway, but most organ agents are not yet reachable through A2A. The nervous system exists; the organs have not all grown nerves.

**Bottom line:** The topology is correct. The wiring is incomplete.

---

## 2. The Doctrine (8 Civilizational Organs)

| Organ | Function | arifOS Mapping |
|-------|----------|----------------|
| **SENSE** | Reality intake | `arif_observe`, `arif_explore`, GEOX sensors, market feeds |
| **MEMORY** | Continuity + provenance | VAULT999, SkillStore, Qdrant, A-ARCHIVE |
| **REASON** | Model the situation | `arif_think`, 333-AGI |
| **JUDGE** | Decide what is allowed | `arif_judge`, 888-APEX, F1-F13 |
| **FORGE** | Build capability | A-FORGE, `forge_*` tools |
| **ACT** | Execute approved action | `arif_act`, `forge_execute`, organ MCP calls |
| **WITNESS** | Independent validation | Tri-Witness (Human × AI × Earth) |
| **SCAR / VAULT** | Learn from failure | VAULT999 immutable receipts, SCAR law |

The loop:

```text
SENSE → MEMORY → REASON → JUDGE → FORGE → ACT → WITNESS → SCAR/VAULT
```

---

## 3. Current State — What Exists

### 3.1 AAA A2A Mesh (LIVE)

- **Server:** `AAA/a2a-server/server.js` on port `:3001`
- **Endpoints:**
  - `POST /a2a/tasks/send`
  - `GET /a2a/tasks/:taskId`
  - `POST /a2a/tasks/:taskId/cancel`
  - `GET /a2a/tasks/:taskId/subscribe`
  - `POST /a2a/message/send`
  - `POST /a2a/message/stream`
- **Discovery:** `/.well-known/agent-card.json`, `/a2a/agent-card.json`, `/.well-known/a2a-discovery.json`
- **Mesh health:** `/api/mesh/state` + `mesh_coordinator.js`
- **Agent cards:** `AAA/a2a-server/agent-cards/` (HEXAGON + tool agents + organ stubs)
- **Reality gating:** `arep-task-manager.js` probes all 6 organs and seals outcomes to VAULT999
- **Witness bridge:** `preforge_bridge.js` registers HUMAN / AI / EARTH witnesses

### 3.2 Organ Agent Cards (EXIST)

| Organ | Card Location | Live Endpoint | Status |
|-------|---------------|---------------|--------|
| arifOS | `AAA/a2a-server/agent-cards/organs/arifos.json` | `:8088/.well-known/agent-card.json` | ✅ Live |
| A-FORGE | `AAA/a2a-server/agent-cards/organs/aforge.json` | `:7071/.well-known/agent-card.json` | ✅ Live |
| GEOX | `AAA/a2a-server/agent-cards/organs/geox.json` | `:8081/.well-known/agent-card.json` | ❌ Not live |
| WEALTH | `AAA/a2a-server/agent-cards/organs/wealth.json` | `:18082/.well-known/agent-card.json` | ❌ Not live |
| WELL | `AAA/a2a-server/agent-cards/organs/well.json` | `:18083/.well-known/agent-card.json` | ❌ Not live |
| VAULT | `AAA/a2a-server/agent-cards/organs/` (no json?) | `:5001/.well-known/agent-card.json` | ❌ Not live |

### 3.3 Peer Contracts (PARTIAL)

Location: `AAA/a2a/peer-contracts/`

| Contract | Status |
|----------|--------|
| `aaa-gateway.json` | ✅ Exists |
| `arifos-kernel.json` | ✅ Exists |
| `a-forge-executor.json` | ✅ Exists |
| `geox-*.json` | ❌ Missing |
| `wealth-*.json` | ❌ Missing |
| `well-*.json` | ❌ Missing |

### 3.4 Federation Envelope (IMPLEMENTED)

`federation_envelope.js` validates:
- Authority source (token, session, delegated, human_888)
- Action class mapping (OBSERVE, MUTATE, ATOMIC)
- observe-before-mutate receipt requirement
- WELL biometric pacing (decision fatigue, cognitive load)
- Allowed tools per policy (omega-forge, etc.)

### 3.5 Mesh Coordinator (IMPLEMENTED)

`mesh_coordinator.js` tracks:
- Organ heartbeats and staleness
- Repeated HOLD counts
- Floor breach bursts
- Mesh gradient status

---

## 4. Gap Matrix

| # | Gap | Severity | Status | Evidence |
|---|-----|----------|--------|----------|
| 1 | **4 organs lack live `/.well-known/agent-card.json`** | HIGH | ❌ Open | GEOX, WEALTH, WELL, VAULT do not serve agent cards on their ports |
| 2 | **3 peer contracts missing** | HIGH | ❌ Open | No GEOX/WEALTH/WELL peer contracts in `AAA/a2a/peer-contracts/` |
| 3 | **Delegation law not enforced in code** | HIGH | ❌ Open | Rules are prose only; no runtime ACL engine |
| 4 | **Dynamic registration returns empty** | MEDIUM | ❌ Open | `/a2a/agents.json` requires auth; live registry probe empty |
| 5 | **Agent cards don't declare owned MCP tools** | MEDIUM | ❌ Open | Organ agent cards lack `owned_mcp` section |
| 6 | **arifOS agent card is MCP-centric** | MEDIUM | ❌ Open | `arifOS/static/agent-card.json` advertises `mcp_endpoint`, not A2A judge skills |
| 7 | **Tri-Witness not a first-class A2A task type** | MEDIUM | ❌ Open | Witness exists via preforge bridge, but no `tasks/send` skill for validation |
| 8 | **No end-to-end cross-organ A2A example** | MEDIUM | ❌ Open | No test/demo for GEOX → WEALTH → WELL → HOLD |
| 9 | **A2A auth dev bypass** | LOW | ⚠️ Open | `AAA/src/gateway/auth.ts` allows `NODE_ENV === 'development'` |
| 10 | **VAULT999 sealing not universal** | LOW | ⚠️ Partial | Only AREP tasks seal; plain A2A tasks may skip receipt |

---

## 5. Per-Gap Detail

### Gap 1 — 4 Organs Missing Live Agent Cards

**What should happen:** Every organ serves `/.well-known/agent-card.json` at its runtime port so AAA can discover and delegate to it.

**What happens now:**
- `arifOS :8088` ✅ serves agent card
- `A-FORGE :7071` ✅ serves agent card
- `GEOX :8081` ❌ 404
- `WEALTH :18082` ❌ 404
- `WELL :18083` ❌ 404
- `VAULT999 :5001` ❌ 404

**Impact:** AAA cannot route tasks to GEOX/WEALTH/WELL as A2A agents. They are only reachable as MCP servers from a client that already knows them.

**Fix:** Add static agent-card.json serving to each organ's HTTP server. No new ports needed.

---

### Gap 2 — Missing Peer Contracts

**What should happen:** Each organ pair has a peer contract defining allowed delegation, action classes, and trust tiers.

**What happens now:** Only 3 contracts exist (aaa-gateway, arifos-kernel, a-forge-executor). GEOX/WEALTH/WELL have no contracts.

**Impact:** Cross-organ delegation defaults to ad-hoc or unvalidated trust.

**Fix:** Create `geox-peer.json`, `wealth-peer.json`, `well-peer.json` under `AAA/a2a/peer-contracts/`.

---

### Gap 3 — Delegation Law Not Enforced

**What should happen:** Runtime ACL prevents invalid delegations (e.g., WELL cannot execute, GEOX cannot mutate WEALTH records).

**What happens now:** Rules exist in agent-card prose and `agent-state/schemas.js`, but no runtime enforcer blocks bad delegation.

**Impact:** A compromised or misconfigured agent could delegate outside its authority.

**Fix:** Implement a `DelegationEnforcer` middleware in AAA A2A task routing.

---

### Gap 4 — Dynamic Registration Empty

**What should happen:** `/a2a/agents.json` returns the live federation registry.

**What happens now:** Endpoint requires auth and returns empty or unauthorized in probes.

**Impact:** External agents cannot discover the federation without pre-shared knowledge.

**Fix:** Make discovery surface public-read (per A2A spec) and populate from registry.

---

### Gap 5 — Agent Cards Don't Declare Owned MCP Tools

**What should happen:** Each organ agent card lists its owned MCP servers and tools (without exposing internal schemas).

**What happens now:** Agent cards describe skills but not owned MCP surfaces.

**Impact:** AAA cannot reason about which organ can satisfy a tool need.

**Fix:** Add `owned_mcp` block to organ agent cards.

---

### Gap 6 — arifOS Agent Card MCP-Centric

**What should happen:** arifOS advertises A2A judge skills (authority check, floor validation, verdict).

**What happens now:** `arifOS/static/agent-card.json` is MCP-centric (`role: mcp_kernel`).

**Impact:** Other agents discover arifOS as a tool server, not a constitutional judge.

**Fix:** Update arifOS agent card to A2A v1.0 format with judge skills.

---

### Gap 7 — Tri-Witness Not an A2A Task Type

**What should happen:** A2A has a `witness` skill/task type that runs Human × AI × Earth validation.

**What happens now:** Witness events are registered via `preforge_bridge.js`, but there is no standalone A2A witness workflow.

**Impact:** Witness is a side effect, not a first-class civilizational organ.

**Fix:** Add a Witness Agent Card and `/a2a/tasks/send` skill for tri-witness validation.

---

### Gap 8 — No End-to-End Cross-Organ Example

**What should happen:** There is a documented, tested example of a task moving across organs.

**What happens now:** No such example exists in tests or docs.

**Impact:** The mesh is unproven in practice.

**Fix:** Create a proof-of-concept: PETRONAS risk analysis task flowing through GEOX → WEALTH → WELL → arifOS judge.

---

### Gap 9 — A2A Auth Dev Bypass

**What should happen:** Bearer token or API key is always required.

**What happens now:** `NODE_ENV === 'development'` bypasses auth.

**Impact:** Production could accidentally run in dev mode.

**Fix:** Remove dev bypass or require explicit `A2A_DEV_AUTH_BYPASS=true` with logging.

---

### Gap 10 — VAULT999 Sealing Not Universal

**What should happen:** Every completed A2A task writes a receipt.

**What happens now:** Only AREP tasks explicitly seal. Plain A2A tasks may not.

**Impact:** Incomplete audit trail for federation actions.

**Fix:** Add default receipt writing to all `/a2a/tasks/send` completions.

---

## 6. Recommended Fix Priority

### P0 — Block Federation Operation Until Done

1. **Gap 1:** Serve agent cards from GEOX, WEALTH, WELL, VAULT
2. **Gap 3:** Implement runtime delegation law enforcement

### P1 — Required for Civilization-Grade Mesh

3. **Gap 2:** Create GEOX/WEALTH/WELL peer contracts
4. **Gap 6:** Update arifOS agent card to A2A judge format
5. **Gap 5:** Add `owned_mcp` declarations to organ agent cards

### P2 — Hardening + Demonstration

6. **Gap 7:** Make Tri-Witness an A2A task type
7. **Gap 8:** Build end-to-end cross-organ task example
8. **Gap 4:** Fix dynamic registration
9. **Gap 9:** Remove dev auth bypass
10. **Gap 10:** Universal VAULT999 receipts

---

## 7. Evidence Paths

```
AAA/a2a-server/server.js                 # A2A task endpoints
AAA/a2a-server/mesh_coordinator.js       # mesh health, HOLD tracking
AAA/a2a-server/arep-task-manager.js      # task lifecycle + VAULT999 seal
AAA/a2a-server/federation_envelope.js    # authority + floor validation
AAA/a2a-server/preforge_bridge.js        # witness registration
AAA/a2a/peer-contracts/                  # existing peer contracts
AAA/a2a-server/agent-cards/organs/       # organ agent card stubs
AAA/src/gateway/auth.ts                  # A2A auth middleware
arifOS/static/agent-card.json            # MCP-centric arifOS card
arifOS/arifosmcp/transport/a2a.py        # arifOS A2A transport
A-FORGE/test/a2a.test.ts                 # A2A conformance tests
```

---

## 8. One-Line Verdict

> **The architecture is correct. The wiring is 60% done. The remaining 40% is making every organ discoverable, delegatable, and accountable through A2A.**

DITEMPA BUKAN DIBERI.
