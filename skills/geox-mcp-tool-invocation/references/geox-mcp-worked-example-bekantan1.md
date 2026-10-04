# GEOX MCP Worked Example — Bekantan-1 Pre-Drill Model
*Session: 2026-08-13 · GEOX session: 83e765d1...*

## Setup sequence (actual output)

```bash
# Step 1: initialize → got mcp-session-id: 83e765d15d0f4f458df732ff72851767
# Step 2: notifications/initialized
# Step 3: geox_workspace mode=set → workspace set to "Malay · Group K · Bekantan-1 · Cendor"
```

## What works

| Tool | Mode | Args | Status |
|---|---|---|---|
| `geox_workspace` | `set` | `mode=set, basin="Malay", well_id="Bekantan-1", field="Cendor", play="Group K"` | ✅ Returns `_well_conformance` + context banner |
| `geox_workspace` | `view` | `mode=view` | ✅ Returns current context |
| `geox_geomechanics` | (default) | `state={"rho":2300,"vp":3500,"vs":2000}` | ✅ Requires state dict with rho/vp/vs |

## What doesn't work (yet)

| Tool | Mode | Error | Why |
|---|---|---|---|
| `geox_basin` | `profile` | `EVIDENCE_SCHEMA_VIOLATION` | Missing `basin_profile.yaml` for Malay Basin at full detail; ontology data exists but basin tools require local profile |
| `geox_basin` | `resolve` | Same | Same — basin profile file is skeletal |
| `geox_basin` | `profile` with extra `basin=` kwarg | `ValidationError: unexpected keyword argument` | Tool inherits workspace context; doesn't accept extra kwargs |

## Source of truth for pre-drill analysis

When GEOX basin tools lack data, fall back to:

1. **GEOX ontology** (always available, no tool needed):
   - `/root/GEOX/resources/ontology/formation_water.yaml` — pressure gradients, Rw models per formation
   - `/root/GEOX/resources/ontology/pressure_states.yaml` — Eaton calibration rules, overpressure indicators
   - `/root/GEOX/resources/basins/malay_basin/claims.json` — geological claims with evidence refs

2. **Public literature** (web search + extract):
   - Madon et al 2004, SPE 88455 — overpressure history of Malay Basin
   - GSM Bulletin 37 — occurrence and implications of overpressure
   - USGS OF99-50T — petroleum systems of Malay Basin

3. **Build model from literature + ontology** (what we did):
   - Combined GEOX ontology pressure gradients with published overpressure compartment data
   - Applied basin-process model (not just Eaton) for T > 120°C secondary mechanisms
   - Confidence: 0.65-0.70 (pre-drill, no well control)

## Malay Basin Group K parameters (from ontology + literature)

| Parameter | Value | Source |
|---|---|---|
| Top of overpressure (centre) | 1900-2000m TVDSS | Madon 2004 [OBS] |
| Top seal | Group F regional shale | Madon 2004 [OBS] |
| Geothermal gradient (average) | 47°C/km | GSM Bulletin 37 [OBS] |
| Geothermal gradient (range) | 36-60°C/km | Madon 2004 [OBS] |
| Heat flow (average) | 86 mW/m² | Durham thesis [OBS] |
| Pp gradient at Group K | 0.440-0.520 psi/ft | GEOX ontology [DER] |
| Temperature at Group K base (~4200m) | 227-259°C | Calculated [DER] |
| HPHT threshold | >15000 psi / >177°C | API definition [OBS] |

## Confirmed for Bekantan-1 specifically

| Fact | Status |
|---|---|
| Well drilled by PETRONAS (May 2024) | ✅ [OBS] Public: petronas.com press release Aug 2024 |
| Discovery with strong flow rate | ✅ [OBS] Public: Rigzone, TGS, Offshore Technology |
| "Shallowest oil ever flowed" (1218 stb/d at 730m TVDSS) | ⚠️ [INT] From SCAR-4 registry — sovereign testimony |
| SCAR-4 "execution without rasa" | ⚠️ [INT] Personal scar — father died during drilling |
| PSC was Petrofac-operated, PCSB drilled on MPM behalf | ⚠️ [INT] Sovereign testimony, not public |
