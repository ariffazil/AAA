#!/usr/bin/env python3
"""HAB — Human Attention Burden.

    HAB = human intervention events / successful missions

WHY THIS EXISTS
---------------
The anti-bangang law says: "Kalau benda tu tambah kerja manusia, ia bukan
improvement." That law is currently prose. This is its instrument.

HONESTY CONTRACT (read before trusting any number it prints)
------------------------------------------------------------
The numerator — human intervention — was NOT being recorded anywhere before
this file existed. So HAB is UNCOMPUTABLE until enough interventions have
been logged. This script refuses to print a ratio below MIN_SAMPLES. A
dashboard tile that renders "HAB 0.00" because no numerator was ever
captured is exactly the failure mode this exists to prevent.

USAGE
-----
    ./hab.py log --mission <id> --kind <escalate|clarify|interrupt|approve|reject>
                        [--seconds N] [--note "..."]
    ./hab.py close --mission <id> [--success|--fail]
    ./hab.py report [--json]

STATE
-----
    /root/AAA/state/hab/events.jsonl   (append-only)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path("/root/AAA/state/hab")
EVENTS = STATE_DIR / "events.jsonl"

# Below this, the ratio is not reported. Two is enough to fail loudly on a
# broken numerator; twenty is enough to see a direction.
MIN_SAMPLES = 20

# An intervention only counts if the human actually had to act. A notification
# nobody read is not attention spent.
COUNTS_AS_ATTENTION = {"escalate", "clarify", "interrupt", "approve", "reject"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append(rec: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")


def load_events() -> list[dict]:
    if not EVENTS.exists():
        return []
    out = []
    for line in EVENTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def cmd_log(a: argparse.Namespace) -> int:
    if a.kind not in COUNTS_AS_ATTENTION:
        print(f"error: --kind must be one of {sorted(COUNTS_AS_ATTENTION)}", file=sys.stderr)
        return 2
    _append({
        "ts": now(),
        "type": "intervention",
        "mission": a.mission,
        "kind": a.kind,
        "seconds": a.seconds,      # explicit if known; else None (see report)
        "note": a.note or "",
    })
    print(f"logged: {a.kind} on {a.mission}")
    return 0


def cmd_close(a: argparse.Namespace) -> int:
    _append({
        "ts": now(),
        "type": "mission_close",
        "mission": a.mission,
        "success": bool(a.success),
    })
    print(f"closed: {a.mission} success={bool(a.success)}")
    return 0


def compute(events: list[dict]) -> dict:
    interventions = [e for e in events if e.get("type") == "intervention"
                     and e.get("kind") in COUNTS_AS_ATTENTION]
    closed = [e for e in events if e.get("type") == "mission_close"]
    succeeded = [e for e in closed if e.get("success")]

    # Count DISTINCT missions that consumed attention — a mission that
    # escalated three times still cost one interruption of focus, not three.
    touched = {e.get("mission") for e in interventions}

    timed = [e for e in interventions if isinstance(e.get("seconds"), (int, float))]
    total_seconds = sum(e["seconds"] for e in timed)
    timing_coverage = (len(timed) / len(interventions)) if interventions else 0.0

    result = {
        "generated_at": now(),
        "intervention_events": len(interventions),
        "distinct_missions_needing_human": len(touched),
        "missions_closed": len(closed),
        "missions_succeeded": len(succeeded),
        "timing_coverage": round(timing_coverage, 3),
        "human_seconds_recorded": total_seconds,
        "events_by_kind": {},
    }
    for e in interventions:
        k = e.get("kind", "?")
        result["events_by_kind"][k] = result["events_by_kind"].get(k, 0) + 1

    if len(interventions) < MIN_SAMPLES:
        result["hab"] = None
        result["status"] = "INSUFFICIENT_DATA"
        result["note"] = (
            f"{len(interventions)}/{MIN_SAMPLES} interventions logged. "
            "The numerator was never captured before this instrument existed; "
            "any ratio printed now would be fiction."
        )
    elif not succeeded:
        result["hab"] = None
        result["status"] = "INSUFFICIENT_DATA"
        result["note"] = "No successful missions closed yet — denominator is zero."
    else:
        result["hab"] = round(len(touched) / len(succeeded), 4)
        result["status"] = "MEASURED"
        result["note"] = (
            "HAB = distinct missions needing human / successful missions. "
            "Direction matters, not magnitude."
        )
    return result


def cmd_report(a: argparse.Namespace) -> int:
    res = compute(load_events())
    if a.json:
        print(json.dumps(res, indent=2, sort_keys=True))
    else:
        print(f"HAB status      : {res['status']}")
        print(f"HAB value       : {res['hab'] if res['hab'] is not None else '(not computable)'}")
        print(f"interventions   : {res['intervention_events']} "
              f"across {res['distinct_missions_needing_human']} missions")
        print(f"missions closed : {res['missions_closed']} "
              f"({res['missions_succeeded']} successful)")
        print(f"timing coverage : {res['timing_coverage']:.0%} of interventions have --seconds")
        if res["events_by_kind"]:
            print(f"by kind         : {res['events_by_kind']}")
        print(f"\n{res['note']}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Human Attention Burden")
    sub = p.add_subparsers(dest="cmd", required=True)

    lg = sub.add_parser("log", help="record that a human had to be interrupted")
    lg.add_argument("--mission", required=True)
    lg.add_argument("--kind", required=True, choices=sorted(COUNTS_AS_ATTENTION))
    lg.add_argument("--seconds", type=float, default=None,
                    help="explicit attention seconds, if actually measured")
    lg.add_argument("--note", default=None)
    lg.set_defaults(func=cmd_log)

    cl = sub.add_parser("close", help="record that a mission finished")
    cl.add_argument("--mission", required=True)
    grp = cl.add_mutually_exclusive_group()
    grp.add_argument("--success", action="store_true")
    grp.add_argument("--fail", action="store_true")
    cl.set_defaults(func=cmd_close)

    rp = sub.add_parser("report", help="compute HAB (refuses below MIN_SAMPLES)")
    rp.add_argument("--json", action="store_true")
    rp.set_defaults(func=cmd_report)

    a = p.parse_args()
    return a.func(a)


if __name__ == "__main__":
    raise SystemExit(main())