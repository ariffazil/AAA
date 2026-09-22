---
name: federation-service-recovery
description: "Use when a federation service is slow or crash-looping."
owner: AAA
category: devops
tags: [systemd, service-recovery, kernel, d-state, cgroup, redis, health-probe, hermes-config]
triggers:
  - service slow or unresponsive
  - health endpoint times out
  - activating auto-restart
  - systemctl failed unit
  - mem_cgroup_handle_over_high
  - process in D state
  - NOAUTH Authentication required
  - WRONGPASS redis
  - MemoryHigh MemoryMax
  - arifos kernel not responding
  - hermes gateway slow
  - hermes config not sticking
  - federation organ down
source: hermes-only
synthesized: 2026-09-14
floor_scope: [F1, F2, F4, F9, F11]
autonomy_tier: T1
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Federation Service Recovery

> **Reality lives in `/proc` and `systemctl show`, not in the unit files.**

Applies to every systemd-managed service on the federation nodes: `hermes-asi-gateway`, `arifos`, `aaa-a2a`, `federation-state`, `arifflow`, and MCP sidecars.

## Triage order (cheapest first)

1. `systemctl is-active <svc>` and `systemctl status <svc> --no-pager | head -12` — note which of three states: `active`, `failed`, or **`activating (auto-restart)`** (crash loop).
2. `journalctl -u <svc> --since "10 min ago" -p warning --no-pager | tail -30` — the last real error usually names the cause: a missing env var, a bad credential, or a plain code defect.
3. `uptime`, `free -h`, `cat /proc/pressure/cpu`, `ps aux --sort=-%cpu | head` — is the box saturated, or is one service hot? Distinguish host pressure from a single wedged process.
4. `curl -s -o /dev/null -w '%{http_code} %{time_total}s' http://127.0.0.1:<port>/health` — separates "port closed" from "process up but wedged" (the second times out while the process is alive).

## Wedged process that is still listening (D-state)

Symptom: the health port times out, `ps` shows the process alive, and `ss -tnp` shows the socket with a growing `Send-Q` / CLOSE-WAIT backlog.

```bash
ps -p <pid> -o pid,stat,%cpu,%mem,rss,etime,wchan --no-headers
cat /proc/<pid>/wchan          # the kernel function it is blocked in
```

- `stat` containing **D** = uninterruptible sleep (blocked on I/O or cgroup reclaim). **D-state processes do not handle signals promptly** — plan a restart, not a graceful reload.
- `wchan` = **`mem_cgroup_handle_over_high`** → the process is being throttled by its memory cgroup. It hit `MemoryHigh` and the kernel forces reclaim on every allocation. This presents as a **dead event loop**, not an OOM kill, so nothing in the logs says "out of memory".

## Effective limits: read them from systemd, never from the unit file

```bash
systemctl show <svc> --property=MemoryCurrent,MemoryHigh,MemoryMax,CPUQuotaPerSecUSec
```

Drop-ins live in more than one directory and **conflict silently**:

- `/etc/systemd/system/<svc>.service.d/*.conf` — authored drop-ins
- `/etc/systemd/system.control/<svc>.service.d/*.conf` — written by `systemctl set-property`

A unit file that reads `MemoryHigh=2.5G` can still be running at `1.5G` because another drop-in set a lower value at higher precedence. **The value `systemctl show` reports is the only truth.** Compare `MemoryCurrent` against `MemoryHigh`: if current ≈ high, the service is riding the throttle ceiling and every allocation stalls.

**Fix — one drop-in, then confirm:**

```bash
cp /etc/systemd/system/<svc>.service.d/resource-limits.conf{,.bak-$(date +%Y%m%d-%H%M%S)}
# edit MemoryHigh / MemoryMax / CPUQuota / TasksMax to fit the host
systemctl daemon-reload && systemctl restart <svc>
systemctl show <svc> --property=MemoryHigh,MemoryMax   # confirm, never assume
```

Rule of thumb: set the ceiling above observed peak (peak + ~50%), and check `free -h` first — the host's own headroom is the real constraint, and `daemon-reload` alone does not re-apply an already-running unit.

## Credential drift: compare against the RUNNING service, not the vault

A service that authenticates (Redis, Postgres, NATS) fails with `NOAUTH` or `WRONGPASS` when the env file it loads is stale relative to the running daemon's own config.

```bash
grep -n '^requirepass' /etc/redis/redis.conf            # what the daemon actually enforces
grep -n 'REDIS_PASSWORD\|REDIS_URL' /root/.secrets/<env>.flat.env
```

- **`NOAUTH Authentication required`** = the client sent *no* credential → the code reads only the URL and ignores the `*_PASSWORD` env var. Fix the **code path**, not the env.
- **`WRONGPASS`** = a credential was sent but does not match → the env value is **stale**. Align the env file to the running config, then prove it with a direct client call (`redis-cli -a "$REDIS_PASSWORD" ping` → `PONG`).

Never echo secret values: compare lengths, or test-auth and report only `PONG` / `WRONGPASS`.

Also check the systemd unit: an `Environment=` line in the unit **overrides** the same key from `EnvironmentFile=`, so a hand-set `Environment=REDIS_URL=...` can silently shadow a correct value in the env file.

## Crash loop (`activating (auto-restart)`)

The unit starts, exits non-zero, and systemd retries. The cause is in the last stderr block, not in the unit file. Three shapes seen repeatedly:

- **Missing or ignored env var** — the process needs a value the unit never passes (see credential drift above).
- **Plain code defect** — e.g. `NameError: name '<helper>' is not defined` from a call site that was never given a definition. Fix the code; do not restart harder.
- **`ExecStartPre` guard false-negative — the unit and the file are both fine.** A `test -r <path>` precondition fails even though the file is genuinely readable. See below; this one burns the most time because every surface you check says the file is fine.

### ExecStartPre `test -r` false negative (owner/primary-group blindness)

**Symptom:** every restart dies on the *first* `ExecStartPre` with `Control process exited, code=exited, status=1/FAILURE`, no application error, no Python traceback. `journalctl` shows only unrelated noise (e.g. an `iptables` permission line) — that noise is a red herring.

**Mechanism:** on hosts where `/usr/bin/test` is **rust-coreutils (uutils)**, its `-r`/`-w`/`-x` checks are naive — they honour **owner and primary gid only**. They ignore *supplementary groups* and ignore **ACLs entirely**. So `test -r` returns 1 for a file that `cat`, `python3 os.access()`, and the builtin `test` all read successfully. systemd runs the unit as `User=<u>` + `SupplementaryGroups=<g>`; if the guarded file is owned by another user and readable only via that supplementary group, the guard fails and the service never starts. `chgrp`-based hardening is exactly what triggers it.

**Confirm before you touch anything** — reproduce under the unit's own credentials, and prove the split:
```bash
# what is the guard even checking?
systemctl show <svc> -p ExecStartPre -p User -p Group -p SupplementaryGroups | tr ';' '\n' | grep -E 'path=|argv'
ls -la <guarded-path>
# run under the SAME user/group/supplementary as the unit, not as root
systemd-run --unit=permprobe --collect --property=Type=oneshot \
  --property=User=<u> --property=Group=<g> --property=SupplementaryGroups=<g> \
  /bin/bash -c '/usr/bin/test -r <path>; echo "rust=$?"; test -r <path>; echo "builtin=$?"; cat <path> >/dev/null; echo "cat=$?"'
sleep 3; journalctl -u permprobe --no-pager -o cat | grep -E 'rust=|builtin=|cat='
```
`rust=1  builtin=0  cat=0` is the signature. `readlink -f /usr/bin/test` pointing into `*/cargo/bin/coreutils/*` confirms the cause.

**The same symptom has a second cause: a RACE, not a permission defect.** Re-run the probe before
applying any fix. If the guard failed in the journal but the replay under the *identical* identity
**succeeds**, the precondition is not the defect — something rewrote the guarded path between start
attempts. Confirm from mtimes: a file whose mtime falls inside the failing window (minutes before
the first failed start) is the tell.
```bash
stat -c '%y %n' <guarded-path>          # rewrite time
journalctl -u <svc> --no-pager | grep -n 'Starting\|status=1' | head
```
Classify it `SYNCHRONIZATION_FAULT` and report it as such. **Do not apply the owner-change fix**
to a file you could not reproduce as unreadable — you would mutate a working access control to
solve a problem that was a concurrent write. Distinguish the two signatures before touching anything:
`rust=1 builtin=0 cat=0` = persistent meta-check defect (fix the ownership); replay reads clean =
race (fix the writer ordering, or add a retry, and leave permissions alone).

**Fix — preserve the access set, do not widen it.** Make the service user the file's *owner* rather than relying on a supplementary group:
```bash
stat -c '%a %U %G' <path>          # record before
cp <path> /tmp/<name>.before-fix    # reversible
chown <svc-user>:<access-group> <path> && chmod 440 <path>
# 440 + that group = identical access set: svc-user reads, group reads, others never
systemd-run ... '/usr/bin/test -r <path>; echo rust=$?'   # re-prove the guard now passes
systemctl reset-failed <svc> && systemctl start <svc>
```
`reset-failed` is required — after enough failures systemd refuses further starts with `Start request repeated too quickly`.

**Clear the whole dependency chain, then re-probe the readers.** Units wired `Requires=`/`After=`
onto the failed service are left holding `Dependency failed for <peer>.service` and their own failed
jobs — start them after the parent is healthy. Then re-probe every organ that *reports metrics
derived from* the recovered unit: their fields moving from `UNMEASURED` back to real values is the
only proof the recovery reached the consumers. Finish with `systemctl --failed` and clear any
leftover probe units (`diag-*`, `permprobe`) so the next audit starts from a clean board.

**Sweep for the same bomb after fixing one:** other guarded files can share the shape and only detonate when someone hardens them next.
```bash
find <unit-root> -maxdepth 4 -type f ! -perm -o+r | head -30
```
Any file in that list that appears in an `ExecStartPre` will fail the same way the moment it stops being world-readable.

**Do not "fix" this by loosening permissions or by deleting the precondition.** Both trade a real access control for a green light. Owner-change keeps the boundary intact.

**A degraded-posture claim is not a liveness claim.** A session report that says the system was verified/degraded/SABAR can coexist with the unit being dead — degraded reporting and crash-looping are different states. `systemctl is-active <svc>` is its own probe; run it before repeating any health verdict.

**A null metric with an `unreachable` note is an ABSENT value, not a low one.** An organ that reads
its scalars from an upstream will report them honestly as unavailable when that upstream is down:
```
{"W3": {"status": "UNMEASURED", "note": "<upstream> unreachable: [Errno 111] Connection refused"}}
```
Read the note, not just the key. The reporting organ is healthy; every figure derived from that
upstream is *unverifiable at that instant* and must not be quoted as a measurement, a zero, or a
degradation. Restore the upstream and re-derive each headline number before repeating it.

**A document authored while the verifier was offline is a draft, not a record** — regardless of its
ratification header. A status claim of "verified / wired / ready" made during a verifier outage is
unverifiable, which is a stronger defect than merely unproven: the substrate that would have
contradicted it was unavailable. Re-derive every figure after recovery and state which were obtained
before vs after. Check `systemctl --failed` *first* in any audit that consumes health output.

## Config that rewrites itself (Hermes `config.yaml`)

Hermes normalises and rewrites `~/.hermes/config.yaml` at gateway start — it reindents, reorders provider/fallback lists, and drops keys it does not recognise. A hand-added provider entry, or a hand-set fallback order, can vanish or reorder on the next restart.

- Write config through the CLI: `hermes config set <key> <value> [--force]`, read it back with `hermes config get <key>`.
- **After a restart, re-read the key** — the effective value Hermes reports, not the file you wrote, is the truth.
- `hermes gateway restart` can hang (prints nothing, same PID minutes later). Kill it and use `systemctl restart hermes-asi-gateway`, which returns a new PID.
- Restart from a shell **outside** the gateway conversation, or the SIGTERM propagates and kills the restart command itself.

## Verify with the federation doctor

```bash
bash /root/scripts/doctor.sh          # NOTE: /root/scripts/, not /root/AAA/scripts/
```

Ends with `PASS: N  WARN: N  FAIL: N` and a `VERDICT:`. Organs appear as `name :port (UP+LOADED)`. A `WARN` on a slow-but-serving organ is not a failure; only `FAIL` is.

## Pitfalls

- **Do not declare a service "down" from a single timeout.** Check `systemctl show <svc> --property=ActiveState` and `ss -tlnp` first. An HTTP 401/403 on `/health` means **UP but auth-gated** — not down.
- **Do not read limits by grepping unit files.** `systemctl set-property` drop-ins live in `/etc/systemd/system.control/` and can win over the authored `.service.d/` values.
- **A crash loop plus a stale credential is usually two independent faults.** Fix the code path AND the env, then verify both once — restarting alone will not clear either.
- **After raising a limit, confirm with `systemctl show`.** Editing the drop-in without `daemon-reload` + restart changes nothing at runtime.
- **Record the before/after**: `uptime`, `free -h`, and the service's `curl %{time_total}` before and after — the receipt proves the fix, not the restart.
- **A restart that fails in `ExecStartPre` never reaches your code.** Add a traceback, a config, or a dependency and it will still fail identically — check the precondition commands first, not last.
- **`iptables ... Permission denied` in the journal is usually decorative noise**, not the cause: those `ExecStartPre` lines carry a `-` prefix (failure tolerated) precisely so they cannot block the unit. Read which command actually returned non-zero.
- A wedged service that fronts every user turn (a gateway, a kernel) shows up as *user-facing latency*, not as an outage. Trace the user-visible symptom to the slowest hop before optimising anything else.
