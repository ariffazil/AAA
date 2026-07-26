# Federation Constitution Matrix — Hops, Authority, and Seals

**Version:** v2026.07.16  
**Scope:** arifOS federation — A2A mesh, AAA control plane, MCP organs, VAULT999 chain.  
**Evidence:** `AAA/.well-known/agent.json`, `AAA/a2a-server/a2a-port-map.json`, `AAA/.clinerules/30-aaa-federation.md`, `AAA/a2a-server/a2a-mcp-bridge.js`, `arifOS/.github/copilot-instructions.md`.

---

## 1. The Authority Stack

```
F13 SOVEREIGN (Arif)
        ↓  ratify / veto
888_JUDGE (arifOS :8088)
        ↓  SEAL / HOLD / SABAR / VOID
AAA CONTROL PLANE (:3001)
        ↓  display · route · queue · register
A2A MESH GATEWAY
        ↓  A2A task → MCP tool
MCP ORGANS:
  GEOX    :8081   Earth intelligence
  WEALTH  :18082 Capital intelligence
  WELL    :18083 Human readiness (reflect only)
  A-FORGE :7072  Execution shell (lease-gated)
        ↓  approved action + lease
VAULT999 (:8100 API) — immutable seal chain
```

---

## 2. Federation Nodes — Can / Cannot / Authority

| Node | Port | Status | Role | Can | Cannot | Authority / Seal |
|---|---|---|---|---|---|---|
| **F13 SOVEREIGN** (Arif) | — | LIVE | Final human veto | Ratify any SEAL; veto anything; override all tool outputs | Delegate F13 away; be automated | F13 — final |
| **arifOS** | 8088 | LIVE | Constitutional kernel | Judge; render SEAL/HOLD/SABAR/VOID; route intent; append to VAULT999; reason with F1–F13 | Execute without prior SEAL; self-authorize irreversible mutations; override F13; act as domain specialist | 888_JUDGE |
| **AAA** | 3001 | LIVE | Control plane | Display federation state; route A2A tasks; queue; register agents; host A2A gateway | Judge; seal; execute; approve mutations; expose kernel secrets | None — routing/display only |
| **A-FORGE** | 7071 / 7072 | REGISTERED | Execution shell / MCP gateway | Execute after SEAL+lease; build; deploy; shell; git | Self-approve execution; bypass arifOS; run without lease | L0–L4 lease-gated |
| **GEOX** | 8081 | LIVE | Earth intelligence | Compute seismic/basin/petrophysics evidence; return data | Make capital/execution decisions; claim truth without evidence; bypass chain | L0 evidence computation |
| **WEALTH** | 18082 | LIVE | Capital intelligence | Compute NPV/IRR/risk; conservation checks | Execute trades; bypass WELL dignity floor; bypass evidence chain | L0–L2 advisory |
| **WELL** | 18083 | DEGRADED | Human readiness | Reflect vitality/fatigue/dignity signals | Diagnose; prescribe; bypass human dignity; act without provenance | L0 reflect only |
| **VAULT999** | 8100 (API) | OPTIONAL | Immutable ledger | Append seal; verify chain; produce receipts | Delete; modify; unseal; skip cryptographic chain | Cryptographic + chain |

---

## 3. Protocol Hops — Can / Cannot

| Hop | From → To | What It Carries | Can | Cannot | Evidence Left |
|---|---|---|---|---|---|
| **P2P** | node ↔ node | Reachability | Discover, ping, transport | Authorize; semantic meaning; verdict | Transport log / health check |
| **A2A** | agent ↔ agent | Identity + task | Exchange agent cards; negotiate tasks; stream lifecycle (`submitted → working → completed/failed`) | Execute tool; access memory; render verdict | Task ID + metadata + receipt |
| **AAA route** | A2A → organ | Routing decision | Resolve `metadata.routing` + `metadata.tool` to MCP organ; validate dependency provenance | Judge the request; modify the payload | Bridge log |
| **MCP** | AAA → organ | Tool call | Call declared tool with schema; return structured result | Call undeclared tool; bypass organ authority; self-authorize | `tools/call` JSON-RPC + result |
| **arifOS judge** | evidence → verdict | Verdict | Render SEAL/HOLD/SABAR/VOID; check F1–F13; route to correct organ | Execute; self-approve; override F13 | Verdict object + violated floors |
| **A-FORGE exec** | SEAL → mutation | Approved action | Run shell/build/deploy after SEAL + lease; return execution output | Run without SEAL; run without lease | Lease + execution receipt |
| **VAULT999 seal** | verdict → chain | Irreversible record | Append cryptographic seal with BLS signature + chain hash | Delete or modify | Chain entry + `receipt_id` |

---

## 4. The Three Separation Axioms

| Axiom | Enforced By | What It Prevents |
|---|---|---|
| **Identity ≠ Authority** | Agent cards + F13 verification | A node being discoverable does not mean it can SEAL |
| **Capability ≠ Right** | arifOS `888_JUDGE` + MCP tool boundaries | Having a tool does not mean it can self-authorize mutation |
| **Route ≠ Verdict** | AAA control plane (no judge) | The router can forward but cannot decide |

---

## 5. Example Walkthrough: A Foreign Agent Requests a Capital Computation

1. **Foreign agent** discovers `arifOS Kernel` via A2A card at `/.well-known/agent.json`.
2. **A2A task** sent to `AAA:3001` with `metadata.routing = "wealth"`, `metadata.tool = "wealth_compute_npv"`, plus provenance.
3. **AAA bridge** validates dependency seal (e.g., requires GEOX `geox_subsurface_explorer` parent seal).
4. **MCP call** to `WEALTH:18082/mcp` with tool arguments.
5. **WEALTH** returns NPV computation (L0–L2 advisory).
6. **arifOS** (if requested) renders SEAL/HOLD/SABAR/VOID based on F1–F13 floors.
7. **A-FORGE** may execute only after arifOS SEAL + lease.
8. **VAULT999** appends seal/receipt with chain hash and BLS signature.

---

## 6. One-Line Summary

> **P2P is the road. A2A is the language. AAA is the traffic tower. MCP is the loading dock. arifOS is the judge. A-FORGE is the crane. VAULT999 is the deed office. F13 is the landowner.**

---

*Ditempa Bukan Diberi*
