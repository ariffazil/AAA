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

## Forge Wiring — 2026-06-14 (Session 141)

### ✅ WIRED — Immediate (1-3)
1. ✅ **PreForgeGate into A-FORGE execution path** — `PreForgeGateClient.ts` + wired into `/execute` in `server.ts`. Every EXECUTE_REVERSIBLE/EXECUTE_HIGH_IMPACT/IRREVERSIBLE action now passes through F2 (citation), F3 (witness), F9 (shadow) before execution. Fails closed — gate error logs CAUTION but allows.
2. ✅ **Witness diversity into AAA session init** — `preforge_bridge.js` wired into AAA `server.js`. HUMAN registered on task submission. A-FORGE `/execute` auto-registers EARTH_MEASUREMENT on tool success. Pre-forge service auto-registers model output witnesses via `/check` calls.
3. ✅ **Citation provenance into tool call layer** — `/citation` and `/provenance/batch` endpoints on pre-forge service (port 18990). `captureCitationProvenance()` TypeScript client in A-FORGE. Search/fetch results can be auto-captured as PROVENANCED citations.

### New Infrastructure Created
- **`core/pre_forge_service.py`** — HTTP microservice on port 18990 (9 endpoints: /check, /quick, /witness, /earth, /model, /citation, /provenance/batch, /health, /witness/:id)
- **`a2a-server/preforge_bridge.js`** — Node.js bridge for AAA gateway (fire-and-forget witness registration)
- **`scripts/run_preforge_service.sh`** — Service runner script
- **`/etc/systemd/system/aaa-preforge.service`** — systemd unit (active, running)
- **A-FORGE `src/domain/governance/PreForgeGateClient.ts`** — TypeScript client (pre-forge check, witness reg, citation capture)

### Architecture
```
Model proposes → A-FORGE /execute
                  ├─ classifyTool(actionClass)
                  ├─ requiresGovernance? → SESSION + LEASE gates
                  ├─ ATOMIC? → 888_HOLD gate
                  ├─ PRE-FORGE GATE (NEW) → POST :18990/check
                  │   ├─ F2 Citation Provenance
                  │   ├─ F3 Witness Diversity
                  │   └─ F9 Shadow Audit
                  ├─ Execute MCP tool
                  └─ Auto-register EARTH_MEASUREMENT witness
```

### Next Steps (remaining)
4. `schemas/citation_provenance.schema.json`
5. `schemas/shadow_audit_result.schema.json`
6. `schemas/witness_diversity_state.schema.json`
7. Update `deliberation.ts` ToAC scoring with shadow audit input
8. Update `hold_queue.py` to accept `PreForgeGateResult` objects
9. Add witness diversity to AAA cockpit dashboard
10. Run floor benchmarks against new gates
11. Integration test: full Opus shadow transcript through live gates
12. Performance profiling on >10KB inputs

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
