# arifos_memory: 40 live vs 99 expected — 2026-09-13

**Class:** OBSERVE. Not a restore. Not a SEAL.

## Cause (not a test typo)

| Source | Count |
|---|---:|
| Backup `qdrant_arifos_memory_backup_20260912.json` | **99** |
| Live `arifos_memory` | **40** |
| Intersection | 40 |
| Extra in live | 0 |
| **Missing from live** | **59** |

Of the 59 missing (as they were in the backup): **50 ACTIVE**, **9 EXPIRED**.

This is not “the test still wants 99.” The collection **lost 59 points** after 2026-09-12. Mostly ACTIVE. Not an expiry purge (that would drop EXPIRED first). Live remainder: 9 ACTIVE + 31 EXPIRED, all SRO v1.

AAA test `assertEqual(len(points), 99)` then expects 59 operational + 40 excluded. Live fails at the first assert (40 ≠ 99). **Do not change 99 → 40** until the 59 IDs have a disposition.

## Disposition (HOLD)

Restore from backup is a memory mutation. F13 if it re-admits claims. Next: classify the 59 IDs (ACTIVE_LOST / EXPIRED_DROPPED / INTENTIONAL_PURGE with evidence). Then either restore with gate, or tombstone with receipt.

Backup path: `/root/.local/share/arifos/qdrant_arifos_memory_backup_20260912.json`
