# SHADOW-RUNBOOK.md — RSR v0 Phase 1 (acceptance report + rollback)

2026-10-30, KVM8. Design status: ACCEPTED FOR PROTOTYPING (review directive 30/10).
Production change authorized: NONE. Kernel verdict on this work: null (not requested).

## What was built

- `shadow_capture.py` — thin capture adapter, ~200 lines, stdlib only.
  Append-only JSONL ledger + quarantine file. No verdict issuance, no approval
  changes, no execution, no CHRON writes, no telemetry auto-forwarded.
- `test_fixtures.py` — the 7 mission fixtures + 3 acceptance tests, replayable.

## Tests actually executed (this session, 11/11 pass)

| Test | Result |
|---|---|
| F1 transport ok + kernel HOLD → both preserved, mismatch in projection | PASS |
| F2 same observation 2x → duplicate, one lineage | PASS |
| F3 supersede → only dependent lineage stales | PASS |
| F4 future-dated ts → quarantined | PASS |
| F5 malformed payload → quarantined, no fabricated defaults | PASS |
| F6 capture restart → replay deduped against persisted ledger | PASS |
| F6b corrupt trailing line → quarantined, clean records readable | PASS |
| F7 execution w/o verification → stays unknown/pending | PASS |
| A2 update → new version, original kept with freshness=stale | PASS |
| A9 forecast event type recorded at lock | PASS |
| A10 projection exposes zero authorization fields | PASS |

## Persistence behavior

- Ledger: append-only JSONL at store_dir/shadow_ledger.jsonl; supersede rewrites
  atomically via tmp+os.replace (crash-safe).
- Quarantine: store_dir/quarantine.jsonl; corrupt ledger lines land here — nothing
  silently dropped.
- State dir default (proposed): /root/forge_work/reality/RSR-2026-10-30/shadow_store/
  (on /dev/sda1 durable block, NOT tmpfs).

## Remaining unknowns / open items

1. Real-world soak not started — 14-day window is a proposal, fixtures ≠ field evidence.
2. CHRON adapter not written yet: mode stamp (retrospective/prospective), 4 timestamps,
   baseline_ref, retrieval manifest hash — contract agreed in TEMPORAL-CONTRACT.md,
   wiring pending.
3. Brier discrepancy 0.1780 vs 0.1735 (REALITY_MAP §4.3) unreconciled.
4. WELL drift + arifOS 4 uninstrumented floors: standing organ issues, out of Phase 1 scope.
5. Supersede rewrites the ledger file (marks stale in place). History preserved via
   fields, but a strict append-only purist would prefer supersede-as-new-record.
   Accepted for v0; revisit if CHRON chain discipline requires it.

## Rollback / removal procedure

1. Stop capture (if scheduled): remove any cron referencing shadow_capture.py.
2. Archive: `mv /root/forge_work/reality/RSR-2026-10-30 ~/archive/` or delete tree —
   capture layer has zero integration points with organs, so removal is complete
   by deleting the directory. No service imports it; no gate depends on it.
3. Verify clean removal: `grep -r "shadow_capture" /root/AAA /root/arifOS /root/A-FORGE`
   → must return nothing (it will: nothing was wired).

— DITEMPA BUKAN DIBERI ⚒️
