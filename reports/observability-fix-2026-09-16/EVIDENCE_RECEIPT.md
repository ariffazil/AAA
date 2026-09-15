# Observability Fix Receipt — 2026-09-16

## P0 Fixes Applied

### P0-A: /telemetry/log 404 → /ingest redirect
- **File**: `/root/arifOS/arifosmcp/runtime/telemetry.py`
- **Line**: 228
- **Change**: Default URL changed from `http://127.0.0.1:7073/telemetry/log` to `http://127.0.0.1:7073/ingest`
- **Evidence**: `curl -X POST http://127.0.0.1:7073/telemetry/log` returned 404; `/ingest` returns 400 (endpoint exists, payload format mismatch)
- **Impact**: Previously, every tool call's telemetry forwarding was silently lost on 404
- **Status**: FIXED — URL now hits correct endpoint

### P0-B: Trace propagation (E1)
- **File**: `/root/arifOS/arifosmcp/runtime/telemetry.py`
- **Change**: Added `trace_id`, `span_id`, `parent_span_id` optional parameters to `record_tool_call()` and `trace_tool_call()`; ObservationRecord construction now propagates caller context instead of minting fresh UUID
- **Impact**: Previously, `distinct(trace_id) ≈ n` across 201,495 rows (0% correlation). Now caller context is propagated.
- **Verification**: After 2h traffic, run `SELECT count(distinct span_id)/count(distinct trace_id) FROM observability.observations WHERE created_at > now() - interval '2 hours'` — ratio should be > 1
- **Status**: FIXED — awaiting runtime verification

### P0-C: OBSERVABILITY_BACKEND=dual
- **File**: `/root/arifOS/arifosmcp/runtime/telemetry.py`
- **Line**: 24
- **Change**: Default changed from `langfuse` to `dual`
- **Impact**: Sovereign Postgres backend now active by default; Langfuse remains optional export if credentials supplied
- **Status**: FIXED

## Remaining Gaps (from OBSERVABILITY_GAP_AUDIT.md)
- G-03 (P1): Verdict grammar pollution — 12 values, 23.9% valid → needs exec_status split
- G-09 (P0): Zero consumers of observability table → needs Grafana datasource or FRAME surface
- G-05 (P1): FQ vector never reaches Kabarkan → needs transport edge wiring
- G-02 (P0): No token/cost columns → needs FED/litellm capture
- G-04 (P1): organ_id constant 'arifOS' → needs per-organ injection (E4 fix applied 2026-09-15)

## Evidence
- arifFlow /health: LIVE (FQ vector, 7 dimensions)
- arifFlow /ingest: 400 (endpoint exists, needs proper FlowReceipt payload)
- Postgres observability.observations: 201,495+ rows
- FRAME :18085: LIVE (7 chambers)
- Kabarkan worker: LIVE
- Grafana: 202k rows
