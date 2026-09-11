import sys
import os
import json

# Ensure path is included
sys.path.insert(0, '/root/AAA/mcp/duckdb_enclave')
from server import duckdb_query, duckdb_describe, duckdb_list_approved_datasets

print("=== RUNNING DUCKDB ENCLAVE VALIDATION SUITE ===")

# Test 1: Valid Read-Only Query on Parquet
q1 = """
SELECT 
    well_id, 
    formation, 
    COUNT(*) AS sample_count, 
    AVG(gr_api) AS avg_gr, 
    MIN(md_m) AS top_md, 
    MAX(md_m) AS base_md 
FROM read_parquet('/data/geox/derived/well_intervals.parquet')
GROUP BY well_id, formation;
"""
res1 = json.loads(duckdb_query(q1, dataset_id="well_intervals"))
assert res1["status"] == "SUCCESS", f"Test 1 Failed: {res1}"
assert res1["data"]["row_count"] == 1, f"Expected 1 row, got {res1['data']['row_count']}"
print("[PASS] Test 1: Valid Parquet Aggregation Query succeeded!")

# Test 2: Row Truncation Test (Generating 1000 rows, should cap at 500)
q2 = "SELECT i FROM range(1, 1001) t(i);"
res2 = json.loads(duckdb_query(q2))
assert res2["status"] == "SUCCESS"
assert res2["data"]["row_count"] == 500, f"Expected 500 rows, got {res2['data']['row_count']}"
assert res2["data"]["truncated"] is True, "Expected truncated=True"
print("[PASS] Test 2: Row Truncation (500 limit) verified!")

# Test 3: Path Containment Denial (Forbidden Root /etc/passwd)
q3 = "SELECT * FROM read_csv('/etc/passwd');"
res3 = json.loads(duckdb_query(q3))
assert res3["status"] == "DENIED", f"Expected DENIED, got {res3['status']}"
assert "Access Denied" in res3["message"], f"Expected Access Denied message, got {res3['message']}"
print(f"[PASS] Test 3: Blocked unauthorized path /etc/passwd: {res3['message']}")

# Test 4: Path Containment Denial (Forbidden Root /root/.secrets)
q4 = "SELECT * FROM read_csv('/root/.secrets/token.csv');"
res4 = json.loads(duckdb_query(q4))
assert res4["status"] == "DENIED"
assert "Access Denied" in res4["message"]
print(f"[PASS] Test 4: Blocked unauthorized path /root/.secrets: {res4['message']}")

# Test 5: Keyword Denial (INSTALL)
q5 = "INSTALL httpfs;"
res5 = json.loads(duckdb_query(q5))
assert res5["status"] == "DENIED"
assert "forbidden" in res5["message"].lower()
print(f"[PASS] Test 5: Blocked forbidden keyword INSTALL: {res5['message']}")

# Test 6: Keyword Denial (ATTACH)
q6 = "ATTACH 'test.db' AS test;"
res6 = json.loads(duckdb_query(q6))
assert res6["status"] == "DENIED"
assert "forbidden" in res6["message"].lower()
print(f"[PASS] Test 6: Blocked forbidden keyword ATTACH: {res6['message']}")

# Test 7: Keyword Denial (DROP / DDL)
q7 = "DROP TABLE IF EXISTS dummy;"
res7 = json.loads(duckdb_query(q7))
assert res7["status"] == "DENIED"
print(f"[PASS] Test 7: Blocked forbidden keyword DROP: {res7['message']}")

# Test 8: Schema Inspection (duckdb_describe)
res8 = json.loads(duckdb_describe("/data/geox/derived/well_intervals.parquet"))
assert res8["status"] == "SUCCESS"
assert len(res8["schema"]) >= 6
print(f"[PASS] Test 8: Schema inspection verified ({len(res8['schema'])} columns detected)!")

# Test 9: Dataset Listing (duckdb_list_approved_datasets)
res9 = json.loads(duckdb_list_approved_datasets())
assert res9["status"] == "SUCCESS"
assert res9["dataset_count"] >= 2
print(f"[PASS] Test 9: Dataset discovery verified ({res9['dataset_count']} datasets found in approved roots)!")

# Test 10: Audit Log Verification
audit_file = "/data/aaa/audit/duckdb_enclave_audit.jsonl"
assert os.path.exists(audit_file)
with open(audit_file, "r") as f:
    lines = f.readlines()
assert len(lines) >= 7, f"Expected at least 7 audit entries, found {len(lines)}"
last_entry = json.loads(lines[-1])
assert "query_hash" in last_entry
assert "timestamp" in last_entry
print(f"[PASS] Test 10: Audit log verified ({len(lines)} audit events recorded with SHA-256 hashes)!")

print("=== ALL 10 ENCLAVE SECURITY TESTS PASSED ===")
