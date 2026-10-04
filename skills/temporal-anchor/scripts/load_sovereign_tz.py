#!/usr/bin/env python3
"""
load_sovereign_tz.py — Canonical sovereign timezone loader for any AAA agent script.

Single source of truth: /root/.local/share/arifos/state.json.iana_tz (F13 SOVEREIGN).
Falls back to Asia/Kuala_Lumpur (UTC+8, alias MYT) if state.json is missing or malformed.

Usage:
  # As module (preferred — copy-paste import)
  from load_sovereign_tz import load_sovereign_tz, SOVEREIGN_TZ, now_myt, format_myt
  print(format_myt(datetime.now(timezone.utc)))

  # As CLI
  python3 load_sovereign_tz.py --now         # print current MYT
  python3 load_sovereign_tz.py --json        # print canonical state
  python3 load_sovereign_tz.py --check       # exit 0 if state.json healthy, 1 if drift

This is the canonical loader pattern referenced from temporal-anchor SKILL.md
(zen/temporal-anchor/SKILL.md, "Mandatory canonical loader" section, binding 2026-08-11).

DITEMPA BUKAN DIBEI — every AAA agent handling timestamps imports this.
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

STATE_FILE = Path("/root/.local/share/arifos/state.json")
FALLBACK = ("Asia/Kuala_Lumpur", 8, "MYT")


def load_sovereign_tz():
    """Return (iana_tz, utc_offset_hours, tz_alias). Canonical from state.json, fallback MYT+8.

    Never raises — any failure (missing file, malformed JSON, wrong types) returns
    the FALLBACK tuple. Callers can rely on the return shape.
    """
    try:
        if not STATE_FILE.exists():
            return FALLBACK
        d = json.loads(STATE_FILE.read_text())
        iana = d.get("iana_tz") or d.get("timezone")
        off = d.get("utc_offset_hours")
        alias = d.get("tz_alias")
        if not iana:
            return FALLBACK
        return (iana, int(off) if off is not None else 8, alias or "MYT")
    except Exception:
        return FALLBACK


# Module-level constants — set once at import time
_IANA, _OFFSET_HOURS, _TZ_LABEL = load_sovereign_tz()
SOVEREIGN_TZ = timezone(timedelta(hours=_OFFSET_HOURS))
TZ_LABEL = _TZ_LABEL
TZ_IANA = _IANA
TZ_OFFSET_HOURS = _OFFSET_HOURS
TZ_SOURCE = f"state.json ({_IANA})" if STATE_FILE.exists() else "fallback (MYT+8 hardcoded)"


def now_myt():
    """Return current datetime in sovereign timezone."""
    return datetime.now(timezone.utc).astimezone(SOVEREIGN_TZ)


def format_myt(dt_utc, fmt=None):
    """Format a UTC datetime as sovereign-local string. Default: 'YYYY-MM-DD HH:MM:SS TZ (Day)'."""
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    dt_local = dt_utc.astimezone(SOVEREIGN_TZ)
    if fmt is None:
        fmt = f"%Y-%m-%d %H:%M:%S {TZ_LABEL} (%A)"
    return dt_local.strftime(fmt)


def check_drift():
    """Return (ok: bool, message: str). True if state.json exists and is well-formed."""
    if not STATE_FILE.exists():
        return False, f"state.json missing at {STATE_FILE}"
    try:
        d = json.loads(STATE_FILE.read_text())
        if not d.get("iana_tz"):
            return False, "state.json.iana_tz missing"
        return True, f"OK: {d.get('iana_tz')} (offset +{d.get('utc_offset_hours', '?')}h)"
    except Exception as e:
        return False, f"state.json malformed: {e}"


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--now" in args:
        print(format_myt(datetime.now(timezone.utc)))
    elif "--json" in args:
        print(json.dumps({
            "iana_tz": TZ_IANA,
            "utc_offset_hours": TZ_OFFSET_HOURS,
            "tz_label": TZ_LABEL,
            "source": TZ_SOURCE,
            "state_file_exists": STATE_FILE.exists(),
            "now_myt": format_myt(datetime.now(timezone.utc)),
            "now_utc": datetime.now(timezone.utc).isoformat(),
        }, indent=2, ensure_ascii=False))
    elif "--check" in args:
        ok, msg = check_drift()
        print(msg)
        sys.exit(0 if ok else 1)
    else:
        print(f"IANA: {TZ_IANA}  Offset: +{TZ_OFFSET_HOURS}h  Label: {TZ_LABEL}")
        print(f"Source: {TZ_SOURCE}")
        print(f"State file: {STATE_FILE} ({'exists' if STATE_FILE.exists() else 'MISSING'})")
        print(f"Current MYT: {format_myt(datetime.now(timezone.utc))}")
