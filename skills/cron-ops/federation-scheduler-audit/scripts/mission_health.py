#!/usr/bin/env python3
"""
mission_health.py -- "did the promised thing actually HAPPEN?"

Companion to /root/.hermes/skills/cron-ops/federation-scheduler-audit/SKILL.md, which states:

    "`hermes cron doctor` returning no issues is a statement about the BOOK,
     not about execution. It cannot see a job that holds `enabled: true` /
     `last_status: ok` while never firing."

That skill describes the check. This performs it.

Mechanism health  = the daemon runs, the config validates, no exception was raised.
Mission health    = the expected event occurred inside its promised window.

A job may be mechanism-healthy and mission-dead for weeks. That class of failure is what
this tool makes visible.

USAGE
  mission_health.py                 human summary
  mission_health.py --json          machine record
  mission_health.py --grace 1.5     tolerance in units of the job's own interval
  mission_health.py --no-write      do not stamp state

EXIT
  0 = every enabled job fired inside its promised window
  3 = >=1 SILENT (missed >= 1 full window)  -> alarmable
  2 = the job book itself is unreadable

SELF-TEST (run after ANY change to the parser; the verdict is worthless without it)
  daily 22:00 over 13.5 days -> 13
  Mon 06:30 over 23 days     -> 3
  daily 02:00, last fire 9h ago -> 0 (must read OK, not SILENT)
  Sun/Tue/Thu/Sat 07:00 over 13 days -> 7
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import socket
import sys
import urllib.error
import urllib.request
from pathlib import Path

MYT = dt.timezone(dt.timedelta(hours=8))
JOBS = Path("/root/.hermes/cron/jobs.json")
OUT_DIR = Path("/root/.hermes/cron/output")
STATE_DIR = Path("/root/.local/share/arifos/state")

# Grace: how far past a due fire we tolerate before calling it silent.
# 1.5 units == one missed window plus half, which absorbs clock skew and one skipped tick
# without crying wolf.
DEFAULT_GRACE = 1.5


def _field(spec: str, lo: int, hi: int) -> set[int]:
    out: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        step = 1
        if "/" in part:
            part, s = part.split("/", 1)
            step = int(s)
        if part == "*":
            out |= set(range(lo, hi + 1, step))
        elif "-" in part:
            a, b = part.split("-", 1)
            out |= set(range(int(a), int(b) + 1, step))
        else:
            out.add(int(part))
    return out


def fires_between(expr: str, start: dt.datetime, end: dt.datetime, cap: int = 200000) -> int:
    """Count 5-field cron fires in (start, end]. Minute-granularity brute force:
    boring, exact, and impossible to get subtly wrong."""
    f = expr.split()
    if len(f) != 5:
        return -1
    mins, hrs, dom, mon, dow = (_field(f[0], 0, 59), _field(f[1], 0, 23),
                                _field(f[2], 1, 31), _field(f[3], 1, 12), _field(f[4], 0, 6))
    dom_restricted = f[2] != "*"
    dow_restricted = f[4] != "*"
    n = start.replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
    count = steps = 0
    while n <= end and steps < cap:
        steps += 1
        if n.minute in mins and n.hour in hrs and n.month in mon:
            d_ok = n.day in dom
            w_ok = (n.weekday() + 1) % 7 in dow          # cron dow: Sun=0
            # standard cron: if BOTH dom and dow are restricted, either may match
            day_ok = (d_ok or w_ok) if (dom_restricted and dow_restricted) else (d_ok and w_ok)
            if day_ok:
                count += 1
        n += dt.timedelta(minutes=1)
    return count


def interval_hours(expr: str) -> float | None:
    """Nominal spacing, used as the grace unit."""
    f = expr.split()
    if len(f) != 5:
        return None
    mins, hrs, dom, mon, dow = f
    if mins.startswith("*/"):
        return max(1.0, int(mins[2:]) / 60.0)
    if hrs == "*":
        return 1.0
    if hrs.startswith("*/"):
        return float(hrs[2:])
    if dow != "*" and dom == "*":
        return 24 * 7.0
    return 24.0


def parse_interval_display(display: str) -> float | None:
    """'every 120m' / 'every 6h' -> hours."""
    m = re.match(r"every\s+(\d+)\s*([mh])", str(display or ""), re.I)
    if not m:
        return None
    v = int(m.group(1))
    return v / 60.0 if m.group(2).lower() == "m" else float(v)


def assess(job: dict, now: dt.datetime, grace: float) -> dict:
    name = job.get("name", "?")
    sched = job.get("schedule", {}) or {}
    expr = sched.get("expr") or job.get("schedule_display") or ""
    kind = sched.get("kind", "cron")
    last_raw = job.get("last_run_at")
    try:
        last = dt.datetime.fromisoformat(str(last_raw).replace("Z", "+00:00")).astimezone(MYT)
    except Exception:
        last = None

    if kind == "interval" or str(expr).lower().startswith("every"):
        iv = parse_interval_display(job.get("schedule_display") or expr) or 1.0
        missed, window = None, iv
    else:
        iv = interval_hours(str(expr))
        if iv is None:
            return {"name": name, "verdict": "UNPARSED",
                    "detail": f"cannot read schedule '{expr}'",
                    "last_run_at": last_raw, "expr": str(expr)}
        missed = -1 if last is None else fires_between(str(expr), last, now)
        window = iv

    age_h = (now - last).total_seconds() / 3600 if last else None
    tol = grace * window

    if last is None or age_h is None:
        verdict, why = "SILENT", "enabled but has never run"
    elif age_h > tol:
        missed_txt = missed if isinstance(missed, int) and missed >= 0 else "?"
        verdict = "SILENT"
        why = f"last fire {age_h:.0f}h ago, tolerance {tol:.0f}h ({missed_txt} fires missed)"
    else:
        verdict, why = "OK", f"fired {age_h:.1f}h ago (tolerance {tol:.0f}h)"

    artifact = False
    try:
        if OUT_DIR.exists():
            newest = max((p.stat().st_mtime for p in OUT_DIR.rglob("*") if p.is_file()), default=0)
            artifact = (dt.datetime.now().timestamp() - newest) < 86400
    except Exception:
        pass

    return {
        "name": name, "verdict": verdict, "detail": why, "expr": str(expr),
        "schedule_display": job.get("schedule_display"), "last_run_at": last_raw,
        "age_h": None if age_h is None else round(age_h, 1),
        "tolerance_h": round(tol, 1),
        "fires_missed": missed if isinstance(missed, int) and missed >= 0 else None,
        "book_status": job.get("last_status"), "lane": job.get("lane"),
        "job_id": job.get("id"), "any_artifact_last_24h": artifact,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--grace", type=float, default=DEFAULT_GRACE)
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--self-test", action="store_true",
                    help="assert the parser against hand-computed windows, then exit")
    a = ap.parse_args()
    now = dt.datetime.now(MYT)

    if a.self_test:
        cases = [
            ("0 22 * * *", dt.datetime(2026, 9, 2, 22, 1, tzinfo=MYT),
             dt.datetime(2026, 9, 16, 11, 0, tzinfo=MYT), 13),
            ("30 6 * * 1", dt.datetime(2026, 8, 24, 6, 33, tzinfo=MYT),
             dt.datetime(2026, 9, 16, 11, 0, tzinfo=MYT), 3),
            ("0 2 * * *", dt.datetime(2026, 9, 16, 2, 3, tzinfo=MYT),
             dt.datetime(2026, 9, 16, 11, 0, tzinfo=MYT), 0),
            ("0 7 * * 0,2,4,6", dt.datetime(2026, 9, 3, 7, 2, tzinfo=MYT),
             dt.datetime(2026, 9, 16, 11, 0, tzinfo=MYT), 7),
        ]
        bad = 0
        for expr, s, e, expect in cases:
            got = fires_between(expr, s, e)
            ok = got == expect
            bad += 0 if ok else 1
            print(f"{'PASS' if ok else 'FAIL'}  {expr:18s} got={got:3d} expect={expect:3d}")
        return 1 if bad else 0

    if not JOBS.exists():
        print(f"FATAL: job book unreadable: {JOBS}", file=sys.stderr)
        return 2
    book = json.loads(JOBS.read_text(encoding="utf-8"))
    jobs = book.get("jobs", book)

    results = [assess(j, now, a.grace) for j in jobs if j.get("enabled")]
    silent = [r for r in results if r["verdict"] == "SILENT"]
    migrated = [j.get("name") for j in jobs
                if not j.get("enabled") and j.get("state") == "migrated"]

    record = {
        "schema": "arifos.mission_health.v1", "ts_myt": now.isoformat(),
        "book": str(JOBS),
        "book_mtime": dt.datetime.fromtimestamp(JOBS.stat().st_mtime, MYT).isoformat(),
        "enabled_count": len(results), "silent_count": len(silent),
        "ok_count": len(results) - len(silent), "grace_units": a.grace,
        "silent": silent, "all_enabled": results,
        "migrated_off_host": migrated,
    }

    if not a.no_write:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        (STATE_DIR / f"mission-health-{now.strftime('%Y-%m-%d')}.json").write_text(
            json.dumps(record, indent=1, ensure_ascii=False), encoding="utf-8")

    if a.json:
        print(json.dumps(record, indent=1, ensure_ascii=False))
    else:
        print(f"MISSION HEALTH -- {now.strftime('%a %d %b %Y %H:%M')} MYT")
        print(f"   book: {JOBS} (mtime {record['book_mtime'][:16]})")
        print(f"   enabled={len(results)}  mission-OK={record['ok_count']}  SILENT={len(silent)}")
        if silent:
            print("\n   ENABLED BUT NOT HAPPENING:")
            for r in sorted(silent, key=lambda x: -(x.get("age_h") or 0)):
                print(f"     - {r['name']}  [{r['schedule_display']}]")
                print(f"       {r['detail']} | book says status={r['book_status']}")
        else:
            print("\n   every enabled job fired inside its promised window")
        if migrated:
            print(f"\n   (booked as migrated off this host: {len(migrated)} -- VERIFY the target")
            print("    actually runs a scheduler before treating these as live; see Step 2b)")
        print("\n   Reminder: this reads EXECUTION, not the book.")

    return 3 if silent else 0


if __name__ == "__main__":
    sys.exit(main())
