# canon-replicate — Edge Registry Addition Receipt (Lane B Audit)

> **Status:** `external_advisory_infrastructure_receipt` (Lane B autonomous, no F13 seal claimed)
> **Writer:** FI-003 anonymous session, `actor_verified=false`, `OBSERVE_ONLY` (per F13 directive "add edge_assertions.jsonl to canon-replicate")
> **Date:** 2026-09-25T00:40 MYT
> **Method:** Script edit + systemd cron (every 15 min)

---

## 0. Per Reality Test v2 (FIX priority 1)

Per `/root/AAA/reports/edge-registry-reality-test-v2-kvm4-2026-09-25.md` §4.1 — Edge Registry not federated invariant:

> *"Edge registry is KVM8-only; KVM4 doesn't have arifFlow, no replicate target. Add to `canon-replicate` cron (replicate `edge_assertions.jsonl` KVM8 → KVM2)"*

**Executed:** Edited `/root/scripts/canon-replicate` to add STEP 5.5 (Edge Registry replication). KVM2 was the correct target (per topology: KVM8 = forge, KVM4 = workshop, KVM2 = witness).

---

## 1. Implementation Result

| Component | Status |
|---|---|
| **Script edit** | ✓ `/root/scripts/canon-replicate` (167 lines, +27 lines for STEP 5.5) |
| **STEP 5.5 added** | ✓ Lines 140-164 (rsync Edge Registry + chattr + parity) |
| **Test execution** | ✓ Manual run + cron will trigger every 15 min |
| **KVM2 edge file** | ✓ `/var/lib/arifos/edge_assertions.jsonl` (9954 bytes, sha256:d7851dae…, chattr ----ia--------e-------) |
| **Parity verified** | ✓ KVM8 == KVM2 (`edge_parity_pass` event in receipt log) |

---

## 2. STEP 5.5 Implementation (the new code)

```bash
# === STEP 5.5 (v0.5): rsync Edge Registry → KVM2 ===
# Per reality-graph-doctrine-20260912: Edge Registry as Reality Graph substrate
# Per writer-governance-ownership: writer needs flock + atomic write + schema validation
# Edge file is APPEND-ONLY locally (chattr +a); preserve on KVM2 mirror
if [ -f "$EDGE_SRC" ]; then
  if rsync -avz -e 'ssh -o StrictHostKeyChecking=no' \
    "$EDGE_SRC" "root@$KVM2_HOST:$KVM2_EDGE" 2>/dev/null; then
    emit "rsync_edge_complete" "src=$EDGE_SRC" "dest=$KVM2_HOST:$KVM2_EDGE"
    ssh -o StrictHostKeyChecking=no "root@$KVM2_HOST" \
      "chattr +a $KVM2_EDGE 2>/dev/null; chattr +i $KVM2_EDGE 2>/dev/null"
    K8_EDGE_HASH=$(sha256sum "$EDGE_SRC" 2>/dev/null | awk '{print $1}')
    K2_EDGE_HASH=$(ssh -o StrictHostKeyChecking=no "root@$KVM2_HOST" \
      "sha256sum $KVM2_EDGE 2>/dev/null" | awk '{print $1}')
    if [ -n "$K8_EDGE_HASH" ] && [ -n "$K2_EDGE_HASH" ] && [ "$K8_EDGE_HASH" = "$K2_EDGE_HASH" ]; then
      emit "edge_parity_pass" "hash=$K8_EDGE_HASH"
    else
      emit "edge_parity_fail" "kvm8=$K8_EDGE_HASH" "kvm2=$K2_EDGE_HASH"
      telegram_alert "CRITICAL" "EDGE REGISTRY DRIFT..."
    fi
  else
    emit "rsync_edge_failed"
    telegram_alert "CRITICAL" "rsync edge_assertions.jsonl FAILED..."
  fi
else
  emit "rsync_edge_skipped" "reason=no_source_file"
fi
```

---

## 3. Test Run Receipt Log (live)

```
{"ts":"2026-09-24T16:34:45Z","event":"started","src":"/root/AAA/canon","kvm2":"100.64.0.4"}
{"ts":"2026-09-24T16:34:46Z","event":"kvm2_reachable","host":"100.64.0.4"}
{"ts":"2026-09-24T16:34:46Z","event":"rsync_canon_complete","files":"total"}
{"ts":"2026-09-24T16:34:47Z","event":"rsync_receipt_complete"}
{"ts":"2026-09-24T16:34:47Z","event":"lock_applied"}
{"ts":"2026-09-24T16:34:47Z","event":"parity_pass","hash":"ba7badbe…"}
{"ts":"2026-09-24T16:34:48Z","event":"rsync_edge_complete","src":"edge_assertions.jsonl"}
{"ts":"2026-09-24T16:34:49Z","event":"edge_parity_pass","hash":"d7851dae…"}
{"ts":"2026-09-24T16:34:49Z","event":"complete","verified":"true"}
```

✓ All 9 events present (7 original + 2 new edge events).

---

## 4. Storage Discipline on KVM2

Per `seal_chain.jsonl append-only` + `edge_assertions.jsonl` discipline:

```
$ lsattr -d /var/lib/arifos/edge_assertions.jsonl (KVM2)
----ia--------e-------  (append-only + immutable enforced)
```

| Attribute | Flag | Meaning |
|---|---|---|
| `i` | immutable | File cannot be modified, renamed, deleted |
| `a` | append-only | New content can be APPENDED, existing content cannot be modified |
| `e` | extent format | ext4 (not strictly tamper-evidence, just format indicator) |

**Both KVM8 + KVM2 have identical append-only + immutable on `edge_assertions.jsonl`.**

---

## 5. F2 TRUTH Labels + Receipts

| Claim | F2 Class | Confidence | Basis |
|---|---|---|---|
| "STEP 5.5 added to canon-replicate (lines 140-164)" | OBS | CONFIRMED | grep + line count |
| "STEP 5.5 fires on manual run (rsync_edge_complete + edge_parity_pass)" | OBS | CONFIRMED | receipt log |
| "KVM8 sha256:d7851dae == KVM2 sha256:d7851dae (parity)" | OBS | CONFIRMED | sha256sum comparison |
| "KVM2 chattr +a +i applied to edge_assertions.jsonl" | OBS | CONFIRMED | lsattr remote probe |
| "Timer still active (Fri 00:48:08 next run)" | OBS | CONFIRMED | systemctl list-timers |
| "Edge Registry NOT yet cross-node witness agreement (federation invariant gap remains)" | INT | PLAUSIBLE | per `federation-invariant-identification-20260906` (cross-node replication ≠ cross-node agreement) |

| Receipt | Type | Path |
|---|---|---|
| `OBS-KVM8-20260925-0035-001` | Script edit verification (STEP 5.5 present) | local probe |
| `OBS-KVM8-20260925-0035-002` | Manual test run (script executes, exits 0) | direct exec |
| `OBS-KVM8-20260925-0035-003` | Receipt log shows edge_parity_pass | receipt log probe |
| `OBS-KVM8-20260925-0035-004` | KVM2 sha256 == KVM8 sha256 | sha256sum comparison |
| `OBS-KVM8-20260925-0035-005` | KVM2 lsattr (chattr +a +i confirmed) | ssh + lsattr |
| `OBS-KVM8-20260925-0035-006` | Timer still scheduled (next: 00:48:08) | systemctl list-timers |

---

## 6. Cross-References

- `/root/scripts/canon-replicate` — Modified script (167 lines)
- `/var/lib/arifos/edge_assertions.jsonl` (KVM8) — Edge Registry source
- `/var/lib/arifos/edge_assertions.jsonl` (KVM2) — Edge Registry mirror (NEW — via STEP 5.5)
- `/root/AAA/canon/EDGE-REGISTRY-PERSONS-YAML-CONNECTION-RECEIPT-2026-09-25.md` — Connection receipt (canonical)
- `/root/AAA/reports/edge-registry-implementation-receipt-2026-09-25.md` — Implementation receipt
- `/root/AAA/reports/edge-registry-reality-test-v2-kvm4-2026-09-25.md` — Reality Test v2 (FIX priority 1 source)
- `/etc/systemd/system/canon-replicate.timer` — Cron schedule (every 15 min)
- `/etc/systemd/system/canon-replicate.service` — Service unit
- `/var/lib/arifos/replication_receipts.jsonl` — Cron receipt log

---

## 7. Constitutional Status

```yaml
artifact:
  type: infrastructure_receipt
  status: external_advisory (Lane B)
  canonical_standing: NONE — Lane B audit (script edit, no F13 seal claimed)
  lane: B (autonomous)

constitutional_status:
  f1_amanah: satisfied (reversible — script edit, can revert)
  f2_truth: explicit F2 labels + 6 receipts + edge_parity_pass in receipt log
  f4_clarity: entropy reduction via single new step
  f7_humility: Ω₀ = 0.05 (declared gap: cross-node agreement ≠ cross-node replication)
  f8_genius: simplest correct path — extend existing cron, no new infrastructure
  f9_anti_hantu: witnessing ≠ claiming (replication ≠ federation invariant)
  f10_ontology: substrate ≠ being (KVM8 + KVM2 have identical sha256, distinct substrates)
  f11_audit: 6 receipts captured
  f12_injection: no external content propagated
  f13_sovereign: PROMULGATED via F13 directive "add edge_assertions.jsonl to canon-replicate"
```

---

## 8. Writer Authority

```yaml
writer:
  agent_id: FI-003 (anonymous session)
  actor_verified: false
  authority_band: OBSERVE_ONLY
  f13_standing: NONE
  role: external_advisory_infrastructure_author (Lane B)

edit_authority: F13 directive "add edge_assertions.jsonl to canon-replicate"
edit_scope: script modification + cron trigger
edit_method: bash edit + chmod +x + systemctl list-timers verification
```

---

DITEMPA BUKAN DIBERI — canon-replicate v0.5 STEP 5.5 added per F13 directive. Edge Registry now replicated KVM8 → KVM2 via cron every 15 min. sha256 parity verified (d7851dae…). Append-only + immutable preserved on both nodes. Receipt log shows all 9 events (7 original + 2 new edge). Timer still scheduled. Honest gap disclosure: cross-node replication ≠ cross-node agreement (federation invariant gap remains). Standing by.

`#CANON-REPLICATE-EDGE-ADDITION-RECEIPT-2026-09-25`
