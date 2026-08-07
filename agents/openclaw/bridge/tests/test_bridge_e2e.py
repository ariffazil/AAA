#!/usr/bin/env python3
"""
E2E test for OpenClaw A2A bridge + delivery adapter.

Verifies:
  1. Router dispatch → rule + organ correct (all 10 rules sample-tested)
  2. Envelope schema (A2A-Version 1.0 contract)
  3. Ed25519 signature present + verifiable
  4. HTTP POST to /tasks returns 200 (live gateway)
  5. Delivery adapter renders valid Telegram MD2 chunks

Run: python3 tests/test_bridge_e2e.py
"""

from __future__ import annotations

import base64
import json
import os
import sys
import time
from pathlib import Path

# Make sibling modules importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from a2a_bridge import (
    route, build_envelope, sign_envelope, dispatch,
    OPENCLAW_KEY_PATH, A2A_BASE,
)
from delivery_adapter import format_telegram, format_a2a, format_local, deliver

# ──────────────────────────── assertion helpers ────────────────────────────

PASS = "✅"
FAIL = "❌"
results: list[tuple[str, str, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    mark = PASS if ok else FAIL
    results.append((mark, name, detail))
    print(f"{mark} {name}" + (f"  — {detail}" if detail else ""))


# ──────────────────────────── 1. Router rule coverage ────────────────────────────

ROUTER_CASES = [
    ("Hold everything", "R01_HOLD_ESCALATE", "arifos"),
    ("Just research gold market trends", "R02_RESEARCH", "hermes-asi"),
    ("Fix the swap issue on af-forge", "R03_CODE_EXECUTE", "a-forge"),
    ("What's my gold position?", "R04_POSITION_QUICK", "local-cache"),
    ("What's the porosity in the Malay Basin?", "R05_EARTH_DOMAIN", "geox"),
    ("Calculate NPV for project Alpha", "R06_CAPITAL_DOMAIN", "wealth"),
    ("How am I doing today?", "R07_VITALITY_DOMAIN", "well"),
    ("How's the federation health?", "R08_SYSTEM_STATUS", "aaa"),
    ("Send me the weekly brief", "R09_DELIVER_ARTIFACT", "local-cache"),
    ("random unclear message", "R10_DEFAULT_TRIAGE", "hermes-asi"),
]

print("\n=== Router rule coverage ===")
for text, expected_rule, expected_organ in ROUTER_CASES:
    rr = route(text)
    ok = rr.rule_id == expected_rule and rr.organ == expected_organ
    check(
        f"route({text!r:50s}) → {rr.rule_id}",
        ok,
        f"organ={rr.organ} (expected {expected_organ})",
    )

# ──────────────────────────── 2. Envelope schema ────────────────────────────

print("\n=== Envelope schema ===")
rr = route("How's the federation health?")
env = build_envelope("How's the federation health?", rr)
check("envelope has jsonrpc=2.0", env["jsonrpc"] == "2.0")
check("envelope has method=message/send", env["method"] == "message/send")
check("envelope has session_id", "session_id" in env["params"])
check("envelope has actor_id", "actor_id" in env["params"])
check("envelope has message.parts", "parts" in env["params"]["message"])
check("envelope metadata has routing", "routing" in env["params"]["metadata"])
check(
    "routing.rule_id matches",
    env["params"]["metadata"]["routing"]["rule_id"] == "R08_SYSTEM_STATUS",
)

# ──────────────────────────── 3. Ed25519 signature ────────────────────────────

print("\n=== Ed25519 signature ===")
if OPENCLAW_KEY_PATH.exists():
    signed = sign_envelope(env)
    sig = signed.get("signature")
    check("signature present", sig is not None)
    if sig:
        check("signature algo=ed25519", sig["algo"] == "ed25519")
        check("signature value present", bool(sig["value"]))
        check("canonical_hash is sha256 hex", len(sig["canonical_hash"]) == 64)

        # Verify round-trip
        try:
            from cryptography.hazmat.primitives.serialization import load_pem_public_key
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
            pub_path = Path(str(OPENCLAW_KEY_PATH).replace("_private", "_public"))
            if pub_path.exists():
                pub = load_pem_public_key(pub_path.read_bytes())
                if isinstance(pub, Ed25519PublicKey):
                    canon = json.dumps(env, sort_keys=True, separators=(",", ":")).encode("utf-8")
                    sig_bytes = base64.urlsafe_b64decode(sig["value"] + "==")
                    try:
                        pub.verify(sig_bytes, canon)
                        check("signature VERIFIES against public key", True)
                    except Exception as e:
                        check("signature VERIFIES against public key", False, str(e))
                else:
                    check("signature VERIFIES against public key", False, "public key not Ed25519")
            else:
                check("signature VERIFIES against public key", False, f"public key missing: {pub_path}")
        except Exception as e:
            check("signature verification path", False, f"{type(e).__name__}: {e}")
else:
    check("signature present", False, f"key missing: {OPENCLAW_KEY_PATH}")

# ──────────────────────────── 4. Live HTTP dispatch ────────────────────────────

print(f"\n=== Live HTTP dispatch to {A2A_BASE}/tasks ===")
try:
    out = dispatch(
        "Send me the weekly brief",
        sign=True,
        send=True,
        timeout=15.0,
    )
    resp = out.get("a2a_response", {})
    check(
        "POST /tasks returns 200",
        resp.get("status") == 200,
        f"got status={resp.get('status')}",
    )
    if resp.get("body"):
        body_preview = json.dumps(resp["body"])[:200]
        check("response has body", True, body_preview)
    check("task_id present", resp.get("task_id") is not None)
    # Routing metadata should match
    check(
        "routing.rule_id in response",
        out["routing"]["rule_id"] == "R09_DELIVER_ARTIFACT",
    )
except Exception as e:
    check("POST /tasks returns 200", False, f"{type(e).__name__}: {e}")

# ──────────────────────────── 5. Delivery adapter ────────────────────────────

print("\n=== Delivery adapter ===")
sample_payload = {
    "result": {
        "id": "test-task-123",
        "metadata": {
            "routing": {
                "rule_id": "R08_SYSTEM_STATUS",
                "organ": "aaa",
                "intent_class": "query",
            }
        },
        "history": [
            {"role": "assistant", "parts": [{"kind": "text", "text": "All 8 organs healthy. FQ=1.11."}]}
        ],
        "artifacts": [{"text": "All 8 organs healthy. FQ=1.11."}],
    }
}

chunks = format_telegram(sample_payload)
check("telegram renders ≥1 chunk", len(chunks) >= 1)
check("telegram chunk ≤ 4096", all(len(c) <= 4096 for c in chunks))
check("telegram has footer", "DITEMPA BUKAN DIBERI" in chunks[0])
check("telegram has rule header", "R08_SYSTEM_STATUS" in chunks[0])

a2a_report = format_a2a(sample_payload)
check("a2a envelope has delivery.kind", a2a_report["delivery"]["kind"] == "a2a_json")

local_report = format_local(sample_payload, "test-session-001")
check("local file path set", "path" in local_report["delivery"])

# ──────────────────────────── summary ────────────────────────────

print("\n" + "=" * 60)
n_pass = sum(1 for m, _, _ in results if m == PASS)
n_fail = sum(1 for m, _, _ in results if m == FAIL)
print(f"PASS: {n_pass}  FAIL: {n_fail}")
if n_fail:
    print("\nFailures:")
    for m, n, d in results:
        if m == FAIL:
            print(f"  {FAIL} {n}: {d}")
    sys.exit(1)
sys.exit(0)
