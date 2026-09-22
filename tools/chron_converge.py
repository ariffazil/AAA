#!/usr/bin/env python3
"""CHRON tree consolidation — converge T1 (/root/AAA/scripts) onto the canonical
tree T2 (/root/chron).

Method: symlink-from-one-side. Every T1 file that DUPLICATES a canonical
/root/chron module is MOVED into a non-sys.path holding area and replaced by an
absolute symlink to the canonical file. Result: one inode per module, so the two
trees can never diverge again.

NOT a copy-from-both-sides: no byte of the diverged T1 content is promoted to
canonical. Every divergent T1 file is preserved in full (holding area + backup +
git) and the lost behaviour is reported, not silently dropped.

Nothing is deleted. Run with --apply; default is a dry run.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

T1 = Path("/root/AAA/scripts")
T2 = Path("/root/chron")
DIR = Path("/root/AAA/forge_work/chron-tree-consolidation-2026-09-21")
TS = (DIR / "CONSOLIDATION_TS.txt").read_text().strip()
HOLD = DIR / f"originals-moved-{TS}"          # NOT on any sys.path
LEDGER = DIR / "DISPOSITION-LEDGER.json"

# files that duplicate a canonical /root/chron module -> converge to symlink
DUPLICATES = [
    # diverged: T1 content is stale / different
    "chron_loop_close.py", "chron_prediction.py", "chron_verify.py",
    "chron_learn.py", "chron_cron_verify.py", "chron_ariflow_bridge.py",
    "chron_mcp.py",
    # byte-identical duplicates
    "chron_store.py", "chron_episode.py", "chron_frame.py", "chron_nats.py",
    "chron_temporal_root.py", "chron_e2e_proof.py",
]

# files that exist ONLY in T1 and are consumed live by the ALPHA-ZEN card path
# -> untouched. Moving or shadowing these breaks the card (proof c) and the
# clock entrypoint (proof d).
T1_ORIGINAL = [
    "chron.py", "chron_events.json", "chron_events.schema.json",
    "chron_spine_gate.py", "seal_chron_day.py",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    apply = "--apply" in sys.argv
    if not apply:
        print("DRY RUN (pass --apply to execute)\n")
    HOLD.mkdir(parents=True, exist_ok=True)

    ledger: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "canonical_tree": str(T2),
        "host": "KVM8",
        "method": "symlink-from-one-side (move-aside + absolute symlink)",
        "holding_area": str(HOLD),
        "backup_dir": str(DIR / f"backup-{TS}"),
        "modules": [],
        "t1_original_untouched": [],
    }

    for name in DUPLICATES:
        src, dst = T1 / name, T2 / name
        rec: dict[str, Any] = {"module": name, "t1": str(src), "canonical": str(dst)}
        if not dst.exists():
            rec.update({"action": "SKIP", "reason": "no canonical counterpart"})
            ledger["modules"].append(rec)
            print(f"SKIP   {name}: no canonical counterpart")
            continue
        if not src.is_symlink() and not src.exists():
            rec.update({"action": "SKIP", "reason": "no T1 file"})
            ledger["modules"].append(rec)
            print(f"SKIP   {name}: no T1 file")
            continue

        t2_hash = sha(dst)
        rec["canonical_sha256"] = t2_hash

        if src.is_symlink():
            rec.update({"action": "ALREADY_CONVERGED",
                        "points_to": os.readlink(src),
                        "t2_sha256": t2_hash})
            ledger["modules"].append(rec)
            print(f"OK     {name}: already a symlink -> {os.readlink(src)}")
            continue

        t1_hash = sha(src)
        rec["t1_sha256_before"] = t1_hash
        rec["diverged"] = (t1_hash != t2_hash)

        held = HOLD / name
        if held.exists():
            rec["held_copy"] = str(held)
            rec["held_copy_sha256"] = sha(held)
        if apply:
            shutil.move(str(src), str(held))       # MOVE, never delete
            os.symlink(str(dst), str(src))          # absolute symlink
            rec["held_copy"] = str(held)
            rec["held_copy_sha256"] = sha(held)
            rec["symlink_target"] = os.readlink(src)
            rec["resolves_to"] = str(src.resolve())
            rec["resolved_sha256_after"] = sha(src.resolve())
            rec["verified"] = (
                rec["resolved_sha256_after"] == t2_hash
                and rec["held_copy_sha256"] == t1_hash
            )
        rec["action"] = "CONVERGED" if apply else "WOULD_CONVERGE"
        ledger["modules"].append(rec)
        tag = "DIVERGED" if rec["diverged"] else "identical"
        print(f"{'CONVERGED' if apply else 'WOULD CONVERGE'}  {name} [{tag}] "
              f"-> {dst}")

    for name in T1_ORIGINAL:
        p = T1 / name
        rec: dict[str, Any] = {"module": name, "path": str(p), "action": "UNTOUCHED",
               "reason": "T1-original; exists only in T1; live consumer"}
        if p.exists():
            rec["sha256"] = sha(p)
            rec["exists"] = True
        else:
            rec["exists"] = False
        ledger["t1_original_untouched"].append(rec)
        print(f"KEEP   {name}: T1-original, live consumer — untouched")

    if apply:
        LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
        print(f"\nledger -> {LEDGER}")

    # convergence assertion
    still = []
    for name in DUPLICATES:
        src, dst = T1 / name, T2 / name
        if dst.exists() and src.exists() or src.is_symlink():
            if not src.is_symlink() and sha(src) != sha(dst):
                still.append(name)
    print(f"\nmodules still diverged in T1: {still if still else 'NONE'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
