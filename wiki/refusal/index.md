---
title: "Refusal: The Missing Runtime Object"
description: "Specification of the prospective refusal object as a bounded execution gate, distinct from retrospective receipts and numeric consent scores."
type: concept
tags: [refusal, governance, consequence, runtime]
confidence: high
---

# Refusal: The Missing Runtime Object

!!! warning "Status: Proposed Runtime Object"
    **Classification:** `PROPOSED_OPERATIONAL_INVARIANT`  
    **Live Runtime Enforcement:** `NOT YET DEMONSTRATED`  
    This specification represents an engineering target, not currently deployed runtime capability. No mathematical physics, scalar consent scores, or formulaic authority are asserted.

---

## 1. Why a Receipt is Not Consent

A machine receipt records that an action occurred, which command was executed, or which internal gate evaluated the payload. 

- **A written receipt is not proof of human consent.**
- **Absence of refusal is not consent.**
- **A named bearer after the consequence has landed is not prospective sovereignty.**

Recording history protects evidence; it does not protect the person who bears the consequence if they were never given the power to stop the machine before execution.

---

## 2. Refusal as a Signed Bounded State

Refusal cannot be modeled as a continuous probability, a floating-point score, or a self-attested boolean flag (`prospective_veto: true`).

It must exist as an authenticated, discrete data object:

```json
{
  "refusal_id": "ref-20261028-001",
  "bearer_id": "human:consequence_bearer_identifier",
  "scope": "domain_or_action_mutation_boundary",
  "position": "NO",
  "issued_at": "2026-10-28T02:00:00Z",
  "signature": "cryptographic_or_authenticated_channel_proof",
  "provenance": {
    "channel": "authenticated_human_membrane",
    "verified_by": "independent_external_witness"
  }
}
```

---

## 3. Scope Overlap and Physical Execution Blocking

A refusal object acts as a physical logic gate positioned directly before the actuator (e.g. A-FORGE):

```text
                     [ Proposed Consequential Action ]
                                     │
               Is consequence-bearer named in advance?
                              ├── NO  ──► HOLD (BEARER_UNKNOWN)
                              └── YES
                                     │
           Is an active Signed Refusal Object registered?
                              ├── YES ──► HOLD (EXECUTION_BLOCKED)
                              └── NO
                                     │
                                     ▼
                  Pass to standard governance evaluation
              (Does NOT authorize execution; only permits review)
```

**Cardinal Rule:** A refusal gate may block execution; it may never authorize execution.

---

## 4. Refusal Persistence

A valid human refusal must survive system restarts, session clears, network outages, and agent context compaction. 

If an agent can "forget" a human refusal simply because a new conversation starts, or because an LLM summarizer truncates context, the refusal is non-binding. Refusal states must be written to durable, append-only local storage and checked synchronously prior to any state mutation.

---

## 5. Absence of Refusal is Not Consent

If a consequence-bearer cannot be reached, is unaware of the proposed action, or does not respond, the system **cannot** interpret silence as approval. 

Silence is an unverified state:
- `RESPONSE_RECEIVED: FALSE`
- `GOVERNANCE_ACTION: HOLD`

Execution may only proceed when affirmative, authenticated authority exists within the declared authority envelope.

---

## 6. Required Tests Before Activation

Before this mechanism can be moved from `PROPOSED` to `DEPLOYED`, three falsification tests must pass:

1. **Persistence Test:** A signed refusal survives a VPS service restart and agent harness reset without loss.
2. **Actuator Enforcement Test:** A-FORGE physical execution halts deterministically when a refusal scope matches the mutation target.
3. **Non-Override Test:** No automated agent, LLM prompt optimization, or high governance score can bypass an active bearer refusal.
