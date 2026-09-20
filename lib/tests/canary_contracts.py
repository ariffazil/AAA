#!/usr/bin/env python3
"""canary_contracts.py — example service contracts for the canary primitive.

These define what each service needs to declare for behavioral canary testing.

Per F13: "Don't make 24 bespoke scripts. Infrastructure stays shared."

This file is the SERVICE-SPECIFIC layer. The shared infra is /root/AAA/lib/canary.py.
"""

from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canary import CanaryContract, Probe, http_probe, process_probe, always_pass_rules, critical_failure_rules, noop_rollback


# ── 1. arifos contract (was sliced to 1 key) ────────────────────────

def arifos_start() -> dict:
    """No-op start condition for already-running services."""
    out = subprocess.check_output(["systemctl", "show", "-p", "MainPID", "--value", "arifos"],
                                   text=True, timeout=3).strip()
    pid = int(out) if out.isdigit() else 0
    return {"ok": pid > 0, "instance_id": f"arifos-{pid}", "pid": pid}


arifos_contract = CanaryContract(
    service="arifos",
    description="Constitutional kernel — proves forge_runtime_verify + canonical tools + boot attestation",
    start_condition=arifos_start,
    critical_probes=[
        http_probe("http://127.0.0.1:8088/health",
                   expect_keys=["status", "software_release"],
                   timeout_s=3, weight=2.0),  # high weight
        http_probe("http://127.0.0.1:8088/tools",
                   expect_keys=[],  # /tools is a list; we just need it to return non-empty
                   timeout_s=3, weight=1.0),
    ],
    success_rules=always_pass_rules,
    failure_rules=critical_failure_rules,
    rollback_action=noop_rollback,
    observation_window_s=10,
)


# ── 2. a-forge contract (was sliced to 2 keys) ──────────────────────

def aforge_start() -> dict:
    out = subprocess.check_output(["systemctl", "show", "-p", "MainPID", "--value", "a-forge"],
                                   text=True, timeout=3).strip()
    pid = int(out) if out.isdigit() else 0
    return {"ok": pid > 0, "instance_id": f"a-forge-{pid}", "pid": pid}


aforge_contract = CanaryContract(
    service="a-forge",
    description="A-FORGE core — proves identity_hash + tool registry + federation schema",
    start_condition=aforge_start,
    critical_probes=[
        http_probe("http://127.0.0.1:7071/health",
                   expect_keys=["status", "tools_loaded", "identity_hash"],
                   timeout_s=3, weight=2.0),
    ],
    success_rules=always_pass_rules,
    failure_rules=critical_failure_rules,
    rollback_action=noop_rollback,
    observation_window_s=10,
)


# ── 3. a-forge-mcp contract (kept on flat 192 keys) ───────────────

def aforge_mcp_start() -> dict:
    out = subprocess.check_output(["systemctl", "show", "-p", "MainPID", "--value", "a-forge-mcp"],
                                   text=True, timeout=3).strip()
    pid = int(out) if out.isdigit() else 0
    return {"ok": pid > 0, "instance_id": f"a-forge-mcp-{pid}", "pid": pid}


aforge_mcp_contract = CanaryContract(
    service="a-forge-mcp",
    description="A-FORGE MCP gateway — proves tool exposure on :7072",
    start_condition=aforge_mcp_start,
    critical_probes=[
        http_probe("http://127.0.0.1:7072/health",
                   expect_keys=["status", "ok"],
                   timeout_s=3, weight=2.0),
    ],
    success_rules=always_pass_rules,
    failure_rules=critical_failure_rules,
    rollback_action=noop_rollback,
    observation_window_s=10,
)


# ── 4. aaa-a2a contract (sliced to 6 keys) ─────────────────────────

def aaa_a2a_start() -> dict:
    out = subprocess.check_output(["systemctl", "show", "-p", "MainPID", "--value", "aaa-a2a"],
                                   text=True, timeout=3).strip()
    pid = int(out) if out.isdigit() else 0
    return {"ok": pid > 0, "instance_id": f"aaa-a2a-{pid}", "pid": pid}


aaa_a2a_contract = CanaryContract(
    service="aaa-a2a",
    description="A2A gateway — proves discovery + agent card + endpoints",
    start_condition=aaa_a2a_start,
    critical_probes=[
        http_probe("http://127.0.0.1:3001/.well-known/agent-card.json",
                   expect_keys=["capabilities", "skills"],
                   timeout_s=3, weight=2.0),
    ],
    success_rules=always_pass_rules,
    failure_rules=critical_failure_rules,
    rollback_action=noop_rollback,
    observation_window_s=10,
)


# ── Contract registry ─────────────────────────────────────────────

ALL_CONTRACTS = [arifos_contract, aforge_contract, aforge_mcp_contract, aaa_a2a_contract]


def run_all_canaries(verbose: bool = True) -> list[dict]:
    """Run canary for every registered contract. Returns list of result dicts."""
    from canary import canary
    results = []
    for contract in ALL_CONTRACTS:
        if verbose:
            print(f"\n========== canary: {contract.service} ==========")
        result = canary(contract, candidate_env_path=None)
        results.append({
            "service": result.service,
            "verdict": result.verdict,
            "elapsed_s": result.elapsed_s,
            "receipt_path": result.receipt_path,
            "notes": result.notes,
        })
        if verbose:
            print(f"   verdict={result.verdict} elapsed={result.elapsed_s}s receipt={result.receipt_path}")
    return results


if __name__ == "__main__":
    import json
    results = run_all_canaries()
    print(f"\n=== {len(results)} canaries completed ===")
    print(json.dumps(results, indent=2))
