---
name: service-state-schema-drift
description: "Use when a service won't start after a version bump."
risk_tier: low
tags:
- service
- upgrade
- sqlite
- systemd
- diagnostics
floor_scope:
- F2
- F11
---

# Service state-schema drift — the binary that refuses its own data

Distinct from `deploy-drift-verification`, which is about **code** not reaching runtime. This is the
other axis: the code is fine and the **persisted state is ahead of it**. A build opens its data
store, finds a schema written by a newer build, and refuses to start — on purpose, because running
an old binary against forward-migrated data can corrupt it.

The tell is that every other layer reads healthy: the host pings, the app's port may still be
served by a proxy or a sidecar, and a watchdog keeps restarting the unit. The failure is one layer
down, in the unit's journal.

## Symptoms

- Unit flaps: `start` → fail → restart, until systemd gives up (`restart counter is at N`).
- A watchdog or path-unit fires repeatedly; its restarts are the **symptom**, not the cause.
- Exit status `78`/`CONFIG` or the ecosystem's equivalent "my config/state is not for me".
- Peers still reach the host and any reverse proxy still answers, so uptime checks stay green.

## Diagnosis — read the service's own refusal, do not infer it

```bash
systemctl status <unit> --no-pager
journalctl -u <unit> --since '3 hours ago' --no-pager | tail -40
```

The unit usually states the fault verbatim, including both version numbers and the store path, e.g.

```
state database <path> uses newer schema version 18; this build supports 17
Refused by <product> <version> installed at <path>
```

Then establish the two sides of the mismatch independently:

```bash
# what does the INSTALLED build actually claim?
<binary> --version
# what schema does the state store carry? (table name differs per product — list first)
sqlite3 <state-file> '.tables' | tr ' ' '\n' | grep -i -E 'schema|migration|version'
```

## Resolution — forward, not back

Default to completing the upgrade. A newer build that owns the newer schema will migrate on start
and normally writes a **pre-migration backup** of each store before touching it — capture that fact
as your safety net.

```bash
ls -la <state-dir>/ | grep -i 'pre-.*migration\|backup'   # expect these to appear/refresh
systemctl reset-failed <unit>.service                      # required once the restart counter tripped
systemctl start <unit>.service
sleep 25                                                   # first boot migrates; do not judge early
systemctl is-active <unit>.service
```

Rolling the **state** back (restoring a pre-upgrade backup to satisfy an older binary) is the
fallback, not the first move: it discards everything written since the upgrade and must be an
explicit human decision, never a reflex to make a unit go green.

## Pitfalls

- **The restart counter blocks the fix that works.** After repeated failures systemd stops trying; a plain `systemctl start` reports a stale failure until you run `systemctl reset-failed <unit>` first. A retry that "doesn't work" may never have been attempted.
- **A version bump may already be in flight.** Check `<binary> --version` against the version quoted in the *earliest* failure log before planning anything — an auto-updater can pull a compatible build between the first crash and your probe, and the incident has resolved itself. Compare the versions in the journal against the versions now on disk; a mismatch there means the fault is stale.
- **First boot after a migration is slow and the unit may look wedged.** Sleep, then read the journal tail for the migration lines before declaring failure.
- **Judge readiness by the unit's own status transition, not by a port that was already open.** A proxy or a co-located listener can answer on the same port throughout the outage.
- **Do not "tidy" the accumulated pre-migration backups.** They are the rollback path and are sized like the store; note them in the report rather than deleting them to reclaim space.

## Report shape

The useful receipt names: the refusal line from the journal (both versions), the store path, the
installed build now serving, the unit's `active` timestamp, and which pre-migration backups exist.
Do not report the watchdog's restart count as the fault — it is the thing that noticed.
