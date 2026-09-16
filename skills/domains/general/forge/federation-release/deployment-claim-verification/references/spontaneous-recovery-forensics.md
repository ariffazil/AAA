# Verifying "recovered by itself" claims — forensic heuristics (2026-09-01)

Applied during the LiteLLM/FED crash-loop incident. A recovery report claimed
the system self-healed with zero intervention. Verification showed otherwise:

## Heuristic 1 — diff mtimes against the claimed timeline

Recoveries are rarely spontaneous. For every "nothing needed to change" claim:

```bash
stat -c '%y %n' /path/to/config.yaml                          # edited? when?
ls -la --time-style=full-iso <unit>.service.d/                # drop-ins? mtime?
ps -o pid,ppid,etime,args -p <pid>                            # process age vs claim
```

In the incident: config comment at 13:18, systemd drop-in at 13:32, litellm
process elapsed 01:17 at 15:35 → restart at ~14:17. Three artifacts of
surgery the report had omitted (or misattributed to spontaneous recovery).
The facts it DID report (ports up, paths healthy) were accurate — the narrative
about WHY was wrong. Verify the causal story, not just the endpoints.

## Heuristic 2 — journal volume is ground truth

`journalctl -u <unit> --since today --no-pager | grep -c <pattern>` turns a
vague "prisma was slow" claim into a countable event (264 hits) with exact
timestamps (migration applied 11:13). Claims about cause must match journal
evidence or they are speculation.

## Heuristic 3 — verify from the consumer's vantage, not just localhost

A service healthy on `127.0.0.1` can still be unreachable by the caller.
Probe the same surface the dependent node uses:

```bash
curl -sS -m 5  http://127.0.0.1:4000/health/liveliness   # internal
curl -sS -m 20 http://100.64.0.2:4000/health/liveliness  # as wawa sees it
tailscale status                                          # node online? path?
ping -c 2 <tailnet-peer-ip>
```

Here the box IS the tailnet IP host, so the tailnet-IP curl also exercises
the tailscale stack — the real consumer path. One timeout on that path is not
a verdict (flake on first attempt, 200 on retry) — retry once before
declaring.

## Heuristic 4 — stateless-recovery caveats are part of the verdict

When recovery was achieved by disabling a dependency (e.g. LiteLLM
`database_url` commented out for stateless boot), the verification verdict
must state what was traded away (spend tracking / persistence), not just
"service is up". Uptime with reduced function ≠ full recovery.
