---
name: federation-organ-recovery
description: Use when a federation organ is down or crash-looping.
id: federation-organ-recovery
version: 1.0.4
owner: AAA-curator
risk_tier: low
autonomy_tier: T1
tags: [federation, systemd, organ, recovery, diagnostics, crash-loop, haproxy, litellm]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Federation Organ Recovery — systemd-era Diagnosis & Healing

> The federation's organs are now **systemd units** (docker-compose era is legacy; Docker remains
> only for infra: postgres, qdrant, falkordb, minio, searxng). This skill covers diagnosing and
> recovering organ services when an alert fires. Complements `incident-response` (lifecycle/
> escalation) — this one is the hands-on *how to find and fix it* layer.

## When to Use

- A pulse/monitor reports an organ unreachable or a port refused (wawa-pulse, FRAME witness, etc.)
- A systemd unit is "active" but its port never binds / health probe fails
- Suspected crash-loop (restart counter climbing)
- FED :4000 unreachable or model lane "blind" (fallback to gemini/ollama triggered)

## Prime Rule: Trust Sockets, Not Labels

Monitoring/registry port labels drift from reality. Before believing any "port X is down":

```bash
# 1. What actually listens?
ss -tlnp | grep -E ':(PORT|4000|1808[0-9]|8088)'

# 2. What does the unit file actually say?
systemctl cat <unit>.service | grep -E 'ExecStart|PORT|Environment='

# 3. What do the logs actually show?
journalctl -u <unit>.service --no-pager -n 15
```

Example (2026-09-02): alert said "wealth :18086 DOWN" — wealth was alive on :18082 the whole time.
One false label wasted a branch of the diagnosis. Ground truth first.

## Failure Pattern 1: Permission-Drift Crash Loop (bad deploy)

**Symptoms:** unit "active"/"activating", port never binds, restart counter climbing (observed:
501 restarts), journal shows:

```
PermissionError: [Errno 13] Permission denied: '/opt/arifos/app/arifosmcp/schemas/action_profile.py'
```

Bad deploys can leave individual files unreadable (e.g. mode `604`).

**Fix — repair the WHOLE tree, never one file at a time:**

```bash
chmod -R a+rX /opt/arifos/app/arifosmcp   # or the affected app tree
systemctl restart arifos.service
```

**Pitfall:** fixing only the file in the traceback burns another restart cycle on the NEXT
unreadable file. Scan first if unsure: `find /opt/arifos/app/arifosmcp -type f ! -perm -o+r`.

## Failure Pattern 2: Thundering Herd After Long Downtime

**Symptoms:** organ was down hours; after fix + restart, CPU pegs ~80%, `/health` times out,
journal floods with `Exceeded concurrency limit` / 503s, `ss -tlnp` shows nonzero Send-Q
(accept backlog saturated).

**Cause:** every watchdog, heartbeat, and fed-watchdog queued probes while the organ was dead and
now hammers it simultaneously the moment it binds.

**Response:**
- Do NOT restart-loop it — that resets progress each time.
- Wait. Probe with 10–15s timeouts. Observed: bind ~1 min after start, but stable 200 on
  `/health` only ~4–5 min later once the herd drained and startup finished.
- Check `journalctl -u <unit> --since "1 min ago"` — if you see fresh 200 OK lines, it's serving
  even if your curl raced.
- arifOS kernel startup is heavy: budget 3–4 min from `systemctl restart` to bound port
  (uvicorn "Application startup complete" line), plus settle time.

## Failure Pattern 3: FED :4000 "Unreachable"

haproxy fronts the model lane; backend pool is litellm.

```bash
# no-auth liveness (the canonical path)
curl -s http://127.0.0.1:4000/health/liveliness   # -> "I'm alive!"

# litellm backend on :4013 (auth-gated: /health = 401 means UP)
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:4013/health/liveliness  # 200 = UP

# end-to-end model lane through haproxy
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:4000/v1/models          # 200 = lane OK
```

**Decision rule:** haproxy process listening (`ss -tlnp | grep :4000`) but curl fails → suspect
backend pool (litellm) first, not the proxy.

## Post-Fix Verification (all 6 surfaces)

```bash
for svc in "FED:4000/health/liveliness" "arifOS:8088/health" "GEOX:18082/health" \
           "WELL:18083/health" "AAA:18084/health" "FRAME:18085/health"; do
  n=${svc%%:*}; p=${svc#*:}
  curl -s -m 10 -o /dev/null -w "$n -> %{http_code}\n" http://127.0.0.1:$p
done
```

Declare green only when every probe returns 200 — AND re-probe once more after a minute;
warm-up lag can make a healthy organ look dead on the first pass.

## Port Map (verified 2026-09-02 on KVM8/af-forge)

| Port | Service | Notes |
|---|---|---|
| 4000 | haproxy → litellm | FED model lane; `/health/liveliness` no auth |
| 4013 | litellm | backend; `/health` 401 (auth-gated) = UP |
| 8088 | arifOS kernel | systemd arifos.service; slow cold start |
| 18082 | GEOX + WEALTH | wealth-organ.service registers here (NOT 18086) |
| 18083 | WELL | well.service |
| 18084 | AAA | |
| 18085 | FRAME | independent observer |
| 7071-7074 | A-FORGE executor / MCP gateway / arifFlow / FED router | |

## Pitfalls

- A 401/403 on a health endpoint = service UP, auth-gated. Only conn-refused/timeout = DOWN.
- `systemctl is-active` saying "active" means NOTHING about the socket during startup.
- Don't batch fixes. One mutation, one restart, one verify.
- FED 1 timeout ≠ down — retry up to 3× before declaring (established house rule).
- After declaring all-green, tell downstream nodes (wawa etc.) they may drop their fallback lane.

## References

- `references/2026-09-02-arifos-permission-crash-loop.md` — full incident transcript: journal
  signatures, fix commands, false-alarm postmortem, recovery timeline.


## Lessons (auto)

*Auto-ingested from agent learning. F2-gated: every entry carries evidence.*
- **[2026-09-15] hermes-rsi-loop** (evidence: [{"layer": "runtime", "source": "session-trace:cli:20260912_003048_fd50", "excerpt": "Auto-traced session 20260912_003048_fd509c. 15 tool calls, 87% success. Errors: 2."}, {"layer"): SILENT_FAIL observed 14x — impact=session_error. First surface: session-trace:cli:20260912_003048_fd50 — all four checks passed, but independence is NAME-LEVEL ONLY (same author) — verdict is PROVISIONAL: may enter the capability graph, may NOT record a survival event
- **[2026-09-15] hermes-rsi-loop** (evidence: [{"layer": "runtime", "source": "session-trace:subagent:20260912_022918_fdec", "excerpt": "Auto-traced session 20260912_022918_fdec01. 10 tool calls, 70% success. Errors: 3."}, {"l): SILENT_FAIL observed 10x — impact=session_error. First surface: session-trace:subagent:20260912_022918_fdec — all four checks passed, but independence is NAME-LEVEL ONLY (same author) — verdict is PROVISIONAL: may enter the capability graph, may NOT record a survival event
- **[2026-09-15] hermes-rsi-loop** (evidence: [{"layer": "runtime", "source": "session-trace:telegram:20260912_012105_3a49", "excerpt": "Auto-traced session 20260912_012105_3a49a4f9. 18 tool calls, 89% success. Errors: 2."}, {): SILENT_FAIL observed 6x — impact=session_error. First surface: session-trace:telegram:20260912_012105_3a49 — all four checks passed, but independence is NAME-LEVEL ONLY (same author) — verdict is PROVISIONAL: may enter the capability graph, may NOT record a survival event
- **[2026-09-15] hermes-rsi-loop** (evidence: [{"layer": "runtime", "source": "session-trace:cron:cron_5a8cdae52298_20", "excerpt": "Auto-traced session cron_5a8cdae52298_20260914_090032. 25 tool calls, 36% success. Errors: 16): SILENT_FAIL observed 3x — impact=session_error. First surface: session-trace:cron:cron_5a8cdae52298_20 — all four checks passed, but independence is NAME-LEVEL ONLY (same author) — verdict is PROVISIONAL: may enter the capability graph, may NOT record a survival event
