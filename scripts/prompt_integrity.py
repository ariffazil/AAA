#!/usr/bin/env python3
"""prompt_integrity.py — mechanical falsification layer for identity/law files.

F13 question (2026-09-17): "how can we make sure SOUL.md and AGENTS.md reflect
the agentic intelligence state itself — no chaos, no shadow, no bangang."

The answer this script enforces: prompt files must not ASSERT mutable state —
they must POINT at the surface that owns it, and the pointers must be swept.
Hermes SOUL.md's own doctrine line says it best: "a dead pointer is invisible
until someone sweeps for it." This IS the sweep.

Checks (per target file):
  1. DEAD_POINTER   — /root/... or /opt/... paths referenced but nonexistent (WARN)
  2. STALE_STAMP    — Rendered:/updated= stamp older than MAX_AGE_DAYS (WARN)
  3. HOST_MISMATCH  — stamp claims host=KVMx but this machine is a different node (ERROR)
  4. MUTABLE_CENSUS — count of port/version/path tokens (informational; SCP watch)

Exit code: 1 only on ERROR (warnings do not fail the build — a noisy gate gets
ignored, an exact one gets read).

Usage:
  python3 prompt_integrity.py                     # default targets
  python3 prompt_integrity.py FILE [FILE...]       # explicit targets
  python3 prompt_integrity.py --strict             # warnings also fail
"""

from __future__ import annotations

import re
import socket
import sys
import time
from pathlib import Path

MAX_AGE_DAYS = 14

# hostname → canonical mesh node (MACHINE_MAP.md SOT)
HOST_CANON = {
    "forge": "KVM8",        # af-forge, seat/court, 100.64.0.2
    "kvm4-forge": "KVM4",   # workshop, 100.64.0.5
    "azwaos": "KVM2",       # witness, 100.64.0.4
}

DEFAULT_TARGETS = [
    "/root/AGENTS.md",
    "/root/.hermes/SOUL.md",
    "/root/.hermes/AGENTS.md",
    "/root/QWEN.md",
]

PATH_TOKEN = re.compile(r"(?:/root|/opt|/etc)/[A-Za-z0-9_./-]+")
STAMP_HOST = re.compile(r"host=(KVM\d)")
STAMP_UPDATED = re.compile(r"(?:Rendered|updated)[:=]\s*(\d{4}-\d{2}-\d{2})")
MUTABLE_TOKEN = re.compile(r":[0-9]{4}\b|v\d+\.\d+\.\d+")

# Paths referenced as historical/illustrative in doctrine prose — known-benign.
ALLOW_MISSING = {
    "/root/forge_work/2026-08-21-FI-003-seal-b-c-implementation.md",  # dated receipt
}


def check_file(path: str) -> tuple[list[str], list[str]]:
    """Returns (errors, warnings) for one target file."""
    errors: list[str] = []
    warnings: list[str] = []
    p = Path(path)
    if not p.exists():
        return ([], [f"{path}: TARGET_MISSING (file listed but absent)"])
    text = p.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    # 1. Dead pointers — every absolute path token must resolve on this machine.
    NEGATION = re.compile(r"not exist|doesn'?t exist|no longer|bukan|retired|removed", re.I)
    for i, line in enumerate(lines, 1):
        if NEGATION.search(line):
            continue  # the line asserts absence, not a pointer
        if "…" in line or "..." in line and PATH_TOKEN.search(line):
            continue  # ellipsis = illustrative, not a pointer
        for m in PATH_TOKEN.finditer(line):
            tok = m.group(0).rstrip(".,;:)")
            if tok in ALLOW_MISSING or Path(tok).exists():
                continue
            warnings.append(f"{path}:{i}: DEAD_POINTER {tok}")

    # 2. Stamp freshness
    for m in STAMP_UPDATED.finditer(text):
        stamp_day = m.group(1)
        try:
            age_days = (time.time() - time.mktime(time.strptime(stamp_day, "%Y-%m-%d"))) / 86400
            if age_days > MAX_AGE_DAYS:
                warnings.append(
                    f"{path}: STALE_STAMP {stamp_day} ({age_days:.0f}d old, max {MAX_AGE_DAYS})"
                )
        except ValueError:
            warnings.append(f"{path}: STALE_STAMP unparseable date {stamp_day!r}")

    # 3. Host anchor — a stamp claiming another node's host is drift evidence
    live_host = HOST_CANON.get(socket.gethostname())
    for m in STAMP_HOST.finditer(text):
        claimed = m.group(1)
        if live_host and claimed != live_host:
            errors.append(
                f"{path}: HOST_MISMATCH stamp claims host={claimed} but this machine is "
                f"{socket.gethostname()}={live_host} — stamp not re-anchored on sync/copy"
            )

    # 4. Mutable-fact census (informational)
    census = len(MUTABLE_TOKEN.findall(text))
    print(f"    census: {path}: {census} mutable tokens (ports/versions)")

    return errors, warnings


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    strict = "--strict" in argv
    targets = args or DEFAULT_TARGETS

    print("=== Prompt Integrity Sweep (SOUL/AGENTS truth layer) ===")
    all_errors: list[str] = []
    all_warnings: list[str] = []
    for t in targets:
        e, w = check_file(t)
        all_errors += e
        all_warnings += w

    for w in all_warnings:
        print(f"  ⚠  {w}")
    for e in all_errors:
        print(f"  ✖  {e}")

    verdict = "PASS" if not all_errors and not (strict and all_warnings) else "FAIL"
    print(f"  → {verdict}: {len(all_errors)} errors, {len(all_warnings)} warnings "
          f"across {len(targets)} files")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
