#!/usr/bin/env python3
"""name_only_env_probe — inspect process environments and secret stores WITHOUT emitting values.

WHY THIS EXISTS
---------------
Inspecting /proc/<pid>/environ is a value-emitting operation by default. The usual reflex,
`tr '\0' '\n' < /proc/$PID/environ | grep -iE 'pattern'`, matches the regex against the VALUE as
well as the name: a filter containing `db` matches a key whose material happens to contain those
bytes, and the whole KEY=VALUE line prints into the transcript.

The defect is not the pattern. It is that a line-level filter over an environment dump cannot be
made safe by choosing better keywords.

THE RULE
--------
Inspection of process environments, systemd Environment=, and secret stores defaults to NAME-ONLY
output. Values are never emitted unless the caller supplies an explicit, exceptional authorisation,
and even then a non-interactive stdout (agent / pipe / CI) is REFUSED.

ENFORCEMENT IS STRUCTURAL, NOT ADVISORY
---------------------------------------
Every output line passes through `emit()`, and the ONLY representation of a value this module can
produce is `redact()`. There is no code path here that formats a secret into output.

USAGE
-----
    name_only_env_probe env  <pid|unit>   [--classify]   names only
    name_only_env_probe file <path>                      names only
    name_only_env_probe units                            services carrying broad secret stores
    name_only_env_probe agentcheck                       JSON: credential NAMES per live service
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

CRED_RE = re.compile(r"(APIKEY|API_KEY|_KEY$|TOKEN|SECRET|PASSWORD|_PWD|CREDENTIAL)", re.I)
VAR_RE = re.compile(r"^[A-Z_][A-Z0-9_]*$")

STORE_CANDIDATES = (
    "/root/.secrets/kunci-root.env",
    "/root/.secrets/vault.flat.env",
    "/root/.secrets/kunci-mas.flat.env",
)


# ── the only value representation this module may produce ─────────────────────

def fingerprint(value: str) -> str:
    """Non-reversible short identity. Safe to print; enough to compare hosts."""
    return hashlib.sha256(value.encode("utf-8", "replace")).hexdigest()[:12]


def redact(value: str) -> str:
    if not value:
        return "<empty>"
    return f"<redacted len={len(value)} fp={fingerprint(value)}>"


def emit(line: str) -> None:
    """Single emission point. Callers pass already-redacted text."""
    sys.stdout.write(line + "\n")


def raw_mode_refused() -> bool:
    """Raw output needs a real terminal. Agent/pipe/CI contexts are refused outright."""
    if os.environ.get("SECRETSAFE_RAW") != "1":
        return False
    return not sys.stdout.isatty()


# ── loaders ──────────────────────────────────────────────────────────────────

def load_store(path: str) -> dict[str, str]:
    out: dict[str, str] = {}
    p = Path(path)
    if not p.exists():
        return out
    for line in p.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if VAR_RE.match(k):
            out[k] = v.strip().strip('"').strip("'")
    return out


def known_names() -> set[str]:
    names: set[str] = set()
    for p in STORE_CANDIDATES:
        names |= set(load_store(p))
    return names


def read_environ(pid: str) -> dict[str, str]:
    raw = Path(f"/proc/{pid}/environ").read_bytes().decode("utf-8", "replace")
    env: dict[str, str] = {}
    for entry in raw.split("\0"):
        if "=" in entry:
            k, v = entry.split("=", 1)
            env[k] = v
    return env


def resolve(target: str) -> tuple[str, str] | None:
    if target.isdigit():
        return target, f"pid:{target}"
    name = os.path.basename(target)
    if name.endswith(".service"):
        pid = subprocess.run(
            ["systemctl", "show", name, "-p", "MainPID", "--value"],
            capture_output=True, text=True,
        ).stdout.strip()
        return (pid, name) if pid and pid != "0" else None
    return None


# ── commands ─────────────────────────────────────────────────────────────────

def cmd_env(target: str, classify: bool) -> int:
    got = resolve(target)
    if not got:
        emit(f"# cannot resolve process for {target!r} (not running?)")
        return 1
    pid, label = got
    try:
        env = read_environ(pid)
    except (FileNotFoundError, PermissionError) as exc:
        emit(f"# unreadable: {type(exc).__name__}")
        return 1

    creds = sorted(n for n in env if CRED_RE.search(n))
    emit(f"# {label} pid={pid} vars={len(env)} credential_vars={len(creds)}")
    emit("# --- credential variables (names only) ---")
    if not creds:
        emit("#   (none)")
    known = known_names() if classify else set()
    for n in creds:
        line = f"  {n:30} {redact(env[n])}"
        if classify:
            line += "  store=" + ("yes" if n in known else "-")
        emit(line)
    emit("# --- non-credential variables (names only) ---")
    for n in sorted(n for n in env if n not in set(creds)):
        emit(f"  {n}")
    return 0


def cmd_file(path: str) -> int:
    d = load_store(path)
    if not d:
        emit(f"# {path}: no parseable variables (absent or empty)")
        return 0
    creds = {n for n in d if CRED_RE.search(n)}
    emit(f"# {path}: vars={len(d)} credential_vars={len(creds)}")
    for n in sorted(d):
        tag = "credential" if n in creds else "config"
        emit(f"  {n:34} [{tag}] {redact(d[n])}")
    return 0


def cmd_units() -> int:
    known = known_names()
    units = sorted(
        list(Path("/etc/systemd/system").glob("*.service"))
        + list(Path("/etc/systemd/system").glob("*/*.service"))
    )
    rows = []
    for u in units:
        try:
            txt = u.read_text(errors="replace")
        except OSError:
            continue
        efs = re.findall(r"^EnvironmentFile=-?(\S+)", txt, re.M)
        if not any(("kunci" in e or "vault" in e or "flat" in e) for e in efs):
            continue
        carried: set[str] = set()
        for e in efs:
            base = os.path.basename(e)
            for store in STORE_CANDIDATES:
                if os.path.basename(store) == base:
                    carried |= {n for n in load_store(store) if CRED_RE.search(n)}
        rows.append((len(carried), u.name, [os.path.basename(e) for e in efs]))
    rows.sort(reverse=True)
    emit(f"# units loading broad secret stores: {len(rows)}")
    for n, name, efs in rows:
        emit(f"  creds_carried={n:4}  {name:44} <- {','.join(efs)[:70]}")
    emit(f"# known credential-shaped names across stores: {len(known)}")
    return 0


def cmd_agentcheck() -> int:
    """Machine-readable: credential variable NAMES per running service. No values, ever."""
    known = known_names()
    out: dict[str, list[str]] = {}
    units = sorted(
        list(Path("/etc/systemd/system").glob("*.service"))
        + list(Path("/etc/systemd/system").glob("*/*.service"))
    )
    for u in units:
        pid = subprocess.run(
            ["systemctl", "show", u.name, "-p", "MainPID", "--value"],
            capture_output=True, text=True,
        ).stdout.strip()
        if not pid or pid == "0":
            continue
        try:
            env = read_environ(pid)
        except (FileNotFoundError, PermissionError):
            continue
        creds = sorted(n for n in env if n in known or CRED_RE.search(n))
        if creds:
            out[u.name] = creds
    emit(json.dumps(out, indent=1, sort_keys=True))
    return 0


# ── entry ────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="name_only_env_probe",
        description="name-only inspection of process environments and secret stores",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_env = sub.add_parser("env", help="names-only view of a process environment")
    p_env.add_argument("target", help="pid, unit name, or unit file path")
    p_env.add_argument("--classify", action="store_true", help="mark vars coming from a known store")

    p_file = sub.add_parser("file", help="names-only view of a secret store")
    p_file.add_argument("path")

    sub.add_parser("units", help="services carrying overly-broad secret stores")
    sub.add_parser("agentcheck", help="JSON: credential NAMES per running service")

    args = ap.parse_args(argv)

    if raw_mode_refused():
        emit("REFUSED: raw mode requires an interactive terminal (SECRETSAFE_RAW=1 plus a tty)")
        return 2

    if args.cmd == "env":
        return cmd_env(args.target, args.classify)
    if args.cmd == "file":
        return cmd_file(args.path)
    if args.cmd == "units":
        return cmd_units()
    if args.cmd == "agentcheck":
        return cmd_agentcheck()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
