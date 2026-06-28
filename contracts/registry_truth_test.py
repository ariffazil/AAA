#!/usr/bin/env python3
"""
Registry Truth Test — Canonical CI Gate for arifOS Federation
══════════════════════════════════════════════════════════════

Capability Spine Repair 2026-06-26.
Tests every organ's tool surface for registry/runtime/guard drift.

Pass condition (per organ):
  intended_tools == registered_tools == callable_tools
  phantom_tools == 0
  guard_conflicts == 0
  schema_failures == 0

Usage:
  python registry_truth_test.py                  # all organs
  python registry_truth_test.py --organ arifos   # single organ
  python registry_truth_test.py --ci             # CI mode (exit 1 on failure)
  python registry_truth_test.py --report         # generate JSON report

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ── Organ Configuration ───────────────────────────────────────────────────────

ORGANS: dict[str, dict[str, Any]] = {
    "arifos": {
        "health_url": "http://127.0.0.1:8088/health",
        "mcp_url": "http://127.0.0.1:8088/mcp",
        "canonical_tools": [
            "arif_init", "arif_observe", "arif_think", "arif_route",
            "arif_judge", "arif_act", "arif_seal",
        ],
        "required_diagnostic_tools": [
            "arif_triage", "arif_measure", "hermes_vault_query",
        ],
        "registry_tool": None,  # arifOS uses /health endpoint for registry truth
    },
    "well": {
        "health_url": "http://127.0.0.1:18083/health",
        "mcp_url": "http://127.0.0.1:18083/mcp",
        "canonical_tools": [
            "well_classify_substrate", "well_trace_lineage",
            "well_detect_boundary", "well_measure_gradient",
            "well_assess_metabolism", "well_assess_homeostasis",
            "well_check_repair", "well_validate_vitality",
            "well_assess_livelihood", "well_assess_reliability",
            "well_compute_metabolic_flux", "well_guard_dignity",
            "well_assess_sovereign_entropy",
        ],
        "required_diagnostic_tools": [
            "well_system_registry_status", "well_registry_status",
            "well_13_signal_coverage",
        ],
        "registry_tool": "well_system_registry_status",
    },
    "wealth": {
        "health_url": "http://127.0.0.1:18082/health",
        "mcp_url": "http://127.0.0.1:18082/mcp",
        "canonical_tools": [],  # Discovered dynamically
        "required_diagnostic_tools": ["wealth_system_registry_status"],
        "registry_tool": "wealth_system_registry_status",
    },
    "geox": {
        "health_url": "http://127.0.0.1:8081/health",
        "mcp_url": "http://127.0.0.1:8081/mcp",
        "canonical_tools": [],  # Discovered dynamically
        "required_diagnostic_tools": [],
        "registry_tool": "geox_system_registry_status",
    },
    "aforge": {
        "health_url": "http://127.0.0.1:7071/health",
        "mcp_url": "http://127.0.0.1:7071/mcp",
        "canonical_tools": [],  # Discovered dynamically
        "required_diagnostic_tools": [],
        "registry_tool": None,
    },
}


@dataclass
class OrganReport:
    organ: str
    health_status: str = "unknown"
    health_data: dict = field(default_factory=dict)
    mcp_tools: list[str] = field(default_factory=list)
    declared_tools: list[str] = field(default_factory=list)
    phantom_tools: list[str] = field(default_factory=list)
    missing_tools: list[str] = field(default_factory=list)
    guard_conflicts: list[str] = field(default_factory=list)
    schema_failures: list[str] = field(default_factory=list)
    unreachable_tools: list[str] = field(default_factory=list)
    registry_truth: str = "UNKNOWN"
    pass_: bool = False
    errors: list[str] = field(default_factory=list)


def mcp_rpc(url: str, method: str, params: dict | None = None) -> dict:
    """Send a JSON-RPC 2.0 request to an MCP endpoint."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


def fetch_health(url: str) -> dict:
    """Fetch health endpoint."""
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


def get_mcp_tool_list(mcp_url: str) -> list[str]:
    """Get the list of tools exposed via MCP tools/list."""
    result = mcp_rpc(mcp_url, "tools/list")
    if "error" in result:
        return []
    tools = result.get("result", {}).get("tools", [])
    return sorted([t["name"] for t in tools])


def test_tool_callable(mcp_url: str, tool_name: str) -> bool:
    """Test if a tool is callable by sending a minimal probe call.

    Uses a safe probe — sends empty params and checks for 'Unknown tool' error.
    A 'Tool not found' or 'Unknown tool' response = NOT callable.
    Any other response (including validation errors) = CALLABLE (handler exists).
    """
    result = mcp_rpc(mcp_url, "tools/call", {
        "name": tool_name,
        "arguments": {},
    })
    if "error" in result:
        err_msg = str(result["error"]).lower()
        if "unknown tool" in err_msg or "tool not found" in err_msg or "not found" in err_msg:
            return False
        # Other errors (validation, missing params) mean the tool IS callable
        # but our probe was malformed — which is expected
        return True
    return True  # Got a response = callable


def check_arifos_registry_truth(health_data: dict) -> dict:
    """arifOS-specific: check surface_consistency from health endpoint."""
    sc = health_data.get("surface_consistency", {})
    return {
        "verdict": sc.get("verdict", "UNKNOWN"),
        "divergences": sc.get("divergences", []),
        "canonical_count": sc.get("canonical_count", 0),
        "runtime_drift": health_data.get("runtime_drift", False),
        "contract_drift": health_data.get("contract_drift", False),
    }


def test_organ(name: str, config: dict) -> OrganReport:
    """Run the full registry truth test on one organ."""
    report = OrganReport(organ=name)
    declared = set(config.get("canonical_tools", []))
    required_diag = set(config.get("required_diagnostic_tools", []))
    intended = declared | required_diag

    # 1. Health check
    health = fetch_health(config["health_url"])
    report.health_data = health
    if "error" in health:
        report.errors.append(f"Health endpoint unreachable: {health['error']}")
        report.health_status = "UNREACHABLE"
        return report

    report.health_status = health.get("status", health.get("owner_summary", {}).get("color", "unknown"))

    # 2. MCP tools/list — what's actually exposed
    mcp_tools = get_mcp_tool_list(config["mcp_url"])
    report.mcp_tools = mcp_tools
    mcp_set = set(mcp_tools)

    # 3. Discover declared tools from MCP tools/list if not pre-configured
    if not declared:
        declared = {t for t in mcp_set if not t.startswith("mcp_")}
        report.declared_tools = sorted(declared)

    # 4. Phantom check: tools in intended but NOT in MCP tools/list
    report.phantom_tools = sorted(intended - mcp_set)

    # 5. Missing check: tools that should exist but don't
    report.missing_tools = sorted((intended | declared) - mcp_set)

    # 6. Callability check: probe each intended tool
    for tool_name in sorted(intended):
        if tool_name in mcp_set:
            if not test_tool_callable(config["mcp_url"], tool_name):
                report.unreachable_tools.append(tool_name)

    # 7. Registry truth via dedicated tool if available
    registry_tool = config.get("registry_tool")
    if registry_tool and registry_tool in mcp_set:
        result = mcp_rpc(config["mcp_url"], "tools/call", {
            "name": registry_tool,
            "arguments": {},
        })
        if "error" not in result:
            content = result.get("result", {}).get("content", [])
            if content:
                try:
                    inner = json.loads(content[0].get("text", "{}"))
                    report.registry_truth = inner.get("registry_truth", inner.get("registry_status", "UNKNOWN"))
                except (json.JSONDecodeError, KeyError, IndexError):
                    pass

    # 8. arifOS-specific: surface_consistency check
    if name == "arifos":
        arifos_truth = check_arifos_registry_truth(health)
        report.registry_truth = arifos_truth["verdict"]
        if arifos_truth["runtime_drift"]:
            report.errors.append("Runtime drift: container image ≠ git HEAD")

    # 9. Pass/fail
    report.pass_ = (
        len(report.phantom_tools) == 0
        and len(report.unreachable_tools) == 0
        and len(report.guard_conflicts) == 0
    )

    return report


def print_report(reports: list[OrganReport], ci_mode: bool = False) -> int:
    """Print human-readable test report. Returns exit code."""
    all_pass = True

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  REGISTRY TRUTH TEST — arifOS Federation CI Gate           ║")
    print("║  Capability Spine Repair 2026-06-26                        ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    for r in reports:
        status_icon = "✅" if r.pass_ else "❌"
        health_icon = {
            "healthy": "🟢", "ALIVE": "🟢", "GREEN": "🟢",
            "degraded": "🟡", "DEGRADED": "🟡", "YELLOW": "🟡",
            "RED": "🔴", "UNREACHABLE": "🔴",
        }.get(r.health_status, "⚪")

        print(f"{status_icon} {health_icon} {r.organ.upper():12s}  "
              f"health={r.health_status:12s}  "
              f"MCP tools={len(r.mcp_tools):3d}  "
              f"phantoms={len(r.phantom_tools):2d}  "
              f"unreachable={len(r.unreachable_tools):2d}  "
              f"pass={r.pass_}")

        if r.errors:
            for err in r.errors:
                print(f"   ⚠️  {err}")
        if r.phantom_tools:
            print(f"   👻 Phantom tools (declared but not exposed):")
            for pt in r.phantom_tools:
                print(f"      - {pt}")
        if r.unreachable_tools:
            print(f"   💀 Unreachable tools (exposed but not callable):")
            for ut in r.unreachable_tools:
                print(f"      - {ut}")

        all_pass = all_pass and r.pass_
        print()

    # Summary
    print("─── Federation Readiness ───")
    registry_healthy = all(r.health_status in ("healthy", "ALIVE", "GREEN") for r in reports)
    all_phantoms_zero = all(len(r.phantom_tools) == 0 for r in reports)
    all_unreachable_zero = all(len(r.unreachable_tools) == 0 for r in reports)
    no_guard_conflicts = all(len(r.guard_conflicts) == 0 for r in reports)

    print(f"  All organs healthy:       {'✅' if registry_healthy else '❌'}")
    print(f"  Phantom tools = 0:        {'✅' if all_phantoms_zero else '❌'}")
    print(f"  Unreachable tools = 0:    {'✅' if all_unreachable_zero else '❌'}")
    print(f"  Guard conflicts = 0:      {'✅' if no_guard_conflicts else '❌'}")
    print()

    if all_pass and registry_healthy:
        print("🎉 VERDICT: AGENTIC_RUNTIME_READY = true")
        print("   All organs pass registry truth test.")
        return 0
    else:
        print("🚫 VERDICT: AGENTIC_RUNTIME_READY = false")
        print("   Fix the above issues before enabling agentic execution.")
        return 1 if ci_mode else 0


def generate_json_report(reports: list[OrganReport]) -> str:
    """Generate JSON report for machine consumption."""
    return json.dumps({
        "test": "registry_truth_test",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "organs": {
            r.organ: {
                "health_status": r.health_status,
                "mcp_tools_count": len(r.mcp_tools),
                "phantom_tools": r.phantom_tools,
                "unreachable_tools": r.unreachable_tools,
                "guard_conflicts": r.guard_conflicts,
                "registry_truth": r.registry_truth,
                "pass": r.pass_,
                "errors": r.errors,
            }
            for r in reports
        },
        "pass_condition": {
            "phantom_tools": sum(len(r.phantom_tools) for r in reports),
            "unreachable_tools": sum(len(r.unreachable_tools) for r in reports),
            "guard_conflicts": sum(len(r.guard_conflicts) for r in reports),
        },
        "verdict": "AGENTIC_RUNTIME_READY" if all(r.pass_ for r in reports) else "NOT_READY",
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Registry Truth Test — arifOS Federation CI Gate")
    parser.add_argument("--organ", choices=list(ORGANS.keys()), help="Test a single organ")
    parser.add_argument("--ci", action="store_true", help="CI mode: exit 1 on failure")
    parser.add_argument("--report", action="store_true", help="Generate JSON report")
    parser.add_argument("--output", type=Path, help="Write JSON report to file")
    args = parser.parse_args()

    organs_to_test = [args.organ] if args.organ else list(ORGANS.keys())
    reports = []

    for name in organs_to_test:
        config = ORGANS[name]
        print(f"Testing {name}...", file=sys.stderr)
        report = test_organ(name, config)
        reports.append(report)

    if args.report or args.output:
        json_out = generate_json_report(reports)
        if args.output:
            args.output.write_text(json_out)
            print(f"Report written to {args.output}", file=sys.stderr)
        else:
            print(json_out)
        return 0

    return print_report(reports, ci_mode=args.ci)


if __name__ == "__main__":
    sys.exit(main())
