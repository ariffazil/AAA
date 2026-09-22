#!/usr/bin/env python3
"""CHRON canonical-tree drift check — machine-checkable.

Asserts the invariant that consolidating three diverged CHRON trees established:
CHRON orchestration code exists in exactly ONE place, /root/chron, and every
/root/AAA/scripts entry that duplicates it is either

  (a) a DELEGATION SHIM — a real file that contains no CHRON logic and resolves
      to the canonical package (required for the 7 modules whose T1 twins had
      actually diverged, because a symlink there is a write-through hazard: a
      concurrent writer can follow it and clobber the canonical module), or
  (b) BYTE-IDENTICAL to the canonical module (the 6 twins that never diverged).

Exit 0 = invariant holds. Exit 1 = drift, with the offending path named.

Run:  python3 /root/AAA/tools/chron_tree_drift_check.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

T1 = Path("/root/AAA/scripts")
T2 = Path("/root/chron")

# must be delegation shims (they diverged historically)
SHIMMED = [
    "chron_loop_close.py", "chron_prediction.py", "chron_verify.py",
    "chron_learn.py", "chron_cron_verify.py", "chron_ariflow_bridge.py",
    "chron_mcp.py",
]
# must be byte-identical copies
IDENTICAL = [
    "chron_store.py", "chron_episode.py", "chron_frame.py", "chron_nats.py",
    "chron_temporal_root.py", "chron_e2e_proof.py",
]
# T1-original: exist only in T1 and are consumed live by the ALPHA-ZEN card
T1_ORIGINAL = ["chron.py", "chron_events.json", "chron_events.schema.json",
               "chron_spine_gate.py", "seal_chron_day.py"]

# the live units' ExecStart targets — the canonical tree must satisfy these
LIVE_UNITS = {
    "chron-loop-closer.service": "/root/chron/chron_loop_close.py",
    "chron-prediction-verifier.service": "/root/chron/chron_cron_verify.py",
    "chron-task0-reconciliation.service": "/root/scripts/chron_personal/task0_reconciliation.py",
    "chron-mcp.service": "/root/chron/mcp_server.py",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def is_shim(p: Path) -> tuple[bool, str]:
    """A shim is a REAL file that contains no CHRON logic and delegates."""
    if p.is_symlink():
        return False, "is a symlink (write-through hazard)"
    txt = p.read_text()
    if '_PKG_DIR = "/root/chron"' not in txt:
        return False, "does not declare the canonical package dir"
    stem = p.stem
    if f'_CANONICAL = "chron.{stem}"' not in txt:
        return False, f'does not declare _CANONICAL = "chron.{stem}"'
    # contains no CHRON logic of its own
    if "def " in txt and "_mod = importlib.import_module" not in txt:
        return False, "contains function definitions — it is a copy, not a shim"
    banned = ("chron_store import", "get_store(", "save_calibration(")
    for b in banned:
        if b in txt and "globals().update" not in txt:
            return False, f"contains CHRON logic marker {b!r}"
    return True, "delegation shim"


def main() -> int:
    fails: list[str] = []
    rows: list[dict] = []

    for name in SHIMMED:
        p = T1 / name
        if not p.exists() and not p.is_symlink():
            fails.append(f"{name}: MISSING from {T1}")
            rows.append({"module": name, "kind": "shim", "ok": False,
                         "detail": "missing"})
            continue
        ok, why = is_shim(p)
        rows.append({"module": name, "kind": "shim", "ok": ok, "detail": why,
                     "size": p.stat().st_size})
        if not ok:
            fails.append(f"{name}: {why}")

    for name in IDENTICAL:
        p, c = T1 / name, T2 / name
        if not p.exists() or not c.exists():
            fails.append(f"{name}: missing (T1={p.exists()} T2={c.exists()})")
            rows.append({"module": name, "kind": "identical", "ok": False,
                         "detail": "missing"})
            continue
        if p.is_symlink():
            fails.append(f"{name}: is a symlink (write-through hazard)")
            rows.append({"module": name, "kind": "identical", "ok": False,
                         "detail": "symlink"})
            continue
        h1, h2 = sha(p), sha(c)
        ok = h1 == h2
        rows.append({"module": name, "kind": "identical", "ok": ok,
                     "t1_sha256": h1[:16], "t2_sha256": h2[:16]})
        if not ok:
            fails.append(
                f"{name}: DIVERGED again — T1 {h1[:16]} != T2 {h2[:16]}. "
                f"Converge it: shim it or make it byte-identical.")

    for name in T1_ORIGINAL:
        p = T1 / name
        ok = p.exists() and not p.is_symlink()
        rows.append({"module": name, "kind": "t1-original", "ok": ok})
        if not ok:
            fails.append(f"{name}: T1-original missing or shadowed")

    for unit, target in LIVE_UNITS.items():
        ok = Path(target).exists()
        rows.append({"module": target, "kind": "live-entrypoint", "ok": ok,
                     "unit": unit})
        if not ok:
            fails.append(f"{unit}: ExecStart target absent: {target}")

    # no stray symlink anywhere in the T1 chron surface
    strays = [str(p) for p in T1.glob("chron*") if p.is_symlink()]
    if strays:
        fails.append("stray symlinks in T1 (write-through hazard): "
                     + ", ".join(strays))

    # the `chron` package must not shadow the clock module for the card
    probe = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0,'/root/AAA/scripts'); import chron; "
         "print(chron.__file__)"],
        capture_output=True, text=True, cwd="/",
    )
    clock_ok = probe.stdout.strip() == "/root/AAA/scripts/chron.py"
    rows.append({"module": "import chron (card clock)", "kind": "resolution",
                 "ok": clock_ok, "resolved": probe.stdout.strip()})
    if not clock_ok:
        fails.append("ALPHA-ZEN card clock no longer resolves to "
                     "/root/AAA/scripts/chron.py — got " + probe.stdout.strip())

    print(json.dumps({"ok": not fails, "checks": rows, "failures": fails},
                     indent=2))
    print("\nRESULT:", "PASS — one canonical CHRON tree, no divergence"
          if not fails else f"FAIL — {len(fails)} drift(s)")
    for f in fails:
        print("  -", f)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
