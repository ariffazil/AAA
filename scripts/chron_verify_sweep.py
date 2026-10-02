#!/usr/bin/env python3
"""CHRON verify-sweep — raise VERIFY throughput by making verification debt loud.

AAA FEDERATION CONVERGENCE v1 (2026-10-02). The measured bottleneck:

    OBSERVE (110k) >> PREDICT (29) > VERIFY (13) >> LEARN (3)

CHRON stores reality; predictions come due; if nobody classifies them at the
verify window, they rot into blind `insufficient-*` lessons (4 today). This
sweep runs daily and answers exactly one question loudly:

    WHAT DOES THE FEDERATION OWE REALITY RIGHT NOW?

It READS via the shared adapter transport (adapters/_mcp_http.py, read-only
law) and WRITES nothing to CHRON. Classification of a due prediction is a
warga act (chron_record_verification / chron_resolve_unverifiable) — this
script never invents an outcome (F2 TRUTH; PortAlive != ToolCallable !=
Verified).

Outputs (compressed, anti-bangang):
  - verification debt: every due prediction + its claim + age
  - funnel health: observe/predict/verify/learn ratios
  - learning closure gap: lots of experience + zero actionable lessons
  - state snapshot: state/chron/sweep-latest.json (for tooling)

Exit codes: 0 sweep ran · 2 CHRON unreachable (typed, never silent).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from adapters._mcp_http import McpHttpSession, McpTransportError  # noqa: E402

CHRON_URL = "http://127.0.0.1:18102"  # McpHttpSession appends /mcp itself
OUT_STATE = REPO / "state" / "chron" / "sweep-latest.json"
ADAPTER_VERSION = "1.0.0"


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _result_json(resp: dict) -> dict:
    """Unwrap an MCP tools/call response whose content[0].text is JSON."""
    content = (resp.get("result") or {}).get("content") or []
    text = content[0].get("text", "") if content else ""
    try:
        return json.loads(text)
    except Exception:
        return {}


def collect() -> dict:
    with McpHttpSession(CHRON_URL, timeout=8.0) as s:
        due = s.call_tool("chron_predictions_due", {}) or {}
        loop = s.call_tool("chron_last_loop", {}) or {}
        lessons = s.call_tool("chron_lessons", {"limit": 50}) or {}

    now = dt.datetime.now(dt.timezone.utc)
    due_items = []
    for p in due.get("due", []) or []:
        verify_at = p.get("verify_at") or p.get("due_at") or ""
        age_days = None
        if verify_at:
            try:
                va = dt.datetime.fromisoformat(verify_at.replace("Z", "+00:00"))
                age_days = round((now - va).total_seconds() / 86400, 2)
            except Exception:
                pass
        due_items.append({
            "prediction_id": p.get("prediction_id") or p.get("id"),
            "claim": (p.get("claim") or "")[:160],
            "confidence": p.get("confidence"),
            "verify_at": verify_at,
            "overdue_days": age_days,
        })

    loop_data = (loop.get("last_loop") or {}).get("data") or {}
    state = loop_data.get("state") or {}
    by_fn = state.get("episodes_by_function") or {}
    lesson_health = state.get("lesson_health") or {}
    lessons_list = lessons.get("lessons") or []
    actionable = [l for l in lessons_list if l.get("status") == "active" or l.get("actionable")]

    observe_n = by_fn.get("observe", 0)
    predict_n = by_fn.get("predict", 0)
    verify_n = by_fn.get("verify", 0)
    learn_n = by_fn.get("learn", 0)

    gap = {
        "episodes_total": state.get("episodes_total", 0),
        "actionable_lessons": len(actionable),
        "unclassified_outcomes": lesson_health.get("unclassified_outcomes", 0),
        "gap": bool(state.get("episodes_total", 0) >= 100 and len(actionable) == 0),
        "rule": "gap = (episodes_total >= 100) and (actionable_lessons == 0)",
    }
    funnel = {
        "observe": observe_n, "predict": predict_n, "verify": verify_n, "learn": learn_n,
        "predict_per_1000_observe": round(predict_n / max(1, observe_n) * 1000, 3),
        "verify_per_predict": round(verify_n / max(1, predict_n), 3),
        "learn_per_verify": round(learn_n / max(1, verify_n), 3),
    }
    return {
        "swept_at": _now(),
        "adapter_version": ADAPTER_VERSION,
        "verification_debt": {"count": len(due_items), "items": due_items},
        "next_verify_at": due.get("next_verify_at"),
        "funnel": funnel,
        "learning_closure_gap": gap,
        "lesson_health": {
            "total": lesson_health.get("lesson_total", 0),
            "active": lesson_health.get("lesson_active", 0),
            "blind": lesson_health.get("lesson_blind", 0),
        },
    }


def render(r: dict) -> str:
    lines = [f"CHRON VERIFY SWEEP {r['swept_at']}"]
    debt = r["verification_debt"]
    if debt["count"] == 0:
        lines.append(f"  verification debt: 0 due (next verify window: {r.get('next_verify_at')})")
    else:
        lines.append(f"  verification debt: {debt['count']} DUE — classify now")
        for it in debt["items"]:
            age = f", {it['overdue_days']}d overdue" if it.get("overdue_days") is not None else ""
            lines.append(f"    - {it['prediction_id']}: {it['claim']}{age}")
    f = r["funnel"]
    lines.append(
        f"  funnel: observe {f['observe']} > predict {f['predict']} > verify {f['verify']} > learn {f['learn']}"
        f"  (verify/predict {f['verify_per_predict']}, learn/verify {f['learn_per_verify']})"
    )
    g = r["learning_closure_gap"]
    flag = "GAP OPEN" if g["gap"] else "closed"
    lines.append(
        f"  learning closure: {flag} — {g['episodes_total']} episodes, {g['actionable_lessons']} actionable,"
        f" {g['unclassified_outcomes']} unclassified outcomes"
    )
    lh = r["lesson_health"]
    lines.append(f"  lessons: {lh['total']} total / {lh['active']} active / {lh['blind']} blind")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="also print full JSON")
    args = ap.parse_args()
    try:
        report = collect()
    except McpTransportError as exc:
        print(f"chron-verify-sweep: CHRON unreachable ({exc}) — typed failure, not silent", file=sys.stderr)
        return 2

    OUT_STATE.parent.mkdir(parents=True, exist_ok=True)
    OUT_STATE.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(render(report))
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
