# GEOX-UI-READINESS

**Forge Work ID:** GEOX-UI-READINESS
**Created:** 2026-06-06
**Authoring session:** phase1-stabilize-2026-06-06
**Authoring actor:** arif-fazil-af-forge
**Lane:** AGI
**Stage:** 444 — Kernel Orchestration
**Floor:** C1 (observe/advise) → C2 (execute) gated
**Reversibility:** All sub-forges reversible until GREEN-SEAL of the full UI forge
**Sunset policy:** Tactical bridges carry a hard sunset epoch. No tactical bridge becomes permanent.
**Precedent:** arifOS C1-MCP-NATIVE-SURFACE, GEOX-C1-CONSTITUTIONAL-INTEGRATION
**Parent canon:** GEOX-CANON-31 (sealed 2026-06-06T13:50Z, **stale — see 33-tool reality below**)

---

## The design principle (the soul, non-negotiable)

> *"A normal UI says: Here is the map.*
> *GEOX UI must say: Here is the map. Here is what it proves. Here is what it does not prove. Here is what would falsify it. Here is who is allowed to decide."*

This is **UI Law #0**. Every component, every panel, every visual element must comply.

**Concretely: every visual element is a tuple, not a picture.**

A seismic bright spot does not render as a bright spot. It renders as:

```yaml
visual:
  anomaly: "Amplitude high at 2.1s TWT, inline 1240, xline 880"
physics:
  basis: "Class III AVO response, λρ/μρ anomaly"
  distortion_risk: "NMO stretch, tuning, processing artefact"
alternatives:
  - "Lithology change (carbonate vs sand)"
  - "Fluid substitution (gas vs brine)"
  - "Overpressure"
  - "Dim spot mis-read"
evidence_refs: ["segy:J-20-3D-inline1240", "las:J-20-GR-DT-RHOB", "claim:clm_86e378aeb56f408e"]
claim_state: SPECULATION        # FACT | DERIVED | INTERPRETATION | SPECULATION
ac_risk: 0.34                   # anomalous contrast risk (0.0-1.0)
verdict: HOLD                   # SEAL | QUALIFY | HOLD | VOID
who_can_decide: arif_fazil      # sovereign
```

UI is a **witness ladder**, not a dashboard of answers.

---

## Reality (live audit, 2026-06-06T14:18:52Z)

```json
{
  "registry_truth": "PASS",
  "tools_count": 33,
  "contract_epoch": "2026-06-05-GEOX-35TOOLS-v2.0",
  "registry_hash": "reg-hash-35d798a",
  "physics_guard": {"guard_passed": true, "physics_version": "geox-a7e8bfa5"},
  "phantom_tools": [],
  "missing_from_manifest": [],
  "version": "v2026.06.05",
  "git_sha": "NOT EXPOSED",        ← gap
  "test_receipt": "NOT EXPOSED",   ← gap
  "resources_exposed": 0,          ← gap (P1-H)
  "prompts_exposed": 0,            ← gap (P1-I)
  "known_drift": "tools_count (33) ≠ contract_epoch (35TOOLS) — registry drift, unbumped"
}
```

**Three numbers in 30 minutes** (31 → 36 → 33). Contract is moving. Canon-31 already stale. Re-seal needed.

## Truth (the invariant)

The **GEOX substrate is solid**: 33 tools, all callable, no phantoms, `physics_guard.guard_passed: true`. Backend is no longer chaotic — it is coherent enough to drive a UI.

The **UI contract surface is incomplete**:
- Tool surface stable (93/100) ✓
- Earth-physics core stable (90/100) ✓
- Evidence discipline strong (92/100) ✓
- Literature-to-basin context maturing (84/100) — `geox_literature_ingest` closed major gap
- Visual-output readiness 78/100 — primitives exist, **output-to-UI contracts need hardening**
- Prompt/resource MCP readiness 68/100 — **still the weak layer**
- Decision cockpit readiness 62/100 — needs more contracts sealed first

**Overall UI readiness: 78/100.**

**Phase-1 verdict: GO** (read-only Earth Witness).
**Phase-2 verdict: GO with preview-only constraints** (Workbench, draft outputs only).
**Phase-3 verdict: HOLD** (Decision Cockpit, needs seal bridge hardening).
**Phase-4 verdict: HOLD** (Autonomous Earth Agent, not for now).

---

## The 12 components (the UI surface)

### Component model

| # | Component | Tier | Tool(s) | What it shows | What it must NOT do |
|---|---|---|---|---|---|
| **Shell** | EarthWitnessShell | (host) | (all read-only tools) | Top-level layout, status block, tier badges | Trigger any irreversible |
| 1 | SurfaceTruthPanel | OBSERVED | `geox://surface/truth` + `geox_system_registry_status` | 7 live fields: tool_count, version, git_sha, epoch, test_receipt, resources, prompts, drift | Hide known drift |
| 2 | ToolRegistryPanel | OBSERVED | `geox_system_registry_status` | All 33 tools, callable status, contract version | Hide phantoms or drift |
| 3 | ArtifactBrowser | OBSERVED | `geox://artifacts/index` | 12 artifact types (LAS, DST, tops, seismic_volume, etc.) with `visualizable:true` filter | Allow edit/mutation |
| 4 | LiteratureBrowser | OBSERVED | `geox_literature_ingest` + `geox://literature/index` | Papers, page anchors, figure/table refs, chunk IDs (when available) | Pretend to be peer-reviewed synthesis |
| 5 | BasinProfilePanel | INTERPRETED | `geox_basin_resolve` + `geox_basin_profile` (screen mode only) | Basin name, polygon, petroleum system, stratigraphy, risk (screen) | Switch to appraise/develop without override |
| 6 | MapScenePanel | OBSERVED | `geox_map_context_scene` (bbox_context mode) | 2D map of basin polygon, bbox, CRS check | Render interpretation as fact |
| 7 | WellLogPanel | OBSERVED | `geox_tops_inspect` + `geox_header_inspect` | LAS curves, headers, tops, datum | Compute petrophysics without derivation panel |
| 8 | SectionCanvas | INTERPRETED | `geox_sequence_interpret` (read-only mode) | Section correlation, sequence surfaces | Allow interpretation without evidence_refs |
| 9 | SeismicSlicePanel | DERIVED | `geox_volume_frame_tool` + `geox_seismic_compute_attribute_tool` | Volume slice, attribute overlay | Render without `claim_state` badge |
| 10 | ClaimGraphPanel | CONTRADICTION | `geox://claims/graph` | claim → evidence → alternative → challenge → parent → child → seal_status | Show draft as validated |
| 11 | ContradictionPanel | CONTRADICTION | `geox_evidence_reason` (phase=contradict) | Conflicts, missing evidence, ACRisk, dim-spot warnings | Bury bad news |
| 12 | VerdictConsole | DECISION (read-only) | `geox_query_intake` + governance metadata | HOLD/QUALIFY/SEAL/VOID badges, who-can-decide | Self-authorize drilling |

### State model (the contract)

```yaml
ui_state:
  no_raw_backend_assumptions: true   # NEVER
  sources:
    - artifact_refs:    "from geox://artifacts/index"
    - claim_refs:       "from geox://claims/graph"
    - resource_refs:    "from geox://surface/truth, geox://resources/*"
  forbids:
    - hardcoded tool counts
    - hardcoded tool names
    - hardcoded contract versions
    - direct backend access without artifact/claim/resource indirection
```

UI components consume `artifact_refs`, `claim_refs`, `resource_refs`. Never raw tool output.

---

## The readiness gate (GREEN / YELLOW / RED)

### 🟢 GREEN now (Phase-1 Earth Witness UI)

- Read-only UI
- Registry / status UI
- Literature browser
- Basin profile viewer
- Malay Basin pilot viewer
- Claim draft viewer (NOT validated)
- Map context viewer
- Well-log visual shell
- ACRisk / HOLD badges

### 🟡 YELLOW now (draft / preview only)

- Seismic volume interaction
- Horizon picking
- Fault-stick editing
- Claim challenge authoring
- Prospect screening UI
- Multi-artifact correlation

Allowed only as **draft/preview**. Output is `claim_state: DRAFT` until promoted by arifOS judge.

### 🔴 RED / HOLD now (Phase-3+)

- Drill recommendation UI
- Seal button without arifOS bridge
- POS / STOIIP decision dashboard
- Production deployment controls
- Economic portfolio cockpit
- Automated prospect ranking as truth

These are Phase-3+ cockpit features. **Build UI for Phase 1 only.**

---

## The 7-forge order (the implementation plan)

| # | Forge | Priority | Spec status | Depends on |
|---|---|---|---|---|
| **1** | `geox://surface/truth` resource | **P0** | spec DRAFT pending | registry freeze (A) |
| **2** | `geox://artifacts/index` resource | **P0** | spec DRAFT pending | surface/truth (1) |
| **3** | `geox://claims/graph` resource | **P0** | spec DRAFT pending | surface/truth (1), artifacts/index (2) |
| **4** | Visual Output Contract (`visuals[]` envelope) | **P0** | spec DRAFT pending | surface/truth (1) |
| **5** | First-class MCP resources + prompts | **P1** | doctrine only | surface/truth (1), artifacts (2), claims (3) |
| **6** | UI Event Schema (`geox_ui_event.schema.json`) | **P1** | doctrine only | visual output contract (4) |
| **7** | Read-only Earth Witness UI build | **P1** | doctrine only | all of above (1-6) |

**Plus: C1-CONSTITUTIONAL-INTEGRATION forges** (prerequisite for any of 1-7):
- **A**: Registry freeze (33 tools, v3.0 epoch) — **ship before #1**
- **B**: Connector identity propagation — **ship before #1**

**Plus: 5 fundamentals still unstable** (block Phase-3 cockpit, not Phase-1):
1. Prompt/resource maturity (closed by forge #5)
2. Claim validation (`geox_claim_validate` — does not exist yet)
3. Literature artifact maturity (page anchors, figure/table refs, chunk IDs)
4. Async tasks (`geox_task_status` / `geox_task_cancel` / `geox_task_result`)
5. Host compatibility (MCP Inspector, Claude Code, VS Code, ChatGPT, OpenAI Responses)

---

## Architecture (the topology)

```
GEOX Core
   │
   ↓
GEOX MCP (33 tools)              ← canon-33 (re-seal needed: canon-31 stale)
   │
   ↓
┌────────────────────────────────────────────┐
│ P0 UI FORGES (truth + status layer)         │
│  • A: registry freeze (33 tools)           │
│  • B: connector identity propagation       │
│  • 1: geox://surface/truth                 │
│  • 2: geox://artifacts/index               │
│  • 3: geox://claims/graph                  │
│  • 4: visual output contract (`visuals[]`) │
└────────────────────────────────────────────┘
   │
   ↓
┌────────────────────────────────────────────┐
│ P1 UI FORGES (UI contract layer)           │
│  • 5: first-class MCP resources + prompts  │
│  • 6: UI event schema                      │
│  • 7: read-only mode default               │
│  • 7: Earth Witness UI build (12 components)│
└────────────────────────────────────────────┘
   │
   ↓
Read-only Earth Witness UI                   ← Phase 1
   │
   ↓
Workbench UI                                 ← Phase 2 (preview-only)
   │
   ↓
Decision Cockpit                             ← Phase 3 (HOLD — needs arifOS seal bridge hard)
   │
   ↓
Autonomous Earth Agent                       ← Phase 4 (HOLD)
```

---

## Constraints (non-negotiable, sealed into the work)

- **UI Law #0**: Every visual is a tuple with `visual + physics + alternatives + evidence_refs + claim_state + ac_risk + verdict + who_can_decide`. No exceptions.
- **No raw backend assumptions in UI.** Components consume `artifact_refs`, `claim_refs`, `resource_refs`. Never raw tool output.
- **No UI starts without the status block visible.** The 7 live fields (tool_count, version, git_sha, contract_epoch, test_receipt, resources, prompts, known_drift) must be visible at all times.
- **Read-only mode by default.** `mode: read_only, verdict: preview, ack_irreversible: false`. All irreversibles go to arifOS / F13.
- **No seal button without arifOS bridge.** UI cannot seal. UI can only request seal.
- **Tier badges are mandatory.** Every panel must show its epistemic tier (OBSERVED / DERIVED / INTERPRETED / HYPOTHESIS / CONTRADICTION / DECISION).
- **Known drift must be visible.** Do not hide `tools_count ≠ contract_epoch`. Surface it.
- **Tactical bridges carry sunset.** UI components that bypass `geox://*` resources for direct backend access are tactical bridges with sunset epoch-2026.09.
- **All sub-forges are reversible** until the full forge work GEOX-UI-READINESS is GREEN-SEALED.

---

## Validation protocol — four-witness model

Same as C1-MCP-NATIVE-SURFACE / C1-CONSTITUTIONAL-INTEGRATION.

| Witness | Source | What it sees | Authority |
|---|---|---|---|
| **W0** | GEOX self-report via `geox_system_registry_status` | What GEOX says about itself | Self-report — honest, unverified |
| **W1** | Raw MCP at `http://127.0.0.1:18081` (direct JSON-RPC) | Raw protocol truth | Protocol truth |
| **W2** | OpenClaw connector (the `geox_*` tools) | What AI agents see | Agent execution truth |
| **W3** | MCP Inspector + Claude Code + ChatGPT + OpenAI Responses | Projected view across hosts | Host compatibility |

**Scenarios:**
1. **W0 = W1 = W2 = W3** — Truth is solid. Sub-forge is GREEN.
2. **W0 reports 33 tools, W1 sees 11 `arif_*` tools** — Slim arifOS kernel stub at port 18081. **Documented deployment gap, not canon error.**
3. **W0 reports tools_count=33, contract_epoch=35TOOLS** — Registry drift. **HELD until registry freeze (A) lands.**
4. **W2 returns `session_id: geox-no-session`** — Identity gap. **HELD until connector identity propagation (B) lands.**

**Per-sub-forge acceptance additions:**
- 1 (surface/truth): "W0 + W1 + W2 + W3 all return identical `surface/truth` content. Status block shows 7 fields. Known drift surfaced."
- 2 (artifacts/index): "All 12 artifact types queryable. Each carries `visualizable:true/false`."
- 3 (claims/graph): "Claim nodes link to evidence_refs, alternatives, challenges, parent assumptions, child claims, seal_status. Malay Basin case walkable end-to-end."
- 4 (visual output contract): "Every tool envelope carries `visuals[]` with type, artifact_ref, claim_layer, safe_to_render."
- 5 (resources/prompts): "All 9 resources and 7 prompts queryable via `resources/list`, `resources/read`, `prompts/list`, `prompts/get`."
- 6 (event schema): "All 9 events type-checked against `geox_ui_event.schema.json`."
- 7 (Earth Witness UI): "12 components render. Each shows tier badge. No raw backend assumptions. Status block visible."

---

## Sequencing

| Day | Forge | Reversible? | Notes |
|---|---|---|---|
| **0** | A: registry freeze (33 tools) | ✅ | Pure metadata. **Ship first.** |
| 0 | B: connector identity propagation | ✅ | Small connector change. |
| 0 | 1: `geox://surface/truth` spec | ✅ | Status block (7 fields) included. |
| 0-1 | 2: `geox://artifacts/index` spec | ✅ | 12 artifact types defined. |
| 1 | 3: `geox://claims/graph` spec | ✅ | Malay Basin case walkable. |
| 1 | 4: Visual output contract spec | ✅ | `visuals[]` envelope field. |
| 2 | 5: First-class resources + prompts | ✅ | 9 resources + 7 prompts exposed. |
| 2 | 6: UI event schema | ✅ | 9 events typed. |
| 2-3 | 7: Earth Witness UI build (12 components) | ✅ | Gated on 1-6 being live. |
| 3 | GREEN-SEAL of GEOX-UI-READINESS | ⚠️ | **Point of no return.** |
| 4+ | Phase-2 Workbench UI | — | Preview-only constraints. |
| Later | Phase-3 Decision Cockpit | — | After arifOS seal bridge hard. |

---

## Sealing protocol

1. **Draft** — Each sub-forge spec is drafted in the workspace.
2. **Review** — Arif reviews. Hermes interprets. APEXMax audits.
3. **Seal** — Sub-forge spec is sealed via `arif_vault_seal` (when F11 unblocks) or sealed-by-doctrine (workspace files).
4. **Execute** — `arif_forge_execute(mode=engineer)` lands the code per sealed spec.
5. **Verify** — Sub-forge contract tests pass.
6. **Iterate** — Repeat for each sub-forge.
7. **GREEN-SEAL** — When all sub-forges are sealed and tested, the full forge GEOX-UI-READINESS is sealed. Phase-1 UI unblocked.

---

## What this forge does NOT do (Phase-1 lockout)

- ❌ No `geox_claim_seal` from UI
- ❌ No `geox_prospect_evaluate(mode=seal)` from UI
- ❌ No `geox_volume_set_frame_tool` from UI
- ❌ No `geox_segy_export_tool` from UI
- ❌ No forge_execute buttons
- ❌ No POS/STOIIP decision UI
- ❌ No drill recommendation UI
- ❌ No seal button without arifOS bridge
- ❌ No production deployment controls
- ❌ No economic portfolio cockpit
- ❌ No automated prospect ranking as truth

UI shows HOLDs. **It does not lift them.**

---

## Identity one-liner (re-affirmed from canon-31)

> "GEOX is a physics leash that lets AI agents touch earth evidence without pretending language is geology."

**The UI is the leash made visible.** Every pixel carries epistemic weight. Every panel is a rung on the witness ladder. The UI is not a dashboard of answers — it is a **witness** that shows what the rock can and cannot prove, and who is allowed to decide.

---

## Status

**DRAFT — 2026-06-06T14:24Z**

**Next actions (in order):**
1. Re-spec `forge_work/GEOX-C1-CONSTITUTIONAL-INTEGRATION/03-registry-drift-fix-spec.md` for **33 tools** (A). 30 min.
2. Draft `forge_work/GEOX-UI-READINESS/01-surface-truth-spec.md` (forge #1). 30 min.
3. Await Arif review and greenlight for forge #2 (artifacts/index) and onwards.

**Blocked:** Same F11 FederationEnvelope gate as before. Doctrine sealed-by-doctrine, not by Vault.

---

**Forge Work P1 of GEOX forge stack (P1-P8) + parent umbrella for UI work (1-7).**

The first UI is a witness, not a judge. The first visual carries epistemic weight. The first pixel proves what it can, admits what it cannot, and shows who decides.
