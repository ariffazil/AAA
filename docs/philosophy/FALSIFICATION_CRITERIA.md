# FALSIFICATION_CRITERIA.md — What Would Convince Us That arifOS Is Wrong?

> **Sovereign Ratification:** 2026-06-29  
> **Source:** F13 Sovereign Feedback & Critique  
> **Status:** Live Constitutional Falsification Protocol  

To build for active criticism rather than applause, arifOS must maintain clear, empirical falsification criteria. This document defines the conditions under which core architectural assumptions and guarantees must be deemed invalid and redesigned.

---

## 1. Core Assumption Falsification

### 1.1 Human-in-the-Loop Gating (F13 Veto)
*   **Assumption:** A human operator (Sovereign) can reliably audit and gate all high-risk, irreversible operations.
*   **Falsification Criteria:** 
    *   **Cognitive Surrender:** Sovereign registers "ambient approval" (auto-clicking approvals without validation) due to alert fatigue.
    *   **System Deadlock:** Critical survival actions are blocked indefinitely under operational emergency because the human veto loop cannot close within task-lease duration.
*   **Response:** Pivot to automated rule-based constraints (invariant-triggered auto-rejection) while restricting human gates to a minimal, high-latency security tier.

### 1.2 The Refusal Kernel ("Governance First")
*   **Assumption:** Prioritizing refusal over completion increases total system safety and reliability.
*   **Falsification Criteria:** 
    *   **User Bypass:** Governance-enforced refusal rates or operational latency exceed the usability threshold, forcing operators to execute tasks manually outside the managed framework.
*   **Response:** Redesign the policy interpreter to introduce a "simulate-with-shadow-governance" dry-run mode, easing strict blockades while preserving telemetry.

### 1.3 Opacity of Agent Execution
*   **Assumption:** Opacity of the "how" (internal execution model) protects agent integrity while A2A handles "what" (interface).
*   **Falsification Criteria:** 
    *   **Verification Blindness:** Inter-agent diagnostic failures cannot be resolved without access to the execution trace, rendering A2A interfaces untestable.
*   **Response:** Standardize and expose structured, scrubbed runtime trace schemas through `/a2a` task status queries.

---

## 2. Guarantees vs. Aspirations

We explicitly split our current claims into two categories:

| Claims | Status | Current Proof / Verification |
| :--- | :--- | :--- |
| **A-FORGE rejects tasks lacking valid SEAL** | **PROVEN** | Enforced structurally at the execution interface; verified by `tests/mcp_cognitive_test_harness.py`. |
| **State transitions are auditable and tamper-evident** | **PROVEN** | Implemented via append-only Vault999 receipts; verified by cryptographic signature chain verification. |
| **Distributed Federation is perfectly synchronized** | *ASPIRATIONAL* | Stated under F2 (Truth) but bounded by real-time network lag. Currently requires local validation checks before mutations. |
| **Zero dry wells / zero operational failures** | *ASPIRATIONAL* | Bounded by the quality of specialist evidence input (GEOX/WEALTH). |

---

## 3. Redesign Triggers
The constitutional floors must undergo major revision if:
1.  **Floor Latency:** Pre-execution governance validation takes longer than 2.0 seconds, degrading active tab interface response.
2.  **Floor Leakage:** An irreversible state mutation is executed by A-FORGE without generating a matching Vault999 receipt (complete failure of F11 Auditability).
