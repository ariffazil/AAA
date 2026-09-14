# Federation Naming Refrigerator (Phase B)
**Document:** `NAMING_REFRIGERATOR.md`  
**Standard:** QQQ Protocol · One Concept, One Name  
**Date:** 2026-09-14T09:50:00+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::ENTROPY_REDUCTION::REALITY_GRAPH::v1`

---

## 1. Concept-to-Name Reconciliation Table

| Old / Fragmented Name | Canonical Name | Status | Impact / Root Cause | Action Required |
|---|---|---|---|---|
| `SCT` (`session_capability_token`) | **`ACT` (`arif_capability_token`)** | **ALIAS / DEPRECATED** | Renamed to reflect Arif's sovereign authority. Older schemas still take `sct` alias. | Complete transition to `act_v1.*` across all tool parameter docs. |
| `A2A Port 18100` | **`A2A Port 3001`** | **DEPRECATED / MISMATCH** | `aaa-a2a.service` binds `PORT=3001` on loopback. `18100` was legacy or external Tailscale redirect resulting in connection reset. | Update all federation documentation and configs to point to `127.0.0.1:3001`. |
| `flame` / `flame-free` | **`fed-flash-cascade`** | **DEPRECATED / DEAD** | FLAME was decommissioned on 2026-09-04. 24 rule IDs and `flame-free` routes remain in `federation-models.json`. | Purge `flame_*` rule IDs and alias `low` effort to `fed-flash-cascade`. |
| `nervous_visvesvaraya` | **`fed-litellm-kvm8`** | **ORPHAN / ANONYMOUS** | Default Docker container name generated at spawn. Causes operational confusion. | Re-create container with `--name fed-litellm-kvm8`. |
| `APA Lease` | **`Path-5 Lease`** | **DEPRECATED / ALIAS** | `lease_engine.py` referenced legacy "APA v1.0". Canonical entity is now Path-5 Swarm Capability Lease. | Normalize terminology in `A-FORGE/leases/` to Path-5. |
| `OpenCode Zen` | **`OpenCode Go`** | **ALIAS / SPLIT** | `zen` endpoint is drained (401), while `go` endpoint is actively subscribed ($10/mo). Both referred to interchangeably. | Clearly demarcate `opencode-go` as active primary, `zen` as dormant. |
| `BOP` (Blast Overpressure / Gate) | **`Hook PEP (Sensor)`** | **DEPRECATED** | Legacy hooks attempted hard blocking; modernized to Policy Enforcement Point (PEP) forwarding to Kernel. | Deprecate "BOP" nomenclature in favor of "Hook Sensor & Forwarder". |
