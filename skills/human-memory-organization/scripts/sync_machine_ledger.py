#!/usr/bin/env python3
"""
sync_machine_ledger.py -- rewrite /root/.local/share/arifos/scars/index.json
from H5 canonical at /root/memory/H5-scars/H5_SCAR_REGISTRY.json.

Preserves any machine-only scars (e.g. SCAR-002-CEREMONY_FAILED_406).
Updates schema to v2.0.0 with synced_from, updated, stats.{human_scars,machine_scars}.

Usage:
  python3 sync_machine_ledger.py [--h5 H5_REGISTRY] [--machine MACHINE_INDEX]

Exit codes:
  0 -- already in sync
  1 -- drift detected, sync performed
  2 -- error
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

H5_DEFAULT = "/root/memory/H5-scars/H5_SCAR_REGISTRY.json"
MACHINE_DEFAULT = "/root/.local/share/arifos/scars/index.json"

# Canonical MYT timezone (F13 standing ruling 2026-08-11)
MYT = timezone(timedelta(hours=8))


def now_myt():
    return datetime.now(MYT).isoformat(timespec="seconds")


def load_h5(path):
    with open(path) as f:
        data = json.load(f)
    if data.get("version") != "2.0.0":
        print(f"WARN: H5 registry version is {data.get('version')}, expected 2.0.0",
              file=sys.stderr)
    return data.get("scars", [])


def load_machine(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"WARN: machine ledger is malformed JSON; treating as empty",
                  file=sys.stderr)
            return []
    return data.get("scars", [])


def map_h5_to_machine(h5_scar):
    cross_links = h5_scar.get("cross_links", {})
    floors = cross_links.get("floors", []) if isinstance(cross_links, dict) else []

    return {
        "scar_id": h5_scar.get("scar_id"),
        "title": h5_scar.get("title"),
        "created": h5_scar.get("created"),
        "file_path": h5_scar.get("file_path"),
        "cross_links": floors,
        "meaning_anchor": h5_scar.get("meaning_anchor"),
        "last_verified": h5_scar.get("last_verified"),
    }


def detect_drift(h5_scars, machine_scars):
    h5_ids = {s.get("scar_id") for s in h5_scars}
    machine_ids = {s.get("scar_id") or s.get("id") for s in machine_scars}

    human_in_h5 = h5_ids - machine_ids
    machine_only = machine_ids - h5_ids

    return len(human_in_h5) > 0 or len(machine_only) > 0, len(h5_scars), len(machine_scars)


def sync(h5_path, machine_path):
    h5_scars = load_h5(h5_path)
    machine_scars = load_machine(machine_path)

    drift, h5_count, machine_count = detect_drift(h5_scars, machine_scars)
    if not drift and len(h5_scars) == len(machine_scars):
        print(f"OK Already in sync: {h5_count} scars on both sides")
        return 0

    print(f"Drift detected: H5={h5_count} scars, machine={machine_count} scars")

    new_machine_scars = []
    for h5 in h5_scars:
        new_machine_scars.append(map_h5_to_machine(h5))

    h5_ids = {s.get("scar_id") for s in h5_scars}
    for m in machine_scars:
        mid = m.get("scar_id") or m.get("id")
        if mid and mid not in h5_ids:
            new_machine_scars.append(m)
            print(f"  preserving machine-only scar: {mid}")

    stats = {
        "total_scars": len(new_machine_scars),
        "human_scars": len(h5_scars),
        "machine_scars": len(new_machine_scars) - len(h5_scars),
        "verified": len(new_machine_scars),
        "stale": 0,
    }

    new_data = {
        "version": "2.0.0",
        "created": "2026-08-08T00:00:00+08:00",
        "updated": now_myt(),
        "synced_from": h5_path,
        "description": "Machine-side scar ledger -- synced from H5 canonical registry.",
        "sovereignty": "Agent does not read scar content unless scar:<id> invoked.",
        "scars": new_machine_scars,
        "stats": stats,
    }

    with open(machine_path, "w") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)

    print(f"\nOK Synced: {stats['total_scars']} scars total "
          f"({stats['human_scars']} human + {stats['machine_scars']} machine)")
    print(f"   Wrote: {machine_path}")
    return 1


if __name__ == "__main__":
    args = sys.argv[1:]
    h5_path = H5_DEFAULT
    machine_path = MACHINE_DEFAULT
    if "--h5" in args:
        h5_path = args[args.index("--h5") + 1]
    if "--machine" in args:
        machine_path = args[args.index("--machine") + 1]

    sys.exit(sync(h5_path, machine_path))