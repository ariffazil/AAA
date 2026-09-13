# KVM8 Script-Bound Jobs — Phase-2 System-Cron Migration Plan (5.2)

> **Lane:** RECEIPT (Lane B) — plan + recon. No cron mutation executed yet.
> **Actor:** kimi-code FI-008 under F13 chat directive (option 5.2 selected — selection
> acknowledges the migration; execution still staged per plan below).
> **Forged:** 2026-09-12T15:35Z (23:35 MYT).

## 1. Recon (live, this session)

- This VPS **is KVM8** (hostname `forge`) — jobs are local, no cross-machine hop needed.
- Source of the "19 orphaned" claim: `HERMES_FLEET_MAP.md` L60 — when the 9 sovereign
  rituals migrated KVM8→KVM4 gateway book (2026-09-04, F13 "go", receipts
  20260904-001536/001732), script-bound jobs stayed in the KVM8 book with no runner.
- Live book: `/root/.hermes/cron/jobs.json` — **24 jobs** (backup `jobs.json.bak-20260912`
  exists). The 19-figure is the 2026-09-04 state; live count differs — Phase-2a re-enumerates.

## 2. Classification rubric

- **Agent-prompt jobs** (i-ARIF / Hermes persona messaging — syed-morning-brief,
  arif-market-brief, alpha-zen-morning-intel, …): these are NOT cron conversions —
  they need the Hermes gateway runtime. Out of scope for system cron.
- **Script-invocation jobs** (prompt = direct `python3`/`bash` command): the migration
  population. Preliminary from book scan: `snap-morning-01`, `snap-afternoon-02`,
  `snap-evening-03`, `skill-drift-watch`, `experience-surface-regen`,
  `capability-fitness-cycle`, `pull-openclaw-traces`, `maintenance-health-loop`,
  `session-auto-trace`, `cron-receipt-bridge` (+ remainder to be confirmed in 2a).

## 3. Migration plan (staged, F1 AMANAH — tombstone, never discard)

1. **2a — Enumerate+classify** all 24 book entries; for each: runner status (orphan vs
   KVM4-scheduled via validator adds[]), last execution (`executions.db`), dependency list.
   Output: inventory table appended to this file.
2. **2b — Pre-clearance:** read `/root/.hermes/AGENTS.md` (boundary doc) before first
   mutation in `.hermes`; confirm `flock` discipline on jobs.json (lock file present:
   `/root/.hermes/cron/.jobs.lock`).
3. **2c — Generate** `/etc/cron.d/arifos-hermes-legacy` entries: one per script-job,
   schedules lifted from book, each with `flock -n /run/lock/<job>.lock`, logging to
   `/var/log/hermes/legacy-<job>.log`, entries written COMMENTED (inactive).
4. **2d — Staged cutover:** uncomment one job at a time → observe one fire → receipt →
   next. Tombstone book entry (`"status": "MIGRATED_TO_CRON", "cron_file": "…"`) —
   never delete.
5. **2e — Verify (terminal state):** 48h watch — `/var/log/hermes/legacy-*.log` growth,
   `ticker_heartbeat`/`ticker_last_success` advance, executions.db stops growing for
   migrated ids, zero orphan alarms. Then close R-4 with evidence.

## 4. Guards

- Cron mutation = 888_HOLD class; 5.2 selection satisfies the hold for THIS plan's scope;
  any schedule CHANGES (not just porting) come back for sovereign confirm.
- `/etc/cron.d/` hygiene: 0644 root:root, no dots in filename.
- Rollback: commented entries + book tombstones make every step reversible.

## 5. Execution trigger

Ready to execute 2a–2e on explicit "go" (or sovereign re-confirm in next session).
Estimated: 2a+2c one session-hour; 2d+2e spread over 48h observation.

```
verdict_class: RECEIPT (Lane B) — plan, no mutation
r_task:        R-4 / sovereign ask 5.2
next_action:   "go" → Phase-2a enumeration
```

DITEMPA BUKAN DIBERI ⚒️
