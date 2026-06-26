#!/usr/bin/env python3
"""
Tool Health Checker — OpenClaw Skill
Smoke-tests critical MCP tools across all organs.
Returns PASS/FAIL/UNTESTABLE per tool with reason.

Read-only. No mutations. Safe for cron or manual invocation.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import json
import time
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError

# ─── Configuration ───
GATEWAY_URL = "http://127.0.0.1:8091/mcp"
TIMEOUT_SEC = 10

# Critical tool subsets — OBSERVE only for smoke tests
ARIFOS_SMOKE_TOOLS = [
    {"name": "arif_os_attest",         "args": {},                     "tier": "OBSERVE"},
    {"name": "arif_ops_measure",       "args": {"mode": "health"},     "tier": "OBSERVE"},
    {"name": "arif_heartbeat",         "args": {},                     "tier": "OBSERVE"},
    {"name": "arif_organ_attest_all",  "args": {},                     "tier": "OBSERVE"},
    {"name": "arif_sense_observe",     "args": {"mode": "vitals"},     "tier": "OBSERVE"},
    {"name": "arif_memory_recall",     "args": {"mode": "recall", "query": "test"}, "tier": "OBSERVE"},
]

ARIFOS_UNTESTABLE_TOOLS = [
    "arif_session_init",      # requires actor signature
    "arif_lease_issue",       # requires session + sovereign
    "arif_judge_deliberate",  # requires full constitutional chain
    "arif_vault_seal",        # irreversible — F1 gate
    "arif_forge_execute",     # requires SEAL verdict
    "arif_gateway_connect",   # requires target_agent routing
]

GATEWAY_SMOKE_TOOLS = [
    {"name": "gateway_health",        "args": {}, "tier": "OBSERVE"},
    {"name": "gateway_receipts",      "args": {}, "tier": "OBSERVE"},
    {"name": "gateway_lease_inspect", "args": {}, "tier": "OBSERVE"},
]

ORGAN_SMOKE_PROBES = [
    {"organ": "GEOX",   "url": "http://127.0.0.1:18081/mcp", "tool": "geox_system_registry_status", "args": {}},
    {"organ": "WEALTH", "url": "http://127.0.0.1:18082/mcp", "tool": "wealth_system_registry_status", "args": {}},
    {"organ": "WELL",   "url": "http://127.0.0.1:18083/mcp", "tool": "well_system_registry_status",  "args": {}},
]

INFRA_PROBES = [
    {"name": "NATS connectivity", "cmd": ["nats", "server", "check", "connection"], "timeout": 5},
    {"name": "A-FORGE health",    "cmd": ["curl", "-sf", "--max-time", "5", "http://127.0.0.1:7071/health"], "timeout": 6},
    {"name": "arifOS /health",    "cmd": ["curl", "-sf", "--max-time", "5", "http://127.0.0.1:8088/health"], "timeout": 6},
    {"name": "AAA gateway /health","cmd": ["curl", "-sf", "--max-time", "5", "http://127.0.0.1:8091/health"], "timeout": 6},
]


def call_mcp_tool(url: str, tool_name: str, args: dict) -> dict:
    """Call an MCP tool and return raw result dict."""
    import json as _json
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": args}
    }
    req = Request(url, data=_json.dumps(payload).encode(),
                  headers={"Content-Type": "application/json", "Accept": "application/json"})
    with urlopen(req, timeout=TIMEOUT_SEC) as resp:
        return _json.loads(resp.read().decode())


def test_tool(url: str, tool: dict) -> dict:
    """Smoke-test one tool. Returns PASS/FAIL with evidence."""
    name = tool["name"]
    start = time.monotonic()
    try:
        result = call_mcp_tool(url, name, tool["args"])
        latency_ms = round((time.monotonic() - start) * 1000, 1)

        if "error" in result:
            return {
                "tool": name, "organ": "arifOS",
                "status": "FAIL", "latency_ms": latency_ms,
                "reason": str(result["error"].get("message", "Unknown error"))[:200]
            }
        return {
            "tool": name, "organ": "arifOS",
            "status": "PASS", "latency_ms": latency_ms,
            "evidence": f"MCP response received in {latency_ms}ms"
        }
    except Exception as e:
        return {
            "tool": name, "organ": "arifOS",
            "status": "FAIL", "latency_ms": None,
            "reason": str(e)[:200]
        }


def test_organ_tool(probe: dict) -> dict:
    """Smoke-test an organ-specific tool."""
    name = probe["tool"]
    organ = probe["organ"]
    start = time.monotonic()
    try:
        result = call_mcp_tool(probe["url"], name, probe["args"])
        latency_ms = round((time.monotonic() - start) * 1000, 1)
        if "error" in result:
            return {
                "tool": name, "organ": organ,
                "status": "FAIL", "latency_ms": latency_ms,
                "reason": str(result["error"].get("message", "?"))[:200]
            }
        return {
            "tool": name, "organ": organ,
            "status": "PASS", "latency_ms": latency_ms,
            "evidence": f"{organ} registry responded in {latency_ms}ms"
        }
    except Exception as e:
        return {
            "tool": name, "organ": organ,
            "status": "FAIL", "latency_ms": None,
            "reason": str(e)[:200]
        }


def test_infra(probe: dict) -> dict:
    """Smoke-test an infrastructure probe."""
    import subprocess
    start = time.monotonic()
    try:
        r = subprocess.run(probe["cmd"], capture_output=True, text=True,
                          timeout=probe.get("timeout", 10))
        latency_ms = round((time.monotonic() - start) * 1000, 1)
        if r.returncode == 0:
            return {"name": probe["name"], "status": "PASS", "latency_ms": latency_ms,
                    "evidence": f"exit 0 in {latency_ms}ms"}
        else:
            return {"name": probe["name"], "status": "FAIL", "latency_ms": latency_ms,
                    "reason": r.stderr[:200] or f"exit code {r.returncode}"}
    except Exception as e:
        return {"name": probe["name"], "status": "FAIL", "latency_ms": None,
                "reason": str(e)[:200]}


def main():
    start = time.monotonic()
    results = []

    # 1. Gateway tools
    for tool in GATEWAY_SMOKE_TOOLS:
        results.append(test_tool(GATEWAY_URL, tool))

    # 2. arifOS OBSERVE tools
    for tool in ARIFOS_SMOKE_TOOLS:
        results.append(test_tool(GATEWAY_URL, tool))

    # 3. arifOS UNTESTABLE tools (report, don't test)
    for name in ARIFOS_UNTESTABLE_TOOLS:
        results.append({
            "tool": name, "organ": "arifOS",
            "status": "UNTESTABLE",
            "reason": "Requires full session init / sovereign signature / constitutional chain — not smokable"
        })

    # 4. Organ tools
    for probe in ORGAN_SMOKE_PROBES:
        results.append(test_organ_tool(probe))

    # 5. Infrastructure probes
    for probe in INFRA_PROBES:
        results.append(test_infra(probe))

    # Summary
    passed = [r for r in results if r.get("status") == "PASS"]
    failed = [r for r in results if r.get("status") == "FAIL"]
    untestable = [r for r in results if r.get("status") == "UNTESTABLE"]

    summary = "OK" if not failed else ("WARN" if len(failed) <= 2 else "CRITICAL")

    output = {
        "tool_health_check": {
            "summary": summary,
            "stats": {
                "total": len(results),
                "pass": len(passed),
                "fail": len(failed),
                "untestable": len(untestable)
            },
            "failed_tools": [f["tool"] for f in failed],
            "results": results,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "scan_duration_ms": round((time.monotonic() - start) * 1000)
        }
    }

    print(json.dumps(output, indent=2))
    return 0 if summary == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
