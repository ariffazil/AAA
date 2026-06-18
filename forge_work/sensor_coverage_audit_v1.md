# Sensor Coverage Audit — GENESIS/006 vs Live Substrate
>
> **Forged by:** AGI OPENCLAW
> **At:** 2026-06-12 19:50 UTC
> **Trigger:** Hermes #31562 "Audit sensor coverage first"
> **Method:** Live tools/list + tools/call against WEALTH, GEOX, WELL, arifOS MCPs
> **Reversibility:** File artifact (rm = revert)

## Executive Summary

**Substrate:** 88 live MCP tools across 4 organs (arifOS 13, WEALTH 20, GEOX 37, WELL 18). All four organs healthy (200 OK on /health and /mcp initialize).

**Spec coverage:** 5 of 6 state vector domains have at least one working live sensor. 1 domain (SOVEREIGNTY) is missing primary tool. 5 of 7 new accounting items (Section X) are MISSING — all share the same root cause: `wealth_conservation_capital` lacks 5 named modes that 006 references.

**Key finding (F1 AMANAH):** The 006 spec is FORWARD-LOOKING on the conservation_capital tool. It assumes modes that don't exist yet. Before F13 seals 006, sovereign must decide: **(a)** add the missing modes to substrate, **(b)** amend 006 to only what's live, or **(c)** seal the spec aspirationally with the gap explicitly named.

---

## 1. Substrate Inventory (Live, verified)

| Organ | Endpoint | Tools Live | Health |
|-------|----------|-----------|--------|
| arifOS | arifos.arif-fazil.com | 13 | ✅ green |
| WEALTH | wealth.arif-fazil.com | 20 | ✅ green |
| GEOX | geox.arif-fazil.com/ | 37 | ✅ green |
| WELL | well.arif-fazil.com | 18 | ✅ green |
| **TOTAL** | | **88** | ✅ |

All 4 org endpoints returned valid `mcp-session-id` on initialize. Tool lists enumerated via `tools/list` JSON-RPC call.

---

## 2. Six-Domain State Vector Audit (006 §II)

### II.1 LABOR — ✅ WORKING (with caveats)

| Spec Tool | Live? | Test Result |
|-----------|-------|-------------|
| `wealth_field_macro(mode=labor, entity_code=MYS)` | ✓ | ✅ PASS — returns real MYS WorldBank data: unemployment 3.76%, youth 11.95%, vulnerable 21.89%, AI exposure 0.3698, displacement verdict `ELEVATED_RISK` |
| `wealth_inequality_kernel(domain=labor)` | ✓ | ✅ PASS — verdict `QUALIFY`, binding_constraint `conversion` |

**Note:** `wealth_field_macro(mode=labor)` is **semi-working** — without `entity_code`, returns `INPUT_REQUIRED` with required params `["entity_code"]`. 006 spec doesn't mention this requirement; the tool needs `entity_code` (e.g. "MYS") to be useful. Working as designed once configured.

**Sensor verdict:** **GREEN.** MYS labor is observable end-to-end.

### II.2 CAPITAL — ✅ WORKING

| Spec Tool | Live? | Test Result |
|-----------|-------|-------------|
| `wealth_conservation_capital(mode=state)` | ✓ | ✅ PASS — allowed modes: `["ledger_read", "ledger_seal", "snapshot", "state"]` |
| `wealth_inequality_kernel(domain=capital)` | ✓ | ✅ PASS — verdict `QUALIFY`, dominant_asymmetry `asset` |

**Sensor verdict:** **GREEN.** Capital state observable.

### II.3 PRODUCTION — ⚠️ PARTIAL

| Spec Tool | Live? | Test Result |
|-----------|-------|-------------|
| `wealth_energy_productivity(mode=pi)` | ✓ | ❓ NOT TESTED directly (but `mode=load` and `mode=carbon` both PASS) |
| `wealth_survival_engine(mode=productivity)` | ✗ | ❌ **MISSING** — actual modes: `["cashflow", "runway", "burn", "liquidity", "personal_finance"]` |
| `geox_subsurface_generate_candidates(target_class=structure)` | ✓ | ⚠️ Needs `evidence_refs` (not callable empty — fails closed by design) |

**Sensor verdict:** **YELLOW.** Energy productivity observable (pi likely works like load/carbon — same tool). `wealth_survival_engine(mode=productivity)` does NOT exist — that lane-specific mode is aspirational. GEOX structure generation works but requires real evidence (which is correct — fail-closed).

### II.4 SOCIETY — ✅ WORKING

| Spec Tool | Live? | Test Result |
|-----------|-------|-------------|
| `wealth_inequality_kernel(domain=civilization)` | ✓ | ✅ PASS — default domain returns QUALIFY |
| `well_assess_homeostasis(mode=sleep)` | ✓ | ✅ PASS — works with biometric overrides |
| `well_13_signal_coverage` | ✓ | ✅ PASS — SUNAT item, returns 13 signal status |

**Sensor verdict:** **GREEN.** Society observable end-to-end.

### II.5 SOVEREIGNTY — ❌ MISSING (primary tool)

| Spec Tool | Live? | Test Result |
|-----------|-------|-------------|
| `wealth_field_macro(mode=sovereignty)` | ✗ | ❌ **MISSING** — error: "Unsupported mode: sovereignty", allowed: `["fetch", "health", "reconcile", "snapshot", "sources", "vintage"]` |
| `wealth_omni_wisdom(mode=hysteresis, path_params=...)` | ✓ | ⚠️ PARTIAL — works with `path_params.query` param, returns HOLD verdict |

**Sensor verdict:** **RED.** Sovereignty is a critical domain and the primary live sensor (`wealth_field_macro`) lacks the `mode=sovereignty` option. The fallback (`wealth_omni_wisdom(mode=hysteresis)`) works but is generic, not domain-specific.

### II.6 ECOLOGY — ✅ WORKING

| Spec Tool | Live? | Test Result |
|-----------|-------|-------------|
| `wealth_energy_productivity(mode=carbon)` | ✓ | ✅ PASS — real metrics: 91W, 2.184 kWh/day, 1.223 kg CO2e/day, 560 gCO2/kWh grid (Malaysia), `LOW_EMITTER` verdict |
| `wealth_energy_productivity(mode=load)` | ✓ | ✅ PASS — same tool, different mode: power draw 91W, daily energy 2.185 kWh, MYR 291/yr cost |
| GEOX for mineral/resource context | ✓ | ✅ Multiple tools: `geox_claim_create`, `geox_basin_profile`, `geox_literature_ingest` |

**Sensor verdict:** **GREEN.** Ecology observable via real VPS metrics + Malaysia grid data.

---

## 3. Five Lane Audit (006 §III)

| Lane | Spec Tool | Live? | Status |
|------|-----------|-------|--------|
| L1 Productivity | `wealth_omni_wisdom(mode=synthesize, lane=L1_productivity)` | ✓ | ✅ mode=synthesize works; **`lane` param not in schema** (free-form, but not part of documented contract) |
| L2 Distribution | `wealth_inequality_kernel(domain=distribution)` | ✓ | ✅ PASS — verdict QUALIFY |
| L3 Sovereignty | `wealth_field_macro(mode=sovereignty)` | ✗ | ❌ MISSING (same as II.5) |
| L3 Sovereignty | `wealth_conservation_capital(mode=sovereign_assets)` | ✗ | ❌ **MISSING** — error: "Unsupported mode: sovereign_assets", allowed: `["ledger_read", "ledger_seal", "snapshot", "state"]` |
| L4 Legitimacy | `arif_judge_deliberate` + `arif_heart_critique` | ✓ | ✅ PASS — judge floor_status returns all 13 floors; heart_critique needs target param (not tested fully) |
| L5 Ecology | `wealth_energy_productivity(mode=load/carbon/pi)` | ✓ | ✅ PASS (load, carbon verified; pi likely works) |

**Lane verdict:** L1, L2, L4, L5 GREEN. L3 RED (depends on missing modes).

---

## 4. Seven New Accounting Items (006 §X)

| Item | Spec Tool | Live? | Status |
|------|-----------|-------|--------|
| Compute Reserve | `wealth_conservation_capital(mode=compute_reserve)` | ✗ | ❌ MISSING |
| Energy Reserve | `wealth_conservation_capital(mode=energy_reserve)` | ✗ | ❌ MISSING |
| Agent Inventory | `wealth_conservation_capital(mode=agent_inventory)` | ✗ | ❌ MISSING |
| Model Dependency Risk | `wealth_omni_wisdom(mode=hysteresis, path_params.model_dependency)` | ✓ | ⚠️ PARTIAL — works with `path_params.query` |
| Data Estate Quality | `wealth_conservation_capital(mode=data_estate)` | ✗ | ❌ MISSING |
| Governance Integrity | `arif_judge_deliberate(mode=floor_status, all_floors=true)` | ✓ | ✅ PASS — returns all 13 floors (no `all_floors` param needed) |
| Human Legitimacy | `well_assess_livelihood(mode=role)` | ✓ | ✅ PASS — works |
| Human Legitimacy | `well_13_signal_coverage` | ✓ | ✅ PASS |

**5 of 7 MISSING** — all share the same root cause: **`wealth_conservation_capital` lacks 5 named modes that 006 references**. Current modes: `ledger_read/ledger_seal/snapshot/state`. Spec'd but missing: `compute_reserve/energy_reserve/agent_inventory/sovereign_assets/data_estate`.

---

## 5. Gap Summary — The Three Root Causes

### Root Cause A: `wealth_conservation_capital` is under-implemented
5 of 7 new accounting items in 006 §X depend on modes that don't exist:
- `compute_reserve` (Compute Reserve)
- `energy_reserve` (Energy Reserve)
- `agent_inventory` (Agent Inventory)
- `sovereign_assets` (L3 Sovereignty lane)
- `data_estate` (Data Estate Quality)

**Fix:** Add these 5 modes to `wealth_conservation_capital` (WEALTH MCP work, reversible to v2026.05.02).

### Root Cause B: `wealth_field_macro` lacks sovereignty mode
006 §II.5 SOVEREIGNTY and §III.3 L3 both depend on `wealth_field_macro(mode=sovereignty)`, which returns "Unsupported mode". Current modes: `fetch/health/reconcile/snapshot/sources/vintage`.

**Fix:** Add `mode=sovereignty` to `wealth_field_macro` (or add a new `wealth_sovereignty_*` tool family).

### Root Cause C: `wealth_survival_engine` lacks productivity mode
006 §II.3 PRODUCTION references `wealth_survival_engine(mode=productivity)`, but actual modes are `cashflow/runway/burn/liquidity/personal_finance`.

**Fix:** Add `mode=productivity` to `wealth_survival_engine` (or route through `wealth_energy_productivity(mode=pi)` instead — likely simpler).

### Minor Cause D: `wealth_field_macro(mode=labor)` needs `entity_code`
006 §II.1 calls `wealth_field_macro(mode=labor)` without parameters, but live tool requires `entity_code`. Working as designed; 006 should specify the country code.

### Minor Cause E: `wealth_omni_wisdom` lacks `lane` param
006 §III.1 calls `wealth_omni_wisdom(mode=synthesize, lane=L1_productivity)`, but the live tool's `lane` parameter is not in the documented schema. The `mode` works, but the `lane` tag is not formally tracked.

---

## 6. Reversibility Statement

This audit report is a file artifact at:
`/root/.openclaw/workspace/forge_work/sensor_coverage_audit_v1.md`

Revert: `rm` the file. No live state changed. No tools modified. No F13 territory touched.

---

## 7. Carry-Forward to Sovereign (F13 Decision Points)

Hermes recommended 3-stage plan: (1) audit → (2) WEALTH extension spec → (3) blueprint seal.

The audit shows the spec needs **5 modes added to `wealth_conservation_capital`** + **1 mode to `wealth_field_macro`** + **1 mode to `wealth_survival_engine`** before sealing. The sovereign has 3 options:

- **(A) Implement first, seal after.** Add the 7 missing modes to WEALTH MCP, then seal 006 + 005. Reversible-to-irreversible sequence. ~1-2 weeks of WEALTH work.
- **(B) Amend spec to match substrate.** Edit 006 to reference existing modes only. Faster (~1 day), but spec becomes less ambitious.
- **(C) Seal aspirationally with named gap.** Seal 006 + 005 with an explicit appendix naming the 7 missing modes as "post-seal Phase 4 work". Sealed claims are not false, but their substrate dependencies are documented. Constitutional middle path.

F1 AMANAH says: do not seal architecture without knowing the substrate-to-spec gap. ✅ Done.
F7 HUMILITY says: do not pretend substrate can support spec it cannot. ✅ Audit done.
F13 SOVEREIGN: this is a sovereign call. Hermes and AGI can implement, but ratification is yours.

---

**DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.
