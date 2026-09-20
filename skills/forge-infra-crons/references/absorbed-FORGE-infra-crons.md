<!-- absorbed by case-dupe collapse 2026-09-20 (BRIEF-v2 wave 2) -->
<!-- source dir : /root/.hermes/skills/FORGE-infra-crons -->
<!-- source file: /root/.hermes/skills/FORGE-infra-crons/SKILL.md -->
<!-- sha256     : c13939308470ff4dac15a1b9865c557aad04f4a6d227d51944cd7ff888d059f0 -->
<!-- winner     : /root/AAA/skills/forge-infra-crons -->

---
name: FORGE-infra-crons
description: 'Infrastructure cron job management — schedule, audit, and govern VPS
  cron entries. Read-only observation of root crontab, /etc/crontab, and /etc/cron.d.
  F1 AMANAH: never mutate crontabs without 888_HOLD.'
owner: A-FORGE
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
