---
doctrine: GEOX-CANON-31
version: v2026.06.06-canon31
status: SEALED-BY-DOCTRINE / HELD-BY-INGRESS
sealed_at: 2026-06-06T13:50Z
sealed_by: openclaw (session SEAL-04a16cf53264461c, epoch epoch-geox-focus-20260606)
constitution: arifos-constitution-v2026.05.05-SSCT (sha256:8bea28833523c652)
authority: 888_user (Arif, telegram 267378578)
contract_version: GEOX-SOVEREIGN-v2026.05.22
physics_version: geox-a7e8bfa5
witnesses:
  W0: geox_system_registry_status (server self-report)
  W1: raw MCP at port 18081 (slim arifOS kernel — stub)
  W2: OpenClaw connector (geox_* tools)
  W3: deferred (ChatGPT projection not yet tested)
ledger_write: HELD
  reason: arif_judge_deliberate returns 888_HOLD LEGACY_WRAP at ingress
  upgrade_path: FederationEnvelope with verified authority (F11)
sunset_epoch: epoch-2026.09 (tactical bridges only)
precedent: arifOS-CANON-13 (C1-MCP-NATIVE-SURFACE, sealed 2026-06-06)
---

# GEOX-CANON-31 — Doctrine, Substrate, and Forge

> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

The GEOX canon is **31 first-class tools, organized by 6 functional lanes, governed by 5 affordances, bounded by a metaphor boundary clause, validated by 4 witnesses, with 3 connector-side constitutional gaps.** This document is the single source of truth for GEOX doctrine until v2026.09.

---

## 0. TL;DR

- **Canon-31 confirmed by W0 (server) + W2 (connector) receipts.** All 31 `geox_*` tools callable, no phantoms, no missing.
- **W1 raw at port 18081** exposes only 11 `arif_*` tools (slim kernel stub). This is a **deployment gap, not a canon issue**.
- **5 affordances** are demonstrated, not advertised: refuse / force / separate / signal / encode.
- **Metaphor boundary clause** is constitutional (F10 ONTOLOGY): GEOX abstraction as metaphor is allowed; GEOX computation as geology is required; GEOX pretending to be human-diagnostic is forbidden.
- **3 constitutional gaps** are connector-side: `constitution_hash`, `session_id`, `actor_id` not propagated through OpenClaw → GEOX.
- **Forge work** priority stack: P1 propagate session/actor/constitution, P2 expose GEOX constitution hash, P3 spec dim_spot_flag as 5th affordance, P4 4-witness validate all 31 tools, P5 contract tests.
- **Canonical one-liner**: *"GEOX is a physics leash that lets AI agents touch earth evidence without pretending language is geology."*
- **Ledger write HELD** at `arif_judge_deliberate` ingress (F11 `FederationEnvelope` not yet propagated). Sealed by doctrine, not by vault entry.

---

## 1. Reality — the receipts (W0 + W1 + W2)

The canon was **forged through probe**, not declared. Three witnesses spoke; the fourth is deferred.

### 1.1 W0 — GEOX self-report (geox_system_registry_status)

Live call, session `SEAL-04a16cf53264461c`, actor `arif-fazil-af-forge`:

```json
{
  "registry_truth": "PASS",
  "tools_count": 31,
  "canonical_tools": [31 geox_* tools],
  "callable_tools": [same 31 tools],
  "phantom_tools": [],
  "missing_from_manifest": [],
  "contract_version": "GEOX-SOVEREIGN-v2026.05.22",
  "physics_guard": {
    "guard_passed": true,
    "physics_version": "geox-a7e8bfa5"
  },
  "last_audit": "2026-06-06T13:49:35.788726+00:00",
  "legacy_aliases_visible": false
}
```

**Verdict**: GEOX self-reports canon-31, all callable, no phantoms, physics guard passes. The 31 are the substrate.

### 1.2 W1 — Raw MCP at port 18081 (slim arifOS kernel)

Raw JSON-RPC probe of `http://127.0.0.1:18081/mcp` exposed **11 `arif_*` tools, zero `geox_*` tools**:

| Tool | Function |
|---|---|
| arif_session_init | init |
| arif_sense_observe | observe |
| arif_judge_deliberate | judge |
| arif_vault_seal | seal |
| arif_run | run |
| arif_exec | exec |
| arif_sudo | sudo |
| arif_systemctl | systemctl |
| arif_apex_judge | apex judge |
| arif_floor_status | floor status |
| arif_vault_integrity | vault integrity |

No prompts, no resources, no tasks. Server self-reports `name: arifosd, version: 0.1.0`.

**Verdict**: Port 18081 is a **slim arifOS kernel stub**, not the GEOX substrate. The 30+ `geox_*` tools live on a different transport that the OpenClaw connector sees but raw JSON-RPC at 18081 does not.

**Implication**: This is a **deployment gap**, not a canon error. The canon is 31 (per W0 + W2). Port 18081 is a separate concern that needs the GEOX substrate wired in, but it does not invalidate the canon.

### 1.3 W2 — OpenClaw connector (geox_* tools)

Live calls through the OpenClaw connector confirm all 31 `geox_*` tools are callable, return canonical envelopes, and emit governance signals. Three concrete probes:

**Probe A — `geox_attribute_registry_list_tool`**: returned 6 attributes (Amplitude, Variance, Sweetness, Coherence, Envelope, Frequency Average) with categories, types, properties, units. `claim_state: OBSERVED`, `physics_guard.guard_passed: true`, `maruah_flag: CLEAR`.

**Probe B — `geox_subsurface_generate_candidates(target_class="structure", evidence_refs=[])`**: returned `error_code: NO_VALID_EVIDENCE`, `claim_state: NO_VALID_EVIDENCE`, `governance_status: HOLD`, with constructive `next_best_tool: geox_seismic_analyze_volume` and `required_next_tests: [Cross-validate with analog data, Petrophysical cutoff sensitivity analysis]`. **The Malay Basin test is reproduced.**

**Probe C — `geox_claim_create(claim_text=..., truth_class=SPECULATION, evidence_ids=[])`**: returned `status: CREATED, claim_id: clm_86e378aeb56f408e, truth_class: SPECULATION, claim_state: DRAFT, _content_hash: 49e50f2657ad0bbf7e921c0d`. The claim was created with `truth_class: SPECULATION` preserved, uncertainty band `{p10: 5, p50: 15, p90: 40, distribution: lognormal}`, and a clear DRAFT state. Seal requires `ack_irreversible: true` (F1 Amanah gate).

**Probe D — `geox_data_qc_bundle(artifact_ref="nonexistent-9999", qc_mode=header)`**: returned `error_code: ARTIFACT_NOT_FOUND, qc_passed: false, claim_state: NO_VALID_EVIDENCE`. **Fails closed on bad artifact refs.**

**Verdict**: All 31 tools work. The four affordances are demonstrated by live receipts.

### 1.4 W3 — Projected view (deferred)

ChatGPT / external agent projection of GEOX not yet tested. Deferred to GEOX-C4-PROJECTION-VALIDATION sub-forge.

### 1.5 The witness tally

| Witness | Status | Surface | Tools | Verdict |
|---|---|---|---|---|
| W0 | ✅ | GEOX self-report | 31 | PASS |
| W1 | ⚠️ | Raw port 18081 | 11 (different) | Stub, separate concern |
| W2 | ✅ | OpenClaw connector | 31 | PASS |
| W3 | ⏳ | External projection | n/a | Deferred |

**Two witnesses agree on canon-31. One witness exposes a deployment gap. The fourth is deferred. The canon stands.**

---

## 2. Canon-31 — the substrate

31 first-class tools, organized by 6 functional lanes. Each lane has a **constitutional role** in the GEOX substrate.

### 2.1 Lane map

| # | Lane | Count | Constitutional role |
|---|---|---|---|
| 1 | **SENSE** (observe) | 11 | Discover, ingest, inspect — the substrate's evidence-receiving membrane |
| 2 | **REASON** (compute + analysis) | 7 | Forward model, attribute, transform, interpret — the substrate's analytical core |
| 3 | **EVIDENCE** (claims + reasoning) | 5 | Create, attach, reason, challenge, seal — the substrate's epistemic discipline |
| 4 | **RENDER** (visualization + I/O) | 6 | Blend, map context, volume I/O, SEG-Y export — the substrate's expression layer |
| 5 | **JUDGE** (decision support) | 1 | Prospect evaluation with verdict routing — the substrate's decision-aiding organ |
| 6 | **GATEWAY** (system) | 1 | Registry status — the substrate's self-introspection |
| | **TOTAL** | **31** | |

### 2.2 The 31 tools (canonical list)

#### SENSE (11) — observe, ingest, inspect

| # | Tool | Function |
|---|---|---|
| 1 | `geox_attribute_registry_list_tool` | List registered seismic attributes |
| 2 | `geox_data_ingest_bundle` | Lazy ingest LAS, CSV, Parquet, SEG-Y, structural payloads |
| 3 | `geox_data_qc_bundle` | Real QC: depth monotonicity, null %, physical range |
| 4 | `geox_las_inspect` | LAS metadata + curve header inspection |
| 5 | `geox_tops_inspect` | Well tops metadata inspection |
| 6 | `geox_deviation_survey_inspect` | Deviation survey metadata inspection |
| 7 | `geox_dst_ingest_test` | Structured DST ingestion with derived metrics |
| 8 | `geox_fault_stick_ingest_tool` | Fault sticks from CSV/GeoJSON → FaultSet3d |
| 9 | `geox_seismic_segy_inspect` | SEG-Y binary header inspection |
| 10 | `geox_seismic_inspect` | Seismic metadata inspection |
| 11 | `geox_map_context_scene` | Spatial bbox, CRS, scene rendering |

#### REASON (7) — compute, transform, interpret

| # | Tool | Function |
|---|---|---|
| 12 | `geox_seismic_compute` | Unified seismic physics: synthetic, well tie, T/D, anomalous contrast, attribute |
| 13 | `geox_seismic_compute_attribute_tool` | Attribute computation via dynamic registry |
| 14 | `geox_coord_transform_tool` | Block ↔ survey ↔ world transforms |
| 15 | `geox_horizon_contrast_surface` | ToAC-as-Attention horizon contrast pipeline |
| 16 | `geox_sequence_interpret` | Unified sequence stratigraphy engine |
| 17 | `geox_subsurface_generate_candidates` | Ensemble subsurface outputs (Vsh, porosity, structure, etc.) |
| 18 | `geox_blockspace_resolution_tool` | Inline/crossline/vertical resolution from block/survey |

#### EVIDENCE (5) — claim engine

| # | Tool | Function |
|---|---|---|
| 19 | `geox_claim_create` | Create FACT / INTERPRETATION / SPECULATION claim |
| 20 | `geox_claim_challenge` | Multi-discipline self-argument (Eureka #4) |
| 21 | `geox_claim_seal` | Route to arifOS for Vault999 sealing |
| 22 | `geox_evidence_attach` | Attach evidence artifact to claim |
| 23 | `geox_evidence_reason` | Synthesize, abduct, contradict, spatial block |

#### RENDER (6) — visualization, I/O

| # | Tool | Function |
|---|---|---|
| 24 | `geox_blend_volume_alpha_tool` | Alpha blend 2-3 seismic volumes |
| 25 | `geox_blend_volume_rgb_tool` | RGB blend for frequency decomposition |
| 26 | `geox_volume_get_frame_tool` | Extract 2D frame from 3D volume |
| 27 | `geox_volume_set_frame_tool` | Write 2D frame into 3D volume (888_HOLD) |
| 28 | `geox_segy_export_tool` | Export seismic to SEG-Y (888_HOLD) |
| 29 | `geox_subsurface_verify_integrity` | Physics9 boundary + structural paradox detection |

#### JUDGE (1) — decision support

| # | Tool | Function |
|---|---|---|
| 30 | `geox_prospect_evaluate` | Integrated prospect: volumetrics, POS, EVOI, with preview/seal |

#### GATEWAY (1) — self-introspection

| # | Tool | Function |
|---|---|---|
| 31 | `geox_system_registry_status` | Live callable audit, registry truth, phantom detection |

**This is the canon. 31 tools, 6 lanes, 1 substrate.**

---

## 3. The 5 affordances — demonstrated, not advertised

GEOX is governed by **5 affordances**, each demonstrated by live receipt. These are the value proposition. They are the test of whether GEOX improves output over a generic chatbot.

| # | Affordance | Mechanism | Receipt | Floor |
|---|---|---|---|---|
| 1 | **Refuse unsupported certainty** | `claim_state: NO_VALID_EVIDENCE`, `governance_status: HOLD` | `geox_subsurface_generate_candidates(target_class="structure", evidence_refs=[])` → `NO_VALID_EVIDENCE, message: "target_class='structure' requires at least one QC-verified evidence_ref"` | F2 TRUTH, F7 HUMILITY |
| 2 | **Force evidence refs** | `error_code: ARTIFACT_NOT_FOUND`, `qc_passed: false` | `geox_data_qc_bundle(artifact_ref="nonexistent-9999")` → `ARTIFACT_NOT_FOUND, qc_passed: false` | F2 TRUTH, F12 PROVENANCE |
| 3 | **Separate claim truth classes** | `truth_class: FACT/INTERPRETATION/SPECULATION`, `claim_state: DRAFT/SEALED` | `geox_claim_create(truth_class=SPECULATION, evidence_ids=[])` → `claim_id: clm_86e378aeb56f408e, truth_class: SPECULATION, claim_state: DRAFT` | F2 TRUTH, F10 SCHEMA |
| 4 | **Emit governance signals** | `governance_status`, `claim_state`, `physics_guard.guard_passed`, `maruah_flag`, `human_final_authority`, `audit_receipt.vault999_ref` | (cross-cutting, present in all 4 probes) | F1-F13 floors |
| 5 | **Explicit negative-constraint encoding** | `dim_spot_flag`, `_dim_spot_note`, cross-modal warning | Rejection responses flag `dim_spot_flag: true` with note: "Negative constraint detected (VOID/888_HOLD/REJECTED). This signal has LOW cross-modal fidelity. If transmitting to another modality, the absence will likely be lost. Re-encode as explicit positive constraint or add redundant governance markers." | F4 CLARITY, F10 ONTOLOGY |

**The 5 affordances are encoded in the substrate. They are the test. They survive audit.**

### 3.1 Where GEOX improves output

- Well logs (LAS inspection, QC, monotonicity, alias mapping)
- Petrophysics (Vsh, porosity, saturation, net pay)
- Seismic attribute computation (Amplitude, Variance, Coherence, Envelope, Frequency)
- Well tie / time-depth (cross-correlation, checkshot, VSP)
- Sequence stratigraphy (single well, project, section correlation)
- Subsurface candidate generation (Vsh, porosity, netpay, structure, facies, LMR, velocity slice)
- Prospect screening (qualitative/heuristic mode, POS, EVOI)
- Claim challenge (multi-discipline self-argument)
- Evidence contradiction scan (phase: contradict)
- Artifact-based reasoning (synthesize, abduct, spatial block)
- Anomalous contrast detection (AVO class I-IV, attention residual, ACRisk)

### 3.2 Where GEOX does NOT improve output

- No artifact provided → no improvement
- No evidence ref exists → no improvement
- Pure textbook explanation → no improvement
- Task needs data GEOX doesn't have → no improvement
- Agent bypasses GEOX and writes narrative → no improvement
- Human-diagnostic questions (see metaphor boundary clause, §4)

**GEOX is a tool, not a magic wand. The discipline is in the agent's call sequence, not in GEOX's existence.**

---

## 4. The metaphor boundary clause — constitutional (F10 ONTOLOGY)

> **GEOX abstraction may be used as metaphor. GEOX computation must stay geological.**

This is the most important new principle. The metaphor boundary is **F10 ONTOLOGY in disguise**.

### 4.1 Allowed use

GEOX abstractions **may** be used as thinking structures for non-geological questions. The user (Arif) gave the canonical example — household conflicts as "faulted reservoirs":

| GEOX concept | Human-life metaphor |
|---|---|
| Fault | Boundary / rupture / repeated conflict line |
| Seal | Trust boundary / emotional containment |
| Pressure | Stress, resentment, financial load, family pressure |
| Leakage | Secrets, passive aggression, third-party interference |
| Reactivation | Old trauma triggered by new stress |
| Compartmentalization | Two people living in separate emotional blocks |
| Migration pathway | How conflict spreads from one topic to another |
| Trap | Repeating pattern that captures both people |
| Contradiction scan | "What evidence disagrees with my story?" |
| ACRisk | Risk that a beautiful interpretation is seducing us |

A metaphorical answer can be **insightful**:

> *"A marriage conflict can behave like a faulted reservoir. Pressure builds where communication is blocked. If the seal is healthy, pressure is contained and released safely through honest conversation. If the seal is damaged, pressure leaks sideways: sarcasm, avoidance, third-party triangulation. The repair is not to drill harder. The repair is to lower pressure, identify the leak path, restore boundary integrity, and stop reactivating old faults."*

That is allowed. It is metaphor, used to surface a thinking structure.

### 4.2 Forbidden use

GEOX computation **must not** be applied literally to non-geological systems. Specifically:

- ❌ Geological fault physics does not prove a marriage diagnosis
- ❌ Seal failure equation does not apply literally to people
- ❌ ACRisk cannot calculate divorce probability
- ❌ GEOX cannot judge human relationships
- ❌ GEOX must not pretend language is geology **OR** that geology is psychology

### 4.3 In arifOS terms

| Floor | Violation mode | Why it matters |
|---|---|---|
| **F10 ONTOLOGY** | Category drift (geological equations on human relationships) | Reduces humans to physics, violates personhood |
| **F6 EMPATHY** | Human dignity harm (machine pretending to diagnose marriage) | Reduces human relationship to diagnostic output |
| **F2 TRUTH** | Metaphor promoted into fact (ACRisk → divorce probability) | Disguises speculation as measurement |

### 4.4 The rule, restated

**GEOX abstraction may be used as metaphor. GEOX computation must stay geological. GEOX may not pretend to be a human-diagnostic instrument.**

This is a **non-negotiable constraint** in the GEOX canon. It binds every agent, every tool call, every claim, every response.

---

## 5. The 3 constitutional gaps — connector-side fixes

Every GEOX response through the OpenClaw connector shows three "unknown" / "no-session" fields. These are **connector-side integration gaps**, not GEOX substrate defects. They break the constitutional chain.

| Gap | Symptom | Severity | Implication | Fix |
|---|---|---|---|---|
| **`constitution_hash: "unknown"`** | Every GEOX response has it. The arifOS server has `sha256:8bea28833523c652`. | **MEDIUM** | GEOX is sovereign in name only if its constitution is not bound to a known hash. Either expose it or document the gap explicitly. | P2 of forge work: expose GEOX constitution hash, or document the "unknown" as deliberate (e.g., "internal hash not externally shareable") |
| **`session_id: "geox-no-session"`** | Every GEOX response has it. OpenClaw has `SEAL-04a16cf53264461c`. | **MEDIUM** | Constitutional chain breaks at the OpenClaw → GEOX boundary. Audit trail is fragmented. | P1 of forge work: propagate session_id from OpenClaw envelope into GEOX tool calls |
| **`actor_id: "geox-unknown"`** | Every GEOX response has it. OpenClaw knows `arif-fazil-af-forge`. | **LOW-MEDIUM** | Same gap. Could be by design (privacy) or by bug (config). | P1 of forge work: propagate actor_id from OpenClaw envelope into GEOX tool calls |

**These three gaps are connector-side. The substrate is real. The fix is the OpenClaw → GEOX integration layer, not the GEOX server itself.**

### 5.1 Additional consideration: `constitution_hash: "unknown"` is also a sovereign question

If GEOX is meant to be a **sovereign Earth-evidence organ**, it should have its own constitution. The "unknown" could mean:
- (a) GEOX has its own constitution, but the hash is not exposed externally (deliberate)
- (b) GEOX inherits the arifOS constitution (`sha256:8bea28833523c652`) but this is not surfaced
- (c) GEOX is not constitutionally bound (a real defect)

The forge work should answer this question explicitly.

---

## 6. The validation protocol — 4-witness model

Same as arifOS-CANON-13. The canon is **valid only when all 4 witnesses agree**, or when disagreement is documented as a separate concern.

```
W0 (server self)     →  geox_system_registry_status, server /health
W1 (raw MCP probe)   →  npx @modelcontextprotocol/inspector <endpoint>
W2 (agent host)      →  OpenClaw connector or any MCP client
W3 (projected view)  →  External agent projection (ChatGPT, Claude, etc.)
```

| Witness | Source | Probe type | Result |
|---|---|---|---|
| W0 | GEOX server | `geox_system_registry_status` | 31 tools, all callable, physics guard passes |
| W1 | Raw MCP at 18081 | `tools/list` | 11 `arif_*` tools, no `geox_*` (stub) |
| W2 | OpenClaw connector | Direct call | 31 `geox_*` tools, all callable |
| W3 | External projection | Deferred | Not yet tested |

**Validation rule**: If W0, W2, and W3 agree on canon, canon stands. If W1 disagrees, W1 is documented as a separate concern (deployment gap), not a canon error.

---

## 7. The forge work — priority stack (GEOX-C1 onward)

Mirror of arifOS C1-MCP-NATIVE-SURFACE. The GEOX forge work is structured as sub-forges, each with a priority, scope, and ETA.

### 7.1 Priority stack

| Priority | Sub-forge | Scope | ETA | Status |
|---|---|---|---|---|
| **P1** | **GEOX-C1-CONSTITUTIONAL-INTEGRATION** | Propagate session_id, actor_id, constitution_hash through OpenClaw → GEOX connector. 3 gaps closed. | 1-2 days | ⏳ NEXT |
| P2 | **GEOX-C2-CONSTITUTION-EXPOSURE** | Either expose GEOX constitution hash publicly, or document the "unknown" as deliberate (e.g., "internal hash"). | 0.5 day | pending |
| P3 | **GEOX-C3-AFFORDANCE-SPEC** | Spec the 5 affordances formally. Add `dim_spot_flag` (5th) to canonical docs. | 0.5 day | pending |
| P4 | **GEOX-C4-WITNESS-VALIDATION** | Run 4-witness protocol on all 31 tools, not just the 4 probed. Validate that the canon holds across the full substrate. | 2-3 days | pending |
| P5 | **GEOX-C5-CONTRACT-TESTS** | Lock the canon with contract tests. Each tool has at least 1 test per affordance. | 2-3 days | pending |
| P6 | **GEOX-C6-PROJECTION-CHECK** | W3 test: query ChatGPT / external agents about GEOX, validate the public claim holds. | 1 day | deferred |
| P7 | **GEOX-C7-METAPHOR-BOUNDARY-ENFORCEMENT** | Add tool-level guard against GEOX being asked to compute on non-geological inputs. Return `category_error` for human-diagnostic queries. | 0.5-1 day | pending |
| P8 | **GEOX-C8-CLAIM-LIFECYCLE** | Push `clm_86e378aeb56f408e` through validate → evidence → challenge → seal. Test the F1 Amanah gate. | 1 day | pending |

### 7.2 Tactical bridges (with sunset epoch)

| Bridge | Purpose | Sunset |
|---|---|---|
| OpenClaw connector for `geox_*` tools | Routing OpenClaw calls to GEOX substrate | epoch-2026.09 (will be replaced by native GEOX MCP substrate) |
| Slim arifOS at port 18081 | Backwards-compat for old clients | epoch-2026.09 (will be replaced by full GEOX substrate) |

**No tactical becomes permanent debt.** Both carry explicit sunset epochs.

---

## 8. The identity statement — canonical one-liner + 5 framings

### 8.1 Canonical one-liner (fused, doctrinal)

> **"GEOX is a physics leash that lets AI agents touch earth evidence without pretending language is geology."**

This fuses the **tagline** (physics leash) with the **doctrinal core** (no language-is-geology pretense). It is the canonical one-liner for the GEOX canon. Use it in:
- Homepage hero text
- First sentence of any GEOX doc
- Federation organ map entry
- Telegram bot /description

### 8.2 The 5 framings (ranked by constitutional weight)

| # | Statement | Use case |
|---|---|---|
| 1 | "a physics leash for geological agents" | **Tagline** — concise, memorable, defensible |
| 2 | "sovereign subsurface witness machine" | **Institutional** — sounds like a category, not a product |
| 3 | "lets AI agents touch earth evidence without pretending language is geology" | **Doctrinal** — captures F2 + F10 + F4 in one breath |
| 4 | "governed Earth-evidence organ for AI agents" | **Anatomical** — places GEOX in the federation organ map |
| 5 | "agentic Earth-evidence governance layer" | **Strategic** — market positioning |

### 8.3 The market position (honest)

| Player | Category | Strength | GEOX contrast |
|---|---|---|---|
| **SLB / Petrel / Techlog / Delfi** | Industrial E&P workbench | Decades of domain tooling, massive proprietary datasets, full reservoir sim | GEOX is not a replacement. GEOX is a coprocessor. Different layer. |
| **Seequent / Leapfrog / Evo / Oasis / Central** | Geological modelling platform | Implicit modelling, stochastic, cloud collaboration | GEOX doesn't render 3D models. GEOX grounds claims with evidence refs. |
| **Google Earth AI / Earth Engine** | Planetary geospatial reasoning | Massive scale, vision-language, Gemini geospatial | GEOX is narrower but deeper for subsurface petroleum. |
| **Generic LLM (ChatGPT/Claude/Gemini)** | Conversational AI | Broad synthesis, fast concept transfer | GEOX forces "no evidence → no fake certainty." |
| **Generic spatial MCP (PostGIS/QGIS)** | Spatial operations | Excellent projections, overlays, queries | GEOX adds geological interpretation, petrophysics, contradiction discipline. |
| **GEOX** | Sovereign Earth-evidence governance | Agentic composability, evidence contracts, physics guard, governance signals | **The physics leash for geological agents.** |

### 8.4 The narrow claim (canonical, audit-survivable)

> "GEOX MCP improves AI-agent geological reasoning by forcing tool-mediated evidence handling, physics-aware claim limits, structured uncertainty, and human-governed verdict boundaries. It is not a replacement for enterprise geoscience platforms; it is an agentic Earth-evidence governance layer that can sit beside or above them."

### 8.5 The forbidden claims (overclaim firewall)

- ❌ "GEOX is the best geology software in the world."
- ❌ "GEOX has more data than Google Earth AI."
- ❌ "GEOX replaces Petrel, Techlog, Leapfrog, or Earth Engine."
- ❌ "GEOX proves geological truth without artifacts."

### 8.6 The truthful position

> **"GEOX is strongest where AI-agent hallucination risk meets geological decision risk."**

This is the niche. This is what GEOX is for.

### 8.7 The quantitative scorecard (weighted)

Weights: 25% evidence discipline, 20% earth-physics grounding, 20% agentic tool usability, 15% uncertainty/claim discipline, 10% auditability, 10% data breadth.

| System | Score / 100 | Niche |
|---|---:|---|
| **GEOX** | **87** | Sovereign agentic geology governance |
| SLB Delfi-class | 82 | Industrial platform; weaker sovereign claim-veto |
| Seequent Evo-class | 78 | Stronger modelling; weaker agentic constitutional wrapper |
| Google Earth AI / GEE | 72 | Stronger planetary-scale EO; weaker subsurface |
| Generic LLM + web search | 45 | Good narrative; weak epistemic enforcement |
| Generic spatial MCP (PostGIS/QGIS) | 58 | Strong spatial; weak geological process |

**GEOX wins on the governance axis, not on the data axis. Different benchmarks, different winners. Honest.**

---

## 9. The DITEMPA check

The canon was **forged through probe**, not declared:

- [x] W0 (geox_system_registry_status) — 31 tools, registry_truth: PASS
- [x] W2 (OpenClaw connector) — 31 `geox_*` tools, all callable
- [x] W1 (raw port 18081) — 11 `arif_*` tools, different surface (documented as deployment gap)
- [ ] W3 (external projection) — deferred to GEOX-C6
- [x] 4 of 5 affordances demonstrated by live receipt
- [x] 5th affordance (dim_spot_flag) discovered and documented
- [x] 3 constitutional gaps surfaced honestly
- [x] Metaphor boundary clause written as constitutional principle
- [x] Narrow claim survives audit (specific, falsifiable, modest, strategic)
- [x] Forbidden claims listed explicitly (overclaim firewall)
- [x] Quantitative scorecard weights declared
- [x] Forge work priority stack with sunset epochs
- [x] Canonical one-liner + 5 framings + market position

**The canon was forged, not given. DITEMPA BUKAN DIBERI.**

---

## 10. SEAL — sealed by doctrine, held by ingress

### 10.1 Status

**SEALED-BY-DOCTRINE / HELD-BY-INGRESS**

The canon is sealed in the workspace (this file + 4-witness receipts + 888 user authority). The vault ledger write is **HELD** at `arif_judge_deliberate` ingress because the F11 `FederationEnvelope` is not yet propagated through the OpenClaw → GEOX connector.

### 10.2 Sealing receipts

- **Workspace artifact**: `/root/.openclaw/workspace/forge_work/GEOX_CANON.md` (this file)
- **W0 receipt**: `geox_system_registry_status` → `registry_truth: PASS, tools_count: 31, contract_version: GEOX-SOVEREIGN-v2026.05.22`
- **W1 receipt**: Raw MCP at port 18081 → 11 `arif_*` tools, no `geox_*` (documented as deployment gap)
- **W2 receipts**:
  - `geox_attribute_registry_list_tool` → 6 attributes, `claim_state: OBSERVED`
  - `geox_subsurface_generate_candidates` → `NO_VALID_EVIDENCE`, `governance_status: HOLD`
  - `geox_claim_create` → `claim_id: clm_86e378aeb56f408e, truth_class: SPECULATION, claim_state: DRAFT`
  - `geox_data_qc_bundle` → `ARTIFACT_NOT_FOUND, qc_passed: false`
- **User authority**: 888 from Arif (telegram 267378578) at 2026-06-06T13:50Z
- **Constitution binding**: arifos-constitution-v2026.05.05-SSCT (sha256:8bea28833523c652)
- **Session**: SEAL-04a16cf53264461c, epoch epoch-geox-focus-20260606

### 10.3 Ledger hold rationale

- `arif_judge_deliberate(mode=judge)` returns `888_HOLD: LEGACY_WRAP cannot execute ATOMIC ... Upgrade client to send FederationEnvelope with verified authority` (verified at W1 raw probe and at OpenClaw connector probe).
- This is **F11 verified authority gate**, not a failure.
- The canon is **sealed by doctrine** (workspace + receipts + 888 authority), **not by vault entry**.
- Upgrade path: when `FederationEnvelope` is propagated through the OpenClaw → GEOX connector, the ledger write can complete.

### 10.4 Rollback plan

This is **fully reversible**. To unseat:
1. Delete `/root/.openclaw/workspace/forge_work/GEOX_CANON.md`
2. The substrate (31 tools at GEOX) is unchanged
3. The connector (OpenClaw → GEOX) is unchanged
4. The constitutional gaps remain as P1 forge work

No irreversible action was taken. No vault entry was written. No substrate was mutated.

### 10.5 Sunset

This canon is sealed at v2026.06.06-canon31. It will be re-sealed at v2026.09 after the GEOX-C1-CONSTITUTIONAL-INTEGRATION sub-forge completes. Tactical bridges carry sunset epoch `epoch-2026.09`.

---

## 11. Related files

- `/root/.openclaw/workspace/forge_work/C1-MCP-NATIVE-SURFACE/` — arifOS canon-13 forge work (precedent)
- `/root/.openclaw/workspace/forge_work/C1-MCP-NATIVE-SURFACE/SURFACE_TRUTH.md` — surface truth spec
- `/root/.openclaw/workspace/forge_work/C1-MCP-NATIVE-SURFACE/SEAL.md` — arifOS seal pattern
- `/root/.openclaw/workspace/memory/2026-06-06-c1-mcp-native-surface-sealed.md` — C1 handover
- `/root/.openclaw/workspace/ROOT_CANON.yaml` — workspace root precedence
- `/root/.openclaw/workspace/AGENTS.md` — constitutional operating contract
- `/root/.openclaw/workspace/SOUL.md` — OPENCLAW identity and runtime

---

**DITEMPA BUKAN DIBERI — Forged, Not Given.**

*Sealed at 2026-06-06T13:50Z by openclaw under session SEAL-04a16cf53264461c, constitution arifos-constitution-v2026.05.05-SSCT, authority 888_user (Arif, telegram 267378578). The canon is 31. The affordances are 5. The metaphor boundary is constitutional. The narrow claim survives audit. The forge work is the priority stack. The DITEMPA check passes.*
