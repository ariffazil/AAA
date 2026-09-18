#!/usr/bin/env python3
"""Probe which controls a running service ACTUALLY enforces.

Stdlib only. Talks to a service you started yourself on a loopback port with a
throwaway credential, so a finding never costs a production side effect.

Spec file (JSON):

    {
      "base": "http://127.0.0.1:8799",
      "token": "throwaway-token",
      "probes": [
        {"label": "liveness, no token",       "path": "/health",              "auth": false, "expect": "allow"},
        {"label": "guarded route, no token",  "path": "/v1/status/battery",   "auth": false, "expect": "deny"},
        {"label": "guarded route, token",     "path": "/v1/status/battery",   "auth": true,  "expect": "allow"},
        {"label": "deny-listed, token",       "path": "/sms/send",            "auth": true,  "expect": "deny"},
        {"label": "sensitive, token only",    "path": "/v1/camera/capture",   "auth": true,  "expect": "any"}
      ]
    }

Run:
    python3 contract_probe.py --spec probes.json
    python3 contract_probe.py --spec probes.json --source /path/server.py \
        --markers "_auth_ok,denied_by_policy,X-Signature,approval_id,nonce"

HOW TO READ THE OUTPUT

  expect=deny  -> PASS only on 401/403 (an explicit refusal).
  expect=allow -> PASS on anything that is NOT a refusal. This is deliberate:
                  a 500 from inside the handler means the request cleared every
                  policy gate and died later, which is evidence the gate is
                  ABSENT, not that it works.
  expect=any   -> informational: recorded, never judged.

A uniform failure across every probe means the probe is broken (bad port or bad
credential), not that the service is hardened. Fix the probe before concluding.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

REFUSAL_CODES = {401, 403}


def call(base: str, path: str, token: str | None, method: str, timeout: int):
    req = urllib.request.Request(base + path, method=method)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()[:160].decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:160].decode(errors="replace")
    except Exception as e:  # noqa: BLE001
        return "ERR", str(e)


def judge(expect: str, code) -> str:
    if expect == "any":
        return "INFO"
    refused = code in REFUSAL_CODES
    if expect == "deny":
        return "PASS" if refused else "FAIL"
    if expect == "allow":
        return "FAIL" if refused else "PASS"
    return "?"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="JSON probe spec")
    ap.add_argument("--source", help="source file to scan for declared checks")
    ap.add_argument("--markers", default="", help="comma-separated strings/calls to look for")
    ap.add_argument("--timeout", type=int, default=8)
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    base = spec["base"].rstrip("/")
    token = spec.get("token")

    print(f"CONTRACT PROBE  base={base}")
    print("=" * 78)
    print(f"{'probe':46} {'expect':8} {'code':>5}  verdict")
    print("-" * 78)

    codes = []
    failures = 0
    for p in spec["probes"]:
        sent = token if p.get("auth") else None
        code, body = call(base, p["path"], sent, p.get("method", "GET"), args.timeout)
        expect = p.get("expect", "any")
        verdict = judge(expect, code)
        codes.append(code)
        if verdict == "FAIL":
            failures += 1
        print(f"{p['label'][:46]:46} {expect:8} {str(code):>5}  {verdict}")
        if verdict == "FAIL":
            print(f"    -> {body[:120]}")
    print("=" * 78)

    if codes and len(set(map(str, codes))) == 1:
        print("WARNING: every probe returned the same result. That is usually a")
        print("         broken probe (wrong port or credential), not a hardened")
        print("         service. Fix the probe before drawing a conclusion.")

    if args.source:
        src = Path(args.source).read_text()
        print("\nDECLARED CHECKS PRESENT IN SOURCE")
        for marker in [m.strip() for m in args.markers.split(",") if m.strip()]:
            present = marker in src
            # A check that exists in code can still never be called. Grep proves
            # presence, never invocation — say so rather than implying ENFORCED.
            state = "present" if present else "ABSENT "
            print(f"  {state}  {marker}")
        print("  note: presence in source != called on the request path.")
        print("        confirm invocation before reporting a control as active.")

    print(f"\n{failures} probe(s) contradicted their declared expectation.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
