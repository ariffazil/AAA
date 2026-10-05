# UNKNOWN_ATLAS v1 — Classified-Uncertainty Surveys Across the Federation

**Generated:** 2026-10-05 · 333-AGI (session SEAL-121c33c37b4a4436) · Directive: F13 Arif, TASK::CLASSIFIED_UNKNOWN_AUDIT
**Method:** tool-schema SOT (live MCP surfaces) + source greps + today's operational receipts. Read-only; no schema changed.

## Finding (one line)
Classified-UNKNOWN **already exists in ≥6 distributed surfaces** — but is **absent from the two most load-bearing envelopes** (kernel judge claim_class, arifFlow epistemic_label), where uncertainty collapses into HOLD instead of a first-class classified state.

## Survey

| Surface | Field(s) | Unknown-class states | Notes |
|---|---|---|---|
| **arifOS `arif_judge`** | `claim_class` | **GAP — enum is OBS/DER/INT/SPEC only.** No UNKNOWN class. | Uncertainty is expressible only as verdict HOLD (binary), losing *what kind* of unknown. Verdicts: SEAL/HOLD/SABAR/VOID |
| **arifFlow `flow_ingest`** | `epistemic_label`, `floor_verdict` | **GAP — labels Observation/Derivation/Interpretation/Specification/Seal; verdicts Pass/Caution/Hold/Void.** No Unknown label. | Receipts carry consequence lineage but cannot say "unwitnessed" |
| **CHRON** | `chron_resolve_unverifiable` | **UNVERIFIABLE** — dedicated closure, excluded from Brier scoring | Best-in-class: unknown ≠ wrong, scored separately |
| **HERMES** | `hermes_uncreated_classify` | **KNOWN / UNKNOWN / UNCREATED** — three-way | Distinguishes "I don't know" from "not yet created/undecidable" |
| **GEOX gates** | gate verdicts + claim `truth_class` | **UNMEASURED** (structural_invariants, structural_vision) · CANNOT TEST (claim falsification) | Gate-level unknown with receipt_hash |
| **WEALTH** | `wealth_synthesize` | **INSUFFICIENT_EVIDENCE** verdict class | Analyst-side unknown, never a constitutional verdict |
| **WELL** | calibration gates | UNMEASURED / DEGRADED states | Sensor-side unknown |
| **Agent membrane (proven 2026-10-05)** | cutoff-test lane C envelope | `claim_class: UNKNOWN` + falsifier | Empirical: classified UNKNOWN beat bare AND harness on Brier (0.2057) |
| **SOUL (Hermes)** | Hypothesis-Output H-class | labeled hypothesis + "Confirm/reject?" | H-class ≠ UNKNOWN but adjacent: labeled partial knowledge |

## Implication
The federation already speaks classified-uncertainty everywhere EXCEPT the kernel judge and the metabolic receipt — the two places where verdicts become permanent. A judge that can only say HOLD cannot record *dated, anchored* abstention; a receipt that cannot say UNKNOWN cannot meter the federation's honest ignorance. Both are additive enum/field extensions — **not built here** (discovery-first directive).

## Kernel probe caveat
Kernel :8088 currently reports `verdict HOLD / last_seal None` with runtime drift (pre-existing, flagged at session init). Enum claims above come from live MCP tool schemas, not kernel source reading.
