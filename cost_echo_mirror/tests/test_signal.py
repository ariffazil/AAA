"""Tests for cost_echo.signal thresholds, incl. exact boundaries."""

from __future__ import annotations

from cost_echo.ledger import LedgerRow
from cost_echo.signal import Thresholds, classify


def _row(drain: float, closure: float) -> LedgerRow:
    return LedgerRow(
        chat_id="c1",
        actor="u1",
        display_name="Ali",
        messages_given=5,
        tokens_given=10,
        tokens_received=5,
        response_latency_s=12.0,
        closure_rate=closure,
        asymmetry=2.0,
        drain_score=drain,
    )


def test_green():
    s = classify(_row(drain=0.5, closure=0.7))
    assert s.level == "green"
    assert "balanced" in s.reason


def test_green_requires_closure():
    # drain low but closure below 0.6 -> yellow, not green
    assert classify(_row(drain=0.5, closure=0.5)).level == "yellow"


def test_boundary_drain_exactly_0_8():
    # drain == 0.8 is NOT < 0.8 -> cannot be green; falls to yellow (< 2.0)
    assert classify(_row(drain=0.8, closure=1.0)).level == "yellow"


def test_boundary_closure_exactly_0_6():
    # closure == 0.6 satisfies >= -> green when drain < 0.8
    assert classify(_row(drain=0.79, closure=0.6)).level == "green"


def test_boundary_drain_exactly_2_0():
    # drain == 2.0 is NOT < 2.0 -> red
    assert classify(_row(drain=2.0, closure=0.0)).level == "red"


def test_just_below_2_0_is_yellow():
    assert classify(_row(drain=1.999, closure=0.0)).level == "yellow"


def test_red_reason_mentions_hanging():
    s = classify(_row(drain=3.0, closure=0.25))
    assert s.level == "red"
    assert "75%" in s.reason


def test_custom_thresholds():
    th = Thresholds(green_drain=1.0, green_closure=0.5, yellow_drain=3.0)
    assert classify(_row(drain=0.9, closure=0.5), th).level == "green"
    assert classify(_row(drain=2.5, closure=0.0), th).level == "yellow"
    assert classify(_row(drain=3.0, closure=0.0), th).level == "red"
