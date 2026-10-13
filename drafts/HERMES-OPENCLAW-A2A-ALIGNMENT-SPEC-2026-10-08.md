# ARIFOS::AGY_ALIGNMENT::HERMES_OPENCLAW_A2A::v1
## Governed Multi-Organism Alignment Specification

> **Status:** RATIFIED_DRAFT · Tier A · 2026-10-08  
> **Constitutional Anchors:** Reality > Narrative · Evidence > Confidence · Capability ≠ Authority · Execution ≠ Governance · Human remains sovereign (F13)  
> **Artifact Path:** `/root/AAA/drafts/HERMES-OPENCLAW-A2A-ALIGNMENT-SPEC-2026-10-08.md`

---

## 0. Executive Invariant

$$\boxed{\text{HERMES} \perp \text{OPENCLAW} \quad \text{mediated by} \quad \text{A2A Bus} \quad \text{governed by} \quad \text{arifOS 888}}$$

- **HERMES (Y-Axis / Cognitive Plane):** Sense, Remember, Learn, Synthesize Skills, Preserve Context, Long-horizon Reasoning.
- **OPENCLAW (X-Axis / Execution Plane):** Execute, Mutate Systems, Orchestrate Worktrees, Invoke Tools, Emit Telemetry.
- **A2A (Interoperability Fabric):** Capability discovery, delegation contracts, task routing, receipts.
- **arifOS (Governance Spine):** Policy enforcement, 888 Gate, lease issuance, state transition authority, VAULT999 witness.

---

## A. Capability Graph

```text
HERMES (Cognition)                 A2A BUS (Nerves)               OPENCLAW (Actuator)
┌─────────────────────────┐        ┌──────────────────────┐        ┌─────────────────────────┐
│ • Memory Ingest (Mem0)  │        │ • Agent Card Registry│        │ • Worktree Isolation    │
│ • Long-Horizon Reason   │───────►│ • Task Delegation    │───────►│ • CLI / Tool Execution  │
│ • Skill Synthesis       │        │ • Status Callback    │        │ • System Mutation       │
│ • Epistemic Claims      │        │ • Evidence Packaging │        │ • Physical Tests (TDD)  │
│ • Proof Obligations     │        └──────────────────────┘        │ • Telemetry / Exit Codes│
└─────────────────────────┘                   ▲                    └─────────────────────────┘
             ▲                                │                                 │
             └────────────────────────────────┴─────────────────────────────────┘
                              Witness Bundle (Diff, SHA, ms)
```

---

## B. Authority Graph

1. **Hermes Authority Ceiling:** Authorized to plan, formulate claims, and draft skills. **Forbidden** from executing physical system mutation or declaring task success without receipts.
2. **OpenClaw Authority Ceiling:** Authorized to actuate commands inside bounded git worktrees under an active `X-Lease`. **Forbidden** from self-authorizing policy, bypassing 888 Gate, or deciding business intent.
3. **arifOS 888 Gate:** The sole authority for mutation leases. Validates that OpenClaw's physical evidence satisfies Hermes' proof obligations before granting a **`SEAL`**.

---

## C. Delegation Graph

```text
1. [HERMES] ── Formulate Plan + Proof Obligations ──► [A2A Envelope]
2. [A2A Envelope] ── Request Lease ──► [arifOS 888 Gate]
3. [arifOS 888 Gate] ── Issue X-Lease ──► [OPENCLAW]
4. [OPENCLAW] ── Execute in Worktree + Run Tests ──► Produce Diff & Telemetry
5. [OPENCLAW] ── Submit Witness Bundle ──► [arifOS 888 Gate]
6. [arifOS 888 Gate] ── Verify Invariants:
       ├── If TRUE ──► Issue SEAL ──► Merge Branch ──► [HERMES Memory Commit]
       └── If FALSE ──► Issue HOLD ──► Auto-Revert ──► [HERMES Re-plan]
```

---

## D. Conflict Surface Analysis

- **Tool Duplication:** Strip shell actuation tools from Hermes; route all physical tasks to OpenClaw.
- **Success Hallucination:** Hermes is barred from reporting completion without an A2A-signed witness receipt.
- **Context Pollution:** OpenClaw retains zero conversational memory across runs; memory belongs exclusively to Hermes.
- **Blast Radius:** OpenClaw runs in isolated git worktrees; out-of-bounds mutation aborts the lease immediately.

---

## E. A2A Integration Strategy

- **Agent Cards:** Registered at `/root/.hermes/agent-card.json` and `/root/.openclaw/agent-card.json`.
- **Contracts:** JSON-schema validated work orders with explicit `proof_obligations`, `timeout_seconds`, and `rollback_sha`.
- **Receipts:** Signed witness objects with `exit_code`, `latency_ms`, `commit_sha`, and `falsifier_logs`.

---

## F. Minimal Alignment Roadmap

1. **Step 1 (T+24h) Boundary Clamp:** Disable direct shell mutations in Hermes when OpenClaw is present.
2. **Step 2 (T+48h) Agent Cards & Transport:** Bind local A2A endpoints over loopback IPC.
3. **Step 3 (T+72h) 888 Lease Gate:** Require cryptographic `lease_id` before OpenClaw executes.
4. **Step 4 (T+96h) Closed Memory Loop:** Auto-metabolize OpenClaw witness receipts into Hermes `state.db`.

DITEMPA BUKAN DIBERI ⚒️
