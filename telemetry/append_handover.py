#!/usr/bin/env python3
import os, sys, json, hashlib, fcntl, argparse
from datetime import datetime, timezone
from pathlib import Path

TELEMETRY_DIR = Path("/root/AAA/telemetry")
HANDOVER_LOG = TELEMETRY_DIR / "handover.log"

ALLOWED_CATEGORIES = {
    "collision_fix",
    "blueprint_map",
    "config_patch",
    "port_shift",
    "drift_alert",
    "seal_record",
    "handover_intake",
    "sot_mutation",
    "constitutional_pivot",
}

ALLOWED_STATUSES = {"ACTIVE", "RESOLVED", "SEALED", "SUPERSEDED"}

def get_last_line_hash(log_path: Path) -> str:
    if not log_path.exists() or log_path.stat().st_size == 0:
        return "GENESIS"
    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
        if not lines:
            return "GENESIS"
        last_line = lines[-1]
        return hashlib.sha256(last_line.encode("utf-8")).hexdigest()

def append_record(
    actor: str,
    session_id: str,
    category: str,
    summary: str,
    sots_touched: list,
    delta_s: float,
    status: str = "ACTIVE",
    floor_impact: list = None,
    ts: str = None
) -> dict:
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"Invalid category {category}. Must be one of {sorted(ALLOWED_CATEGORIES)}")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status {status}. Must be one of {sorted(ALLOWED_STATUSES)}")
    if delta_s > 0:
        raise ValueError(f"Entropy violation: delta_s must be <= 0, got {delta_s}")

    timestamp = ts or datetime.now(timezone.utc).isoformat()
    floors = floor_impact or ["F11"]

    with open(HANDOVER_LOG, "a+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            prev_hash = get_last_line_hash(HANDOVER_LOG)
            record = {
                "ts": timestamp,
                "actor": actor,
                "session_id": session_id,
                "category": category,
                "summary": summary[:120],
                "sots_touched": sots_touched,
                "delta_s": round(float(delta_s), 4),
                "status": status,
                "prev_hash": prev_hash,
                "floor_impact": floors
            }
            line = json.dumps(record, separators=(",", ":"))
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())
            return record
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

def main():
    ap = argparse.ArgumentParser(description="Append entry to telemetry handover.log")
    ap.add_argument("--actor", required=True, help="Actor ID")
    ap.add_argument("--session", required=True, help="Session ID")
    ap.add_argument("--category", required=True, choices=sorted(ALLOWED_CATEGORIES), help="Category enum")
    ap.add_argument("--summary", required=True, help="Single-line summary")
    ap.add_argument("--sots", nargs="*", default=[], help="SOT paths touched")
    ap.add_argument("--delta-s", type=float, default=0.0, help="Delta S")
    ap.add_argument("--status", default="ACTIVE", choices=sorted(ALLOWED_STATUSES))
    ap.add_argument("--floors", nargs="*", default=["F11"], help="Floors impacted")
    
    args = ap.parse_args()
    try:
        rec = append_record(
            actor=args.actor,
            session_id=args.session,
            category=args.category,
            summary=args.summary,
            sots_touched=args.sots,
            delta_s=args.delta_s,
            status=args.status,
            floor_impact=args.floors
        )
        print(json.dumps(rec, indent=2))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
