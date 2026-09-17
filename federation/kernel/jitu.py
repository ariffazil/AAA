#!/usr/bin/env python3
"""jitu.py — THE single circuit breaker. One power button, one receipt, one authority.

F13 directive 2026-09-18: *"Kolaps 3 implementasi jadi SATU butang kuasa mutlak. Wayarkan terus ke
urat saraf enforcement semua lane automatik. Apabila JITU diaktifkan, ia mesti jadi hard interrupt
(henti serta-merta) dan tinggalkan receipt jelas."*

WHAT THIS REPLACES (all three earlier implementations, now tombstoned):
  /root/arifOS/core/paradox/circuit_breakers.py    epistemic CB1-CB5 only, no live caller
  /root/scripts/governance/circuit-breaker.sh      3-strikes task cap, no live caller
  /root/arifOS/scripts/wire/arif-circuit-breaker   RSI lock, no live caller

WHY A TRIP FILE AND NOT A KEYWORD
  "JITU is explicitly invoked" as a phrase can only be obeyed by something that reads phrases.
  An automated lane does not read phrases; it executes. So the brake is a FILE whose existence and
  content any lane can test BEFORE its first side effect. A word is a request. A file is a state.

THE CONTRACT
  trip.json carries the full authority tuple:
      { tripped_at, by, scope[], reason, until, trace_id }
  `check` is the enforcement call. Exit 0 = lane may run. Exit 3 = HARD INTERRUPT (do not run).
  `trip` and `release` accept ONLY a sovereign identity. Nothing automated may release its own
  brake — that is the one failure this mechanism exists to prevent.

USAGE
  jitu trip --by F13 --reason "runaway escalation in <lane>" [--scope lane1,lane2] [--until ISO8601]
  jitu release --by F13 [--reason "..."]
  jitu status [--json]
  jitu check [--lane NAME]        -> exit 0 allow / exit 3 tripped
  jitu selftest                   -> proves the brake actually stops something (a brake never tested
                                     is a brake nobody should trust)

CRON / SHELL WIRING
  <lane command>   becomes   jitu-guard <lane> && <lane command>
  `jitu-guard` is a one-line wrapper that calls `check` and exits non-zero when tripped, so a
  shell `&&` chain cannot proceed. That is the hard interrupt for non-Python lanes.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

JITU_DIR = Path(os.environ.get("JITU_DIR", "/root/.local/share/arifos/jitu"))
TRIP_PATH = JITU_DIR / "trip.json"
EVENTS_PATH = JITU_DIR / "jitu_events.jsonl"

SOVEREIGN = {"F13", "f13", "arif", "ARIF", "sovereign", "SOVEREIGN"}
EXIT_ALLOW = 0
EXIT_TRIPPED = 3


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mint_trace() -> str:
    return os.environ.get("ARIFOS_TRACE_ID") or f"trc-{uuid.uuid4().hex[:12]}"


def _record(event: str, **fields) -> dict:
    """Append-only event trail. A halt nobody can prove happened is not a halt."""
    row = {"event": event, "ts": _now(), **fields}
    try:
        JITU_DIR.mkdir(parents=True, exist_ok=True)
        with EVENTS_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, default=str) + "\n")
    except Exception:
        pass  # trail failure must never deadlock the brake itself
    return row


def read_state() -> dict | None:
    """The trip state, or None when the brake is idle. Unreadable state = TRIPPED.

    Fail-closed is the only safe default here: if the file is corrupt or unreadable we cannot
    prove the brake is released, so the lane must not run.
    """
    if not TRIP_PATH.exists():
        return None
    try:
        state = json.loads(TRIP_PATH.read_text(encoding="utf-8"))
        if not isinstance(state, dict):
            return {"corrupt": True, "by": "UNKNOWN", "scope": ["all"],
                    "reason": "trip file is not an object", "tripped_at": None, "until": None}
        return state
    except Exception as exc:
        return {"corrupt": True, "by": "UNKNOWN", "scope": ["all"],
                "reason": f"trip file unreadable: {exc}", "tripped_at": None, "until": None}


def _expired(state: dict) -> bool:
    until = state.get("until")
    if not until:
        return False
    try:
        end = datetime.fromisoformat(str(until).replace("Z", "+00:00"))
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) >= end
    except Exception:
        return False  # unparseable deadline = never expires; a deadline nobody can compute is not one


def in_scope(state: dict, lane: str | None) -> bool:
    scope = state.get("scope") or ["all"]
    if isinstance(scope, str):
        scope = [scope]
    if "all" in scope or "*" in scope:
        return True
    if lane is None:
        return True  # unlabelled caller: treat as in scope (fail-closed)
    return lane in scope


def check(lane: str | None = None, quiet: bool = False) -> tuple[bool, str]:
    """(allowed, human_reason). This is the enforcement call."""
    state = read_state()
    if state is None:
        return True, "brake idle"
    if _expired(state):
        return True, f"brake expired (until {state.get('until')})"
    if not in_scope(state, lane):
        return True, f"brake tripped but lane '{lane}' is out of scope {state.get('scope')}"
    reason = (
        f"JITU TRIPPED by {state.get('by')} at {state.get('tripped_at')} "
        f"scope={state.get('scope')} reason={state.get('reason')!r}"
    )
    if state.get("corrupt"):
        reason = f"JITU FAIL-CLOSED: {state.get('reason')} — brake state cannot be read as released"
    if not quiet:
        _record("check_denied", lane=lane, trace_id=_mint_trace(), detail=reason)
    return False, reason


def trip(by: str, reason: str, scope: list[str], until: str | None) -> int:
    if by not in SOVEREIGN:
        print(f"REFUSED: '{by}' is not a sovereign identity. Only F13 trips the brake. "
              f"An automated lane may never trip it either — escalate to F13.", file=sys.stderr)
        _record("trip_refused", by=by, reason=reason)
        return 4
    if not reason:
        print("REFUSED: a trip with no stated reason cannot be audited or released with confidence.",
              file=sys.stderr)
        return 4
    state = {
        "tripped_at": _now(),
        "by": by,
        "scope": scope or ["all"],
        "reason": reason,
        "until": until,
        "trace_id": _mint_trace(),
    }
    JITU_DIR.mkdir(parents=True, exist_ok=True)
    TRIP_PATH.write_text(json.dumps(state, indent=1), encoding="utf-8")
    _record("trip", **state)
    print(f"JITU TRIPPED  scope={state['scope']}  trace={state['trace_id']}")
    print(f"  reason: {reason}")
    if until:
        print(f"  auto-expires: {until}")
    return 0


def release(by: str, reason: str) -> int:
    if by not in SOVEREIGN:
        print(f"REFUSED: '{by}' is not a sovereign identity. Nothing automated releases the brake.",
              file=sys.stderr)
        _record("release_refused", by=by)
        return 4
    state = read_state()
    if state is None:
        print("brake already idle — nothing to release")
        return 0
    try:
        TRIP_PATH.unlink()
    except FileNotFoundError:
        pass
    _record("release", by=by, reason=reason, was=state)
    print(f"JITU RELEASED by {by}  (was tripped at {state.get('tripped_at')})")
    return 0


def status(as_json: bool) -> int:
    state = read_state()
    if as_json:
        print(json.dumps({"tripped": state is not None, "state": state}, indent=1))
        return EXIT_TRIPPED if state is not None else EXIT_ALLOW
    if state is None:
        print("JITU: idle (brake closed)")
        return EXIT_ALLOW
    print("JITU: TRIPPED")
    for k in ("tripped_at", "by", "scope", "reason", "until", "trace_id"):
        print(f"  {k:<11} {state.get(k)}")
    return EXIT_TRIPPED


def selftest() -> int:
    """Prove the brake stops something, then restore the prior state exactly.

    A brake that has never been tested is indistinguishable from decoration. This runs the whole
    cycle against a scratch directory so the live trip file is never touched.
    """
    global JITU_DIR, TRIP_PATH, EVENTS_PATH
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        saved = (JITU_DIR, TRIP_PATH, EVENTS_PATH)
        JITU_DIR = Path(tmp)
        TRIP_PATH = JITU_DIR / "trip.json"
        EVENTS_PATH = JITU_DIR / "jitu_events.jsonl"
        try:
            steps = []
            ok, why = check("lane-a", quiet=True)
            steps.append(("idle -> allowed", ok is True))
            trip("NOT-A-SOVEREIGN", "should be refused", ["all"], None)
            steps.append(("non-sovereign trip refused", read_state() is None))
            trip("F13", "selftest", ["all"], None)
            ok, _ = check("lane-a", quiet=True)
            steps.append(("tripped -> denied", ok is False))
            trip("F13", "selftest scoped", ["lane-b"], None)
            ok_a, _ = check("lane-a", quiet=True)
            ok_b, _ = check("lane-b", quiet=True)
            steps.append(("scoped trip spares out-of-scope lane", ok_a is True and ok_b is False))
            trip("F13", "expired", ["all"], "1970-01-01T00:00:00+00:00")
            ok, _ = check("lane-a", quiet=True)
            steps.append(("expired trip -> allowed", ok is True))
            trip("F13", "selftest", ["all"], None)
            release("NOT-A-SOVEREIGN", "nope")
            steps.append(("non-sovereign release refused", read_state() is not None))
            release("F13", "selftest done")
            steps.append(("sovereign release -> idle", read_state() is None))
            TRIP_PATH.write_text("{ this is not json", encoding="utf-8")
            ok, why = check("lane-a", quiet=True)
            steps.append(("corrupt state -> fail-closed denied", ok is False))
            failed = [name for name, passed in steps if not passed]
            for name, passed in steps:
                print(f"  {'PASS' if passed else 'FAIL'}  {name}")
            print(f"selftest: {len(steps) - len(failed)}/{len(steps)} passed")
            return 0 if not failed else 1
        finally:
            JITU_DIR, TRIP_PATH, EVENTS_PATH = saved


def main() -> int:
    ap = argparse.ArgumentParser(prog="jitu", description="the single circuit breaker")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_trip = sub.add_parser("trip", help="activate the brake")
    p_trip.add_argument("--by", required=True)
    p_trip.add_argument("--reason", required=True)
    p_trip.add_argument("--scope", default="all", help="comma list of lanes, or 'all'")
    p_trip.add_argument("--until", default=None, help="ISO8601 auto-expiry")

    p_rel = sub.add_parser("release", help="deactivate the brake (sovereign only)")
    p_rel.add_argument("--by", required=True)
    p_rel.add_argument("--reason", default="")

    p_st = sub.add_parser("status", help="report brake state")
    p_st.add_argument("--json", action="store_true")

    p_ck = sub.add_parser("check", help="enforcement call: exit 0 allow / exit 3 tripped")
    p_ck.add_argument("--lane", default=None)
    p_ck.add_argument("--quiet", action="store_true")

    sub.add_parser("selftest", help="prove the brake stops something")

    a = ap.parse_args()
    if a.cmd == "trip":
        scope = [s.strip() for s in a.scope.split(",") if s.strip()]
        return trip(a.by, a.reason, scope, a.until)
    if a.cmd == "release":
        return release(a.by, a.reason)
    if a.cmd == "status":
        return status(a.json)
    if a.cmd == "check":
        allowed, why = check(a.lane, quiet=a.quiet)
        if not allowed:
            print(f"HARD INTERRUPT — {why}", file=sys.stderr)
            print("  This lane must not run. Release requires F13: jitu release --by F13", file=sys.stderr)
            return EXIT_TRIPPED
        if not a.quiet:
            print(f"jitu: {why}")
        return EXIT_ALLOW
    if a.cmd == "selftest":
        return selftest()
    return 2


if __name__ == "__main__":
    sys.exit(main())
