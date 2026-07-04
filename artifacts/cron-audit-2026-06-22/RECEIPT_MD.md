# Hermes Cron Audit — 2026-06-22

**Operator:** Hermes (sovereign relay) per Arif directive
**Directive:** "map all my hermes asi chron task. chron task audit and improvement. max 3 chron task daily and 1 weekly. all human related. not code cot machine."
**Scope:** T1 reversible — backup created at `~/.hermes/cron/jobs.json.bak-2026-06-22-cron-audit`

---

## Before State — 10 jobs

| # | Job | Schedule (UTC) | MYT | Status | Layer |
|---|-----|----------------|-----|--------|-------|
| 1 | Hermes Pagi Brief | 0 23 * * * | 07:00 daily | ok | HUMAN |
| 2 | Hermes Malam Brief | 0 14 * * * | 22:00 daily | ok | HUMAN |
| 3 | Hermes Event Radar | 0 10 * * 5 | Fri 18:00 weekly | ok | HUMAN |
| 4 | Hermes Vitality Check-in | 0 0,12 * * * | 08:00 + 20:00 daily | error (402) | HUMAN |
| 5 | l3-feed | 0 */6 * * * | every 6h | ok | MACHINE (memory pipeline) |
| 6 | Pagi → WEALTH Site Publish | 0 0 * * * | 08:00 daily | error (402) | MACHINE (publish) |
| 7 | WELL Autonomous Sleep Detection | 0 23,11 * * * | 07:00 + 19:00 daily | ok | MACHINE (sleep detect) |
| 8 | peer-probe-monitor | */5 * * * * | every 5 min | ok | MACHINE (A2A probe) |
| 9 | Hermes Health Probe | 0 * * * * | every hour | error (402) | MACHINE (health) |
| 10 | GitHub PR Watcher | 0 */4 * * * | every 4h | error (402) | MACHINE (code) |

**Layer breakdown:** 4 HUMAN, 6 MACHINE.
**HTTP 402 errors:** 4 jobs (DeepSeek billing exhausted — independent problem, fix billing separately).

---

## After State — 4 jobs

| # | Job | Schedule (UTC) | MYT | Cadence | Layer |
|---|-----|----------------|-----|---------|-------|
| 1 | Hermes Pagi Brief | 0 23 * * * | 07:00 daily | daily | HUMAN |
| 2 | Hermes Vitality Check-in | 0 6 * * * | 14:00 daily | daily (reduced from 2x) | HUMAN |
| 3 | Hermes Malam Brief | 0 14 * * * | 22:00 daily | daily | HUMAN |
| 4 | Hermes Event Radar | 0 10 * * 5 | Fri 18:00 weekly | weekly | HUMAN |

**Cadence:** 3 daily + 1 weekly. ✅ Arif directive satisfied.
**All human-life layer.** ✅ No code/machine cron in Hermes.
**Vitality Check-in: reduced from 2x/day (08:00+20:00 MYT) to 1x/day (14:00 MYT).** Reasoning: Pagi (07:00) and Malam (22:00) already cover rhythm boundaries; midday check catches the middle gap. Reduces noise + saves 1 daily cron slot.

---

## Removed Jobs (6) — Migration Path

These are infrastructure concerns, not Hermes agent concerns. Migrate to systemd timers.

| Job | Original Schedule | Why in Hermes cron | Migration target |
|-----|-------------------|-------------------|------------------|
| l3-feed | every 6h | Memory pipeline (L1→L3 vector store ingestion) | systemd timer (`/etc/systemd/system/hermes-l3-feed.timer`) |
| Pagi → WEALTH Site Publish | 08:00 daily | Static site publisher (data pipeline) | systemd timer (`/etc/systemd/system/wealth-site-publish.timer`) |
| WELL Autonomous Sleep Detection | 07:00 + 19:00 daily | Sleep state autosleeper | systemd timer (`/etc/systemd/system/well-autosleeper.timer`) |
| peer-probe-monitor | every 5 min | A2A mesh health probe | systemd timer (`/etc/systemd/system/aaa-peer-probe.timer`) — or fold into aaa-a2a service's own health loop |
| Hermes Health Probe | hourly | Federation organ health | systemd timer (`/etc/systemd/system/hermes-health-probe.timer`) — or fold into hermes-asi-gateway service |
| GitHub PR Watcher | every 4h | PR inbox watcher | systemd timer (`/etc/systemd/system/github-pr-watcher.timer`) |

**Note:** These migrations are NOT done in this turn. They are flagged for a future forge cycle that needs Arif ratification (each migration = at least one systemd unit file change = T2).

---

## Skill Bindings (Verified)

Each kept job's skill IS bound:

| Job | Skill | Card Citizen | Binding Status |
|-----|-------|--------------|----------------|
| Hermes Pagi Brief | briefing-system | hermes-asi ✓ (card declared) | LEASED |
| Hermes Malam Brief | briefing-system | hermes-asi ✓ | LEASED |
| Hermes Vitality Check-in | vitality-check-cron | hermes-asi ✓ | LEASED |
| Hermes Event Radar | event-calendar-research | hermes-asi ✓ | LEASED |

All 4 bound skills now appear in the patched hermes-asi agent-card.json (from earlier session work).

---

## Open Issues (NOT in scope of this audit, flagged for follow-up)

1. **DeepSeek HTTP 402** — Vitality Check-in, WEALTH Publish, Health Probe, PR Watcher all fail. Root cause: DeepSeek account balance exhausted. Fix by topping up DeepSeek credits at https://platform.deepseek.com/ — independent task.
2. **peer-probe-monitor every 5 min** — was creating log noise. After migration to systemd, set log level appropriately.
3. **l3-feed wrap script** — backup at ~/.hermes/scripts/l3-feed-wrap.sh should be inspected before systemd migration to ensure script semantics preserved.

---

## Files Modified

- `~/.hermes/cron/jobs.json` — removed 6 machine jobs, adjusted Vitality schedule, added `audit` block + per-job `audit_note`
- `~/.hermes/cron/jobs.json.bak-2026-06-22-cron-audit` — backup of original 10-job state

## Files Created

- `/root/AAA/artifacts/cron-audit-2026-06-22/RECEIPT_MD.md` — this file

---

## Receipt

T0: Verified 10 cron jobs in `/root/.hermes/cron/jobs.json`. 4 human-life + 6 machine/infra.
T1: Classified each by layer. Proposed 3 daily + 1 weekly.
T2: Arif approved Option A (recommended). Executed:
  - 6 machine jobs removed (migrate to systemd in future cycle)
  - Vitality reduced to 1x/day at 14:00 MYT
  - Pagi/Malam/Event Radar unchanged
  - Backup saved at jobs.json.bak-2026-06-22-cron-audit
State: jobs.json now has 4 jobs. hermes-asi-gateway service restart still pending (Arif ratify).

DITEMPA BUKAN DIBERI — 10 → 4 cron jobs. Human-life layer only. Federation sovereignty intact.