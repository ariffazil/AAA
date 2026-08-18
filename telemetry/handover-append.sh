#!/usr/bin/env bash
# Append one handover line. Does not compute FQ. Does not write SOT.
# Usage:
#   handover-append.sh <category> "<summary ≤100>" [sot,sot] [F2,F11]
# Env: HANDOVER_ACTOR HANDOVER_SESSION HANDOVER_DELTA_S
set -euo pipefail
exec python3 - "$@" <<'PY'
import fcntl, hashlib, json, os, sys
from datetime import datetime, timezone

LOG = "/root/AAA/telemetry/handover.log"
CATS = {
    "collision_fix", "blueprint_map", "config_patch", "port_shift",
    "drift_alert", "seal_record", "handover_intake", "sot_mutation",
    "constitutional_pivot",
}
GENESIS = "0" * 64

def usage():
    sys.stderr.write(
        "usage: handover-append.sh <category> \"<summary>\" [sot,sot] [F2,F11]\n"
    )
    sys.exit(2)

args = sys.argv[1:]
if len(args) < 2:
    usage()
cat, summary = args[0], args[1][:100]
if cat not in CATS:
    sys.stderr.write(f"unknown category: {cat}\nallowed: {' '.join(sorted(CATS))}\n")
    sys.exit(2)
sots = [s.strip() for s in (args[2] if len(args) > 2 else "").split(",") if s.strip()]
floors = [s.strip() for s in (args[3] if len(args) > 3 else "").split(",") if s.strip()]

os.makedirs(os.path.dirname(LOG), exist_ok=True)
fd = os.open(LOG, os.O_RDWR | os.O_CREAT | os.O_APPEND, 0o644)
try:
    fcntl.flock(fd, fcntl.LOCK_EX)
    # prev line: read file (not via the append fd offset)
    prev_hash = GENESIS
    if os.path.getsize(LOG) > 0:
        with open(LOG, "rb") as rf:
            data = rf.read()
        if data:
            last = data.rsplit(b"\n", 2)
            # file ends with \n → last nonempty line is last[ -2] if trailing nl
            lines = [ln + b"\n" for ln in data.split(b"\n") if ln]
            if lines:
                prev_hash = hashlib.sha256(lines[-1]).hexdigest()
    rec = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "actor": os.environ.get("HANDOVER_ACTOR") or os.environ.get("USER") or "clerk",
        "session_id": os.environ.get("HANDOVER_SESSION") or os.environ.get("ARIFOS_SESSION_ID") or "local",
        "category": cat,
        "summary": summary,
        "sots_touched": sots,
        "delta_s": float(os.environ.get("HANDOVER_DELTA_S") or "0"),
        "status": os.environ.get("HANDOVER_STATUS") or "ACTIVE",
        "prev_hash": prev_hash,
        "floor_impact": floors,
    }
    line = (json.dumps(rec, ensure_ascii=False) + "\n").encode("utf-8")
    os.write(fd, line)
    os.fsync(fd)
    sys.stdout.write(rec["ts"] + "\n")
finally:
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)
PY
