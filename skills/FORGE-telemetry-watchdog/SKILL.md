---
name: FORGE-telemetry-watchdog
description: >
  Monitor organ telemetry freshness across the federation. Checks state.json age,
  biometric data staleness, and watchdog cron health. USE WHEN: "check telemetry",
  "WELL state stale", "vitality unknown", "watchdog status", "biometric freshness".
version: 2026.07.19
floors: [F2, F4]
risk_tier: low
autonomy_tier: T1
---
# 📡 FORGE — Telemetry Watchdog

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Monitor telemetry freshness across federation organs. Detects stale state.json, missing biometric data, and broken watchdog crons. Born from the 2026-07-19 discovery that WELL had been YELLOW/vitality=0.00 for 3+ weeks due to telemetry not being populated.

## When to Use
- Morning health probe shows vitality unknown/degraded
- WELL/WEALTH/GEOX state.json older than 12 hours
- After cron changes to verify telemetry pipeline
- As part of `make prove`

## Quick Check
```bash
# WELL state freshness
cat /root/WELL/state.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'freshness: {d.get(\"freshness\")}, truth: {d.get(\"truth_status\")}, telemetry: {d.get(\"telemetry_confidence\")}')"

# WELL cron status
crontab -l | grep -i well
ls /etc/cron.d/*well* 2>/dev/null

# Run keepalive (refreshes timestamps, does NOT invent vitals)
cd /root/WELL && python3 scripts/well_auto_keepalive.py
```

## Telemetry Sources
| Organ | Cron | Script | Frequency |
|-------|------|--------|-----------|
| WELL | `0 */6 * * *` | `well_auto_keepalive.py` | Every 6h |
| WELL | `0 */6 * * *` | `google_fit_bridge.py` | Every 6h |
| WELL | `/etc/cron.d/well-dream` | dream engine | System cron |

## Known Issue: QUARANTINE State
When state.json shows `"truth_status": "INSUFFICIENT_DATA"` and `"telemetry_confidence": "NONE"`:
- This means biometric data was quarantined (test/mock separation)
- Keepalive script refreshes timestamps but does NOT invent vitals
- **Fix:** Arif must inject fresh biometrics via WELL UI or sovereign command
- The `state.test.json` file contains quarantined test data

**SOT:** 2026-07-19 · **seal_seq:** 4
