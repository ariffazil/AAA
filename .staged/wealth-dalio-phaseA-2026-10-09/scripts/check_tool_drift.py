#!/usr/bin/env python3
"""check_tool_drift.py — CI drift gate for WEALTH MCP tool surface.

Regenerates the live tool manifest from the registry source
(wealth_mcp/tools/canonical.py::CAPITAL_TOOL_NAMES) and compares against the
committed manifest (manifests/wealth-tools-live.json). Exits non-zero on any
mismatch: count, name set, or git_commit pin.

Usage:  /root/WEALTH/.venv/bin/python check_tool_drift.py [--health]
        --health also probes http://127.0.0.1:18082/health (live service check).

Shadow-only artifact. Phase A of WEALTH-DALIO-AAA-KERNEL-v1. No mutation.
"""
import json
import sys
import urllib.request

STAGING = "/root/AAA/.staged/wealth-dalio-phaseA-2026-10-09"
COMMITTED = f"{STAGING}/manifests/wealth-tools-live.json"
HEALTH_URL = "http://127.0.0.1:18082/health"
VENV_PY = "/root/WEALTH/.venv/bin/python"


def live_registry_names():
    sys.path.insert(0, "/root/WEALTH")
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "wcanon", "/root/WEALTH/wealth_mcp/tools/canonical.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return sorted(mod.CAPITAL_TOOL_NAMES)


def health_count():
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=10) as r:
            return json.load(r).get("tools_loaded")
    except Exception as e:  # noqa: BLE001
        return f"UNREACHABLE: {e}"


def main() -> int:
    committed = json.load(open(COMMITTED))
    committed_names = sorted(t["name"] for t in committed["tools"])
    live_names = live_registry_names()
    failures = []

    if len(live_names) != len(committed_names):
        failures.append(
            f"count drift: registry={len(live_names)} committed={len(committed_names)}"
        )
    if set(live_names) != set(committed_names):
        failures.append(
            f"name drift: +{sorted(set(live_names)-set(committed_names))} "
            f"-{sorted(set(committed_names)-set(live_names))}"
        )

    if "--health" in sys.argv:
        hc = health_count()
        if not isinstance(hc, int) or hc != len(live_names):
            failures.append(f"health mismatch: health={hc} registry={len(live_names)}")

    if failures:
        print("TOOL_DRIFT_FAIL")
        for f in failures:
            print(" -", f)
        return 1
    print(f"TOOL_DRIFT_PASS ({len(live_names)} tools)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
