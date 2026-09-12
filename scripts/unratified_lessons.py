#!/usr/bin/env python3
"""unratified_lessons.py — append-only steward for the UNRATIFIED-LESSONS lane.

Gate-2 item 3 (U20, FEDERATION-CONSTITUTIONAL-INVARIANTS-v1.1 [S3]).
Mechanizes what FI-008 practiced by hand 2026-09-12 (UL-001..010):
  - append under flock (two-writer race is live — parallel lanes append)
  - schema validation matching the lane's evolved field set
  - supersession, never edit (UL-006 precedent)
  - promotion to scar as a NEW entry carrying the F13 instrument

Promotion law (UL-009, sovereign synthesis 2026-09-12):
  Narrative -> Guardrail -> Test -> Receipt -> Independent Audit.
  A scar is not real because it was recorded; it is real because future
  behavior is constrained by it. Grading per UL-010: Witnessed / ASSERTED.

DITEMPA BUKAN DIBERI.
"""

import argparse
import fcntl
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

LANE_PATH = Path("/root/AAA/governance/UNRATIFIED-LESSONS-LEDGER.jsonl")
ID_RE = re.compile(r"^UL-(\d{3,})$")
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
F13_MARKER_RE = re.compile(r"F13[_\s-]*RATIFIED[_\s-]*CHAT", re.IGNORECASE)
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

REQUIRED = ["id", "ts_utc", "lane", "class", "title", "finding", "status", "recorded_by", "session"]
KNOWN_OPTIONAL = {
    "kernel_warts", "onchain", "origin_scar", "durable_record_prior", "disk_witness",
    "collateral", "supersedes", "severity", "next_action", "resolves", "still_open",
    "traffic_wiring", "live_confirmations_tonight", "sharpenings_accepted_for_fold",
    "instrument", "fold_target", "close_condition", "note", "scar_ref",
}


def load_entries():
    entries = []
    if LANE_PATH.exists():
        for i, line in enumerate(LANE_PATH.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"ERR line {i}: unparseable JSON ({e})", file=sys.stderr)
                sys.exit(1)
    return entries


def validate(entries):
    errors, warnings = [], []
    ids = []
    for e in entries:
        eid = e.get("id", "?")
        for f in REQUIRED:
            if not e.get(f):
                errors.append(f"{eid}: missing required field '{f}'")
        if not ID_RE.match(str(eid)):
            errors.append(f"{eid}: id must match UL-###")
        if not TS_RE.match(str(e.get("ts_utc", ""))):
            errors.append(f"{eid}: ts_utc must be ISO-8601 Zulu")
        if e.get("lane") != "unratified-lessons":
            errors.append(f"{eid}: lane must be 'unratified-lessons'")
        st = str(e.get("status", ""))
        if not (st.startswith("UNRATIFIED") or st.startswith("PROMOTED")):
            errors.append(f"{eid}: status must start UNRATIFIED* or PROMOTED* (got '{st}')")
        ids.append(eid)
        unknown = set(e.keys()) - set(REQUIRED) - KNOWN_OPTIONAL
        if unknown:
            warnings.append(f"{eid}: unknown fields {sorted(unknown)} (pass-through allowed)")
    dupes = {i for i in ids if ids.count(i) > 1}
    for d in dupes:
        errors.append(f"{d}: duplicate id")
    nums = sorted(int(ID_RE.match(i).group(1)) for i in ids if ID_RE.match(i))
    for a, b in zip(nums, nums[1:]):
        if b != a + 1:
            warnings.append(f"numbering gap: UL-{a:03d} -> UL-{b:03d} (supersession/reservation? not renumbered)")
    # promotion entries must carry instrument
    for e in entries:
        if str(e.get("class")) == "promotion":
            inst = str(e.get("instrument", ""))
            if not (F13_MARKER_RE.search(inst) and DATE_RE.search(inst)):
                errors.append(f"{e.get('id')}: promotion requires instrument with F13 marker + date")
    return errors, warnings


def next_id(entries):
    nums = [int(ID_RE.match(e["id"]).group(1)) for e in entries if ID_RE.match(str(e.get("id", "")))]
    return f"UL-{(max(nums) + 1) if nums else 1:03d}"


def append_entry(args):
    entries = load_entries()
    promoted = {e.get("supersedes") for e in entries if e.get("class") == "promotion"}
    entry = {
        "id": next_id(entries),
        "ts_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lane": "unratified-lessons",
        "class": args.class_name,
        "title": args.title,
        "finding": args.finding,
        "status": args.status or "UNRATIFIED_LESSON",
        "recorded_by": args.recorded_by,
        "session": args.session,
    }
    if args.supersedes:
        if args.supersedes in promoted:
            print(f"ERR: {args.supersedes} already has a promotion entry", file=sys.stderr)
            sys.exit(1)
        entry["supersedes"] = args.supersedes
    if args.kernel_warts:
        entry["kernel_warts"] = [w.strip() for w in args.kernel_warts.split(";") if w.strip()]
    if args.scopes:
        entry["onchain"] = [w.strip() for w in args.scopes.split(";") if w.strip()]
    if args.instrument:
        entry["instrument"] = args.instrument
    if args.scar_ref:
        entry["scar_ref"] = args.scar_ref
    with open(LANE_PATH, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)
    errors, warnings = validate(load_entries())
    for w in warnings:
        print(f"WARN {w}", file=sys.stderr)
    if errors:
        print(f"ERR appended {entry['id']} but lane now INVALID:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)
    print(f"APPENDED {entry['id']} ({entry['class']}) — lane valid, {len(load_entries())} entries")


def main():
    p = argparse.ArgumentParser(description="UNRATIFIED-LESSONS lane steward (append-only)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate", help="validate the lane (schema, ids, promotions)")
    sub.add_parser("list", help="list entries")
    lp = sub.add_parser("append", help="append a lesson (flock-protected)")
    lp.add_argument("--class-name", required=True, dest="class_name")
    lp.add_argument("--title", required=True)
    lp.add_argument("--finding", required=True)
    lp.add_argument("--recorded-by", required=True, dest="recorded_by")
    lp.add_argument("--session", required=True)
    lp.add_argument("--status")
    lp.add_argument("--supersedes")
    lp.add_argument("--kernel-warts", help="semicolon-separated")
    lp.add_argument("--scopes", help="semicolon-separated onchain refs")
    lp.add_argument("--instrument")
    lp.add_argument("--scar-ref", dest="scar_ref")
    args = p.parse_args()

    if args.cmd == "validate":
        errors, warnings = validate(load_entries())
        for w in warnings:
            print(f"WARN {w}")
        if errors:
            for e in errors:
                print(f"ERR {e}", file=sys.stderr)
            print(f"INVALID: {len(errors)} error(s)", file=sys.stderr)
            sys.exit(1)
        print(f"VALID: {len(load_entries())} entries, schema OK")
    elif args.cmd == "list":
        for e in load_entries():
            print(f"{e.get('id')} | {e.get('class')} | {e.get('status')} | {e.get('title')}")
    elif args.cmd == "append":
        append_entry(args)


if __name__ == "__main__":
    main()
