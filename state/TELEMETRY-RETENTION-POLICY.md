# TELEMETRY RETENTION & SAMPLING POLICY — v1 (2026-10-29)

> Delegated policy decision (Arif → FI-008, Packet P7 pre-condition).
> Grounded in measured disk state (P0 report, same date). One page. LAW 2/10.
> Home: /root/AAA/state/ (governance/ is canon-locked). Enforcer:
> /etc/logrotate.d/arifos-telemetry

## Measured reality (2026-10-29, P0 disk report)

| Stream | Size | Rotatable? |
|---|---|---|
| flow_outbox.jsonl (drained harness receipts) | 41 MB | YES |
| /var/lib/arifflow/receipts.jsonl (arifFlow store) | 72 MB | YES* |
| mcp-audit.jsonl (witness audit lines) | 44 MB | YES |
| hook-invocations.jsonl | 8.5 MB | YES |
| posttool_heal.log | 1.8 MB | YES |
| VAULT999 ledgers + arifflow_sealed.jsonl | ~7 MB | **NO — canon, append-only (F1)** |

Total telemetry today ≈ 175 MB. Disk = 363G/387G used (94%).

**Finding: telemetry is NOT the disk risk.** Even 10 wired edges × 10k
calls/day × ~500 B/receipt ≈ 5 MB/day ≈ 1.8 GB/year vs 25 GB free. The real
consumers are backups (26G), .cache (22G), forge_work (20G), runtime (28G),
archives (8.3G) — outside this policy, listed for separate sovereign decision.

## The rule (F13-delegated, effective 2026-10-29)

1. **Hot retention: 7 days full fidelity.** Every receipt/telemetry line stays
   byte-exact 7 days (FQ, cooling correlation, edge verification window).
2. **Warm: days 8–30, gzipped in place.** ~10:1; 30-day archive of all streams
   ≈ 50–80 MB. Queryable by zgrep.
3. **Cold: deleted after day 30.** No summary layer — canonical ledgers below
   already carry the permanent record; a summary copy = duplicate system (L8).
4. **Never rotated:** VAULT999/*, arifflow_sealed.jsonl (hash-chained canon),
   CHRON episode ledger (institution memory, F1 amanah).
5. **Sampling: NONE on receipts.** FQ = verify/execute ratio; sampling either
   class corrupts the metabolism signal. Noisy stdout INSIDE receipts is
   truncated at source (2000 chars, already in posttool_engine_heal.py).
6. **No new telemetry stream without a row in this table.** New stream = add
   row + rotator entry in the same PR (P7 rule, binds E1–E5).

## Enforcement

- logrotate: weekly, rotate 4, maxage 30, compress, copytruncate.
- Review trigger: rotatable stream > 500 MB hot → tighten at next session,
  never by silent config edit.

## Reclaimed 2026-10-29 (initial pass)

- journal vacuum: ~0B freed (archived journals already rotated 22:00); 3756
  stray dirs removed. npm cache cleaned. Big items NOT touched (sovereign
  call): backups 26G, forge_work 20G, archives+_archive 8.3G, runtime 28G,
  docker images 17.3G.
