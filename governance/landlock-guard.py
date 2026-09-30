#!/usr/bin/env python3
"""
landlock-guard — OS-level write-set asymmetry for arifOS agent processes.

Implements (C) monotonic tightening from the Godel-lock survey
(/root/AAA/reports/godel-lock-2026-09-29.md): a Landlock sandbox that is
deny-by-default on write rights, allow-list on the agent's legitimate work
dirs, and binds even when the process runs as root.

Why Landlock is the correct primitive (not chmod, not a shell guard):
  - Landlock restricts the *process*, independent of uid. A root process that
    restricts itself CANNOT lift the restriction (restrict_self is monotonic —
    a process may only add rules, never remove). This is the OS form of
    "policy may only tighten, never widen."
  - chmod/ownership is meaningless while agents run as root (root bypasses it).
    The mail-gateway audit verdict was exactly this: ENFORCED_WITH_ROOT_RESIDUAL
    because the *caller processes were unconfined*.

Usage:
  landlock-guard.py --policy policy.json -- COMMAND [ARGS...]
  landlock-guard.py --probe [--policy policy.json]   # inspect, don't restrict

No pip dependency: pure ctypes against the Landlock syscalls (kernel >= 5.13).
The ABI is queried live, so REFER/TRUNCATE rights are masked off on older kernels.
"""

import ctypes
import json
import os
import sys

# ── Landlock syscall numbers (x86-64) ─────────────────────────────────────
SYS_landlock_create_ruleset = 444
SYS_landlock_add_rule = 445
SYS_landlock_restrict_self = 446

LANDLOCK_RULE_PATH_BENEATH = 1
LANDLOCK_CREATE_RULESET_VERSION = 1  # query-only flag (attr=NULL, size=0)

ACCESS_FS_EXECUTE = 1 << 0
ACCESS_FS_WRITE_FILE = 1 << 1
ACCESS_FS_READ_FILE = 1 << 2
ACCESS_FS_READ_DIR = 1 << 3
ACCESS_FS_REMOVE_DIR = 1 << 4
ACCESS_FS_REMOVE_FILE = 1 << 5
ACCESS_FS_MAKE_CHAR = 1 << 6
ACCESS_FS_MAKE_DIR = 1 << 7
ACCESS_FS_MAKE_REG = 1 << 8
ACCESS_FS_MAKE_SOCK = 1 << 9
ACCESS_FS_MAKE_FIFO = 1 << 10
ACCESS_FS_MAKE_BLOCK = 1 << 11
ACCESS_FS_MAKE_SYM = 1 << 12
ACCESS_FS_REFER = 1 << 13  # ABI v2+
ACCESS_FS_TRUNCATE = 1 << 14  # ABI v3+

RIGHT_BITS = {
    "EXECUTE": ACCESS_FS_EXECUTE,
    "WRITE_FILE": ACCESS_FS_WRITE_FILE,
    "READ_FILE": ACCESS_FS_READ_FILE,
    "READ_DIR": ACCESS_FS_READ_DIR,
    "REMOVE_DIR": ACCESS_FS_REMOVE_DIR,
    "REMOVE_FILE": ACCESS_FS_REMOVE_FILE,
    "MAKE_REG": ACCESS_FS_MAKE_REG,
    "MAKE_DIR": ACCESS_FS_MAKE_DIR,
    "MAKE_SYM": ACCESS_FS_MAKE_SYM,
    "REFER": ACCESS_FS_REFER,
    "TRUNCATE": ACCESS_FS_TRUNCATE,
}

WRITE_SET = (
    ACCESS_FS_WRITE_FILE
    | ACCESS_FS_TRUNCATE
    | ACCESS_FS_REMOVE_FILE
    | ACCESS_FS_REMOVE_DIR
    | ACCESS_FS_MAKE_REG
    | ACCESS_FS_MAKE_DIR
    | ACCESS_FS_MAKE_SYM
    | ACCESS_FS_REFER
)


class PathBeneathAttr(ctypes.Structure):
    _fields_ = [("allowed_access", ctypes.c_uint64), ("parent_fd", ctypes.c_int32), ("_reserved", ctypes.c_uint32)]


_libc = ctypes.CDLL(None, use_errno=True)


def _abi_version() -> int:
    """Query the kernel's Landlock ABI version (attr=NULL, size=0, VERSION flag)."""
    v = _libc.syscall(SYS_landlock_create_ruleset, 0, 0, LANDLOCK_CREATE_RULESET_VERSION)
    if v < 0:
        e = ctypes.get_errno()
        raise OSError(e, f"landlock ABI query failed (errno={e})")
    return v


def _ruleset_attr_size(abi: int) -> int:
    # v1: 8 (handled_access_fs) · v4: 16 (+handled_access_net) · v6: 24 (+scoped)
    if abi >= 6:
        return 24
    if abi >= 4:
        return 16
    return 8


def _mask_available(handled: int, abi: int) -> int:
    if abi < 3:
        handled &= ~ACCESS_FS_TRUNCATE
    if abi < 2:
        handled &= ~ACCESS_FS_REFER
    return handled


def _create_ruleset(handled_fs: int, abi: int) -> int:
    size = _ruleset_attr_size(abi)
    # handled_access_fs is always the first u64 of the ruleset attr at offset 0,
    # so a raw buffer of `size` bytes with the value written at offset 0 is a
    # valid struct for any ABI version.
    buf = (ctypes.c_uint8 * size)()
    ctypes.c_uint64.from_buffer(buf).value = handled_fs
    fd = _libc.syscall(SYS_landlock_create_ruleset, buf, size, 0)
    if fd < 0:
        e = ctypes.get_errno()
        raise OSError(e, f"landlock_create_ruleset failed (errno={e}, abi={abi})")
    return fd


def _add_path_beneath(ruleset_fd: int, allowed_access: int, path: str) -> None:
    fd = os.open(path, os.O_PATH | os.O_CLOEXEC)
    try:
        attr = PathBeneathAttr(allowed_access=allowed_access, parent_fd=fd)
        r = _libc.syscall(SYS_landlock_add_rule, ruleset_fd, LANDLOCK_RULE_PATH_BENEATH, ctypes.byref(attr), 0)
    finally:
        os.close(fd)
    if r != 0:
        e = ctypes.get_errno()
        raise OSError(e, f"landlock_add_rule failed for {path!r} (errno={e})")


def _restrict_self(ruleset_fd: int) -> None:
    r = _libc.syscall(SYS_landlock_restrict_self, ruleset_fd, 0)
    if r != 0:
        e = ctypes.get_errno()
        raise OSError(e, f"landlock_restrict_self failed (errno={e})")


def load_policy(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def resolved_bits(names) -> int:
    bits = 0
    for n in names:
        if n not in RIGHT_BITS:
            raise ValueError(f"unknown right {n!r}; known: {sorted(RIGHT_BITS)}")
        bits |= RIGHT_BITS[n]
    return bits


def apply_policy(policy: dict) -> dict:
    """Create + self-restrict. Returns an audit dict of what was enforced."""
    handled = resolved_bits(policy["handled_rights"])
    abi = _abi_version()
    handled = _mask_available(handled, abi)

    allow_write = policy.get("allow_write", [])
    protected = policy.get("protected", [])

    # assert protected paths are not allow-listed (write-set asymmetry invariant)
    allow_real = [os.path.realpath(p) for p in allow_write]
    for p in protected:
        rp = os.path.realpath(p)
        for ap in allow_real:
            if rp == ap or rp.startswith(ap.rstrip("/") + "/"):
                raise SystemExit(
                    f"POLICY ERROR: protected path {p!r} is inside allow_write {ap!r} "
                    f"— that defeats the lock. Refusing to run."
                )

    ruleset_fd = _create_ruleset(handled, abi)
    for p in allow_write:
        _add_path_beneath(ruleset_fd, handled, p)
    _restrict_self(ruleset_fd)

    return {
        "abi": abi,
        "handled_rights": policy["handled_rights"],
        "handled_bits": hex(handled),
        "allow_write": allow_write,
        "protected": protected,
    }


def main(argv):
    if not argv or argv[0] in ("--help", "-h"):
        print(__doc__)
        return 0

    if argv[0] == "--probe":
        policy_path = None
        if len(argv) >= 3 and argv[1] == "--policy":
            policy_path = argv[2]
        abi = _abi_version()
        print(f"probe: kernel Landlock ABI v{abi}")
        if policy_path is not None:
            policy = load_policy(policy_path)
            handled = _mask_available(resolved_bits(policy["handled_rights"]), abi)
            print(f"probe: would handle rights {policy['handled_rights']} (bits {hex(handled)})")
            print(f"probe: allow_write = {policy.get('allow_write', [])}")
            print(f"probe: protected   = {policy.get('protected', [])}")
        return 0

    if argv[0] != "--policy":
        print("error: expected --policy <json> [-- COMMAND...] or --probe", file=sys.stderr)
        return 2
    policy_path = argv[1]
    rest = argv[2:]
    if rest and rest[0] == "--":
        rest = rest[1:]

    policy = load_policy(policy_path)
    audit = apply_policy(policy)
    print(f"[landlock-guard] confined: {json.dumps(audit)}", file=sys.stderr)

    if not rest:
        return 0

    os.execvp(rest[0], rest)
    return 127


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
