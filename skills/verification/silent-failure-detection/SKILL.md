---
name: silent-failure-detection
description: "Use when a system claims success - verify it landed."
tags: [verification, silent-failure, delivery, receipts, docker, connectivity, monitoring]
owner: Hermes
authority_of: AAA
triggers:
  - "sent=true but not received"
  - "delivered but missing"
  - "reports success"
  - "silent failure"
  - "optimistic receipt"
  - "healthy but no data"
  - "postgres_healthy false"
  - "password authentication failed"
  - "stub handler"
  - "wired via (future"
  - "false positive monitor"
  - "verify delivery"
---

# Silent Failure Detection — the effect that never arrived

## The Core Law

**A success flag describes what the SENDER did, not what the RECEIVER experienced.**
`sent`, `delivered`, `published`, `applied`, `healthy` are claims about a hop the sender
controls. Prove the far end on a surface the sender does **not** own.

A silent failure is worse than a crash: a crash raises a stack trace and triggers failover; a
silent failure writes a success into the system's own timeline, so the agent reasons forward from
a false premise ("the human was told"). The defect is not the missing effect — it is the receipt
that says it happened.

## The four hops where an effect dies

Check in this order. Each hop can drop the effect while the previous hop reports green.

1. **Handler (app)** — the code that "sends" never calls anything.
2. **Network / address** — the call goes out but arrives from/to an address the far end rejects.
3. **Process (stale)** — the code is right, the running process holds old bytecode/config.
4. **Consumer** — the message is queued but nothing drains it.

## Hop 1 — read the handler, not the flag

Before trusting any `sent` / `delivered` / `published` / `queued` / `applied` value, read the
handler body.

```bash
grep -nE 'requests\.|httpx|aiohttp|urlopen|client\.|\.post\(' <handler>.py   # empty => likely a stub
```

Red flags:
- the handler logs, then returns a success object — with no outbound call above it;
- a comment like *"wired via <X> (future: direct integration)"* — that is a TODO, not a wire;
- the `reason` string names a bridge/consumer that is never invoked inside that function.

The canonical poison: `return {sent: true, event_id: <uuid>, reason: "routed to <X>"}` with **zero
network I/O**. Cross-check the claim against a surface the handler does not control — a consumer
log, a DB row, the upstream API.

## Hop 2 — a connection arrives from the address the network path gives it

A host process reaching a **containerised** service does **not** arrive from `127.0.0.1`. Docker's
port mapping (`docker-proxy`) forwards the host->container connection with the **bridge source IP**
(`172.17.0.0/16`, `docker network inspect bridge` -> `IPAM`), so a `pg_hba` rule aimed at
container-localhost (`host all all 127.0.0.1/32 trust`) does not match the host's clients — they
fall through to the catch-all (`host all all all scram-sha-256`) and die `password authentication
failed`, while `docker exec ... psql -h 127.0.0.1` (inside the container namespace) succeeds as `trust`.

**Verify from the same vantage the failing client uses:**

```bash
# HOST vantage — this is what the failing client sees
psql -h 127.0.0.1 -U <user> -d <db> -c 'select current_user, current_database();'
# container vantage — proves the data/user exist regardless of the host result
docker exec <ctr> cat /var/lib/postgresql/data/pg_hba.conf | grep -v '^#\|^$'
docker exec -e PGPASSWORD=<pw> <ctr> psql -h 127.0.0.1 -U <user> -d <db> -c '\dt'
```

The `docker exec` path never exercises the docker-proxy hop — it cannot reproduce the host failure.

**Fix:** hand the host clients the credential (a systemd `EnvironmentFile`, or an explicit
`password=` argument), or add a trust rule for the bridge subnet in `pg_hba.conf` and reload.
Note **`asyncpg` does not read `PGPASSWORD`/libpq env vars the way `psql` does**, so env alone is
not enough for a Python client. Do not conclude "the database is down".

## Hop 3 — read the running process, not the file

A change on disk is a request; it is the process's state only after re-import.

```bash
systemctl show <unit> -p MainPID -p ExecMainStartTimestamp --value
stat -c '%y %n' <source-file>          # newer than process start == stale runtime
```

## Hop 4 — a queue with no consumer is not a gate

Name the process that drains every queue. A producer writing into a stream nothing consumes is
"doctrine present, executor absent" — report both halves.

```bash
journalctl -u <worker> -n 20 --no-pager | grep -iE 'failed|refused|closed|error'
ss -tlnp | grep <port>
```

## Monitoring: a probe's own error classifies the defect

When a monitor reports `false` / `degraded` / `down` for a component you can reach, read the
monitor's own journal. The error string separates a **probe defect** from a real **outage**:

| Probe's own error | Meaning |
|---|---|
| `password authentication failed` / `no password supplied` | **probe defect** — the client credential/context is wrong; the service is fine |
| `connection refused` | nothing listening on that address — check the bind |
| timeout | down, or hung mid-request |
| `200` / `401` / `403` / `400` | up (`400` = parsed and rejected; `404` = wrong **path**, not the service) |

A monitor that invents absence is worse than no monitor, because it signs a confident report. Fix
the probe, not the component.

## Verdict taxonomy

Classify every claim against a **fresh** probe:
**LIVE_VERIFIED** (re-derived this session) · **DOCUMENT_ONLY** (stated, unprobed) · **DRIFTED**
(true before, not now) · **UNKNOWN**.
And every named defect: **STILL_ACTIVE** · **PARTIALLY_RESOLVED** · **RESOLVED** · **UNKNOWN**.
Never repeat a historical finding as current — a fixed problem appears in runtime, not in the report.

## Always-on rules

- A sender's success flag is not evidence about the receiver. Prove the far end on a surface the
  sender does not control.
- Read the handler before trusting its receipt; a stub that returns a plausible `event_id` is the
  canonical silent-failure shape.
- When a monitor and your probe disagree, read the **monitor's** own error before restarting the
  component — a probe defect and an outage have different remedies.
- Disclose any repair you made before the verification window; an unreported mutation contaminates
  the reconciliation.
- Prefer the smallest mutation that restores **truth** over the smallest that restores service: if
  you cannot wire the real send, make the flag tell the truth (`sent:false, reason:"NOT_WIRED"`) —
  the lie is the defect.

## References
- `references/verification-recipes.md` — copy-paste probe recipes for each hop.
