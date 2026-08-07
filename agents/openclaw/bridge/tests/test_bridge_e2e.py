#!/usr/bin/env python3
"""
E2E test for OpenClaw A2A bridge + delivery adapter.

Verifies:
  1. All 10 router rules resolve correctly
  2. JSON-RPC 2.0 envelope shape (A2A-Version 1.0 contract)
  3. Live HTTP POST to /a2a returns success (real gateway)
  4. Delivery adapter renders valid Telegram MD2 chunks with footer
  5. A2A delivery envelope + local file persistence

Run: python3 tests/test_bridge_e2e.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import a2a_bridge
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

print("\n=== Router rule coverage (ROUTER_TO_AGENT mapping) ===")
EXPECTED = {
    "R01_HOLD_ESCALATE":     "arifos",
    "R02_RESEARCH":          "hermes-asi",
    "R03_CODE_EXECUTE":      "333-AGI",
    "R04_POSITION_QUICK":    "wealth",
    "R05_EARTH_DOMAIN":      "geox",
    "R06_CAPITAL_DOMAIN":    "wealth",
    "R07_VITALITY_DOMAIN":   "well",
    "R08_SYSTEM_STATUS":     "hermes-asi",
    "R09_DELIVER_ARTIFACT":  "hermes-asi",
    "R10_DEFAULT_TRIAGE":    "hermes-asi",
}
for rule_id, expected_agent in EXPECTED.items():
    target = a2a_bridge.resolve_target(rule_id, query="probe")
    if rule_id in a2a_bridge.LOCAL_RULES:
        check(f"resolve_target({rule_id}) is local", target.get("local", False))
    else:
        actual = target.get("target_agent", "?")
        check(f"resolve_target({rule_id}) → {actual}", actual == expected_agent,
              f"expected {expected_agent}")

# ──────────────────────────── 2. Envelope schema ────────────────────────────

print("\n=== Envelope schema ===")
task = a2a_bridge.build_task(
    query="How's the federation health?",
    target_agent="hermes-asi",
    target_skill="federation-health",
    session_id="test-session-001",
)
check("envelope has jsonrpc=2.0", task["jsonrpc"] == "2.0")
check("envelope has method=tasks/send", task["method"] == "tasks/send")
check("envelope has params.id", "id" in task["params"])
check("envelope has params.sessionId", "sessionId" in task["params"])
check("envelope has params.targetAgent", "targetAgent" in task["params"])
check("envelope has params.message", "message" in task["params"])
check("envelope has params.metadata", "metadata" in task["params"])
check("metadata has source_agent=openclaw", task["params"]["metadata"].get("source_agent") == "openclaw")

# ──────────────────────────── 3. Live HTTP dispatch ────────────────────────────

print("\n=== Live HTTP dispatch to :3001/a2a ===")
try:
    out = a2a_bridge.dispatch("R08_SYSTEM_STATUS", "Federation health probe")
    check("R08 dispatch success", out.get("success", False), str(out)[:200])
    check("R08 has aaa_task_id", out.get("aaa_task_id") is not None)
    check("R08 has task_id", out.get("task_id") is not None)
except Exception as e:
    check("R08 dispatch success", False, f"{type(e).__name__}: {e}")

# ──────────────────────────── 4. Delivery adapter ────────────────────────────

print("\n=== Delivery adapter ===")
sample_payload = {
    "result": {
        "id": "test-task-123",
        "metadata": {
            "routing": "hermes-asi",
            "source_agent": "openclaw",
        },
        "history": [
            {"role": "assistant", "parts": [{"type": "text", "text": "All 8 organs healthy. FQ=1.11."}]}
        ],
        "artifacts": [{"text": "All 8 organs healthy. FQ=1.11."}],
    }
}

chunks = format_telegram(sample_payload)
check("telegram renders ≥1 chunk", len(chunks) >= 1)
check("telegram chunk ≤ 4096", all(len(c) <= 4096 for c in chunks))
check("telegram has footer", "DITEMPA BUKAN DIBERI" in chunks[0])

a2a_report = format_a2a(sample_payload)
check("a2a kind=a2a_json", a2a_report["delivery"]["kind"] == "a2a_json")
check("a2a has agent=OpenClaw", a2a_report["delivery"]["agent"] == "OpenClaw")

local_report = format_local(sample_payload, "test-session-001")
check("local file path set", "path" in local_report["delivery"])
check("local file exists", Path(local_report["delivery"]["path"]).exists())

# Telegram deliver() returns chunk count
report = deliver(sample_payload, channel="telegram", session_id="test-session-001")
check("deliver telegram has chunks", "chunks" in report)
check("deliver telegram chunk_count", report.get("chunk_count", 0) >= 1)

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
