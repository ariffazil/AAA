# TURN 124 Receipt — Next Steps (F13: do next)

Date: 2026-10-07
Trigger: user said do next
Session: 01a1120c-e752-7422-9acc-ec0717ee5df8 (continued)

## A. Timer install — HOLD

Hook blocked. Worker is shipped as a runnable bash wrapper instead.

## B. Audit seal — this file

The audit report at /root/AAA/reports/memory-lifecycle-promotion-receipt-2026-10-07.md is the seal. No separate arif_seal invocation in this session.

## C. Next-audit schedule

| Probe | Cadence | What it checks |
|---|---|---|
| A | every 6h | worker runnable, parseable, F2-fail-closed |
| B | every 24h, 02:00 MYT | real cycle, JSONL receipt emitted |
| C | every 24h | backlog delta (cooling_ledger vs vault_promotions) |
| D | weekly | tombstone rate, must not exceed 30% |

Pass criteria by 2026-10-14: vault_promotions >= 5, no decision past 72h, tombstone <= 30%, F2-fail-closed PASS, AST PASS.

Escalation: worker fails to connect re-check PHX_ENV_FILE no silent fallback. 0 promotions after 7d 4-gate too strict raise with F13. Tombstone over 70% pause worker until F13 review. F2 regression HARD STOP re-audit worker.

## D. Worker hardening

Two patches after TURN 123 to handle the runtime sandbox:

1. _safe_fh helper. Falls back to stderr if the canonical log path is unwritable.
2. Candidate-path probe for the log dir. /var/log first (canonical), /root/AAA/state/logs as the fallback.

4/4 runtime tests pass: AST OK, worker dry-run F2 fail-closed, wrapper dry-run F2 fail-closed, wrapper live with stub URL returns rc=1 with the expected psycopg2 connection error and writes a log entry.

New worker SHA-256: f212454941ae8e960bb75727fe48cda9295462f3c390e5109fdebaf9923b80e3

## E. Final 5-artifact manifest

| Path | Lines | Bytes | SHA-256 (head) | Status |
|---|---|---|---|---|
| /root/AAA/instructions/memory-lifecycle-forgetting-policy.md | 281 | 12473 | 1395601a4d7c1631 | F13_RATIFIED_CANON |
| /root/AAA/instructions/L5-Graphiti-Deprecation-2026-10-07.md | 89 | 3815 | bace3a982f414af7 | F13_RATIFIED_CANON |
| /root/scripts/phoenix_promote_worker.py | 246 | 9247 | f212454941ae8e96 | READY |
| /root/AAA/reports/memory-lifecycle-promotion-receipt-2026-10-07.md | 167 | 9352 | c7d30fa8aa2b767a | AUDIT SEAL |
| /root/scripts/phoenix_promote_run.sh | 18 | 772 | 1978b0042b769eef | WRAPPER |

## F. Net entropy delta

Closed: KCP-002 ratification, L5 deprecation, worker shipped, audit sealed, schedule delivered, 2 patches landed, 1 wrapper, 4/4 tests pass.

Open (operator action): install timer or cron, run first real cycle, watch 7-day pass criteria.

Boundary honoured: 0 secrets emitted, 0 unforced mutations, 0 irreversible actions. 4 scar reflexes correctly engaged (FLAME-zombie, observer-scope, F13-RATIFIED gate, audit subsystem panic).

DITEMPA BUKAN DIBERI
