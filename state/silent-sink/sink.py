#!/usr/bin/env python3
"""silent-sink — append-only record of what an agent did NOT say out loud.

Canonical: /root/AAA/state/silent-sink/README.md

Commands:
  append --lane L --reason R [--note N] [--ref X]
  report [--json]
  check
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SINK = Path("/root/AAA/state/silent-sink/silent-sink.jsonl")
REASONS = {
    "DECISION_REQUIRED",
    "CONSENT_REQUIRED",
    "COMMITMENT_DUE",
    "MATERIAL_CHANGE",
    "SAFETY",
    "PERSONAL_INFORMATION_REQUESTED",
    "EXCEPTION_UNRESOLVED",
    "NONE_OF_THE_ABOVE",
}
# reasons that also require delivery to a human surface
HUMAN_FACING = REASONS - {"NONE_OF_THE_ABOVE"}


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append(lane: str, reason: str, note: str = "", ref: str = "") -> dict:
    if reason not in REASONS:
        raise ValueError(f"reason {reason!r} not in enum: {sorted(REASONS)}")
    SINK.parent.mkdir(parents=True, exist_ok=True)
    rec = {"ts": _now(), "lane": lane, "reason": reason, "note": note[:200], "ref": ref}
    with SINK.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def load() -> list[dict]:
    if not SINK.exists():
        return []
    out = []
    for line in SINK.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def report(as_json: bool = False) -> dict:
    recs = load()
    by_reason = Counter(r.get("reason") for r in recs)
    by_lane = Counter(r.get("lane") for r in recs)
    actionable = [r for r in recs if r.get("reason") in HUMAN_FACING]
    payload = {
        "total": len(recs),
        "by_reason": dict(by_reason),
        "by_lane": dict(by_lane),
        "actionable": len(actionable),
        "oldest_actionable": actionable[0]["ts"] if actionable else None,
        "verdict": (
            "QUIET — nothing needs a human"
            if not actionable
            else f"{len(actionable)} record(s) declare a human reason"
        ),
    }
    if as_json:
        print(json.dumps(payload, indent=1))
    else:
        print(f"SILENT SINK — {payload['total']} records")
        print(f"  {payload['verdict']}")
        for r, n in by_reason.most_common():
            print(f"    {r:30} {n}")
        print(f"  lanes: {len(by_lane)}")
    return payload


def check() -> int:
    recs = load()
    bad = [r for r in recs if r.get("reason") not in REASONS]
    print(f"records={len(recs)} malformed_reason={len(bad)}")
    print("SINK_CHECK=" + ("PASS" if not bad else "FAIL"))
    return 0 if not bad else 1


def main() -> int:
    ap = argparse.ArgumentParser(prog="sink")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("append")
    a.add_argument("--lane", required=True)
    a.add_argument("--reason", required=True)
    a.add_argument("--note", default="")
    a.add_argument("--ref", default="")
    r = sub.add_parser("report")
    r.add_argument("--json", action="store_true")
    sub.add_parser("check")
    args = ap.parse_args()

    if args.cmd == "append":
        print(json.dumps(append(args.lane, args.reason, args.note, args.ref)))
        return 0
    if args.cmd == "report":
        report(args.json)
        return 0
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
