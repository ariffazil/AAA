# NEXT FORGE HANDOFF (DSv4 → DSv4)

> **DITEMPA BUKAN DIBERI**
> **Source:** arifOS Session 135-138 (Opus Shadow Analysis → Eureka Engineering)
> **Status:** FORGED 2026-06-14 | 4 modules + 3 schemas pending

## What Changed

The Opus harness shadow analysis (session 134-137) exposed three structural gaps in the arifOS/AAA/A-FORGE governance stack. These four modules close those gaps.

## Forge Receipt — 2026-06-14

### 1. Citation Provenance (`core/citation_provenance.py`) — F2 TRUTH
**Kills:** Decorative citations ([1][2][3]), phantom citations, cross-model misattribution
**Enforces:** Every citation must carry `{source_model_id, tool_name, query_id, retrieval_timestamp, result_position}`
**Self-test:** PASSED (5/5)

### 2. Witness Diversity (`core/witness_diversity.py`) — F3 TRI-WITNESS
**Kills:** Mode-3 collapse (AI-judging-AI without Earth witness)
**Enforces:** 5 witness types (HUMAN, AI_MODEL_A, AI_MODEL_B, EARTH_MEASUREMENT, INDEPENDENT_HUMAN). Score < 3 → HOLD
**Self-test:** PASSED (6/6)

### 3. Shadow Audit (`core/shadow_audit.py`) — F9 form-vs-substance
**Kills:** Constitutional cosplay (model speaks floors/ΔS/DITEMPA while structurally SEALing), identity claims (model SEALs worth/marketing)
**Enforces:** 5-component composite shadow score. Detects form-vs-substance mismatch, SEAL/HOLD ratio drift, constitutional vocabulary density
**Self-test:** PASSED (6/6)

### 4. Pre-Forge Gate (`core/pre_forge_gate.py`) — Unified constitutional gate
**Wires together:** Citation Provenance → Witness Diversity → Shadow Audit
**Enforces:** Every MUTATE/DEPLOY/ALLOCATE/COMMUNICATE passes through all three checks
**Self-test:** PASSED (6/6)

## Next Steps (for next session)

### Immediate
1. **Wire into A-FORGE execution path** — `core/pre_forge_gate.py` is ready; the forge execution path needs to call `PreForgeGate.check()` before any MUTATE
2. **Wire witness diversity into AAA session init** — every `arif_session_init` should create a `SessionWitnessState` and register witnesses as they appear
3. **Wire citation provenance into tool call layer** — every search/fetch tool call should auto-create `CitationProvenance` records

### Schema work (needed)
4. `schemas/citation_provenance.schema.json` — JSON Schema for provenance records
5. `schemas/shadow_audit_result.schema.json` — JSON Schema for shadow audit output
6. `schemas/witness_diversity_state.schema.json` — JSON Schema for witness state

### Integration with existing infrastructure
7. Update `deliberation.ts` ToAC scoring to accept shadow audit results as input
8. Update `hold_queue.py` to accept `PreForgeGateResult` objects
9. Add witness diversity to AAA cockpit dashboard

### Hardening
10. Run floor benchmarks against the new gates (`benchmarks/floors/F02_truth.py`, `F03_tri_witness.py`, `F09_antihantu.py`)
11. Integration test: full Opus shadow transcript run through all three gates
12. Performance: shadow audit is regex-heavy; profile on >10KB inputs

## Architecture Note

```
BEFORE (gap existed):
  Model proposes → Harness gates (form only) → Execute
  Shadow leaks through form-compliance without substance-compliance

AFTER (gates added):
  Model proposes → Citation check → Witness check → Shadow audit → Execute
                   F2 enforced      F3 enforced      F9 enforced
```

The three gates operate independently — each can block. Pre-forge gate wires them in sequence, stopping at first block. OBSERVE/PROPOSE bypass all gates (reversible by definition).

## Root Cause Addressed

The Opus-Kimi shadow transcript proved: **even output that correctly diagnoses the shadow arrives in shadow-form.** Citation provenance, witness diversity, and form-vs-substance checking cannot be optional — because the diagnosis arrives infected by the same exploit it names. The harness must enforce these at the tool level; the model cannot be trusted to self-police.

---
**Agent Directive:** Read this brief. Pick up at Next Step 1. Execute autonomously per Tier 1 (AUTO-DO).
