# Path-5 Domain Stewardship & Semantic Conflict Governance
**Document:** `DOMAIN_STEWARDSHIP_MAP.md`  
**Standard:** QQQ Protocol · F1 Truth · Semantic Integrity  
**Date:** 2026-09-14T09:48:30+08:00  
**Authority:** ARIF (F13 Sovereign Principal) · `ARIFOS::PATH5_OPERATIONALIZATION::v1`

---

## 1. Problem Statement: The Semantic Conflict Risk

Even with complete physical worktree isolation and zero Git merge conflicts, two parallel agents can introduce semantic contradiction:
- *Agent A* renames an MCP tool parameter or updates an epistemic enum.
- *Agent B* writes a consumer module relying on the legacy parameter/enum.
- Both worktrees compile and pass local unit tests, but merging both breaks the federation reality graph.

**Governance Rule:** *Semantic boundaries are defended by Domain Stewardship before code is merged to main.*

---

## 2. Domain Stewardship Map

| Domain | Repository / Path | Primary Steward | Co-Steward / Witness | Sensitivity Level | Mutation Policy |
|---|---|---|---|---|---|
| **Kernel & Law** | `/root/arifOS/` | **arifOS Kernel (888-APEX)** | FRAME (:18085) | **P0 Critical** | Strict fail-closed; Gate 2d perimeter check required. |
| **Institution** | `/root/AAA/` | **333-AGI (MIND)** | A-AUDIT | **P1 High** | Invariant preservation; Hook mesh compliance mandatory. |
| **Engineering & MCP** | `/root/A-FORGE/` | **777-FORGE** | A-FORGE MCP (:7072) | **P1 High** | Build integrity, schema compatibility, no unwhitelisted write paths. |
| **Telemetry & Graph**| `/root/arifFlow/` | **FLOW Engine (:7073)** | arifFlow | **P2 Medium** | Causal DAG preservation; hash-chained events. |
| **Earth Reasoning** | `/root/GEOX/` | **GEOX Domain Council** | 333-AGI | **P2 Medium** | Domain physics rules; petrophysical constraints. |
| **Capital Substrate**| `/root/WEALTH/` | **WEALTH Council** | 555-ASI | **P1 High** | Entropy check, ledger conservation laws. |
| **Human Homeostasis**| `/root/WELL/` | **WELL Guardian** | Arif (F13) | **P0 Critical** | Human dignity (F6), no simulated/hallucinated biometric data. |

---

## 3. Pre-Merge Semantic Conflict Checks

Before any reconciliation merge is approved by A-FORGE:
1. **Scope Boundary Verification:** Compare `git diff --name-only` against the Lease's `allowed_paths`. Any file outside scope blocks reconciliation instantly (`SCOPE_BREACH`).
2. **Cross-Domain Impact Check:** If changes touch multiple domains (e.g., modifying `arifOS` models and `A-FORGE` tools), co-steward signoff or sequential verification is enforced.
3. **Interface Parity Check:** If interfaces (`types.ts`, `schemas.py`, OpenAPI specs) are mutated, dependent consumers are statically scanned across all worktrees before merge approval.
