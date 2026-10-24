# Docker group removal — `arifos` (T2, executed 2026-10-24T03:22Z)

**Change:** `gpasswd -d arifos docker`
**Why:** uid 994 ran non-root (DAC correctly denied canon writes) but held `docker` group membership, which is root-equivalent via the socket. One `docker run -v /etc:/host` restored full host write. The kernel's non-root posture was nominal (ambient authority inherited from configuration, not from capability).

## Before

```
groups(arifos)        arifos nogroup docker ariffazil arifos-auth mailgw-clients
proc <MainPID> Groups 969 971 983 989 1002 65534
docker as arifos      ALLOWED — 12 containers listed
```

## Mutation

```
$ gpasswd -d arifos docker
Removing user arifos from group docker
```

## After — fresh identity context (`runuser`, which calls initgroups)

```
groups(arifos)        arifos nogroup ariffazil arifos-auth mailgw-clients
docker as arifos      DENIED  (Permission denied on /var/run/docker.sock)
docker info as arifos DENIED
writable system paths /etc, /etc/systemd/system, docker.sock, /root → none
```

Lane D identity probe: `arifos` flipped **ROOT_EQUIVALENT → COMPLIANT**; still `DENIED / DENIED / DENIED` on the three canon targets. Canon integrity unchanged: `3/3`, version `2026.10.23-e8dd4ab`.

Full probe verdict is still `NOT_SEPARATED`, because three services remain uid 0: `a-forge-mcp`, `hermes-asi-gateway`, `forge-bot` (all measured `ALLOWED` on `/etc/arifos/canon`).

## Why this does not break anything

The **only** docker consumer in kernel code is `arifosmcp/runtime/webmcp/live_metrics.py:199-204`, wrapped in `try/except: pass` — losing the socket sets `docker_containers / docker_running / docker_images` to `0`.

A **narrow, pre-existing, documented** path covers the legitimate monitoring need:

```
/etc/sudoers.d/arifosd-docker:2
arifos ALL=(root) NOPASSWD: /usr/bin/docker ps --format *
# "Allow arifos to run docker ps for organ monitoring (no docker run/exec)"
```

So the read-only monitoring capability survives without ambient root-equivalence.

## Residual (stated, not hidden)

- The **running kernel process still holds gid 989** in `/proc/<MainPID>/status` — group membership is set at exec. The removal bites for every new context; the live process keeps the inherited credential until its next restart (≈8s, or automatically at the next deploy/reboot).
- `arifos` remains in group `ariffazil` (1002) — read access to the human's home area, not root-equivalent, not measured further. Flagged, not touched.
- Three root services remain (see `p1-root-agent-services-write-canon`).

## Other root-equivalent paths — tested, not assumed (2026-10-24T03:30Z)

| Path | Result |
|---|---|
| sudo | one rule only: `NOPASSWD: /usr/bin/docker ps --format *` — read-only, **no `run`/`exec`**, documented in `/etc/sudoers.d/arifosd-docker` |
| root-owned files writable via arifos's groups, under `/etc` (units, sudoers, cron) | **none** |
| group-reachable sockets under `/run` | only `/run/mailgw/broker.sock` (mail), not root-equivalent |
| writable entries on `PATH` | **none** |
| host setuid binaries | scan **incomplete** — timed out inside `/var/lib/docker` layers; every hit returned was a container-layer file, not a host path. **Not claimed as tested.** |

**New finding (not escalation, hygiene):** 898 files under `/opt/arifos` are group-writable by the kernel's own groups — including `commands/*.md`, `.gitleaks.toml`, `app/`, `staging-*`, and `current/venv/.../site-packages/commands/*.md`. `/opt/arifos/app` and `/opt/arifos/commands` are writable; `/opt/arifos/venv` is read-only. This is self-modification of the kernel's own runtime, not privilege escalation (it already runs as that identity), but `fhs-map.yaml` declares `never_write: /opt/arifos`. Declared ≠ live. Logged as `p2-opt-arifos-group-writable`.

## Precise claim (replaces the earlier over-broad sentence)

> **Through the tested Docker path, the `arifos` identity in a fresh context no longer acquires root-equivalent power. Other paths and the three UID-0 services remain in a separate audit scope.**

Not: "the kernel can no longer regain constitution write power through any new context" — that universal was never tested.


## Rollback

```
gpasswd -a arifos docker     # group entry restored
systemctl restart arifos     # only if the live process must regain it immediately
```
