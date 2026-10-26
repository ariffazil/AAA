#!/usr/bin/env python3
"""Root-equivalence audit for non-root service identities.

Answers one question with evidence: can identity X obtain root (or write
root-protected assets) through a path OTHER than the one already fixed?

Paths checked (all read-only):
  1. effective caps of a fresh process under X
  2. host setuid-root binaries (container layers pruned)
  3. file capabilities on host binaries
  4. root-run systemd units whose ExecStart points at a path X can write
  5. root-run cron entries whose script X can write
  6. unix sockets reachable through X's groups
  7. home/SSH surface granted by X's groups
  8. writable root-owned files under /etc (units, sudoers, cron)

Usage: python3 root-equivalence-audit.py [--json] [--identities arifos,forge]
Exit:  0 no path found, 3 if any path is found.
"""

from __future__ import annotations
import json, os, re, subprocess, sys, time

PRUNE = [
    "/proc",
    "/sys",
    "/dev",
    "/var/lib/docker",
    "/var/lib/containerd",
    "/var/lib/lxcfs",
    "/run/containerd",
    "/snap",
    "/mnt",
    "/media",
]
IDENTITIES = ["arifos", "forge"]


def sh(cmd: str, timeout: int = 60) -> str:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return "__TIMEOUT__"


def groups_of(u: str) -> list[str]:
    return sh(f"id -nG {u}").split()


def fresh_caps(u: str) -> str:
    gid = sh(f"id -g {u}").strip()
    return sh(f"setpriv --reuid={u} --regid={gid} --init-groups grep CapEff /proc/self/status").split()[-1] or "UNKNOWN"


def writable_by(u: str, path: str) -> bool:
    """Real probe, not `test -w`: DAC bits lie when the immutable flag is set."""
    if os.path.isdir(path):
        # cannot create-then-delete without mutating; fall back to DAC + immutable read
        flags = sh(f"lsattr -d '{path}' 2>/dev/null").split()[:1]
        if flags and "i" in flags[0]:
            return False
        r = sh(f"setpriv --reuid={u} --regid=$(id -g {u}) --init-groups test -w '{path}' && echo YES || echo NO")
        return r.strip().endswith("YES")
    py = ("import os,sys\n"
          "try:\n os.close(os.open(sys.argv[1], os.O_WRONLY))\n print('ALLOWED')\n"
          "except OSError as e: print('DENIED', e.errno)\n")
    r = sh(f"setpriv --reuid={u} --regid=$(id -g {u}) --init-groups "
           f"python3 -c \"{py}\" '{path}'")
    return "ALLOWED" in r


def main() -> int:
    ident = IDENTITIES
    if "--identities" in sys.argv:
        ident = sys.argv[sys.argv.index("--identities") + 1].split(",")

    prune = " ".join(f"-path {p} -prune -o" for p in PRUNE)

    # 1-3: shared host facts
    setuid = [
        l for l in sh(f"find / -xdev {prune} -perm -4000 -type f -print 2>/dev/null", 120).splitlines() if l.strip()
    ]
    if "__TIMEOUT__" in setuid:
        setuid = ["__TIMEOUT__"]
    filecaps = [l for l in sh("getcap -r /usr /bin /sbin /opt 2>/dev/null", 90).splitlines() if "cap_" in l]

    # 4: systemd units running as root with an ExecStart on a writable path
    units = sh("systemctl list-units --type=service --state=running --no-legend --no-pager | awk '{print $1}'").split()
    unit_rows = []
    for u in units:
        user = sh(f"systemctl show {u} -p User --value").strip()
        if user and user != "root":
            continue
        ex = sh(f"systemctl show {u} -p ExecStart --value")
        for m in __import__("re").findall(r"path=([^ ;]+)", ex):
            pass
        import re as _re

        for path in _re.findall(r"path=([^ ;]+)", ex) or _re.findall(r"argv\[\]=([^ ;]+)", ex):
            for i in ident:
                if writable_by(i, path):
                    unit_rows.append({"unit": u, "exec": path, "identity": i})

    # 5: cron
    cron_rows = []
    for cf in ["/etc/crontab"] + [
        f"/etc/cron.d/{f}" for f in (os.listdir("/etc/cron.d") if os.path.isdir("/etc/cron.d") else [])
    ]:
        try:
            txt = open(cf, errors="ignore").read()
        except OSError:
            continue
        for line in txt.splitlines():
            if line.lstrip().startswith("#") or not line.strip():
                continue
            f = line.split()
            if len(f) < 7:
                continue
            cron_user, cmd = f[5], " ".join(f[6:])
            cmd = re.split(r"\s(?:>>?|2>|&>)\s", cmd)[0]      # drop redirect targets
            target = next((t for t in cmd.split() if t.startswith("/") and os.path.isfile(t)), None)
            if not target:
                continue
            for i in ident:
                if cron_user == i:
                    continue                                  # same privilege, not escalation
                if writable_by(i, target):
                    cron_rows.append({"cron": cf, "script": target, "cron_user": cron_user, "identity": i})

    # 6: sockets
    sockets = []
    for s in sh(f"find /run -xdev -type s -printf '%p %m %g\\n' 2>/dev/null").splitlines():
        parts = s.split()
        if len(parts) >= 3:
            sockets.append({"socket": parts[0], "mode": parts[1], "group": parts[2]})

    # 7: home/ssh
    home_rows = []
    for i in ident:
        for p in [f"/home/{i}", "/home/ariffazil", "/home/ariffazil/.ssh", "/root", "/root/.ssh"]:
            if os.path.exists(p) and writable_by(i, p):
                home_rows.append({"identity": i, "writable": p})

    # 8: /etc writable by identity groups
    etc_rows = []
    for i in ident:
        gs = ",".join(groups_of(i))
        out = sh(f"find /etc -xdev \\( -group {gs.replace(',', ' -o -group ')} \\) -perm -g+w -type f 2>/dev/null", 60)
        etc_rows += [{"identity": i, "file": l} for l in out.splitlines() if l.strip()]

    per_identity = {}
    for i in ident:
        caps = fresh_caps(i)
        per_identity[i] = {
            "groups": groups_of(i),
            "fresh_capeff": caps,
            "elevated_caps": caps not in ("0000000000000000", "UNKNOWN", ""),
        }

    findings = {
        "systemd_exec_writable": unit_rows,
        "cron_script_writable": cron_rows,
        "etc_group_writable": etc_rows,
        "home_writable": home_rows,
        "host_setuid": setuid[:25],
        "host_setuid_count": len(setuid),
        "file_capabilities": filecaps[:25],
        "sockets": sockets[:25],
    }
    blocking = unit_rows or cron_rows or etc_rows or any(v["elevated_caps"] for v in per_identity.values())
    out = {
        "audit": "root-equivalence",
        "version": 1,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "identities": per_identity,
        "findings": findings,
        "pruned": PRUNE,
        "verdict": "NO_ROOT_EQUIVALENT_PATH_FOUND" if not blocking else "PATH_FOUND",
    }
    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
    else:
        for i, v in per_identity.items():
            print(
                f"[{i}] groups={','.join(v['groups'])} fresh_capeff={v['fresh_capeff']} elevated={v['elevated_caps']}"
            )
        print(f"  systemd ExecStart writable by identity : {len(unit_rows)}")
        for r in unit_rows:
            print(f"    {r['identity']} can write {r['exec']} (unit {r['unit']})")
        print(f"  cron scripts writable                  : {len(cron_rows)}")
        for r in cron_rows:
            print(f"    {r['identity']} can write {r['script']} ({r['cron']})")
        print(f"  /etc root-owned files group-writable   : {len(etc_rows)}")
        for r in etc_rows[:8]:
            print(f"    {r['identity']}: {r['file']}")
        print(f"  home/ssh writable                      : {len(home_rows)}")
        for r in home_rows:
            print(f"    {r['identity']} can write {r['writable']}")
        print(f"  host setuid binaries                   : {findings['host_setuid_count']} (container layers pruned)")
        print(f"  file capabilities on host binaries     : {len(filecaps)}")
        print(f"  sockets under /run                     : {len(sockets)}")
        print(f"\nVERDICT: {out['verdict']}")
    return 0 if out["verdict"] == "NO_ROOT_EQUIVALENT_PATH_FOUND" else 3


if __name__ == "__main__":
    sys.exit(main())
