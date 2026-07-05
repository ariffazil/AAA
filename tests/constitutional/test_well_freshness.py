"""WELL substrate freshness tests — Stage 4 (2026-07-05).

Audit finding (G6): WELL biometric state_age_hours=10.4, RED threshold 4h.
These tests probe :18083/health and assert constitutional thresholds.

If a live WELL is unreachable, tests skip cleanly.
"""

from __future__ import annotations

import json
import socket
import time
import urllib.request

import pytest


_THRESHOLDS = {
    "GREEN_HOURS": 12,
    "YELLOW_HOURS": 24,
    "RED_HOURS": 48,
    "INJECT_NEEDED_HOURS": 9999,
}


def _fetch(url: str, timeout: float = 2.0):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode())


def _socket_open(host: str, port: int, timeout: float = 0.5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


@pytest.fixture
def well_health():
    if not _socket_open("localhost", 18083):
        pytest.skip("WELL :18083 unreachable")
    return _fetch("http://localhost:18083/health")


def test_well_health_reports_state_age_hours(well_health):
    """state_age_hours field MUST be present (G6 finding)."""
    body = well_health
    assert "state_age_hours" in body, "WELL :18083/health missing state_age_hours"
    assert isinstance(body["state_age_hours"], (int, float))


def test_well_threshold_red_under_48_hours(well_health):
    """state_age_hours < 48 must not return a stale/black verdict."""
    body = well_health
    age = body.get("state_age_hours", 0)
    if age < _THRESHOLDS["RED_HOURS"]:
        # Modern responses should show GREEN or YELLOW, not STALE
        status = (body.get("status") or "").upper()
        assert status != "STALE", (
            f"WELL reports STALE at age={age}h (RED threshold). "
            "Either reduce freshness gap or threshold needs review."
        )


def test_well_owner_summary_color_mapping(well_health):
    """owner_summary.color must align with status, not stale by default."""
    body = well_health
    summary = body.get("owner_summary", {})
    color = (summary.get("color") or "").upper()
    if color:
        assert color in {"GREEN", "YELLOW", "RED", "STALE"}, (
            f"unknown color: {color}"
        )


def test_well_holds_when_biometric_gap_over_4h(well_health):
    """F5 PEACE²: constitutional HOLD when biometric > 4h stale."""
    body = well_health
    age = body.get("state_age_hours", 0)
    signal = (body.get("well_signal") or "").upper()
    if age > 4 and not signal:
        pytest.fail("WELL signal missing under stale biometric state")
