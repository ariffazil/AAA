# KERNEL_HASI_APEX — Sovereign Interface Specification

**Status:** PENDING | **Version:** v0.1-DRAFT
**Authority:** arifOS Governance Kernel

> ⚠️ **STUB NOTICE:** This document is a placeholder. The full SI spec is pending 888_JUDGE ratification.
> The Apex Dashboard (`apex_dashboard_widget.py`) exists as a UI layer but is NOT the Sovereign Interface.
> SI = contracted organ (protocol + API + invariants), not a React/Streamlit widget.

---

## Purpose

The Sovereign Interface (SI) is the constitutional organ through which the human sovereign:
- Views the live Nine-Signal Matrix
- Reviews and acts on pending 888_HOLDs
- Approves or rejects Plans from the Planning Organ
- Exercises F13 hard veto

---

## Minimum Viable SI Contract (TODO)

```yaml
si_contract:
  endpoints:
    nine_signal_matrix: GET /si/matrix       # live system state
    pending_holds: GET /si/holds             # queue of 888_HOLD items
    plan_queue: GET /si/plans?status=PENDING_APPROVAL
    approve_plan: POST /si/plans/{id}/approve
    reject_plan: POST /si/plans/{id}/reject
    veto: POST /si/veto                      # F13 hard veto
  invariants:
    - sovereign_id must be verified on all writes
    - veto is unconditional and immediate
    - holds queue must be real-time (< 5s latency)
```

---

## Open Questions

1. Authentication: what verifies sovereign identity? (F0/F13 binding)
2. Notification: push vs pull for pending 888_HOLDs?
3. Scope: does SI surface only Planning Organ items, or all F1-F13 governance events?

---

*This stub is addressable. Contributors implement against this contract.*
