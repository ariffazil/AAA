---
name: forge-infra-crons
description: "Infrastructure cron job management — schedule, audit, and govern VPS cron entries. Read-only observation of root crontab, /etc/crontab, and /etc/cron.d. F1 AMANAH: never mutate crontabs without 888_HOLD."
owner: A-FORGE
capability_tier: fed-long-context
ecology_state: WARM
---
> **Case-duplicate collapse (2026-09-20).** This skill was stored twice as two real
> directories differing only in case. The second copy (`/root/.hermes/skills/FORGE-infra-crons`) is now an alias
> symlink here. Its full pre-collapse body is preserved at
> `references/absorbed-FORGE-infra-crons.md` and in `.frozen/2026-09-20-case-dupes/FORGE-infra-crons/`.
# FORGE-infra-crons

Infrastructure cron governance skill. Scans and audits cron entries across the VPS.

## Capabilities
- List all cron jobs from root crontab, /etc/crontab, /etc/cron.d
- Detect orphaned or duplicate cron entries
- Verify cron entries against Machine Constitution registry

## Floors
- F1 AMANAH: Read-only by default. Mutations require 888_HOLD.
- F11 AUDITABILITY: All cron observations logged.
