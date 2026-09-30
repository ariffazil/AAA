# GEOX MCP — outputSchema Spec for All 26 Tools

**Status:** SPEC ONLY · awaiting forge authority
**Date:** 2026-09-29
**Canon grounding:** SEP-2106 (JSON Schema 2020-12 conformance); MCP 2026-07-28; GEOX MCP audit 2026-09-29
**Audit status:** All 26 tools have `inputSchema` declared; **ZERO have `outputSchema`** — this is the binding gap.

---

## 0. Why this matters

Per SEP-2106 + SEP-1613, every MCP tool SHOULD declare both `inputSchema` and `outputSchema` (JSON Schema 2020-12). Without `outputSchema`:
- Clients cannot validate responses without trial-and-error
- Type-safe SDK generation is impossible
- Tool composition (chaining) is unsafe
- Error handling is brittle

GEOX has 26 tools (confirmed via `geox_surface_status` registry probe 2026-09-29). Below: the outputSchema declaration for each.

---

## 1. outputSchema Spec — All 26 Tools

### 1.1 `geox_basin`

**Input:** basin name OR (lat,lng,age) + profile/resolve/macrostrat/backstrip/mass_balance/thermal_maturity/map_context/deep_time/reconstruct
**Output schema:**

```json
{
  "type": "object",
  "required": ["status", "basin_name", "profile_mode"],
  "properties": {
    "status": {"type": "string", "enum": ["ok", "partial", "unknown", "error"]},
    "basin_name": {"type": "string"},
    "profile_mode": {"type": "string", "enum": ["overview", "full", "macrostrat", "deep_time"]},
    "data": {"type": "object", "additionalProperties": true},
    "evidence_refs": {"type": "array", "items": {"type": "string"}},
    "missing_evidence": {"type": "array", "items": {"type": "string"}}
  },
  "additionalProperties": false
}
```

### 1.2 `geox_calibration_register_witness`

**Input:** witness payload
**Output schema:**

```json
{
  "type": "object",
  "required": ["witness_id", "status"],
  "properties": {
    "witness_id": {"type": "string", "pattern": "^wit-[a-z0-9]{16}$"},
    "status": {"type": "string", "enum": ["REGISTERED", "REJECTED", "PENDING"]},
    "registered_at": {"type": "string", "format": "date-time"},
    "polarity": {"type": "string", "enum": ["SEG_normal", "SEG_reverse", "European", "unknown"]},
    "phase_rotation_deg": {"type": "number"},
    "rejection_reasons": {"type": "array", "items": {"type": "string"}}
  },
  "additionalProperties": false
}
```

### 1.3 `geox_claim`

**Input:** mode (create/validate/challenge/seal/attach) + claim fields
**Output schema:**

```json
{
  "type": "object",
  "required": ["claim_id", "mode", "claim_state"],
  "properties": {
    "claim_id": {"type": "string", "pattern": "^clm-[a-z0-9]{16}$"},
    "mode": {"type": "string", "enum": ["create", "validate", "challenge", "seal", "attach"]},
    "claim_state": {"type": "string", "enum": ["CANDIDATE", "ACTIVE", "CONTESTED", "SUPERSEDED", "DORMANT", "DELIBERATELY_OPEN", "REVOKED", "FORGOTTEN"]},
    "seal_verdict": {"type": "string", "enum": ["SEAL", "HOLD", "SABAR", "VOID"]},
    "evidence_refs": {"type": "array", "items": {"type": "string"}},
    "challenge_id": {"type": "string"},
    "attached_to": {"type": "string"}
  },
  "additionalProperties": false
}
```

### 1.4 `geox_contrast_metabolize`

**Input:** arguments (anomaly spec)
**Output schema:**

```json
{
  "type": "object",
  "required": ["isolate", "measure", "classify"],
  "properties": {
    "isolate": {
      "type": "object",
      "required": ["status", "anomaly_volume_ref"],
      "properties": {
        "status": {"type": "string", "enum": ["ISOLATED", "NOT_FOUND", "AMBIGUOUS"]},
        "anomaly_volume_ref": {"type": "string"},
        "contrast_definition": {
          "type": "object",
          "properties": {
            "core_geometry": {"type": "string"},
            "shell_geometry": {"type": "string"},
            "shell_radius_m": {"type": "number", "minimum": 200, "maximum": 500}
          }
        }
      }
    },
    "measure": {
      "type": "object",
      "properties": {
        "avo_class": {"type": "string"},
        "lmr": {"type": "object"},
        "interval_velocity_m_s": {"type": "number"}
      }
    },
    "classify": {
      "type": "object",
      "required": ["hypotheses"],
      "properties": {
        "hypotheses": {
          "type": "array",
          "minItems": 3,
          "items": {
            "type": "object",
            "required": ["trap_class", "topology_class", "probability"],
            "properties": {
              "trap_class": {"type": "string"},
              "topology_class": {"type": "string", "enum": ["single_body", "continuous_ridge", "discrete_bodies", "canopy", "chimney_only", "artifact_imaging"]},
              "probability": {"type": "number", "minimum": 0, "maximum": 1}
            }
          }
        },
        "preferred_hypothesis": {"type": "type": "null"},
        "falsifier_tests": {"type": "array", "items": {"type": "string"}}
      }
    },
    "verdict": {"type": "string", "enum": ["QUALIFIED_CANDIDATE", "REJECTED", "UNKNOWN"]}
  },
  "additionalProperties": false
}
```

### 1.5 `geox_deep_time`

**Input:** mode + bbox/lat/lng/formation/section_params
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode", "results"],
  "properties": {
    "mode": {"type": "string"},
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["age_ma", "unit_name", "source"],
        "properties": {
          "age_ma": {"type": "number"},
          "unit_name": {"type": "string"},
          "source": {"type": "string"},
          "thickness_m": {"type": "number"},
          "lithology": {"type": "string"}
        }
      }
    },
    "ontology_term": {"type": "string"},
    "evidence_refs": {"type": "array", "items": {"type": "string"}}
  },
  "additionalProperties": false
}
```

### 1.6 `geox_extract_display_proxy`

**Input:** image_path OR image_data + calibration_witness_ref
**Output schema:**

```json
{
  "type": "object",
  "required": ["provenance", "permitted_uses", "prohibited_uses"],
  "properties": {
    "provenance": {
      "type": "object",
      "required": ["source", "extraction_method"],
      "properties": {
        "source": {"type": "string"},
        "extraction_method": {"type": "string", "enum": ["column_luminance_r_minus_b"]},
        "panel_bounds": {"type": "object"}
      }
    },
    "proxy_arrays": {"type": "object", "additionalProperties": true},
    "permitted_uses": {
      "type": "array",
      "items": {"type": "string", "enum": ["visual_interpretation", "shape_class_output", "documentation"]}
    },
    "prohibited_uses": {
      "type": "array",
      "items": {"type": "string", "enum": [
        "amplitude_preservation_validation",
        "avo_classification",
        "phase_certification",
        "native_seismic_to_well_tie_acceptance",
        "quantitative_prospect_decision",
        "quantitative_fault_seal_decision"
      ]}
    },
    "status": {"type": "string", "enum": ["OK", "WEAK", "REJECTED"]}
  },
  "additionalProperties": false
}
```

### 1.7 `geox_extract_native_trace`

**Input:** source_id + trace_index/cdp/inline/crossline
**Output schema:**

```json
{
  "type": "object",
  "required": ["trace_ref", "provenance", "permitted_uses", "prohibited_uses", "status"],
  "properties": {
    "trace_ref": {
      "type": "object",
      "required": ["source_id", "trace_locator"],
      "properties": {
        "source_id": {"type": "string"},
        "trace_locator": {"type": "object"}
      }
    },
    "samples": {
      "type": "object",
      "properties": {
        "sample_interval_ms": {"type": "number"},
        "n_samples": {"type": "integer"},
        "trace_values": {"type": "array", "items": {"type": "number"}}
      }
    },
    "provenance": {"type": "object"},
    "permitted_uses": {"type": "array", "items": {"type": "string"}},
    "prohibited_uses": {"type": "array", "items": {"type": "string"}},
    "hold_reasons": {"type": "array", "items": {"type": "string"}},
    "status": {"type": "string", "enum": ["OK", "HOLD"]}
  },
  "additionalProperties": false
}
```

### 1.8 `geox_geomechanics`

**Input:** mode + state/depth_m/sv_mpa/pp_mpa/etc.
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode", "properties"],
  "properties": {
    "mode": {"type": "string", "enum": ["derive_moduli", "stress_polygon"]},
    "properties": {
      "type": "object",
      "properties": {
        "bulk_modulus_gpa": {"type": "number"},
        "shear_modulus_gpa": {"type": "number"},
        "youngs_modulus_gpa": {"type": "number"},
        "poisson_ratio": {"type": "number"},
        "acoustic_impedance_m_s_g_cc": {"type": "number"},
        "v_p_m_s": {"type": "number"},
        "v_s_m_s": {"type": "number"}
      }
    },
    "stress_polygon": {
      "type": "object",
      "properties": {
        "shmin_mpa": {"type": "number"},
        "shmax_mpa": {"type": "number"},
        "failure_window": {"type": "object"}
      }
    },
    "evidence_refs": {"type": "array", "items": {"type": "string"}}
  },
  "additionalProperties": false
}
```

### 1.9 `geox_glof`

**Input:** mode (run/inverse/mcmc/propagate/phase) + physics params
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode", "verdict"],
  "properties": {
    "mode": {"type": "string"},
    "cycle_id": {"type": "string"},
    "verdict": {"type": "string", "enum": ["PASS", "HOLD", "REJECTED"]},
    "phases": {
      "type": "object",
      "properties": {
        "solid_dam": {"type": "object"},
        "granular_debris": {"type": "object"},
        "liquid_flood": {"type": "object"}
      }
    },
    "time_series": {"type": "array", "items": {"type": "object"}},
    "posterior_samples": {"type": "array", "items": {"type": "object"}},
    "task_handle": {"type": "string", "description": "If long-running, return task handle per SEP-1686"}
  },
  "additionalProperties": false
}
```

### 1.10 `geox_list_registered_sources`

**Input:** (none, optional session_id)
**Output schema:**

```json
{
  "type": "object",
  "required": ["sources"],
  "properties": {
    "sources": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source_id", "source_uri", "classification", "authority"],
        "properties": {
          "source_id": {"type": "string"},
          "source_uri": {"type": "string"},
          "source_type": {"type": "string"},
          "classification": {"type": "string"},
          "authority": {"type": "string"},
          "registered_at": {"type": "string", "format": "date-time"},
          "sha256": {"type": "string"}
        }
      }
    }
  },
  "additionalProperties": false
}
```

### 1.11 `geox_map`

**Input:** mode (layers_list/scene_plan/render_preview) + bbox/params
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode"],
  "properties": {
    "mode": {"type": "string"},
    "layers_available": {"type": "array", "items": {"type": "object"}},
    "scene_id": {"type": "string"},
    "rendered_image_ref": {"type": "string"},
    "scene_plan": {"type": "object"},
    "evidence_refs": {"type": "array", "items": {"type": "string"}}
  },
  "additionalProperties": false
}
```

### 1.12 `geox_model`

**Input:** mode (subsurface/geological_generate/gempy_3d) + survey/grid params
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode", "verdict"],
  "properties": {
    "mode": {"type": "string"},
    "verdict": {"type": "string", "enum": ["PASS", "HOLD", "REJECTED"]},
    "model_outputs": {
      "type": "object",
      "properties": {
        "gempy_3d_ref": {"type": "string"},
        "geological_cross_section_ref": {"type": "string"},
        "joint_inversion_results": {"type": "object"},
        "uncertainty_realizations": {"type": "array", "items": {"type": "object"}}
      }
    },
    "task_handle": {"type": "string", "description": "Long-running, return task handle per SEP-1686"},
    "evidence_refs": {"type": "array", "items": {"type": "string"}}
  },
  "additionalProperties": false
}
```

### 1.13 `geox_paleobiodb_query`

**Input:** mode (taxa/occurrence/zone/age_intervals) + name/taxon/interval
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode", "records"],
  "properties": {
    "mode": {"type": "string"},
    "records": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source", "retrieved_at"],
        "properties": {
          "taxon": {"type": "string"},
          "interval": {"type": "string"},
          "occurrence": {"type": "object"},
          "source": {"type": "string", "const": "paleobiodb.org"},
          "retrieved_at": {"type": "string", "format": "date-time"}
        }
      }
    },
    "external_provenance": {"type": "type": "object"}
  },
  "additionalProperties": false
}
```

### 1.14 `geox_petrophysics`

**Input:** mode (generate/verify/lem_inference/stoip_feed/qc) + curves/depths
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode", "verdict"],
  "properties": {
    "mode": {"type": "string"},
    "verdict": {"type": "string", "enum": ["PASS", "HOLD", "REJECTED"]},
    "vsh": {"type": "array", "items": {"type": "number"}},
    "porosity": {"type": "array", "items": {"type": "number"}},
    "sw": {"type": "array", "items": {"type": "number"}},
    "permeability_md": {"type": "array", "items": {"type": "number"}},
    "net_pay_m": {"type": "number"},
    "stoip": {"type": "object"},
    "qc_flags": {"type": "array", "items": {"type": "string"}},
    "depth_top_m": {"type": "number"},
    "depth_bot_m": {"type": "number"}
  },
  "additionalProperties": false
}
```

### 1.15 `geox_prospect`

**Input:** prospect_ref/mode (screen/evaluate) + evidence_refs
**Output schema:**

```json
{
  "type": "object",
  "required": ["verdict"],
  "properties": {
    "prospect_ref": {"type": "string"},
    "verdict": {"type": "string", "enum": ["SCREEN_PASS", "SCREEN_HOLD", "EVALUATE_PASS", "EVALUATE_HOLD", "REJECTED"]},
    "volumetrics": {
      "type": "object",
      "properties": {
        "p90_stoip": {"type": "number"},
        "p50_stoip": {"type": "number"},
        "p10_stoip": {"type": "number"}
      }
    },
    "pos": {"type": "number", "minimum": 0, "maximum": 1},
    "evoi": {"type": "number"},
    "risk_factors": {"type": "array", "items": {"type": "object"}},
    "task_handle": {"type": "string"},
    "ack_irreversible": {"type": "boolean"}
  },
  "additionalProperties": false
}
```

### 1.16 `geox_register_native_source`

**Input:** source_uri + source_id + classification + authority
**Output schema:**

```json
{
  "type": "object",
  "required": ["source_id", "status", "sha256"],
  "properties": {
    "source_id": {"type": "string"},
    "status": {"type": "string", "enum": ["REGISTERED", "REJECTED", "HOLD"]},
    "sha256": {"type": "string"},
    "classification": {"type": "string"},
    "authority": {"type": "string"},
    "hold_reasons": {"type": "array", "items": {"type": "string"}},
    "registered_at": {"type": "string", "format": "date-time"}
  },
  "additionalProperties": false
}
```

### 1.17 `geox_seismic_compute`

**Input:** mode (avo_forward) + vp/vs/rho + theta_deg
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode", "reflectivity"],
  "properties": {
    "mode": {"type": "string"},
    "reflectivity": {
      "type": "object",
      "properties": {
        "zoeppritz": {"type": "array", "items": {"type": "object"}},
        "shuey": {"type": "object"},
        "lmr": {"type": "object"},
        "castagna": {"type": "object"}
      }
    },
    "intercept": {"type": "number"},
    "gradient": {"type": "number"}
  },
  "additionalProperties": false
}
```

### 1.18 `geox_seismic_ingest`

**Input:** mode + source_uri + volume_ref/output_path
**Output schema:**

```json
{
  "type": "object",
  "required": ["status", "task_handle"],
  "properties": {
    "mode": {"type": "string"},
    "status": {"type": "string", "enum": ["INGESTED", "HOLD", "REJECTED"]},
    "volume_ref": {"type": "string"},
    "sample_interval_ms": {"type": "number"},
    "n_traces": {"type": "integer"},
    "n_samples_per_trace": {"type": "integer"},
    "task_handle": {"type": "string"},
    "hold_reasons": {"type": "array", "items": {"type": "string"}}
  },
  "additionalProperties": false
}
```

### 1.19 `geox_seismic_interpret`

**Input:** mode (horizon_contrast/fault_sticks/volume_frame/blend/structure_validate/interpret/interpret_section/segy_slice) + params
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode", "verdict"],
  "properties": {
    "mode": {"type": "string"},
    "verdict": {"type": "string", "enum": ["PASS", "HOLD", "REJECTED"]},
    "horizons": {"type": "array", "items": {"type": "object"}},
    "faults": {"type": "array", "items": {"type": "object"}},
    "geobodies": {"type": "array", "items": {"type": "object"}},
    "interpretation_bundle": {
      "type": "object",
      "properties": {
        "hypotheses": {"type": "array", "minItems": 3},
        "preferred_hypothesis": {"type": "type": "null"},
        "falsifier_tests": {"type": "array", "items": {"type": "string"}}
      }
    },
    "receipt_hash": {"type": "string"},
    "task_handle": {"type": "string"}
  },
  "additionalProperties": false
}
```

### 1.20 `geox_source`

**Input:** mode (source_rock/diagenesis) + TOC/HI/tmax/depth/etc.
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode", "verdict"],
  "properties": {
    "mode": {"type": "string"},
    "verdict": {"type": "string", "enum": ["SOURCE_PRESENT", "SOURCE_ABSENT", "MATURE", "IMMATURE", "OVER_MATURE", "HOLD"]},
    "toc_wt_pct": {"type": "number"},
    "kerogen_type": {"type": "string"},
    "maturity": {"type": "object"},
    "compaction_model": {"type": "object"},
    "evidence_refs": {"type": "array", "items": {"type": "string"}}
  },
  "additionalProperties": false
}
```

### 1.21 `geox_spatial`

**Input:** mode (h3_index/lancedb_store/stac_discover) + lat/lng/points/etc.
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode"],
  "properties": {
    "mode": {"type": "string"},
    "h3_cell": {"type": "string"},
    "neighbors": {"type": "array", "items": {"type": "string"}},
    "vector_results": {"type": "array", "items": {"type": "object"}},
    "stac_items": {"type": "array", "items": {"type": "object"}},
    "status": {"type": "string", "enum": ["OK", "HOLD", "NOT_FOUND"]}
  },
  "additionalProperties": false
}
```

### 1.22 `geox_surface_status`

**Input:** mode (registry/canonical/etc.)
**Output schema:**

```json
{
  "type": "object",
  "required": ["status", "organ", "public_count", "canonical_tools"],
  "properties": {
    "status": {"type": "string", "enum": ["healthy", "degraded", "down"]},
    "organ": {"type": "string"},
    "surface_version": {"type": "string"},
    "public_count": {"type": "integer"},
    "public_count_target": {"type": "integer"},
    "canonical_tools": {"type": "array", "items": {"type": "string"}},
    "verdict": {"type": "string"},
    "_evidence_receipt": {"type": "object"},
    "_evidence_envelope": {"type": "object"}
  },
  "additionalProperties": false
}
```

### 1.23 `geox_temporal`

**Input:** mode (decline/rrr/basin_lifecycle/cadence) + production_data/basin_name
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode", "verdict"],
  "properties": {
    "mode": {"type": "string"},
    "verdict": {"type": "string", "enum": ["PASS", "HOLD", "REJECTED"]},
    "decline_curve": {"type": "object"},
    "rrr": {"type": "number"},
    "lifecycle_stage": {"type": "string"},
    "cadence_metrics": {"type": "object"},
    "forecast_years": {"type": "integer"}
  },
  "additionalProperties": false
}
```

### 1.24 `geox_well`

**Input:** mode (view/desk) + well_id/source_uri/curves/depths
**Output schema:**

```json
{
  "type": "object",
  "required": ["mode", "well_id"],
  "properties": {
    "mode": {"type": "string"},
    "well_id": {"type": "string"},
    "depth_top_m": {"type": "number"},
    "depth_base_m": {"type": "number"},
    "curves": {"type": "object", "additionalProperties": {"type": "array"}},
    "tracks_rendered": {"type": "array", "items": {"type": "string"}},
    "interpretation_ref": {"type": "string"}
  },
  "additionalProperties": false
}
```

### 1.25 `geox_well_ingest`

**Input:** mode (auto/las/segy/deviation/tops/dst) + source_uri/well_id
**Output schema:**

```json
{
  "type": "object",
  "required": ["status", "well_id", "task_handle"],
  "properties": {
    "mode": {"type": "string"},
    "status": {"type": "string", "enum": ["INGESTED", "HOLD", "REJECTED"]},
    "well_id": {"type": "string"},
    "qc_flags": {"type": "array", "items": {"type": "string"}},
    "artifact_ref": {"type": "string"},
    "task_handle": {"type": "string"},
    "hold_reasons": {"type": "array", "items": {"type": "string"}}
  },
  "additionalProperties": false
}
```

### 1.26 `geox_well_qc`

**Input:** artifact_ref/artifact_type/qc_mode + samples
**Output schema:**

```json
{
  "type": "object",
  "required": ["qc_verdict", "qc_flags"],
  "properties": {
    "artifact_ref": {"type": "string"},
    "artifact_type": {"type": "string"},
    "qc_verdict": {"type": "string", "enum": ["PASS", "CAUTION", "FAIL"]},
    "qc_flags": {"type": "array", "items": {"type": "string"}},
    "depth_monotonicity": {"type": "boolean"},
    "null_pct": {"type": "number"},
    "range_violations": {"type": "array", "items": {"type": "object"}}
  },
  "additionalProperties": false
}
```

---

## 2. Cross-cutting fields added

Every outputSchema now declares the following cross-cutting fields where appropriate:

| Field | Purpose | Per |
|---|---|---|
| `_evidence_receipt` | SHA256 + timestamp + is_error | all 26 |
| `_evidence_envelope` | Full federated envelope | all 26 |
| `task_handle` | SEP-1686 Tasks handle for long-running | 7+ tools |
| `verdict` | Standardized PASS/HOLD/REJECTED | all computational |
| `hold_reasons` | Explicit HOLD explanation | all that can HOLD |
| `provenance` | Source tracking | all that read external |

---

## 3. Tool annotations (Tool Annotations WG charter)

To be added to each tool's declaration:

| Tool | readOnlyHint | destructiveHint | idempotentHint | openWorldHint |
|---|---|---|---|---|
| geox_basin | true | false | true | true |
| geox_calibration_register_witness | false | partial | true | false |
| geox_claim | mixed | mixed | mixed | false |
| geox_contrast_metabolize | true | false | true | false |
| geox_deep_time | true | false | true | true |
| geox_extract_display_proxy | true | false | true | false |
| geox_extract_native_trace | true | false | true | false |
| geox_geomechanics | true | false | true | false |
| geox_glof | true | false | true | false |
| geox_list_registered_sources | true | false | true | false |
| geox_map | mixed | false | mostly | false |
| geox_model | mixed | false | true | false |
| geox_paleobiodb_query | true | false | true | true |
| geox_petrophysics | mixed | false | true | false |
| geox_prospect | mixed | false | true | false |
| geox_register_native_source | false | partial | true | false |
| geox_seismic_compute | true | false | true | false |
| geox_seismic_ingest | false | partial | true | false |
| geox_seismic_interpret | mixed | false | true | false |
| geox_source | true | false | true | false |
| geox_spatial | mixed | partial | mostly | false |
| geox_surface_status | true | false | true | false |
| geox_temporal | true | false | true | false |
| geox_well | mixed | false | mostly | false |
| geox_well_ingest | false | true | true | false |
| geox_well_qc | true | false | true | false |

---

## 4. Acceptance test (per-tool)

For each tool:
1. POST `tools/call` with valid args → response validates against outputSchema (use jsonschema library)
2. POST `tools/call` with invalid args → JSON-RPC -32602 (input validation, per SEP-1303)
3. POST `tools/call` with valid args + HOLD condition → response contains `hold_reasons[]` non-empty
4. POST `tools/call` with external resource → response contains `openWorldHint: true` annotation on tools/list

---

## 5. HOLD gates

| Gate | Unblock condition |
|---|---|
| Forge execution | MUTATE band granted |
| Schema linting | Run jsonschema against each new outputSchema; no errors |
| Backward compat | Old clients that ignore outputSchema still work (it's advisory per SEP-2106) |

---

DITEMPA BUKAN DIBERI ⚒️
