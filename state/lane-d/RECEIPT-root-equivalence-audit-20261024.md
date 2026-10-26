# Root-equivalence audit — `arifos` and `forge` (2026-10-24T03:4xZ)

**Question:** after removing `arifos` from the `docker` group, can either non-root service identity still reach root (or write root-protected assets) through another path?

**Tool:** `/root/AAA/state/lane-d/root-equivalence-audit.py` (read-only; exits 0 = no path, 3 = path found)
**Verdict:** `NO_ROOT_EQUIVALENT_PATH_FOUND` for both identities.

| Path class | Method | Result |
|---|---|---|
| effective capabilities of a fresh process | `setpriv --init-groups` + `/proc/self/status` | `CapEff=0x0` for both — no ambient caps |
| root-run systemd units whose `ExecStart` the identity can write | `systemctl show` × running services + real open probe | **0** |
| root-run cron targets writable by the identity | parse `/etc/cron.d/*`, drop redirect targets, require a privilege boundary (`cron_user ≠ identity`) | **0** |
| root-owned files under `/etc` group-writable via the identity's groups (units, sudoers, cron) | `find /etc -group ... -perm -g+w` | **0** |
| group-reachable unix sockets | `find /run -type s` + group match | 85 sockets; none root-equivalent (only `/run/mailgw/broker.sock` reachable, mail) |
| writable `PATH` entries | `echo $PATH` loop under the identity | **0** |
| host setuid binaries | bounded scan of standard dirs (container layers pruned) | 26 — stock Ubuntu set (`passwd`, `su`, `mount`, `firejail`, `at`, `ssh-keysign`, …); `su` needs a root password |
| file capabilities on host binaries | `getcap -r /usr/bin /usr/sbin /bin /sbin /usr/local/bin /opt` | ping/mtr `cap_net_raw` only — not root-equivalent |
| home surface granted by groups | real open probe | `arifos` can write `/home/arifos` (its own home) |

## Method correction during the audit (matters)

The first run reported a **false positive**: `/etc/cron.d/arifos-repo-audit` runs `/root/A-FORGE/scripts/repo-audit.sh` as **root**, and `forge` "could write" it according to `test -w`.

`test -w` checks DAC bits only. The file carries `+i`, and `forge` has `CapEff=0x0` — so:

```
forge open(O_WRONLY) on repo-audit.sh   → EPERM (errno 1)
forge chattr -i on repo-audit.sh        → EPERM
```

No escalation. The probe was fixed to perform a **real open attempt** instead of trusting `test -w`, and the cron parser was narrowed to *executed targets across a privilege boundary* (a cron job running as `arifos` writing its own log is not escalation).

Lesson: **`test -w` lies when the immutable flag is set.** DAC permission is necessary, not sufficient, for writability.

## What remains — not escalation, still exposure

`/opt/arifos` is genuinely writable by the kernel's own groups (verified with a real open attempt, not `test -w`):

```
/opt/arifos/commands/init.md      flags: --------------e-------   WRITE_ALLOWED (uid 994)
/opt/arifos/app                   (dir)                          WRITE_ALLOWED
/opt/arifos/.gitleaks.toml        flags: --------------e-------   WRITE_ALLOWED
/opt/arifos/venv                  read-only
```

That is self-modification of the kernel's own runtime (prompt commands, scanner config), not privilege escalation — it already runs as that identity. `fhs-map.yaml` declares `never_write: /opt/arifos`, so this is a declared-vs-live gap. Tracked as `p2-opt-arifos-group-writable` (T2).

## Out of scope of this audit

- `a-forge-mcp`, `hermes-asi-gateway`, `forge-bot` remain **uid 0** and can write `/etc/arifos/canon` (`p1-root-agent-services-write-canon`).
- The running kernel `MainPID` still holds gid 989 until its next restart.

## Reproduce

```
python3 /root/AAA/state/lane-d/root-equivalence-audit.py            # table
python3 /root/AAA/state/lane-d/root-equivalence-audit.py --json     # receipt
```
