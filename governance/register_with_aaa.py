#!/usr/bin/env python3
"""
Federation Organ Registration — Mandatory Boot Gate

Sends organ identity to AAA's /federation/register endpoint.
Blocks startup until AAA confirms registration or timeout expires.

Usage: python3 register_with_aaa.py --organ-id arifos --port 8088
Exit 0 = registered (or AAA unreachable after timeout — start anyway with warning)
Exit 1 = registration rejected by AAA (organ identity invalid)

DITEMPA BUKAN DIBERI — 2026-07-14
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error

AAA_REGISTER_URL = "http://localhost:3001/federation/register"
MAX_RETRIES = 6
RETRY_DELAY_SEC = 5  # Total timeout: 30 seconds


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
        with urllib.request.urlopen(req, timeout=10) as resp:
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
