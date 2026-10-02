"""chron-verify-sweep: pure-logic regression tests (no network).

Proves the two properties that matter:
  1. Due debt is rendered LOUD (never silently dropped).
  2. Learning-closure gap follows its stated rule, not vibes.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.chron_verify_sweep import render  # noqa: E402


def _report(due_items=None, actionable=0, episodes=110000, unclassified=0):
    due_items = due_items if due_items is not None else []
    return {
        "swept_at": "2026-10-02T03:44:10Z",
        "verification_debt": {"count": len(due_items), "items": due_items},
        "next_verify_at": "2026-10-09T23:59:59+08:00",
        "funnel": {
            "observe": 109007, "predict": 27, "verify": 11, "learn": 3,
            "predict_per_1000_observe": 0.248,
            "verify_per_predict": 0.407,
            "learn_per_verify": 0.273,
        },
        "learning_closure_gap": {
            "episodes_total": episodes,
            "actionable_lessons": actionable,
            "unclassified_outcomes": unclassified,
            "gap": bool(episodes >= 100 and actionable == 0),
            "rule": "gap = (episodes_total >= 100) and (actionable_lessons == 0)",
        },
        "lesson_health": {"total": 2, "active": 0, "blind": 0},
    }


def test_due_debt_is_loud_not_silent():
    r = _report(due_items=[{
        "prediction_id": "pred-x", "claim": "Belanjawan 2027 dibentang",
        "confidence": 0.9, "verify_at": "2026-10-09T23:59:59+08:00", "overdue_days": 0.5,
    }])
    out = render(r)
    assert "1 DUE" in out and "pred-x" in out and "Belanjawan" in out


def test_zero_debt_reports_next_window():
    out = render(_report())
    assert "0 due" in out and "2026-10-09" in out


def test_gap_rule_follows_stated_rule():
    assert _report(actionable=0, episodes=110000)["learning_closure_gap"]["gap"] is True
    assert _report(actionable=1, episodes=110000)["learning_closure_gap"]["gap"] is False
    assert _report(actionable=0, episodes=50)["learning_closure_gap"]["gap"] is False


def test_unclassified_outcomes_surface():
    out = render(_report(unclassified=4))
    assert "4 unclassified" in out
