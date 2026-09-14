# Path-5 Capability Inventory & Component Map
**Document:** `PATH5_CAPABILITY_MAP.md`  
**Standard:** QQQ Protocol · F1 Truth · No Pretending  
**Date:** 2026-09-14T09:47:00+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::PATH5_OPERATIONALIZATION::v1`

---

## 1. Subsystem Inventory Matrix

| Subsystem Component | Existing Path / Reference | Classification | Evidence & Defect Analysis |
|---|---|---|---|
| **1. Lease Engine (APA)** | `/root/A-FORGE/leases/lease_engine.py` | **PARTIAL** | Basic `request()`, `activate()`, `validate()`, `revoke()` prototype exists in Python. Stores to `/root/A-FORGE/leases/lease_store.jsonl`. **Defects:** No heartbeat mechanism, no automatic TTL expiration loop, not integrated into file mutation or Git actuators. |
| **2. Capability Token (ACT)** | Kernel `:8088` `arif_init` (`act_v1.*`) | **EXISTS** | Issues deterministic, signed cryptographic capability claims with `allowed` verb arrays and APEX scalar bounds. |
| **3. Worktree Sensor** | `/root/A-FORGE/src/interfaces/mcp/gatewayTools.ts:882` (`forge_worktree`) | **PARTIAL** | OBSERVE-class physics sensor. Accurately reports branch, ahead/behind, stash, dirty files, conflicts, and blast radius. **Defects:** Read-only; lacks lifecycle operations (`create`, `resume`, `archive`, `destroy`). |
| **4. Native Worktree Engine** | Git core binary (`git worktree`) | **EXISTS** | Verified working (`git -C /root/arifOS worktree list`). High stability, kernel-level atomic directory links. |
| **5. Ad-Hoc Swarm Worktrees** | `/root/forge_work/worktrees/` | **PARTIAL** | Directory exists with prior manual session worktrees (`RG2-HEAD-VERIFY-*`). **Defects:** No programmatic manager, no lease-binding, manual pruning required. |
| **6. Reconciler Pipeline** | N/A (Manual git merge currently) | **MISSING** | No automated institutional agent/service executing: `diff → policy check → drift guard → unit tests → reconcile → merge → receipt`. |
| **7. Drift Protection** | `arifOS/tests/runtime/test_gate_2d_sensitive_path.py`<br>`AAA/tests/hooks/test_agentic_hooks_suite.py` | **EXISTS** | Gate 2d blocks sensitive paths (11 paths, F12). Hook suite (94 tests) enforces pre/post gate invariant. |
| **8. Receipt & Witness Chain** | `arifFlow` (`:7073/ingest`), `VAULT999` (`/root/.local/share/arifos/vault999/outcomes.jsonl`) | **EXISTS** | Receipt emission functional and witnessed in live session boot. |

---

## 2. Summary of Gaps to Bridge

1. **Lease Gap:** Bridge `lease_engine.py` into a unified CLI/service with heartbeat, auto-expiration, and hard gate enforcement.
2. **Worktree Lifecycle Gap:** Implement programmatic lifecycle wrapper (`worktree_create`, `worktree_resume`, `worktree_archive`, `worktree_destroy`) mapped to `/root/forge_work/worktrees/<lease_id>`.
3. **Reconciler Gap:** Build the automated A-FORGE Reconciler pipeline with pre-merge test verification and zero direct-to-main mutation bypass.
4. **Governance Gaps:** Formalize Domain Stewardship (semantic conflicts) and Merge Queue Limits (flood control).
