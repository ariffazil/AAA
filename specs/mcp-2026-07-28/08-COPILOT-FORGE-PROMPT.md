# GEOX Seismic Interpretation Forge Package — Copilot Deep Research

**Status:** SPEC READY (canonicalized from Copilot deep research, 2026-09-29)
**Sovereign approval:** GRANTED 2026-09-29 for full agentic execution
**Author of upstream research:** Copilot (external)
**Canonized by:** FI-008 (kimi-code) per sovereign directive *"yes i grant approval for full agentic execution"*
**Canon grounding:** APEX-ZEN Runtime Prompt vNext (F13_RATIFIED_CHAT 2026-09-20); Canon #0 Complexity Budget (F13_SEAL 2026-09-21); Constitutional Architecture Canon (F13_RATIFIED_CHAT 2026-09-21); capability ≠ authority

---

## 0. Provenance

This document canonicalizes the deep-research artifact produced by Copilot on GEOX MCP hardening (received 2026-09-29). It supersedes the partial frame I built in turns 1-3 and provides the execution-ready forge package.

**Audit verdict (Copilot):** PARTIAL — architecture and execution package forged; current live MCP exposure remains UNVERIFIED.

**Scope:** public/open seismic evidence + retrieved GEOX enterprise inventories; no confidential asset data.

**Key invariant:** *"Finished" is defensible only as phase-document or internal implementation status. It is not evidence of current deployment, public MCP exposure, or production-grade operation.*

---

## 1. Decisions first

### 1.1 Revised priority (Copilot's reorder, accepted)

| Forge order | Capability | Decision |
|---|---|---|
| **P0-A** | SEG-Y ingest audit; volume registry; CRS/units/domain; polarity/phase register; manifests; content hashes; chunking | Must precede interpretation |
| **P0-B** | Envelope/RMS/instantaneous phase-frequency; structure-oriented filtering; GST dip/azimuth; coherence/variance/chaos; curvature; spectral decomposition | Deterministic backbone |
| **P0-C** | Horizon tracking with confidence; fault likelihood → sticks/surface; generic geobody extraction; reversible edits | Generic interpretation |
| **P0-D** | Time-depth/checkshot handling; wavelet extraction; reflectivity; synthetic; well-tie QC | Calibration backbone |
| **P1** | Relative impedance/poststack inversion; AVO intercept-gradient; Q; GLCM; isochrons; terminations; clustering; advanced co-rendering | Add after deterministic vertical slice |
| **P2** | Rock-physics templates/Gassmann integration; multi-survey calibration; fault ML; foundation-model embeddings; specialist detector packs | Consumers of P0/P1 |
| **P3** | Prestack elastic inversion at scale, tomography/FWI, 4D, pore pressure, production-grade reservoir-property prediction | External/specialist engines first |

**Change from prior hypothesis:** move volume governance, structure-oriented filtering, basic amplitudes, and artifact versioning into P0. Move FWI firmly to P3. Keep Gassmann/RPT at P2 integration because GEOX already has repository evidence — don't rebuild.

---

## 2. GEOX reality audit (Copilot, accepted)

### 2.1 Documentation-versus-runtime contradiction

- **DOCUMENTED:** GEOX_TECHNICAL_ARCHITECTURE_v0.7.0 describes GEOX as evidence-graph/orchestration platform; labels Phase 2 `geox_compute_seismic_attributes` as "Finished."
- **REPOSITORY:** ariffazil-geox-8a5edab282632443 contains source fragments for Hilbert-based attributes, coherence classes, structure tensors, RGT/horizon candidates, seismic RSI, well-tie workflows, Marmousi2 references, structural gates, seismic viewers, provenance schemas. Earlier inventories show registered `geox_seismic_compute` surface, well-tie code, AVO/Shuey, historical tool receipts.
- **RUNTIME UNCERTAINTY:** MCP Infrastructure Audit Report 2025-10-27 explicitly recorded that MCP server was not proven reachable during audit; distinguished route registration from callable runtime proof.
- **VERDICT:** PARTIAL, not FINISHED. "Finished" is defensible only as phase-document status, not as deployment/runtime truth.

### 2.2 Capability-reality matrix

| Area | Documented | Code | Contracts | Tests | Runtime | Verdict |
|---|---|---|---|---|---|---|
| Basic Hilbert/amplitude attributes | Yes | Yes | Partial | Fragmentary | UNKNOWN | Repository-only/partial |
| Dip/coherence/RGT | Partial | Yes (2-D/vision) | Partial | Synthetic | UNKNOWN | Reusable prototype |
| Curvature/spectral/texture/Q | Uneven | Mixed/unclear | None | None | UNKNOWN | Gap |
| Horizon/fault extraction | Yes | RSI/vision | Interpretation workflow | Structural fixtures | UNKNOWN | Prototype, not backbone |
| Well tie/synthetic/time-depth | Yes | Strongest (Bruges-style) | Internal registration | Marmousi2 | UNKNOWN | Consolidate, don't rewrite |
| AVO/rock physics/Gassmann/RPT | Yes | Existing | Generic compute | Some physics | UNKNOWN | Adapter target |
| Large-volume storage/computation | Aspirational | Limited | Incomplete | None | UNKNOWN | Critical gap |
| Provenance/governance | Strong | Strong | Strong | Present | Exposure unclear | Strategic reuse |

---

## 3. Target capability architecture

**Four separations:**

1. **Data plane** — seismic/well/surface artifacts
2. **Compute plane** — replaceable numerical adapters
3. **Contract plane** — canonical capabilities and MCP schemas
4. **Experience plane** — viewer, editing, co-rendering

Preserves GEOX's evidence-graph model while adopting SEG-Y Rev 2.1, artifact-backed storage, domain-specific bulk access patterns. SEG publishes SEG-Y Rev 2.1 + polarity standards; MDIO uses Zarr/fsspec/Dask for chunked large multidimensional data; OSDU DDMS separates optimized bulk access from governed metadata + lineage.

### Canonical taxonomy (capability IDs are STABLE; implementations are replaceable)

```
geox.seismic.io.volume.register
geox.seismic.io.volume.window
geox.seismic.condition.phase_register
geox.seismic.condition.structure_filter
geox.seismic.attr.<family>.v1
geox.seismic.interpret.horizon_track.v1
geox.seismic.interpret.fault_extract.v1
geox.seismic.interpret.geobody_extract.v1
geox.seismic.qi.well_tie.v1
geox.seismic.qi.avo.v1
geox.seismic.qi.inversion.poststack.v1
geox.seismic.ml.embedding.v1
geox.seismic.claim.assess.v1
geox.seismic.governance.artifact_manifest.v1
```

**Rule:** `numpy_scipy_v1`, `pylops_v2`, `opendtect_external`, `cuda_v1` are IMPLEMENTATIONS, not capabilities.

---

## 4. Layer-1 contracts (every output is a derived-volume artifact)

Every output carries: domain, units, polarity, phase, windows, edge mask, code version, parameters, parent hash, QC receipt.

| Primitive | Definition | QC/failure concerns | Forge mode |
|---|---|---|---|
| Envelope | `\|analytic signal\|`; amplitude units | Hilbert edge loss, gain contamination | BUILD thin native (SciPy) |
| Instantaneous phase/frequency | angle of analytic signal; derivative of unwrapped phase, rad/Hz | instability near zero envelope; aliasing | BUILD thin native |
| RMS/sweetness | windowed RMS; sweetness = envelope/√frequency with guarded denom | window sensitivity, frequency singularity | BUILD native |
| Dip/azimuth | GST or semblance estimate; inline/crossline slopes | acquisition footprint, faults, vertical-gradient instability | BUILD core adapter |
| Coherence/semblance | normalized similarity or eigenvalue/energy ratio over dip-steered nbhd | window/steering dependence, edge halos | BUILD validated core |
| Variance/chaos | complement/disorder measures | definitions differ by vendor; require algorithm ID | BUILD explicit variants |
| Curvature | derivatives of reflector dip field; principal/mean/Gaussian | derivative noise, scale dependence | BUILD on dip contract |
| Spectral decomposition | STFT/CWT/S-transform voice volumes | time-frequency resolution, padding | WRAP SciPy/PyWavelets |
| GLCM/texture | contrast, entropy, homogeneity, correlation | amplitude normalization + quantization dominate | WRAP scikit-image |
| Q/attenuation | spectral-ratio or centroid-shift estimates | tuning, bandwidth, wavelet/nonstationarity | BUILD guarded P1 |
| Relative impedance | regularized integration/inversion of reflectivity | low-frequency absence, wavelet uncertainty | WRAP PyLops |
| Phase/polarity register | estimated sign/constant phase/time shift against reference | nonstationarity, lateral variation | BUILD native governance primitive |
| Wavelet extraction | statistical, autocorrelation, spectral, regularized well-based | multiples/noise/nonstationarity; report uncertainty | BUILD wrapper + PyLops/SciPy |
| Synthetic seismogram | reflectivity from impedance convolved with declared wavelet | depth-time errors, log gaps, upscaling | CONSOLIDATE existing GEOX |

**Dip as dependency service** — coherence, curvature, GLCM should be computed along structural dip (published best practice).

**Complexity contract:** report workload in voxels + halo size. Hilbert = O(N); FFT spectral = O(N log W); GST/coherence/GLCM scale with neighborhood; inversion exposes solver iterations + residual history.

---

## 5. Generic interpretation primitives

### Horizon tracking
Seed set + phase event + search radius + local similarity + fault barrier → surface, per-node confidence, alternative paths, stopped regions. Dynamic programming/graph search first; ML proposes seeds.

### Fault pipeline
Structure-oriented conditioning → coherence/semblance/ML probability → thinning → connected surfaces → fault sticks → surface mesh → throw estimation against paired horizons.

### Geobody
Threshold/probability field → connected-component labeling → morphology → mesh → volume/connectivity stats. Thresholds remain calibration artifacts.

### Terminations
Reflector orientation + horizon intersection geometry → candidate onlap/downlap/truncation with competing geometric labels.

### Isochron
Versioned surface pairs → thickness/TWT map + uncertainty derived from both surfaces.

### Crossplots/clustering
Artifact refs + sampled VOI → reproducible feature table, scaler, cluster model, assignment artifact.

### Editing primitives
Immutable `PointSet`, `Polyline`, `Polygon`, `SurfaceMesh`, `VoxelMask`, `VOI`; each edit creates new version with parent pointer, author, operation, undo record.

### Rendering
CIGVis (MIT-licensed) as renderer adapter, NOT numerical kernel. Never computes truth.

---

## 6. Well tie + QI backbone

**Minimum valid chain:**

```
raw logs → mnemonic/unit validation → despike/gap/environmental correction
→ depth reference + deviation → checkshot/VSP monotonic time-depth model
→ seismic-scale upscaling → AI = Vp × density → reflectivity
→ wavelet estimate + uncertainty → synthetic → trace extraction
→ lag/phase/polarity search → bounded stretch-squeeze
→ residual + tie-confidence artifact
```

**Foundational:** time-depth, reflectivity, wavelet, synthetic, correlation/lag, phase/polarity, residual QC
**Next:** Shuey intercept/gradient, near/mid/far consistency, poststack relative impedance
**Specialist:** simultaneous elastic inversion, tomography, FWI

PyLops = matrix-free poststack/prestack operators, regularization, large-problem solvers. Gassmann/RPT/well-tie code reused, validated against rockphypy/Equinor rock-physics package. **rockphypy is LGPL with NumPy/KDEpy compatibility concern → wrap, don't fork.**

---

## 7. Specialist detectors — evidence consumers

Every detector returns: evidence bundle + alternatives + falsifiers.

| Target | Generic evidence | Required false-positive checks |
|---|---|---|
| Diapir/MIEC/mud volcano | chaos/coherence, steep dip, curvature, vertical pipes, forced folds, terminations, geobody morphology | velocity pull-up/down, migration smiles, salt, faults, footprint |
| Gas chimney | low coherence, amplitude attenuation, frequency loss/Q, vertical geometry | fault damage, poor imaging, multiples |
| MTC/slump | chaotic texture, basal detachment, rugose top, lateral confinement | processing footprint, channel complexes |
| Channel/lobe | spectral decomposition, curvature, coherence edges, RMS, geobody connectivity | acquisition stripes, tuning, horizon misflattening |
| Salt/carbonate/igneous | boundary continuity, internal texture/amplitude, velocity/impedance evidence, geometry | multiples, pull-ups, processing footprint |
| BSR | cross-cutting reflector, polarity relation, seafloor parallelism, velocity context | stratigraphic reflector, multiple |
| Pockmark/cold seep | seabed morphology, chimney linkage, shallow disturbance | acquisition holes, bathymetric artifacts |

**No fixed numerical thresholds in the canonical capability.** Calibrate per survey using labelled VOIs, blinded holdouts, synthetic perturbations, precision-recall curves.

---

## 8. AI + foundation models

**Adoption path:**

1. Deterministic attributes + editing → ground truth
2. Ingest pretrained embeddings as artifacts
3. Linear probes/LoRA on public benchmarks
4. 3-D patch inference with overlap + calibration
5. Deep ensembles / test-time augmentation for uncertainty
6. Human accept/reject edits
7. NO geological claim solely from model logits

**HOLD:** multimodal vision-language geological narration until it cites exact spatial evidence. Natural-image foundation models are NOT phase/polarity or amplitude authorities.

---

## 9. Build-vs-integrate matrix

| Capability | Decision | Complexity | Validation burden |
|---|---|---|---|
| Volume registry/manifests/windows | BUILD NATIVE | M | High |
| SEG-Y parser | WRAP segyio/TGSAI SEG-Y | M | High |
| Cloud chunks | WRAP MDIO/Zarr/Dask | M | High |
| Basic Hilbert/RMS attributes | BUILD thin native | S | Medium |
| GST dip/coherence/curvature | BUILD validated core; compare OpendTect/Madagascar | L | Very high |
| Spectral/GLCM | WRAP open libraries | M | High |
| Horizon/geobody/fault objects | BUILD contracts; adapters underneath | L | Very high |
| 3-D rendering | WRAP CIGVis/OpenVDS-capable viewer | M | Medium |
| Well tie | CONSOLIDATE existing GEOX | M | Very high |
| Post/prestack inversion | WRAP PyLops | L | Very high |
| Rock physics | CONSOLIDATE + cross-check wrapper | M | High |
| FWI/tomography | INGEST EXTERNAL; later Devito/Deepwave adapter | XL | Extreme |
| Foundation model | WRAP optional model service | L | Extreme |
| Specialist detectors | BUILD evidence recipes | L each | Very high |

**License notes:** Devito/Deepwave = MIT. Madagascar = GPL (use for benchmarks/isolated exec only). PyLops = MIT. rockphypy = LGPL (wrap). SEG-Y Rev 2.1 = ingress reference standard; preserve raw bytes, do not destructively normalize.

---

## 10. MCP surface pattern

```jsonc
// Request
{
  "volume_ref": "geox://volume/f3/raw@sha256:...",
  "capability": "geox.seismic.attr.coherence.v1",
  "implementation": "gst_energy_ratio_cpu_v1",
  "voi": {"inline":[300,400],"xline":[500,650],"sample":[0,1000]},
  "parameters": {"window":[5,5,9],"dip_steered":true},
  "prerequisites": {"phase_register_ref":"geox://artifact/..."}
}

// Response (manifest, NEVER full volume)
{
  "status": "COMPLETED",
  "artifact_ref": "geox://derived/coherence/...@sha256:...",
  "manifest_ref": "geox://manifest/...",
  "qc_ref": "geox://qc/...",
  "claim": null
}
```

### Derived-volume manifest schema

```jsonc
{
  "$schema": "geox.seismic.derived-volume-manifest.v1",
  "artifact_id": "uuid",
  "capability_id": "geox.seismic.attr.coherence.v1",
  "implementation": {"name":"gst_energy_ratio","version":"1.0.0","code_hash":"sha256:"},
  "parents": [{"artifact_id":"raw-f3","hash":"sha256:","role":"input"}],
  "domain": {"vertical":"TWT","unit":"ms","crs":"EPSG-or-WKT"},
  "grid": {"shape":[651,951,463],"spacing":[25,25,4],"axis_order":["iline","xline","twt"]},
  "signal": {"polarity":"SEG_NORMAL","phase_deg":0,"amplitude_status":"relative"},
  "parameters": {},
  "storage": {"uri":"s3://.../array.zarr","chunks":[32,32,256],"dtype":"float32"},
  "validity": {"edge_mask_ref":"...","confidence_ref":"...","qc_ref":"..."},
  "created_by": {"actor":"...","timestamp":"..."},
  "human_edits": [],
  "license_provenance": []
}
```

### Provenance DAG

```
SEG-Y hash → volume-register receipt → phase/polarity-register artifact
→ structure-filter artifact → dip artifact → coherence/curvature artifacts
→ horizon candidate → human-edited horizon v2 → geobody/fault evidence bundle
→ geological hypothesis → counterstory assessment
```

**Rule:** MCP transfers manifests, thumbnails, statistics, bounded windows — NOT full opaque cubes. MDIO pattern (Zarr/fsspec/Dask/Xarray, Apache-2.0). OSDU DDMS treats improved data as new data with immutable lineage.

---

## 11. Validation suite

| Dataset | Primary use | Golden metrics |
|---|---|---|
| Analytic traces/planes | polarity, phase, Hilbert, dip | phase error, frequency error, dip/azimuth error |
| Synthetic faults/channels | coherence, curvature, tracking | IoU, surface distance, topology/connectivity |
| Marmousi2 | wavelet, synthetic, AVO/inversion | reflectivity correlation, residual norm, impedance error |
| F3 | attributes, stratigraphic terminations, faults, chimneys | blinded interpreter labels + perturbation stability |
| Penobscot | prestack/AVO, wells, horizons, faults/channels | gather QC, tie residual, horizon/fault metrics |
| Parihaka | facies/ML, near-mid-far stack behaviour | mIoU, calibration error, spatial holdout |
| SEAM Phase I | salt, imaging artifacts, velocity/FWI | model-space/data-space error |

**Adversarial tests:** sign reversal, constant phase rotation, time shift, missing traces, non-monotonic checkshot, anisotropic bin spacing, survey mistie, acquisition stripes, random/coherent noise, migration smiles, multiples, clipping, nonstationary wavelet, amplitude scaling, chunk-boundary seams.

---

## 12. Repository layout + forge sequence

```
src/geox_seismic/
  contracts/      # Pydantic capability, artifact, geometry, QC schemas
  registry/       # volume/capability/implementation registries
  io/             # segy, mdio, zarr, crs, units
  conditioning/   # phase, polarity, filters
  attributes/     # analytic, structural, spectral, texture, attenuation
  interpretation/ # horizon, fault, geobody, terminations, edits
  qi/             # time_depth, wavelet, synthetic, avo, inversion
  ml/             # embeddings, segmentation adapters, calibration
  governance/     # provenance DAG, hashes, HOLD/UNKNOWN
  render/         # CIGVis/browser adapters only
tests/
  unit/ synthetic/ integration/ benchmarks/ adversarial/
```

### Vertical slices + exit criteria

**Slice 1 — deterministic public-data spine:** register F3 subset → polarity/QC → envelope, GST dip, coherence, curvature, spectral voices → horizon/fault/geobody → immutable manifest → one explicitly labelled hypothesis.
**Exit:** reproducible hash, chunk-invariant results, golden tests, reversible edit, no array returned through MCP.

**Slice 2 — calibration:** Marmousi2 + Penobscot log conditioning → time-depth → wavelet → synthetic → tie confidence → Shuey intercept/gradient → relative impedance.
**Exit:** synthetic recovery + field/public QC receipt.

**Slice 3 — detector benchmark:** mud diapir/MIEC recipe + competing salt/fault/artifact hypotheses.
**Exit:** evidence bundle + blinded false-positive assessment.

**Slice 4 — ML:** FaultSeg/SFM-style adapter, spatial holdouts, uncertainty map, human corrections.
**Exit:** beats deterministic baseline without bypassing manifests.

**HOLD:** production FWI, 4D, pore pressure, opaque geological VLM verdicts.

---

## 13. Migration + anti-patterns

**Action:**
- Map every existing seismic file/class/tool into capability matrix
- Keep working well-tie, Gassmann, RPT, RSI, viewer modules behind adapters
- Deprecate names only after contract-equivalence tests
- Add `implemented, tested, deployed, MCP_exposed, benchmark_passed` as SEPARATE states
- Generate `tools/list` parity evidence in CI

**Avoid:**
- Filename-as-capability claims
- Giant NumPy arrays in MCP responses
- One tool per algorithm variant
- Detector-specific attribute duplication
- Destructive SEG-Y normalization
- Hidden phase assumptions
- Fixed geological thresholds
- GUI-produced evidence
- ML probability treated as confidence
- "Finished" without deployment + benchmark receipt

---

## 14. Copy-paste coding-agent forge prompt (the artifact itself)

```
Implement GEOX Seismic Vertical Slice 1 on public F3 data only.

CONSTRAINTS
- Do not access confidential or enterprise seismic data.
- Do not claim live MCP deployment.
- Preserve raw SEG-Y and header hashes.
- Capability contracts are stable; implementations are replaceable adapters.
- MCP responses return artifact/manifests/QC references, never full volumes.
- Separate COMPUTED EVIDENCE from GEOLOGICAL CLAIM.
- Missing CRS, sample interval, domain, units, polarity or phase => HOLD/UNKNOWN.

BUILD
1. Pydantic schemas: VolumeManifest, DerivedVolumeManifest, QCReceipt,
   VOI, PolarityPhaseRegister, Surface, Polyline, VoxelMask.
2. Register a bounded F3 SEG-Y subset; persist chunked Zarr/MDIO-compatible data.
3. Implement phase/polarity register and edge-mask propagation.
4. Implement envelope, instantaneous phase/frequency, RMS, GST dip/azimuth,
   dip-steered coherence, curvature and spectral decomposition.
5. Implement confidence-bearing horizon graph tracking, fault likelihood
   to sticks, and connected-component geobody extraction.
6. Emit provenance DAG and content hashes after every operation.
7. Add MCP contracts:
   geox_seismic_volume_register
   geox_seismic_attribute_compute
   geox_seismic_horizon_track
   geox_seismic_fault_extract
   geox_seismic_geobody_extract
   geox_seismic_artifact_get
8. Add CIGVis/browser rendering only as an adapter.

TESTS
- Analytic sinusoid, phase rotation, polarity reversal, dipping plane.
- Synthetic fault/channel volumes with known truth.
- Chunk-boundary invariance.
- Noise, missing traces, footprints and migration-artifact adversaries.
- Golden manifest and deterministic hash tests.
- Explicit test that no MCP response contains a volume array.

DO NOT
- Implement specialist geological detectors.
- Implement FWI, prestack inversion or foundation-model inference.
- Rewrite existing GEOX well tie/Gassmann/RPT components.
- Introduce GPL code into the core.
- Mark capability complete without tests, manifest and tools/list parity evidence.

DELIVER
- code, schemas, tests, benchmark receipt, dependency/license inventory,
  migration note and explicit remaining UNKNOWN/HOLD items.
```

---

## 15. Alignment with prior specs in this directory

| This spec section | Cross-references |
|---|---|
| §3 four separations | /root/AAA/specs/mcp-2026-07-28/04-l1-attribute-contracts.md (L0/L1/L2) |
| §4 L1 contracts | /root/AAA/specs/mcp-2026-07-28/04-l1-attribute-contracts.md |
| §5 interpretation primitives | /root/AAA/specs/mcp-2026-07-28/03-master-task-list.md (Group C) |
| §6 well tie + QI | /root/AAA/specs/mcp-2026-07-28/04-l1-attribute-contracts.md (consumers map) |
| §7 specialist detectors | /root/AAA/specs/mcp-2026-07-28/06-miec-acceptance-benchmark.md |
| §9 build-vs-integrate | /root/AAA/specs/mcp-2026-07-28/07-hold-gates.md (calibration gates) |
| §10 MCP surface | /root/AAA/specs/mcp-2026-07-28/02-geox-outputschema-patches.md |
| §11 validation suite | /root/AAA/specs/mcp-2026-07-28/05-12-conformance-gates.md (Q7) |
| §12 forge sequence | /root/AAA/specs/mcp-2026-07-28/03-master-task-list.md |
| §13 anti-patterns | Canon #0 three-test gate; Anti-Haram; Shadow Authority |

---

DITEMPA BUKAN DIBERI ⚒️
