"""TemporalAdapter — the ONE DOOR to CHRON's temporal capability (PR-3).

Contract (stable, AAA-owned):
    briefing() -> {
        available: bool,
        degradation: str | None,
        source: str,
        observed_at: str,
        adapter_version: str,

        prediction_due: [...],            # due prediction objects (list)
        prediction_due_count: int,
        next_verify_at: str | None,       # next calibration deadline
        attention_debt: float | None,     # owed attention (CHRON total_ad)

        verification_backlog: int | None, # due-unverified predictions
        unclassified_outcomes: int | None,# verified outcomes with UNKNOWN error class
        actionable_lessons: int | None,   # lessons flagged actionable
        lessons_returned: int | None,     # window size actually read (auditability)

        calibration_health: {"mean_brier": float, "accuracy": float} | None,
        learning_closure_gap: {           # auditable formula + inputs
            "gap": bool | None,           # None = unmeasurable, never guessed
            "episodes_total": int | None,
            "actionable_lessons": int | None,
            "lessons_window": int,
            "rule": str,
        } | None,
        last_loop: {...} | None,
    }

Canonical sources (live probe 2026-10-02, CHRON :18102 MCP):
    chron_temporal_briefing — predictions_due, calibration, attention_debt, last_loop
    chron_predictions_due   — due list + next_verify_at
    chron_store_stats       — episode totals + resolution states (DUE = backlog)
    chron_lessons           — actionable lesson count (within lessons_window)
    GET /health             — acceptable fallback (attention_debt, calibration);
                              it cannot see lessons ⇒ learning_closure_gap.gap
                              stays None under fallback (no data ≠ all clear)

F1 AMANAH — fail closed: CHRON unreachable ⇒ available=False, numeric
fields None (never 0-as-all-clear), degradation names the reason.
"""

from __future__ import annotations

import datetime as _dt
import os
from typing import Any

from ._mcp_http import McpHttpSession, McpTransportError, http_json

ADAPTER_VERSION = "1.0.0"
DEFAULT_CHRON_URL = "http://127.0.0.1:18102"

# learning_closure_gap parameters — explicit so the formula is auditable
LESSONS_WINDOW = 100        # how many recent lessons we read
GAP_EPISODE_FLOOR = 100     # "many episodes" threshold
_GAP_RULE = (
    f"gap = (episodes_total >= {GAP_EPISODE_FLOOR}) and "
    f"(actionable_lessons == 0 within lessons_window={LESSONS_WINDOW})"
)


def _utcnow_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def _empty_briefing() -> dict[str, Any]:
    return {
        "available": False,
        "degradation": None,
        "source": "unavailable",
        "observed_at": _utcnow_iso(),
        "adapter_version": ADAPTER_VERSION,
        "prediction_due": [],
        "prediction_due_count": 0,
        "next_verify_at": None,
        "attention_debt": None,
        "verification_backlog": None,
        "unclassified_outcomes": None,
        "actionable_lessons": None,
        "lessons_returned": None,
        "calibration_health": None,
        "learning_closure_gap": None,
        "last_loop": None,
    }


class TemporalAdapter:
    """Stable briefing() contract over CHRON MCP. Read-only."""

    def __init__(self, base_url: str | None = None, timeout: float = 5.0):
        self.base_url = (
            base_url or os.getenv("CHRON_MCP_URL") or DEFAULT_CHRON_URL
        ).rstrip("/")
        self.timeout = timeout

    def briefing(self) -> dict[str, Any]:
        out = _empty_briefing()
        try:
            with McpHttpSession(self.base_url, timeout=self.timeout) as session:
                summary = session.call_tool("chron_temporal_briefing", {})
                due = session.call_tool("chron_predictions_due", {})
                stats = session.call_tool("chron_store_stats", {})
                lessons = session.call_tool(
                    "chron_lessons", {"limit": LESSONS_WINDOW, "status": "all"}
                )
        except McpTransportError:
            return self._health_fallback(out)
        return self._assemble(out, summary, due, stats, lessons, source="chron-mcp")

    # ── assembly ────────────────────────────────────────────────────

    def _assemble(
        self,
        out: dict[str, Any],
        summary: dict[str, Any],
        due: dict[str, Any],
        stats: dict[str, Any],
        lessons: dict[str, Any],
        source: str,
    ) -> dict[str, Any]:
        out["available"] = True
        out["source"] = source
        out["degradation"] = None

        due_list = summary.get("predictions_due") or due.get("due") or []
        out["prediction_due"] = due_list
        out["prediction_due_count"] = len(due_list) or int(due.get("count") or 0)
        out["next_verify_at"] = due.get("next_verify_at")

        debt = summary.get("attention_debt")
        if isinstance(debt, dict):
            out["attention_debt"] = float(debt.get("total_ad", 0) or 0)
        elif debt is not None:
            out["attention_debt"] = float(debt)

        calibration = summary.get("calibration") or {}
        if calibration:
            out["calibration_health"] = {
                "mean_brier": calibration.get("mean_brier"),
                "accuracy": calibration.get("accuracy"),
            }
            by_error = calibration.get("by_error_type") or {}
            out["unclassified_outcomes"] = int(by_error.get("UNKNOWN", 0) or 0)
            if not out["unclassified_outcomes"] and calibration.get("raw"):
                raw = calibration.get("raw") or {}
                out["unclassified_outcomes"] = int((raw.get("by_error_type") or {}).get("UNKNOWN", 0) or 0)

        predictions = stats.get("predictions") or {}
        resolution = predictions.get("resolution_states") or {}
        if predictions:
            backlog = predictions.get("due_now")
            if backlog is None:
                backlog = len(resolution.get("DUE") or [])
            out["verification_backlog"] = int(backlog or 0)

        episode_stats = stats.get("episodes") or {}
        episodes_total = episode_stats.get("total")

        lesson_rows = lessons.get("lessons") or []
        actionable = sum(1 for row in lesson_rows if row.get("actionable") is True)
        out["lessons_returned"] = len(lesson_rows)
        out["actionable_lessons"] = actionable

        gap: dict[str, Any] = {
            "gap": None,
            "episodes_total": episodes_total,
            "actionable_lessons": actionable,
            "lessons_window": LESSONS_WINDOW,
            "rule": _GAP_RULE,
        }
        if episodes_total is not None:
            gap["gap"] = bool(
                int(episodes_total) >= GAP_EPISODE_FLOOR and actionable == 0
            )
        out["learning_closure_gap"] = gap

        out["last_loop"] = summary.get("last_loop")
        return out

    def _health_fallback(self, out: dict[str, Any]) -> dict[str, Any]:
        """GET /health — acceptable fallback; it cannot see lessons."""
        try:
            status, _hdrs, body = http_json(
                f"{self.base_url}/health", timeout=self.timeout
            )
        except McpTransportError:
            out["degradation"] = "CHRON_UNREACHABLE"
            return out
        if status != 200:
            out["degradation"] = f"CHRON_UNREACHABLE:http_{status}"
            return out
        try:
            import json as _json

            health = _json.loads(body)
        except _json.JSONDecodeError:
            out["degradation"] = "CHRON_HEALTH_MALFORMED"
            return out

        out["available"] = True
        out["source"] = "chron:/health-fallback"
        out["degradation"] = "MCP_UNAVAILABLE_HEALTH_FALLBACK"
        debt = health.get("attention_debt") or {}
        if isinstance(debt, dict):
            out["attention_debt"] = float(debt.get("total_ad", 0) or 0)
        calibration = health.get("calibration") or {}
        if calibration:
            out["calibration_health"] = {
                "mean_brier": calibration.get("mean_brier"),
                "accuracy": calibration.get("accuracy"),
            }
        predictions = health.get("predictions") or {}
        out["prediction_due_count"] = int(predictions.get("due_now", 0) or 0)
        out["verification_backlog"] = out["prediction_due_count"]
        out["learning_closure_gap"] = {
            "gap": None,  # /health cannot see lessons — unmeasured, never guessed
            "episodes_total": health.get("episodes"),
            "actionable_lessons": None,
            "lessons_window": LESSONS_WINDOW,
            "rule": _GAP_RULE + " [UNMEASURED: lessons source unavailable via /health]",
        }
        return out
