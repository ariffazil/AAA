"""BRIDGING_SEAL override tests — Stage 4 (2026-07-05).

Constitutional design constraints (F1/F2/F11/F13):
  1. actor_verified stays FALSE. Only actor_override toggles true.
  2. Every BRIDGING_SEAL must seal to VAULT999 first (audit-first).
  3. TTL bounded: 900s default, 3600s max.
  4. FAIL-CLOSED: stubs raise NotImplementedError; no fake crypto.

These tests verify the stubs RESPECT constraints — they are the
contract for what real implementations must keep.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta

import pytest


def test_ttl_default_is_fifteen_minutes(identity_pkgs):
    bs = identity_pkgs.bridge_seal_module
    assert bs.ttl_default_seconds() == 900


def test_ttl_max_is_one_hour(identity_pkgs):
    bs = identity_pkgs.bridge_seal_module
    assert bs.max_ttl_seconds() == 3600


def test_estimated_expiry_arithmetic(identity_pkgs):
    bs = identity_pkgs.bridge_seal_module
    BridgingSealRequest = bs.BridgingSealRequest
    estimated_expiry = bs.estimated_expiry

    start = datetime(2026, 7, 5, 13, 0, 0, tzinfo=timezone.utc)
    req = BridgingSealRequest(
        sovereign_authorization="yes seal",
        intent="test",
        ttl_seconds=900,
    )
    exp = estimated_expiry(req, start_epoch=start)
    assert exp == start + timedelta(seconds=900)
