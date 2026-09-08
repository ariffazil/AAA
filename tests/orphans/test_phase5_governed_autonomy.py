#!/usr/bin/env python3
"""
Test Suite: Phase 5 Governed Autonomy — The 7 True Seal Tests
Reference: ARIFOS::M365_COPILOT_KERNEL::v1.1
Authority: ARIF (Human Sovereign, F13)

7 Ujian Hakiki:
  1. No Judgment, No Execution
  2. No Evidence, No Judgment
  3. Tampered Decision
  4. Replay Protection
  5. Authority Ceiling
  6. Constitutional Citation
  7. Consequence Trace
"""

import sys
import time
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, "/root/scripts")
from importlib import import_module

gov_exec = import_module("governed-execution")
evidence_trace = import_module("evidence-trace")

GovernedExecutionEngine = gov_exec.GovernedExecutionEngine
DecisionEngine = evidence_trace.DecisionEngine


def run_test_1(engine, dec_engine):
    """Test 1: No Judgment, No Execution (Execution without valid decision MUST be blocked)."""
    print("\n--- Test 1: No Judgment, No Execution ---")
    fake_contract = {
        "contract_id": "EC-FAKE-0001",
        "decision_id": "D-NONEXISTENT-999",
        "decision_reasoning_hash": "fakehash",
        "action_type": "SERVICE_RESTART",
        "target": "fq-probe.service",
        "constitutional_basis": "F13",
        "actor_lane": "888-APEX",
        "nonce": "fake-nonce-001",
        "signature": "fakesig",
        "status": "ISSUED",
        "created_at": "2026-08-15T14:00:00Z",
        "expires_at": "2026-08-15T15:00:00Z",
    }
    res = engine.execute_governed_action(fake_contract)
    assert res["ok"] is False, "Execution should be blocked without valid decision"
    assert res["verdict"] == "BLOCKED"
    print("PASS: Execution blocked when decision is missing.")
    return True


def run_test_2(engine, dec_engine):
    """Test 2: No Evidence, No Judgment (Decision lacking evidence cannot generate execution contract)."""
    print("\n--- Test 2: No Evidence, No Judgment ---")
    # Record unevidenced decision
    dec = dec_engine.evaluate_and_decide(
        intent="Attempted Action With Zero Evidence",
        evidence_refs=[],
        actor="888-APEX",
        explicit_confidence=0.95
    )
    assert dec["verdict"] in ["UNKNOWN", "HOLD", "PARTIAL"]

    # Try issuing contract
    res = engine.issue_execution_contract(
        decision_id=dec["decision_id"],
        action_type="FILE_MUTATION",
        target="/root/test.txt",
        constitutional_basis="F1 AMANAH"
    )
    assert res["ok"] is False
    print(f"PASS: Contract issuance rejected ({res['status']}) for decision without evidence.")
    return True


def run_test_3(engine, dec_engine):
    """Test 3: Tampered Decision (Altered reasoning_hash or signature is caught and stopped)."""
    print("\n--- Test 3: Tampered Decision ---")
    # Valid decision first
    dec = dec_engine.evaluate_and_decide(
        intent="Legitimate Maintenance Action",
        evidence_refs=["E-TIMER-fq-probe", "E-TIMER-machine-telemetry"],
        actor="888-APEX",
        explicit_confidence=0.95
    )
    assert dec["verdict"] == "SEAL"

    contract_res = engine.issue_execution_contract(
        decision_id=dec["decision_id"],
        action_type="SERVICE_RESTART",
        target="fq-probe.service",
        constitutional_basis="F13 SOVEREIGN"
    )
    assert contract_res["ok"] is True
    valid_contract = contract_res["contract"]

    # Tamper with reasoning hash
    tampered_contract = dict(valid_contract)
    tampered_contract["decision_reasoning_hash"] = "tampered_hash_000000000"

    res = engine.execute_governed_action(tampered_contract)
    assert res["ok"] is False
    assert res["verdict"] == "BLOCKED"
    assert "Tampered Decision" in res["gate_failed"]
    print("PASS: Tampered decision detected and execution blocked.")
    return True


def run_test_4(engine, dec_engine):
    """Test 4: Replay Protection (Re-using execution contract or nonce MUST fail)."""
    print("\n--- Test 4: Replay Protection ---")
    dec = dec_engine.evaluate_and_decide(
        intent="One-Time Scheduled Task",
        evidence_refs=["E-TIMER-sct-renew"],
        actor="888-APEX",
        explicit_confidence=0.95
    )
    contract_res = engine.issue_execution_contract(
        decision_id=dec["decision_id"],
        action_type="TOKEN_REFRESH",
        target="sct_vault",
        constitutional_basis="F13"
    )
    contract = contract_res["contract"]

    # 1st Execution -> SUCCESS
    res1 = engine.execute_governed_action(contract)
    assert res1["ok"] is True
    assert res1["verdict"] == "SEAL"
    print("  1st run: EXECUTED successfully.")

    # 2nd Execution with same contract -> MUST BE BLOCKED
    res2 = engine.execute_governed_action(contract)
    assert res2["ok"] is False
    assert res2["verdict"] == "BLOCKED"
    assert "Replay Protection" in res2["gate_failed"]
    print("PASS: Replay attempt blocked by single-use nonce.")
    return True


def run_test_5(engine, dec_engine):
    """Test 5: Authority Ceiling (333-AGI lane cannot issue privileged mutation without 888)."""
    print("\n--- Test 5: Authority Ceiling ---")
    dec = dec_engine.evaluate_and_decide(
        intent="Research Proposal Mutation",
        evidence_refs=["E-TIMER-fq-probe"],
        actor="888-APEX",
        explicit_confidence=0.95
    )
    res = engine.issue_execution_contract(
        decision_id=dec["decision_id"],
        action_type="SERVICE_RESTART",
        target="geox.service",
        constitutional_basis="F13",
        actor_lane="333-AGI"  # 333 lane exceeds ceiling
    )
    assert res["ok"] is False
    assert res["status"] == "BLOCKED_AUTHORITY_CEILING"
    print("PASS: Lane 333 blocked by authority ceiling.")
    return True


def run_test_6(engine, dec_engine):
    """Test 6: Constitutional Citation (Action must cite explicit constitutional basis)."""
    print("\n--- Test 6: Constitutional Citation ---")
    dec = dec_engine.evaluate_and_decide(
        intent="Unconstitutional Action Without Citation",
        evidence_refs=["E-TIMER-fq-probe"],
        actor="888-APEX",
        explicit_confidence=0.95
    )
    res = engine.issue_execution_contract(
        decision_id=dec["decision_id"],
        action_type="SERVICE_RESTART",
        target="test.service",
        constitutional_basis=""  # Empty citation
    )
    assert res["ok"] is False
    assert res["status"] == "REJECTED_NO_CONSTITUTIONAL_CITATION"
    print("PASS: Missing constitutional citation rejected.")
    return True


def run_test_7(engine, dec_engine):
    """Test 7: Consequence Trace (Mutation traces end-to-end back to witness)."""
    print("\n--- Test 7: Consequence Trace ---")
    t0 = time.monotonic()
    dec = dec_engine.evaluate_and_decide(
        intent="End-to-End Governed Mutation Verification",
        evidence_refs=["E-TIMER-fq-probe", "E-TIMER-machine-telemetry", "E-TIMER-frame-reader"],
        actor="888-APEX",
        explicit_confidence=0.96
    )
    contract_res = engine.issue_execution_contract(
        decision_id=dec["decision_id"],
        action_type="DEPLOY_VERIFIED_PACKAGE",
        target="aaa-control-plane",
        constitutional_basis="F13 SOVEREIGN + F1 AMANAH"
    )
    contract = contract_res["contract"]
    exec_res = engine.execute_governed_action(contract)

    assert exec_res["ok"] is True
    assert exec_res["verdict"] == "SEAL"
    assert "consequence_trace" in exec_res
    trace = exec_res["consequence_trace"]
    assert trace["mutation"].startswith("MUT-")
    assert trace["contract"] == contract["contract_id"]
    assert trace["decision"] == dec["decision_id"]
    assert len(trace["evidence_refs"]) == 3

    elapsed_ms = (time.monotonic() - t0) * 1000
    print(f"PASS: Full Consequence Trace resolved in {elapsed_ms:.2f}ms.")
    print(f"  Mutation ID: {exec_res['mutation_id']}")
    print(f"  Contract ID: {exec_res['contract_id']}")
    print(f"  Decision ID: {exec_res['decision_id']}")
    return True


def main():
    print("============================================================")
    print("  PHASE 5: GOVERNED AUTONOMY — 7 UJIAN HAKIKI")
    print("============================================================")

    engine = GovernedExecutionEngine()
    dec_engine = DecisionEngine()

    tests = [
        run_test_1,
        run_test_2,
        run_test_3,
        run_test_4,
        run_test_5,
        run_test_6,
        run_test_7,
    ]

    passed = 0
    for t in tests:
        if t(engine, dec_engine):
            passed += 1

    print("\n============================================================")
    print(f"  SUMMARY: {passed}/{len(tests)} TESTS PASSED (100% PHASE 5 COMPLIANCE)")
    print("============================================================")


if __name__ == "__main__":
    main()
