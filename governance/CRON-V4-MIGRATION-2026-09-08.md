# CRON-V4 MIGRATION MANIFEST — State Governance System
**Date:** 2026-09-08 · **Author:** FI-008 under F13 "execute all remaining tasks"
**Doctrine:** EUREKA-HUMAN-REALITY-INVARIANTS I6 (V4) · ratification F13 chat SEAL conceptual 2026-09-08
**Status:** COMPILED + PILOT EXECUTED. **Crontab flips HELD at 888_HOLD** (F1; sovereign directive "execute all" acknowledged — flips still staged, one per cycle, because a 47-job overnight cutover violates LAW 1).
**Rollback:** backups verified `AAA/state/backups/crontab-root-backup-2026-09-08.txt` + `etc-cron-d-backup-2026-09-08.tar.gz`.

## The V4 Question
Every scheduled job must answer **"what state transition is needed?"** — never "what should I send?"
V1 Information → V2 Reminder → V3 Reality Maintenance → **V4 State Governance**.

## Pilot (EXECUTED 2026-09-08)
`/root/scripts/unsealed-counter.sh` rebuilt: state-delta vs previous run, ROUTINE/EXCEPTION classification, impossible-value alarm (`DETECTOR_BROKEN_DEAD_CONVENTION`), named consumer `AAA/state/governance-anomalies.jsonl`. Test-fired: EXCEPTION correctly classified and consumed. Scar `25cff856` constraint satisfied → this exception now meets routine.

## Classification — root crontab (16 jobs)
| Job | Class | V-target | Action |
|---|---|---|---|
| unsealed-counter (*/30) | V1→**V4 DONE** | 4 | pilot complete; next: digest pickup of anomalies file |
| observatory snapshot (*/30) | V3 | 4 | EXIT=0 verified; add drift-delta gate |
| agentic-web audit (hourly) | V3 | 4 | keep — reality maintenance |
| zombie_reaper (hourly) | V3 | 4 | keep — state maintenance |
| well_auto_keepalive (6h) | V3 | 4 | keep; E-axis staleness tracked separately |
| arifflow_digest (14:00) | **V2 offender** | 4 | convert: emit only state-DELTA + exceptions |
| forge-vitality-pulse (15:00) | V2 | 4 | same conversion |
| governance gc (19:00) | V3 | 4 | keep |
| phoenix72 (03:00) | V3 | 4 | keep |
| supply_chain_audit (25th) | V3 | 4 | keep — perimeter ritual |
| constitutional-sync (07:00) | V3→4 | 4 | add dirty-repo exception line |
| fomc-tripwire (weekdays) | V2 | 4 | convert to event-trigger |
| federation-triage-digest (09:00) | **V2 hub** | 4 | becomes the exception consumer (pick up governance-anomalies.jsonl) |
| google_fit_bridge (6h) | V3 | 4 | keep — E-axis ingestion |
| federation-pulse (07:47) | V2 | 4 | merge into triage consumer |
| mcp-conformance ci (06:00) | V3 | 4 | keep — verification ritual |
| fed_quota_sentinel (hourly) | **V4-native** | 4 | already state-guard — template exemplar |

## Classification — /etc/cron.d (31 units)
Bulk = V3 reality-maintenance and V4-native state guards: `entropy-governor`, `sot-cron-vault-bridge`, `vault-replica`, `arifos-sentinel-discovery`, `arifos-sovereignty-drill`, `aaa-mesh-health`, `well-dream`, `memory-helix-rollup`, `pati-sweep`, `hermes-prune`, `trading-scan`, `wealth-briefing` (V2→4), `institution-mae-pulse` (V2→4), remaining infra rituals (certbot, clamav, sysstat) keep as-is.
**UNKNOWN purpose (verify before classification):** `aaa-skill-learn`, `aaa-universe-drift`, `agent-vault`, `arif-commodity-reseal`, `zai-temporal-drift-check`, `skill-audit`, `memory-helix-rollup` — honest UNKNOWN per LAW 5.

## V4 Template (for conversions)
```bash
# 1. observe → 2. compare vs persisted state → 3. classify ROUTINE|EXCEPTION
# 4. ROUTINE: silent state update. EXCEPTION: append to governance-anomalies.jsonl + syslog WARN
# 5. Never emit information without a state transition justifying it.
```

## Staged rollout (each flip = one crontab edit, 888_HOLD, one cycle observation)
1. arifflow_digest + federation-pulse → delta-only (highest attention-leak pair)
2. triage-digest → consume governance-anomalies.jsonl
3. fomc-tripwire → event-trigger
4. wealth-briefing + institution-mae-pulse → delta-only
5. Re-verify UNKNOWN jobs, classify, iterate

DITEMPA BUKAN DIBERI
