# RSR Compatibility Matrix — Evidence-Backed

## Inspection Date
2026-10-30 09:15 MYT

## Components Inspected

### 1. CHRON (Temporality)
- **Location:** `/root/CHRON/`
- **Branch:** `feat/observer-attribution-derived`
- **Schema:** `chron_events.json` (91 events, prediction Schema v1)
- **Lifecycle:** event → prediction → due → verification → lesson
- **Persistence:** JSONL birth store + verification ledger + chron_events.json
- **MCP Tools:** 22 tools (chron_create_event, chron_record_verification, etc.)
- **Key Contract:** Brier scoring, attention debt, calibration state
- **Verified:** Live MCP server, events.json exists, predictions due works

### 2. A-FORGE (Execution)
- **Location:** `/root/A-FORGE/`
- **Branch:** `repair/aforge-f3-f8-2026-10-25`
- **Reality Loop:** 7-stage ledger (MEANING→OBSERVE→ENCODE→IMPROVE→VERIFY→SEAL→RETURN)
- **Persistence:** In-memory Map + VAULT999 append (via arifOS)
- **Key Contract:** No autonomous self-modification, human judgment at RETURN
- **Verified:** Source exists, types defined, engine.ts implements state tracking

### 3. arifOS (Authorization)
- **Location:** `/root/arifOS/`
- **Branch:** `main`
- **Lifecycle:** init → observe → think → judge → forge → seal
- **Verdicts:** SEAL, HOLD, SABAR, VOID
- **Key Contract:** Capability ≠ Authority, kernel adjudicates floors
- **Verified:** TypeScript project, MCP server structure present

### 4. HERMES (Reasoning)
- **Location:** `/root/HERMES/`
- **Tools:** claim_validate, contradiction_scan, counterstory_test, reality_grounding
- **Key Contract:** Evidence transport, not verdict generation
- **Verified:** MCP tools available via config.toml

### 5. FRAME (Witness)
- **Location:** `/root/FRAME/`
- **Branch:** `fix/frame-witness-reach-20261019`
- **Tools:** probe, drift, trend, baseline, behavioral_drift
- **Key Contract:** Observational only, evidence not verdict
- **Verified:** Source exists, MCP tools defined

### 6. GEOX/WEALTH/WELL (Evidence Envelopes)
- **GEOX:** `fix/geox-p0-rebased` — Earth observation packets
- **WEALTH:** `fix/agentic-ci-portable-tests-20261018` — Capital analysis envelopes
- **WELL:** `chore/well-ignore-runtime-pointer-2026-10-25` — Vitality assessments
- **Key Contract:** Each organ produces evidence envelopes, not constitutional verdicts

### 7. Sado Prototype (Reality Graph)
- **Location:** `/root/forge_work/sado/reality-graph/`
- **Files:** reality_graph.py, demo.py, syed-reality-graph.json
- **Schema:** Evidence, Hypothesis, Link, Question, SafetyAssessment, Proposal, Approval, Outcome
- **Key Contract:** tick() evaluates but never executes; exact proposal binding
- **Verified:** Python module imports, dataclasses defined, export works

## Compatibility Matrix

| Requirement | Existing Implementation | Verified Scope | Gap | Adapter |
|---|---|---|---|---|
| Stable IDs | CHRON: event_id, pred_id; A-FORGE: session_id; Sado: uuid prefix | All organs use unique IDs | No cross-organ correlation ID | RSR correlation_id field |
| Evidence lineage | CHRON: parent_receipt_ids; Sado: lineage_id, supersedes | CHRON has full lineage, Sado has basic | A-FORGE loop lacks explicit lineage | RSR wraps evidence with lineage |
| Source + observation time | CHRON: source, target_date; Sado: source, observed_at | Both have timestamps | No standardized ingestion time | RSR adds ingested_at |
| Dependency references | CHRON: parent_receipt_ids; Sado: links | CHRON has receipt chains | No cross-organ dependency graph | RSR dependency edges |
| Supersession history | CHRON: supersession status; Sado: supersedes field | Both support supersession | No scoped invalidation | RSR stale marking |
| Exact action binding | Sado: canonical JSON hash; arifOS: action_hash | Sado enforces exact match | A-FORGE uses manifest string | RSR validates binding |
| Authorization reference | arifOS: seal_verdict_id, constitutional_chain_id | arifOS has full auth chain | Sado has Approval but no kernel link | RSR links approval to kernel |
| Execution attempt identity | A-FORGE: run_id; Sado: proposal_id | Both have execution IDs | No cross-reference | RSR execution_id |
| Outcome evidence | Sado: outcome.evidence_ids; CHRON: verification | Both capture outcomes | No consequence verification | RSR consequence field |
| Unknown/conflicting states | CHRON: UNVERIFIABLE; Sado: Safety.UNKNOWN | Both handle unknown | No explicit conflicting state | RSR conflict flag |
| Schema versions | CHRON: _prediction_schema; A-FORGE: types.js | Both versioned | No cross-schema versioning | RSR schema_version field |

## Reused Components

1. **Sado RealityGraph** — Core data model (Evidence, Hypothesis, Link, etc.)
2. **CHRON lifecycle** — Event → Prediction → Verification → Lesson
3. **arifOS authorization** — Kernel verdicts, seal_verdict_id
4. **HERMES contradiction_scan** — Engine-detected conflicts
5. **FRAME probe** — Independent witness, observational only
6. **A-FORGE reality loop** — 7-stage state tracking

## New Components (Thin Adapter Only)

1. **RSR Adapter** — Validates envelopes, preserves dimensions, detects duplicates
2. **Correlation ID** — Cross-organ trace linking
3. **Stale Marking** — Scoped invalidation on supersession
4. **Quarantine** — Malformed event isolation
5. **Visual Projection** — Render from runtime state

