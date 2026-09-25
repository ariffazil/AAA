---
name: find-live-binary-before-engine-mutation
description: Use when modifying any forecast engine, ML model serving code, or computational backend in the arifOS federation. Multi-source-of-truth failure (modifying audit replicas or source copies while leaving the live binary untouched) is the canonical mistake — calibration looks like it improved, but production output is unchanged. Procedure: identify the live systemd service, locate its canonical script path, mutate THAT, restart, verify before claiming success.
trigger: engine mutation, modify forecast, edit fetch_*.py, calibration didn't improve, live API unchanged, production forecast, cone engine, model server, WEALTH backend, forecast orchestrator
---

# Find the Live Binary Before Mutating

The arifOS federation has the same Python cone engine at 3+ paths for historical reasons (auditing, replication, federation shims). Editing the wrong one is the canonical mistake — subagents in 2026-09-25 did this twice in one session before the pattern was caught.

## The Three (or More) Copies

For XAUUSD on this federation (and likely XAUUSD-shaped problems on every commodity organ):

| Path | Role | Reaches users? |
|---|---|---|
| /var/www/html/<commodity>/api/fetch_<commodity>.py | LIVE — spawned by node server.js via systemd unit <commodity>-api.service (e.g. gold-api.service, port 3456) | YES |
| /root/WEALTH/engines/commodity/<commodity>-api/fetch_<commodity>.py | Source-of-truth copy — exists for source code review but NOT served | NO |
| /root/WEALTH/forecast/calibration/harness.py:model_cone_at() | Audit-replica — pure synthetic, used only by calibration harness | NO |

Generalizing: any organ with a systemd unit + node shim + Python subprocess will have this pattern. The same risk applies to oil-api, gas-api, klci-api, usdmyr-api if the patterns hold.

## Mandate Before Any Engine Mutation

1. Identify the live systemd service.

   systemctl status <organ>-api.service
   # or grep: grep -rn "ExecStart=" /etc/systemd/system/ | grep <organ>

   Read ExecStart= to get the canonical script path. That path is what gets served. Everything else is a replica.

2. Identify ALL replica paths.

   grep -rl "def <function_name>" /root/WEALTH/ 2>/dev/null

   Compare against the systemd ExecStart path. Any path that defines the same logic but isn't the ExecStart target is a replica.

3. Mutate the canonical file first. If replicas need to mirror the change (so calibration doesn't drift), do that after the live file is updated, restarted, and verified.

4. Restart the systemd unit. Without restart, the running node process still imports the old bytecode. Mutation is invisible.

   sudo systemctl restart <organ>-api.service
   systemctl status <organ>-api.service  # confirm "active (running) since <new time>"

5. Verify the change reached production.

   curl -s https://<public-host>/<organ>/api/<endpoint> | python3 -m json.tool

   Compare a deterministic field against the pre-mutation value. If unchanged, the restart didn't pick up the new code OR the file you edited isn't the one the service runs.

6. Only then run calibration. Calibration metrics are meaningless until step 5 succeeds. A recovered pinball_skill from calibration while the live API still returns the old cone.p50[0] is fabrication.

## Pitfalls

Editing the audit replica and claiming victory. Calibration reads model_cone_at from harness.py. Live API reads cmd_forecast from fetch_gold.py. They are not the same function. Editing one does not change the other. Calibration showing improvement while live API returns identical output means the edit was on the wrong path.

Not restarting after editing the live file. The systemd-managed node process holds the Python interpreter warm. New code in the .py file is not picked up until restart. The mutation is invisible to users.

Trusting calibration over a live curl. Calibration harness is a synthetic replica. Live API output is what users see. When they disagree, the live curl wins. Recalibrate the audit replica after the live change if needed.

Synthetic-vs-real data divergence. Calibration harness runs on synthetic GBM (matched volatility). Live engine reads yfinance. A model that passes calibration on synthetic data may fail on real data — and vice versa. Always cross-check forecast_basis.close against ticker.price before trusting the calibration verdict. If they diverge by >5%, the live data feed is broken and calibration is irrelevant.

## Diagnostic Procedure When Calibration Does Not Match Live Behavior

1. curl https://<host>/<organ>/api/<endpoint> → get live cone.p50[0]
2. Read <service ExecStart> file → identify canonical path
3. curl https://<host>/<organ>/api/calendar (or equivalent introspection endpoint)
   → verify the data backend yfinance/feed is producing expected values
4. If live API returns sane data but stale or wrong cone:
   → service hasn't been restarted since last edit
   → OR canonical file was edited but service reads from cached import
5. If live API returns broken data (close=2400 when ticker says 4284):
   → data feed bug, not engine bug
   → fix feed first; calibration is downstream noise until then

## Receipt Discipline

Every engine mutation must write to /root/AAA/VAULT999/receipts/:

```
{
  "mutation_id": "uuid",
  "canonical_path": "/var/www/html/gold/api/fetch_gold.py",
  "replicas_modified": ["/root/WEALTH/engines/.../fetch_gold.py"],
  "service_restarted": "gold-api.service",
  "restart_verified_at": "2026-09-25T11:24:00+08:00",
  "live_api_verification": {
    "cone.p50[0]_before": 2407.93,
    "cone.p50[0]_after": 2407.93,
    "changed": false
  },
  "calibration_run_only": false
}
```

A receipt that says live_api_verification.changed = false AND calibration_run_only = true is a receipt for failure, not success. Surface it as such.

DITEMPA BUKAN DIBERI
