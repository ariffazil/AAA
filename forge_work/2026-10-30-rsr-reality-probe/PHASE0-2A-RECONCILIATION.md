# PHASE0-2A-RECONCILIATION.md — receipts-only corrections (no new live probes)
2026-10-30. Per directive: stop additional live probes; fix claims using existing
receipts; E5 offline only; CHRON write proposals returned separately below.

## R1 — arif_seal-absent claim: RETRACTED

General claim "arif_seal tiada" ditarik balik. Receipts: tools/list :8088 [PROBE]
shows arif_seal among 9 tools with 6 modes; REST surface /tools/arif_seal reported
by Hermes lane [RELAYED]. What survives: the two surfaces (connector catalog vs live
endpoint) expose different capability sets for the inspected context; bound-actor
consequential path remains UNTESTED. HOLD on claim: call_hash pairs request/response
but does not by itself prove a receipt was persisted or a grant issued.

## R2 — WEALTH reconciliation: attempted receipt write recorded as finding

Facts from existing receipts:
- Hermes lane report (earlier): capital_claims NOT called due to schema-declared
  vault-write side effect [RELAYED].
- My probe: capital_registry(mode=list) on :18082 [PROBE]. Tool executed the list,
  and its response _meta.wealth_receipt self-reports: persisted:false,
  error "[Errno 1] Operation not permitted: /root/VAULT999/wealth/receipts.jsonl",
  receipt_id 1d4000e1-21eb-4730-886e-1d83969c272d, call_status FAIL.
Reconciliation: two DIFFERENT tools. The lane avoided capital_claims by schema; I
called capital_registry, whose wrapper attempts receipt persistence automatically —
side effect NOT visible in the schema I inspected before the call. So the accurate
record: one WEALTH call this batch attempted receipt persistence and failed; the
registry answer itself was served; receipt NOT persisted (tool self-report).
receipt_persisted: not_established independently; other_side_effects: unknown.
No chmod/chown/retry performed. Errno 1 insufficient for root cause (candidates:
file ownership, immutable flag, mount, wrapper path) — repair is a separate mission.

Batch closure sentence (corrected): "Tiada closure CHRON atau perubahan
gate/deployment dilakukan. Fail audit lokal ditulis. Satu panggilan WEALTH
melakukan cubaan persistence receipt secara automatik dan GAGAL; kesan lain
belum ditentukan."

## R3 — A-FORGE restart debt: UNCONFIRMED HYPOTHESIS

Observed [PROBE]: HEAD 22348c55 (30/10 01:15 +0800) > dist mtime 29/10 22:36 (+0800
local) > process start 29/10 19:58 (+0800 local, ps lstart). Caveats accepted:
mtimes share host-local timezone here, but file may have been overwritten while the
process ran; running-code identity NOT fully established (no artifact hash captured);
unit ExecStart points at dist/src/interfaces/mcp/cli.js [DOC systemd unit].
Verdict: source_build_difference observed; running_code_identity not_fully_established;
restart_required: undetermined; rebuild_required: undetermined. Restart is a service
change — separate decision, NOT a hygiene step. N5 (artifact hash + cmdline capture,
read-only) remains the cheap path to close provenance.

## R4 — CHRON proposals matched to original criterion/window

Only pred-9b8ad was near-closable; its ORIGINAL criterion tightened:
- Claim: "Verified predictions reach >= 40 by 2026-10-22 (Lane A evidence growth)"
- success_rule: `cd /root && PYTHONPATH=/root python3 -m chron status -> predictions.verified`
- falsifier: "predictions.verified < 40 at 2026-10-22"
Open definitional questions before correct=true: does `predictions.verified` count
raw verification records or effective/deduped observations? Which store/scope? The
existing receipts give: store_stats verified:54 and calibration total_verified:47
[PROBE 30/10] — two different counters already visible. Value AS OF 22 Oct was NOT
captured and is not reconstructible from receipts in hand (verified-record timestamps
were retrieved but their 22-Oct distribution was not recorded before the probe-stop).
=> Proposal DOWNGRADED from "close as correct=true" to "close only after one
read-only as-of-count derivation". Exact write args drafted below, conditional.

Seven governance falsifiers: "resolvable offline" downgraded to PROPOSAL — each needs
criterion matching first (static inspection vs live behaviour vs absence-over-window).
pred-a955a: needs sourced news evidence or UNVERIFIABLE; memory insufficient.

## R5 — calibration readings preserved raw, both kept

| reading | value | n | source | cohort metadata |
|---|---|---|---|---|
| A | 0.17346889 mean_brier | total_verified 47 (store), calibration snapshot effective_n 41 | /root/chron/data/calibration.json, snapshot updated_at 2026-10-26T23:15Z [PROBE-embedded] | policy chron-observation-level-rule-v1; effective (deduped) counting; accuracy 0.7947 in embedded snapshot |
| B | 0.1780 recomputed | 40 records with brier_score, of 50 retrieved | chron_verified_predictions live retrieval 2026-10-30 [PROBE] | raw per-record brier_score mean; includes records verified AFTER snapshot A |

Both retained; neither averaged, neither discarded. Delta hypothesis (snapshot
timing: B includes post-26-Oct verifications) remains HYPOTHESIS until record-level
timestamps are joined — one read-only join, deferred under probe-stop.

## E5 — offline fixtures status

test_fixtures.py: 11/11 PASS (recorded earlier this session, replayable offline;
no live calls). No new offline work required by this directive; sanitized-replay
extension (replay recorded CHRON responses through the capture layer) listed as
optional next offline item.

---

## CHRON WRITE PROPOSALS — returned separately, NOT submitted, per-proposal approval

Schema note: chron_record_verification required fields observed on live connector:
prediction_id, observed_outcome, correct. Optional fields named in the pasted
adapter contract (witness_claim_id, criterion, evidence_ref, outcome_time,
observation_time, coverage, entailment, resolver_id, resolver_relation) are
UNVERIFIED against live schema — each proposal below uses only required fields;
optional fields to be confirmed by one schema read before submission.

### P1 — pred-9b8ad2e39891 (CONDITIONAL on as-of derivation)
```json
{
  "prediction_id": "pred-9b8ad2e39891",
  "observed_outcome": "predictions.verified counter observed 54 on 2026-10-30 via chron_store_stats; criterion threshold 40 at 2026-10-22; as-of-2026-10-22 derived count = <TO_FILL from ledger verified_at join before submission>",
  "correct": true
}
```
Preconditions: (a) as-of-22-Oct count >= 40 derived from existing ledger timestamps;
(b) counter semantics matched to success_rule command. If (a) fails -> correct=false
with same observed_outcome structure. If counter semantics ambiguous -> UNVERIFIABLE
via chron_resolve_unverifiable {prediction_id, reason} instead.

### P2..P8 — seven governance falsifiers (pred-b1c05, f843a, da1bd, 387b, 2792d, e9e75, 8b835)
NO arguments drafted yet: each requires criterion-match pass first (R4). Submitting
now would be verdict-first-evidence-later. Order after P1: evidence pass -> per-item
proposal -> per-item approval.

### P9 — pred-7229f (EROI /opt)
Requires one fresh read-only filesystem audit (find on /opt). Deferred: probe-stop.
### P10 — pred-a955a (Nik Nazmi identity)
Requires sourced news probe (external surface) -> correct=true/false with
evidence_ref, or chron_resolve_unverifiable if sources conflict/absent. Deferred
pending external-probe approval.

STOP STATE: no forecasts closed, no permissions changed, no services restarted,
no retries of WEALTH persistence. All live probes halted per directive.
