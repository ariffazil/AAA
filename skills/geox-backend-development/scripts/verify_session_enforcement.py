#!/usr/bin/env python3
"""Verify session enforcement, tool tiers, and rate limiter after changes.

Run from GEOX root:
  PYTHONPATH=src .venv/bin/python3 scripts/verify_session_enforcement.py
"""
from __future__ import annotations
import sys

def main() -> int:
    errors: list[str] = []
    passed = 0

    def check(label: str, condition: bool, detail: str = ""):
        nonlocal passed
        if condition:
            passed += 1
            print(f"  OK {label}")
        else:
            errors.append(f"  FAIL {label}{f' -- {detail}' if detail else ''}")
            print(f"  FAIL {label}{f' -- {detail}' if detail else ''}")

    # Imports
    print("\n-- Imports --")
    try:
        from geox_mcp.session_enforcement import (
            validate_session, enforce_session_or_400, _error_code_to_http_status,
        )
        check("session_enforcement imports", True)
    except ImportError as e:
        check("session_enforcement imports", False, str(e))
        print("\n".join(errors))
        return 1

    try:
        from geox_mcp.tool_tiers import get_tool_tier
        check("tool_tiers imports", True)
    except ImportError as e:
        check("tool_tiers imports", False, str(e))

    try:
        from geox_mcp.rate_limiter import RateLimiter
        check("rate_limiter imports", True)
    except ImportError as e:
        check("rate_limiter imports", False, str(e))

    # Auto-mint
    print("\n-- Auto-mint --")
    r = validate_session(None, "test")
    check("None auto-mints", r.ok and r.session and r.session.get("auto_minted"))
    check("None gets ANON- prefix", r.ok and r.session["session_id"].startswith("ANON-"))
    check("None gets OBSERVE_ONLY", r.ok and r.authority == "OBSERVE_ONLY")

    r = validate_session("", "test")
    check("Empty auto-mints", r.ok and r.session and r.session.get("auto_minted"))

    r = validate_session("  ", "test")
    check("Whitespace auto-mints", r.ok and r.session and r.session.get("auto_minted"))

    r = validate_session("__auto_mint__", "test")
    check("__auto_mint__ gets ANON-", r.ok and r.session["session_id"].startswith("ANON-"))

    r = validate_session("ANON-passthrough", "test")
    check("ANON-xxx passthrough", r.ok and r.session["session_id"] == "ANON-passthrough")

    # Tool tiers
    print("\n-- Tool tiers --")
    for t in ["geox_temporal", "geox_source", "geox_map"]:
        check(f"{t} is anon", get_tool_tier(t) == "anon")
    for t in ["geox_workspace", "geox_well"]:
        check(f"{t} is session", get_tool_tier(t) == "session")
    for t in ["geox_well_ingest", "geox_claim"]:
        check(f"{t} is verified", get_tool_tier(t) == "verified")
    check("unknown defaults anon", get_tool_tier("no_such_tool") == "anon")

    # Rate limiter
    print("\n-- Rate limiter --")
    rl = RateLimiter()
    for i in range(30):
        assert rl.check("rl-anon", "anon")
    check("anon 30 allowed", True)
    check("anon 31st blocked", not rl.check("rl-anon", "anon"))
    check("anon other session OK", rl.check("rl-other", "anon"))

    for i in range(100):
        assert rl.check("rl-sess", "session")
    check("session 100 allowed", True)
    check("session 101st blocked", not rl.check("rl-sess", "session"))

    # HTTP status mapping
    print("\n-- HTTP status mapping --")
    check("SESSION_MISSING 400", _error_code_to_http_status("SESSION_MISSING") == 400)
    check("ACTOR_MISSING 400", _error_code_to_http_status("ACTOR_MISSING") == 400)
    check("RATE_LIMITED 429", _error_code_to_http_status("RATE_LIMITED") == 429)
    check("SESSION_INVALID 401", _error_code_to_http_status("SESSION_INVALID") == 401)
    check("SCT_INVALID 401", _error_code_to_http_status("SCT_INVALID") == 401)
    check("ACTOR_MISMATCH 401", _error_code_to_http_status("ACTOR_MISMATCH") == 401)
    check("TRANSPORT_DEGRADED 401", _error_code_to_http_status("TRANSPORT_DEGRADED") == 401)
    check("INSUFFICIENT_AUTHORITY 403", _error_code_to_http_status("INSUFFICIENT_AUTHORITY") == 403)

    # enforce_session_or_400
    print("\n-- enforce_session_or_400 --")
    r = enforce_session_or_400(None, "test")
    check("None session returns None", r is None)
    r = enforce_session_or_400("", "test")
    check("Empty session returns None", r is None)
    r = enforce_session_or_400("SEAL-abcd1234efgh5678", None)
    check("None actor returns error", r is not None and "ACTOR_MISSING" in str(r.get("error")))

    # Summary
    print(f"\n{'='*50}")
    total = passed + len(errors)
    if errors:
        print(f"FAILED: {len(errors)}/{total}")
        for e in errors:
            print(e)
        return 1
    else:
        print(f"PASSED: {passed}/{total}")
        return 0

if __name__ == "__main__":
    sys.exit(main())
