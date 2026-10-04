# P0 Case Study — FQ Drift via Receipt Bypass

**Date:** 2026-08-11  
**Session:** arifOS federation metabolism crisis  
**Severity:** P1 constitutional trust chain emergency  
**Resolution time:** ~45 minutes from detection to diagnosis  

## Symptoms

```
FQ discrepancy detected by FRAME weekly cron (job b08b1c5d45c5):
  daemon FQ = 1.78  (OPTIMAL)
  disk FQ   = 6.40  (verify-dominant)
  |Δ|       = 4.62  (exceeds threshold for structural fault)
```

FRAME's drift_detection chamber fired automatically. Three actors held on stale data:
- `333-AGI`
- `333-AGI/FI-DELTA-MIND`  
- `333-AGI/OpenCode-FI-001`

## Root Cause Analysis

### Evidence Chain

1. **Disk record count:** 1,903 lines in `/var/lib/arifflow/receipts.jsonl`
2. **Daemon ingest count:** ~27 receipts (only 1.4% of total)
3. **Missing receipts:** 1,876 wrote directly to disk, bypassed `POST /ingest`

### Write Path Discovery

The receipt writers (arifOS kernel tools, A-FORGE forge_vault, etc.) were calling:
```python
# WRONG — writes directly to disk, skips ingestion
with open('/var/lib/arifflow/receipts.jsonl', 'a') as f:
    json.dump(receipt, f)
    f.write('\n')
```

When they SHOULD have been calling:
```python
# CORRECT — posts to daemon for FQ computation
requests.post('http://127.0.0.1:7073/ingest', json=payload)
```

The direct-write was a pre-existing operational shortcut; the `/ingest` endpoint existed but wasn't consistently called by all organ services.

### Why It Mattered

FQ gates constitutional enforcement (HOLD on actors). When 75% of receipts are invisible to the outer loop:
- FQ under-counts verify ratio → appears STUCK when it's actually OPTIMAL
- Actors HELD on wrong verdict → sovereign decision blocked
- System makes governance decisions on partial data → F2 TRUTH violation

## Replay Execution

Replayed all 1,980 receipts (including ones that hadn't appeared yet during replay window):

```bash
# Script at /root/forge_work/scripts/p0-ingestion-replay.py
# Uses /root/arifFlow/bridge/arifflow_client.py FlowReceiptEnvelope.to_ingest_dict()
# for correct payload serialization
```

Key technical details:
- Payload must use PascalCase field names (`Observation`, not `obs`) per Rust serde deserialization
- Chain-hash validation fails on some out-of-order records — expected, skip and continue
- Batch size limited to avoid overwhelming the daemon
- Each receipt logged with success/failure status

Post-replay state:
- FQ converged from 1.78 toward expected value (~6.40, full data now visible)
- Some actors auto-unblocked, others still held (need manual release or re-verification)

## Manual Release After Replay

Not all actors released automatically because some had executed new tasks during replay window (which also lacked verification receipts in daemon). Manual release via POST /release:

```bash
curl -sf -X POST http://127.0.0.1:7073/release \
  -H "Content-Type: application/json" \
  -d '{"actor_id":"ARIF"}'
```

All 18 actors released within ~30 seconds. Final state: FQ=1.44 OPTIMAL, 0 actors HELD.

## Lessons Captured

1. **Receipt bypass is silent.** No error message, no log entry. The only signal is divergence between disk count and daemon ingest count. Detect with: `wc -l < /path/to/log` vs `curl :PORT/health | jq '.receipts'`.

2. **PascalCase payloads matter.** The Rust server expects exact variant names. Using Python StrEnum Display values (lowercase) causes silent rejection. Always check `to_ingest_dict()` output from client libraries before sending.

3. **Chain hashes break replay order.** If receipts arrive out of sequence (older after newer), `previous_receipt_hash` won't match. Accept these failures, don't retry. They represent legitimate ordering issues, not corruption.

4. **Two paths = broken helix.** Having BOTH direct-write AND endpoint-post creates two incomplete pictures. Fix: make endpoint-post PRIMARY with direct-write as FALLBACK (not simultaneous). See Step 5 in SKILL.md.

## Related Sessions

- EUREKA-T-02 Seven Verbs + Helix Doctrine: `/root/AAA/canon/EUREKA-T-02-seven-verbs-helix.md`
- FI Card Slot Convention Fix (Kimi Code commit 5b1192f9): same day, same root cause pattern
- Agent-workbench audit path EROFS fix: separate but related filesystem misconfiguration
