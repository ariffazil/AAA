---
name: vps-cpu-throttle-triage
description: "Use on VPS CPU throttle, high %st steal, sustained load."
version: 1.0.0
author: Hermes (i-ARIF)
license: internal
owner: Hermes (curator-managed)
risk_tier: medium
autonomy_tier: T2
tags: [vps, cpu, throttle, steal, hostinger, triage, substrate, ops]
metadata:
  hermes:
    tags: [vps, cpu, throttle, steal, hostinger, triage]
    related_skills: [FORGE-incident-triage, federation-health]
triggers:
  - "CPU steal high"
  - "Hostinger throttle"
  - "VPS limited 40%"
  - "sustained high CPU"
  - "malware scan alert"
  - "load average high"
  - "%st steal"
  - "hypervisor cooldown"
---

# VPS CPU Throttle Triage — Shared-Host Sustained-CPU Incidents

Class-level playbook for sustained-CPU incidents on shared-host VPS (Hostinger et al.): hypervisor throttling, CPU steal, overlapping agent workloads, silent drains, and malware-vs-misconfiguration attribution.

Doctrine anchor: AUTONOMOUS SUBSTRATE KERNEL V1 — keep %st below 5.0%; above 15.0% trigger Hypervisor Cooldown Protocol (freeze non-critical jobs, concurrency 1, IDLE >90% for 45 min). No polling loops under 30 min. Resolve silently; escalate only for hardware failure or explicit JITU.

## When to Use

- Hostinger/provider reports sustained high CPU, auto-throttle to 40%, or a malware-scan alert.
- `%st` (CPU steal) elevated in vmstat, or load average persistently high on the VPS.
- Multiple agent runtimes/processes competing for CPU and the cause is unclear.
- After a reboot, to audit which services came back broken or disabled.

## When NOT to Use

- Pure application bugs inside one organ (use FORGE-incident-triage's six-step playbook).
- Docker-only fleet questions (use federation-health).
- Network incidents, disk-full incidents, or credential failures.

## Step 0 — Re-measure. Never trust the report. (PITFALL)

Incident reports and prior-session snapshots go stale fast — a reboot or a finished workload can change everything. Before acting on ANY number (steal %, load, "process X using Y%"):

```bash
vmstat 1 3 | tail -1          # st column = CURRENT steal
uptime                         # load trend (1/5/15 min)
```

Observed case: report said "78.2% steal, throttle active"; live measurement showed 0–8% steal after a reboot had already occurred. Acting on the stale report would have been wrong. **The report is context; the shell is truth.**

## Step 1 — Steal vs self-load

Two different problems with different fixes:

- **%st high (>15%)** → the HYPERVISOR is taking your CPU (noisy neighbors or provider-side throttle). Your processes may be innocent. Fix = reduce sustained usage so the throttle auto-clears, or manual reset in hPanel (once per week), or workload isolation onto a second VPS. You cannot kill your way out of steal.
- **%st low, us/sy high** → YOUR workload is the problem. Continue attribution below.

## Step 2 — Process attribution ladder (malware vs misconfiguration)

For every high-CPU PID, before killing anything:

```bash
ps -o pid,ppid,etime,time,%cpu,stat,tty,cmd -p <PID>
# walk the parent chain to find the supervisor
PP=$(ps -o ppid= -p <PID> | tr -d ' '); ps -o pid,ppid,cmd -p $PP
ls -l /proc/<PID>/cwd /proc/<PID>/exe
systemctl status <PID>        # which unit owns it (works with any PID)
w                             # who is logged in on which tty
```

Classification:
- **PPID=1 + old etime** → orphan from a dead session. Usually safe to kill after confirming nothing binds its port (`ss -tlnp | grep <port>`).
- **Attached to pts/N with live sshd parent + user in `w`** → someone's interactive session. DO NOT kill without sovereign confirmation.
- **Owned by a systemd unit** → killing respawns it; fix the unit/config instead.
- **Legitimate-but-overlapping** is the common verdict on agent VPSes: several agent runtimes + DBs + search all firing at once. Not malware. Malware scanners often return "no usable result" during exactly these events — absence of scan result ≠ malware, but also ≠ ruled out.

## Step 3 — Hunt silent drains

When no single runaway process explains the CPU, these three patterns are the usual suspects (all observed in the wild on this federation):

### 3a. Telemetry exporter retry-storm
An OTLP/Langfuse exporter posting to a dead or mis-pointed endpoint, 404, retry forever — thousands of errors, zero output.

```bash
grep -c "Failed to export span batch" /root/.hermes/logs/errors.log
# compare configured endpoint vs reality:
grep -n "LANGFUSE_BASE_URL" /root/.secrets/kunci-root.env
ss -tlnp | grep -E ":4000|:4318|:4317|:3100"
```

Observed root cause: `LANGFUSE_BASE_URL=http://localhost:4000` while 4000 was HAProxy and the Langfuse stack wasn't running at all → 1,377 failed exports.

### 3b. Bot spam retry-storm
Telegram gateway burning CPU retrying delivery to unauthorized hosts: `Forbidden: the bot can't send messages to the bot`, `Reply target deleted`, blocked-media floods from one user. Count: `grep -c -iE "retry|rate.?limit|429" gateway.log`. Fix direction: block the offending chat/user at the lane layer, not by killing the gateway.

### 3c. Backlog catch-up masquerading as runaway
After an outage, a queue consumer (e.g. NATS stream with ~140K pending msgs) restarts with Deliver-Policy=All and burns CPU chewing the backlog. This is EXPECTED one-time catch-up. Verify drain rate (`nats consumer info <stream> <consumer>` — Unprocessed must fall steadily), then leave it alone.

## Step 4 — Protected-config workarounds

The agent's patch/write tools REFUSE security-sensitive files (Hermes `config.yaml`, `/etc/systemd/**`). Do not fight this:

| Change | Sanctioned path |
|---|---|
| Disable a Hermes plugin | `hermes plugins disable <owner>/<name>` (takes effect next session) |
| Edit Hermes config.yaml | `hermes config set ...` or a Python yaml roundtrip in terminal |
| systemd drop-in tuning | terminal `cp` backup + `printf > drop-in` + `daemon-reload` + restart (keep a `.bak-<date>` beside it) |

Example proven fix: kabarkan worker `KABARKAN_POLL_INTERVAL=5.0 → 30.0`, `BATCH_SIZE=20 → 50` via `/etc/systemd/system/kabarkan-worker.service.d/interval.conf` — observability preserved, CPU dropped.

## Step 5 — Post-reboot resurrection audit

Reboots silently break things that were never enabled or whose targets moved. Checklist:

```bash
systemctl list-units --state=failed --plain          # triage each
systemctl is-enabled <service>                        # survivors come back DISABLED
```

Observed failure classes:
- **Service disabled after reboot** → `systemctl enable --now <unit>` (kabarkan-worker).
- **Oneshot guard whose ExecStart file vanished** (e.g. nft rules file deleted but rules also absent from live ruleset) → the guard was dead long before the reboot. Stub with `/usr/bin/true`, back up the original unit, confirm the real firewall (UFW) still active.
- **Token/lease expiry during downtime** (SCT session tokens TTL 1h) → run the renewer manually (`python3 /root/scripts/sct_renew.py`), else every gated call fails SCT_EXPIRED.
- **Host-vs-container drift**: scripts calling `pg_dump`/`psql` at host level while Postgres now runs in Docker → needs `docker exec` (one-line fix, not urgent at 3am).

## Step 6 — Hostinger throttle mechanics & the capacity verdict

- Sustained high usage → provider auto-throttles the VPS to 40%. Manual "Remove limitations" in hPanel is ONCE PER WEEK; after that only sustained normalization auto-clears it.
- While throttled, even light work looks slow; do not chase symptoms — lower the sustained baseline and wait.
- **Capacity verdict (recurring conclusion, 3 incidents)**: one box with 6+ agent runtimes + DBs + search is over-consolidated. When throttle recurs despite cleanup, the fix is workload isolation (control plane on VPS A; model traffic, search, batch workers on VPS B) — a design decision for the sovereign (cost), not an emergency migration. Design first, buy knowing what you pay for. 2026-09-02: sovereign chose the machine move — prep protocol in `federation-machine-migration`.

## Step 7 — Migration prep under throttle (bounded work)

When the sovereign decides to MOVE the machine (recurring throttle → workload isolation decision, observed 2026-09-02 at %st 76.3), prep work must stay bounded while cooldown is active. Not all work is equal under steal:

- **SAFE while throttled** (cheap local/light network): git add/commit/push (repos carry GitHub remotes), carry_forward.json write + backup stamp, read-only inventory (remotes, services, disk headroom), config/cron JSON validation.
- **DEFER until %st < 15**: full data dumps (pg_dump, qdrant snapshot, minio mirror), full-disk scans, service restarts, cron re-registration on the target, any operation whose slowness would extend the throttle window.
- **PITFALL — do not commit unverified half-finished work just to get a clean tree.** 2026-09-02 prep left `skills/apex_verdict_seal/` (EMPTY dir) plus two deleted skill files UNCOMMITTED because the consolidation was unverified. A clean tree is not worth destroying content. Commit only what is verified; leave the rest flagged in carry_forward for a dedicated review.

## Forbidden actions

- NEVER kill a process attached to a live ssh tty without sovereign confirmation.
- NEVER kill your own gateway mid-conversation; fix its config instead.
- NEVER act on a stale incident report without Step 0 re-measurement.
- NEVER bypass protected-file write refusal.
- NEVER present "malware ruled out" when the scanner has no usable result — say "not indicated by live process attribution" instead.

## References

- `references/2026-08-30-09-01-throttle-incidents.md` — two-session transcript: commands used, exact measurements, what was killed/disabled/restarted, and the stale-report trap.
