#!/usr/bin/env python3
"""
register_with_aaa.py — MANUAL DIAGNOSTIC ONLY (deprecated for boot)

Historical role: this script used to be called by organ boot scripts as a
mandatory boot gate.  As of the 2026-07-22 PRL/recovery refactor it is
NO LONGER wired into systemd.  Production auto-registration is performed
by ``AAA/a2a-server/auto-register-organs.js`` on the AAA side, with
bounded readiness probes (timeout + retry + backoff).

This script remains as a manual diagnostic for ops:

    python3 register_with_aaa.py --organ-id arifos --port 8088

It will print what AAA thinks of the organ's identity and exit non-zero
on rejection.  Do NOT add it back to ExecStartPre without explicit
approval — the auto-registration path is the canonical mechanism.

Exit codes (preserved from original):
  0 = registered (or AAA unreachable after timeout — start anyway with warning)
  1 = registration rejected by AAA (organ identity invalid)

DITEMPA BUKAN DIBERI — 2026-07-22 (manual-diagnostic reclassification)
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error

# Manual diagnostic endpoint — production auto-registration is on the AAA side.
AAA_REGISTER_URL = "http://localhost:3001/federation/register"
MAX_RETRIES = 3            # Bounded — don't block manual ops for >18s
RETRY_DELAY_SEC = 3        # Bounded retry delay
CONNECT_TIMEOUT_SEC = 3    # Bounded — AAA is localhost, not internet


def register(organ_id: str, port: int, name: str, skills: list[str]) -> bool:
    """Attempt registration with AAA. Returns True if successful."""
    health_url = f"http://localhost:{port}/health"
    payload = {
        "identity": {
            "organId": organ_id,
            "name": name,
        },
        "endpoints": {
            "healthUrl": health_url,
        },
        "skills": skills,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        AAA_REGISTER_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=CONNECT_TIMEOUT_SEC) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            stage = body.get("handshake", {}).get("stage", "UNKNOWN")
            if stage in ("REGISTERED", "COMPLETE"):
                print(f"[register] {organ_id}: REGISTERED with AAA (stage={stage}, stages: {body['handshake'].get('stages', [])})")
                return True
            else:
                print(f"[register] {organ_id}: AAA returned stage={stage}, expected REGISTERED/COMPLETE", file=sys.stderr)
                return False
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(f"[register] {organ_id}: AAA rejected ({e.code}): {body}", file=sys.stderr)
        return False
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        print(f"[register] {organ_id}: AAA unreachable: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Register organ with AAA federation registry")
    parser.add_argument("--organ-id", required=True, help="Organ identifier (e.g. arifos, geox)")
    parser.add_argument("--port", required=True, type=int, help="Organ's HTTP port")
    parser.add_argument("--name", required=True, help="Human-readable organ name")
    parser.add_argument("--skills", nargs="*", default=[], help="Organ skills/capabilities")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if registration fails (blocks boot)")
    args = parser.parse_args()

    for attempt in range(1, MAX_RETRIES + 1):
        if register(args.organ_id, args.port, args.name, args.skills):
            sys.exit(0)

        if attempt < MAX_RETRIES:
            print(f"[register] {args.organ_id}: retry {attempt}/{MAX_RETRIES} in {RETRY_DELAY_SEC}s...")
            time.sleep(RETRY_DELAY_SEC)

    # All retries exhausted
    if args.strict:
        print(f"[register] {args.organ_id}: FAILED after {MAX_RETRIES} retries. STRICT mode: blocking boot.", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"[register] {args.organ_id}: FAILED after {MAX_RETRIES} retries. Starting anyway (non-strict).", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
