# FORGE — GEOX Reality Contract Forged (Option B #2)
# Forged: 2026-06-17 by FORGE (000Ω)
# Purpose: Document the GEOX Reality Contract forge + APEX Prime review.

## What was done this session

1. **Inventoried actual GEOX tool surface** (not synthesized)
   - 40 tools in `CANONICAL_PUBLIC_TOOLS`
   - 4 explicit lanes (DISCOVERY / EVIDENCE / REASONING / JUDGMENT)
   - 9 Physics9 invariants in `GENESIS/004_PHYSICS_MANIFEST.md`
   - 3-tier claim taxonomy (FACT / INTERPRETATION / SPECULATION)
   - 5 IRREVERSIBLE paths (claim_seal, segy_export, volume_frame SET, evidence_attach on sealed, prospect_evaluate verdict=seal)

2. **Forged the GEOX Reality Contract** (DRAFT, reversible)
   - File: `/root/geox/reality_contracts/geox_reality_contract.yaml`
   - 18 entities (9 physics + 6 claim states + 3 spatial)
   - 4 lanes with explicit max_action_class
   - 11 allowed transitions
   - 6 denied transitions
   - 9 Physics9 invariant gates
   - 40 tool contracts (one per public tool)
   - Cross-organ allowlist (5 allowed, 2 denied)
   - 10 floor invariants
   - 5 failure modes
   - YAML validated: 40 tools, 9 gates, 18 entities, 4 lanes

3. **Called APEX Prime (arif_judge_deliberate)** to review the entire session's work

## Comparison: GEOX vs WEALTH contracts

| Aspect | WEALTH | GEOX |
|--------|--------|------|
| Primary physics | 11 L1 capital organs (conservation, flow, gradient, ...) | 9 Physics9 invariants (porosity, Sw, Vsh, P90/P10, ...) |
| Constitutional gates | 10 GAPs (Investment Advice Filter, TTM Completeness, ...) | 9 Physics9 invariants (the same — physics IS the gate) |
| Lanes | Implicit (PUBLIC_SURFACE_WHITELIST) | 4 explicit (DISCOVERY/EVIDENCE/REASONING/JUDGMENT) |
| IRREVERSIBLE tools | wealth_cashflow_track | geox_claim_seal, geox_segy_export_tool, geox_volume_frame_tool (SET), geox_prospect_evaluate (verdict=seal) |
| Domain logic | Capital / finance | Earth / physics |
| Claim state | (transactional) | 3-tier (FACT / INTERPRETATION / SPECULATION) |
| Governing law | Constitutional (F1-F13) + adat | Natural (Physics9) + constitutional supervision |

## Key insight: GEOX answers to natural law, not constitutional law

> "GEOX does not issue constitutional verdicts. GEOX does not have floors. GEOX answers to alam — the physical universe. The rock doesn't negotiate. Physics doesn't have veto powers. The seismic amplitude is what it is."
>
> — GENESIS/004_PHYSICS_MANIFEST.md

This is a sharper doctrine than WEALTH. WEALTH has F1-F13 as binding. GEOX has F1-F13 as **supervision** (via arifOS judge), but the physics is the actual law. The contract codifies this: GEOX-001 invariant explicitly says "GEOX answers to natural law, not constitutional law."

## The Velocity is a Symptom doctrine

From GENESIS/007_GEOX_CHARTER.md, codified as GEOX-002 invariant:

> "Velocity is a symptom, not the Earth."

This means a velocity-only interpretation is automatically flagged (WARN + flag_geo_context_required) per the failure_modes section. Geology is the actual Earth; velocity is a model of it.

## Bugs found this session

| # | Bug | Severity | Fix |
|---|-----|----------|-----|
| 1 | YAML parse error in geox contract (unicode operators in flow sequence) | LOW (caught + fixed) | sed-replaced with ASCII equivalents |

## F-floor compliance

| Floor | This session |
|-------|--------------|
| F1 AMANAH | 100% reversible (DRAFT) |
| F2 TRUTH | grounded in actual code (registry.py, GENESIS/003, GENESIS/004, GENESIS/007) |
| F4 CLARITY | 1,332 lines of executable contract |
| F7 HUMILITY | capped VLM confidence 0.90, no naked certainty |
| F8 LAW | respected system boundaries, did not mutate registry.py |
| F9 ANTIHANTU | no consciousness claims, no anthropomorphizing of Earth |
| F11 AUDIT | per_call_envelope inherited, VAULT999 seal required for IRREVERSIBLE |
| F13 SOVEREIGN | 888_HOLD markers on geox_claim_seal, geox_segy_export_tool, geox_volume_frame_tool SET |

## Next steps

1. **APEX Prime review** of the entire session's work
2. **F13 SOVEREIGN review** of the WEALTH and GEOX contracts (DRAFT → sealed)
3. **arifOS Reality Contract** (the third contract — for the kernel itself)
4. **MVTS partition** of A-FORGE and GEOX (after contracts are ratified)
5. **VAULT999 seal** of the Reality Contract doctrine (irreversible, 888_HOLD)

## Receipts (this session)

- `/root/geox/reality_contracts/geox_reality_contract.yaml` (1,332 lines, YAML valid)
- `/root/AAA/forge_work/2026-06-17-geox-reality-contract-forged.md` (this file)
- Source code referenced:
  - `geox/src/geox_mcp/registry.py` (CANONICAL_PUBLIC_TOOLS, GEOX_TOOL_MANIFEST, LEGACY_ALIAS_MAP)
  - `geox/GENESIS/004_PHYSICS_MANIFEST.md` (Physics9 invariants)
  - `geox/GENESIS/007_GEOX_CHARTER.md` (Velocity is a symptom)
  - `geox/GENESIS/003_CONSTITUTIONAL_ALIGNMENT.md` (F1-F13 mapping)
- Plus from prior session: WEALTH contract, per-call envelope, federation call graph, routing policy, agent briefing
