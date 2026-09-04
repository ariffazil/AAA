# Scheduler — Retired / Reconciled Entries
> Archived: 2026-09-04T21:45+08:00 by FI-008 (kimi-code) — 888 sovereign "go" on cron-zen-audit
> Reason: Cooldown-debt triage (13 jobs paused since ~Aug 24–27, never revisited); duplicate schedules consolidated; SOT reconciled to live reality; zombie cron removed.
> Restore: `/root/BACKUPS/cron-audit-20260904/` (root.crontab.bak, ariffazil.crontab.bak, etc-cron.d/*, scheduler_obligations_sot.yaml.bak, removed-paused-lines.txt, status.json.bak)
> Full audit + evidence: `/root/forge_work/cron-zen-audit-20260904/AUDIT.md`

## Retired from root crontab (12 lines; full text: removed-paused-lines.txt)
| Job | Was | Why retired |
|---|---|---|
| qwen-free-quota-probe.sh | */15 | superseded by fq-probe.timer |
| fq-probe.sh | */15 | superseded by fq-probe.timer |
| metabolism_cron_wrapper.sh | */30 | metabolism plane now arifFlow daemon (:7073) |
| asi-pulse.sh | */30 | superseded by mesh-health + drift-detector |
| sync-cockpit-static.sh | */5 | no live consumer found |
| claude-code-verify-flusher.sh | */5 | no live consumer found |
| m6-collect.sh | */5 | superseded by well-machine-telemetry.timer |
| gotong-royong qwen -p | 6h | LLM-in-cron, expensive, superseded |
| gotong-royong claude -p | 4h | LLM-in-cron, expensive, superseded |
| gotong-royong codex -p | 8h | LLM-in-cron, expensive, superseded |
| metabolize_cron.py | */30 | superseded by arifFlow FQ |
| "FI Gotong Royong" header | — | context of removed jobs |

## Disabled in place (tagged, rollback = uncomment)
- root crontab `0 18 direct-backup.sh` — duplicate of arifos-backup.timer 04:30 (service verified OK 2026-09-04)

## Removed entirely
- `ariffazil` user crontab: `arif_cron_deploy.sh` — **113 Permission-denied fires/24h since 2026-05-23**; script deleted; user cannot read /root

## /etc/cron.d
- `federation-backup.daily` retired — log silent since Aug 10; superseded by GOV-A002 + vault999-backup.timer + arifos-backup.timer
- `well-dream` (4 lines) FIXED not retired: log redirect `/var/log/` (unwritable by user arifos → 3 months of silent failures) → `/var/lib/arifos/well_dream/logs/` (writability + py_compile verified)

## systemd
- `arifflow-fq-mirror.timer` disabled — once-per-boot ghost (OnBootSec only) duplicating fq-probe.timer

## SOT reconciliation (scheduler_obligations_sot.yaml → rendered 2026-09-04)
- **GOV-A003 RESUMED** (external witness probe, F3 floor) — was PAUSED_COOLDOWN
- GOV-A005 RETIRED — script dir deleted by forge_work GC; 0 fires since Aug 28
- GOV-A007 SUSPENDED — completion-contract gate parked pending F13 decision (unit stays on disk, not enabled)
- GOV-A008 cadence `*:0/5` → `hourly` (match live ratified timer)
- GOV-A009 cadence `*:0/15` → `hourly`; exec path `/root/HERMES/...` → `/root/scripts/zen/...` (HERMES moved to KVM4; old path gone)

## Other fixes
- `federation-triage-digest` cron: now sources `kunci-root.env` (GITHUB_TOKEN absent in cron env → silent death since Aug 25; manual run writes digest fine)
- `federation_pulse.sh` rehomed `forge_work/` → `/root/A-FORGE/duties/federation-pulse.sh` (GC would have deleted it in ≤7 days)

## Public artifacts
- `/var/www/html/status.json` removed — stale since 2026-08-18 (generator in .hermes-cron-ban-20260904); AGENTS.md discovery table still references it (holds.txt flagged)
