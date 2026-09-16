---
name: federation-state-report
description: "Use when asked for the state of the machine or system."
risk_tier: low
floor_scope:
  - F2
  - F7
  - F11
tags: [probe, federation, health, systemd, docker, mcp, state-report, narrative-vs-state]
---

# Federation State Report

Class: the sovereign asks for "the latest state of the machine / system / agents / intelligence" — or pastes a public console, landing page, or dashboard and wants it reconciled with what is actually running. This is a narrative-vs-state audit: banners, pages, and dashboards are narratives; only probes are witnesses.

Read-only throughout. Nothing here needs an approval gate; a mutation discovered along the way gets reported, not done.

## Probe ladder — four layers, in this order

```bash
# 1. MACHINE — identity + resources. Never report specs from memory.
hostname; date -u '+%Y-%m-%dT%H:%M:%SZ'; date '+%Y-%m-%d %H:%M:%S %Z'
uptime; free -h; df -h /; nproc
cat /proc/pressure/cpu /proc/pressure/memory /proc/pressure/io

# 2. SYSTEM — service inventory. list-units, NOT is-active on guessed names.
systemctl --failed --no-pager --plain                       # the only authoritative failure list
systemctl list-units --type=service --state=running --no-pager --plain | grep -iE '<organ>|<agent>'
docker ps --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'
ss -tlnp                                                    # what is bound, and to which interface

# 3. AGENT — sessions, gateway, organ surfaces
ps -eo pid,etime,pcpu,rss,args --sort=-pcpu | grep -iE '<agent-cli>' | grep -v grep
curl -s -m 5 http://127.0.0.1:4000/health/liveliness        # FED no-auth liveness (401/403 = up, auth-gated)
curl -s -m 5 http://127.0.0.1:<organ-port>/health

# 4. INTELLIGENCE — ledgers and loops, not vibes
python3 -c "import json;d=json.load(open('/root/.hermes/cron/jobs.json'));j=d if isinstance(d,list) else d.get('jobs',[]);print(len(j),'jobs,',sum(1 for x in j if x.get('enabled')),'enabled')"
tail -5 /root/AAA/canon/eureka-entries.jsonl
```

A ready-made run of all four layers: `scripts/probe.sh`.

## Rules

- **A guessed unit name returns `inactive` with no error.** `systemctl is-active hermes-gateway arifos-forge aforge geox wealth well frame fed` reports "inactive" for every name that is not a unit — while `hermes-asi-gateway`, `arifos.service`, `a-forge.service`, `geox-mcp.service`, `wealth-organ.service`, `frame-organ.service`, `fed-router.service` are all running. Never declare a service DOWN from `is-active` on a remembered name. Enumerate first, and take failures from `systemctl --failed`. The probe's identifier must come from the box, not from memory.
- **A health-port 000/DOWN is a port fact, not an organ fact.** Take ports from `ss -tlnp`, and check `docker ps` for containerised organs. Containers and systemd units are two namespaces — postgres/qdrant/redis/falkordb are containers, the organs are units; check both before calling anything down.
- **Probe `/ready` as well as `/health`.** A health endpoint can honestly report `healthy` while the machine readiness probe returns `status: fail` with a named failing-subsystem list (`ops_health`, `mind_check`, `heart_check`, `memory_dry_run`). Health that delegates its infra verdict to `/ready` is being honest; a front-door banner reading "Operational" while `/ready` is 503 is not. Report both, and say which one the banner is standing on.
- **A readiness check that says `human_decision_required: true` is F13 territory.** Surface it as the one open question and stop there — do not resolve it, do not re-run it until it goes green.
- **Advertised counts and endpoints are hardcoded until proven live.** A public console advertising "10 prompts, 4 resources" while `prompts/list` returns 13 and `resources/list` returns 35 is a stale page, not a live surface. Same class: `GET /metrics/json` and `GET /sse` advertised on the page and returning 404. Probe each advertised endpoint for a real status code, and each advertised count against the wire (`tools/list`, `prompts/list`, `resources/list`, `.well-known/mcp/server.json`) before repeating it. A count that matches no surface is a finding even when it is small.
- **Registry size > public wire is BY DESIGN, not hidden capability.** Read the endpoint's own `tool_count_semantics` before treating the gap (registry / declared / diagnostic vs exposed) as a lie.
- **A self-reported human metric is not sensor data.** `truth_status: OPERATOR_REPORTED` with `is_sensor_verified: false` means quote the number only with that provenance attached — record freshness does not upgrade source class. Machine-substrate telemetry and human-biometric telemetry are separate fields; never merge them into one "the system is healthy".
- **A page's "0 open gaps" is scoped.** Tracked-gap tables usually cover one named list only; the issue tracker and the readiness probe carry the rest. Reconcile against the tracker before echoing "all clear".
- **PSI before you call a machine loaded or fine.** High `some` with `full` ≈ 0 is contention, not saturation. Swap near-full with `MemAvailable` healthy and `full` = 0 is cold pages, not thrashing — say which one it is rather than guessing from the raw free/swap numbers.
- **Two writers may share the box.** Other agent sessions can restart services mid-probe. Before attributing a restart to anyone, check `journalctl --since` and the sessions' own state — a single probe window is not the world.

## Reporting shape (Arif)

Plain BM Penang, short, no tables and no receipt labels. Lead with what is actually wrong or what changed, then the layers in order, then one bounded decision.

- Pattern that works: *"Tulang belakang kuat, tiada yang tumbang."* followed by the one or two things that are genuinely off, then the exact question you will not answer yourself.
- Never say "semua OK" when `/ready` is red — name the failing checks and keep the two verdicts separate.
- Close with at most one decision. If a probe returned `human_decision_required`, that is the decision; do not offer a menu.
- Do not paste raw JSON at the sovereign. Extract the fields, state the delta, keep evidence paths for when he asks.

## Related

- `live-probe-audit-pattern` — auditing *someone else's* claim; this skill is producing the state picture. Same probe discipline, different trigger.
- `federation-machine-verification` — machine/organ/port identity before multi-machine ops.
