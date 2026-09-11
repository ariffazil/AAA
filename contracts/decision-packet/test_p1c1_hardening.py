import os
import sys
import json
import shutil
import tempfile

test_ledger = tempfile.mkdtemp(prefix="test_dp_ledger_")
os.environ["DECISION_PACKET_LEDGER_DIR"] = test_ledger

sys.path.insert(0, '/root/AAA/contracts/decision-packet')
from engine import (
    seal_decision_packet,
    verify_chain,
    DecisionPacketError,
    ReplayDetectedError,
    LEDGER_DIR,
    LEDGER_CHAIN_FILE,
    NONCE_CACHE_FILE
)
from duckdb_adapter import execute_and_seal_geox_packet

print("=== RUNNING P1-C.1 HARDENING & VERIFICATION SUITE ===")

# 1. Monotonic Sequence & Envelope Fields Test
observations1 = [{"statement": "Well Malay-1 depth range confirmed.", "confidence": 0.99, "evidence_refs": ["tool_calls[0]"]}]
interpretations1 = [{"statement": "Interval is sand-prone.", "confidence": 0.70, "status": "hypothesis", "assumptions": ["Standard facies model"], "evidence_refs": ["tool_calls[0]"]}]

p1 = execute_and_seal_geox_packet(
    intent="Step 1: Profile well intervals",
    sql_query="SELECT COUNT(*) FROM read_parquet('/data/geox/derived/well_intervals.parquet');",
    dataset_id="geox_well_intervals_v1",
    dataset_path="/data/geox/derived/well_intervals.parquet",
    observations=observations1,
    interpretations=interpretations1
)
assert p1["integrity"]["sequence_no"] == 1
assert p1["integrity"]["hash_algorithm"] == "SHA-256"
assert p1["integrity"]["ledger_id"] == "aaa-decision-ledger-main"
assert "request_nonce" in p1["integrity"]
assert "correlation_id" in p1["integrity"]
print(f"[PASS] Test 1: Packet 1 sealed with sequence_no=1, correlation_id={p1['integrity']['correlation_id']}")

p2 = execute_and_seal_geox_packet(
    intent="Step 2: Profile ledger",
    sql_query="SELECT COUNT(*) FROM read_parquet('/data/aaa/ledgers/sample_ledger.parquet');",
    dataset_id="sample_ledger_v1",
    dataset_path="/data/aaa/ledgers/sample_ledger.parquet",
    observations=[{"statement": "Ledger is populated.", "confidence": 0.99, "evidence_refs": ["tool_calls[0]"]}],
    interpretations=[{"statement": "Ledger healthy.", "confidence": 0.80, "status": "hypothesis", "assumptions": ["No gaps in dates"], "evidence_refs": ["tool_calls[0]"]}]
)
assert p2["integrity"]["sequence_no"] == 2
assert p2["integrity"]["previous_ledger_hash"] == p1["integrity"]["packet_hash"]
print(f"[PASS] Test 2: Packet 2 sealed with monotonic sequence_no=2, linked to Packet 1 hash!")

p3 = execute_and_seal_geox_packet(
    intent="Step 3: Check max depth",
    sql_query="SELECT MAX(md_m) FROM read_parquet('/data/geox/derived/well_intervals.parquet');",
    dataset_id="geox_well_intervals_v1",
    dataset_path="/data/geox/derived/well_intervals.parquet",
    observations=[{"statement": "Max depth is 2200.5m.", "confidence": 1.0, "evidence_refs": ["tool_calls[0]"]}],
    interpretations=[{"statement": "Well reaches target TD.", "confidence": 0.85, "status": "hypothesis", "assumptions": ["TD marker verified"], "evidence_refs": ["tool_calls[0]"]}]
)
assert p3["integrity"]["sequence_no"] == 3
print(f"[PASS] Test 3: Packet 3 sealed with monotonic sequence_no=3!")

# 2. Chain Verification
v = verify_chain()
assert v["valid"] is True
assert v["count"] == 3
assert v["latest_sequence"] == 3
print(f"[PASS] Test 4: verify_chain() returned VALID for 3-block chain!")

# 3. Replay Attack Detection (Reusing Nonce)
used_nonce = p1["integrity"]["request_nonce"]
try:
    task = {"task_id": "replay_task", "intent": "replay", "task_class": "research", "risk_class": "R0", "requester": {"type": "agent", "id": "a", "authority": "test"}}
    exec_c = {"orchestrator": "h", "route": {"router": "f", "selected_agent": "g", "selected_model": "m", "allowed_capabilities": []}, "session": {"session_id_hash": "s", "authority_context": "a", "policy_version": "p"}}
    ev = {"datasets": [], "sources": [], "tool_calls": []}
    fnd = {"observations": [{"statement": "valid", "confidence": 0.95, "evidence_refs": []}], "interpretations": [{"statement": "valid", "confidence": 0.7, "status": "hypothesis", "assumptions": ["a"], "evidence_refs": []}]}
    act = {"proposed": False, "human_approval": {"required": False, "state": "not_required"}}
    out = {"status": "completed", "limitations": []}
    seal_decision_packet(task, exec_c, ev, fnd, act, out, request_nonce=used_nonce)
    raise AssertionError("Replay attack was not detected!")
except ReplayDetectedError as e:
    print(f"[PASS] Test 5: Replay attack blocked successfully: {e}")

# 4. Sequence Gap / Middle Packet Deletion Detection
with open(LEDGER_CHAIN_FILE, "r") as f:
    lines = f.readlines()
# Delete middle packet (Packet 2)
tampered_lines = [lines[0], lines[2]]
with open(LEDGER_CHAIN_FILE, "w") as f:
    f.writelines(tampered_lines)

gap_res = verify_chain()
assert gap_res["valid"] is False
assert gap_res["status"] in ("SEQUENCE_GAP_OR_REORDER", "CORRUPTED_CHAIN")
print(f"[PASS] Test 6: Middle packet removal immediately caught: {gap_res['status']} at index {gap_res['index']}")

# Restore valid chain
with open(LEDGER_CHAIN_FILE, "w") as f:
    f.writelines(lines)
assert verify_chain()["valid"] is True

# 5. Replay Reproducibility Drill
# Read Packet 1, extract its query and result hash, re-execute against DuckDB
with open(os.path.join(LEDGER_DIR, f"{p1['packet_id']}.json"), "r") as f:
    recovered_pkt = json.load(f)

from server import duckdb_query
re_res_raw = duckdb_query(
    query="SELECT COUNT(*) FROM read_parquet('/data/geox/derived/well_intervals.parquet');",
    dataset_id="geox_well_intervals_v1"
)
re_res = json.loads(re_res_raw)
original_result_hash = recovered_pkt["evidence"]["tool_calls"][0]["result_hash"]
replay_result_hash = f"sha256:{re_res['result_hash']}"

assert original_result_hash == replay_result_hash, f"Replay mismatch: {original_result_hash} != {replay_result_hash}"
print(f"[PASS] Test 7: Full Replay Reproducibility drill PASSED (Result Hash exact match: {replay_result_hash[:16]}...)")

print("=== ALL 7 P1-C.1 INTEGRITY & REPLAY TESTS PASSED ===")
