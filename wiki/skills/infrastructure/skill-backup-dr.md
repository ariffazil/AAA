---
title: "SKILL: Backup & Disaster Recovery"
type: skill
version: 1.0.0
category: infra
risk_band: HIGH
floors: [F1]
evidence_required: true
sources: [/root/.opencode/skills/backup-dr/SKILL.md]
confidence: high
---

# SKILL: Backup & Disaster Recovery

> **⚠️ DITEMPA BUKAN DIBERI — Backups are not optional.**
> **Source:** `/root/.opencode/skills/backup-dr/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Backup operations, restore testing
- Disaster recovery planning
- Configuring offsite backups
- Cron schedule review
- Keywords: backup, restore, disaster recovery, restic, vault999, offsite, B2, DR

---

## Current Backup Schedule (2026-05-14)

| What | When | How | Where |
|------|------|-----|-------|
| vault999 (restic) | Daily 2:00 AM | Docker restic container | `/opt/arifos/backups/restic/` |
| vault999 (plain) | Weekly Sun 4:00 AM | `/usr/local/bin/vault backup` | `/var/log/vault999.log` |
| vault999 retention | Daily 3:05 AM | `restic forget --keep-daily 7` | Keeps 7 daily snapshots |
| Hermes | Daily 5:00 AM MYT | `backup-hermes.sh` | `/root/AAA/hermes-backup/` |
| AAA maintenance | Daily 9:00 PM | `daily-maintenance.sh` | `/root/AAA/scripts/` |
| SOT scan | Weekly Sun | `sot-scan.sh` | `/var/log/sot-scan.log` |

---

## ⚠️ Critical Gap: No Offsite Backup

**All backups are on the same VPS.** VPS failure = backups lost.

### Recommended: rclone to Backblaze B2 (~$6/TB/month)

```bash
# 1. Install rclone
apt install rclone

# 2. Configure Backblaze B2
rclone config

# 3. Add to crontab (weekly offsite sync)
0 6 * * 0 rclone sync /opt/arifos/backups/restic b2:arifos-vault999 --progress >> /var/log/offsite-backup.log 2>&1
```

---

## Restore Test (Monthly)

```bash
docker run --rm -v /tmp/restore-test:/restore -v /opt/arifos/backups/restic:/restic \
  -e RESTIC_PASSWORD_FILE=/restic/password-file \
  restic/restic restore latest --target /restore --repo /restic

ls -la /tmp/restore-test/
diff /root/.local/share/arifos/vault999/outcomes.jsonl /tmp/restore-test/data/outcomes.jsonl
```

---

## What to Back Up (Priority Order)

| Priority | Data | Location |
|----------|------|----------|
| 🔴 Critical | vault999 outcomes + SEALED_EVENTS | `/root/.local/share/arifos/vault999/` |
| 🔴 Critical | PostgreSQL (vault999 DB) | `docker exec postgres pg_dump` |
| 🟠 High | arifOS source (git → GitHub) | `/root/arifOS/` |
| 🟠 High | AAA workspace configs | `/root/AAA/` |
| 🟡 Medium | Docker compose files | `/root/compose/`, `/root/arifOS/deploy/` |
| 🟡 Medium | Caddy + SSL configs | `/etc/caddy/` |
| 🟢 Low | Container images (rebuildable) | GHCR |

---

## Quick Health Check

```bash
ls -lt /opt/arifos/backups/restic/data/ | head -5
ls -lt /root/AAA/hermes-backup/ | head -5

docker run --rm -v /opt/arifos/backups/restic:/restic \
  -e RESTIC_PASSWORD_FILE=/restic/password-file \
  restic/restic snapshots --repo /restic
```

---

## Related Pages

- [[skill-vault999-ops]] — VAULT999 safe operations
- [[skill-database-tuning]] — database performance
- [[skill-vps-audit]] — full system audit
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Backup verified. Offsite still needed.*
