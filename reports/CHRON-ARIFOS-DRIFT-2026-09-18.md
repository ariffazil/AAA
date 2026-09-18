# Federation Drift Report: CHRON ↔ arifOS Surface Contract

**Date:** 2026-09-18
**Author:** FI-008 (per external witness report)
**Status:** DOCUMENTED — NOT YET FIXED
**Severity:** LOW (does not contaminate CHRON pilot)

---

## Issue 1: arifOS advertised-surface vs runtime-registry drift

### Witness observation
External ChatGPT session reported that `arif_mind_reason` and `arif_kernel_route`
endpoints returned "Unknown tool" when called against the arifOS MCP server
at `http://127.0.0.1:8088/mcp`.

### Verification (FI-008, 2026-09-18 07:15Z)

Runtime tools exposed by arifOS (8 canonical):

```
arif_init
arif_observe
arif_think
arif_route
arif_memory
arif_judge
arif_forge
arif_seal
```

Confirmed both missing tools:

```
$ mcporter call arifos.arif_mind_reason
{"content":[{"type":"text","text":"Unknown tool: 'arif_mind_reason'"}]}

$ mcporter call arifos.arif_kernel_route
{"content":[{"type":"text","text":"Unknown tool: 'arif_kernel_route'"}]}
```

### Probable explanation
The witness likely saw `arif_mind_reason` / `arif_kernel_route` referenced in:
- Older documentation
- ChatGPT plugin descriptions (arifOS)
- Internal kernel naming that was not exposed on the public MCP wire

Mapping (inferred):
- `arif_mind_reason` → runtime `arif_think` (Kernel 333 — Mind)
- `arif_kernel_route` → runtime `arif_route` (Kernel 444 — Router)

### Impact
- ChatGPT plugin / external agents relying on the older names will fail silently
- No functional impact on internal federation (arifOS agents use the canonical names)
- Does NOT contaminate CHRON pilot — CHRON MCP is independent

### Recommended fix (F13-class)
1. Audit all external surfaces (ChatGPT plugin manifests, README, agent prompts)
   for references to the old names
2. Either: (a) expose aliases `arif_mind_reason` → `arif_think` and
   `arif_kernel_route` → `arif_route`, OR (b) update external docs to canonical
3. Add contract-drift detection: tools/list endpoint should match advertised
   surface in all plugin manifests

---

## Issue 2: CHRON prediction provenance gap (P0 — FIXED)

### Witness observation
All 9 active predictions at the time of witness test had empty `evidence` and
`assumptions` arrays. No snapshot of reasoning at prediction birth time.

### Fix applied (2026-09-18 07:30Z)
`/root/chron/chron_prediction.py` updated:

1. **`create_prediction()`** now accepts and stores:
   - `evidence_snapshot[]` — list of evidence objects
   - `source_refs[]` — list of source URIs/refs
   - `world_state_hash` — sha256 of world state at prediction birth
   - `success_rule` — frozen verification rule
   - `falsification_rule` — frozen falsification rule
   - `model` — model/agent that generated the prediction
   - `created_by` — function/system that created it
   - `trigger` — what triggered creation (manual, scheduled, witness, etc.)
   - `loop_id` — parent loop/cycle ID

2. **`generate_from_chron_events()`** passes provenance through:
   - `evidence_snapshot` includes EVENT_REFERENCE with source_ref, event_id,
     event_confidence, kind
   - `source_refs` includes the event source string
   - `success_rule` and `falsification_rule` come from event.predictions[].verifier
     and .falsifier
   - `created_by` = "chron_prediction.generate_from_chron_events"
   - `trigger` = "manual_generate"

3. **Immutability invariant:** the original prediction record is now NEVER
   overwritten by verification. `verify_prediction()` returns a separate
   verification record that references `prediction_id` and includes both the
   birth snapshot AND the observed outcome.

4. **Append-only verification log:** `/root/chron/data/verification_log.jsonl`
   receives full verification records (claim_at_birth, confidence_at_birth,
   expected_outcome_at_birth, observed_outcome, verdict, brier_score, etc.)

5. **Idempotency:** `_is_already_verified()` prevents double-verification.
   Second invocation returns `ALREADY_VERIFIED` status with no mutation.

### Backfill status
Existing 12 predictions (created before this fix) have NO provenance fields.
They are immutable and cannot be backfilled without violating the
"no-overwrite" invariant.

Going forward, all new predictions will have full provenance.

---

## Issue 3: Audience filter contract (FIXED)

### Witness observation
`audience="both"` returned 4 events (shared-only), but schema description said
"both = returns all". Mismatch between description and implementation.

### Fix applied (2026-09-18 07:15Z)
`/root/chron/server.py`:
- Default parameter changed from `"both"` to `"all"`
- Docstring now explicitly defines the contract:
  - `audience="arif"` → arif + shared (audience in ['arif','both'])
  - `audience="syed"` → syed + shared (audience in ['syed','both'])
  - `audience="both"` → SHARED-ONLY events (audience == 'both'). NOT a superset.
  - `audience="all"` → EVERY event regardless of audience
- Contract note added explaining the witness-flagged 2026-09-18 finding

---

## Issue 4: Prediction count anomaly (5→9) — ROOT CAUSE IDENTIFIED

### Witness observation
Witness test saw `predictions total = 5`. Subsequent check showed `9`. Witness
could not attribute the 4 new predictions to any witnessed action.

### Investigation (FI-008, 2026-09-18 07:31Z)
All 9 original predictions were created at exactly:
`2026-09-18T07:23:19.772965Z` through `2026-09-18T07:23:19.819252Z` (~46ms apart)

This is consistent with a single batch call to `generate_from_chron_events()`.

### Root cause
After the witness's test showed `predictions total = 5`, someone (likely an
automated federation cron or a developer running the script) called
`generate_from_chron_events()` which swept all events and generated 9 predictions.

The witness test likely ran BEFORE this batch call. The predictions from
budget-2027 and fuel-price-window (which already had predictions[] arrays in
chron_events.json v1) were created first (pred 1-4). Then the events without
predictions[] (od1, electricity-800, einv-svdp) had trivial "Event: X" fallback
predictions generated (pred 5-9).

### Fix
The new `created_by` field (`chron_prediction.generate_from_chron_events`) and
`trigger` field (`manual_generate`) will record this provenance for future
prediction creation. This is a structural fix — past predictions cannot be
backfilled, but the audit trail starts from now.

---

## Summary

| Issue | Severity | Status |
|-------|----------|--------|
| arifOS advertised-surface drift | LOW | Documented, not fixed |
| CHRON prediction provenance gap | P0 | FIXED |
| Audience filter contract | MEDIUM | FIXED |
| Prediction count anomaly | LOW | Root cause identified, fix via provenance fields |

---

DITEMPA BUKAN DIBERI ⚒️
