#!/usr/bin/env python3
"""
xz_probe.py — fleet XZ-signature + sovereign-load quick probe.

Statically re-runnable verification for the agentic-trust-trajectory skill.
Read-only: parses guard ledger + hold queue, prints sovereign load band and
any attributable actor trajectories. stdlib only (every dependency is xz-surface).

Usage:
    python3 xz_probe.py            # full probe
    python3 xz_probe.py --sovereign
    python3 xz_probe.py --xz
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

GUARD = Path("/root/AAA/ledger/constitutional_guard.jsonl")
HOLDS = Path("/root/AAA/data/hold_queue.jsonl")


def rows(path: Path):
    if not path.exists():
        return []
    out = []
    for line in path.open(errors="replace"):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def ts(raw):
    if not isinstance(raw, str):
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def sovereign(guard, user_id="267378578"):
    hours = defaultdict(set)
    for r in guard:
        if r.get("user_id") != user_id:
            continue
        t = ts(r.get("timestamp"))
        if t is None:
            continue
        loc = t + timedelta(hours=8)
        hours[loc.strftime("%Y-%m-%d")].add(loc.hour)
    if not hours:
        return {"status": "no-data"}
    marathon = [d for d, h in hours.items() if len(h) >= 12]
    predawn = [d for d, h in hours.items() if min(h) <= 4]
    return {
        "days_observed": len(hours),
        "marathon_days": len(marathon),
        "predawn_wakes": len(predawn),
        "load_band": "HIGH" if len(marathon) >= 3 else "MEDIUM" if marathon else "LOW",
    }


def actors(guard, holds):
    A = defaultdict(lambda: {"n": 0, "holds": 0, "days": defaultdict(int), "first": None, "last": None})
    for r in guard + holds:
        a = r.get("proposed_by") or r.get("actor") or r.get("from_agent")
        if not a:
            continue
        d = A[a]
        d["n"] += 1
        if "violated_floors" in r:
            d["holds"] += 1
        t = ts(r.get("timestamp") or r.get("created_at"))
        if t:
            loc = t + timedelta(hours=8)
            d["days"][loc.strftime("%Y-%m-%d")] += 1
            d["first"] = t if d["first"] is None else min(d["first"], t)
            d["last"] = t if d["last"] is None else max(d["last"], t)
    return A


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    guard, holds = rows(GUARD), rows(HOLDS)
    if mode in ("--sovereign", ""):
        print(json.dumps(sovereign(guard), indent=2))
    if mode in ("--xz", ""):
        A = actors(guard, holds)
        attributable = {k: v["n"] for k, v in A.items() if v["n"] >= 5}
        blind = len(guard) - sum(v["n"] for v in A.values())
        print(
            json.dumps(
                {
                    "attributable_actors": attributable or "NONE with >=5 events",
                    "identity_blind_rows_in_guard": blind,
                    "note": "empty scan = attribution gap, NOT proven innocence",
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
