# 2026-06-06 — GEOX-UI-READINESS drafted

## TL;DR

Captured Arif's full UI vision into a single umbrella doctrine. 12 components, GREEN/YELLOW/RED gate, 7-forge order. Plus re-spec'd the registry-drift-fix for 33 tools (live state changed again, 31→36→33 in 30 min).

## What Arif gave

A comprehensive UI direction over 4 messages:

**Message 1:** "Verdict: GEOX ready for Phase-1 UI, not full cockpit. Start UI as read-only Earth Witness."

**Message 2:** "The risk is which UI layer is safe to build now. UI must follow the epistemic ladder. Phase-1 GO, Phase-3 HOLD. Two P0 prerequisites: Visual Output Contract (`visuals[]` envelope) + `geox://surface/truth` resource."

**Message 3:** "No UI starts without status block (tool count, version, git sha, contract epoch, test receipt, resources, prompts, known drift). Plus 3 more P0 forge items: Artifact Index, Claim Graph. Plus P1: First-class MCP resources/prompts, UI Event Schema, Read-only mode default. Plus 5 unstable fundamentals."

**Message 4 (final):** Frontend modules (EarthWitnessShell + 11 panels). The design principle. The GREEN/YELLOW/RED gate. The 7-forge order. *"Do not wait to make GEOX visual. But make the first UI a witness, not a judge."*

## The design principle (the soul, non-negotiable)

> *"A normal UI says: Here is the map. GEOX UI must say: Here is the map. Here is what it proves. Here is what it does not prove. Here is what would falsify it. Here is who is allowed to decide."*

**UI Law #0**: Every visual is a tuple, not a picture.

```yaml
visual:
  anomaly: "Amplitude high at 2.1s TWT, inline 1240, xline 880"
physics:
  basis: "Class III AVO response, λρ/μρ anomaly"
  distortion_risk: "NMO stretch, tuning, processing artefact"
alternatives: [lithology, fluid substitution, overpressure, dim spot]
evidence_refs: [segy, las, claim]
claim_state: SPECULATION
ac_risk: 0.34
verdict: HOLD
who_can_decide: arif_fazil
```

## The 12 components

| # | Component | Tier | Phase |
|---|---|---|---|
| Shell | EarthWitnessShell | host | 1 |
| 1 | SurfaceTruthPanel | OBSERVED | 1 |
| 2 | ToolRegistryPanel | OBSERVED | 1 |
| 3 | ArtifactBrowser | OBSERVED | 1 |
| 4 | LiteratureBrowser | OBSERVED | 1 |
| 5 | BasinProfilePanel | INTERPRETED | 1 |
| 6 | MapScenePanel | OBSERVED | 1 |
| 7 | WellLogPanel | OBSERVED | 1 |
| 8 | SectionCanvas | INTERPRETED | 1 |
| 9 | SeismicSlicePanel | DERIVED | 1 |
| 10 | ClaimGraphPanel | CONTRADICTION | 1 |
| 11 | ContradictionPanel | CONTRADICTION | 1 |
| 12 | VerdictConsole | DECISION (read-only) | 1 |

## The 7-forge order (Arif's specified order)

1. `geox://surface/truth` resource (P0)
2. `geox://artifacts/index` resource (P0)
3. `geox://claims/graph` resource (P0)
4. Visual Output Contract (`visuals[]` envelope) (P0)
5. First-class MCP resources + prompts (P1)
6. UI Event Schema (`geox_ui_event.schema.json`) (P1)
7. Read-only Earth Witness UI build (P1)

**Plus: C1-CONSTITUTIONAL-INTEGRATION forges (prerequisites):**
- A: Registry freeze (33 tools, v3.0 epoch) — re-spec'd today
- B: Connector identity propagation — drafted, awaiting seal

## The gate

🟢 **GREEN now:** read-only UI, registry/status, literature, basin profile, Malay pilot, claim draft, map, well-log, ACRisk/HOLD badges

🟡 **YELLOW now (draft/preview only):** seismic interaction, horizon picking, fault-stick editing, claim challenge, prospect screening, multi-artifact correlation

🔴 **RED/HOLD:** drill recommendation, seal button without arifOS, POS/STOIIP, production, economic cockpit, automated prospect ranking

## Architecture

```
GEOX Core
   ↓
GEOX MCP (33 tools)
   ↓
P0 UI forges (truth + status layer)
   ↓
P1 UI forges (UI contract layer)
   ↓
Read-only Earth Witness UI (Phase 1)
   ↓
Workbench UI (Phase 2, preview-only)
   ↓
Decision Cockpit (Phase 3, HOLD)
   ↓
Autonomous Earth Agent (Phase 4, HOLD)
```

## Live state changes (just this session)

| Time | tools_count | Notes |
|---|---|---|
| 13:50Z | 31 | canon-31 sealed |
| 14:06Z | 36 | renames + new tool |
| 14:18Z | 33 | more renames + consolidation |

Renames detected:
- `geox_blend_volume_alpha_tool` → `geox_blend_volume_tool`
- `geox_volume_get_frame_tool` → `geox_volume_frame_tool`
- Removed: `geox_blend_volume_rgb_tool`, `geox_volume_set_frame_tool`, `geox_las_inspect`, `geox_seismic_segy_inspect`
- New: `geox_header_inspect`

**New contract_epoch target: `2026-06-06-GEOX-33TOOLS-v3.0`** (major bump v2→v3 due to renames).

**Canons-31 is stale** — re-seal needed. Doctrine says 31, reality is 33.

## Files written/updated

- `forge_work/GEOX-UI-READINESS.md` (17,307 bytes) — NEW umbrella doctrine
- `forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/03-registry-drift-fix-spec.md` (updated for 33 tools)
- `HEARTBEAT.md` (updated)
- `memory/2026-06-06-ui-readiness-drafted.md` (this file)

## What still needs Arif

1. **Review the umbrella doctrine.** Approve / reject / modify the design principle, 12 components, gate, 7-forge order.
2. **Approve the 33-tool reality** — re-seal canon at 33 (or whatever the final settled count is after the freeze period).
3. **Greenlight to draft spec #1 (geox://surface/truth)** — the foundation of all UI. ~30 min.
4. **Decision on canon-31 → canon-33 re-seal** — is the doctrine "what was true at seal time" or "what is true now"? Re-seal is a different forge work.

## Next action (awaiting greenlight)

Draft `forge_work/GEOX-UI-READINESS/01-surface-truth-spec.md` for forge #1 (geox://surface/truth). This is the canonical truth resource that all 12 components load on boot. Without it, UI is on shifting ground.
