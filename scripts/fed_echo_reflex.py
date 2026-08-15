#!/usr/bin/env python3
"""
FED echo reflex — constitutional seat attestation (SHADOW-GLM-004 guard).

Doctrine: ACTOR_SURFACE_DOCTRINE.md §The Exception — kerusi 888/666-999/i-arif
tidak sesekali dilayan zai coding plan. Litellm returns the *alias* in the
response body, but response headers carry the truth:
  x-litellm-model-api-base  → endpoint of the deployment that actually served
  x-litellm-model-group     → alias (requested seat)

This probe asks each constitutional seat one token, reads the header truth,
and appends a drift event when a banned provider serves the seat.

Drift events → /root/.local/share/arifos/fed_echo/drift_events.jsonl
Usage: fed_echo_reflex.py [--seat NAME]...   (default: all constitutional seats)
Exit: 0 clean · 2 drift detected · 3 probe failure
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

GATEWAYS = [
    "http://127.0.0.1:4000/v1/chat/completions",  # haproxy sovereign gateway
    "http://127.0.0.1:4011/v1/chat/completions",  # litellm direct
]

# seat → banned serving providers (substring match on x-litellm-model-api-base)
CONSTITUTIONAL_SEATS = {
    "apex-888": {"z.ai", "bigmodel"},   # 666_JUDGE — Gödel E3 diversity too
    "i-arif":   {"z.ai", "bigmodel"},   # 999-adjacent sovereign seat
}

EVENTS = Path("/root/.local/share/arifos/fed_echo/drift_events.jsonl")
KEY = os.environ.get("LITELLM_MASTER_KEY", "")


def probe(seat: str, banned: set) -> dict:
    body = json.dumps({
        "model": seat,
        "messages": [{"role": "user", "content": "Reply with exactly: ECHO"}],
        "max_tokens": 4096,
    }).encode()
    last_err = None
    for url in GATEWAYS:
        req = urllib.request.Request(url, data=body, headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
        }, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                api_base = resp.headers.get("x-litellm-model-api-base", "unknown")
                group = resp.headers.get("x-litellm-model-group", seat)
                served_by_banned = any(b in api_base for b in banned)
                return {
                    "seat": seat, "gateway": url.split(":")[1].lstrip("/"),
                    "requested": group, "served_api_base": api_base,
                    "drift": served_by_banned,
                }
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = str(e)
            continue
    return {"seat": seat, "error": last_err, "drift": None}


def main() -> int:
    seats = CONSTITUTIONAL_SEATS
    args = [a for a in sys.argv[1:] if a != "--seat"]
    if args:
        seats = {s: CONSTITUTIONAL_SEATS[s] for s in args if s in CONSTITUTIONAL_SEATS}

    if not KEY:
        print("FATAL: LITELLM_MASTER_KEY not in env (source kunci-mas.env)")
        return 3

    rc = 0
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    for seat, banned in seats.items():
        r = probe(seat, banned)
        ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        if r.get("error"):
            print(f"[{ts}] {seat}: PROBE-FAIL {r['error'][:90]}")
            rc = max(rc, 3)
            continue
        line = json.dumps({
            "schema": "arifos.echo.v1", "ts": ts, "seat": r["seat"],
            "requested_model": r["requested"], "served_api_base": r["served_api_base"],
            "drift": r["drift"], "guard": "SHADOW-GLM-004",
        }, ensure_ascii=False, separators=(",", ":"))
        print(f"[{ts}] {seat}: requested={r['requested']} served_by={r['served_api_base']} drift={r['drift']}")
        if r["drift"]:
            with open(EVENTS, "a") as f:
                f.write(line + "\n")
            rc = max(rc, 2)
    return rc


if __name__ == "__main__":
    sys.exit(main())
