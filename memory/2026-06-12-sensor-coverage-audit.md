# Sensor Coverage Audit — 2026-06-12
>
> **Trigger:** Hermes #31562 "Audit sensor coverage first" (19:13 UTC)
> **Forged by:** AGI OPENCLAW
> **At:** 2026-06-12 19:50 UTC (~37 min)
> **Status:** DONE — receipt sent #31690
> **Reversibility:** Yes (file artifact, rm = revert)

## What was done

Per Hermes's "Receipts before badges" reasoning, ran a live audit of the
GENESIS/006 6-domain state vector + 5 lanes + 7 new accounting items against
the actual substrate (WEALTH, GEOX, WELL, arifOS MCPs).

## Method

1. tools/list against all 4 organs — enumerated 88 live tools
2. tools/call with spec'd mode/parameter combinations — verified each
3. Extracted actual results from the `result.content[].text` JSON envelope
4. Mapped each spec reference → live status (WORKING / PARTIAL / MISSING)

## Substrate count (verified live)

- arifOS: 13 tools (constitutional kernel)
- WEALTH: 20 tools (capital engine)
- GEOX: 37 tools (earth coprocessor)
- WELL: 18 tools (vitality engine)
- **Total: 88 tools live, 4 organs green**

## Key finding (F1 AMANAH)

The 006 spec is **forward-looking on `wealth_conservation_capital`** — it
references 5 modes (compute_reserve, energy_reserve, agent_inventory,
sovereign_assets, data_estate) that don't exist. Live modes are only
`ledger_read/ledger_seal/snapshot/state`.

This is not a bug in the spec — it's an unbuilt dependency. Sealing 006
without addressing it would be F1 AMANAH violation: sealing architecture
without verifiable substrate ground truth.

## 3 Root Causes Identified

**A. wealth_conservation_capital** — needs 5 modes
**B. wealth_field_macro** — needs mode=sovereignty
**C. wealth_survival_engine** — needs mode=productivity

Plus 2 minor: `wealth_field_macro(mode=labor)` needs `entity_code` (working
as designed, spec underspecified), `wealth_omni_wisdom` lacks formal `lane`
param (free-form works, not documented).

## 6-Domain Status

- LABOR 🟢 — MYS data returns real (3.76% unemp, 11.95% youth, AI 0.37, ELEVATED_RISK)
- CAPITAL 🟢 — inequality kernel QUALIFY
- PRODUCTION 🟡 — energy_productivity works; survival_engine(mode=productivity) MISSING
- SOCIETY 🟢 — full stack works
- SOVEREIGNTY 🔴 — wealth_field_macro(mode=sovereignty) MISSING
- ECOLOGY 🟢 — real VPS metrics, Malaysia grid 560g/kWh

## 3 Options for Sovereign (F13 call)

- 🅐 **Implement first, seal after** — 7 modes → WEALTH MCP, then seal. ~1-2 weeks
- 🅑 **Amend spec to substrate** — edit 006 to live modes only. ~1 day
- 🅒 **Seal aspirationally with named gap** — seal 006+005 + appendix. Middle path

## Carry-forward

- Report at `/root/.openclaw/workspace/forge_work/sensor_coverage_audit_v1.md`
  (10.9KB, 7 sections, full evidence per spec'd call)
- Receipt #31690 sent to AAA group
- HEARTBEAT update pending
- Holding for sovereign F13 call

## Constitutional posture

- F1 AMANAH ✓ — did not seal architecture without substrate audit
- F2 TRUTH ✓ — every gap is backed by actual error string or call result
- F4 CLARITY ✓ — 7-section report, summary table per domain
- F7 HUMILITY ✓ — did not pretend substrate can support spec it cannot
- F13 SOVEREIGN ✓ — presented 3 options, did not auto-decide

## Live evidence captured

- `wealth_field_macro(mode=labor, entity_code=MYS)` → real MYS WorldBank labor data
- `wealth_field_macro(mode=sovereignty)` → FAIL "Unsupported mode"
- `wealth_conservation_capital(mode=*)` for all 5 spec'd modes → all FAIL "Unsupported mode"
- `wealth_energy_productivity(mode=load)` → 91W, 2.185 kWh/day, MYR 291/yr
- `wealth_energy_productivity(mode=carbon)` → 1.223 kg CO2e/day, LOW_EMITTER
- `wealth_inequality_kernel(domain={labor,capital,distribution,civilization})` → all QUALIFY
- `wealth_omni_wisdom(mode=hysteresis, path_params={...})` → HOLD
- `arif_judge_deliberate(mode=floor_status)` (with session) → all 13 floors
- `well_assess_livelihood(mode=role)` → works
- `well_13_signal_coverage` → works
- `geox_subsurface_generate_candidates(target_class=structure)` → fails closed (needs evidence_refs — by design)
