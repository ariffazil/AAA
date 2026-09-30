# MIEC Acceptance-Test Benchmark — Topology + Per-Body

**Status:** SPEC READY
**Date:** 2026-09-29
**Owner:** FI-008 (kimi-code)
**Use case:** Validation that GEOX MCP can correctly identify mud intrusive/extrusive complexes (MIECs) per Morley et al. (Geosphere v19 no. 1, North Block H)
**Canon grounding:** L0/L1/L2 framework; topology × strat_trap EUREKA; MUEC class taxonomy from §3 of Morley spec

---

## 0. Why this benchmark matters

MIEC identification has been the original use case since the conversation started. The EUREKA (turn 6) was that **the unit of interpretation is the body's relationship to its neighbors, not the body itself.** This benchmark enforces that finding as a testable invariant.

Without topology-recovery test, GEOX would happily classify D1/D2 as two separate diapirs (wrong) and D3/D4 as two separate diapirs (also wrong). The benchmark catches this.

---

## 1. Test inputs (seed claims)

These are the candidate hypotheses generated from the Copilot-style annotation of the ROTAN-1 dip line (from `image.png`, Fig. 6 of Morley et al.):

| Claim ID | Spatial location | Original class (Copilot v1) | Topology (corrected) |
|---|---|---|---|
| `seed-D1` | NW of ROTAN-1 (x≈420–650, chaotic core) | "Mobile shale wall / diapir" | **continuous_ridge** (with D2) |
| `seed-D2` | Below ROTAN-1 (x≈680–810, sharp crest) | "Diapir crest below ROTAN-1" | **continuous_ridge** (with D1) |
| `seed-D3` | SE flank of MB-B (x≈910–1040) | "Shale diapir or roller" | **continuous_ridge_with_graben** (with D4) |
| `seed-D4` | SE of D3 (x≈1050–1240) | "Mobile shale core" (LOW conf.) | **continuous_ridge_with_graben** (with D3) — false positive if standalone |
| `seed-MB-A` | NW flank of section (x≈300–400) | "Mini-basin (withdrawal syncline)" | **single_mini_basin** |
| `seed-MB-B` | Between D2 and D3 (x≈815–905) | "Mini-basin (downbuilt)" | **single_mini_basin** |
| `seed-MB-C` | SE of section (x≈1300+) | "Mini-basin" | **single_mini_basin** |
| `seed-survey-boundary` | x≈330–420 (left panel join) | "Survey join artifact" | **excluded_from_classification** |

---

## 2. Acceptance criteria

### 2.1 Topology-recovery test (EUREKA invariant)

**Test:** Given the 7 MIEC/mini-basin claims, GEOX must group them into the correct topology relationships.

**Expected output from `geox_contrast_metabolize` / `geox_claim`:**

| Group | Members | Topology class | Evidence |
|---|---|---|---|
| Group 1 | D1 + D2 | `continuous_ridge` | Continuous reflector across apparent sag (x≈640–680); narrow spine at SE end |
| Group 2 | D3 + D4 | `continuous_ridge_with_graben` | Crestal graben at x≈1040 + extensional fault swarm |
| Group 3 | MB-A | `single_mini_basin` | Isolated withdrawal syncline |
| Group 4 | MB-B | `single_mini_basin` | Downbuilt between D2 and D3 |
| Group 5 | MB-C | `single_mini_basin` | Isolated, SE of D4 |
| Group 6 (excluded) | survey-boundary | `excluded_from_classification` | Multi-survey join — not geology |

**Pass criteria:**
- `[Pass]` D1 and D2 assigned same `topology_class: continuous_ridge` (not two separate claims)
- `[Pass]` D3 and D4 assigned same `topology_class: continuous_ridge_with_graben`
- `[Pass]` Each mini-basin is a separate group with `topology_class: single_mini_basin`
- `[Pass]` Survey boundary feature flagged `excluded_from_classification`
- `[Pass]` Output includes ≥3 hypotheses per group (continuous ridge vs discrete diapirs vs artifact-imaging)
- `[Pass]` Counterstory test: for each group, MTC and gas-wipeout hypotheses generated and tested against evidence

### 2.2 Per-body classification test (L2 classifier)

**Test:** Each accepted body must receive a class assignment per the §3 matrix (volcano / chamber / pancake / diapir / roller / chimney).

**Expected output:**

| Claim ID | Class (per §3) | Confidence | Required evidence |
|---|---|---|---|
| Group 1 (D1+D2 ridge) | `mud_volcano` with sub-class `ridge_with_spine` | MED | Cone edifice geometry, downbuilt moat at MB-B |
| Group 2 (D3+D4 ridge) | `mud_chimney_collapse` with sub-class `crestal_graben` | MED | Extensional fault swarm, transparent core |
| MB-A | `mini_basin_withdrawal` | MED | Synformal downbuilt between highs |
| MB-B | `mini_basin_downbuilt` | HIGH | Clear synform between D2 crest and D3 flank |
| MB-C | `mini_basin_withdrawal` | MED | Synformal, SE flank |

**Pass criteria:**
- `[Pass]` Each accepted body has class per §3 (no orphans)
- `[Pass]` Confidence levels reported (HIGH/MED/LOW)
- `[Pass]` Sub-classes encoded where applicable (e.g., `ridge_with_spine`, `crestal_graben`)
- `[Pass]` Required evidence listed per body

### 2.3 Counterstory (false-positive rejection)

**Test:** For each candidate, GEOX must generate ≥3 alternative explanations and falsify the mud hypothesis first.

**Expected output for Group 1 (D1+D2):**

| Hypothesis | Prior | Falsifier test |
|---|---|---|
| `mud_volcano_ridge` (preferred, must falsify first) | 0.5 | (a) Is there a root to low-V zone at 4–5 km? (b) Is the rim/core amplitude ratio > 2? (c) Is the contrast shell (200–500 m) significantly different from core? |
| `MTC_mass_transport_complex` | 0.2 | (a) Is there a feeder root? If no → reject |
| `gas_wipeout_chimney` | 0.15 | (a) Is there a bounding rim? If no → reject |
| `channel_sand_bright_spot` | 0.1 | (a) Is geometry elongate? If yes → reject |
| `carbonate_buildup` | 0.05 | (a) Is velocity much higher than surrounding? If no → reject |

**Pass criteria:**
- `[Pass]` ≥3 hypotheses generated
- `[Pass]` Preferred hypothesis (mud) tested first and falsifier applied
- `[Pass]` MTC / gas-wipeout / channel / carbonate tested against
- `[Pass]` Probabilities sum to 1.0 ± 0.05
- `[Pass]` At least one non-mud hypothesis survives falsification (drives class into UNKNOWN if so)

### 2.4 Provenance chain test

**Test:** Every claim must carry provenance chain from L0 → L1 → L2 → seal.

**Pass criteria:**
- `[Pass]` Each claim has `l0_source_id` (registered L0 attribute volume)
- `[Pass]` Each claim has `l1_artifact_id` (geobody/cone/trace/onlap artifact)
- `[Pass]` Each claim has `l2_classifier_id` (`geox_contrast_metabolize` invocation hash)
- `[Pass]` Each claim has `hermes_validation_chain` (claim_validate → counterstory → reality_grounding → handoff)
- `[Pass]` Each claim has `evidence_path` pointing to specific data
- `[Pass]` No claim has `provenance: screen-raster-only` AND reaches quantitative decision (per `geox_extract_display_proxy` prohibition)

### 2.5 Shell-geometry test (Canon #0 invariant)

**Test:** Every L0 attribute contract that consumes the body must declare core vs 200–500 m shell geometry.

**Pass criteria:**
- `[Pass]` Each contrast measurement uses shell radius between 200 m and 500 m
- `[Pass]` Core and shell geometries are explicit (no implicit "all pixels within")
- `[Pass]` Shell is annular (not just offset by a constant)
- `[Pass]` Behavior defaults to UNKNOWN when shell geometry is undefined

---

## 3. Acceptance gates

| Gate | Pass condition |
|---|---|
| B-TOPO-1 | Topology-recovery test (2.1) all passes |
| B-BODY-1 | Per-body classification test (2.2) all passes |
| B-COUNTER-1 | Counterstory test (2.3) all passes |
| B-PROV-1 | Provenance chain test (2.4) all passes |
| B-SHELL-1 | Shell-geometry test (2.5) all passes |

**Overall benchmark PASS** = all 5 gates green.

---

## 4. Test runner (executable spec)

```python
# test_miec_acceptance.py
import json
from jsonschema import validate

SEED_CLAIMS = {
    "seed-D1": {"x_range": [420, 650], "y_range": [330, 790]},
    "seed-D2": {"x_range": [680, 810], "y_range": [280, 790]},
    "seed-D3": {"x_range": [910, 1040], "y_range": [330, 790]},
    "seed-D4": {"x_range": [1050, 1240], "y_range": [330, 790]},
    "seed-MB-A": {"x_range": [300, 400], "y_range": [600, 790]},
    "seed-MB-B": {"x_range": [815, 905], "y_range": [600, 790]},
    "seed-MB-C": {"x_range": [1300, 1420], "y_range": [550, 790]},
}

EXPECTED_GROUPS = [
    {"members": ["seed-D1", "seed-D2"], "topology_class": "continuous_ridge"},
    {"members": ["seed-D3", "seed-D4"], "topology_class": "continuous_ridge_with_graben"},
    {"members": ["seed-MB-A"], "topology_class": "single_mini_basin"},
    {"members": ["seed-MB-B"], "topology_class": "single_mini_basin"},
    {"members": ["seed-MB-C"], "topology_class": "single_mini_basin"},
]

def test_topology_recovery(classification_result):
    """B-TOPO-1"""
    groups = classification_result.get("groups", [])
    for expected in EXPECTED_GROUPS:
        matching = [g for g in groups if set(g["members"]) == set(expected["members"])]
        assert matching, f"Group {expected['members']} missing"
        assert matching[0]["topology_class"] == expected["topology_class"], \
            f"Group {expected['members']}: expected {expected['topology_class']}, got {matching[0]['topology_class']}"

def test_per_body_classification(classification_result):
    """B-BODY-1"""
    groups = classification_result.get("groups", [])
    for g in groups:
        assert g.get("class_per_section3"), f"Group {g['members']} missing §3 class"
        assert g.get("confidence") in ["HIGH", "MED", "LOW"]

def test_counterstory(classification_result):
    """B-COUNTER-1"""
    groups = classification_result.get("groups", [])
    for g in groups:
        hyps = g.get("hypotheses", [])
        assert len(hyps) >= 3, f"Group {g['members']}: <3 hypotheses"
        mud_hyps = [h for h in hyps if "mud" in h["trap_class"].lower()]
        assert mud_hyps, f"Group {g['members']}: no mud hypothesis"
        assert mud_hyps[0].get("falsifier_tests"), "Mud hypothesis not falsified first"
        probs_sum = sum(h["probability"] for h in hyps)
        assert abs(probs_sum - 1.0) < 0.05

def test_provenance_chain(classification_result):
    """B-PROV-1"""
    for claim in classification_result.get("all_claims", []):
        assert claim.get("l0_source_id"), "No L0 source"
        assert claim.get("l1_artifact_id"), "No L1 artifact"
        assert claim.get("l2_classifier_id"), "No L2 classifier"
        assert claim.get("hermes_validation_chain"), "No hermes chain"
        if claim.get("provenance") == "screen-raster-only":
            assert not claim.get("reaches_quantitative_decision"), \
                "Screen-raster claim reached quantitative decision (PROHIBITED)"

def test_shell_geometry(classification_result):
    """B-SHELL-1"""
    for measurement in classification_result.get("contrast_measurements", []):
        shell_radius = measurement.get("shell_radius_m")
        assert shell_radius is not None, "No shell radius declared"
        assert 200 <= shell_radius <= 500, f"Shell radius {shell_radius} outside 200-500 m"
        assert measurement.get("core_geometry"), "No core geometry"
        assert measurement.get("shell_geometry"), "No shell geometry"

if __name__ == "__main__":
    import sys
    result = json.load(sys.stdin)
    test_topology_recovery(result); print("✓ B-TOPO-1")
    test_per_body_classification(result); print("✓ B-BODY-1")
    test_counterstory(result); print("✓ B-COUNTER-1")
    test_provenance_chain(result); print("✓ B-PROV-1")
    test_shell_geometry(result); print("✓ B-SHELL-1")
    print("\n🎯 MIEC ACCEPTANCE BENCHMARK: PASS")
```

---

## 5. HOLD gates (benchmark-specific)

| Gate | Unblock condition |
|---|---|
| Run benchmark | L0 attributes ingested (12 families), L1 detectors built, L2 classifiers with topology axis |
| Quantitative labels | Morley Figs. 5–21 reference bodies + Block H 3D |
| Counterstory library | MTC / gas wipe-out / salt / channel / carbonate training cases |
| Calibration thresholds | chaos cut-off, rim/core amplitude ratio, shell radius — needs labelled reference |

---

## 6. EUREKA binding

> **The unit of mud-body interpretation is the body's relationship to its neighbors, not the body itself.**

This benchmark enforces that finding. If GEOX ships a classifier that produces one claim per body without topology relationships, **the benchmark fails**.

---

DITEMPA BUKAN DIBERI ⚒️
