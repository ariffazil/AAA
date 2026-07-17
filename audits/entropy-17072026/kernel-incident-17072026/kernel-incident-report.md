# INCIDENT-KERNEL-17072026-001 — arifos.service crash-restart loop

**Status:** ACTIVE at time of report (2026-07-17 ~14:30 UTC). **Authority:** Observe-only. **Mutation:** none performed.
**Host:** af-forge VPS (72.62.71.199 / tailscale af-forge). **Unit:** `arifos.service`.

## Layer diagnosis

**PROCESS_FAILURE** (primary) — confirmed. `arifos.service` main process is receiving **SIGKILL** (`status=9/KILL`, `Result=signal`) repeatedly, not exiting via unhandled exception. 18 service starts recorded since 2026-07-17 00:00 UTC; at least 9 confirmed SIGKILL events between 13:23 and 14:26 UTC, cadence accelerating from ~37 min apart to ~30-90s apart in the final 15 minutes observed. `StartLimitBurst=5` within `StartLimitIntervalUSec=1min` was hit at least once (`Failed to start arifos.service` at 14:25:50), meaning systemd's own auto-restart was at risk of giving up entirely.

**ACTOR_BINDING_DRIFT** (secondary, confirmed) — every external MCP call observed in the logs (`arif_ops_measure`, `arif_triage`, `arif_judge_deliberate`, `arif_think`) fails with `ARIF_SESSION_NOT_FOUND` because callers invoke tools without first completing `arif_init`. `wrap_legacy_call` is silently coercing `actor_id=None` to `'openclaw-anon'`, which is the "identity/authority fields: contradictory" symptom named in the incident brief.

**DEPENDENCY_FAILURE** (contributing, confirmed) — every boot attempt logs `[register] arifos: AAA rejected (503): {"ok":false,"error":"UNREACHABLE","detail":"fetch failed"}` from `register_with_aaa.py`. This is despite `aaa-a2a.service` itself answering healthy on `127.0.0.1:3001` when probed directly (`{"status":"healthy", ...}` HTTP 200) — so the failure is in the registration call path/timing, not in AAA being down. UNKNOWN: exact cause (wrong URL, race at boot, timeout too short).

**SCHEMA_DRIFT / PERMISSION** (contributing, confirmed) — every single boot logs two permission errors:
- `PermissionError: [Errno 13] Permission denied: '/root/AAA/skills/atlas333-cognitive-geometry'` (SkillsDirectoryProvider wiring fails)
- `Permission denied: '/root/secrets/did/registry.json'` (DID/challenge issuance fails — "Failed to issue challenge for FORGE")
- Two `INJECTION FAILED` lines at boot for `arif_route` and `arif_judge` (extra `_envelope`/`actor_id`/`session_id` props not matching expected handler signature — dependency-injection/schema mismatch, not fatal but degrades those tools)
- `KERNEL INTERCEPTOR: DENY for arif_ops_measure: Capability not registered in graph` (capability graph `v0.2.3` missing an entry `/contracts/tools.yaml` is supposed to supply)

None of these four are individually fatal (all are caught/logged), but together they mean the kernel comes up in a **degraded, unregistered, permission-broken state on every single boot**, which is very likely why an automated watchdog keeps deciding to kill and restart it.

**Resource exhaustion ruled out:** `free -h` shows 20Gi available / 31Gi total, swap unused. Process memory peak 175-408M against a 2G cgroup limit. `earlyoom` explicitly excludes `arifos` from its kill patterns (`--avoid ...arifos...`). Disk 42% used. Not OOM, not disk pressure.

## PROBABLE PROXIMATE CAUSE OF THE SIGKILL LOOP — flag for Arif, UNKNOWN/PLAUSIBLE

`journalctl -u ssh` shows **repeated short-lived root SSH sessions from the same source IP (202.185.89.85)**, opening roughly every 30-90 seconds during the exact window the SIGKILLs were observed (14:22:40, 14:23:12, 14:25:00→closed 1s later, 14:25:51, 14:26:39, 14:28:45, 14:29:30 — still ongoing as this report was written). This cadence closely tracks the crash cadence. No cron job or watchdog script found on the box actually issues `systemctl restart/kill` against `arifos` (`arifos-watchdog.sh` only logs to a state file; `zreaper` explicitly excludes `arifos` from its reap patterns; the crontab also references `self-heal-watchdog.sh` and `identity-drift-watchdog.sh` under `/root/A-FORGE/forge_work/` that **no longer exist on disk** — stale cron entries, separate minor finding).

**PLAUSIBLE:** something else — another automated agent/remediation loop, or a human, connecting from `202.185.89.85` — is manually restarting/killing `arifos` every time it detects the degraded-boot state described above, which then re-triggers the same degraded boot, in a loop. If that is a background AI agent session working the same incident concurrently with this one, it should be paused so the two efforts don't collide. **This needs Arif to confirm** whether `202.185.89.85` is expected activity (his own IP running something) before anyone attempts remediation.

## Chronic pre-existing condition (NOT new today)

`/var/log/arifos-watchdog.log` shows the **"ZOMBIE: systemd=active but port_8088=unbound"** and later **"UNHEALTHY: port_bound=true but health=000"** pattern recurring intermittently since at least **2026-07-16 21:25 UTC** — i.e. this instability predates the sharp escalation window observed in this report by close to 17 hours. The service has been flaky all day; today's SIGKILL storm is an acute worsening of a chronic issue, not a fresh regression.

## What was NOT done (per Lane B mandate)

- Kernel was not restarted, stopped, or reconfigured by this session.
- No file was edited on the VPS.
- No `systemctl`, `kill`, or mutation command was issued — only `status`, `show`, `journalctl`, `ss`, `curl`, `ps`, `git status`, `crontab -l`, `cat`, `who`/`w` (all read-only).
