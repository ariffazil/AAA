# Missed Morning-Brief — 2026-08-06 Case Study

## Symptom

User reported: "why no chron daily briefing?" at 11:21 MYT Thursday Aug 6 2026.

- Job `morning-brief` (`4b2d9690c7d9`) — schedule `0 7 * * *`, `no_agent: true`
- `last_run_at: 2026-08-05T07:00:16+08:00` (yesterday) — `last_status: ok`
- `next_run_at: 2026-08-06T07:00:00+00:00` — but NO file for Aug 6 in `output/4b2d9690c7d9/`

## Root cause: gateway outage window

Gateway restart log (`profiles/aaa-hermes/logs/gateway.log`):
```
2026-08-05 15:38:38,348 INFO gateway.run: Starting Hermes Gateway...
2026-08-06 02:29:40,709 INFO gateway.run: Starting Hermes Gateway...   ← 11h gap
```

Gap window: Aug 5 23:38 MYT → Aug 6 10:29 MYT.
Morning-brief fire time: 07:00 MYT (within gap).
→ Job did not fire. No error, no catch-up.

Preceding symptom (15:30+ MYT Aug 5): repeated `Gateway drain timed out after 0.0s with N active agent(s)` warnings — the gateway was struggling with active agent contention before crashing.

## Diagnostic steps that worked (the recipe)

1. `ls -la /root/HERMES/cron/output/4b2d9690c7d9/` — last file `2026-08-05_07-00-15.md`, none for Aug 6
2. `stat /root/HERMES/cron/ticker_heartbeat` — recent (ticker alive but in fresh process)
3. `awk '/Starting Hermes Gateway/{print $1,$2}' .../gateway.log | tail -5` — found the 11h gap
4. Confirmed Aug 6 was inside the gap window

Total investigation: ~10 tool calls, no orchestration.

## Recovery

Ran script manually: `bash /root/HERMES/scripts/morning-brief.sh`
Output: kernel SEAL, all 8 organs ✅, vitality PROCEED, 49 pending items, 1 priority (AAA 71 dirty files).

## Lessons

1. **The ticker heartbeat is NOT proof of recent fires.** It updates when the ticker process runs, even if no jobs were due. Always check output dirs for the expected date.
2. **No catch-up for missed fires.** Restart doesn't replay past schedules.
3. **Gateway uptime IS the cron uptime** for any job that depends on the ticker. A systemd restart creates a gap.
4. **The drain-timeout pattern before a crash** is a leading indicator — repeated `drain timed out after 0.0s with N active agents` warnings preceded this outage. Worth a separate watchdog.

## Open follow-ups (not yet actioned)

- Drain-timeout watchdog skill/cron — emit alert when N+ drain timeouts in M minutes
- "Why no brief" pre-bake into morning-brief.sh itself — self-heal check on startup
- Sequence the `overnight quiet hours` end (07:00 MYT) with the first scheduled cron so a slow gateway boot can't miss it

## Cross-references

- `references/config-path-liveness-2026-08-06.md` — the same outage revealed Hermes gateway's config-load-path trap (edits to `/root/HERMES/` don't affect running service that reads `/usr/local/lib/hermes-agent/`). Both findings share the same root: service restart creates gaps, edits at wrong path create illusions of effect.