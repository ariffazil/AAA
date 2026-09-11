import os
import sys
import json
import tempfile

test_ledger = tempfile.mkdtemp(prefix="test_dp_ledger_")
os.environ["DECISION_PACKET_LEDGER_DIR"] = test_ledger

sys.path.insert(0, '/root/AAA/contracts/decision-packet')
from engine import seal_decision_packet, verify_chain, DecisionPacketError, PolicyHoldRequired, LEDGER_CHAIN_FILE, LEDGER_DIR
from duckdb_adapter import execute_and_seal_geox_packet

print("=== RUNNING DECISION PACKET INTEGRITY SUITE ===")

# 1. Test GEOX Data QA Packet via DuckDB Enclave Adapter
sql = """
SELECT 
    formation, 
    COUNT(*) as count, 
    ROUND(AVG(gr_api), 2) as avg_gr,
    ROUND(MIN(md_m), 1) as min_depth,
    ROUND(MAX(md_m), 1) as max_depth
FROM read_parquet('/data/geox/derived/well_intervals.parquet')
GROUP BY formation;
"""

observations = [
    {
        "statement": "Formation 'B_Sands' contains 100 sample intervals across depth 2151.0m to 2200.5m with mean GR of 45.19 API.",
        "confidence": 0.99,
        "evidence_refs": ["tool_calls[0]"]
    }
]

interpretations = [
    {
        "statement": "Low mean GR (45.19 API) in B_Sands interval indicates potential clean reservoir sand facies.",
        "confidence": 0.72,
        "status": "hypothesis",
        "assumptions": [
            "GR baseline calibrated correctly",
            "No heavy radioactive mineral contamination"
        ],
        "evidence_refs": ["tool_calls[0]"]
    }
]

packet1 = execute_and_seal_geox_packet(
    intent="Profile approved well-interval dataset for QA and facies preliminary classification",
    sql_query=sql,
    dataset_id="geox_well_intervals_v1",
    dataset_path="/data/geox/derived/well_intervals.parquet",
    observations=observations,
    interpretations=interpretations
)

assert packet1["integrity"]["packet_hash"], "Packet 1 missing hash"
assert packet1["integrity"]["previous_ledger_hash"] == "0000000000000000000000000000000000000000000000000000000000000000", "Genesis hash mismatch"
print(f"[PASS] Test 1: Created & sealed Packet 1: {packet1['packet_id']} (Hash: {packet1['integrity']['packet_hash'][:16]}...)")

# 2. Test Second Packet (Chain Continuity)
observations2 = [
    {
        "statement": "Ledger contains 50 sample transactions with zero missing values.",
        "confidence": 1.0,
        "evidence_refs": ["tool_calls[0]"]
    }
]

interpretations2 = [
    {
        "statement": "Ledger integrity is consistent with baseline ledger standard.",
        "confidence": 0.85,
        "status": "preliminary",
        "assumptions": ["Transactions cover the full date range"],
        "evidence_refs": ["tool_calls[0]"]
    }
]

packet2 = execute_and_seal_geox_packet(
    intent="Profile sample ledger dataset",
    sql_query="SELECT count(*) FROM read_parquet('/data/aaa/ledgers/sample_ledger.parquet');",
    dataset_id="sample_ledger_v1",
    dataset_path="/data/aaa/ledgers/sample_ledger.parquet",
    observations=observations2,
    interpretations=interpretations2
)

assert packet2["integrity"]["previous_ledger_hash"] == packet1["integrity"]["packet_hash"], "Chain linkage failed!"
print(f"[PASS] Test 2: Chain Linkage confirmed: Packet 2 links to Packet 1 hash!")

# 3. Test Chain Verification
chain_res = verify_chain()
assert chain_res["valid"] is True, f"Chain invalid: {chain_res}"
assert chain_res["count"] == 2, f"Expected 2 blocks, got {chain_res['count']}"
print(f"[PASS] Test 3: Cryptographic ledger chain verified (2 blocks chained, status=VALID)!")

# 4. Policy Gate Test: Observation Low Confidence Must Fail
try:
    bad_task = {"task_id": "bad1", "intent": "bad", "task_class": "research", "risk_class": "R0", "requester": {"type": "agent", "id": "t", "authority": "low"}}
    bad_exec = {"orchestrator": "h", "route": {"router": "f", "selected_agent": "a", "selected_model": "m", "allowed_capabilities": []}, "session": {"session_id_hash": "s", "authority_context": "a", "policy_version": "p"}}
    bad_ev = {"datasets": [], "sources": [], "tool_calls": []}
    bad_findings = {
        "observations": [{"statement": "Dubious fact", "confidence": 0.60, "evidence_refs": []}],
        "interpretations": []
    }
    bad_act = {"proposed": False, "human_approval": {"required": False, "state": "not_required"}}
    bad_out = {"status": "completed", "limitations": []}
    seal_decision_packet(bad_task, bad_exec, bad_ev, bad_findings, bad_act, bad_out)
    raise AssertionError("Failed to block low-confidence observation!")
except DecisionPacketError as e:
    print(f"[PASS] Test 4: Blocked invalid observation confidence: {e}")

# 5. Policy Gate Test: R3 Action Without 888 HOLD Human Approval Must Fail
try:
    r3_task = {"task_id": "r3_prod", "intent": "Deploy to prod", "task_class": "code_engineering", "risk_class": "R3", "requester": {"type": "agent", "id": "builder", "authority": "builder"}}
    r3_act = {
        "proposed": True,
        "action_class": "deploy_production",
        "target": "live_gateway",
        "human_approval": {"required": True, "state": "pending_888_hold"}
    }
    r3_findings = {
        "observations": [{"statement": "All tests passed", "confidence": 0.99, "evidence_refs": []}],
        "interpretations": [{"statement": "Safe to deploy", "confidence": 0.90, "status": "preliminary", "assumptions": ["Tests cover edge cases"], "evidence_refs": []}]
    }
    seal_decision_packet(r3_task, bad_exec, bad_ev, r3_findings, r3_act, bad_out)
    raise AssertionError("Failed to block unapproved R3 action!")
except PolicyHoldRequired as e:
    print(f"[PASS] Test 5: Blocked R3 action without granted 888 HOLD approval: {e}")

# 6. Tamper Resistance Test
# Intentionally alter packet 1 in chain.jsonl
with open(LEDGER_CHAIN_FILE, "r") as f:
    lines = f.readlines()
p1_tampered = json.loads(lines[0])
p1_tampered["findings"]["observations"][0]["statement"] = "TAMPERED VALUE"
lines[0] = json.dumps(p1_tampered) + "\n"
with open(LEDGER_CHAIN_FILE, "w") as f:
    f.writelines(lines)

tamper_check = verify_chain()
assert tamper_check["valid"] is False, "Failed to detect ledger tampering!"
assert tamper_check["status"] in ("HASH_MISMATCH", "CORRUPTED_CHAIN"), f"Unexpected status: {tamper_check}"
print(f"[PASS] Test 6: Tamper detection succeeded! Tampered block flagged immediately: {tamper_check['status']}")

print("=== ALL 6 DECISION PACKET TESTS PASSED ===")
