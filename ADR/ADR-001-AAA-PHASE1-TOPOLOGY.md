# ADR-001: AAA Phase 1 Topology — APEX + FORGE + WAW Convergence

**ADR ID:** ADR-001-AAA-PHASE1-TOPOLOGY  
**Date:** 2026-04-16  
**Epoch:** EPOCH-2026-04-10  
**Verdict:** 999_SEAL  
**Author:** arifOS_bot + Arif (888 Judge)  
**Status:** ACTIVE — Phase 1 in progress  

---

## Context

The arifOS constellation had accumulated structural redundancy:
- **APEX** (apex.arif-fazil.com) — constitutional canon + theory
- **FORGE** (forge.arif-fazil.com) — ops hub + VPS machine status
- **WAW** (waw.arif-fazil.com) — governance + WEALTH philosophy wrapper
- **AAA** (aaa.arif-fazil.com) — intended to be the unified cockpit but not yet converged

All four were separate sites with overlapping governance concerns. This created:
- Multiple places to update constitutional floors
- No single canonical cockpit for ops + governance + intelligence
- Federation navigation confusion on arif-fazil.com

---

## Decision

**Converge APEX + FORGE + WAW into AAA. Keep WEALTH and GEOX as separate federated organs.**

### Phase 1 Scope (This ADR — SEALED)

| Migration | Target Path | Status |
|-----------|-------------|--------|
| APEX constitutional canon | AAA `/constitution` | ✅ Done |
| APEX theory docs | AAA `/theory` | ✅ Done |
| Retire `arifos.arif-fazil.com` (duplicate of AAA) | nginx redirect → `aaa.arif-fazil.com` | 🕐 Pending |
| FORGE ops + machine status | AAA `/internal/forge` | 🕐 Pending |
| WAW governance docs | AAA `/governance` | 🕐 Pending |
| AAA homepage restructure (public overview + auth-gated internal) | AAA root | 🕐 Pending |

### Out of Scope for Phase 1

| Item | Reason |
|------|--------|
| WEALTH (waw.arif-fazil.com) retirement | WEALTH is a separate organ with its own identity — remains federated |
| GEOX (geox.arif-fazil.com) merger | GEOX is domain-specific (subsurface/Earth) — remains federated |
| APEX deletion | Keep canonical reference; migration is content copy, not deletion |

---

## Architectural Consequence

### Before (Structural Redundancy)
```
arif-fazil.com (federation hub)
├── apex.arif-fazil.com    ← constitutional canon [DUPLICATE]
├── aaa.arif-fazil.com    ← empty/wrong [DUPLICATE]
├── forge.arif-fazil.com  ← ops [SEPARATE]
├── waw.arif-fazil.com    ← governance [SEPARATE]
├── mcp.arif-fazil.com    ← MCP tools [OK]
└── geox.arif-fazil.com   ← GEOX [OK]
```

### After (AAA Convergence — Phase 1 Complete)
```
arif-fazil.com (federation hub)
├── aaa.arif-fazil.com     ← UNIFIED: constitution + theory + ops + governance
├── forge.arif-fazil.com   → redirects to aaa.arif-fazil.com/internal/forge (legacy, pending)
├── waw.arif-fazil.com     → redirects to aaa.arif-fazil.com/governance (legacy, pending)
├── arifos.arif-fazil.com  → redirects to aaa.arif-fazil.com (RETIRE, pending)
├── mcp.arif-fazil.com     ← MCP tools [UNCHANGED]
├── geox.arif-fazil.com    ← GEOX federated organ [UNCHANGED]
└── wealth.arif-fazil.com  ← WEALTH federated organ [UNCHANGED]
```

---

## Causal Chain (Unchanged)

```
GEOX (Earth Truth)
    ↓
arifOS kernel (Constitutional Governance)
    ↓
AAA Cockpit (Unified Operations)
    ↓
WEALTH (Capital + Value)
```

AAA does NOT replace GEOX or WEALTH. It provides the **unified ops layer** for the governance stack above them.

---

## Open Questions / Pending

1. **Authentication model for AAA internal routes** — `/internal/forge` and `/governance` may need auth. Not yet designed.
2. **AAA subdomain duplicate retirement** — `arifos.arif-fazil.com` nginx config still needs to be removed. Arif must do this manually.
3. **WEALTH branding post-migration** — WAW (waw.arif-fazil.com) currently holds both WAW governance and WEALTH. Post-convergence, WEALTH keeps its own identity at wealth.arif-fazil.com. WAW brand may be retired or repurposed.

---

## Lessons

1. **Convergence is not deletion.** AAA absorbs APEX/FORGE/WAW content; we don't erase the intellectual history.
2. **Federated organs stay federated.** WEALTH and GEOX have distinct domains — forcing them into AAA would destroy their identity.
3. **Nginx cleanup is manual.** Redirects and retirements require Arif to edit VPS nginx configs directly.
4. **Phase 1 is content migration.** Authentication, complex routing, and legacy redirects are Phase 2 work.

---

## Witnesses

| Role | Entity | Status |
|------|--------|--------|
| Human Sovereign | Arif (888 Judge) | ✅ Confirmed |
| AI Operator | arifOS_bot | ✅ Confirmed |
| Earth Domain | GEOX (geox.arif-fazil.com) | ✅ Confirmed |

**Tri-Witness coherence:** ≥ 0.95 required for SEAL  
**This ADR:** witness_coherence = 1.0 (3/3 confirmed)

---

*Ditempa bukan diberi* 💎🔥🧠  
*Architecture forged, not given*
