# L1 Attribute Contracts — Seismic Interpretation Primitives

**Status:** SPEC ONLY (3 examples fully specified; remaining 9 templates provided)
**Date:** 2026-09-29
**Owner:** FI-008 (kimi-code)
**Canon grounding:** L0/L1/L2 framework from prior conversation rounds; GEOX MCP audit; MUEC topology EUREKA
**L0 = external (Petrel/DSG export)** · **L1 = GEOX-native (runs on L0 ingested files)** · **L2 = GEOX + hermes witnessed**

---

## 0. Why L1 contracts matter

Per the L0/L1/L2 framework:
- **L0 primitives** (12 attribute families) are computed by external Petrel/DSG and exported as volumes/grids with metadata, then ingested via `geox_register_native_source`
- **L1 detectors** (4 families) are GEOX-native tools that consume L0 inputs
- **L2 classifiers** (2 families + topology axis) are GEOX tools with hermes hooks

This document specifies the L0 contracts (3 examples fully fleshed out + 9 templates). The full L0 catalog must be computed upstream and registered before L1/L2 can run.

---

## 1. Universal L0 contract shape

Every L0 attribute contract has these fields:

```yaml
attribute_id: <kebab-case>
attribute_family: <one of 12 families>
classification: L0_PRIMITIVE
computation_target: EXTERNAL  # Petrel/DSG computes
ingestion_path: geox_register_native_source
provenance_required:
  - polarity
  - processing_flow
  - survey_id
  - crs
  - classification_authority

contrast_definition:
  core_extent: { type: geobody_or_polygon, ref: <input> }
  shell_extent: { type: annular, inner_radius_m: 0, outer_radius_m: <200-500> }
  metric: <difference operator>

inputs:
  - <typed input schema>

outputs:
  volume:
    type: 3d_grid | 2d_map | 1d_curve
    units: <SI or domain>
    sampling: <interval_ms or m>
    grid_ref: <CRS, extent>
  attributes_attached:
    - <key>: <typed value>

failure_modes:
  - condition: <what goes wrong>
    behavior: UNKNOWN  # per canon
    receipt: <failure hash>

verification_tests:
  - name: <test_name>
    given: <input>
    expects: <output>
    tolerance: <value>

consumers: [<list of L1/L2 tools that use this>]
```

---

## 2. Example 1: Variance (coherence family)

```yaml
attribute_id: variance-amplitude
attribute_family: discontinuity
classification: L0_PRIMITIVE
computation_target: EXTERNAL
ingestion_path: geox_register_native_source

provenance_required:
  - polarity
  - processing_flow
  - survey_id
  - crs
  - window_samples_n
  - window_traces_n

contrast_definition:
  core_extent: { type: geobody_or_polygon }
  shell_extent: { type: annular, inner_radius_m: 0, outer_radius_m: 300 }
  metric: variance_difference  # σ²_core - σ²_shell

inputs:
  seismic_volume_ref:
    type: string
    description: "Registered L0 seismic amplitude volume"
  window_samples_n:
    type: integer
    default: 5
    minimum: 3
    maximum: 21
  window_traces_n:
    type: integer
    default: 5
    minimum: 3
    maximum: 21

outputs:
  volume:
    type: 3d_grid
    units: dimensionless  # normalized 0..1
    sampling: same_as_input
    grid_ref: same_as_input
  attributes_attached:
    mean: float
    median: float
    p10_p90_range: float

failure_modes:
  - condition: input_unregistered
    behavior: UNKNOWN
  - condition: window_too_small
    behavior: UNKNOWN
  - condition: polarity_unknown
    behavior: UNKNOWN  # cannot normalize contrast without polarity

verification_tests:
  - name: synthetic_fault_detection
    given: "Vertical fault at inline=500, throw=20ms"
    expects: "Variance peak at fault plane, σ² > 0.5 in core vs σ² < 0.1 in shell"
    tolerance: 0.05

consumers:
  - L1_geobody_detector
  - L2_MIEC_classifier  # uses variance to detect chimney cores
  - L1_fault_extractor
```

---

## 3. Example 2: Most-positive curvature (geometry family)

```yaml
attribute_id: curvature-most-positive
attribute_family: geometry
classification: L0_PRIMITIVE
computation_target: EXTERNAL
ingestion_path: geox_register_native_source

provenance_required:
  - polarity
  - processing_flow
  - survey_id
  - crs
  - smoothing_kernel_m

contrast_definition:
  core_extent: { type: geobody_or_polygon }
  shell_extent: { type: annular, inner_radius_m: 0, outer_radius_m: 400 }
  metric: k_pos_difference  # k_pos_core - k_pos_shell

inputs:
  seismic_volume_ref:
    type: string
  horizon_ref:
    type: string
    description: "Required — curvature is computed along a horizon"
  smoothing_kernel_m:
    type: number
    default: 100
    minimum: 25
    maximum: 500

outputs:
  volume:
    type: 3d_grid  # if horizon is a volume; else 2d_map
    units: 1/m  # inverse meters
    sampling: same_as_input
  attributes_attached:
    k_pos_mean: float
    k_pos_p10: float
    k_pos_p90: float

failure_modes:
  - condition: horizon_not_registered
    behavior: UNKNOWN
  - condition: smoothing_kernel_m_too_large
    behavior: UNKNOWN  # over-smoothing destroys signal
  - condition: horizon_has_discontinuities
    behavior: WARN  # curvature at discontinuity is undefined

verification_tests:
  - name: synthetic_anticline_detection
    given: "Gaussian-shaped anticline, amplitude 50m, wavelength 1000m"
    expects: "k_pos peak at crest, value proportional to amplitude/wavelength²"
    tolerance: 0.1

consumers:
  - L1_fault_extractor  # fault-related curvature anomalies
  - L1_fracture_predictor
  - L2_MIEC_classifier  # crestal graben diagnostic
```

---

## 4. Example 3: Spectral decomposition CWT (frequency family)

```yaml
attribute_id: spectral-cwt-bandpass
attribute_family: frequency
classification: L0_PRIMITIVE
computation_target: EXTERNAL
ingestion_path: geox_register_native_source

provenance_required:
  - polarity
  - processing_flow
  - survey_id
  - crs
  - wavelet_family
  - cwt_scales_n

contrast_definition:
  core_extent: { type: geobody_or_polygon }
  shell_extent: { type: annular, inner_radius_m: 0, outer_radius_m: 300 }
  metric: spectral_amplitude_ratio  # at specific frequency band

inputs:
  seismic_volume_ref:
    type: string
  target_frequency_hz:
    type: number
    description: "Center frequency for CWT bandpass"
    minimum: 5
    maximum: 120
  wavelet_family:
    type: string
    enum: ["morlet", "ricker", "mexican_hat", "dog"]
    default: "morlet"
  cwt_scales_n:
    type: integer
    default: 32
    minimum: 8
    maximum: 128

outputs:
  volume:
    type: 3d_grid
    units: amplitude_units (same as input)
    sampling: same_as_input
  attributes_attached:
    dominant_frequency_hz: float
    spectral_bandwidth_hz: float
    q_factor_estimate: float

failure_modes:
  - condition: target_frequency_above_nyquist
    behavior: UNKNOWN
  - condition: input_bandwidth_too_narrow
    behavior: WARN  # spectral decomposition adds little
  - condition: cwt_scales_n_below_8
    behavior: UNKNOWN  # insufficient frequency resolution

verification_tests:
  - name: thin_bed_tuning
    given: "Layer of thickness = 1/(4*f_target)"
    expects: "Peak spectral amplitude at f_target"
    tolerance: 0.1

consumers:
  - L1_geobody_detector  # thin-bed tuning reveals hidden channels
  - L2_DHI_classifier  # frequency-dependent amplitude anomalies
  - L2_gas_chimney_detector  # low-frequency shadow
```

---

## 5. Templates — remaining 9 L0 contracts

For brevity, full contracts are deferred. The pattern is identical: each declares `attribute_id, attribute_family, classification: L0_PRIMITIVE, provenance_required, contrast_definition, inputs, outputs, failure_modes, verification_tests, consumers`.

| ID | Family | Key inputs | Key outputs | Primary consumers |
|---|---|---|---|---|
| `coherence-eigenstructure` | discontinuity | volume, window_size | coherence ∈ [0,1] | fault extractor, fracture predictor |
| `rms-amplitude` | reflectivity | volume, window_ms | amplitude | DHI classifier, geobody detector |
| `sweetness` | reflectivity | volume | amp/freq ratio | bright-spot classifier |
| `glcm-entropy` | texture | volume, window_size, bin_n | entropy ∈ [0, ln(N)] | facies classifier |
| `dip-azimuth` | geometry | volume | azimuth ∈ [0°,360°] | radial-dip cone detector |
| `radial-dip-cone` | geometry | dip_volume | cone_fit_quality ∈ [0,1] | volcano detector |
| `q-attenuation` | frequency | volume, ref_horizon | Q factor | gas-chimney detector |
| `relative-impedance` | physics | volume, low_freq_model | impedance ∈ ℝ | QI inversion, fluid factor |
| `isochron` | stratigraphic | horizon_top_ref, horizon_base_ref | time_thickness_ms | onlap mapper, mini-basin detector |
| `onlap-detection` | stratigraphic | horizon_ref, paleo_bathymetry_ref | onlap_class ∈ {onlap, downlap, toplap, trunc} | canopy detector |
| `polarity-gate` | polarity | volume, witness_ref | polarity ∈ {SEG_normal, SEG_reverse, European} | All — required first |

Total L0 attributes: **12 families → ~15 specific contracts** (polarity gate is universal prerequisite).

---

## 6. L0 → L1 → L2 handoff pattern

```
L0_Petrel_DSG_compute
        ↓
L0_export (volume/grid + metadata)
        ↓
geox_register_native_source(source_uri=L0_export, classification="L0_VOLUME", ...)
        ↓ (verifies SHA256, classification, authority)
L0 volume available as source_id
        ↓
L1_detector(source_id=L0_ref, contrast_spec={core, shell, metric})
        ↓ (computes L1 output)
L1 output (geobody, cone, trace, onlap_map) available as artifact_ref
        ↓
L2_classifier(artifact_ref=L1_ref) + hermes hooks (claim_validate → counterstory → reality_grounding → handoff_package)
        ↓
L2 classification + sealed claim → human SEAL → trap volume math
```

---

## 7. L0 contrast-shell geometry (per Canon #0)

Every L0 contract **must** declare the contrast shell (core vs 200–500 m annulus). This is the universal rule that prevents the per-pixel classification failure mode (Copilot's PNG annotation failure). Without explicit shell geometry, the contrast is undefined → `behavior: UNKNOWN`.

---

## 8. HOLD gates (L0-specific)

| Gate | Unblock |
|---|---|
| Petrel/DSG export tooling | PETRONAS Path A (GEOX inside PETRONAS) decision |
| Calibration of chaos cut-off, rim/core ratio, shell radius | labelled Morley bodies (Figs. 5–21) on Block H 3D |
| Topology EUREKA validation (D1+D2 = one ridge, D3+D4 = one ridge with crestal graben) | L1 detector run on Morley reference data |

---

## 9. Consumers map (L1/L2 tools that use these L0 contracts)

| L0 attribute | L1 consumers | L2 consumers |
|---|---|---|
| variance | geobody_detector, fault_extractor | MIEC_classifier |
| coherence | fault_extractor, fracture_predictor | MIEC_classifier |
| RMS amplitude | geobody_detector | DHI_classifier |
| sweetness | — | bright_spot_classifier |
| GLCM entropy | facies_detector | — |
| dip + azimuth | radial_dip_cone | volcano_classifier |
| curvature | fault_extractor, fracture_predictor | MIEC_topology (topology × strat axis) |
| spectral CWT | — | DHI_classifier, gas_chimney |
| Q attenuation | — | gas_chimney |
| relative impedance | QI inversion | fluid_factor |
| isochron | mini_basin_detector | canopy_classifier |
| onlap detection | mini_basin_detector | canopy_classifier |
| polarity | ALL | ALL |

---

DITEMPA BUKAN DIBERI ⚒️
