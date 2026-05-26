---
name: geox-basin-interpreter
description: Subsurface reasoning for basin screening, petroleum systems analysis, trap/seal/reservoir framing, and evidence-led interpretations. Load when geology, geophysics, or petrophysics tasks appear.
---

# geox-basin-interpreter (Ψ_GEOX Domain Layer)

## Purpose
Subsurface reasoning for basin screening, petroleum systems analysis, trap/seal/reservoir framing, and evidence-led interpretations.

## Use When
1. Screening basins or prospects for petroleum systems presence (source rock, migration pathway, reservoir, trap, and seal).
2. Interpretations are requested based on seismic sections, structural maps, or well-log correlations.
3. Conducting subsurface risk assessments (e.g. calculation of Geological Chance of Success - GCoS).
4. Verifying subsurface candidate validity against structural or stratigraphic constraints.
5. Ingesting or synthesizing geologic domain lit reviews, papers, or basin reports.

## Do Not Use When
1. The task is purely focused on petrophysical QC, well-log curve normalization, or curve sanity checks (use `geox-well-log-audit` instead).
2. The task requires calculating specific fluid-flow dynamic parameters inside well casings (use standard production engineering tools).
3. The task requires writing standard system scripts or web designs (use generic engineering or design skills instead).

## Inputs
*   **Seismic/Map Data:** Grid coordinates, structural mapping files, or interpretive cross-sections.
*   **Well Context:** Core descriptions, formation picks, or petrophysical summaries.
*   **Geochemical Context:** Total Organic Carbon (TOC) levels, thermal maturity data (Ro%), or pressure profiles.

## The Five-Box GCoS Evaluation Template

Every basin/prospect screening report must output the following five-box risk matrix:

```markdown
### 1. Geological Chance of Success (GCoS) Matrix

| Element | Probability (Pg) | Primary Evidence | Key Risks & Contradictions |
| :--- | :---: | :--- | :--- |
| **Source (Charge)** | `0.0 - 1.0` | e.g. TOC/Ro% measurements from analogs | e.g. Kitchen thermal migration shadow |
| **Reservoir** | `0.0 - 1.0` | e.g. Core porosity, turbidite facies maps | e.g. Deep diagenetic quartz cementation |
| **Trap** | `0.0 - 1.0` | e.g. 3D seismic horizon closure amplitude | e.g. Lateral fault seal leakage risk |
| **Seal** | `0.0 - 1.0` | e.g. Continuous regional shale interval | e.g. Crestal fault breaching |
| **Timing & Migration** | `0.0 - 1.0` | e.g. Basin modeling maturation curves | e.g. Late trap deformation |

**Composite Geological Chance of Success (GCoS):**
`Pg_total = Pg_source × Pg_reservoir × Pg_trap × Pg_seal × Pg_timing`
`Pg_total = [Calculated Value]%` (Apply Humility Band: uncertainty margin of ±0.03 to ±0.05)
```

## Procedure
1.  **Framework Screening:** Map the active geologic basin setting (e.g., extensional rift, passive margin, foreland basin) to set stratigraphic expectations.
2.  **Petroleum Systems Element Audit:** Evaluate each of the 5 crucial elements using the **Five-Box GCoS Evaluation Template**.
3.  **STDP Geologic Evidential Loop:** Verify all claims. Distinguish *directly measured evidence* (e.g., core plugs, DST tests) from *indirect indicators* (e.g. seismic amplitude anomalies) and *speculative inference*.
4.  **GCoS Calculation:** Compute probability metrics for each element. Multiply the elements to obtain the total Chance of Success (Pg_total).
5.  **Evidence Matrix Serialization:** Document all structural contradictions or faults mapped across the basin.

## Postconditions
1.  All geologic inferences are explicitly tagged with their data source and confidence level.
2.  The resulting basin interpretation maps exact GCoS risk elements with empirical justification.
3.  All trap/seal/reservoir maps comply with physical compaction and pressure gradients.

## Failure Modes & Escalation
*   **Data Scarcity:** No well or seismic control exists for the screened block. *Action:* Rely strictly on analog basins. Tag all findings as *"Estimate Only - Analog Grounded"* and set GCoS risk margins to conservative bounds.
*   **Structural Discontinuity:** Mapped faults show contradictory sealing history. *Action:* Flag the seal parameter as a critical system hazard, degrade interpretation class to `CAUTION`, and escalate for expert validation.

## Telemetry per Run
```json
{
  "skill_name": "geox-basin-interpreter",
  "version": "1.1.0",
  "trigger_phrase": "{{trigger_phrase}}",
  "selected_reason": "{{selected_reason}}",
  "latency_ms": 0,
  "token_in": 0,
  "token_out": 0,
  "commands_run": 0,
  "artifacts_written": 1,
  "postcondition_pass": false,
  "human_approval_required": false,
  "hold_code": "{{hold_code}}"
}
```

## Recursive Scorecard
*   **Activation Precision:** [0.0 - 1.0] (Target: >0.90)
*   **Task Completion Rate:** [0.0 - 1.0] (Target: >0.95)
*   **Rollback Safety:** [0.0 - 1.0] (Target: 1.00)
*   **Context Efficiency:** [0.0 - 1.0] (Target: >0.90)
*   **Doc Freshness:** [0.0 - 1.0] (Target: 1.00)
*   **Cross-Skill Collision Rate:** [0.0 - 1.0] (Target: <0.02)
*   **Human Trust Score:** [0.0 - 1.0] (Target: >0.98)
