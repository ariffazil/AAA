---
name: FORGE-infra-crons
id: forge-infra-crons
version: 1.0.0
risk_tier: low
floor_scope: [F1, F2, F4, F7]
description: 'Infrastructure cron job management — schedule, audit, and govern VPS
  cron entries. Read-only observation of root crontab, /etc/crontab, and /etc/cron.d.
  F1 AMANAH: never mutate crontabs without 888_HOLD.'
owner: A-FORGE
autonomy_tier: T2
---
# FORGE-infra-crons

Infrastructure cron governance skill. Scans and audits cron entries across the VPS.

## Capabilities
- List all cron jobs from root crontab, /etc/crontab, /etc/cron.d
- Detect orphaned or duplicate cron entries
- Verify cron entries against Machine Constitution registry

## Floors
- F1 AMANAH: Read-only by default. Mutations require 888_HOLD.
- F11 AUDITABILITY: All cron observations logged.
