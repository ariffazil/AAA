# CHRON cron layers — the actual topology

CHRON runs across **four independent cron layers** on the federation host. A report that only
checked one of them is wrong by construction. The layers differ in:

- **where they live** (config file vs. system crontab vs. /etc/cron.d vs. systemd unit)
- **how they are wired** (jobs.json is hermes-managed; /etc/cron.d is hand-edited; systemd is
  declared in /etc/systemd/system)
- **what runs them** (hermes cron dispatcher vs. cron daemon vs. systemd --user)
- **what gates them** (no guard; jitu-guard <lane>; systemd's own security)

| Layer | Path | Wrapper | Sample jobs |
|---|---|---|---|
| `jobs.json` (hermes) | `/root/HERMES/cron/jobs.json` | hermes cron dispatcher | ALPHA-ZEN 1/2/3, SADO PERSONAL Morning/Night, docforge-edition-daily, sentinel-tripwire, VPS Backup |
| System crontab | `crontab -l` (root) | bare shell | legacy / one-off jobs |
| `/etc/cron.d/chron*` | `/etc/cron.d/chron-bl02-calibration`, `/etc/cron.d/chron-bridge-flow` | `jitu-guard <lane> && python3 <script>` | bl02 calibration (04:20), bridge_flow (*/5 min) |
| systemd timers | `chron-{reconciliation,prediction-verifier,loop-closer,edge-midday,reality-impact-attestor}.timer` | `ExecStart=/usr/bin/python3 <script>` with `PYTHONPATH=/root` | reconciliation 06:50, verifier 07:00, loop-closer 07:15, edge-midday 12:30, reality-impact-attestor 09:45 |

## Liveness check (canonical, all four)

```bash
# 1) jobs.json — hermes-managed
python3 -c "import json; d=json.load(open('/root/HERMES/cron/jobs.json')); \
  chron=[j for j in d['jobs'] if 'chron' in (j.get('name','') or '').lower()]; \
  print(f'jobs.json: {len(chron)} chron jobs')"

# 2) System crontab
crontab -l 2>/dev/null | grep -iE 'chron|temporal' || echo 'crontab: none'

# 3) /etc/cron.d/
ls /etc/cron.d/ 2>/dev/null | grep -iE '^chron' || echo 'cron.d: none'

# 4) systemd timers
systemctl list-timers --all 2>/dev/null | grep -iE 'chron' || echo 'timers: none'

# 5) Data freshness (real liveness)
for f in /root/chron/data/{episodes,predictions,lessons,calibration,verification_log}.jsonl; do
  [ -f "$f" ] && stat --format='%n  %y  %s bytes' "$f" | head -c 200
  echo
done
```

A CHRON system is **healthy** when all five data files are present, `calibration.json` is < 6 hours
old, and at least one of the layers shows a recent trigger in `journalctl` / log file.

## What runs on what (real schedule, observed)

| Time MYT | Layer | What | Service / script |
|---|---|---|---|
| */5 min | /etc/cron.d/chron-bridge-flow | episode ingest (NATS → chron episodes store) | `bridge_flow.py` |
| 02:00 daily | jobs.json (`cf8cf0f12f0c`) | VPS backup to gdrive | `vps-gdrive-backup-check.sh` |
| 04:20 daily | /etc/cron.d/chron-bl02-calibration | BL02 calibration curves | `bl02_calibration_curves.py` |
| 06:00 daily | jobs.json (`a77681618199`) | docforge daily edition (sovereign PDF brief) | agent |
| 06:23 daily | system crontab | chron-verify-sweep | `chron_verify_sweep.py` |
| 06:50 daily | systemd timer | chron-task0-reconciliation | `chron_task0_reconciliation` |
| 07:00 daily | systemd timer | chron-prediction-verifier | `chron_prediction_verifier` |
| 07:15 daily | systemd timer | chron-loop-closer (metabolic cycle) | `chron_loop_close` |
| 07:15 daily | jobs.json (`8313453a73a7`) | ALPHA-ZEN 1 (morning pulse) | agent |
| 09:30 daily | jobs.json (`b432b9a25b10`) | SADO PERSONAL Morning Fire | agent |
| 09:45 daily | systemd timer | chron-reality-impact-attestor | `cria` |
| 12:30 daily | systemd timer | chron-edge-midday | `edge_midday.py` |
| 14:00 daily | jobs.json (`3e40c50f0ca2`) | ALPHA-ZEN 2 (body check) | agent |
| 15:30 daily | system crontab | chron-verify-due | `verify_due.py` |
| 20:00 / 08:00 | jobs.json (`b1ee87971b9f`) | sentinel-tripwire | agent |
| 21:15 daily | jobs.json (`161c0d5e0d0c`) | ALPHA-ZEN 3 (zen signal) | agent |
| 21:30 daily | jobs.json (`cb22fd1b1c74`) | SADO PERSONAL Night Truth | agent |

## What goes wrong by layer

- **jobs.json** — `last_status: unknown` + `last_error: Scheduler restarted after this
  execution's owner exited before a durable terminal state` means the hermes cron dispatcher
  itself restarted mid-tick. Worker died in 1 second. Check `ticker_heartbeat` freshness and
  systemd status of `hermes-gateway`. Often a config-rotation race; rolling back to the
  pre-rotation `jobs.json.bak-...` recovers immediately.
- **system crontab** — output goes to `/var/log/arifos/*.log` (one file per cron). Empty file
  plus a 0-byte output means the python module failed to import; check the file's first 5
  lines for `ModuleNotFoundError`.
- **/etc/cron.d/chron*** — output to the same `/var/log/arifos/*.log`. Jitu-guard failures log
  the policy lane refused and a non-zero exit; the script then never runs. The `&&` is
  load-bearing: a bare `python3 <script>` invocation bypasses the gate.
- **systemd timers** — `LastTriggerUSecRealtime` is the canonical liveness field. The service
  unit itself reads `inactive` between fires (timer+oneshot pattern); do not call this "down".
  `journalctl -u <svc> --since '7 days ago'` is the witness log.

## Adding a new CHRON cron — decision tree

```
Is the schedule F13-class?  (constitutional, irreversible, money)
  -> HOLD, write proposal to /root/AAA/cockpit/proposals/, wait for binary

Does the cron emit output the principal reads? (e.g. a daily PDF brief)
  -> jobs.json (hermes manages delivery, has failure_streak, integrates with home channel)

Does the cron maintain a state store? (episodes / lessons / calibration)
  -> /etc/cron.d/chron-<lane> with jitu-guard wrapper (lowest-overhead, no hermes dependency)

Does the cron need precise-schedule fires (every 5 min / every 30 sec)?
  -> systemd timer (better than cron for high-frequency; persists across reboots)
```

The same script can be invoked manually for testing:
`jitu-guard <lane> && /usr/bin/python3 <script>`.
The wrapper is not optional; it carries the policy gate that defines what the cron is allowed
to do, and bypassing it for "just this once" turns a recoverable cron into a side channel.
