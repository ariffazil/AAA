# FLOW_MAP — Phase D Flow Integrity Audit

**Program:** Entropy Reduction (Phases C+D) · arifOS Federation
**Node:** KVM8 forge (100.64.0.2) · :8088 kernel · :7072 A-FORGE · :7074 FED
**Date:** 2026-09-14 · Asia/Kuala_Lumpur
**Method:** source trace + live probe. Every edge is cited `file:line` or observed live.
**Companion:** **[FLOW_GAPS.md](./FLOW_GAPS.md)** — the full 18-gap register (embedded summary in §5).

---

## 1. The canonical flow (as doctrine)

```
 Intent → Proposal → Verification → Judgment → Execution → Receipt → Witness
```

Kernel canonical stages (`arifOS/arifosmcp/runtime/run_envelope.py:45–66`):

```
INIT → OBSERVE → EVIDENCE → THINK → ROUTE → MEMORY → JUDGE → FORGE → VERIFY_CONSEQUENCE → RECEIPT
```

The 8 exposed kernel tools map onto these stages (`run_envelope.py:73–84`):

| Stage | Tool |
|---|---|
| INIT | `arif_init` |
| OBSERVE + EVIDENCE | `arif_observe` |
| THINK | `arif_think` |
| ROUTE | `arif_route` |
| MEMORY | `arif_memory` |
| JUDGE | `arif_judge` |
| FORGE + VERIFY_CONSEQUENCE | `arif_forge` |
| RECEIPT | `arif_seal` |

There is **no kernel tool for `Witness`.** Witness is a downstream reader (VAULT999 / FRAME :18085), not a stage in the envelope.

---

## 2. Live flow (observed)

```
                         ┌──────────────────────────────────────────────┐
  Human / agent          │  arifOS kernel  :8088   (8 exposed tools)     │
      │                  │  floors 13/13 · registry 62 · declared 48     │
      │  arif_init ─────►│  [000 INIT]        ── session + SCT/ACT mint  │
      │                  │  [111 OBSERVE]  ◄── arif_observe              │
      │                  │  [333 THINK]    ◄── arif_think                │
      │                  │  [444 ROUTE]    ◄── arif_route                │
      │                  │  [555 MEMORY]   ◄── arif_memory               │
      │                  │  [666 JUDGE]    ◄── arif_judge  ── verdict     │
      │                  │  [777 FORGE]    ◄── arif_forge   ✖ CLOSED      │  G-01
      │                  │  [999 RECEIPT]  ◄── arif_seal ──► VAULT999:5001│
      │                  └──────────────────────────────────────────────┘
      │                                    │
      │                    (execution crosses organ boundary here)
      ▼                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ A-FORGE  :7072   (120 tools)  authority_ceiling 777_FORGE                │
│                                                                           │
│  IntentRouter ──► GovernanceBridge ──► FloorEnforcer / PreForgeGateClient  │
│                                            │                              │
│                                            ├─► forge_verify  ✖ INCONCLUSIVE   G-08
│                                            ├─► ApprovalBoundary  ✖ orphaned   G-07
│                                            ├─► HumanEscalationClient ✖ no-op  G-06
│                                            │                              │
│                                            ▼                              │
│   forge_synthesize → stage → sandbox_run → scar_scan → skillstore_sync     │
│        → tier_bind → docket_prep → forge_execute                          │
│                                        │   ✖ raw `bash` (no sandbox)  G-04 │
│                                        ▼                                   │
│                        Cross-Organ ACT Ingress  actIngress.ts              │
│                                        │                                   │
│                        emitAForgeReceipt ──► arifFLOW :7073                │
│                                        └─(fail)► local JSONL, no sweeper G-13│
└───────────────────────────────────────────────────────────────────────────┘
                                     │
      ┌──────────────────────────────┼──────────────────────────────┐
      ▼                              ▼                              ▼
  GEOX :8081                    WELL :18083                    WEALTH :18082
  100 live / 26 canonical       degraded, REFLECT_ONLY          healthy
  ✖ SURFACE_DRIFT  G-16         ✖ no state  G-17
      │                              │                              │
      └──────── gate_tool_ingress (AAA) ──────┴──────────────────────┘
                                     │
                    ✖ fail-open: forged ACT accepted as SOVEREIGN   G-09
                                     │
      ┌──────────────────────────────┼──────────────────────────────┐
      ▼                              ▼                              ▼
 FED :7074                    VAULT999 :5001                  FRAME :18085
 ADVISORY_ONLY                vault_seals_count 12            independent observer
 ✖ never blocks  G-18         (Witness terminal)
```

---

## 3. Node table

| # | Node | Implemented at | Live state | Gap |
|---|---|---|---|---|
| N1 | Intent | `A-FORGE/src/domain/engine/IntentRouter.ts`; `arif_init` | ok | — |
| N2 | Proposal | `arif_think`, `arif_route` | ok | — |
| N3 | Verification | `arif_observe`; `forge_verify.ts` | kernel ok · A-FORGE **INCONCLUSIVE always** | G-08 |
| N4 | Judgment | `arif_judge`; `FloorEnforcer`, `McpPolicyGate` | ok | — |
| N5 | Execution (kernel) | `arif_forge` | **HALTED** — `mode="query"` only | G-01 |
| N5b | Execution (forge) | `forge_execute`, `forge_sandbox_run` | runs raw `bash`, no sandbox | G-04, G-05 |
| N6 | Receipt | `arif_seal` → VAULT999; `flowEmit.ts` → arifFLOW | kernel ok · forge fallback never replayed | G-12, G-13 |
| N7 | Witness | VAULT999 reader; FRAME :18085 | nominal — position not recorded | G-14 |
| N8 | Gate (ingress) | `federation_act.py::gate_tool_ingress` | fail-open on forged token | G-09, G-10 |
| N9 | Approval (human) | `approval/*` | **no-op** | G-06, G-07 |

---

## 4. Edge table

| Edge | Path | Status |
|---|---|---|
| Intent → Proposal | `arif_init` → `arif_think` | **OK** |
| Proposal → Verification | `arif_think` → `arif_observe` | **OK** |
| Verification → Judgment | `forge_verify` → judge | **BROKEN** — verifier always INCONCLUSIVE (G-08) |
| Judgment → Execution (kernel) | `arif_judge` SEAL → `arif_forge` | **BROKEN** — kernel forge boundary CLOSED (G-01) |
| Judgment → Execution (forge) | `arif_judge` SEAL → A-FORGE `forge_execute` | **PARTIAL** — requires VAULT999 seal, then runs unsandboxed (G-04) |
| Execution → Receipt (kernel) | `arif_forge` → `arif_seal` → VAULT999 | **OK** where it applies |
| Execution → Receipt (forge) | `forge_execute` → `flowEmit` | **PARTIAL** — phantom receipt (G-05); local-only fallback (G-13) |
| Receipt → Witness | VAULT999 → reader | **NOMINAL** — no position recorded (G-14) |
| Any → Approval | `AWAIT_APPROVAL` → human | **DEAD** (G-06) |
| Cross-organ ingress | SCT/ACT gate | **BYPASSABLE** (G-09) |
| Seal (alt path) | `forge_seal_lane_a` | **BYPASS** — skips `arif_seal` HOLD (G-11) |

---

## 5. Flow gaps — embedded register (full detail in [FLOW_GAPS.md](./FLOW_GAPS.md))

| ID | Class | One-line | Cite |
|---|---|---|---|
| G-01 | DEAD_END | kernel Execution stage closed (`mode="query"` only) | `arifOS/arifosmcp/tools/forge.py:382` |
| G-02 | DEAD_GATE | kernel state machine disabled by default | `arifOS/.../runtime/executor.py:23` |
| G-03 | DEAD_GATE | A-FORGE `runStage()` is a timer only | `A-FORGE/.../metrics/prometheus.ts:79` |
| G-04 | SHADOW_EXECUTION | `forge_sandbox_run`/`forge_execute` run raw `bash`; sandbox imported, never called | `A-FORGE/.../mcp/forge8Verbs.ts:382,780` |
| G-05 | PHANTOM_RECEIPT | governance path returns receipt, spawns nothing | `A-FORGE/.../mcp/forge8Verbs.ts:670–706` |
| G-06 | DEAD_END | human escalation is an empty method | `A-FORGE/.../approval/index.ts:146` |
| G-07 | BYPASS | `ApprovalBoundary` marked REPLACED but still used | `A-FORGE/.../personal-v2/PersonalOS.ts:88` |
| G-08 | DEAD_END | `forge_verify` always INCONCLUSIVE | `A-FORGE/.../tools/forge_verify.ts:123,139` |
| G-09 | BYPASS | forged ACT accepted as SOVEREIGN (4/6 proven) | `AAA/governance/federation_act.py:389–417` |
| G-10 | LOOP_BREAK | three token parsers, three grammars | `federation_act.py:37,296` · `actIngress.ts:25` |
| G-11 | BYPASS | `forge_seal_lane_a` skips `arif_seal` HOLD | `A-FORGE/.../mcp/sealLaneA.ts:4` |
| G-12 | DEAD_END | `_SEAL_BUFFER` never flushed | `arifOS/.../runtime/context_audit.py:219,379` |
| G-13 | RECEIPTLESS | arifFLOW fallback has no sweeper | `A-FORGE/.../receipts/flowEmit.ts:8–9` |
| G-14 | DEAD_END | witness position not recorded → self-attestation looks external | `arifOS/.../runtime/witness_class.py:5` |
| G-15 | LOOP_BREAK | HOLD/VOID flattened to "ERROR" | `A-FORGE/.../governance/verdict-interceptor.ts:53–63` |
| G-16 | LOOP_BREAK | GEOX surface drift 100 live / 26 canonical | live `geox-mcp` journal, 2026-09-14 |
| G-17 | DEAD_END | WELL degraded, REFLECT_ONLY, `/metrics` 404 | live `:18083/health` |
| G-18 | DEAD_GATE | FED advisory by construction (never blocks) | live `:7074/health` |

**Total: 18 gaps.**

---

## 6. What the flow actually is (honest summary)

- **Intent → Proposal → Receipt** works at the kernel for read-only and advisory work.
- **Execution** does not happen at the kernel. It crosses to A-FORGE, where it is authorized by a VAULT999 seal and then run as raw shell — declared sandboxed, actually not.
- **Verification** carries no signal: `forge_verify` is a permanent INCONCLUSIVE.
- **Approval** never reaches a human: `escalate()` is empty.
- **Witness** cannot tell a closed loop from an open one: position is not recorded.
- **The ingress gate that protects three organs** accepts a forged token whenever the kernel answers quickly enough.

The entropy is not in the doctrine. The doctrine is coherent. The entropy is in the **distance between the names the system uses and the behaviour the system performs** — which is exactly what Phase C measured.
