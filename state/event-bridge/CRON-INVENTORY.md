# AAA Event Bridge — Cron Inventory & Event Schema
# Updated: 2026-09-14

## Event Schema (FORGE Protocol)

Every post to AAA group follows this format:

```
FORGE | <severity> | <event_type>
event: evt_<YYYYMMDD>_<HHMM>_<hash8>
scope: node
host: <host_id>
source: <source_name>
dedupe: <sha256_16>
time: <ISO-8601 UTC>
verdict: NEW|ESCALATED|ACTIONED|VERIFIED|RESOLVED|SEALED|HOLD

<structured_content>
```

### Severity Levels
- **P0** — interrupt: Security, data-loss, sovereignty, production outage
- **P1** — execution receipt: A system action changed verified state
- **P2** — intelligence digest: Important trend or governance context
- **P3** — telemetry: Routine measurements (LOGS ONLY, never Telegram)

### Event Types
- **DETECTED** — new condition observed (P0/P1)
- **VERIFIED** — health/state restored after action
- **SEALED** — scar or constitution update committed
- **STATE_CHANGED** — material delta in monitored metric
- **888_HOLD** — human authorization required

### Dedup
Event ID = `evt_<timestamp>_<content_hash_8>`
Content hash = `sha256(content)` truncated to 16 chars
Delta gate: posts only when content hash differs from last posted hash

## Cron Inventory — Active Event Bridges

| Source | Cron | Bridge | Severity | Condition | Posts to AAA |
|--------|------|--------|----------|-----------|-------------|
| drift_scanner | 02:00 | scanner-event.sh | P1 | DRIFT_DETECTED | ✅ (delta-gated) |
| federation_pulse | 07:47 | pulse-event.sh | P2 | material delta | ✅ (delta-gated) |
| triage_digest | 09:00 | triage-event.sh | P1 | aged/blocking items | ✅ (delta-gated) |
| vitality_pulse | 15:00 | vitality-event.sh | P2 | vitality changed or unresolved | ✅ (delta-gated) |
| arifflow_digest | 22:00 | flow-event.sh | P1 | GOVERNANCE_COLLAPSE/HOLD | ✅ (delta-gated) |
| weekly_digest | Sun 22:00 | weekly-digest.sh | P2 | always (weekly summary) | ✅ |

## Cron Inventory — Silent (P3, logs only)

| Source | Schedule | Purpose |
|--------|----------|---------|
| cockpit_probe | */15min | Federation status JSON |
| unsealed-counter | */30min | VAULT999 unsealed count |
| well_ingest | */30min | WELL intake |
| observatory_snapshot | */30min | Public state |
| zombie_reaper | hourly | Process cleanup |
| mvm_fire | hourly | MVM fire check |
| fed_quota_sentinel | hourly | FED quota |
| fed_route_weights | hourly | FED route weights |
| fed_retirement_watcher | */6h | Model retirement |
| phoenix72 | 03:00 | Phoenix recovery |
| supply_chain_audit | monthly | Supply chain |
| ci_conformance | 06:00 | MCP conformance |
| constitutional_sync | 07:00 | Constitution sync |
| fomc_tripwire | 08:00 weekdays | FOMC trigger |
| vault999_backup | 03:00 | VAULT999 backup |
| repo_audit | Mon 01:00 | Repo audit |
| self_healing_cycle | */30min | Heartbeat test |
| sentinel_discovery | 02:30 | Sentinel audit |
| sovereignty_drill | Sun 02:00 | Sovereignty drill |
| mesh_health_probe | 03:17 | Mesh health |
| skill_learn_ingest | hourly | Skill learning |
| universe_drift_sentinel | hourly | Universe drift |
| backup_rotation | 02:30 | Backup rotation |
| entropy_governor | 19:00 | Entropy governance |
| memory_helix | */6h | Memory helix |
| hermes_prune | Sat 19:17 | Hermes cleanup |
| skill_extract | */6h | Skill extraction |
| kabarkan_publish | */6h | OTEL publish |
| memory_helix_rollup | 19:00 | Memory rollup |
| musyawarah_sentinel | */15min | Musyawarah check |
| pati_sweep | Sat 18:00 | Pati sweep |
| skill_audit | Sat 20:00 | Skill audit |
| vault_replica | */6h | Vault replication |
| wealth_briefing | 06:00 | Wealth briefing |
| well_dream | 20:00 | Well dream |
| zai_temporal_drift | 18:00 | Z.AI drift check |
| cron_failure_autopause | */15min | Cron failure |
| trading_scan | — | Trading scan |
| sro_expiry | 03:00 | SRO expiry check |
| sro_calibration | Mon 04:00 | SRO calibration |
| receipt-reality-correlator | daily 07:45 | Receipt↔reality gap record — claimed vs predicted vs verified vs observed (T0, F13 2026-09-25) |
| contradiction-accumulator | daily 08:15 | Contradiction economics ledger — CHRON tensions → half-life dormancy + priority (blindspot #6, F13 2026-09-25) |
| governance-hotspot-detector | daily 08:45 | Governance friction concentration — floor Holds / cooling Holds / RG-4 events by actor-organ-day (blindspot #5, F13 2026-09-25) |
| governance-drift-batch | daily 09:15 | Slow-drift batch — #1 authority-drift (seal discipline + identity fragmentation) · #2 registry attestation · #7 SPOF index · #8 scar attestation (F13 2026-09-25) |

## Event Log Location
`/root/AAA/state/event-bridge/events.jsonl`

## State Files
`/root/AAA/state/event-bridge/<source>.last_hash` — delta gate hash
`/root/AAA/state/event-bridge/bridge.log` — bridge execution log

## Rollback
To disable event bridges:
```bash
crontab -l | grep -v "event-bridge\|event\.sh\|weekly-digest" | crontab -
```
