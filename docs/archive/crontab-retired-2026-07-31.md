# Root Crontab — Retired Entries
> Archived: 2026-07-31T16:01:21Z
> Reason: 55% dead code. P1 entropy cleanup per APEX Cron Zen audit.
> Restore: backup at /tmp/root-crontab-backup-2026-07-31.txt

## Retired (42 lines)

```

# === FORGE AUTONOMOUS DUTIES (2026-07-12) ===
# Duty 1: Drift Scanner — 10:00 MYT (02:00 UTC) — silent when clean
# Duty 2: Constitutional Sync — 15:00 MYT (07:00 UTC)
# Duty 3: Vitality Pulse — 23:00 MYT (15:00 UTC)

# === XAUUSD DAILY BRIEFING (Phase 1) ===
# 8am MYT (00:00 UTC) — before London open
# DEAD — trading stack not deployed (2026-07-29 audit)
# 0 0 * * * /root/trading/bin/python3 /root/trading/scripts/daily_scan.py >> /root/trading/logs/daily_scan.log 2>&1

# === HERMES HOURLY MARKET SCAN — XAUUSD (Phase 2) ===
# DEAD — trading stack not deployed (2026-07-29 audit)
# 0 * * * 1-5 /root/trading/cron/hourly_scan.py >> /root/trading/logs/hourly_scan.log 2>&1
# Federation backup — daily 06:00 UTC (14:00 MYT), 7-day retention, silent-on-green

# ZEN SYNTHESIS PIPELINES (2026-07-20)
# VAULT999 Weekly Chronicle — daily 6am MYT (10pm UTC)
# DEAD — script missing (2026-07-29 audit)
# 0 22 * * * /usr/bin/python3 /root/AAA/scripts/chronicle_vault999.py >> /root/AAA/logs/chronicle.log 2>&1
# Federation Health Narrative — every 4 hours
# DEAD — script missing (2026-07-29 audit)
# 0 */4 * * * /usr/bin/python3 /root/AAA/scripts/health_narrative.py >> /root/AAA/logs/health.log 2>&1
# Memory Continuity Bridge — every 6 hours
# DEAD — script missing (2026-07-29 audit)
# 0 */6 * * * /usr/bin/python3 /root/AAA/scripts/memory_bridge.py >> /root/AAA/logs/bridge.log 2>&1
# REMOVED 2026-07-27 (888 auth): hourly self-curl no-op (Caddy served /briefing from the same file it overwrote)

# === EXTERNAL WITNESS (2026-07-20) ===
# Daily 09:00 MYT (01:00 UTC) external HTTPS probe — independent of the kernel

# === BRIEFING REFRESH (2026-07-20) — 4×/day for A3 pipe consistency ===
# MYT: 02:00, 08:00, 14:00, 20:00 → UTC: 18:00, 00:00, 06:00, 12:00
# DISABLED 2026-07-27 (888 auth): dormant 2nd generator, never logged output, writes incompatible schema to latest.json. Canonical generator: /etc/cron.d/wealth-briefing
# 0 0,6,12,18 * * * cd /root/WEALTH && set -a && source /root/.secrets/vault.env && set +a && python3 internal/ingest/refresh_briefing.py >> /var/log/wealth-briefing-refresh.log 2>&1
# FQ autonomous probe — every 15 min (sensor redundancy, independent of OpenClaw)
# === WEALTH RENDER WATCHDOG (2026-07-27, 888 auth) ===
# FOMC tripwire — 17:30 UTC daily; activates only on 2026-07-31
# arifOS model registry auto-probe — weekly Monday 06:00 UTC
# FED Router: Track A balance probe — daily 00:00 UTC
# N9 PRN 2026 Live Telemetry — refresh every 15 min, offset :07 (avoid :00/:15/:30/:45 herd)

```
