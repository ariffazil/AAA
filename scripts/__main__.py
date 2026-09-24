#!/usr/bin/env python3
"""CHRON — Temporal Consequence Tracker.

The organ that answers:
  - What did we think?
  - What happened?
  - Were we wrong?
  - What changed because of it?

Usage:
  python3 -m chron status          # Store stats
  python3 -m chron episodes        # List recent episodes
  python3 -m chron predictions     # List predictions
  python3 -m chron verify          # Run verification on due predictions
  python3 -m chron learn           # Extract lessons from verified predictions
  python3 -m chron generate        # Generate predictions from chron_events
  python3 -m chron calibration     # Show calibration stats
  python3 -m chron tools           # List MCP tools
  python3 -m chron call <tool>     # Call an MCP tool

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add chron to path
sys.path.insert(0, str(Path(__file__).resolve().parent))


def cmd_status():
    from chron_mcp import chron_store_stats

    stats = chron_store_stats()
    print(json.dumps(stats, indent=2, default=str))


def cmd_episodes(args):
    from chron_mcp import chron_episodes

    function = args[0] if args else None
    result = chron_episodes(function=function, limit=10)
    print(f"Episodes: {result['total']} total")
    for ep in result["episodes"]:
        print(f"  [{ep.get('episode_id', '?')[:30]}] fn={ep.get('function', '?')} vt={ep.get('valid_time', '?')[:16]}")
    print(f"By function: {result['functions']}")


def cmd_predictions(args):
    from chron_mcp import chron_predictions

    status = args[0] if args else "all"
    result = chron_predictions(status=status)
    print(f"Predictions ({result['status_filter']}): {result['count']}")
    for p in result["predictions"]:
        print(f"  [{p.get('prediction_id', '?')[:12]}] {p.get('claim', '?')[:50]}")
        print(
            f"    status={p.get('status', '?')} "
            f"verify_at={p.get('verify_at', '?')[:16]} "
            f"confidence={p.get('confidence', '?')}"
        )


def cmd_verify(args):
    from chron_verify import run_verification

    dry_run = "--dry-run" in args
    result = run_verification(dry_run=dry_run)
    print(f"CHRON Verify — {result['timestamp']}")
    print(f"  Due: {result['due']}")
    if result["due"] > 0:
        print(f"  Correct: {result.get('verified_correct', 0)}")
        print(f"  Incorrect: {result.get('verified_incorrect', 0)}")
        print(f"  Unverifiable: {result.get('unverifiable', 0)}")
        for r in result.get("results", []):
            print(f"    [{r['prediction_id'][:12]}] {r['claim'][:50]}")
            print(f"      observed: {str(r['observed'])[:50]}")
            print(f"      error: {r['error']}  class: {r['error_class']}")


def cmd_learn(args):
    from chron_learn import extract_lessons, get_candidates

    if "candidates" in args:
        candidates = get_candidates()
        print(f"Lesson candidates: {len(candidates)}")
        for c in candidates:
            print(f"  [{c['lesson_id']}] {c['lesson'][:60]}")
    else:
        lessons = extract_lessons()
        print(f"CHRON Learn — {len(lessons)} lessons extracted")
        for l in lessons:
            print(f"  [{l['lesson_id']}] {l['lesson'][:60]}")
            print(f"    recurrence: {l['recurrence']}  eligible: {l['promotion_eligible']}")


def cmd_generate(args):
    from chron_prediction import generate_from_chron_events

    preds = generate_from_chron_events()
    print(f"Generated {len(preds)} new predictions")
    for p in preds:
        print(f"  [{p['prediction_id'][:12]}] {p['claim'][:50]}")
        print(f"    verify_at: {p['verify_at'][:16]}  confidence: {p['confidence']}")


def cmd_calibration(args):
    """Honest-scope calibration (audit 2026-09-25 #3): effective sample,
    synthetic tests separated, scope labels, updated_at — read from the
    canonical calibration.json (stamped by the 07:00/07:15 writers)."""
    import json
    from pathlib import Path

    p = Path("/root/chron/data/calibration.json")
    try:
        cal = json.loads(p.read_text())
    except FileNotFoundError:
        print("CHRON data not available: /root/chron/data/calibration.json not found.")
        print("Run the 07:00/07:15 calibration writers first, or check CHRON installation.")
        return
    except json.JSONDecodeError as e:
        print(f"CHRON calibration.json malformed: {e}")
        return
    scopes = cal.get("honest_scopes") or {}
    print("CHRON Calibration (skop jujur):")
    for key, label in (
        ("canonical_unified_excluding_self_tests", "NYATA (tanpa ujian sintetik)"),
        ("canonical_unified_including_self_tests", "GABUNGAN (termasuk sintetik)"),
    ):
        s = scopes.get(key) or {}
        if not s:
            continue
        acc = s.get("accuracy")
        acc_txt = f"{acc:.4f}" if isinstance(acc, (int, float)) else str(acc)
        brier = s.get("mean_brier")
        brier_txt = f"{brier:.4f}" if isinstance(brier, (int, float)) else str(brier)
        print(f"  [{label}] n={s.get('n')}  betul={s.get('correct')}  ketepatan={acc_txt}  Brier={brier_txt}")
    print(f"  sampel efektif: {cal.get('effective_n')}  ujian sintetik: {cal.get('synthetic_self_tests')}")
    print(f"  dikemas kini: {cal.get('updated_at')}")
    print(f"  by error type: {cal.get('by_error_type')}")


def cmd_tools(args):
    from chron_mcp import list_tools

    tools = list_tools()
    print(f"CHRON MCP Tools: {len(tools)}")
    for t in tools:
        print(f"  {t['name']}: {t['description']}")


def cmd_call(args):
    from chron_mcp import call_tool

    if not args:
        print("Usage: python3 -m chron call <tool_name> [kwargs_json]")
        return
    tool_name = args[0]
    kwargs = json.loads(args[1]) if len(args) > 1 else {}
    result = call_tool(tool_name, **kwargs)
    print(json.dumps(result, indent=2, default=str))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 0

    cmd = args[0]
    rest = args[1:]

    commands = {
        "status": cmd_status,
        "episodes": lambda: cmd_episodes(rest),
        "predictions": lambda: cmd_predictions(rest),
        "verify": lambda: cmd_verify(rest),
        "learn": lambda: cmd_learn(rest),
        "generate": lambda: cmd_generate(rest),
        "calibration": lambda: cmd_calibration(rest),
        "tools": lambda: cmd_tools(rest),
        "call": lambda: cmd_call(rest),
    }

    if cmd in commands:
        commands[cmd]()
        return 0
    else:
        print(f"Unknown command: {cmd}")
        print(f"Available: {', '.join(commands.keys())}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
