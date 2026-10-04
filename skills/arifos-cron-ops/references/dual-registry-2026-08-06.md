# Dual Cron Registry — Discovery Log 2026-08-06

The single biggest cron knowledge gap on arifOS. Two separate `jobs.json` files, two separate schedulers, two separate output dirs. Documented after a session where the agent was about to edit the wrong file.

## The two registries

### Gateway registry (canonical, what `cronjob` tool manages)
- **Path:** `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json`
- **Resolved from:** `HERMES_HOME=/usr/local/lib/hermes-agent` + active profile = `aaa-hermes`
- **Manager:** `cronjob` tool (this session), `hermes cron` CLI, `/cron` slash command
- **Fired by:** Gateway scheduler inside `hermes gateway run` — ticks every 60s
- **Output dir:** `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/<job_id>/`
- **Heartbeat file:** `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/ticker_heartbeat`
- **Live job count (2026-08-06):** 5 (the deployed blueprints)
- **Validation tool:** None — `cronjob` tool validates on create/update

### Legacy registry (arifOS custom, mystery scheduler)
- **Path:** `/root/HERMES/cron/jobs.json`
- **Manager:** Unknown — likely an OpenClaw or arifOS-specific scheduler, possibly dead
- **Fired by:** Cannot identify the PID that reads this file. The `ticker_heartbeat` at `/root/HERMES/cron/ticker_heartbeat` does update (last seen 03:37 MYT), but no process appears in `lsof` or `ps` for it.
- **Output dir:** `/root/HERMES/cron/output/<job_id>/` — entries dated today prove something fires it (Reality Snapshot, Watchdog of Watchdogs, Federation Health all wrote at 03:00 UTC)
- **Backup files:** `/root/HERMES/cron/jobs.json.bak-*` (12+ backups, suggesting active edits)
- **Live job count (2026-08-06):** 20 (legacy federation jobs)
- **Validation tool:** `/root/HERMES/scripts/zen/validate_jobs_json.py` (check/apply)

## How the confusion manifested

### Incident 1: Reading the wrong jobs.json
- Read `/root/HERMES/cron/jobs.json` (legacy) → 20 jobs, 13 at `last_status=?`
- Ran `cronjob(action='list')` → 0 jobs
- Concluded "the jobs are dead, nothing fires"
- Reality: the 13 `?`-status jobs were created by a prior sibling agent via direct file-write to legacy registry, never persisted to gateway registry, and the unknown scheduler fired them anyway (or some of them; can't tell)

### Incident 2: Editing the wrong jobs.json
- Started writing patch file for `/root/HERMES/cron/jobs.json`
- If I had written, the 5 new blueprints would have been invisible to `cronjob` tool
- Switched to `cronjob` tool → wrote to gateway registry → end-to-end verified via `cronjob(action='run')` + Telegram `getUpdates`/manual probe

### Incident 3: Sibling's "Telegram env empty" claim
- Sibling agent (separate process) grepped `kunci-mas.env` for `TELEGRAM_*` → empty
- Proposed adding `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID_ARIF`, etc.
- Reality: `ASI_BOT_TOKEN` line 292 is the active token, with aliases `HERMES_TELEGRAM_BOT_TOKEN`, `ASI_ARIFOS_BOT_TOKEN`, `AGI_ASI_BOT_TOKEN`, `HERMESARIFOS_BOT_TOKEN`
- Verified live: `getMe` returns `@ASI_arifos_bot` with status ok

## Why the dual registry exists (best guess)

Legacy pre-dates the Hermes gateway cron subsystem. arifOS built its own cron infrastructure on top of `systemd` + bash scripts + a custom jobs.json. When Hermes added its gateway cron feature, it created a parallel registry. Both kept running because:
1. Migrating the 20 legacy jobs to gateway registry is non-trivial (need to map providers, deliverables, scripts to the new schema)
2. The legacy jobs include `no_agent: true` script-only jobs (e.g. STEEL, morning-brief.sh) that don't fit cleanly into the gateway's prompt-based model
3. The legacy scheduler still works (its jobs continue to fire — proven by today's output files)

## The operational rule (this is what next session needs to know)

**For new cron jobs that fire to Arif's Telegram DM:**
1. Use `cronjob` tool with `deliver: "telegram:267378578"` and `model: null`
2. Job will live in gateway registry and fire reliably
3. Verify end-to-end with `cronjob(action='run')` + Telegram probe

**For legacy jobs that need repair:**
1. Edit `/root/HERMES/cron/jobs.json` via `write_file` + `validate_jobs_json.py check`
2. Don't migrate to gateway registry unless the job's contract demands it

**For auditing what actually fires:**
1. Check BOTH registries' output dirs for today's files
2. `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/` = gateway
3. `/root/HERMES/cron/output/` = legacy
4. The job counts in output dirs prove fires, regardless of which scheduler did it

## Source

Discovered 2026-08-06 during `cron revamp` session. Verified via:
- `cronjob list` returns 0 in fresh session
- `cronjob create` writes to `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/jobs.json`
- `find / -name jobs.json` returns both paths
- `lsof /root/HERMES/cron/jobs.json` returns nothing
- Output files in both `/root/HERMES/cron/output/` and `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cron/output/` prove both registries fire