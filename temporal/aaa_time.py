#!/usr/bin/env python3
"""aaa-time — AAA Temporal Authority Provider

The canonical `now` provider for the arifOS federation.
Reads system UTC + monotonic clock and emits arifos.time.v1.

Usage:
    aaa-time now [--tz Asia/Kuala_Lumpur] [--format json|compact]
    aaa-time validate <json-file>
    aaa-time policy

Design:
    - Wall clock for "what time is it"
    - Monotonic clock for "how long has it been"
    - NTP sync status from timedatectl
    - TTL enforcement (fresh_for_seconds)
    - Feature flag: TEMPORAL_GROUNDING_ENFORCED

CHRON is NOT a clock. CHRON is a temporal consequence tracker.
This tool is the clock.

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

# ── Constants ──

SCHEMA_VERSION = "arifos.time.v1"
DEFAULT_TZ = "Asia/Kuala_Lumpur"
DEFAULT_TTL_SECONDS = 30
ARIF_EPOCH = "1990-05-22T00:00:00+08:00"
ARIF_EPOCH_LABEL = "Arif Fazil"
FEATURE_FLAG = "TEMPORAL_GROUNDING_ENFORCED"

# ── Policy ──

TEMPORAL_POLICY = {
    "timezone": DEFAULT_TZ,
    "anchor_ttl_seconds": 300,
    "claim_refresh_ttl_seconds": 60,
    "require_refresh_for": [
        "current_time",
        "current_part_of_day",
        "today_tomorrow_yesterday",
        "deadline_status",
        "elapsed_duration",
        "schedule_execution",
    ],
    "fallback": {
        "on_clock_unavailable": "state uncertainty; never infer",
    },
    "chron_excluded_from_now": True,
}


def _get_tz_offset(tz_name: str) -> tuple[str, float]:
    """Get UTC offset string and hours for a timezone name."""
    # Map common timezone names
    tz_map = {
        "Asia/Kuala_Lumpur": ("+08:00", 8.0),
        "Asia/Singapore": ("+08:00", 8.0),
        "Asia/Tokyo": ("+09:00", 9.0),
        "UTC": ("+00:00", 0.0),
        "US/Eastern": ("-05:00", -5.0),
        "US/Pacific": ("-08:00", -8.0),
        "Europe/London": ("+00:00", 0.0),
    }
    if tz_name in tz_map:
        return tz_map[tz_name]
    # Default to system local
    offset = time.timezone if time.daylight == 0 else time.altzone
    offset_hours = -offset / 3600
    sign = "+" if offset_hours >= 0 else "-"
    h = int(abs(offset_hours))
    m = int((abs(offset_hours) - h) * 60)
    return (f"{sign}{h:02d}:{m:02d}", offset_hours)


def _check_clock_status() -> str:
    """Check NTP synchronization status."""
    try:
        result = subprocess.run(
            ["timedatectl", "show", "--property=NTPSynchronized", "--value"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            synced = result.stdout.strip()
            if synced == "yes":
                return "OK"
            else:
                return "NTP_UNSYNC"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback: check if chrony is running
    try:
        result = subprocess.run(
            ["chronyc", "tracking"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and "Leap status" in result.stdout:
            return "OK"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return "UNKNOWN"


def now(tz_name: str = DEFAULT_TZ, ttl: int = DEFAULT_TTL_SECONDS) -> dict[str, Any]:
    """Get the current time as an arifos.time.v1 response.

    Returns both wall clock and monotonic clock.
    Wall clock for "what time is it", monotonic for "how long".
    """
    # Wall clock — UTC
    utc_now = datetime.now(timezone.utc)

    # Local time
    offset_str, offset_hours = _get_tz_offset(tz_name)
    local_tz = timezone(timedelta(hours=offset_hours))
    local_now = utc_now.astimezone(local_tz)

    # Monotonic clock (unaffected by NTP adjustments)
    monotonic_ns = time.monotonic_ns()

    # Unix milliseconds
    unix_ms = int(utc_now.timestamp() * 1000)

    # Clock health
    clock_status = _check_clock_status()

    response = {
        "schema": SCHEMA_VERSION,
        "source": "vps_system_clock",
        "observed_at_utc": utc_now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "local": local_now.strftime(f"%Y-%m-%dT%H:%M:%S{offset_str}"),
        "timezone": tz_name,
        "unix_ms": unix_ms,
        "monotonic_ns": monotonic_ns,
        "fresh_for_seconds": ttl,
        "clock_status": clock_status,
        "authority": "LOCAL_RUNTIME",
    }

    # Optional: Arif epoch calculation
    try:
        epoch_dt = datetime.fromisoformat(ARIF_EPOCH)
        seconds_since = int((utc_now - epoch_dt).total_seconds())
        response["epoch_label"] = ARIF_EPOCH_LABEL
        response["epoch_since"] = ARIF_EPOCH
        response["seconds_since_epoch"] = seconds_since
    except Exception:
        pass  # Non-critical

    return response


def validate(data: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate a dict against the arifos.time.v1 schema.

    Returns (is_valid, list_of_errors).
    """
    errors = []

    required = [
        "schema", "source", "observed_at_utc", "local", "timezone",
        "unix_ms", "monotonic_ns", "fresh_for_seconds", "clock_status", "authority"
    ]
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if data.get("schema") != SCHEMA_VERSION:
        errors.append(f"Invalid schema: expected '{SCHEMA_VERSION}', got '{data.get('schema')}'")

    valid_sources = ["vps_system_clock", "public_api", "carry_forward_anchor"]
    if data.get("source") not in valid_sources:
        errors.append(f"Invalid source: '{data.get('source')}' not in {valid_sources}")

    valid_statuses = ["OK", "NTP_UNSYNC", "DRIFT_DETECTED", "UNKNOWN"]
    if data.get("clock_status") not in valid_statuses:
        errors.append(f"Invalid clock_status: '{data.get('clock_status')}' not in {valid_statuses}")

    valid_authorities = ["LOCAL_RUNTIME", "PUBLIC_API", "SESSION_ANCHOR"]
    if data.get("authority") not in valid_authorities:
        errors.append(f"Invalid authority: '{data.get('authority')}' not in {valid_authorities}")

    if not isinstance(data.get("unix_ms"), int) or data.get("unix_ms", 0) < 0:
        errors.append("unix_ms must be a non-negative integer")

    if not isinstance(data.get("monotonic_ns"), int) or data.get("monotonic_ns", 0) < 0:
        errors.append("monotonic_ns must be a non-negative integer")

    return (len(errors) == 0, errors)


def is_fresh(data: dict[str, Any]) -> tuple[bool, int]:
    """Check if a time reading is still within its TTL.

    Returns (is_fresh, age_ms).
    """
    observed_str = data.get("observed_at_utc", "")
    ttl_seconds = data.get("fresh_for_seconds", DEFAULT_TTL_SECONDS)

    try:
        observed = datetime.fromisoformat(observed_str.replace("Z", "+00:00"))
        now_utc = datetime.now(timezone.utc)
        age = now_utc - observed
        age_ms = int(age.total_seconds() * 1000)
        is_ok = age.total_seconds() <= ttl_seconds
        return (is_ok, age_ms)
    except Exception:
        return (False, -1)


def feature_enabled() -> bool:
    """Check if temporal grounding enforcement is enabled."""
    val = os.environ.get(FEATURE_FLAG, "false").lower()
    return val in ("true", "1", "yes")


# ── CLI ──

def main():
    parser = argparse.ArgumentParser(
        description="AAA Temporal Authority — the canonical `now` provider",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  aaa-time now                          # Default: KL timezone, JSON
  aaa-time now --tz UTC --format compact
  aaa-time validate /tmp/time.json      # Validate a time reading
  aaa-time policy                       # Show temporal policy
  aaa-time enforce                      # Check if enforcement is on

CHRON is NOT a clock. This is the clock.
DITEMPA BUKAN DIBERI ⚒️
"""
    )
    sub = parser.add_subparsers(dest="command")

    # now
    now_parser = sub.add_parser("now", help="Get current time as arifos.time.v1")
    now_parser.add_argument("--tz", default=DEFAULT_TZ, help="IANA timezone")
    now_parser.add_argument("--format", choices=["json", "compact"], default="json")
    now_parser.add_argument("--ttl", type=int, default=DEFAULT_TTL_SECONDS, help="Freshness TTL in seconds")

    # validate
    val_parser = sub.add_parser("validate", help="Validate an arifos.time.v1 JSON file")
    val_parser.add_argument("file", help="Path to JSON file to validate")

    # policy
    sub.add_parser("policy", help="Show temporal grounding policy")

    # enforce
    sub.add_parser("enforce", help="Check if temporal grounding enforcement is enabled")

    # check (validate + freshness)
    check_parser = sub.add_parser("check", help="Check if a time reading is valid and fresh")
    check_parser.add_argument("file", help="Path to JSON file to check")

    args = parser.parse_args()

    if args.command == "now":
        response = now(tz_name=args.tz, ttl=args.ttl)
        if args.format == "compact":
            print(f"{response['local']} ({response['timezone']}) | UTC {response['observed_at_utc']} | clock={response['clock_status']}")
        else:
            print(json.dumps(response, indent=2))

    elif args.command == "validate":
        try:
            data = json.loads(Path(args.file).read_text())
        except Exception as e:
            print(f"ERROR: Cannot read {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
        is_valid, errors = validate(data)
        if is_valid:
            print(f"✅ VALID — {SCHEMA_VERSION}")
        else:
            print(f"❌ INVALID — {len(errors)} error(s):")
            for err in errors:
                print(f"  - {err}")
            sys.exit(1)

    elif args.command == "policy":
        print(json.dumps(TEMPORAL_POLICY, indent=2))

    elif args.command == "enforce":
        enabled = feature_enabled()
        flag = os.environ.get(FEATURE_FLAG, "false")
        print(json.dumps({
            "feature_flag": FEATURE_FLAG,
            "current_value": flag,
            "enforcement_active": enabled,
            "policy": TEMPORAL_POLICY,
        }, indent=2))

    elif args.command == "check":
        try:
            data = json.loads(Path(args.file).read_text())
        except Exception as e:
            print(f"ERROR: Cannot read {args.file}: {e}", file=sys.stderr)
            sys.exit(1)

        is_valid, val_errors = validate(data)
        is_ok, age_ms = is_fresh(data)

        result = {
            "valid": is_valid,
            "fresh": is_ok,
            "age_ms": age_ms,
            "ttl_seconds": data.get("fresh_for_seconds", DEFAULT_TTL_SECONDS),
            "validation_errors": val_errors if not is_valid else [],
            "enforcement_active": feature_enabled(),
        }

        if not is_valid:
            result["verdict"] = "INVALID"
        elif not is_ok:
            result["verdict"] = "STALE"
        elif not feature_enabled():
            result["verdict"] = "FRESH_BUT_ENFORCEMENT_OFF"
        else:
            result["verdict"] = "FRESH_AND_ENFORCED"

        print(json.dumps(result, indent=2))
        sys.exit(0 if is_valid else 1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()