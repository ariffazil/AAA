# Incident: arifOS permission-drift crash loop — 2026-09-02

**Trigger:** wawa-pulse alert "FED UNREACHABLE, 100.64.0.2:4000 tak jawab" + OpenClaw thermal
report claiming arifOS :18081 and wealth :18086 conn-refused.

**Root cause:** arifos.service crash-looping (restart counter 501) on unreadable files after a
bad deploy. Journal signature:

```
PermissionError: [Errno 13] Permission denied: '/opt/arifos/app/arifosmcp/schemas/action_profile.py'
systemd[1]: arifos.service: Main process exited, code=exited, status=1/FAILURE
systemd[1]: arifos.service: Scheduled restart job, restart counter is at 501.
```

`stat` showed `-rw----r--` (604) owned by ariffazil. Multiple files affected across
schemas/, runtime/, tools/, hib/ (dependency_gate.py, tool_registry.py, flame_client.py,
audit_fatitude.py, temporal_governance.py, ...).

**Fix:**
```bash
chmod -R a+rX /opt/arifos/app/arifosmcp
systemctl restart arifos.service
```

**Secondary findings (false alarms in the original alert):**
1. "wealth :18086 DOWN" was wrong — wealth-organ.service was alive on :18082 (pid 1416) the
   entire time; its journal showed continuous 200s. Registry label drift, not an outage.
2. FED :4000 was never actually dead during the recovery phase — haproxy was listening and
   `/health/liveliness` answered 200 once probed correctly; litellm :4013 was bound and serving
   (401 on /health = auth-gated = UP; /health/liveliness = 200).

**Recovery timeline (arifOS):**
- chmod + restart → "activating" ~2 min (release attestation, prompt-rpc patch, skills scan)
- Bind at t+~1 min after "Application startup complete" (uvicorn, 127.0.0.1:8088)
- First ~4 min: thundering herd — CPU ~80%, "Exceeded concurrency limit", 503s, /health timeout
- ~5 min post-restart: stable 200 on /health; all 6 surfaces green
- arifOS /health response shape: `{"status":"healthy","degraded_reasons":[],"layer_health":{"constitutional":{"status":"healthy","floors_active":13,"floors_target":13,"vault999":"healthy"},...}`

**Lesson:** a "down" organ and a "slowly recovering under stampede" organ look identical from
outside. Distinguish via journal (fresh 200 lines = serving) and `ss` Send-Q, not just curl exit
codes.
