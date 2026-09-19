"""temporal_root — carry_forward temporal anchor injection.

Provides the TemporalContext object that every AAA session
reads at wake-up. NOT a live clock — an anchor with TTL.

Import from carry_forward.py or any agent init script:
    from temporal_root import get_temporal_root, is_anchor_fresh

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

# ── Import the canonical provider ──
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aaa_time import now as aaa_now, DEFAULT_TZ, DEFAULT_TTL_SECONDS

# ── Policy constants ──

ANCHOR_TTL_SECONDS = 300      # 5 minutes — how long temporal_root stays valid
CLAIM_REFRESH_TTL_SECONDS = 60  # 1 minute — must refresh before any current-time claim
FEATURE_FLAG = "TEMPORAL_GROUNDING_ENFORCED"


def get_temporal_root(tz: str = DEFAULT_TZ) -> dict[str, Any]:
    """Generate a temporal_root object for carry_forward injection.

    This is called ONCE at session init. It captures the moment
    the session started. It does NOT stay fresh forever.

    The anchor is an arifos.time.v1 reading plus session metadata.
    """
    time_reading = aaa_now(tz_name=tz, ttl=ANCHOR_TTL_SECONDS)

    return {
        **time_reading,
        "source": "vps_system_clock",
        "authority": "SESSION_ANCHOR",
        "anchor_ttl_seconds": ANCHOR_TTL_SECONDS,
        "claim_refresh_ttl_seconds": CLAIM_REFRESH_TTL_SECONDS,
        "injected_at_utc": time_reading["observed_at_utc"],
        "requires_refresh_after_utc": _add_seconds_iso(
            time_reading["observed_at_utc"], ANCHOR_TTL_SECONDS
        ),
        "policy": {
            "timezone": tz,
            "anchor_ttl_seconds": ANCHOR_TTL_SECONDS,
            "claim_refresh_ttl_seconds": CLAIM_REFRESH_TTL_SECONDS,
            "require_refresh_for": [
                "current_time",
                "current_part_of_day",
                "today_tomorrow_yesterday",
                "deadline_status",
                "elapsed_duration",
                "schedule_execution",
            ],
            "fallback": "state uncertainty; never infer",
            "chron_excluded_from_now": True,
        },
    }


def is_anchor_fresh(temporal_root: dict[str, Any]) -> tuple[bool, int]:
    """Check if a temporal_root anchor is still within its TTL.

    Returns (is_fresh, age_ms).
    """
    injected_str = temporal_root.get("injected_at_utc", "")
    ttl = temporal_root.get("anchor_ttl_seconds", ANCHOR_TTL_SECONDS)

    try:
        injected = datetime.fromisoformat(injected_str.replace("Z", "+00:00"))
        now_utc = datetime.now(timezone.utc)
        age = now_utc - injected
        age_ms = int(age.total_seconds() * 1000)
        return (age.total_seconds() <= ttl, age_ms)
    except Exception:
        return (False, -1)


def needs_refresh_for_claim(temporal_root: dict[str, Any]) -> bool:
    """Check if a current-time claim needs a fresh reading.

    Returns True if the anchor is older than claim_refresh_ttl_seconds.
    """
    injected_str = temporal_root.get("injected_at_utc", "")
    ttl = temporal_root.get("claim_refresh_ttl_seconds", CLAIM_REFRESH_TTL_SECONDS)

    try:
        injected = datetime.fromisoformat(injected_str.replace("Z", "+00:00"))
        now_utc = datetime.now(timezone.utc)
        age = (now_utc - injected).total_seconds()
        return age > ttl
    except Exception:
        return True  # Can't determine → needs refresh


def _add_seconds_iso(iso_str: str, seconds: int) -> str:
    """Add seconds to an ISO-8601 UTC string."""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        result = dt + timedelta(seconds=seconds)
        return result.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return ""


if __name__ == "__main__":
    # Quick test: generate and display a temporal_root
    root = get_temporal_root()
    print(json.dumps(root, indent=2))
    print()
    fresh, age = is_anchor_fresh(root)
    print(f"Fresh: {fresh}, Age: {age}ms")
    print(f"Needs refresh for claim: {needs_refresh_for_claim(root)}")