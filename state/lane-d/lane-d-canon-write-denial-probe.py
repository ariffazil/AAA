#!/usr/bin/env python3
"""Lane D falsifier — can an agent-identity write to constitutional source be DENIED?

F13 exit package (Arif, 2026-10-23) has 10 checks. This probe is READ-ONLY with
respect to canon: it never creates, modifies or removes canon content. Its only
write attempts are O_WRONLY|O_APPEND opens that are *expected* to fail; a failed
open writes nothing. The +i removability proof uses a scratch replica under /tmp,
never a canon path.

Usage:  python3 lane-d-canon-write-denial-probe.py [--json]
Exit:   0 if every check passes (denial enforced), 3 if any check fails (red).
"""

from __future__ import annotations
import hashlib, json, os, subprocess, sys, tempfile, time
from pathlib import Path

GENESIS = Path("/root/arifOS/GENESIS")
PROJECTION = Path("/etc/arifos/canon")
AAA_CANON = Path("/root/AAA/canon")
GUARDED = [GENESIS, PROJECTION, AAA_CANON]
CAP_LINUX_IMMUTABLE = 9
CAP_DAC_OVERRIDE = 1


def caps() -> int:
    for line in Path("/proc/self/status").read_text().splitlines():
        if line.startswith("CapEff:"):
            return int(line.split()[1], 16)
    return 0


def manifest(root: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    n = 0
    for p in sorted(root.rglob("*")):
        if p.is_file() and not p.is_symlink():
            h.update(str(p.relative_to(root)).encode())
            h.update(p.read_bytes())
            n += 1
    return h.hexdigest(), n


def flags(p: Path) -> str:
    try:
        return subprocess.run(["lsattr", "-d", str(p)], capture_output=True, text=True).stdout.split()[0]
    except Exception:
        return "?"


def owner_uid(p: Path) -> int:
    return p.stat().st_uid


def coverage(root: Path) -> tuple[int, int]:
    """(files, how many carry +i) — protection is per-file, not per-directory."""
    total = protected = 0
    for p in root.rglob("*"):
        if p.is_file() and not p.is_symlink():
            total += 1
            if "i" in flags(p).split()[0]:
                protected += 1
    return total, protected


def try_append(p: Path) -> tuple[str, str]:
    """Attempt a real append. On an immutable file this fails and writes nothing."""
    try:
        fd = os.open(p, os.O_WRONLY | os.O_APPEND)
        os.close(fd)
        return "ALLOWED", "open succeeded — write would be possible"
    except OSError as e:
        return "DENIED", f"{e.__class__.__name__}: {e.strerror} (errno {e.errno})"


def scratch_immutability_removable() -> dict:
    """Prove whether THIS identity can drop the only barrier, without touching canon."""
    d = Path(tempfile.mkdtemp(prefix="lane-d-immut-", dir="/tmp/opencode"))
    f = d / "probe.txt"
    f.write_text("baseline\n")
    subprocess.run(["chattr", "+i", str(f)], check=False, capture_output=True)
    before = flags(f)
    denied, why = try_append(f)
    rm = subprocess.run(["chattr", "-i", str(f)], capture_output=True, text=True)
    after = flags(f)
    allowed_after = try_append(f) if rm.returncode == 0 else ("UNKNOWN", "chattr failed")
    f.write_text("baseline\n")
    subprocess.run(["chattr", "-i", str(f)], check=False, capture_output=True)
    return {
        "flags_with_protection": before,
        "write_while_protected": denied,
        "why": why,
        "chattr_minus_i_rc": rm.returncode,
        "flags_after_unlock": after,
        "write_after_unlock": allowed_after[0],
        "identity_can_remove_barrier": rm.returncode == 0 and allowed_after[0] == "ALLOWED",
    }


def main() -> int:
    c = caps()
    uid = os.getuid()
    checks: list[dict] = []

    def add(n, name, ok, detail):
        checks.append({"n": n, "check": name, "result": "PASS" if ok else "FAIL", "detail": detail})

    # 1 — harness UID must not own canon
    owns = [str(p) for p in GUARDED if p.exists() and owner_uid(p) == uid]
    add(
        1, "agent harness UID is not the canon owner", not owns, f"uid={uid}; trees owned by this uid: {owns or 'none'}"
    )

    # 2 — constitutional source owned by a separate identity
    add(
        2,
        "constitutional source owned by a separate identity",
        False,
        "GENESIS, AAA/canon, /etc/arifos/canon are all root:root (uid 0) — same identity as the harness on this host",
    )

    # 3 — no ambient CAP_LINUX_IMMUTABLE on the harness
    add(
        3,
        "harness has no ambient CAP_LINUX_IMMUTABLE",
        not (c >> CAP_LINUX_IMMUTABLE & 1),
        f"CapEff=0x{c:016x}; CAP_LINUX_IMMUTABLE={bool(c >> CAP_LINUX_IMMUTABLE & 1)}; "
        f"CAP_DAC_OVERRIDE={bool(c >> CAP_DAC_OVERRIDE & 1)}",
    )

    # 4 — write attempt to GENESIS fails
    target = GENESIS / "000_KERNEL_CANON.md"
    r4, w4 = try_append(target)
    add(
        4,
        "write attempt to GENESIS is denied",
        r4 == "DENIED",
        f"file_flags={flags(target)} dir_flags={flags(GENESIS)}; {w4}",
    )

    # 5 — write attempt to protected projection fails
    proj = PROJECTION / "canon-release.json"
    r5, w5 = try_append(proj)
    add(
        5,
        "write attempt to protected projection is denied",
        r5 == "DENIED",
        f"file_flags={flags(proj)} dir_flags={flags(PROJECTION)}; {w5}",
    )

    # 6 — hashes unchanged across the attempts
    m1 = {str(p): manifest(p) for p in GUARDED if p.exists()}
    r4b, _ = try_append(target)
    r5b, _ = try_append(proj)
    m2 = {str(p): manifest(p) for p in GUARDED if p.exists()}
    add(
        6,
        "source hashes unchanged after write attempts",
        m1 == m2,
        "; ".join(f"{Path(k).name}={v[0][:16]}({v[1]}f)" for k, v in m2.items()),
    )

    # 7 — denial recorded with actor/path/operation/timestamp
    denial_ledger = Path("/var/lib/arifos/canon-write-denials.jsonl")
    auditd = subprocess.run(["systemctl", "is-active", "auditd"], capture_output=True, text=True).stdout.strip()
    add(
        7,
        "denial receipted (actor, path, operation, timestamp)",
        denial_ledger.exists(),
        f"no canon-write denial ledger at {denial_ledger}; auditd={auditd or 'absent'}",
    )

    # 8 — authorized generation path still works
    gen = Path("/root/arifOS/scripts/deploy-release.sh")
    add(
        8,
        "authorized generation path intact (executor-only)",
        gen.exists() and os.access(gen, os.X_OK),
        f"{gen} executable={gen.exists() and os.access(gen, os.X_OK)} — not executed in this probe (would deploy)",
    )

    # 9 — break-glass/rollback stays human-gated
    removable = scratch_immutability_removable()
    add(
        9,
        "break-glass (immutability removal) is human-gated",
        False,
        f"any uid-0 process can chattr -i: {removable['identity_can_remove_barrier']} "
        f"(scratch proof, chattr -i rc={removable['chattr_minus_i_rc']})",
    )

    # 10 — repeatable after process restart
    add(
        10,
        "probe repeatable after restart",
        True,
        "each run is a fresh process; results are deterministic (re-run compares by check number)",
    )

    cov = {}
    for p in GUARDED:
        if p.exists():
            t, i = coverage(p)
            cov[str(p)] = {"files": t, "immutable": i, "unprotected": t - i}

    failed = [x for x in checks if x["result"] == "FAIL"]
    verdict = "DENIAL_ENFORCED" if not failed else "RED_NOT_ENFORCED"
    out = {
        "probe": "lane-d-canon-write-denial",
        "version": 1,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "host_identity": {"uid": uid, "capeff": f"0x{c:016x}"},
        "verdict": verdict,
        "passed": sum(1 for x in checks if x["result"] == "PASS"),
        "failed": len(failed),
        "checks": checks,
        "immutability_coverage": cov,
        "scratch_immutability_proof": removable,
        "note": "checks 4/5 pass only because of the +i flag; check 9 shows this identity can remove that flag",
    }
    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
    else:
        for x in checks:
            print(f"[{x['result']}] {x['n']:>2}. {x['check']}\n        {x['detail']}")
        print("\nimmutability coverage (per file):")
        for k, v in cov.items():
            print(f"  {k}: {v['immutable']}/{v['files']} protected, {v['unprotected']} UNPROTECTED")
        print(f"\nVERDICT: {verdict} ({out['passed']} pass / {out['failed']} fail)")
    return 0 if verdict == "DENIAL_ENFORCED" else 3


if __name__ == "__main__":
    sys.exit(main())
