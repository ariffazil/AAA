#!/usr/bin/env python3
"""
Test Suite: Phase 4 — Evidence → Judgment Traceability (7 Ujian Hakiki)
Reference: ARIFOS::M365_COPILOT_KERNEL::v1.1
Authority: ARIF (Human Sovereign)
"""

import json
import os
import sys
import time
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, "/root/scripts")
from importlib import import_module

evidence_trace = import_module("evidence-trace")
DecisionEngine = evidence_trace.DecisionEngine
EvidenceIndex = evidence_trace.EvidenceIndex


def run_test_suite():
    print("=" * 60)
    print("  PHASE 4: 7 UJIAN HAKIKI — TRACEABILITY VERIFICATION")
    print("=" * 60)

    engine = DecisionEngine()
    passed = 0
    total = 7

    # ─────────────────────────────────────────────────────────────
    # Test 1: Evidence Provenance Test
    # ─────────────────────────────────────────────────────────────
    print("\n[Test 1] Evidence Provenance Test...")
    d1 = engine.evaluate_and_decide(
        intent="Substrate Health Verification",
        evidence_refs=["E-TIMER-machine-telemetry", "E-TIMER-fq-probe"],
        actor="888-APEX",
    )
    trace1 = engine.trace(d1["decision_id"])
    assert trace1 is not None, "Trace lookup returned None"
    assert trace1["traceable"] is True, "Decision is not traceable to underlying evidence"
    assert len(trace1["evidence"]) == 2, f"Expected 2 evidence items, got {len(trace1['evidence'])}"
    print(f"  ✓ Decision {d1['decision_id']} successfully resolved to {len(trace1['evidence'])} verified evidence records.")
    passed += 1

    # ─────────────────────────────────────────────────────────────
    # Test 2: Missing Evidence Test (Fail-Closed)
    # ─────────────────────────────────────────────────────────────
    print("\n[Test 2] Missing Evidence Test (Degrade to UNKNOWN/PARTIAL)...")
    d2 = engine.evaluate_and_decide(
        intent="Hypothetical Unproven Claim",
        evidence_refs=["E-NONEXISTENT-999999", "E-TIMER-machine-telemetry"],
        actor="888-APEX",
    )
    assert d2["verdict"] in ["UNKNOWN", "PARTIAL"], f"Expected UNKNOWN/PARTIAL for missing evidence, got {d2['verdict']}"
    assert "E-NONEXISTENT-999999" in d2["missing_refs"], "Missing reference was not tracked in missing_refs"
    print(f"  ✓ Missing evidence correctly degraded verdict to {d2['verdict']} (missing: {d2['missing_refs']}).")
    passed += 1

    # ─────────────────────────────────────────────────────────────
    # Test 3: Contradictory Evidence Test
    # ─────────────────────────────────────────────────────────────
    print("\n[Test 3] Contradictory Evidence Test (Conflict Detection)...")
    # Ingest a mock contradictory pair
    mock_conflict_ev = [
        {"source": "FRAME", "severity": "critical", "payload": {"overall_verdict": "CRITICAL"}},
        {"source": "TELEMETRY", "severity": "info", "payload": {"overall_verdict": "HEALTHY_OK"}},
    ]
    conflict, details = engine._detect_contradictions(mock_conflict_ev)
    assert conflict is True, "Failed to detect explicit contradiction between Critical and Healthy claims"
    print(f"  ✓ Contradiction correctly flagged: '{details}'")
    passed += 1

    # ─────────────────────────────────────────────────────────────
    # Test 4: Replay Determinism Test
    # ─────────────────────────────────────────────────────────────
    print("\n[Test 4] Replay Determinism Test (Same Evidence = Same Verdict)...")
    replay_res = engine.replay(d1["decision_id"])
    assert replay_res["deterministic_match"] is True, f"Replay mismatch: {replay_res}"
    assert replay_res["drift_detected"] is False, "Drift unexpectedly detected on replay"
    print(f"  ✓ Replay identical: original={replay_res['original_verdict']} == replayed={replay_res['replayed_verdict']}")
    passed += 1

    # ─────────────────────────────────────────────────────────────
    # Test 5: Audit Trace Speed (<60s target, expected <100ms)
    # ─────────────────────────────────────────────────────────────
    print("\n[Test 5] Audit Trace Speed Test (<60s)...")
    t0 = time.monotonic()
    trace5 = engine.trace(d1["decision_id"])
    elapsed_ms = (time.monotonic() - t0) * 1000
    assert elapsed_ms < 60000, f"Trace exceeded 60s: {elapsed_ms}ms"
    assert trace5 is not None
    print(f"  ✓ Trace completed in {elapsed_ms:.2f}ms (threshold: <60,000ms).")
    passed += 1

    # ─────────────────────────────────────────────────────────────
    # Test 6: No Orphan Decisions (All Decisions Have Traceable Refs)
    # ─────────────────────────────────────────────────────────────
    print("\n[Test 6] No Orphan Decisions Test...")
    ledger_path = Path("/root/AAA/state/decision_ledger.jsonl")
    records = [json.loads(line) for line in ledger_path.read_text().splitlines() if line.strip()]
    for rec in records:
        assert "decision_id" in rec, "Record missing decision_id"
        assert "evidence_refs" in rec, "Record missing evidence_refs"
        assert len(rec["evidence_refs"]) > 0, f"Orphan decision found: {rec['decision_id']} has 0 evidence_refs"
    print(f"  ✓ Verified {len(records)} decision records in ledger — 0 unevidenced orphan decisions.")
    passed += 1

    # ─────────────────────────────────────────────────────────────
    # Test 7: Eckleburg Preservation Test (0 Actuator Paths from FRAME)
    # ─────────────────────────────────────────────────────────────
    print("\n[Test 7] Eckleburg Preservation Test (Reader ≠ Actor)...")
    reader_source = Path("/root/scripts/frame-evidence-reader.py").read_text()
    forbidden_tokens = ["subprocess.call", "systemctl restart", "os.system", "shutil.rmtree", "DROP TABLE"]
    for token in forbidden_tokens:
        assert token not in reader_source, f"Violation of Eckleburg Principle: found forbidden token '{token}' in reader"
    print("  ✓ Verified frame-evidence-reader.py contains zero direct actuator or destructive mutations.")
    passed += 1

    print("\n" + "=" * 60)
    print(f"  SUMMARY: {passed}/{total} TESTS PASSED (100% CONSTITUTIONAL COMPLIANCE)")
    print("=" * 60)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(run_test_suite())
