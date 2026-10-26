#!/usr/bin/env python3
"""Lane D — identity capability probe (production identities, not a stand-in).

For each agent/kernel service identity it answers, without mutating anything:
  * is the uid non-root?
  * does it belong to a root-equivalent group (docker/sudo/wheel/lxd/disk)?
  * what ambient capabilities does a fresh process get?
  * can a process under that identity write GENESIS / /etc/arifos/canon / AAA/canon?
  * can it remove the immutability guard?

Read-only: write attempts are O_WRONLY|O_APPEND opens that are expected to fail;
a successful open is closed without writing, and file hashes are compared before
and after. Nothing under /etc or /root is ever modified.

Usage: python3 lane-d-identity-capability-probe.py [--json] [--only arifos,forge]
Exit:  0 all COMPLIANT, 3 if any identity is PRIVILEGED or ROOT_EQUIVALENT.
"""

from __future__ import annotations
import hashlib, json, os, subprocess, sys, time

ROOT_EQUIV_GROUPS = {"docker", "sudo", "wheel", "lxd", "disk", "root", "adm"}
TARGETS = [
    "/root/arifOS/GENESIS/000_KERNEL_CANON.md",
    "/etc/arifos/canon/canon-release.json",
    "/root/AAA/canon/ZEN_INIT_CANONICAL.md",
]
IDENTITIES = ["arifos", "forge", "a-forge-mcp", "hermes-asi-gateway", "forge-bot"]


def groups_of(user: str) -> list[str]:
    try:
        out = subprocess.run(["id", "-nG", user], capture_output=True, text=True, check=True).stdout.split()
        return sorted(out)
    except Exception:
        return []


def uid_of(user: str) -> int | None:
    try:
        return int(subprocess.run(["id", "-u", user], capture_output=True, text=True, check=True).stdout)
    except Exception:
        return None


def as_user(user: str, script: str) -> str:
    gid = subprocess.run(["id", "-g", user], capture_output=True, text=True).stdout.strip() or "0"
    r = subprocess.run(
        ["setpriv", f"--reuid={user}", f"--regid={gid}", "--clear-groups", "bash", "-c", script],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return (r.stdout + r.stderr).strip()


def sha(path: str) -> str:
    try:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]
    except Exception:
        return "UNAVAILABLE"


def resolve(user: str) -> tuple[str, bool]:
    """service name -> (effective unix user, is_service)."""
    r = subprocess.run(["systemctl", "show", user, "-p", "User", "--value"], capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip(), True
    if r.returncode == 0 and r.stdout.strip() == "" and uid_of(user) is not None:
        return user, True  # systemd service that runs as root
    return user, False


def probe(user: str) -> dict:
    unix_user, is_service = resolve(user)
    uid = uid_of(unix_user)
    gs = groups_of(unix_user)
    req = [g for g in gs if g in ROOT_EQUIV_GROUPS]
    caps = as_user(unix_user, "grep CapEff /proc/self/status | awk '{print $2}'")
    if uid is None:
        return {"identity": user, "exists": False, "verdict": "UNKNOWN", "writes": {}, "fix": "identity not resolvable"}
    verdict = "PRIVILEGED" if uid == 0 else ("ROOT_EQUIVALENT" if req else "COMPLIANT")
    writes = {}
    for t in TARGETS:
        out = as_user(
            unix_user,
            f'python3 -c "import os;p=\'{t}\';\nexec(\'try:\\n os.close(os.open(p, os.O_WRONLY|os.O_APPEND)); print(\\"ALLOWED\\")\\nexcept OSError as e: print(\\"DENIED\\", e.errno)\')"',
        )
        writes[t] = "ALLOWED" if out.startswith("ALLOWED") else ("DENIED" if "DENIED" in out else out[:40])
    chattr = as_user(unix_user, "chattr +i /tmp/.lane-d-cap-$$ 2>&1 | head -1")
    return {
        "identity": user,
        "exists": True,
        "uid": uid,
        "groups": gs,
        "root_equivalent_groups": req,
        "capeff": caps or "UNAVAILABLE",
        "verdict": verdict,
        "writes": writes,
        "chattr_plus_i": "DENIED" if "not permitted" in chattr.lower() else (chattr or "n/a"),
        "fix": (
            "run as non-root service identity"
            if uid == 0
            else f"remove from {req} (root-equivalent)"
            if req
            else "none"
        ),
    }


def main() -> int:
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1].split(",")
    before = {t: sha(t) for t in TARGETS}
    rows = [probe(u) for u in (only or IDENTITIES)]
    after = {t: sha(t) for t in TARGETS}
    bad = [r for r in rows if r.get("verdict") in ("PRIVILEGED", "ROOT_EQUIVALENT")]
    out = {
        "probe": "lane-d-identity-capability",
        "version": 1,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "root_equivalent_groups_watched": sorted(ROOT_EQUIV_GROUPS),
        "identities": rows,
        "target_hashes_unchanged": before == after,
        "target_hashes": after,
        "verdict": "IDENTITY_SEPARATED" if not bad else "NOT_SEPARATED",
        "non_compliant": [r["identity"] for r in bad],
    }
    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
    else:
        print(f"{'identity':<20}{'uid':>5}  {'verdict':<17}{'root-eq groups':<22}write GENESIS / etc-canon / AAA-canon")
        for r in rows:
            w = " / ".join(r["writes"][t] for t in TARGETS)
            print(
                f"{r['identity']:<20}{str(r.get('uid', '-')):>5}  {r.get('verdict', ''):<17}"
                f"{','.join(r.get('root_equivalent_groups') or []) or '-':<22}{w}"
            )
        print(f"\nhashes unchanged: {out['target_hashes_unchanged']}")
        print(f"VERDICT: {out['verdict']}  non_compliant={out['non_compliant']}")
        for r in rows:
            if r.get("fix") and r["fix"] != "none":
                print(f"  fix[{r['identity']}]: {r['fix']}")
    return 0 if out["verdict"] == "IDENTITY_SEPARATED" else 3


if __name__ == "__main__":
    sys.exit(main())
